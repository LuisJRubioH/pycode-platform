import React, { useEffect, useState } from 'react'
import { CheckCircle2, XCircle, Sparkles, ArrowRight } from 'lucide-react'

export interface EloAttemptResult {
  correct: boolean
  correct_output: string
  explanation: string
  user_elo_before: number
  user_elo_after: number
  elo_delta_user: number
  puzzle_elo_before: number
  puzzle_elo_after: number
  rank_before: string
  rank_after: string
  rank_changed: boolean
  rank_color: string
  expected_probability: number
  win_probability_label: string
}

interface EloResultModalProps {
  result: EloAttemptResult
  onClose: () => void
  onNext?: () => void
  nextLabel?: string
}

const EloResultModal: React.FC<EloResultModalProps> = ({
  result,
  onClose,
  onNext,
  nextLabel = 'Siguiente puzzle',
}) => {
  const [displayElo, setDisplayElo] = useState(result.user_elo_before)

  useEffect(() => {
    const start = result.user_elo_before
    const target = result.user_elo_after
    const diff = target - start
    if (diff === 0) {
      setDisplayElo(target)
      return
    }

    const steps = 30
    let step = 0
    const timer = window.setInterval(() => {
      step += 1
      setDisplayElo(Math.round(start + (diff * step) / steps))
      if (step >= steps) {
        window.clearInterval(timer)
        setDisplayElo(target)
      }
    }, 20)

    return () => window.clearInterval(timer)
  }, [result.user_elo_before, result.user_elo_after])

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  const isPositive = result.elo_delta_user > 0
  const rankColor = result.rank_color || (result.correct ? '#10B981' : '#94A3B8')

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 px-4 py-8"
      role="dialog"
      aria-modal="true"
      aria-labelledby="elo-result-title"
      onClick={onClose}
    >
      <div
        className="w-full max-w-md rounded-2xl bg-white shadow-xl border border-slate-200 overflow-hidden"
        onClick={(event) => event.stopPropagation()}
      >
        <div
          className={`px-6 py-5 text-center ${
            result.correct ? 'bg-emerald-50' : 'bg-rose-50'
          }`}
        >
          <div className="flex justify-center mb-2">
            {result.correct ? (
              <CheckCircle2 className="h-12 w-12 text-emerald-600" />
            ) : (
              <XCircle className="h-12 w-12 text-rose-600" />
            )}
          </div>
          <h2
            id="elo-result-title"
            className={`text-xl font-bold ${
              result.correct ? 'text-emerald-700' : 'text-rose-700'
            }`}
          >
            {result.correct ? '¡Correcto!' : 'Aún se puede mejorar'}
          </h2>
        </div>

        <div className="p-6 space-y-5">
          <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-wide text-slate-500 mb-1">Tu ELO</p>
              <p className="text-3xl font-bold font-mono text-slate-900">
                {displayElo.toLocaleString()}
              </p>
              <p
                className={`text-sm font-semibold mt-1 ${
                  isPositive
                    ? 'text-emerald-600'
                    : result.elo_delta_user < 0
                    ? 'text-rose-600'
                    : 'text-slate-500'
                }`}
              >
                {isPositive ? '+' : ''}
                {result.elo_delta_user} pts
              </p>
            </div>
            <div className="text-right">
              <p className="text-xs uppercase tracking-wide text-slate-500 mb-1">Rango</p>
              <span
                className="inline-block rounded-md px-2.5 py-1 text-xs font-semibold border"
                style={{
                  color: rankColor,
                  borderColor: `${rankColor}55`,
                  backgroundColor: `${rankColor}15`,
                }}
              >
                {result.rank_after}
              </span>
              {result.rank_changed && (
                <p className="mt-2 inline-flex items-center gap-1 text-xs font-semibold text-emerald-700">
                  <Sparkles className="h-3.5 w-3.5" />
                  ¡Nuevo rango!
                </p>
              )}
            </div>
          </div>

          <div className="flex justify-between text-xs text-slate-500">
            <span>
              Dificultad para ti:{' '}
              <strong className="text-slate-700">{result.win_probability_label}</strong>
            </span>
            <span>{Math.round(result.expected_probability * 100)}% prob. esperada</span>
          </div>

          {!result.correct && result.correct_output && (
            <div className="rounded-lg border border-rose-200 bg-rose-50 p-3">
              <p className="text-[11px] font-semibold uppercase tracking-wide text-rose-700 mb-1">
                Solución correcta
              </p>
              <code className="text-sm font-mono text-rose-900 whitespace-pre-wrap break-words">
                {result.correct_output}
              </code>
            </div>
          )}

          {result.explanation && (
            <p className="text-sm text-slate-600 leading-relaxed">{result.explanation}</p>
          )}

          <div className="text-center text-[11px] text-slate-400">
            ELO del puzzle: {result.puzzle_elo_before} → {result.puzzle_elo_after}
          </div>

          <div className="flex gap-3 pt-1">
            <button onClick={onClose} className="btn-secondary flex-1">
              Ver editor
            </button>
            {onNext && (
              <button
                onClick={onNext}
                className="btn-primary flex-[1.4] inline-flex items-center justify-center gap-2"
              >
                {nextLabel}
                <ArrowRight className="h-4 w-4" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default EloResultModal
