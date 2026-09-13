import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { BrainCircuit, Filter, Gauge, ArrowRight, CheckCircle2, Undo2 } from 'lucide-react'
import { api } from '../services/api'
import Markdown from '../components/Markdown'

// El resumen de la tarjeta corta el enunciado a mitad: renderizarlo como
// Markdown dejaria bloques abiertos. Se quitan las marcas y queda texto.
const sinMarcas = (texto: string) => texto.replace(/```\w*|`|\*\*/g, '').replace(/\s+/g, ' ')

interface ChallengeSummary {
  id: number
  title: string
  slug: string
  source: string
  difficulty: string
  topic: string
  prompt_preview: string
  order_index: number
  completed: boolean
  // 1-3 si el reto es un nivel de un problema con progresion; null si es suelto.
  level: number | null
}

interface ChallengeLevel {
  id: number
  level: number
  difficulty: string
  completed: boolean
}

interface ChallengeDetail {
  id: number
  title: string
  slug: string
  source: string
  source_path: string
  difficulty: string
  topic: string
  prompt: string
  starter_code: string
  order_index: number
  level: number | null
  levels: ChallengeLevel[]
}

const difficultyLabel: Record<string, string> = {
  easy: 'Facil',
  medium: 'Medio',
  hard: 'Dificil',
}

const difficultyStyle: Record<string, string> = {
  easy: 'bg-emerald-100 text-emerald-700',
  medium: 'bg-amber-100 text-amber-700',
  hard: 'bg-rose-100 text-rose-700',
}

