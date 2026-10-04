# Recuperación de contraseña

Flujo de "olvidé mi contraseña" por email, añadido el 2026-10-04. Sale de un
fallo real: un estudiante no pudo crear la cuenta, peleó con el formulario
varios intentos, y al final descubrió que tampoco había forma de recuperar el
acceso si se le olvidaba la contraseña.

## Lo que pasó realmente (y por qué hay dos arreglos y no uno)

El alumno reportó "la contraseña no cumple los requisitos". El mensaje que vio
era este:

```
String should match pattern '^[a-zA-Z0-9_-]+$'
```

Ese patrón **no es el de la contraseña**: es el del nombre de usuario. Pero el
formulario lo pintaba en un aviso genérico encima de todo, sin decir de qué
campo hablaba, así que el alumno dedujo lo único que el formulario nombra como
"requisitos" y estuvo cambiando la contraseña intento tras intento mientras el
campo que fallaba era otro.

La cadena completa:

1. `schemas/auth.py` ponía las reglas en `Field(pattern=..., min_length=...)`,
   cuyo mensaje lo escribe Pydantic en inglés.
2. El 422 de FastAPI sí decía en `loc` qué campo era.
3. `authStore.ts` se quedaba con `detail[0].msg` y **tiraba el `loc`**.
4. `Register.tsx` lo pintaba en un banner único, lejos de cualquier campo.
5. El formulario no enseñaba las reglas en ningún momento.

Por eso el trabajo son dos cosas: que el registro explique qué falla, y que
exista recuperación.

## Arreglo 1 — el registro dice qué campo falla

- Las reglas se validan a mano en `schemas/auth.py` (`validar_username`,
  `validar_password`) en vez de con constraints de `Field`, para controlar el
  texto. El `loc` del 422 sigue nombrando el campo.
- `main.py` tiene un handler de `RequestValidationError` que quita el prefijo
  `"Value error, "` y, sobre todo, el `input` que Pydantic mete en cada error:
  en `/auth/register` ese `input` era **la contraseña en claro viajando de
  vuelta en el cuerpo del 422**, que acaba en logs y en cualquier proxy del
  camino.
- `services/erroresApi.ts` conserva el `loc` y agrupa `{campo: mensaje}`.
  `ErrorDeApi` lo transporta hasta el formulario.
- `Register.tsx` pinta cada mensaje dentro de su campo, enseña las reglas de
  usuario y contraseña antes de enviar (con palomitas en vivo), y borra el
  error de un campo en cuanto se corrige.
- El rate limit de `/auth/register` pasó de **3/hora a 10/hora**: tres intentos
  dejaban fuera una hora a quien se equivocara tres veces.

Regresión cubierta en `tests/test_registro_mensajes.py`.

## Arreglo 2 — recuperación por email

### Endpoints

| Endpoint | Respuesta | Límite |
|---|---|---|
| `POST /api/v1/auth/password-reset/request` | **204 siempre** | 10/hora por IP |
| `POST /api/v1/auth/password-reset/confirm` | 204, o 400 si el token no sirve | 10/hora por IP |

`request` responde 204 exista o no la cuenta, a propósito: si dijera "no hay
ninguna cuenta con ese email", el formulario sería un comprobador de qué
direcciones están registradas. Tampoco distingue si el correo llegó a salir.

`confirm` sí responde 400 con el motivo: quien llega con un enlace caducado
necesita saberlo para pedir otro, y el token no revela a qué cuenta pertenece.

### El token

`secrets.token_urlsafe(32)`, guardado **hasheado con SHA-256** (migración
`0017`, tabla `password_reset_tokens`). En la tabla nunca hay un token
utilizable: quien leyera un volcado de la base no se lleva un pase a las
cuentas que pidieron recuperación.

SHA-256 y no bcrypt porque el token hay que *buscarlo* por su valor, y con
bcrypt habría que recorrer todas las filas probando una a una. Es seguro aquí
porque el token no es una contraseña elegida por una persona, sino 32 bytes de
CSPRNG.

