import React, { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { ArrowLeft, ArrowRight, BookOpen, Clock, Code2 } from 'lucide-react'
import { api } from '../services/api'
import { saveTutorContext } from '../services/tutorContext'

interface LessonExercise {
  id: number
  lesson_id: number
  title: string
  description: string
  instructions: string
  starter_code: string
  difficulty: string
  points: number
  order: number
  hints: string[]
}

interface LessonDetailPayload {
  id: number
  title: string
  description: string
  content: string
  difficulty: string
  category: string
  estimated_duration: number
  prerequisites: number[]
  exercises: LessonExercise[]
  progress: number
  status: string
}

const LessonDetail: React.FC = () => {
  const { lessonId } = useParams()
  const navigate = useNavigate()
  const [lesson, setLesson] = useState<LessonDetailPayload | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadLesson = async () => {
      setLoading(true)
      setError('')
      try {
        const res = await api.get(`/lessons/${lessonId}`)
        if (!res.ok) {
          setError('No pudimos cargar esta leccion.')
          setLesson(null)
          return
        }
        setLesson(await res.json())
      } catch (loadError) {
        console.error('Error loading lesson detail:', loadError)
        setError('No pudimos cargar esta leccion.')
      } finally {
        setLoading(false)
      }
    }

    if (lessonId) {
      loadLesson()
    }
  }, [lessonId])

  const practiceExercise = (exercise: LessonExercise) => {
    if (!lesson) return
    saveTutorContext({
      problem_description: `${lesson.title}\n\nEjercicio: ${exercise.title}\n${exercise.instructions}`,
      student_code: exercise.starter_code || '# Escribe tu solucion aqui\n',
      expected_output: '',
      current_lesson: `lesson-${lesson.id}`,
      level: lesson.difficulty,
      source: `lesson:${lesson.id}:exercise:${exercise.id}`,
      exercise_id: exercise.id,
    })
    navigate('/editor')
  }

  if (loading) {
    return <div className="card p-6 text-sm text-slate-500">Cargando leccion...</div>
  }

  if (error || !lesson) {
    return (
      <div className="space-y-4">
        <div className="rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">
          {error || 'Leccion no disponible.'}
        </div>
        <Link to="/lessons" className="btn-secondary inline-flex">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Volver a lecciones
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-500">{lesson.category}</p>
          <h1 className="text-3xl font-bold text-slate-900">{lesson.title}</h1>
          <p className="text-slate-600 mt-2">{lesson.description}</p>
        </div>
        <div className="text-right">
          <p className="text-xs text-slate-500">Progreso</p>
          <p className="text-2xl font-bold text-primary-700">{lesson.progress}%</p>
          <p className="text-xs text-slate-500 flex items-center justify-end gap-1 mt-1">
            <Clock className="h-3 w-3" />
            {lesson.estimated_duration} min
          </p>
        </div>
      </div>

      <Link to="/lessons" className="btn-secondary inline-flex">
        <ArrowLeft className="h-4 w-4 mr-2" />
        Volver al listado
      </Link>

      <div className="card p-6 prose prose-slate max-w-none">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{lesson.content || ''}</ReactMarkdown>
      </div>

      <div className="card p-6 space-y-4">
        <h2 className="text-xl font-semibold text-slate-900">Ejercicios de esta leccion</h2>

        {lesson.exercises.length === 0 ? (
          <p className="text-sm text-slate-500">No hay ejercicios asociados todavia.</p>
        ) : (
          <div className="space-y-4">
            {lesson.exercises.map((exercise) => (
              <div key={exercise.id} className="rounded-xl border border-slate-200 p-4 bg-slate-50">
                <div className="flex items-center justify-between flex-wrap gap-2">
                  <h3 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                    <BookOpen className="h-4 w-4 text-primary-600" />
                    {exercise.title}
                  </h3>
                  <span className="text-xs px-2 py-1 rounded-full bg-primary-100 text-primary-700">
                    {exercise.difficulty} · {exercise.points} pts
                  </span>
                </div>

                <p className="text-sm text-slate-600 mt-2">{exercise.description}</p>
                <p className="text-sm text-slate-700 mt-2 whitespace-pre-wrap">{exercise.instructions}</p>

                {exercise.hints?.length > 0 && (
                  <div className="mt-3 text-xs text-slate-500">
                    Pistas: {exercise.hints.join(' · ')}
                  </div>
                )}

                <div className="mt-4 flex flex-wrap gap-3">
                  <button onClick={() => practiceExercise(exercise)} className="btn-primary">
                    <Code2 className="h-4 w-4 mr-2" />
                    Practicar en editor
                  </button>
                  <button
                    onClick={() => {
                      practiceExercise(exercise)
                      navigate('/tutor')
                    }}
                    className="btn-secondary"
                  >
                    Revisar con tutor
                    <ArrowRight className="h-4 w-4 ml-2" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default LessonDetail
