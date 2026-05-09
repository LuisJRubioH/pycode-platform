import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Briefcase, ArrowRight } from 'lucide-react'
import { api } from '../services/api'
import { saveTutorContext } from '../services/tutorContext'
import EloResultModal, { EloAttemptResult } from '../components/EloResultModal'
import PuzzleAttemptsList from '../components/PuzzleAttemptsList'

interface InterviewPuzzle {
  id: number
  title: string
  category: string
  topic: string
  code_snippet: string
  difficulty_label: string
  elo_rating: number
  solve_rate: number
}

const InterviewProblems: React.FC = () => {
  const navigate = useNavigate()
  const [items, setItems] = useState<InterviewPuzzle[]>([])
  const [selected, setSelected] = useState<InterviewPuzzle | null>(null)
  const [answer, setAnswer] = useState('')
  const [result, setResult] = useState<EloAttemptResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [error, setError] = useState('')
  const [attemptsRefresh, setAttemptsRefresh] = useState(0)

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      setError('')
      try {
        const res = await api.get('/elo/interview-problems?limit=40')
        if (!res.ok) {
          if (res.status === 401) {
            setError('Tu sesion expiro. Inicia sesion para cargar ejercicios de entrevista.')
          } else if (res.status === 404) {
            setError('El endpoint de entrevista aun no esta activo en backend. Reinicia el backend.')
          } else {
            setError('No pudimos cargar los ejercicios de entrevista tecnica.')
          }
          setItems([])
          setSelected(null)
          return
        }
        const data = await res.json()
        const loaded = data.items || []
        setItems(loaded)
        setSelected(loaded[0] || null)
      } catch (loadError) {
        console.error('Error loading interview problems:', loadError)
        setError('Hubo un problema de conexion al cargar esta seccion.')
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [])

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
        setError('No se pudo evaluar tu intento. Intenta nuevamente.')
        return
      }
      setResult(await res.json())
      setAttemptsRefresh((n) => n + 1)
    } catch (submitError) {
      console.error('Error evaluating interview attempt:', submitError)
      setError('No se pudo evaluar tu intento. Intenta nuevamente.')
    } finally {
      setSending(false)
    }
  }

  const goToNext = () => {
    if (!selected) return
    const currentIndex = items.findIndex((p) => p.id === selected.id)
    const nextItem =
      items[currentIndex + 1] ||
      items.find((p) => p.id !== selected.id) ||
      null
    setResult(null)
    setAnswer('')
    if (nextItem) setSelected(nextItem)
  }

  const reviewWithTutor = () => {
    if (!selected) return
    saveTutorContext({
      problem_description: `[Entrevista tecnica] ${selected.title}`,
      student_code: selected.code_snippet,
      actual_output: answer,
      expected_output: result?.correct_output || '',
      current_lesson: `interview-${selected.topic}`,
      level: 'interview',
      source: `interview:${selected.id}`,
    })
    navigate('/tutor')
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Problemas de Entrevista Tecnica</h1>
        <p className="text-slate-600 mt-2">
          Seccion separada para practicar patrones de entrevista, con puntuacion ELO en cada intento.
        </p>
      </div>

      {error && (
        <div className="rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">
          {error}
        </div>
      )}

      <div className="grid lg:grid-cols-[0.95fr,1.3fr] gap-6">
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-slate-900">Banco entrevista</h2>
            <span className="text-xs text-slate-500">{items.length} disponibles</span>
          </div>

          {loading ? (
            <p className="text-sm text-slate-500">Cargando ejercicios...</p>
          ) : items.length === 0 ? (
            <p className="text-sm text-slate-500">Aun no hay ejercicios de entrevista disponibles.</p>
          ) : (
            <div className="space-y-3 max-h-[70vh] overflow-auto pr-1">
              {items.map((item) => (
                <button
                  key={item.id}
                  onClick={() => {
                    setSelected(item)
                    setAnswer('')
                    setResult(null)
                  }}
                  className={`w-full text-left rounded-xl border p-4 transition-colors ${
                    selected?.id === item.id
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-slate-200 bg-white hover:border-slate-300'
                  }`}
                >
                  <p className="text-sm font-semibold text-slate-900">{item.title}</p>
                  <p className="text-xs text-slate-500 mt-1">
                    {item.topic} · {item.difficulty_label} · ELO {item.elo_rating}
                  </p>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="card p-6">
          {!selected ? (
            <p className="text-sm text-slate-500">Selecciona un ejercicio para comenzar.</p>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center gap-2 text-slate-600">
                <Briefcase className="h-4 w-4" />
                <p className="text-sm">
                  Entrevista · {selected.topic} · ELO {selected.elo_rating}
                </p>
              </div>

              <h2 className="text-2xl font-bold text-slate-900">{selected.title}</h2>

              <pre className="bg-slate-950 text-slate-100 text-sm rounded-xl p-4 overflow-auto whitespace-pre-wrap">
                {selected.code_snippet}
              </pre>

              <textarea
                value={answer}
                onChange={(event) => setAnswer(event.target.value)}
                placeholder="Escribe la salida que esperas para este caso..."
                rows={4}
                className="w-full p-3 border border-slate-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />

              <div className="flex flex-wrap gap-3">
                <button
                  onClick={submitAttempt}
                  disabled={!answer.trim() || sending}
                  className="btn-primary disabled:opacity-50"
                >
                  {sending ? 'Evaluando...' : 'Evaluar con ELO'}
                </button>
                <button onClick={reviewWithTutor} className="btn-secondary">
                  Revisar con tutor
                  <ArrowRight className="h-4 w-4 ml-2" />
                </button>
              </div>

              <PuzzleAttemptsList
                puzzleId={selected.id}
                refreshKey={attemptsRefresh}
              />
            </div>
          )}
        </div>
      </div>

      {result && (
        <EloResultModal
          result={result}
          onClose={() => setResult(null)}
          onNext={goToNext}
          nextLabel="Siguiente ejercicio"
        />
      )}
    </div>
  )
}

export default InterviewProblems
