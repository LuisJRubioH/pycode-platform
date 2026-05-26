import React, { useEffect, useState } from 'react'
import { Layers, Flame } from 'lucide-react'
import { api } from '../services/api'

interface RatingItem {
  domain: string
  scope: string
  elo_rating: number
  elo_peak: number
  rank: string
  rank_color: string
  attempts: number
  correct: number
  accuracy: number
  streak_current: number
  streak_best: number
}

interface DomainSummary {
  domain: string
  overall_elo: number
  rank: string
  rank_color: string
  tracks: number
  attempts: number
  correct: number
}

interface RatingsOut {
  global_elo: number
  global_rank: string
  global_rank_color: string
  domains: DomainSummary[]
  tracks: RatingItem[]
}

const DOMAIN_LABEL: Record<string, string> = {
  puzzle: 'Puzzles',
  challenge: 'Retos',
}

const SCOPE_LABEL: Record<string, string> = {
  python: 'Python',
  numpy: 'NumPy',
  pandas: 'Pandas',
  interview: 'Entrevista',
  easy: 'Fácil',
  medium: 'Medio',
  hard: 'Difícil',
}

const label = (map: Record<string, string>, key: string) =>
  map[key] || key.charAt(0).toUpperCase() + key.slice(1)

/**
 * Grid de ratings ELO separados por *(actividad, categoría)*.
 * Cada track muestra su propio ELO, rango (con color del backend), precisión
 * y racha. Arriba, un agregado por dominio.
 */
const EloTracks: React.FC = () => {
  const [data, setData] = useState<RatingsOut | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const run = async () => {
      try {
        const res = await api.get('/elo/ratings')
        if (res.ok) setData(await res.json())
      } catch {
        /* silencioso: el panel simplemente no aparece */
      } finally {
        setLoading(false)
      }
    }
    run()
  }, [])

  if (loading) return null
  if (!data || data.tracks.length === 0) {
    return (
      <div className="card p-6 text-sm text-slate-500">
        Aún no tienes ratings por categoría. Resuelve puzzles o marca retos
        para empezar a medir tu ELO en cada área.
      </div>
    )
  }

  const tracksByDomain = (domain: string) =>
    data.tracks.filter((t) => t.domain === domain)

  return (
    <div className="space-y-6">
      {data.domains.map((dom) => (
        <div key={dom.domain} className="card p-6">
          <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
            <div className="flex items-center gap-2">
              <Layers className="h-5 w-5 text-slate-400" />
              <h3 className="text-lg font-semibold text-slate-900">
                {label(DOMAIN_LABEL, dom.domain)}
              </h3>
            </div>
            <span
              className="text-xs font-bold px-2 py-1 rounded-full"
              style={{ backgroundColor: `${dom.rank_color}22`, color: dom.rank_color }}
            >
              {dom.rank} · {dom.overall_elo}
            </span>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {tracksByDomain(dom.domain).map((t) => (
              <div
                key={`${t.domain}:${t.scope}`}
                className="rounded-xl border border-slate-200 p-4"
              >
                <p className="text-sm font-medium text-slate-900">
                  {label(SCOPE_LABEL, t.scope)}
                </p>
                <p className="text-2xl font-bold text-slate-900 mt-1">
                  {t.elo_rating}
                </p>
                <span
                  className="inline-block text-[11px] font-semibold px-1.5 py-0.5 rounded mt-1"
                  style={{ backgroundColor: `${t.rank_color}22`, color: t.rank_color }}
                >
                  {t.rank}
                </span>
                <div className="flex items-center justify-between text-xs text-slate-500 mt-2">
                  <span>{t.accuracy}% acierto</span>
                  {t.streak_current > 0 && (
                    <span className="inline-flex items-center gap-0.5 text-orange-500">
                      <Flame className="h-3 w-3" />
                      {t.streak_current}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

export default EloTracks
