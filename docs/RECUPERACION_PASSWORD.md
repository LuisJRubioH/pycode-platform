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

`services/email_provider.py`, mismo patrón que `llm_provider.py`: un proveedor
real y un stub.

- **`BrevoProvider`** — API HTTP (`https://api.brevo.com/v3/smtp/email`).
  Se usa API y **no SMTP** porque Render free bloquea los puertos salientes
  25/465/587: un `smtplib` funcionaría en local y se colgaría hasta el timeout
  en producción, que es el peor modo de fallo posible (el mismo perfil que el
  tutor caído del 2026-09-15).
- **`ConsoleProvider`** — sin `BREVO_API_KEY`, escribe el enlace en el log en
  vez de enviarlo. Es lo que corre en desarrollo y en los tests, así que la
  suite no toca la red.

### Variables de entorno

| Variable | Valor | Nota |
|---|---|---|
| `EMAIL_PROVIDER` | `brevo` \| `console` | |
| `BREVO_API_KEY` | secreto | sin ella se cae al `ConsoleProvider` |
| `EMAIL_FROM` | remitente | **tiene que estar verificado en Brevo** |
| `EMAIL_FROM_NAME` | `PyCode Platform` | |
| `FRONTEND_URL` | `https://pycode-platform.vercel.app` | base del enlace del correo |
| `PASSWORD_RESET_TOKEN_TTL_MINUTES` | `60` | |

**`FRONTEND_URL` es la que más fácil se olvida**: por defecto vale
`http://localhost:5173`, así que sin ponerla en Render los correos de
producción llevarían a los alumnos a su propio ordenador.

### Puesta en marcha en Brevo

1. Crear cuenta en [brevo.com](https://www.brevo.com) (plan gratis: 300
   correos/día).
2. **Senders, Domains & Dedicated IPs → Senders → Add a sender**: verificar la
   dirección que se vaya a usar como `EMAIL_FROM`. Brevo manda un correo de
   confirmación a esa dirección. Esto permite enviar desde un email individual
   sin tener dominio propio — es el motivo de elegir Brevo frente a Resend, que
   exige dominio con DNS verificado.
3. **SMTP & API → API Keys**: generar una clave v3 → `BREVO_API_KEY`.
4. En Render: Settings → Environment, añadir las variables de la tabla y
   redesplegar. Ojo con la nota de `CLAUDE.md`: la copia de la env var que vive
   en Render gana sobre `render.yaml`.

### Diagnóstico

Si un alumno dice que no le llega el correo, el orden de sospecha es:

1. ¿Está `BREVO_API_KEY` en Render? Sin ella el backend no falla: escribe el
   enlace en el log y responde 204 igual. Buscar `email_no_enviado_sin_proveedor`
   en los logs de Render.
2. ¿Está `EMAIL_FROM` verificado en Brevo? Si no, Brevo rechaza con 400 y el
   log dice `email_rechazado` con el motivo de Brevo en `cuerpo`.
3. ¿Pidió dos enlaces seguidos? El segundo no se envía
   (`password_reset_throttled` en el log).
4. Carpeta de spam.

Los tres primeros son invisibles para el alumno a propósito —el endpoint
responde 204 siempre—, así que **los logs son el único sitio donde se ve**.

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