Propiedades:

- **Un solo uso** — `used_at` se rellena al canjearlo.
- **Caduca** — `PASSWORD_RESET_TOKEN_TTL_MINUTES`, por defecto 60.
- **Pedir otro invalida el anterior** — si no, cada petición dejaría otra llave
  viva suelta en otro buzón.
- **Un correo cada 2 minutos como mucho por usuario** (`ESPERA_ENTRE_ENVIOS`).
  El rate limit del endpoint es por IP y no frena a quien pida el reset de una
  víctima desde varias; este sí, porque cuelga del usuario destino.
- **Canjearlo revoca los refresh tokens del usuario.** Es parte del arreglo, no
  un extra: si alguien se había metido en la cuenta, cambiar la contraseña sin
  echarlo lo dejaría dentro con su sesión viva.

### Por qué esta tabla NO lleva RLS

Las demás tablas por usuario tienen Row Level Security desde la migración
`0004`, con políticas que filtran por `current_setting('app.current_user_id')`.
Esa variable la setea `get_current_user` a partir del JWT.

Todo el flujo de recuperación ocurre **sin sesión iniciada** —justamente porque
el usuario no puede entrar—, así que no hay `app.current_user_id` que setear y
un `FORCE ROW LEVEL SECURITY` dejaría la tabla ilegible para el propio backend.
La defensa aquí es el diseño del token: hasheado, de un solo uso y con
caducidad.

## El envío del correo

`services/email_provider.py`, mismo patrón que `llm_provider.py`: varios
proveedores reales intercambiables y un stub.

Hay **tres** y no uno porque ninguno garantiza que te deje abrir la cuenta.
Esto no es teórico: el primer intento con Brevo se quedó atascado en su
verificación por SMS —los códigos llegaban pero la web los daba por
incorrectos—, con el flujo entero ya terminado y esperando solo una clave.
Cambiar de proveedor es `EMAIL_PROVIDER`, no un cambio de código.

| Proveedor | Gratis | Pega conocida |
|---|---|---|
| **SendGrid** | 100/día, sin caducidad | 2FA obligatorio (vale app de autenticación, no hace falta SMS) |
| **Mailjet** | 200/día (6.000/mes) | revisa cuentas con remitente de Gmail |
| **Brevo** | 300/día | **exige verificar el teléfono por SMS** antes de dar la clave API |
| `console` | — | no envía: escribe el enlace en el log. Dev y tests |

Todos van por **API HTTP, nunca SMTP**: Render free bloquea los puertos
salientes 25/465/587, así que un `smtplib` funcionaría en local y se colgaría
hasta el timeout en producción — el peor modo de fallo posible, el mismo perfil
que el tutor caído del 2026-09-15.

Comparten `_ProveedorHttp`, que hace el envío, el timeout y el tratamiento de
errores. Cada proveedor solo define su URL, sus cabeceras y la forma de su
payload. **Ninguno lanza nunca**: un rechazo o una caída de red devuelven
`False` y quedan en el log, porque si lanzaran, un timeout del proveedor
tumbaría el endpoint de recuperación. Hay test de las dos cosas para los tres.

### Añadir un cuarto proveedor

Heredar de `_ProveedorHttp`, definir `nombre`, `api_url`, `_cabeceras()` y
`_payload()` (y `_auth()` si usa Basic auth, como Mailjet), y añadir su rama en
`get_email_provider`. Unas 30 líneas. Los tests de forma de payload en
`tests/test_email_provider.py` son la plantilla.

### Variables de entorno

