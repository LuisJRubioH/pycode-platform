import React, { useEffect, useState } from 'react'
import { CheckCircle2, XCircle, ChevronDown, ChevronRight, History } from 'lucide-react'
import { api } from '../services/api'

interface PuzzleAttemptHistoryItem {
  id: number
  correct: boolean
  user_answer: string | null
  user_elo_before: number
  user_elo_after: number
  elo_delta_user: number
  expected_probability: number
  time_spent_seconds: number | null
  created_at: string
}

interface PuzzleAttemptsResponse {
  items: PuzzleAttemptHistoryItem[]
  total: number
}

interface PuzzleAttemptsListProps {
  puzzleId: number
  refreshKey?: number
}

const PuzzleAttemptsList: React.FC<PuzzleAttemptsListProps> = ({
  puzzleId,
  refreshKey = 0,
}) => {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [items, setItems] = useState<PuzzleAttemptHistoryItem[]>([])
  const [open, setOpen] = useState(false)

  useEffect(() => {
    let cancelled = false
    const load = async () => {
      setLoading(true)
      setError('')
      try {
        const res = await api.get(`/elo/puzzles/${puzzleId}/attempts?limit=20`)
        if (!res.ok) {
          if (!cancelled) setError('No se pudo cargar el historial.')
          return
        }
        const data = (await res.json()) as PuzzleAttemptsResponse
        if (!cancelled) setItems(data.items)
      } catch (err) {
        console.error('Error cargando intentos:', err)
        if (!cancelled) setError('Error de red al cargar intentos.')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [puzzleId, refreshKey])

  if (loading) {
    return (
      <p className="text-xs text-slate-400 italic">Cargando intentos previos...</p>
    )
  }

  if (error) {
    return <p className="text-xs text-rose-600">{error}</p>
  }

  if (items.length === 0) {
    return (
      <p className="text-xs text-slate-500 italic">
        Aún no has intentado este ejercicio. Tu primer intento aparecerá aquí.
      </p>
    )
  }

  const correctCount = items.filter((it) => it.correct).length

  return (
    <div className="rounded-lg border border-slate-200 bg-white">
      <button
        onClick={() => setOpen((prev) => !prev)}
        className="w-full flex items-center justify-between px-3 py-2 hover:bg-slate-50 rounded-lg"
      >
        <div className="flex items-center gap-2">
          {open ? (
            <ChevronDown className="h-4 w-4 text-slate-500" />
          ) : (
            <ChevronRight className="h-4 w-4 text-slate-500" />
          )}
          <History className="h-4 w-4 text-slate-500" />
          <span className="text-sm font-medium text-slate-700">
            Tus intentos previos: {correctCount}/{items.length} correctos
          </span>
        </div>
      </button>

      {open && (
        <ul className="divide-y divide-slate-100 border-t border-slate-200">
          {items.map((it) => (
            <li key={it.id} className="px-3 py-2 flex items-start gap-3">
              {it.correct ? (
                <CheckCircle2 className="h-4 w-4 text-emerald-600 mt-0.5 flex-shrink-0" />
              ) : (
                <XCircle className="h-4 w-4 text-rose-600 mt-0.5 flex-shrink-0" />
              )}
              <div className="flex-1 min-w-0">
                <p className="text-xs text-slate-500">
                  {new Date(it.created_at).toLocaleString()}
                </p>
                {it.user_answer && (
                  <p className="text-sm font-mono text-slate-800 truncate">
                    {it.user_answer}
                  </p>
                )}
              </div>
              <span
                className={`text-xs font-semibold whitespace-nowrap ${
                  it.elo_delta_user > 0
                    ? 'text-emerald-600'
                    : it.elo_delta_user < 0
                    ? 'text-rose-600'
                    : 'text-slate-500'
                }`}
              >
                {it.elo_delta_user > 0 ? '+' : ''}
                {it.elo_delta_user} pts
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default PuzzleAttemptsList
