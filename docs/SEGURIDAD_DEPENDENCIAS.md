# Triaje de alertas de dependencias (Dependabot)

Criterio de priorización P1-P4 de PyCode y la clasificación de las alertas
abiertas. **Triaje: 2026-09-03 (35 alertas). Aplicado el 2026-09-13**: de 34
abiertas ese día quedan las 2 de `react-router` aceptadas como P4 (ver
"Estado tras aplicar", al final).

Regenerar el inventario:

```bash
gh api repos/LuisJRubioH/pycode-platform/dependabot/alerts --paginate \
  -q '.[] | select(.state=="open") | [.number, .security_advisory.severity,
      .dependency.package.ecosystem, .dependency.package.name,
      .dependency.scope,
      (.security_vulnerability.first_patched_version.identifier // "sin parche")]
      | @tsv'
```

## El criterio

La severidad CVSS mide el impacto **del fallo en abstracto**, no el riesgo **en
esta aplicación**. La prioridad sale de cruzar tres preguntas:

1. ¿El código vulnerable llega a producción, o solo al build/CI?
2. ¿Puede alcanzarlo una entrada que no controlamos nosotros?
3. ¿Hay parche, y bumpear cuesta algo?

| | Definición | Ventana |
|---|---|---|
| **P1** | Alcanzable desde entrada no confiable **en producción**, con impacto sobre datos o sesión de un alumno. La acción puede ser un bump o una mitigación en código. | Inmediata |
| **P2** | Llega a producción, pero explotarlo exige condiciones que hoy no se dan; **o** el parche es un bump menor de riesgo bajo. | Siguiente tanda |
| **P3** | Solo build, test o CI. No viaja al navegador del alumno ni al contenedor de Render. Se agrupan y se bumpean juntos. | Higiene, sin prisa |
| **P4** | No alcanzable en esta arquitectura, **o** sin parche disponible. Se documenta con el disparador que lo reabriría. | Revisar al cambiar el contexto |

**Por qué la severidad sola no sirve aquí**: la única alerta *critical* del repo
(CVSS 9.8) es `vitest` #56, y solo se explota **con el servidor de Vitest UI
escuchando**. Nunca corremos `vitest --ui`: CI usa `vitest run`. Es P3. En
cambio, las de `react-router` son *medium* y son las que sí viajan al navegador
del alumno.

## Hechos de alcance verificados en el código

- **Ningún módulo del backend importa PIL** (`from PIL` / `import PIL`: 0
  resultados) y **no hay un solo endpoint que acepte ficheros**
  (`UploadFile`/`File(`: 0 resultados). `pillow==12.2.0` está pineado porque
  `reportlab` lo pide para los certificados PDF, que se generan desde plantillas
  propias. **Ninguna imagen de origen no confiable llega a Pillow.**
