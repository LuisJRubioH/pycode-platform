import React, { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { CheckCircle2, Circle, ArrowRight, Trophy } from 'lucide-react'
import { api } from '../services/api'

interface CompetencyLesson {
  id: number
  title: string
  difficulty: string
  completed: boolean
  exercises_completed: number
  exercises_total: number
}

interface Competency {
  category: string
  lessons_total: number
  lessons_completed: number
  exercises_total: number
  exercises_completed: number
  lessons: CompetencyLesson[]
}

const CATEGORY_LABELS: Record<string, string> = {
  fundamentos: 'Fundamentos',
  'control-flujo': 'Control de flujo',
  'estructuras-datos': 'Estructuras de datos',
  funciones: 'Funciones',
  'python-moderno': 'Python moderno',
  'io-sistema': 'I/O y sistema',
  tooling: 'Tooling',
  oop: 'POO',
  concurrencia: 'Concurrencia',
  stdlib: 'Stdlib',
  testing: 'Testing',
  performance: 'Performance',
  otros: 'Otros',
}

const DIFFICULTY_LABEL: Record<string, string> = {
  beginner: 'Principiante',
  intermediate: 'Intermedio',
  advanced: 'Avanzado',
}

const ORDER: string[] = [
  'fundamentos',
  'control-flujo',
  'estructuras-datos',
  'funciones',
  'python-moderno',
  'io-sistema',
  'tooling',
  'oop',
  'concurrencia',
  'stdlib',
  'testing',
  'performance',
]

const labelFor = (key: string) =>
  CATEGORY_LABELS[key] || key.replace(/-/g, ' ').replace(/^\w/, (c) => c.toUpperCase())

const Competencies: React.FC = () => {
  const [items, setItems] = useState<Competency[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false
    const load = async () => {
      setLoading(true)
      setError('')
      try {
        const res = await api.get('/progress/competencies')
        if (!res.ok) {
          if (!cancelled) setError('No pudimos cargar tu mapa de competencias.')
          return
        }
        const data = (await res.json()) as Competency[]
        if (!cancelled) setItems(data)
      } catch (loadErr) {
        console.error('Error cargando competencias:', loadErr)
        if (!cancelled) setError('Error de red al cargar las competencias.')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [])

  const sorted = useMemo(() => {
    const indexOf = (cat: string) => {
      const i = ORDER.indexOf(cat)
      return i === -1 ? ORDER.length : i
    }
    return [...items].sort((a, b) => indexOf(a.category) - indexOf(b.category))
  }, [items])

  const totals = useMemo(() => {
    return items.reduce(
      (acc, c) => ({
        lessons_total: acc.lessons_total + c.lessons_total,
        lessons_completed: acc.lessons_completed + c.lessons_completed,
        exercises_total: acc.exercises_total + c.exercises_total,
        exercises_completed: acc.exercises_completed + c.exercises_completed,
      }),
      {
        lessons_total: 0,
        lessons_completed: 0,
        exercises_total: 0,
        exercises_completed: 0,
      }
    )
  }, [items])

  const overallPct = totals.lessons_total
    ? Math.round((totals.lessons_completed / totals.lessons_total) * 100)
    : 0

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Mapa de competencias</h1>
        <p className="text-slate-600 mt-2">
          Tus avances agrupados por área del Track 1. Cada tarjeta muestra cuántas
          lecciones y ejercicios llevas resueltos.
        </p>
      </div>

      {error && (
        <div className="rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">
          {error}
        </div>
      )}

      {!error && (
        <div className="card p-5">
          <div className="flex items-center gap-3 mb-3">
            <Trophy className="h-5 w-5 text-amber-500" />
            <h2 className="text-lg font-semibold text-slate-900">Progreso global</h2>
          </div>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 text-sm text-slate-600">
            <div>
              <p className="text-xs uppercase tracking-wide text-slate-500">Lecciones</p>
              <p className="text-2xl font-bold text-slate-900">
                {totals.lessons_completed}
                <span className="text-base text-slate-500"> / {totals.lessons_total}</span>
              </p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-wide text-slate-500">Ejercicios</p>
              <p className="text-2xl font-bold text-slate-900">
                {totals.exercises_completed}
                <span className="text-base text-slate-500"> / {totals.exercises_total}</span>
              </p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-wide text-slate-500">Competencias</p>
              <p className="text-2xl font-bold text-slate-900">{items.length}</p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-wide text-slate-500">Avance global</p>
              <p className="text-2xl font-bold text-slate-900">{overallPct}%</p>
            </div>
          </div>
          <div className="mt-4 w-full h-2 bg-slate-100 rounded-full overflow-hidden">
            <div
              className="h-2 bg-emerald-500 transition-all"
              style={{ width: `${overallPct}%` }}
            />
          </div>
        </div>
      )}

      {loading ? (
        <p className="text-sm text-slate-500">Cargando competencias...</p>
      ) : sorted.length === 0 && !error ? (
        <p className="text-sm text-slate-500">
          Aún no hay categorías disponibles. Carga lecciones desde el backend.
        </p>
      ) : (
        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {sorted.map((comp) => {
            const lessonsPct = comp.lessons_total
              ? Math.round((comp.lessons_completed / comp.lessons_total) * 100)
              : 0
            return (
              <article key={comp.category} className="card p-5 flex flex-col">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-lg font-semibold text-slate-900">
                    {labelFor(comp.category)}
                  </h3>
                  <span className="text-xs font-medium text-slate-500">
                    {lessonsPct}%
                  </span>
                </div>
                <p className="text-xs text-slate-500 mb-3">
                  {comp.lessons_completed}/{comp.lessons_total} lecciones ·{' '}
                  {comp.exercises_completed}/{comp.exercises_total} ejercicios
                </p>
                <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden mb-4">
                  <div
                    className={`h-1.5 transition-all ${
                      lessonsPct === 100 ? 'bg-emerald-500' : 'bg-primary-500'
                    }`}
                    style={{ width: `${lessonsPct}%` }}
                  />
                </div>

                <ul className="space-y-2 flex-1">
                  {comp.lessons.map((lesson) => (
                    <li key={lesson.id}>
                      <Link
                        to={`/lessons/${lesson.id}`}
                        className="flex items-start gap-2 group rounded p-1 -m-1 hover:bg-slate-50"
                      >
                        {lesson.completed ? (
                          <CheckCircle2 className="h-4 w-4 text-emerald-600 mt-0.5 flex-shrink-0" />
                        ) : (
                          <Circle className="h-4 w-4 text-slate-300 mt-0.5 flex-shrink-0" />
                        )}
                        <div className="flex-1 min-w-0">
                          <p className="text-sm text-slate-800 group-hover:text-primary-700 truncate">
                            {lesson.title}
                          </p>
                          <p className="text-[11px] text-slate-500">
                            {DIFFICULTY_LABEL[lesson.difficulty] || lesson.difficulty}
                            {lesson.exercises_total > 0 &&
                              ` · ${lesson.exercises_completed}/${lesson.exercises_total} ej.`}
                          </p>
                        </div>
                      </Link>
                    </li>
                  ))}
                </ul>

                {comp.lessons[0] && (
                  <Link
                    to={`/lessons/${comp.lessons.find((l) => !l.completed)?.id ?? comp.lessons[0].id}`}
                    className="mt-4 inline-flex items-center gap-1 text-sm font-medium text-primary-700 hover:text-primary-800"
                  >
                    {comp.lessons_completed === comp.lessons_total
                      ? 'Repasar competencia'
                      : 'Continuar'}
                    <ArrowRight className="h-4 w-4" />
                  </Link>
                )}
              </article>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default Competencies
