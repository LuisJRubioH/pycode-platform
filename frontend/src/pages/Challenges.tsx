import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { BrainCircuit, Filter, Gauge, ArrowRight } from 'lucide-react'
import { api } from '../services/api'
import { saveTutorContext } from '../services/tutorContext'

interface ChallengeSummary {
  id: number
  title: string
  slug: string
  source: string
  difficulty: string
  topic: string
  prompt_preview: string
  order_index: number
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
        const query = filter === 'all' ? '/challenges/recommended?limit=60' : `/challenges?difficulty=${filter}&limit=60`
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

  const solveInEditor = () => {
    if (!selected) return

    saveTutorContext({
      problem_description: selected.prompt,
      student_code: selected.starter_code,
      current_lesson: `challenge-${selected.topic}`,
      level: selected.difficulty,
      source: `challenge:${selected.slug}`,
    })

    navigate('/editor')
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
          placeholder="Buscar por titulo, tema o fuente..."
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
                      : 'border-slate-200 bg-white hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="text-sm font-semibold text-slate-900">{challenge.title}</p>
                      <p className="text-xs text-slate-500 mt-1">
                        {challenge.source} · {challenge.topic}
                      </p>
                    </div>
                    <span className={`text-xs px-2 py-1 rounded-full ${difficultyStyle[challenge.difficulty] || 'bg-slate-100 text-slate-700'}`}>
                      {difficultyLabel[challenge.difficulty] || challenge.difficulty}
                    </span>
                  </div>
                  <p className="text-sm text-slate-600 mt-3 line-clamp-3">{challenge.prompt_preview}</p>
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
                <div>
                  <span>Fuente: {selected.source}</span>
                </div>
              </div>

              <div className="prose prose-slate max-w-none">
                {selected.prompt.split('\n').map((line, index) => (
                  <p key={index} className="text-slate-700 whitespace-pre-wrap">
                    {line}
                  </p>
                ))}
              </div>

              <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
                <p className="text-sm font-medium text-slate-900">Al resolver este reto:</p>
                <p className="text-sm text-slate-600 mt-1">
                  Enviaremos el enunciado al editor para que puedas empezar y luego pedir retroalimentacion al tutor.
                </p>
              </div>

              <button onClick={solveInEditor} className="btn-primary">
                Resolver en el editor
                <ArrowRight className="h-4 w-4 ml-2" />
              </button>
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
