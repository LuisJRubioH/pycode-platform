import React from 'react'
import { Link } from 'react-router-dom'
import { BookOpen, Code2, MessageSquare, Trophy, Flame, Target, TrendingUp, Award } from 'lucide-react'

const Dashboard: React.FC = () => {
  const stats = [
    { label: 'Días de racha', value: '5', icon: Flame, color: 'text-orange-500' },
    { label: 'Ejercicios', value: '12', icon: Code2, color: 'text-primary-600' },
    { label: 'Lecciones', value: '3', icon: BookOpen, color: 'text-green-500' },
    { label: 'XP Total', value: '450', icon: Trophy, color: 'text-yellow-500' },
  ]

  const recentActivity = [
    { type: 'exercise', title: 'Variables y Tipos de Datos', date: 'Hace 2 horas', status: 'completed' },
    { type: 'lesson', title: 'Introducción a Python', date: 'Hace 1 día', status: 'in_progress' },
    { type: 'exercise', title: 'Operadores Aritméticos', date: 'Hace 2 días', status: 'completed' },
  ]

  const nextLessons = [
    { title: 'Estructuras de Control', progress: 0, total: 5 },
    { title: 'Funciones', progress: 0, total: 8 },
    { title: 'Listas y Tuplas', progress: 0, total: 6 },
  ]

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
          <p className="text-slate-600 mt-1">Bienvenido de vuelta, ¡sigue aprendiendo!</p>
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
            {recentActivity.map((activity, index) => (
              <div key={index} className="flex items-center justify-between py-3 border-b border-slate-100 last:border-0">
                <div className="flex items-center gap-3">
                  <div className={`w-2 h-2 rounded-full ${
                    activity.status === 'completed' ? 'bg-green-500' : 'bg-primary-500'
                  }`} />
                  <div>
                    <p className="text-sm font-medium text-slate-900">{activity.title}</p>
                    <p className="text-xs text-slate-500">{activity.date}</p>
                  </div>
                </div>
                <span className={`text-xs px-2 py-1 rounded-full ${
                  activity.status === 'completed' 
                    ? 'bg-green-100 text-green-700' 
                    : 'bg-primary-100 text-primary-700'
                }`}>
                  {activity.status === 'completed' ? 'Completado' : 'En progreso'}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Next Lessons */}
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-slate-900">Próximas Lecciones</h2>
            <Target className="h-5 w-5 text-slate-400" />
          </div>
          <div className="space-y-4">
            {nextLessons.map((lesson, index) => (
              <div key={index} className="py-3 border-b border-slate-100 last:border-0">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-slate-900">{lesson.title}</p>
                  <Award className="h-4 w-4 text-slate-400" />
                </div>
                <div className="w-full bg-slate-200 rounded-full h-2">
                  <div 
                    className="bg-primary-600 h-2 rounded-full transition-all"
                    style={{ width: `${(lesson.progress / lesson.total) * 100}%` }}
                  />
                </div>
                <p className="text-xs text-slate-500 mt-1">
                  {lesson.progress} / {lesson.total} ejercicios
                </p>
              </div>
            ))}
          </div>
          <Link to="/lessons" className="block text-center text-primary-600 hover:text-primary-500 text-sm mt-4">
            Ver todas las lecciones →
          </Link>
        </div>
      </div>

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
          <div className="p-4 bg-slate-50 rounded-lg text-center">
            <Trophy className="h-6 w-6 mx-auto mb-2 text-yellow-600" />
            <p className="text-sm font-medium text-slate-900">Logros</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard