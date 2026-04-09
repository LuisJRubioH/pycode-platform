import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { BookOpen, Clock, CheckCircle, Circle, Lock, Play } from 'lucide-react'

const Lessons: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState('basics')
  
  const categories = [
    { id: 'basics', name: 'Fundamentos', icon: BookOpen },
    { id: 'intermediate', name: 'Intermedio', icon: Circle },
    { id: 'advanced', name: 'Avanzado', icon: CheckCircle },
  ]

  const lessons = {
    basics: [
      { 
        id: 1, 
        title: 'Introducción a Python', 
        description: 'Historia de Python, instalación y tu primer programa',
        duration: '15 min',
        exercises: 3,
        completed: true,
        progress: 100
      },
      { 
        id: 2, 
        title: 'Variables y Tipos de Datos', 
        description: 'Aprende sobre números, strings, booleanos y más',
        duration: '25 min',
        exercises: 5,
        completed: false,
        progress: 60
      },
      { 
        id: 3, 
        title: 'Operadores Aritméticos', 
        description: 'Suma, resta, multiplicación, división y operadores especiales',
        duration: '20 min',
        exercises: 4,
        completed: false,
        progress: 0
      },
      { 
        id: 4, 
        title: 'Entrada y Salida', 
        description: 'Input del usuario y formateo de salida',
        duration: '18 min',
        exercises: 3,
        completed: false,
        progress: 0,
        locked: true
      },
    ],
    intermediate: [
      { 
        id: 5, 
        title: 'Estructuras de Control', 
        description: 'if, elif, else y operadores lógicos',
        duration: '30 min',
        exercises: 6,
        completed: false,
        progress: 0,
        locked: true
      },
      { 
        id: 6, 
        title: 'Bucles', 
        description: 'for, while y control de iteraciones',
        duration: '35 min',
        exercises: 7,
        completed: false,
        progress: 0,
        locked: true
      },
    ],
    advanced: [
      { 
        id: 7, 
        title: 'Funciones', 
        description: 'Definición, parámetros y retorno de valores',
        duration: '40 min',
        exercises: 8,
        completed: false,
        progress: 0,
        locked: true
      },
      { 
        id: 8, 
        title: 'Listas y Tuplas', 
        description: 'Estructuras de datos secuenciales',
        duration: '35 min',
        exercises: 6,
        completed: false,
        progress: 0,
        locked: true
      },
    ]
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Lecciones</h1>
        <p className="text-slate-600 mt-2">
          Explora nuestras lecciones estructuradas y mejora tus habilidades de programación
        </p>
      </div>

      {/* Category Tabs */}
      <div className="flex gap-2 border-b border-slate-200">
        {categories.map((category) => (
          <button
            key={category.id}
            onClick={() => setSelectedCategory(category.id)}
            className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
              selectedCategory === category.id
                ? 'border-primary-600 text-primary-600'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}
          >
            <category.icon className="h-4 w-4" />
            {category.name}
          </button>
        ))}
      </div>

      {/* Lessons Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {lessons[selectedCategory as keyof typeof lessons].map((lesson) => (
          <div
            key={lesson.id}
            className={`card p-6 ${lesson.locked ? 'opacity-75' : 'hover:shadow-md'} transition-shadow`}
          >
            <div className="flex items-start justify-between mb-4">
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                lesson.completed 
                  ? 'bg-green-100 text-green-600' 
                  : lesson.progress > 0
                    ? 'bg-primary-100 text-primary-600'
                    : 'bg-slate-100 text-slate-600'
              }`}>
                {lesson.completed ? (
                  <CheckCircle className="h-5 w-5" />
                ) : lesson.locked ? (
                  <Lock className="h-5 w-5" />
                ) : (
                  <BookOpen className="h-5 w-5" />
                )}
              </div>
              
              {lesson.progress > 0 && lesson.progress < 100 && (
                <span className="text-xs font-medium text-primary-600 bg-primary-50 px-2 py-1 rounded-full">
                  {lesson.progress}%
                </span>
              )}
            </div>

            <h3 className="text-lg font-semibold text-slate-900 mb-2">{lesson.title}</h3>
            <p className="text-sm text-slate-600 mb-4">{lesson.description}</p>

            <div className="flex items-center gap-4 text-xs text-slate-500 mb-4">
              <div className="flex items-center gap-1">
                <Clock className="h-3 w-3" />
                {lesson.duration}
              </div>
              <div className="flex items-center gap-1">
                <Play className="h-3 w-3" />
                {lesson.exercises} ejercicios
              </div>
            </div>

            {lesson.locked ? (
              <button
                disabled
                className="w-full btn-secondary disabled:opacity-50"
              >
                <Lock className="h-4 w-4 mr-2" />
                Bloqueado
              </button>
            ) : (
              <Link
                to={`/lessons/${lesson.id}`}
                className={`w-full btn-primary flex items-center justify-center ${
                  lesson.completed ? 'bg-green-600 hover:bg-green-700' : ''
                }`}
              >
                {lesson.completed ? (
                  <>
                    <CheckCircle className="h-4 w-4 mr-2" />
                    Completado
                  </>
                ) : lesson.progress > 0 ? (
                  <>
                    <Play className="h-4 w-4 mr-2" />
                    Continuar
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4 mr-2" />
                    Comenzar
                  </>
                )}
              </Link>
            )}

            {lesson.progress > 0 && !lesson.completed && (
              <div className="mt-4">
                <div className="w-full bg-slate-200 rounded-full h-2">
                  <div
                    className="bg-primary-600 h-2 rounded-full transition-all"
                    style={{ width: `${lesson.progress}%` }}
                  />
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Learning Path */}
      <div className="card p-6 mt-8">
        <h2 className="text-xl font-semibold text-slate-900 mb-4">Tu Progreso</h2>
        <div className="flex items-center gap-2">
          <div className="flex-1 bg-slate-200 rounded-full h-3">
            <div className="bg-gradient-to-r from-primary-500 to-green-500 h-3 rounded-full transition-all" style={{ width: '25%' }} />
          </div>
          <span className="text-sm font-medium text-slate-700">25%</span>
        </div>
        <p className="text-sm text-slate-600 mt-2">
          Has completado 1 de 8 lecciones. ¡Sigue así!
        </p>
      </div>
    </div>
  )
}

export default Lessons