- El frontend es una **SPA sin SSR**, así que el fallo de hidratación SSR de
  `react-router` (#93) no tiene ruta de ejecución.
- **Ninguna navegación toma su destino de entrada del usuario**: todos los
  `navigate()` usan rutas literales o ids numéricos, y el único
  `window.location.href` es `'/login'`. Los open redirect (#92, #94) no tienen
  por dónde entrar hoy. Revisado de nuevo el 2026-09-13 al añadir el modo reto
  del editor: `?lesson=`, `?exercise=` y `?challenge=` se leen como **ids para
  llamar a la API**, nunca como destino de `navigate()` o `<Link>`.
- `nanoid`, `postcss` y `postcss-selector-parser` los marca Dependabot como
  `runtime`, pero en este repo **solo existen bajo la cadena de PostCSS/Tailwind**
  (`npm ls nanoid` → únicamente vía `postcss`): son build-time. La etiqueta de
  Dependabot describe el `package.json` del paquete, no nuestro despliegue.
- `dompurify` sí se empaqueta al navegador: entra por `@monaco-editor/react` →
  `monaco-editor` y además como dependencia directa.

## Clasificación

**P1 — ninguna.** Ninguna alerta abierta cumple hoy las tres condiciones.

### P2 — siguiente tanda (15 alertas)

| Paquete | Alertas | Sev. máx | Parche | Nota |
|---|---|---|---|---|
| `pillow` | 13 (#75, #79-#90) | high (8.2) | `12.3.0` | Un solo bump `12.2.0 → 12.3.0` cierra las 13. Sin entrada de imágenes no confiables, pero es el mejor ratio esfuerzo/ruido del repo. |
| ~~`dompurify`~~ | ~~2 (#91, #98)~~ | ~~medium~~ | ~~`3.4.13`~~ | **APLICADO 2026-09-03**: `^3.4.11 → ^3.4.13` en la dependencia directa y en `overrides` (resuelve a 3.4.14). El override es lo que arrastra la copia que trae `monaco-editor`; sin tocarlo el bump no sirve de nada. |

### P3 — higiene de build/CI (17 alertas)

Nada de esto viaja al alumno ni al contenedor de Render; explotarlo exigiría que
un atacante ya controlase la entrada del build.

| Paquete | Alertas | Sev. máx | Parche |
|---|---|---|---|
| `vitest` | #56 | critical (9.8) | `3.2.6` |
| `vite` | #13, #72, #73 | high | `6.4.3` |
| `js-yaml` | #74, #78, #100 | high | `4.3.1` |
| `brace-expansion` | #76, #77 | high | `1.1.16` / `5.0.7` |
| `browserslist` | #107 | high | `4.28.7` |
| `postcss` | #96, #103 | high | `8.5.23` |
| `nanoid` | #102, #104 | high | `3.3.18` |
| `postcss-selector-parser` | #106 | low | `6.1.3` |
| `esbuild` | #1 | medium | `0.25.0` |
| `@babel/core` | #71 | low | `7.29.6` |

### P4 — aceptadas y anotadas (3 alertas)

| Alerta | Paquete | Por qué |
|---|---|---|
| #93 | `react-router` | Inyección vía `deserializeErrors()` en hidratación **SSR**. La app es SPA pura: no hay hidratación de servidor. |
| #94 | `react-router` | Open redirect por backslash en `<Link>`/`useNavigate`. Ningún destino de navegación sale de entrada del usuario. |
| ~~#92~~ | `react-router-dom` | Open redirect → XSS. **Cerrada el 2026-09-13**: sí había parche en la línea 6.x (`6.30.6`, sin cambios de API), aplicado. Afectaba a 6.30.2–6.30.5. |

> **Disparador que sube estas tres a P1**: en cuanto se añada cualquier
> navegación cuyo destino venga de la URL o del usuario (un `?next=`, un
> `returnTo`, un deep-link de vuelta tras login). Ahí la migración a
> `react-router` 7.x deja de ser opcional. Revisar esta nota al tocar el routing.

## Acciones (aplicadas el 2026-09-13 salvo la 4)

1. ~~`pillow` `12.2.0 → 12.3.0`~~ — **hecho** (`requirements.txt` y
   `requirements.lock`). Cierra 13 alertas; los tests de certificados (PDF con
   reportlab) pasan.
2. ~~`dompurify`~~ — hecho, ver arriba.
3. ~~Tanda de devDependencies (P3)~~ — **hecho**, en dos commits:
   - `npm audit fix` sin `--force` para las transitivas: `js-yaml`,
     `brace-expansion`, `browserslist`, `baseline-browser-mapping`, `postcss`,
     `nanoid`, `@babel/core`.
   - `vite` 5 → 6.4.3 y `vitest` 1 → 3.2.7 (cierra la crítica #56 y `esbuild`),
     verificado con Pyodide real en dev y en `vite preview`.
4. ~~Dejar `react-router` en 6.30.4~~ — subido a **6.30.6** (cierra #92). #93 y #94
   solo tienen parche en 7.18, que es una migración mayor: se quedan en 6.x
   mientras no se cumpla el disparador de arriba. **Releer este documento**
   cuando se toque el routing.

CI ya corre `pip-audit` y `npm audit` en el job `audit`, y Dependabot abre PRs
semanales para pip, npm y actions.

## Estado tras aplicar (2026-09-13)

Quedan **2 alertas abiertas**, las dos aceptadas, y ninguna llega al alumno por
una vía explotable hoy:

| Aviso | Paquete | Prioridad | Por qué se queda |
|---|---|---|---|
| #93, #94 | `react-router` | P4 | Solo se parchean en 7.18 (migración mayor) y no tienen alcance: ver arriba. |

Tras el push aparecieron #112 y #113 (GHSA-82fw-gwwq-j7x9, path traversal en
los mocks de Vitest, solo tests): se cerraron el mismo día subiendo `vitest` a
**4.1.11**, que admite Vite 6. `npm audit` sugería Vitest 5, pero el parche ya
está en la 4.1.11.

Gotcha al subir Vite: la **primera** carga en frío del servidor de desarrollo
optimiza dependencias y recarga la página; una prueba automática que empiece
justo entonces puede fallar sin que haya un error real.

## Triaje 2026-11-03 (`npm audit` en la laptop nueva)

Al reinstalar el frontend con `npm ci`, `npm audit` dio **25** avisos
(1 critical, 3 high, 21 moderate). Se publicaron advisories nuevos después del
2026-09-13 para versiones que ya teníamos.

### Aplicado el 2026-11-03 (sin versiones mayores)

| Paquete | Antes → después | Severidad | Por qué ahora |
|---|---|---|---|
| `dompurify` | 3.4.14 → **3.4.17** (directa y `overrides`) | critical | Llega al navegador del alumno vía `monaco-editor`. El parche es un bump de patch: P2 "bump menor de riesgo bajo". |
| `vite` | 6.4.3 → **6.4.5** | high | `launch-editor` en Windows, que es justo el equipo de desarrollo. Solo dev, pero el parche es de patch. |
| `vitest` / `@vitest/mocker` | 4.1.11 → **4.1.12** | moderate | Solo tests. |
| `source-map-js`, `brace-expansion` | transitivas, `npm audit fix` | high | Solo build. |

Verificado tras el cambio: `npm run build`, `npm run test -- --run` (71/71) y
`npm run lint` en verde; `npm audit` queda en **0 critical, 0 high, 19 moderate**.
Comprobado otra vez el disparador de `react-router`: todos los `navigate()` y
`<Link to>` van a rutas literales con ids; `ResetPassword` navega a `'/login'`
fijo. No se cumple.

### Plan para las 19 moderadas restantes

Ninguna tiene parche sin versión mayor, y ninguna es P1.

| Grupo | Avisos | Alcance | Prioridad | Acción |
|---|---|---|---|---|
| **Cadena de ESLint 8**: `eslint`, `@eslint/eslintrc`, `@humanwhocodes/config-array`, `@eslint-community/eslint-utils`, `@typescript-eslint/*` (5), `eslint-plugin-react-refresh`, `file-entry-cache`, `flat-cache`, `rimraf`, `glob`, `minimatch` | 15 | Solo lint, local y CI. No viaja al navegador ni a Render. | P3 | Migrar a **ESLint 9 + flat config** (`eslint.config.js`), `eslint-plugin-react-hooks` 5+ y `eslint-plugin-react-refresh` 0.5 (Dependabot ya tiene ramas abiertas para estos dos). Una rama propia; criterio de cierre: `npm run lint` con `--max-warnings 0` sin desactivar reglas para pasar. |
| **`@tailwindcss/typography` → `postcss-selector-parser` 6.0.10** | 2 | Build CSS con selectores propios, no entrada externa. | P4 | Sin parche: la 0.5.20 es la última y fija 6.0.10. `npm audit` propone *bajar* a 0.5.4, que es peor. Reabrir cuando salga una typography que suba la dependencia, o al migrar a Tailwind 4. |
| **`react-router` / `react-router-dom` 6.30.6** | 2 | Llega al navegador, pero sin ruta explotable (SPA sin SSR; ninguna navegación usa destino del usuario). | P4 | Siguen siendo #93/#94. Migrar a 7.18+ **solo** si se cumple el disparador de arriba, o como tarea propia con recorrido E2E del editor (modo lección y modo reto). |

Orden propuesto: (1) migración de ESLint 9, que se lleva 15 de 19 de una vez;
(2) revisar typography y react-router en cada triaje, sin tocarlos mientras no
cambie su condición.
