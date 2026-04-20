import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { BookOpen, Code2, MessageSquare, Trophy, Flame, Target, TrendingUp, Award, BrainCircuit } from 'lucide-react'
import { api } from '../services/api'
import { useAuthStore } from '../stores/authStore'
import ELODashboard from '../components/ELODashboard'

interface Stats {
  total_lessons: number
  completed_lessons: number
  total_score: number
  total_submissions: number
  streak_days: number
  level: string
  xp_points: number
}

interface Activity {
  type: string
  title: string
  lesson_title: string
  result: string
  created_at: string
}

interface Lesson {
  id: number
  title: string
  progress: number
  status: string
}

const Dashboard: React.FC = () => {
  const { user } = useAuthStore()
  const [statsData, setStatsData] = useState<Stats | null>(null)
  const [recentActivity, setRecentActivity] = useState<Activity[]>([])
  const [nextLessons, setNextLessons] = useState<Lesson[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, activityRes, lessonsRes] = await Promise.all([
          api.get('/progress/stats'),
          api.get('/progress/recent-activity'),
          api.get('/lessons/')
        ])

        if (statsRes.ok) {
          setStatsData(await statsRes.json())
        }
        if (activityRes.ok) {
          setRecentActivity(await activityRes.json())
        }
        if (lessonsRes.ok) {
          const lessons = await lessonsRes.json()
          // Only take lessons that are not fully completed for 'next Lessons'
          const next = lessons.filter((l: Lesson) => l.status !== 'completed').slice(0, 3)
          setNextLessons(next)
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
  }, [])

  const stats = [
    { label: 'Días de racha', value: statsData?.streak_days?.toString() || '0', icon: Flame, color: 'text-orange-500' },
    { label: 'Ejercicios', value: statsData?.total_submissions?.toString() || '0', icon: Code2, color: 'text-primary-600' },
    { label: 'Lecciones', value: statsData?.completed_lessons?.toString() || '0', icon: BookOpen, color: 'text-green-500' },
    { label: 'XP Total', value: statsData?.xp_points?.toString() || '0', icon: Trophy, color: 'text-yellow-500' },
  ]

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString()
  }

  if (isLoading) {
    return <div className="p-8 text-center text-slate-500">Cargando tu progreso...</div>
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
          <p className="text-slate-600 mt-1">Bienvenido de vuelta {user?.username}, ¡sigue aprendiendo!</p>
        </div>
        <div className="flex gap-3">
          <Link to="/editor" className="btn-primary">
            <Code2 className="h-4 w-4 mr-2" />
            Abrir Editor
          </Link>
          <Link to="/tutor" className="btn-secondary">
            <MessageSquare className="h-4 w-4 mr-2" />
            Tutor IA
          </Link>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} className="card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-600">{stat.label}</p>
                <p className="text-2xl font-bold text-slate-900">{stat.value}</p>
              </div>
              <stat.icon className={`h-8 w-8 ${stat.color}`} />
            </div>
          </div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Recent Activity */}
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-slate-900">Actividad Reciente</h2>
            <TrendingUp className="h-5 w-5 text-slate-400" />
          </div>
          <div className="space-y-4">
            {recentActivity.length === 0 ? (
              <p className="text-sm text-slate-500 py-4 text-center">Aún no hay actividad. ¡Empieza tu primera lección!</p>
            ) : (
              recentActivity.map((activity, index) => (
                <div key={index} className="flex items-center justify-between py-3 border-b border-slate-100 last:border-0">
                  <div className="flex items-center gap-3">
                    <div className={`w-2 h-2 rounded-full ${
                      activity.result === 'passed' ? 'bg-green-500' : 'bg-primary-500'
                    }`} />
                    <div>
                      <p className="text-sm font-medium text-slate-900">{activity.title}</p>
                      <p className="text-xs text-slate-500">{formatDate(activity.created_at)}</p>
                    </div>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    activity.result === 'passed' 
                      ? 'bg-green-100 text-green-700' 
                      : 'bg-primary-100 text-primary-700'
                  }`}>
                    {activity.result === 'passed' ? 'Completado' : 'Intentado'}
                  </span>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Next Lessons */}
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-slate-900">Próximas Lecciones</h2>
            <Target className="h-5 w-5 text-slate-400" />
          </div>
          <div className="space-y-4">
            {nextLessons.length === 0 ? (
              <p className="text-sm text-slate-500 py-4 text-center">¡Genial! Has completado todo por ahora.</p>
            ) : (
              nextLessons.map((lesson, index) => (
                <div key={index} className="py-3 border-b border-slate-100 last:border-0">
                  <div className="flex items-center justify-between mb-2">
                    <p className="text-sm font-medium text-slate-900">{lesson.title}</p>
                    <Award className="h-4 w-4 text-slate-400" />
                  </div>
                  <div className="w-full bg-slate-200 rounded-full h-2">
                    <div 
                      className="bg-primary-600 h-2 rounded-full transition-all"
                      style={{ width: `${lesson.progress}%` }}
                    />
                  </div>
                  <p className="text-xs text-slate-500 mt-1">
                    {lesson.progress}% completado
                  </p>
                </div>
              ))
            )}
          </div>
          <Link to="/lessons" className="block text-center text-primary-600 hover:text-primary-500 text-sm mt-4">
            Ver todas las lecciones →
          </Link>
        </div>
      </div>

      <section className="space-y-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Motor ELO</h2>
          <p className="text-slate-600">Tu progreso en puzzles ahora se mide con rating, rachas e historial.</p>
        </div>
        <ELODashboard />
      </section>

      {/* Quick Actions */}
      <div className="card p-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">Acciones Rápidas</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Link to="/lessons" className="p-4 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors text-center">
            <BookOpen className="h-6 w-6 mx-auto mb-2 text-primary-600" />
            <p className="text-sm font-medium text-slate-900">Continuar Lección</p>
          </Link>
          <Link to="/editor" className="p-4 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors text-center">
            <Code2 className="h-6 w-6 mx-auto mb-2 text-green-600" />
            <p className="text-sm font-medium text-slate-900">Practicar Código</p>
          </Link>
          <Link to="/tutor" className="p-4 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors text-center">
            <MessageSquare className="h-6 w-6 mx-auto mb-2 text-purple-600" />
            <p className="text-sm font-medium text-slate-900">Preguntar al Tutor</p>
          </Link>
          <Link to="/puzzles" className="p-4 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors text-center">
            <BrainCircuit className="h-6 w-6 mx-auto mb-2 text-yellow-600" />
            <p className="text-sm font-medium text-slate-900">Puzzles ELO</p>
          </Link>
          <Link to="/interview" className="p-4 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors text-center">
            <Award className="h-6 w-6 mx-auto mb-2 text-indigo-600" />
            <p className="text-sm font-medium text-slate-900">Entrevista</p>
          </Link>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
