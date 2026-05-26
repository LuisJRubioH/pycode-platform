# Spec — ELO multidominio + progresión de calidad de código

**Fecha:** 2026-05-26 · **Fase:** 1 (extensión) · **Estado:** aprobado, en implementación.

## Objetivo

1. Reemplazar el ELO único global por **ratings independientes** por *(actividad, categoría)*:
   Puzzles (Python/NumPy/Pandas), Entrevista, Retos (por dificultad) — cada uno con su
   rango, racha e historial propios.
2. Medir y graficar la **progresión de calidad de código y lógica** combinando el evaluador
   socrático (que ya persiste `logic_score`/`general_score`) con **análisis estático** del código.

## Decisiones (confirmadas con el usuario)

- **Granularidad ELO:** por actividad **y** por categoría temática.
- **ELO de retos:** por dificultad al auto-marcar (rápido; se asume gameable; ELO solo en la
  1ª completación, `uncomplete` revierte).
- **Calidad/lógica:** reusar `logic_score`/`general_score` del evaluador **+** análisis estático
  (`ast`, sin ejecutar código).

## Estado actual (lo que se cambia)

- ELO único en `UserProfile.elo_rating` (+ peak/rank/streak). `EloHistory` = una sola línea
  temporal. Puzzles y Entrevista ya comparten ese ELO; "interview" es `Puzzle.category="interview"`.
- Retos (`CodingChallenge`): sin ELO, solo auto-marcado (`ChallengeCompletion`).
- Evaluador: `CodeEvaluation.verdict` ya guarda `logic_score`/`general_score`; nadie los grafica.
- `process_attempt` (en `elo_service.py`) es una función pura y se conserva intacta; solo cambia
  *qué rating* lee/escribe el endpoint.

## Modelo de datos

### `elo_ratings` (nueva) — una fila por *(user, domain, scope)*

Guardamos las **hojas**; los agregados (overall por dominio, global) se calculan al leer.

```
id · user_id (FK CASCADE) · domain ("puzzle"|"challenge") · scope
("python"/"numpy"/"pandas"/"interview" | "easy"/"medium"/"hard")
· elo_rating · elo_peak · rank · attempts · correct
· streak_current · streak_best · last_activity
UniqueConstraint(user_id, domain, scope) · Index(user_id, domain) · RLS Postgres
```

**Lazy-init:** la primera vez que un usuario toca una categoría, su rating se crea heredando el
`UserProfile.elo_rating` global actual (continuidad — nadie se resetea a 1000).

### `EloHistory` (modificada)

Gana columna `domain` (la `category` existente actúa de scope). Filas viejas → `domain="puzzle"`.
Permite un timeline por track.

### `code_quality_snapshots` (nueva)

```
id · user_id (FK CASCADE) · source ("evaluation"|"exercise"|...) · reference_id (nullable)
· logic_score (nullable) · general_score (nullable) · static_score (0-100, nullable)
· metrics (JSON: complejidad, n_funciones, largo_func, docstrings, naming) · created_at
RLS Postgres
```

### `UserProfile.elo_rating`

Se conserva como **overall global denormalizado** para no romper `/elo/profile` ni la UI vieja
durante la transición.

## Piezas (cada una = 1 commit verificado; pytest + black + flake8 + frontend lint/build verdes)

| Pieza | Alcance | Migración |
|---|---|---|
| **I — Core multi-ELO** | `EloRating` + `EloHistory.domain`; helpers `get_or_init_rating`/`apply_attempt_to_rating`; refactor `/elo/attempt` para escribir el rating de `puzzle:<category>` + actualizar overall global. | 0010 |
| **J — ELO de retos** | `/challenges/{id}/complete` otorga ELO a `challenge:<difficulty>` en 1ª completación (revertir en `uncomplete`); usa `_difficulty_elo`. | — |
| **K — Perfil multi-ELO + UI** | `GET /elo/ratings` (todas las tracks + agregados por dominio + global); ELODashboard y Dashboard muestran grid de tracks; cada página muestra su track. | — |
| **L — Análisis estático** | `code_quality_service.py` (métricas `ast`, sin ejecutar → `static_score`); `CodeQualitySnapshot`; `evaluate` guarda snapshot (logic+general+static). | 0011 |
| **M — Progresión calidad/lógica + UI** | `GET /progress/code-quality` (serie temporal + medias móviles); panel "Calidad de código" en Dashboard. | — |

## Tests clave por pieza

- **I:** python ≠ numpy ≠ interview divergen; history por track; lazy-init hereda global;
  aislamiento cross-user; `/elo/profile` sigue verde.
- **J:** otorga 1 vez, idempotente, por dificultad; `uncomplete` revierte.
- **K:** shape de `/elo/ratings`, agregados correctos, auth.
- **L:** métricas deterministas para un código dado; snapshot persiste; análisis no ejecuta código.
- **M:** serie ordenada, medias móviles, aislamiento cross-user.

## Riesgos / invariantes

- **Continuidad** vía lazy-init desde el global.
- **Análisis estático = parsing, NO ejecución** (`ast.parse`, ya usado en `/execute/validate`).
- **Backward-compat:** `/elo/profile` + UI vieja siguen con el overall global toda la transición.
- Nuevas tablas con **RLS Postgres** + filtro por `user_id` en la capa de app (segunda línea).

## Secuencia

I → J → K (cierra ELO separado) · luego L → M (cierra calidad). I y L son independientes;
K depende de I+J; M depende de L.
