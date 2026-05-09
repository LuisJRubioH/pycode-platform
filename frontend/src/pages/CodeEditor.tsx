import React, { useEffect, useState } from 'react'
import Editor, { useMonaco } from '@monaco-editor/react'
import {
  Play,
  RotateCcw,
  Save,
  Share2,
  Terminal,
  Settings,
  ClipboardCheck,
  CheckCircle2,
  XCircle,
  TestTube2,
  History,
  X,
} from 'lucide-react'
import { runPythonCode, runHiddenTests, getCodeRunner } from '../services/codeRunner'
import { api } from '../services/api'
import { loadTutorContext } from '../services/tutorContext'
import EvaluationHistoryModal from '../components/EvaluationHistoryModal'
import type { HiddenTest, RunStatus, RunTestsResult } from '@/sandbox'

const INITIAL_CODE = `# Escribe tu codigo Python aqui
print("Hola, Mundo!")

# Prueba con variables
nombre = "Python"
print(f"Estoy aprendiendo {nombre}")
`

const PLACEHOLDER_PROBLEM =
  'Describe aqui que deberia hacer tu codigo. Mientras mas claro sea el objetivo, mejor sera la evaluacion del tutor.'

interface EvaluationVerdict {
  raw: string
  logic_score: number | null
  general_score: number | null
}

interface EvaluationResult {
  id: number
  created_at: string
  verdict: EvaluationVerdict
  model_used: string | null
}

