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
  Edit3,
  Eye,
  FileText,
  Loader2,
  PlayCircle,
  Trophy,
  XCircle,
} from 'lucide-react'
import toast from 'react-hot-toast'
import { api } from '../services/api'
import { getSandbox } from '../sandbox/PyodideSandbox'
import type { HiddenTest, TestVerdict } from '../sandbox/types'

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
  // Estado de edicion de archivos: ruta -> contenido editado
  const [editedFiles, setEditedFiles] = useState<Record<string, string>>({})
  const [editingFile, setEditingFile] = useState<Record<string, boolean>>({})
  // Estado del envio
  const [submitting, setSubmitting] = useState(false)
  const [submitPhase, setSubmitPhase] = useState<string>('')
  const [lastVerdicts, setLastVerdicts] = useState<TestVerdict[] | null>(null)

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
        const detail = (await detailRes.json()) as CapstoneDetailPayload
        setCapstone(detail)
        // Inicializa el contenido editable con el starter
        const initial: Record<string, string> = {}
        detail.starter_files.forEach((f) => {
          initial[f.path] = f.content
        })
        setEditedFiles(initial)

        if (subRes.ok) {
          const sub = (await subRes.json()) as SubmissionPayload
          setSubmission(sub)
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

  const toggleEdit = (path: string) => {
    setEditingFile((prev) => ({ ...prev, [path]: !prev[path] }))
  }

  const resetFile = (path: string) => {
    const starter = capstone?.starter_files.find((f) => f.path === path)
    if (!starter) return
    setEditedFiles((prev) => ({ ...prev, [path]: starter.content }))
    toast.success(`Reseteado: ${path}`)
  }

  const submitCapstone = async () => {
    if (!capstone || submitting) return
    setSubmitting(true)
    setLastVerdicts(null)
    try {
      // 1) Pide los hidden_tests
      setSubmitPhase('Cargando tests...')
      const testsRes = await api.get(`/capstones/${capstone.slug}/hidden-tests`)
      if (!testsRes.ok) {
        toast.error('No se pudo obtener los tests del capstone.')
        return
      }
      const testsBody = (await testsRes.json()) as { tests: HiddenTest[] }

      // 2) Arranca Pyodide y corre los tests con el contenido editado
      setSubmitPhase('Inicializando Pyodide...')
      const sandbox = getSandbox()
      await sandbox.init()

      setSubmitPhase('Ejecutando tests en el navegador...')
      const files = capstone.starter_files.map((f) => ({
        path: f.path,
        content: editedFiles[f.path] ?? f.content,
      }))
      const result = await sandbox.runCapstoneTests(files, testsBody.tests)
      setLastVerdicts(result.verdicts)

      // 3) Envia el resultado al backend
      setSubmitPhase('Guardando resultado...')
      const postRes = await api.post(
        `/capstones/${capstone.slug}/submissions`,
        {
          files,
          tests_passed: result.passed,
          tests_total: result.total,
          test_results: result.verdicts.map((v) => ({
            name: v.name,
            passed: v.passed,
            error_message: v.errorMessage ?? null,
          })),
        },
      )
      if (!postRes.ok) {
        const txt = await postRes.text()
        toast.error(`Error al guardar: ${txt.slice(0, 120)}`)
        return
      }
      const saved = (await postRes.json()) as SubmissionPayload
      setSubmission(saved)
      if (saved.status === 'passed') {
        toast.success(`Capstone aprobado · ${saved.tests_passed}/${saved.tests_total} tests`)
      } else {
        toast(`Resultado guardado · ${saved.tests_passed}/${saved.tests_total} tests`, {
          icon: 'i',
        })
      }
    } catch (err) {
      console.error('Error enviando capstone:', err)
      toast.error('Error durante la evaluacion. Revisa la consola.')
    } finally {
      setSubmitting(false)
      setSubmitPhase('')
    }
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
          {capstone.starter_files.map((file) => {
            const editing = !!editingFile[file.path]
            const content = editedFiles[file.path] ?? file.content
            const isDirty = content !== file.content
            return (
              <div
                key={file.path}
                className="rounded-xl border border-slate-200 overflow-hidden"
              >
                <div className="flex items-center justify-between bg-slate-100 px-4 py-2">
                  <span className="flex items-center gap-2 text-sm font-mono font-semibold text-slate-700">
                    <FileText className="h-4 w-4" />
                    <span>{file.path}</span>
                    {isDirty && (
                      <span className="text-[10px] uppercase font-bold text-amber-600 px-1.5 py-0.5 rounded bg-amber-100">
                        modificado
                      </span>
                    )}
                  </span>
                  <div className="flex gap-2">
                    <button
                      onClick={() => toggleEdit(file.path)}
                      className="text-xs px-2 py-1 rounded border border-slate-300 hover:bg-white"
                    >
                      {editing ? (
                        <>
                          <Eye className="inline h-3 w-3 mr-1" />
                          Ver
                        </>
                      ) : (
                        <>
                          <Edit3 className="inline h-3 w-3 mr-1" />
                          Editar
                        </>
                      )}
                    </button>
                    {isDirty && (
                      <button
                        onClick={() => resetFile(file.path)}
                        className="text-xs px-2 py-1 rounded border border-slate-300 hover:bg-white"
                      >
                        Reset
                      </button>
                    )}
                    <button
                      onClick={() => copyToClipboard(content, file.path)}
                      className="text-xs px-2 py-1 rounded border border-slate-300 hover:bg-white"
                    >
                      <Copy className="inline h-3 w-3 mr-1" />
                      Copiar
                    </button>
                    <button
                      onClick={() => downloadFile(file.path, content)}
                      className="text-xs px-2 py-1 rounded border border-slate-300 hover:bg-white"
                    >
                      <Download className="inline h-3 w-3 mr-1" />
                      Descargar
                    </button>
                  </div>
                </div>
                {editing ? (
                  <textarea
                    value={content}
                    onChange={(e) =>
                      setEditedFiles((prev) => ({
                        ...prev,
                        [file.path]: e.target.value,
                      }))
                    }
                    className="w-full bg-slate-900 text-slate-100 text-xs font-mono p-4 min-h-[20rem] focus:outline-none"
                    spellCheck={false}
                  />
                ) : (
                  <pre className="bg-slate-900 text-slate-100 text-xs p-4 overflow-x-auto max-h-80">
                    <code>{content}</code>
                  </pre>
                )}
              </div>
            )
          })}
        </div>
      </div>

      <div className="card p-6 space-y-3 border-dashed border-2 border-amber-200 bg-amber-50">
        <h2 className="text-lg font-semibold text-amber-900 flex items-center gap-2">
          <Trophy className="h-5 w-5" />
          Enviar capstone
        </h2>
        <p className="text-sm text-amber-900">
          Editas los archivos arriba (boton "Editar" en cada uno) y al pulsar
          "Enviar capstone" la plataforma corre los {capstone.tests_total} tests
          ocultos directamente en tu navegador via Pyodide. El resultado se
          guarda en tu progreso.
        </p>
        <button
          onClick={submitCapstone}
          disabled={submitting}
          className="btn-primary inline-flex items-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {submitting ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              {submitPhase || 'Enviando...'}
            </>
          ) : (
            <>
              <PlayCircle className="h-4 w-4" />
              Enviar capstone
            </>
          )}
        </button>

        {lastVerdicts && (
          <div className="mt-4 space-y-2">
            <h3 className="text-sm font-semibold text-amber-900">
              Resultado de los tests ({lastVerdicts.filter((v) => v.passed).length}/
              {lastVerdicts.length})
            </h3>
            <ul className="space-y-1">
              {lastVerdicts.map((v, idx) => (
                <li
                  key={`${v.name}-${idx}`}
                  className={`text-xs flex items-start gap-2 p-2 rounded ${
                    v.passed ? 'bg-emerald-50 text-emerald-900' : 'bg-rose-50 text-rose-900'
                  }`}
                >
                  {v.passed ? (
                    <CheckCircle2 className="h-4 w-4 mt-0.5 flex-shrink-0 text-emerald-600" />
                  ) : (
                    <XCircle className="h-4 w-4 mt-0.5 flex-shrink-0 text-rose-600" />
                  )}
                  <div className="flex-1 min-w-0">
                    <p className="font-medium">{v.name}</p>
                    {!v.passed && v.errorMessage && (
                      <pre className="mt-1 whitespace-pre-wrap text-[11px] font-mono text-rose-800">
                        {v.errorMessage}
                      </pre>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default CapstoneDetail
