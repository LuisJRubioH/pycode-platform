import React, { useEffect, useState } from 'react'
import { X, History, ChevronDown, ChevronRight } from 'lucide-react'
import { api } from '../services/api'

interface EvaluationVerdict {
  raw: string
  logic_score: number | null
  general_score: number | null
}

interface EvaluationHistoryItem {
  id: number
  created_at: string
  code: string
  verdict: EvaluationVerdict
  model_used: string | null
}

interface EvaluationHistoryResponse {
  items: EvaluationHistoryItem[]
  total: number
}

interface EvaluationHistoryModalProps {
  exerciseId: number
  onClose: () => void
}

const EvaluationHistoryModal: React.FC<EvaluationHistoryModalProps> = ({
  exerciseId,
  onClose,
}) => {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [items, setItems] = useState<EvaluationHistoryItem[]>([])
  const [expanded, setExpanded] = useState<Set<number>>(new Set())

  useEffect(() => {
    let cancelled = false
    const load = async () => {
      setLoading(true)
      setError('')
      try {
        const res = await api.get(`/exercises/${exerciseId}/evaluations?limit=20`)
        if (!res.ok) {
          if (!cancelled) setError('No se pudo cargar el historial.')
          return
        }
        const data = (await res.json()) as EvaluationHistoryResponse
        if (!cancelled) setItems(data.items)
      } catch (err) {
        console.error('Error cargando historial:', err)
        if (!cancelled) setError('Error de red al cargar el historial.')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [exerciseId])

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  const toggle = (id: number) => {
    setExpanded((prev) => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="eval-history-title"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[85vh] flex flex-col"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="flex items-center justify-between border-b border-slate-200 p-4">
          <div className="flex items-center gap-2">
            <History className="h-5 w-5 text-slate-500" />
            <h2 id="eval-history-title" className="text-lg font-semibold text-slate-900">
              Historial de evaluaciones
            </h2>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600"
            aria-label="Cerrar"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="flex-1 overflow-auto p-4">
          {loading && <p className="text-sm text-slate-500">Cargando historial...</p>}

          {error && (
            <p className="text-sm text-rose-700 bg-rose-50 border border-rose-200 rounded p-3">
              {error}
            </p>
          )}

          {!loading && !error && items.length === 0 && (
            <p className="text-sm text-slate-500">
              Aún no hay evaluaciones para este ejercicio. Pulsa "Evaluar mi código"
              para guardar tu primer intento.
            </p>
          )}

          {!loading && !error && items.length > 0 && (
            <ul className="space-y-2">
              {items.map((item) => {
                const isOpen = expanded.has(item.id)
                return (
                  <li
                    key={item.id}
                    className="rounded-lg border border-slate-200 overflow-hidden"
                  >
                    <button
                      onClick={() => toggle(item.id)}
                      className="w-full flex items-center justify-between px-4 py-3 hover:bg-slate-50"
                    >
                      <div className="flex items-center gap-3 text-left">
                        {isOpen ? (
                          <ChevronDown className="h-4 w-4 text-slate-500" />
                        ) : (
                          <ChevronRight className="h-4 w-4 text-slate-500" />
                        )}
                        <div>
                          <p className="text-sm font-semibold text-slate-900">
                            #{item.id} · {new Date(item.created_at).toLocaleString()}
                          </p>
                          <p className="text-xs text-slate-500">
                            Lógica: {item.verdict.logic_score ?? '—'}/100 · General:{' '}
                            {item.verdict.general_score ?? '—'}/100
                            {item.model_used ? ` · ${item.model_used}` : ''}
                          </p>
                        </div>
                      </div>
                    </button>

                    {isOpen && (
                      <div className="border-t border-slate-200 bg-slate-50 p-4 space-y-3">
                        <div>
                          <p className="text-[11px] uppercase tracking-wide text-slate-500 mb-1">
                            Código enviado
                          </p>
                          <pre className="text-xs font-mono whitespace-pre-wrap bg-white border border-slate-200 rounded p-3 text-slate-800 max-h-60 overflow-auto">
                            {item.code}
                          </pre>
                        </div>
                        <div>
                          <p className="text-[11px] uppercase tracking-wide text-slate-500 mb-1">
                            Veredicto
                          </p>
                          <pre className="text-xs font-mono whitespace-pre-wrap bg-white border border-slate-200 rounded p-3 text-slate-800 max-h-72 overflow-auto">
                            {item.verdict.raw}
                          </pre>
                        </div>
                      </div>
                    )}
                  </li>
                )
              })}
            </ul>
          )}
        </div>
      </div>
    </div>
  )
}

export default EvaluationHistoryModal