const CodeEditor: React.FC = () => {
  const [code, setCode] = useState(INITIAL_CODE)
  const [output, setOutput] = useState('')
  const [problemDescription, setProblemDescription] = useState('')
  const [expectedOutput, setExpectedOutput] = useState('')
  const [isRunning, setIsRunning] = useState(false)
  const [sandboxStatus, setSandboxStatus] = useState<RunStatus>('idle')
  const [theme, setTheme] = useState('vs-dark')
  const [fontSize, setFontSize] = useState(14)
  const [minimap, setMinimap] = useState(false)
  const [showSettings, setShowSettings] = useState(false)
  const [isEvaluating, setIsEvaluating] = useState(false)
  const [evaluation, setEvaluation] = useState<EvaluationResult | null>(null)
  const [evaluationError, setEvaluationError] = useState('')
  const [exerciseId, setExerciseId] = useState<number | null>(null)
  const [isRunningTests, setIsRunningTests] = useState(false)
  const [testsResult, setTestsResult] = useState<RunTestsResult | null>(null)
  const [testsError, setTestsError] = useState('')
  const [showHistory, setShowHistory] = useState(false)

  const monaco = useMonaco()

  useEffect(() => {
    const ctx = loadTutorContext()
    if (!ctx) return
    if (ctx.student_code) setCode(ctx.student_code)
    if (ctx.problem_description) setProblemDescription(ctx.problem_description)
    if (ctx.expected_output) setExpectedOutput(ctx.expected_output)
    if (typeof ctx.exercise_id === 'number') setExerciseId(ctx.exercise_id)
  }, [])

  useEffect(() => {
    if (monaco) {
      document.fonts.ready.then(() => {
        monaco.editor.remeasureFonts()
      })
    }
  }, [monaco])

  useEffect(() => {
    const runner = getCodeRunner()
    setSandboxStatus(runner.status)
    return runner.onStatusChange(setSandboxStatus)
  }, [])

  const runCode = async () => {
    setOutput('')
    setIsRunning(true)
    try {
      const result = await runPythonCode(code)
      const combined = [result.stdout, result.stderr].filter(Boolean).join('\n')
      const finalOutput = combined || (result.ok ? '(sin salida)' : 'Error de ejecución')
      setOutput(finalOutput)
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err)
      setOutput(`Error: ${msg}\n`)
    } finally {
      setIsRunning(false)
    }
  }

  const resetCode = () => {
    setCode(INITIAL_CODE)
    setOutput('')
    setProblemDescription('')
    setExpectedOutput('')
    setEvaluation(null)
    setEvaluationError('')
    setTestsResult(null)
    setTestsError('')
  }

  const saveCode = () => {
    const blob = new Blob([code], { type: 'text/x-python' })
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = 'script.py'
    document.body.appendChild(anchor)
    anchor.click()
    document.body.removeChild(anchor)
    URL.revokeObjectURL(url)
  }

  const shareCode = async () => {
    try {
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(code)
        alert('Codigo copiado al portapapeles')
      } else {
        alert('Tu navegador no soporta esta accion')
      }
    } catch (error) {
      alert('Error al copiar el codigo')
      console.error(error)
    }
  }

  const runTests = async () => {
    if (exerciseId === null) return
    setTestsError('')
    setTestsResult(null)
    setIsRunningTests(true)
    try {
      const res = await api.get(`/exercises/${exerciseId}/hidden-tests`)
      if (!res.ok) {
        setTestsError('No se pudieron obtener los tests del ejercicio.')
        return
      }
      const body = (await res.json()) as { tests: HiddenTest[] }
      if (body.tests.length === 0) {
        setTestsError('Este ejercicio aún no tiene tests configurados.')
        return
      }
      const result = await runHiddenTests(code, body.tests)
      setTestsResult(result)
    } catch (err) {
      console.error('Error al ejecutar tests:', err)
      setTestsError('Error al ejecutar los tests en el sandbox.')
    } finally {
      setIsRunningTests(false)
    }
  }

  const evaluateCode = async () => {
    const trimmedDesc = problemDescription.trim()
    if (trimmedDesc.length < 10 || trimmedDesc === PLACEHOLDER_PROBLEM.trim()) {
      setEvaluationError(
        'Escribe primero qué intenta hacer tu código (mínimo 10 caracteres). El evaluador necesita el enunciado.'
      )
      return
    }
    setEvaluationError('')
    setIsEvaluating(true)
    setEvaluation(null)
    try {
      const res = await api.post('/tutor/evaluate', {
        problem_description: trimmedDesc,
        code,
        expected_output: expectedOutput.trim() || undefined,
        actual_output: output.trim() || undefined,
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        const detail = typeof data.detail === 'string' ? data.detail : 'No se pudo evaluar el código.'
        setEvaluationError(detail)
        return
      }
      const data = (await res.json()) as EvaluationResult
      setEvaluation(data)
    } catch (err) {
      console.error('Error al evaluar:', err)
      setEvaluationError('Error de red al contactar al evaluador.')
    } finally {
      setIsEvaluating(false)
    }
  }

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      <div className="bg-white border-b border-slate-200 p-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-semibold text-slate-900">Editor de Codigo</h1>
          <div
            className={`w-2 h-2 rounded-full ${
              sandboxStatus === 'ready' || sandboxStatus === 'running'
                ? 'bg-green-500'
                : sandboxStatus === 'error'
                ? 'bg-red-500'
                : sandboxStatus === 'loading'
                ? 'bg-yellow-500 animate-pulse'
                : 'bg-slate-400'
            }`}
          />
          <span className="text-sm text-slate-500">
            {sandboxStatus === 'idle' && 'Sandbox sin iniciar'}
            {sandboxStatus === 'loading' && 'Cargando Pyodide...'}
            {sandboxStatus === 'ready' && 'Listo (Pyodide)'}
            {sandboxStatus === 'running' && 'Ejecutando...'}
            {sandboxStatus === 'error' && 'Error en ejecución previa'}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={runCode}
            disabled={isRunning}
            className="btn-primary disabled:opacity-50"
          >
            <Play className="h-4 w-4 mr-2" />
            {isRunning ? 'Ejecutando...' : 'Ejecutar'}
          </button>

          <button onClick={resetCode} className="btn-secondary" title="Reiniciar codigo">
            <RotateCcw className="h-4 w-4" />
          </button>

          <button onClick={saveCode} className="btn-secondary" title="Descargar script Python">
            <Save className="h-4 w-4" />
          </button>

          <button onClick={shareCode} className="btn-secondary" title="Copiar codigo al portapapeles">
            <Share2 className="h-4 w-4" />
          </button>

          {exerciseId !== null && (
            <button
              onClick={runTests}
              disabled={isRunningTests}
              className="btn-secondary disabled:opacity-50"
              title="Correr los tests ocultos del ejercicio en Pyodide"
            >
              <TestTube2 className="h-4 w-4 mr-2" />
              {isRunningTests ? 'Ejecutando tests...' : 'Ejecutar tests'}
            </button>
          )}

          {exerciseId !== null && (
            <button
              onClick={() => setShowHistory(true)}
              className="btn-secondary"
              title="Ver evaluaciones previas de este ejercicio"
            >
              <History className="h-4 w-4 mr-2" />
              Historial
            </button>
          )}

          <button
            onClick={evaluateCode}
            disabled={isEvaluating}
            className="btn-secondary disabled:opacity-50"
            title="Pedir al evaluador una calificación socrática de tu intento"
          >
            <ClipboardCheck className="h-4 w-4 mr-2" />
            {isEvaluating ? 'Evaluando...' : 'Evaluar mi código'}
          </button>

          <div className="relative">
            <button
              onClick={() => setShowSettings(!showSettings)}
              className={`btn-secondary ${showSettings ? 'ring-2 ring-primary-500' : ''}`}
              title="Configuracion"
            >
              <Settings className="h-4 w-4" />
            </button>

            {showSettings && (
              <div className="absolute right-0 mt-2 w-64 bg-white border border-slate-200 rounded-lg shadow-lg z-10 p-4">
                <h3 className="text-sm font-semibold text-slate-800 mb-3 border-b border-slate-100 pb-2">
                  Configurar editor
                </h3>

                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Tema</label>
                    <select
                      value={theme}
                      onChange={(e) => setTheme(e.target.value)}
                      className="w-full text-sm border-slate-300 rounded focus:ring-primary-500 focus:border-primary-500 p-1.5 border"
                    >
                      <option value="vs-dark">Oscuro (vs-dark)</option>
                      <option value="light">Claro (light)</option>
                      <option value="hc-black">Alto contraste</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">
                      Tamaño de fuente: {fontSize}px
                    </label>
                    <input
                      type="range"
                      min="10"
                      max="24"
                      value={fontSize}
                      onChange={(e) => setFontSize(Number(e.target.value))}
                      className="w-full accent-primary-600"
                    />
                  </div>

                  <div className="flex items-center">
                    <input
                      id="minimap-toggle"
                      type="checkbox"
                      checked={minimap}
                      onChange={(e) => setMinimap(e.target.checked)}
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-slate-300 rounded"
                    />
                    <label htmlFor="minimap-toggle" className="ml-2 block text-xs text-slate-600 cursor-pointer">
                      Mostrar minimapa
                    </label>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-[1.4fr,1fr] gap-0 border-b border-slate-200 bg-slate-50">
        <div className="p-4 border-r border-slate-200">
          <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide mb-2">
            Enunciado del ejercicio (requerido para evaluar)
          </label>
          <textarea
            value={problemDescription}
            onChange={(e) => setProblemDescription(e.target.value)}
            placeholder={PLACEHOLDER_PROBLEM}
            className="w-full p-3 border border-slate-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white"
            rows={4}
          />
        </div>

        <div className="p-4">
          <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide mb-2">
            Salida esperada o criterio correcto (opcional)
          </label>
          <textarea
            value={expectedOutput}
            onChange={(e) => setExpectedOutput(e.target.value)}
            placeholder="Ejemplo: debe imprimir la suma total, o devolver una lista ordenada..."
            className="w-full p-3 border border-slate-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white"
            rows={4}
          />
        </div>
      </div>

      {evaluationError && (
        <div className="bg-red-50 border-y border-red-200 px-4 py-2 text-sm text-red-700">
          {evaluationError}
        </div>
      )}

      {testsError && (
        <div className="bg-amber-50 border-y border-amber-200 px-4 py-2 text-sm text-amber-800">
          {testsError}
        </div>
      )}

      {testsResult && (
        <div
          className={`border-y px-4 py-3 ${
            testsResult.passed === testsResult.total
              ? 'bg-emerald-50 border-emerald-200'
              : 'bg-rose-50 border-rose-200'
          }`}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <TestTube2
                className={`h-4 w-4 ${
                  testsResult.passed === testsResult.total
                    ? 'text-emerald-600'
                    : 'text-rose-600'
                }`}
              />
              <span className="text-sm font-semibold text-slate-800">
                Tests: {testsResult.passed} / {testsResult.total} pasaron
                <span className="text-slate-500 font-normal ml-2">
                  ({testsResult.durationMs.toFixed(0)} ms)
                </span>
              </span>
            </div>
            <button
              onClick={() => setTestsResult(null)}
              className="text-slate-400 hover:text-slate-600"
              aria-label="Cerrar"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
          <ul className="mt-2 space-y-1 text-sm">
            {testsResult.verdicts.map((v, i) => (
              <li key={i} className="flex items-start gap-2">
                {v.passed ? (
                  <CheckCircle2 className="h-4 w-4 text-emerald-600 mt-0.5 flex-shrink-0" />
                ) : (
                  <XCircle className="h-4 w-4 text-rose-600 mt-0.5 flex-shrink-0" />
                )}
                <div className="flex-1">
                  <span className="text-slate-800">{v.name || `Test ${i + 1}`}</span>
                  {!v.passed && v.errorMessage && (
                    <pre className="mt-1 text-xs font-mono whitespace-pre-wrap text-rose-700 bg-white/60 rounded px-2 py-1">
                      {v.errorMessage}
                    </pre>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="flex-1 flex">
        <div className="flex-1">
          <Editor
            height="100%"
            defaultLanguage="python"
            value={code}
            onChange={(value) => setCode(value || '')}
            theme={theme}
            options={{
              minimap: { enabled: minimap },
              fontSize,
              fontFamily: 'JetBrains Mono, monospace',
              lineNumbers: 'on',
              roundedSelection: false,
              scrollBeyondLastLine: false,
              automaticLayout: true,
              padding: { top: 16 },
            }}
          />
        </div>

        <div className="w-96 bg-slate-900 text-white flex flex-col">
          <div className="p-3 bg-slate-800 border-b border-slate-700 flex items-center gap-2">
            <Terminal className="h-4 w-4" />
            <span className="text-sm font-medium">Salida</span>
          </div>

          <div className="p-3 bg-slate-800 border-b border-slate-700">
            <p className="text-xs text-slate-300">
              Pulsa <strong>Evaluar mi código</strong> cuando quieras una calificación socrática.
              El tutor de Q&A vive en una página aparte para preguntas conceptuales.
            </p>
          </div>

          <div className="flex-1 p-4 overflow-auto">
            {output ? (
              <pre className="text-sm font-mono whitespace-pre-wrap">{output}</pre>
            ) : (
              <p className="text-slate-400 text-sm">
                La salida aparecera aqui despues de ejecutar el codigo...
              </p>
            )}
          </div>

          <div className="p-3 bg-slate-800 border-t border-slate-700">
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Estado: {isRunning ? 'Ejecutando...' : 'Listo'}</span>
              <span>Python 3.11</span>
            </div>
          </div>
        </div>
      </div>

      {showHistory && exerciseId !== null && (
        <EvaluationHistoryModal
          exerciseId={exerciseId}
          onClose={() => setShowHistory(false)}
        />
      )}

      {evaluation && (
        <div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
          onClick={() => setEvaluation(null)}
        >
          <div
            className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[85vh] flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between border-b border-slate-200 p-4">
              <div>
                <h2 className="text-lg font-semibold text-slate-900">
                  Evaluación socrática
                </h2>
                <p className="text-xs text-slate-500 mt-1">
                  Evaluación #{evaluation.id} · {new Date(evaluation.created_at).toLocaleString()}
                  {evaluation.model_used ? ` · ${evaluation.model_used}` : ''}
                </p>
              </div>
              <button
                onClick={() => setEvaluation(null)}
                className="text-slate-400 hover:text-slate-600"
                aria-label="Cerrar"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="p-4 border-b border-slate-200 grid grid-cols-2 gap-4">
              <div className="bg-slate-50 rounded-lg p-3">
                <p className="text-xs uppercase tracking-wide text-slate-500">Lógica</p>
                <p className="text-2xl font-bold text-slate-900">
                  {evaluation.verdict.logic_score ?? '—'}
                  <span className="text-sm font-normal text-slate-500"> /100</span>
                </p>
              </div>
              <div className="bg-slate-50 rounded-lg p-3">
                <p className="text-xs uppercase tracking-wide text-slate-500">Solución general</p>
                <p className="text-2xl font-bold text-slate-900">
                  {evaluation.verdict.general_score ?? '—'}
                  <span className="text-sm font-normal text-slate-500"> /100</span>
                </p>
              </div>
            </div>

            <div className="p-4 overflow-auto flex-1">
              <pre className="text-sm font-mono whitespace-pre-wrap text-slate-800">
                {evaluation.verdict.raw}
              </pre>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default CodeEditor
