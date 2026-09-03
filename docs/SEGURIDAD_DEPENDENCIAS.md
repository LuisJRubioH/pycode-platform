# Triaje de alertas de dependencias (Dependabot)

Criterio de priorización P1-P4 de PyCode y la clasificación de las alertas
abiertas. **Snapshot: 2026-09-03, 35 alertas abiertas.** Nada de esto está
aplicado todavía: es el triaje, no el parche.

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
  por dónde entrar hoy.
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
| `dompurify` | 2 (#91, #98) | medium | `3.4.13` | Viaja al navegador. Un bypass del saneado sería self-XSS (el alumno contra su propio editor), no cross-user. |

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
| #92 | `react-router-dom` | Open redirect → XSS. Igual que #94 **y además sin parche en la línea 6.x**: el arreglo está en 7.x, que es una migración con cambios de API. |

> **Disparador que sube estas tres a P1**: en cuanto se añada cualquier
> navegación cuyo destino venga de la URL o del usuario (un `?next=`, un
> `returnTo`, un deep-link de vuelta tras login). Ahí la migración a
> `react-router` 7.x deja de ser opcional. Revisar esta nota al tocar el routing.

## Acciones propuestas (sin aplicar)

1. `pillow` `12.2.0 → 12.3.0` en `requirements.txt` + regenerar `requirements.lock`.
   Cierra 13 de 35 alertas con un cambio de una línea.
2. `dompurify` al `3.4.13` como dependencia directa.
3. Una tanda única de devDependencies (P3) con `npm audit fix` y `npm run build`
   + `npm run test` en verde. `vite` y `vitest` son los que más riesgo de rotura
   tienen: van en su propio commit.
4. Dejar `react-router` en 6.30.4 y **releer este documento** cuando se toque el
   routing.

CI ya corre `pip-audit` y `npm audit` en el job `audit`, y Dependabot abre PRs
semanales para pip, npm y actions.