| Variable | Valor | Nota |
|---|---|---|
| `EMAIL_PROVIDER` | `sendgrid` \| `mailjet` \| `brevo` \| `console` | por defecto `console` |
| `SENDGRID_API_KEY` | secreto | solo si usas SendGrid |
| `MAILJET_API_KEY` + `MAILJET_API_SECRET` | secretos | Mailjet necesita **las dos** |
| `BREVO_API_KEY` | secreto | solo si usas Brevo |
| `EMAIL_FROM` | remitente | **tiene que estar verificado en el proveedor** |
| `EMAIL_FROM_NAME` | `PyCode Platform` | |
| `FRONTEND_URL` | `https://pycode-platform.vercel.app` | base del enlace del correo |
| `PASSWORD_RESET_TOKEN_TTL_MINUTES` | `60` | |

Si al proveedor elegido le faltan credenciales **no se revienta**: se cae al
`ConsoleProvider` y lo deja en el log. Que falte una variable de entorno no
puede tumbar el registro ni el login.

**`FRONTEND_URL` es la que más fácil se olvida**: por defecto vale
`http://localhost:5173`, así que sin ponerla en Render los correos de
producción llevarían a los alumnos a su propio ordenador.

### Puesta en marcha (SendGrid, la vía recomendada)

1. Cuenta en [sendgrid.com](https://signup.sendgrid.com) — plan Free, 100/día.
2. Activar el 2FA que pide la cuenta **con una app de autenticación** (Google
   Authenticator, Authy). Evita depender del SMS.
3. **Settings → Sender Authentication → Single Sender Verification**: verificar
   la dirección que se use como `EMAIL_FROM`. Llega un correo con un enlace.
   Esto es lo que permite enviar sin dominio propio.
4. **Settings → API Keys → Create API Key**, permiso *Mail Send* → `SENDGRID_API_KEY`.
5. En Render: Settings → Environment, las variables de la tabla, y redesplegar.
   Ojo: la copia de la env var que vive en Render gana sobre `render.yaml`.

Con **Mailjet** el camino es el mismo cambiando los nombres: *Account settings
→ Sender domains & addresses* para verificar el remitente, y *API Key
Management* para sacar **las dos** claves.

### Enviar desde un Gmail

Funciona, pero los correos tienen más papeletas de caer en spam: `gmail.com` no
es un dominio tuyo, así que no puedes firmarlos (DKIM) y desde 2024 Google,
Yahoo y Microsoft son estrictos con eso. El proveedor avisará con un triángulo
naranja en DKIM/DMARC — **no tiene arreglo con un Gmail**, no pierdas tiempo.
Para arrancar y validar con los primeros estudiantes, sirve. Un dominio propio
(10-15 € al año) lo elimina del todo.

### Diagnóstico

Si un alumno dice que no le llega el correo, el orden de sospecha es:

1. ¿Están las credenciales en Render? Sin ellas el backend **no falla**: escribe
   el enlace en el log y responde 204 igual. Buscar
   `email_sin_credenciales_usando_consola` en los logs de Render.
2. ¿Está `EMAIL_FROM` verificado en el proveedor? Si no, rechaza con 400 y el
   log dice `email_rechazado` con el motivo del proveedor en `cuerpo`.
3. ¿Pidió dos enlaces seguidos? El segundo no se envía
   (`password_reset_throttled` en el log).
4. ¿Cuota diaria agotada? También sale como `email_rechazado`.
5. Carpeta de spam.

Los cuatro primeros son invisibles para el alumno a propósito —el endpoint
responde 204 siempre—, así que **los logs son el único sitio donde se ven**.

## Archivos

```
backend/
  alembic/versions/0017_password_reset_tokens.py
  app/models/password_reset.py
  app/services/email_provider.py
  app/services/password_reset_service.py
  app/schemas/auth.py                        (validadores en español)
  app/api/v1/endpoints/auth.py               (los dos endpoints)
  app/main.py                                (handler de 422 sin eco)
  tests/test_password_reset.py
  tests/test_registro_mensajes.py
frontend/src/
  services/erroresApi.ts
  pages/ForgotPassword.tsx
  pages/ResetPassword.tsx
  pages/Register.tsx
  pages/Login.tsx                            (enlace "¿Olvidaste tu contraseña?")
  App.tsx                                    (/forgot-password, /reset-password)
```