const Challenges: React.FC = () => {
  const navigate = useNavigate()
  const [filter, setFilter] = useState<'all' | 'easy' | 'medium' | 'hard'>('all')
  const [search, setSearch] = useState('')
  const [recommendedDifficulty, setRecommendedDifficulty] = useState('easy')
  const [items, setItems] = useState<ChallengeSummary[]>([])
  const [selected, setSelected] = useState<ChallengeDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadChallenges = async () => {
      setLoading(true)
      setError('')
      try {
        // /recommended admite como mucho limit=50 (le=50 en el endpoint): con 60
        // devolvia 422 y la pestaña por defecto, "Recomendados", salia en error.
        const query = filter === 'all' ? '/challenges/recommended?limit=50' : `/challenges?difficulty=${filter}&limit=60`
        const listRes = await api.get(query)
        if (!listRes.ok) {
          setItems([])
          setSelected(null)
          throw new Error('No se pudieron cargar los retos')
        }
        const listData = await listRes.json()
        setItems(listData.items || [])
        setRecommendedDifficulty(listData.recommended_difficulty || 'easy')

        const firstItem = listData.items?.[0]
        if (firstItem) {
          const detailRes = await api.get(`/challenges/${firstItem.id}`)
          if (detailRes.ok) {
            setSelected(await detailRes.json())
          }
        } else {
          setSelected(null)
        }
      } catch (error) {
        console.error('Error loading challenges:', error)
        setError('No se pudieron cargar los retos en este momento.')
      } finally {
        setLoading(false)
      }
    }

    loadChallenges()
  }, [filter])

  const filteredItems = items.filter((challenge) => {
    if (!search.trim()) return true
    const term = search.toLowerCase()
    return (
      challenge.title.toLowerCase().includes(term) ||
      challenge.topic.toLowerCase().includes(term) ||
      challenge.source.toLowerCase().includes(term)
    )
  })

  const openChallenge = async (id: number) => {
    const detailRes = await api.get(`/challenges/${id}`)
    if (!detailRes.ok) return
    setSelected(await detailRes.json())
  }

  // El reto viaja en la URL, como el ejercicio de una lección: el editor
  // carga su enunciado y su starter, y el enlace se puede recargar.
  const solveInEditor = () => {
    if (!selected) return
    navigate(`/editor?challenge=${selected.id}`)
  }

  const isSelectedCompleted = items.find((c) => c.id === selected?.id)?.completed || false

  const setCompleted = async (challengeId: number, completed: boolean) => {
    const method = completed ? 'post' : 'delete'
    try {
      const res = await api[method](`/challenges/${challengeId}/complete`)
      if (!res.ok) return
      setItems((prev) =>
        prev.map((c) => (c.id === challengeId ? { ...c, completed } : c))
      )
      // La progresion del detalle tambien marca el nivel.
      setSelected((prev) =>
        prev
          ? {
              ...prev,
              levels: prev.levels.map((l) => (l.id === challengeId ? { ...l, completed } : l)),
            }
          : prev
      )
    } catch (err) {
      console.error('Error toggling completion:', err)
    }
  }

  return (
    <div className="space-y-8">
      {error && (
        <div className="rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">{error}</div>
      )}

      <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Retos de programacion</h1>
          <p className="text-slate-600 mt-2">
            Retos importados y recomendados segun tu avance. Tu nivel actual apunta a retos{' '}
            <span className="font-semibold">{difficultyLabel[recommendedDifficulty] || recommendedDifficulty}</span>.
          </p>
        </div>

        <div className="flex items-center gap-2 bg-white border border-slate-200 rounded-xl p-2">
          <Filter className="h-4 w-4 text-slate-500" />
          {(['all', 'easy', 'medium', 'hard'] as const).map((value) => (
            <button
              key={value}
              onClick={() => setFilter(value)}
              className={`px-3 py-2 rounded-lg text-sm transition-colors ${
                filter === value ? 'bg-primary-600 text-white' : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              {value === 'all' ? 'Recomendados' : difficultyLabel[value]}
            </button>
          ))}
        </div>
      </div>

      <div className="card p-4">
        <input
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Buscar por titulo o tema..."
          className="w-full p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
      </div>

      <div className="grid lg:grid-cols-[0.95fr,1.3fr] gap-6">
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-slate-900">Banco de retos</h2>
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <BrainCircuit className="h-4 w-4" />
              <span>{filteredItems.length} disponibles</span>
            </div>
          </div>

          {loading ? (
            <p className="text-sm text-slate-500">Cargando retos...</p>
          ) : filteredItems.length === 0 ? (
            <div className="space-y-3">
              <p className="text-sm text-slate-500">No encontramos retos para ese filtro.</p>
              <Link to="/puzzles" className="btn-secondary inline-flex">
                Ver puzzles ELO
              </Link>
            </div>
          ) : (
            <div className="space-y-3 max-h-[70vh] overflow-auto pr-1">
              {filteredItems.map((challenge) => (
                <button
                  key={challenge.id}
                  onClick={() => openChallenge(challenge.id)}
                  className={`w-full text-left rounded-xl border p-4 transition-colors ${
                    selected?.id === challenge.id
                      ? 'border-primary-500 bg-primary-50'
                      : challenge.completed
                      ? 'border-emerald-200 bg-emerald-50/40 hover:border-emerald-300'
                      : 'border-slate-200 bg-white hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex items-start gap-2 flex-1">
                      <span className="mt-0.5 flex-shrink-0" aria-hidden>
                        {challenge.completed ? (
                          <CheckCircle2 className="h-5 w-5 text-emerald-600" />
                        ) : (
                          <span className="block w-5 h-5 rounded-full border-2 border-slate-300" />
                        )}
                      </span>
                      <div>
                        <p className="text-sm font-semibold text-slate-900 flex items-center gap-2">
                          {challenge.title}
                          {challenge.completed && (
                            <span className="text-[10px] uppercase tracking-wide text-emerald-700 bg-emerald-100 rounded px-1.5 py-0.5">
                              Hecho
                            </span>
                          )}
                        </p>
                        <p className="text-xs text-slate-500 mt-1">
                          {challenge.topic}
                          {challenge.level ? <> · Nivel {challenge.level} de 3</> : null}
                        </p>
                      </div>
                    </div>
                    <span className={`text-xs px-2 py-1 rounded-full ${difficultyStyle[challenge.difficulty] || 'bg-slate-100 text-slate-700'}`}>
                      {difficultyLabel[challenge.difficulty] || challenge.difficulty}
                    </span>
                  </div>
                  <p className="text-sm text-slate-600 mt-3 line-clamp-3">{sinMarcas(challenge.prompt_preview)}</p>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="card p-6">
          {selected ? (
            <div className="space-y-5">
              <div className="flex flex-wrap items-center gap-3">
                <h2 className="text-2xl font-bold text-slate-900">{selected.title}</h2>
                <span className={`text-xs px-2 py-1 rounded-full ${difficultyStyle[selected.difficulty] || 'bg-slate-100 text-slate-700'}`}>
                  {difficultyLabel[selected.difficulty] || selected.difficulty}
                </span>
              </div>

              <div className="flex flex-wrap gap-4 text-sm text-slate-500">
                <div className="flex items-center gap-2">
                  <Gauge className="h-4 w-4" />
                  <span>Tema: {selected.topic}</span>
                </div>
              </div>

              {/* Los tres niveles del mismo problema: se sube la exigencia sobre
                  una idea que ya conoces, en vez de repetir el reto. */}
              {selected.levels.length > 1 && (
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2">
                    Progresión de este problema
                  </p>
                  <ol className="flex flex-wrap items-center gap-2">
                    {selected.levels.map((nivel, index) => {
                      const actual = nivel.id === selected.id
                      return (
                        <li key={nivel.id} className="flex items-center gap-2">
                          {index > 0 && <ArrowRight className="h-3.5 w-3.5 text-slate-300" aria-hidden />}
                          <button
                            onClick={() => openChallenge(nivel.id)}
                            disabled={actual}
                            aria-current={actual ? 'step' : undefined}
                            className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-sm transition-colors ${
                              actual
                                ? 'border-primary-500 bg-primary-600 text-white'
                                : nivel.completed
                                ? 'border-emerald-300 bg-emerald-50 text-emerald-800 hover:bg-emerald-100'
                                : 'border-slate-300 bg-white text-slate-700 hover:bg-slate-50'
                            }`}
                          >
                            {nivel.completed && <CheckCircle2 className="h-3.5 w-3.5" aria-label="hecho" />}
                            Nivel {nivel.level} · {difficultyLabel[nivel.difficulty] || nivel.difficulty}
                          </button>
                        </li>
                      )
                    })}
                  </ol>
                </div>
              )}

              <Markdown className="prose prose-slate max-w-none">{selected.prompt}</Markdown>

              <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                <p className="text-sm font-medium text-slate-900">Al resolver este reto:</p>
                <p className="text-sm text-slate-600 mt-1">
                  Enviaremos el enunciado al editor para que puedas empezar y luego pedir retroalimentacion al tutor.
                </p>
              </div>

              <div className="flex flex-wrap gap-3">
                <button onClick={solveInEditor} className="btn-primary">
                  Resolver en el editor
                  <ArrowRight className="h-4 w-4 ml-2" />
                </button>
                {isSelectedCompleted ? (
                  <button
                    onClick={() => setCompleted(selected.id, false)}
                    className="btn-secondary"
                    title="Desmarcar este reto como hecho"
                  >
                    <Undo2 className="h-4 w-4 mr-2" />
                    Desmarcar
                  </button>
                ) : (
                  <button
                    onClick={() => setCompleted(selected.id, true)}
                    className="btn-secondary text-emerald-700 border-emerald-300 hover:bg-emerald-50"
                    title="Marcar este reto como hecho"
                  >
                    <CheckCircle2 className="h-4 w-4 mr-2" />
                    Marcar como hecho
                  </button>
                )}
              </div>
            </div>
          ) : (
            <p className="text-sm text-slate-500">Selecciona un reto para ver su detalle.</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default Challenges
