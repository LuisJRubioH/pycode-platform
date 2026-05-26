import React, { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import {
  ArrowLeft,
  CheckCircle2,
  Clock,
  Copy,
  Download,
  FileText,
  Trophy,
  XCircle,
} from 'lucide-react'
import toast from 'react-hot-toast'
import { api } from '../services/api'

interface CapstoneRequirement {
  id: string
  text: string
}

interface CapstoneFile {
  path: string
  content: string
  editable: boolean
}

interface CapstoneDetailPayload {
  id: number
  slug: string
  track: string
  title: string
  short_description: string
  description: string
  requirements: CapstoneRequirement[]
  starter_files: CapstoneFile[]
  tests_total: number
  estimated_hours: number
  difficulty: string
  order_index: number
}

interface SubmissionPayload {
  id: number
  capstone_id: number
  status: string
  tests_passed: number
  tests_total: number
  test_results: unknown
  created_at: string
}

const DIFFICULTY_LABEL: Record<string, string> = {
  beginner: 'Principiante',
  intermediate: 'Intermedio',
  advanced: 'Avanzado',
}

const TRACK_LABEL: Record<string, string> = {
  'track-1': 'Track 1 · Python',
  'track-2': 'Track 2 · Data Science',
  'track-3': 'Track 3 · ML Clasico',
  'track-4': 'Track 4 · Deep Learning',
  'track-5': 'Track 5 · AI Engineering',
  'track-6': 'Track 6 · MLOps',
}

const CapstoneDetail: React.FC = () => {
  const { slug } = useParams()
  const [capstone, setCapstone] = useState<CapstoneDetailPayload | null>(null)
  const [submission, setSubmission] = useState<SubmissionPayload | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!slug) return
    const load = async () => {
      setLoading(true)
      setError('')
      try {
        const [detailRes, subRes] = await Promise.all([
          api.get(`/capstones/${slug}`),
          api.get(`/capstones/${slug}/my-submission`),
        ])

        if (!detailRes.ok) {
          if (detailRes.status === 404) {
            setError('Este capstone no existe.')
          } else {
            setError('No pudimos cargar el capstone.')
          }
          setCapstone(null)
          return
        }
        setCapstone(await detailRes.json())

        if (subRes.ok) {
          setSubmission(await subRes.json())
        } else {
          setSubmission(null)
        }
      } catch (loadError) {
        console.error('Error loading capstone:', loadError)
        setError('No pudimos cargar el capstone.')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [slug])

  const copyToClipboard = async (content: string, label: string) => {
    try {
      await navigator.clipboard.writeText(content)
      toast.success(`Copiado: ${label}`)
    } catch {
      toast.error('No se pudo copiar al portapapeles')
    }
  }

  const downloadFile = (path: string, content: string) => {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = path
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const downloadAll = () => {
    if (!capstone) return
    capstone.starter_files.forEach((f) => downloadFile(f.path, f.content))
  }

  const submissionBadge = useMemo(() => {
    if (!submission) return null
    if (submission.status === 'passed') {
      return (
        <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-emerald-100 text-emerald-700 text-sm font-medium">
          <CheckCircle2 className="h-4 w-4" />
          Aprobado · {submission.tests_passed}/{submission.tests_total} tests
        </span>
      )
    }
    if (submission.status === 'failed') {
      return (
        <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-rose-100 text-rose-700 text-sm font-medium">
          <XCircle className="h-4 w-4" />
          En progreso · {submission.tests_passed}/{submission.tests_total} tests
        </span>
      )
    }
    return (
      <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-sm font-medium">
        {submission.status} · {submission.tests_passed}/{submission.tests_total}
      </span>
    )
  }, [submission])

  if (loading) {
    return <div className="card p-6 text-sm text-slate-500">Cargando capstone...</div>
  }

  if (error || !capstone) {
    return (
      <div className="space-y-4">
        <div className="rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">
          {error || 'Capstone no disponible.'}
        </div>
        <Link to="/competencias" className="btn-secondary inline-flex">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Volver a competencias
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="flex items-start justify-between flex-wrap gap-3">
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-500">
            {TRACK_LABEL[capstone.track] || capstone.track} · Capstone
          </p>
          <h1 className="text-3xl font-bold text-slate-900 flex items-center gap-2 mt-1">
            <Trophy className="h-7 w-7 text-amber-500" />
            {capstone.title}
          </h1>
          <p className="text-slate-600 mt-2 max-w-3xl">{capstone.short_description}</p>
        </div>
        <div className="text-right">
          <p className="text-xs text-slate-500">Dificultad</p>
          <p className="text-lg font-semibold text-slate-900">
            {DIFFICULTY_LABEL[capstone.difficulty] || capstone.difficulty}
          </p>
          <p className="text-xs text-slate-500 flex items-center justify-end gap-1 mt-1">
            <Clock className="h-3 w-3" />~{capstone.estimated_hours} h
          </p>
        </div>
      </div>

      <div className="flex items-center justify-between flex-wrap gap-3">
        <Link to="/competencias" className="btn-secondary inline-flex">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Volver a competencias
        </Link>
        {submissionBadge}
      </div>

      <div className="card p-6 prose prose-slate max-w-none">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {capstone.description || ''}
        </ReactMarkdown>
      </div>

      <div className="card p-6 space-y-4">
        <h2 className="text-xl font-semibold text-slate-900">
          Requisitos ({capstone.requirements.length})
        </h2>
        <ul className="space-y-3">
          {capstone.requirements.map((req) => (
            <li
              key={req.id}
              className="flex items-start gap-3 rounded-lg border border-slate-200 bg-slate-50 p-3"
            >
              <span className="shrink-0 inline-flex items-center justify-center min-w-[2.5rem] h-7 rounded-full bg-primary-100 text-primary-700 text-xs font-bold">
                {req.id}
              </span>
              <span className="text-sm text-slate-700">{req.text}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="card p-6 space-y-4">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <h2 className="text-xl font-semibold text-slate-900">
            Archivos del proyecto ({capstone.starter_files.length})
          </h2>
          {capstone.starter_files.length > 1 && (
            <button onClick={downloadAll} className="btn-secondary text-sm">
              <Download className="h-4 w-4 mr-2" />
              Descargar todos
            </button>
          )}
        </div>
        <p className="text-sm text-slate-600">
          Descarga el scaffolding y completa los <code>TODO</code> en tu editor favorito. Cuando termines, podras enviar el proyecto y la plataforma correra {capstone.tests_total} tests ocultos sobre tu codigo.
        </p>
        <div className="space-y-4">
          {capstone.starter_files.map((file) => (
            <div
              key={file.path}
              className="rounded-xl border border-slate-200 overflow-hidden"
            >
              <div className="flex items-center justify-between bg-slate-100 px-4 py-2">
                <span className="flex items-center gap-2 text-sm font-mono font-semibold text-slate-700">
                  <FileText className="h-4 w-4" />
                  {file.path}
                </span>
                <div className="flex gap-2">
                  <button
                    onClick={() => copyToClipboard(file.content, file.path)}
                    className="text-xs px-2 py-1 rounded border border-slate-300 hover:bg-white"
                  >
                    <Copy className="inline h-3 w-3 mr-1" />
                    Copiar
                  </button>
                  <button
                    onClick={() => downloadFile(file.path, file.content)}
                    className="text-xs px-2 py-1 rounded border border-slate-300 hover:bg-white"
                  >
                    <Download className="inline h-3 w-3 mr-1" />
                    Descargar
                  </button>
                </div>
              </div>
              <pre className="bg-slate-900 text-slate-100 text-xs p-4 overflow-x-auto max-h-80">
                <code>{file.content}</code>
              </pre>
            </div>
          ))}
        </div>
      </div>

      <div className="card p-6 space-y-3 border-dashed border-2 border-amber-200 bg-amber-50">
        <h2 className="text-lg font-semibold text-amber-900 flex items-center gap-2">
          <Trophy className="h-5 w-5" />
          Enviar capstone
        </h2>
        <p className="text-sm text-amber-900">
          La evaluacion automatica via Pyodide llega en la siguiente iteracion (Pieza D.3). Mientras tanto, descarga el scaffolding y completa los archivos.
        </p>
        <button
          disabled
          className="btn-primary opacity-60 cursor-not-allowed"
          title="Disponible en Pieza D.3"
        >
          Enviar capstone (proximamente)
        </button>
      </div>
    </div>
  )
}

export default CapstoneDetail
