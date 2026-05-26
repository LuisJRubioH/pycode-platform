import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { CalendarDays, ArrowRight } from 'lucide-react'
import { api } from '../services/api'
import { useAuthStore } from '../stores/authStore'

interface PuzzleOfTheDay {
  id: number
  date: string
  title: string
  category: string
  topic: string
  code_snippet: string
  difficulty_label: string
  elo_rating: number
  solve_rate: number
}

const DIFFICULTY_COLORS: Record<string, string> = {
  Introductory: 'bg-sky-100 text-sky-700',
  Easy: 'bg-emerald-100 text-emerald-700',
  Medium: 'bg-amber-100 text-amber-700',
  Hard: 'bg-orange-100 text-orange-700',
  Expert: 'bg-rose-100 text-rose-700',
  Master: 'bg-purple-100 text-purple-700',
}

/**
 * Widget PÚBLICO del puzzle del día (landing). Cualquiera ve el reto
 * "predice la salida"; para resolverlo y ganar ELO hay que registrarse
 * (o, si ya hay sesión, ir a Puzzles). Nunca recibe la respuesta del backend.
 */
const PuzzleOfTheDay: React.FC = () => {
  const { accessToken } = useAuthStore()
  const [puzzle, setPuzzle] = useState<PuzzleOfTheDay | null>(null)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    const run = async () => {
      try {
        const res = await api.get('/elo/puzzle-of-the-day', { skipAuth: true })
        if (res.ok) {
          setPuzzle(await res.json())
        } else {
          setFailed(true)
        }
      } catch {
        setFailed(true)
      }
    }
    run()
  }, [])

  // Sin puzzles seedeados todavía: no rompemos la landing, solo no mostramos.
  if (failed || !puzzle) return null

  const badge =
    DIFFICULTY_COLORS[puzzle.difficulty_label] || 'bg-slate-100 text-slate-700'

  return (
    <section className="card p-8 max-w-3xl mx-auto">
      <div className="flex items-center justify-between flex-wrap gap-2 mb-4">
        <div className="flex items-center gap-2 text-primary-600">
          <CalendarDays className="h-5 w-5" />
          <h2 className="text-xl font-bold text-slate-900">Puzzle del día</h2>
        </div>
        <span className={`text-xs font-semibold px-2 py-1 rounded-full ${badge}`}>
          {puzzle.difficulty_label} · ELO {puzzle.elo_rating}
        </span>
      </div>

      <p className="text-slate-600 mb-3">
        ¿Cuál es la salida de este código Python?
      </p>

      <pre className="bg-slate-900 text-slate-100 rounded-lg p-4 overflow-x-auto text-sm font-mono mb-4">
        <code>{puzzle.code_snippet}</code>
      </pre>

      <div className="flex items-center justify-between flex-wrap gap-3">
        <p className="text-xs text-slate-500">
          {puzzle.topic} · tasa de acierto {puzzle.solve_rate}%
        </p>
        {accessToken ? (
          <Link
            to="/puzzles"
            className="inline-flex items-center gap-1 btn-primary"
          >
            Resolver y ganar ELO
            <ArrowRight className="h-4 w-4" />
          </Link>
        ) : (
          <Link
            to="/register"
            className="inline-flex items-center gap-1 btn-primary"
          >
            Regístrate para resolverlo
            <ArrowRight className="h-4 w-4" />
          </Link>
        )}
      </div>
    </section>
  )
}

export default PuzzleOfTheDay
