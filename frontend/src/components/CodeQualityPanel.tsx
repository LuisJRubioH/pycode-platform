import React, { useEffect, useState } from 'react'
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { Gauge } from 'lucide-react'
import { api } from '../services/api'

interface QualityPoint {
  created_at: string
  logic_score: number | null
  general_score: number | null
  static_score: number | null
}

interface QualitySummary {
  count: number
  avg_logic: number | null
  avg_general: number | null
  avg_static: number | null
  latest_static: number | null
}

interface QualityProgress {
  points: QualityPoint[]
  summary: QualitySummary
}

const fmt = (v: number | null) => (v === null ? '—' : v.toString())

/**
 * Panel de progresión de calidad de código: combina el static_score del
 * análisis estático (ast) con logic/general del evaluador socrático. Aparece
 * solo cuando el alumno ya tiene evaluaciones.
 */
const CodeQualityPanel: React.FC = () => {
  const [data, setData] = useState<QualityProgress | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const run = async () => {
      try {
        const res = await api.get('/progress/code-quality')
        if (res.ok) setData(await res.json())
      } catch {
        /* silencioso */
      } finally {
        setLoading(false)
      }
    }
    run()
  }, [])

  if (loading) return null
  if (!data || data.summary.count === 0) {
    return (
      <div className="card p-6 text-sm text-slate-500">
        Aún no tienes evaluaciones. Usa “Evaluar mi código” en el editor para
        empezar a medir tu progreso en lógica y calidad.
      </div>
    )
  }

  const chartData = data.points.map((p, i) => ({
    name: `#${i + 1}`,
    static: p.static_score,
    logic: p.logic_score,
    general: p.general_score,
  }))
  const hasLogic = data.points.some((p) => p.logic_score !== null)
  const hasGeneral = data.points.some((p) => p.general_score !== null)

  const stats = [
    { label: 'Calidad (estática)', value: fmt(data.summary.avg_static) },
    { label: 'Lógica (media)', value: fmt(data.summary.avg_logic) },
    { label: 'Solución (media)', value: fmt(data.summary.avg_general) },
    { label: 'Evaluaciones', value: data.summary.count.toString() },
  ]

  return (
    <div className="card p-6">
      <div className="flex items-center gap-2 mb-4">
        <Gauge className="h-5 w-5 text-primary-600" />
        <h3 className="text-lg font-semibold text-slate-900">
          Calidad de código y lógica
        </h3>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        {stats.map((s) => (
          <div key={s.label} className="rounded-xl border border-slate-200 p-3">
            <p className="text-xs text-slate-500">{s.label}</p>
            <p className="text-2xl font-bold text-slate-900">{s.value}</p>
          </div>
        ))}
      </div>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="name" stroke="#64748b" />
            <YAxis domain={[0, 100]} stroke="#64748b" />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="static"
              name="Calidad estática"
              stroke="#4f46e5"
              strokeWidth={3}
              connectNulls
              dot
            />
            {hasLogic && (
              <Line
                type="monotone"
                dataKey="logic"
                name="Lógica"
                stroke="#10b981"
                strokeWidth={2}
                connectNulls
                dot
              />
            )}
            {hasGeneral && (
              <Line
                type="monotone"
                dataKey="general"
                name="Solución"
                stroke="#f59e0b"
                strokeWidth={2}
                connectNulls
                dot
              />
            )}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default CodeQualityPanel
