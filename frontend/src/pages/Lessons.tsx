import React, { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { BookOpen, Clock, CheckCircle, Circle, Filter, Search } from 'lucide-react'
import { api } from '../services/api'

interface LessonSummary {
  id: number
  title: string
  description: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  category: string
  estimated_duration: number
  progress: number
  status: 'not_started' | 'in_progress' | 'completed'
}

const difficultyLabel: Record<string, string> = {
  beginner: 'Principiante',
  intermediate: 'Intermedio',
  advanced: 'Avanzado',
}

const Lessons: React.FC = () => {
  const [items, setItems] = useState<LessonSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [difficulty, setDifficulty] = useState<'all' | 'beginner' | 'intermediate' | 'advanced'>('all')
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState('all')

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      setError('')
      try {
        const res = await api.get('/lessons/')
        if (!res.ok) {
          setError('No pudimos cargar las lecciones por ahora.')
          setItems([])
          return
        }
        const data = (await res.json()) as LessonSummary[]
        setItems(data || [])
      } catch (loadError) {
        console.error('Error loading lessons:', loadError)
        setError('No pudimos cargar las lecciones por ahora.')
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [])

  const categories = useMemo(() => {
    const unique = Array.from(new Set(items.map((item) => item.category).filter(Boolean)))
    return ['all', ...unique]
  }, [items])

  const filtered = useMemo(() => {
    return items.filter((item) => {
      const byDifficulty = difficulty === 'all' || item.difficulty === difficulty
      const byCategory = category === 'all' || item.category === category
      const term = query.trim().toLowerCase()
      const byQuery =
        !term ||
        item.title.toLowerCase().includes(term) ||
        item.description?.toLowerCase().includes(term) ||
        item.category?.toLowerCase().includes(term)
      return byDifficulty && byCategory && byQuery
    })
  }, [items, difficulty, category, query])

  const completed = items.filter((item) => item.status === 'completed').length
  const progressPercent = items.length ? Math.round((completed / items.length) * 100) : 0

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Lecciones</h1>
        <p className="text-slate-600 mt-2">
          Ruta guiada con teoria de Python y ejercicios para practicar cada tema.
        </p>
      </div>

      {error && (
        <div className="rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">{error}</div>
      )}

      <div className="card p-4 grid md:grid-cols-[1fr,auto,auto] gap-3">
        <div className="relative">
          <Search className="h-4 w-4 absolute left-3 top-3.5 text-slate-400" />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Buscar por titulo, descripcion o categoria..."
            className="w-full pl-9 p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-slate-500" />
          <select
            value={difficulty}
            onChange={(event) => setDifficulty(event.target.value as typeof difficulty)}
            className="p-3 border border-slate-300 rounded-lg bg-white"
          >
            <option value="all">Todos los niveles</option>
            <option value="beginner">Principiante</option>
            <option value="intermediate">Intermedio</option>
            <option value="advanced">Avanzado</option>
          </select>
        </div>

        <select
          value={category}
          onChange={(event) => setCategory(event.target.value)}
          className="p-3 border border-slate-300 rounded-lg bg-white"
        >
          {categories.map((value) => (
            <option key={value} value={value}>
              {value === 'all' ? 'Todas las categorias' : value}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className="card p-6 text-sm text-slate-500">Cargando lecciones...</div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((lesson) => (
            <div
              key={lesson.id}
              className={`card p-6 hover:shadow-md transition-shadow ${
                lesson.status === 'completed' ? 'border-emerald-200 bg-emerald-50/40' : ''
              }`}
            >
              <div className="flex items-start justify-between mb-4">
                <div
                  className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                    lesson.status === 'completed'
                      ? 'bg-emerald-100 text-emerald-600'
                      : lesson.status === 'in_progress'
                        ? 'bg-primary-100 text-primary-600'
                        : 'bg-slate-100 text-slate-600'
                  }`}
                >
                  {lesson.status === 'completed' ? (
                    <CheckCircle className="h-5 w-5" />
                  ) : lesson.status === 'in_progress' ? (
                    <Circle className="h-5 w-5" />
                  ) : (
                    <BookOpen className="h-5 w-5" />
                  )}
                </div>
                <div className="flex items-center gap-2">
                  {lesson.status === 'completed' && (
                    <span className="text-[10px] uppercase tracking-wide text-emerald-700 bg-emerald-100 rounded px-1.5 py-0.5 font-semibold">
                      Hecho
                    </span>
                  )}
                  {lesson.status === 'in_progress' && (
                    <span className="text-[10px] uppercase tracking-wide text-primary-700 bg-primary-100 rounded px-1.5 py-0.5 font-semibold">
                      En curso
                    </span>
                  )}
                  <span className="text-xs font-medium text-slate-600 bg-slate-100 px-2 py-1 rounded-full">
                    {difficultyLabel[lesson.difficulty] || lesson.difficulty}
                  </span>
                </div>
              </div>

              <h3 className="text-lg font-semibold text-slate-900 mb-2">{lesson.title}</h3>
              <p className="text-sm text-slate-600 mb-4 line-clamp-3">{lesson.description}</p>

              <div className="flex items-center justify-between text-xs text-slate-500 mb-4">
                <span className="bg-slate-100 px-2 py-1 rounded-md">{lesson.category}</span>
                <span className="flex items-center gap-1">
                  <Clock className="h-3 w-3" />
                  {lesson.estimated_duration} min
                </span>
              </div>

              <Link to={`/lessons/${lesson.id}`} className="btn-primary w-full text-center">
                {lesson.status === 'completed'
                  ? 'Revisar'
                  : lesson.status === 'in_progress'
                    ? 'Continuar'
                    : 'Comenzar'}
              </Link>

              {lesson.progress > 0 && (
                <div className="mt-4">
                  <div className="w-full bg-slate-200 rounded-full h-2">
                    <div className="bg-primary-600 h-2 rounded-full" style={{ width: `${lesson.progress}%` }} />
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="card p-6">
        <h2 className="text-xl font-semibold text-slate-900 mb-3">Tu progreso general</h2>
        <div className="flex items-center gap-3">
          <div className="flex-1 bg-slate-200 rounded-full h-3">
            <div
              className="bg-gradient-to-r from-primary-500 to-emerald-500 h-3 rounded-full transition-all"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
          <span className="text-sm font-semibold text-slate-700">{progressPercent}%</span>
        </div>
        <p className="text-sm text-slate-600 mt-2">
          Has completado {completed} de {items.length || 0} lecciones.
        </p>
      </div>
    </div>
  )
}

export default Lessons
