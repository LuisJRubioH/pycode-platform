import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ArrowRight, BrainCircuit, CheckCircle2, XCircle } from 'lucide-react'
import { api } from '../services/api'
import { saveTutorContext } from '../services/tutorContext'

interface Puzzle {
  id: number
  title: string
  category: string
  topic: string
  code_snippet: string
  difficulty_label: string
  elo_rating: number
  solve_rate: number
}

interface AttemptResult {
  correct: boolean
  correct_output: string
  explanation: string
  user_elo_before: number
  user_elo_after: number
  elo_delta_user: number
  rank_before: string
  rank_after: string
}

const Puzzles: React.FC = () => {
  const navigate = useNavigate()
  const [category, setCategory] = useState<'python' | 'numpy' | 'pandas'>('python')
  const [items, setItems] = useState<Puzzle[]>([])
  const [selected, setSelected] = useState<Puzzle | null>(null)
  const [answer, setAnswer] = useState('')
  const [result, setResult] = useState<AttemptResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadPuzzles = async () => {
      setLoading(true)
      setError('')
      try {
        const res = await api.get(`/elo/puzzles?category=${category}&limit=60`)
        if (!res.ok) {
          setError('No se pudieron cargar los puzzles en este momento.')
          setItems([])
          setSelected(null)
          return
        }

        const data = await res.json()
        const loadedItems = data.items || []
        setItems(loadedItems)
        setSelected(loadedItems[0] || null)
      } catch (loadError) {
        console.error('Error loading puzzles:', loadError)
        setError('Hubo un problema cargando puzzles. Intenta nuevamente.')
      } finally {
        setLoading(false)
      }
    }

    loadPuzzles()
  }, [category])

  const submitAttempt = async () => {
    if (!selected || !answer.trim()) return
    setSending(true)
    setResult(null)

    try {
      const res = await api.post('/elo/attempt', {
        puzzle_id: selected.id,
        user_answer: answer.trim(),
      })
      if (!res.ok) {
        setError('No pudimos evaluar tu respuesta. Vuelve a intentarlo.')
        return
      }
      setResult(await res.json())
    } catch (submitError) {
      console.error('Error submitting attempt:', submitError)
      setError('No pudimos evaluar tu respuesta. Vuelve a intentarlo.')
    } finally {
      setSending(false)
    }
  }

  const sendToTutor = () => {
    if (!selected) return
    saveTutorContext({
      problem_description: selected.title,
      student_code: selected.code_snippet,
      expected_output: result?.correct_output || '',
      actual_output: answer,
      current_lesson: `puzzle-${selected.topic}`,
      level: selected.difficulty_label.toLowerCase(),
      source: `puzzle:${selected.id}`,
    })
    navigate('/tutor')
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Puzzles ELO</h1>
        <p className="text-slate-600 mt-2">
          Selecciona un puzzle, responde y sube de rating segun tu resultado.
        </p>
        <div className="flex flex-wrap gap-2 mt-4">
          {(['python', 'numpy', 'pandas'] as const).map((value) => (
            <button
              key={value}
              onClick={() => setCategory(value)}
              className={`px-3 py-1.5 rounded-lg text-sm border transition-colors ${
                category === value
                  ? 'bg-primary-600 text-white border-primary-600'
                  : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-100'
              }`}
            >
              {value.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">
          {error}
        </div>
      )}

      <div className="grid lg:grid-cols-[0.95fr,1.3fr] gap-6">
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-slate-900">Lista de puzzles</h2>
            <span className="text-xs text-slate-500">{items.length} disponibles</span>
          </div>

          {loading ? (
            <p className="text-sm text-slate-500">Cargando puzzles...</p>
          ) : items.length === 0 ? (
            <div className="space-y-3">
              <p className="text-sm text-slate-500">No hay puzzles activos en la categoria {category.toUpperCase()}.</p>
              <Link to="/challenges" className="btn-secondary inline-flex">
                Ir a retos
              </Link>
            </div>
          ) : (
            <div className="space-y-3 max-h-[70vh] overflow-auto pr-1">
              {items.map((puzzle) => (
                <button
                  key={puzzle.id}
                  onClick={() => {
                    setSelected(puzzle)
                    setResult(null)
                    setAnswer('')
                  }}
                  className={`w-full text-left rounded-xl border p-4 transition-colors ${
                    selected?.id === puzzle.id
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-slate-200 bg-white hover:border-slate-300'
                  }`}
                >
                  <p className="text-sm font-semibold text-slate-900">{puzzle.title}</p>
                  <p className="text-xs text-slate-500 mt-1">
                    {puzzle.topic} · {puzzle.difficulty_label} · ELO {puzzle.elo_rating}
                  </p>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="card p-6">
          {!selected ? (
            <p className="text-sm text-slate-500">Selecciona un puzzle para comenzar.</p>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center gap-2 text-slate-500">
                <BrainCircuit className="h-4 w-4" />
                <p className="text-sm">
                  {selected.topic} · {selected.difficulty_label} · ELO {selected.elo_rating}
                </p>
              </div>

              <h2 className="text-2xl font-bold text-slate-900">{selected.title}</h2>

              <pre className="bg-slate-950 text-slate-100 text-sm rounded-xl p-4 overflow-auto whitespace-pre-wrap">
                {selected.code_snippet}
              </pre>

              <textarea
                value={answer}
                onChange={(event) => setAnswer(event.target.value)}
                placeholder="Escribe la salida esperada de este fragmento..."
                rows={4}
                className="w-full p-3 border border-slate-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />

              <div className="flex flex-wrap gap-3">
                <button
                  onClick={submitAttempt}
                  disabled={!answer.trim() || sending}
                  className="btn-primary disabled:opacity-50"
                >
                  {sending ? 'Evaluando...' : 'Evaluar respuesta'}
                </button>
                <button onClick={sendToTutor} className="btn-secondary">
                  Revisar con tutor
                  <ArrowRight className="h-4 w-4 ml-2" />
                </button>
              </div>

              {result && (
                <div
                  className={`rounded-xl border p-4 ${
                    result.correct ? 'border-emerald-200 bg-emerald-50' : 'border-amber-200 bg-amber-50'
                  }`}
                >
                  <div className="flex items-center gap-2">
                    {result.correct ? (
                      <CheckCircle2 className="h-5 w-5 text-emerald-600" />
                    ) : (
                      <XCircle className="h-5 w-5 text-amber-700" />
                    )}
                    <p className="font-semibold text-slate-900">
                      {result.correct ? 'Respuesta correcta' : 'Respuesta por mejorar'}
                    </p>
                  </div>
                  <p className="text-sm text-slate-700 mt-2">{result.explanation}</p>
                  <p className="text-xs text-slate-600 mt-2">
                    ELO {result.user_elo_before} → {result.user_elo_after} ({result.elo_delta_user > 0 ? '+' : ''}
                    {result.elo_delta_user})
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Puzzles
