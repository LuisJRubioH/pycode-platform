import React, { useEffect, useState } from 'react'
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { Trophy, Target, Flame, BrainCircuit } from 'lucide-react'
import { api } from '../services/api'

interface EloProfile {
  elo_rating: number
  elo_peak: number
  rank: string
  rank_color: string
  puzzles_attempted: number
  puzzles_correct: number
  accuracy: number
  streak_current: number
  streak_best: number
}

interface EloHistoryPoint {
  elo_value: number
  delta: number
  correct: boolean
  rank_label: string
  puzzle_title: string
  category: string
  created_at: string
}

interface PuzzleRecommendation {
  id: number
  title: string
  category: string
  topic: string
  code_snippet: string
  difficulty_label: string
  elo_rating: number
  solve_rate: number
}

const ELODashboard: React.FC = () => {
  const [profile, setProfile] = useState<EloProfile | null>(null)
  const [history, setHistory] = useState<EloHistoryPoint[]>([])
  const [nextPuzzle, setNextPuzzle] = useState<PuzzleRecommendation | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadData = async () => {
      try {
        const [profileRes, historyRes, nextPuzzleRes] = await Promise.all([
          api.get('/elo/profile'),
          api.get('/elo/history?limit=20'),
          api.get('/elo/next-puzzle?category=python'),
        ])

        if (profileRes.ok) {
          setProfile(await profileRes.json())
        }

        if (historyRes.ok) {
          const historyData = await historyRes.json()
          setHistory(historyData.history || [])
        }

        if (nextPuzzleRes.ok) {
          setNextPuzzle(await nextPuzzleRes.json())
        }
      } catch (error) {
        console.error('Error loading ELO dashboard:', error)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [])

  if (loading) {
    return <div className="card p-6 text-sm text-slate-500">Cargando progreso ELO...</div>
  }

  if (!profile) {
    return <div className="card p-6 text-sm text-slate-500">No se pudo cargar el sistema ELO.</div>
  }

  const chartData = history.map((point, index) => ({
    name: index + 1,
    elo: point.elo_value,
    delta: point.delta,
    title: point.puzzle_title,
  }))

  return (
    <div className="space-y-6">
      <div className="grid md:grid-cols-4 gap-4">
        <div className="card p-5">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-wide text-slate-500">ELO actual</p>
              <p className="text-3xl font-bold" style={{ color: profile.rank_color }}>
                {profile.elo_rating}
              </p>
            </div>
            <Trophy className="h-8 w-8 text-yellow-500" />
          </div>
          <p className="text-sm text-slate-600 mt-2">{profile.rank}</p>
        </div>

        <div className="card p-5">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-wide text-slate-500">Precision</p>
              <p className="text-3xl font-bold text-slate-900">{profile.accuracy}%</p>
            </div>
            <Target className="h-8 w-8 text-emerald-500" />
          </div>
          <p className="text-sm text-slate-600 mt-2">
            {profile.puzzles_correct} correctos de {profile.puzzles_attempted}
          </p>
        </div>

        <div className="card p-5">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-wide text-slate-500">Racha actual</p>
              <p className="text-3xl font-bold text-slate-900">{profile.streak_current}</p>
            </div>
            <Flame className="h-8 w-8 text-orange-500" />
          </div>
          <p className="text-sm text-slate-600 mt-2">Mejor racha: {profile.streak_best}</p>
        </div>

        <div className="card p-5">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-wide text-slate-500">Pico historico</p>
              <p className="text-3xl font-bold text-slate-900">{profile.elo_peak}</p>
            </div>
            <BrainCircuit className="h-8 w-8 text-primary-600" />
          </div>
          <p className="text-sm text-slate-600 mt-2">Tu mejor rating hasta ahora</p>
        </div>
      </div>

      <div className="grid lg:grid-cols-[1.4fr,1fr] gap-6">
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-lg font-semibold text-slate-900">Curva de progreso ELO</h3>
              <p className="text-sm text-slate-500">Tus ultimos intentos y como movieron tu rating</p>
            </div>
          </div>

          {chartData.length === 0 ? (
            <p className="text-sm text-slate-500">Resuelve tu primer puzzle para ver tu progreso.</p>
          ) : (
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="name" stroke="#64748b" />
                  <YAxis stroke="#64748b" />
                  <Tooltip />
                  <Line type="monotone" dataKey="elo" stroke={profile.rank_color} strokeWidth={3} dot />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        <div className="card p-6">
          <h3 className="text-lg font-semibold text-slate-900">Puzzle recomendado</h3>
          {nextPuzzle ? (
            <div className="mt-4 space-y-4">
              <div>
                <p className="text-sm font-medium text-slate-900">{nextPuzzle.title}</p>
                <p className="text-xs text-slate-500">
                  {nextPuzzle.category} · {nextPuzzle.topic} · {nextPuzzle.difficulty_label}
                </p>
              </div>
              <pre className="bg-slate-950 text-slate-100 text-xs rounded-lg p-4 overflow-auto whitespace-pre-wrap">
                {nextPuzzle.code_snippet}
              </pre>
              <div className="text-xs text-slate-600 space-y-1">
                <p>Rating del puzzle: {nextPuzzle.elo_rating}</p>
                <p>Tasa de resolucion: {nextPuzzle.solve_rate}%</p>
              </div>
            </div>
          ) : (
            <p className="text-sm text-slate-500 mt-4">Aun no hay puzzles recomendados disponibles.</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default ELODashboard
