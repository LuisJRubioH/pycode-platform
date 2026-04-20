import React, { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Editor, { useMonaco } from '@monaco-editor/react'
import { Play, RotateCcw, Save, Share2, Terminal, Settings, MessageSquare } from 'lucide-react'
import { loadTutorContext, saveTutorContext } from '../services/tutorContext'

const INITIAL_CODE = `# Escribe tu codigo Python aqui
print("Hola, Mundo!")

# Prueba con variables
nombre = "Python"
print(f"Estoy aprendiendo {nombre}")
`

const DEFAULT_PROBLEM_DESCRIPTION =
  'Describe aqui que deberia hacer tu codigo. Mientras mas claro sea el objetivo, mejor sera la evaluacion del tutor.'

const CodeEditor: React.FC = () => {
  const navigate = useNavigate()
  const existingTutorContext = loadTutorContext()
  const [code, setCode] = useState(existingTutorContext?.student_code || INITIAL_CODE)
  const [output, setOutput] = useState(existingTutorContext?.actual_output || '')
  const [problemDescription, setProblemDescription] = useState(
    existingTutorContext?.problem_description || DEFAULT_PROBLEM_DESCRIPTION
  )
  const [expectedOutput, setExpectedOutput] = useState(existingTutorContext?.expected_output || '')
  const [isRunning, setIsRunning] = useState(false)
  const [wsConnected, setWsConnected] = useState(false)
  const [theme, setTheme] = useState('vs-dark')
  const [fontSize, setFontSize] = useState(14)
  const [minimap, setMinimap] = useState(false)
  const [showSettings, setShowSettings] = useState(false)

  const wsRef = useRef<WebSocket | null>(null)
  const monaco = useMonaco()

  useEffect(() => {
    if (monaco) {
      document.fonts.ready.then(() => {
        monaco.editor.remeasureFonts()
      })
    }
  }, [monaco])

  useEffect(() => {
    let reconnectTimeout: ReturnType<typeof setTimeout>

    const connect = () => {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const ws = new WebSocket(`${protocol}//${window.location.host}/ws/code`)

      ws.onopen = () => {
        setWsConnected(true)
      }

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (data.type === 'output') {
          setOutput((prev) => prev + data.content)
        } else if (data.type === 'done') {
          setIsRunning(false)
        } else if (data.type === 'error') {
          setOutput((prev) => prev + `Error: ${data.content}\n`)
          setIsRunning(false)
        }
      }

      ws.onclose = () => {
        setWsConnected(false)
        wsRef.current = null
        reconnectTimeout = setTimeout(connect, 3000)
      }

      wsRef.current = ws
    }

    connect()

    return () => {
      clearTimeout(reconnectTimeout)
      if (wsRef.current) {
        wsRef.current.onclose = null
        wsRef.current.close()
      }
    }
  }, [])

  const persistTutorContext = (nextOutput?: string) => {
    const normalizedOutput = (nextOutput ?? output).trim()
    const recentErrors = normalizedOutput
      ? normalizedOutput
          .split('\n')
          .filter((line) => /error|exception|traceback/i.test(line))
          .slice(0, 5)
      : []

    saveTutorContext({
      problem_description: problemDescription.trim() || DEFAULT_PROBLEM_DESCRIPTION,
      student_code: code,
      actual_output: normalizedOutput || undefined,
      expected_output: expectedOutput.trim() || undefined,
      current_lesson: 'python-basics',
      level: 'beginner',
      recent_errors: recentErrors,
      source: 'editor',
    })
  }

  const runCode = () => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      const errorMessage = 'Error: No hay conexion con el servidor\n'
      setOutput(errorMessage)
      persistTutorContext(errorMessage)
      return
    }

    setOutput('')
    setIsRunning(true)
    persistTutorContext('')

    wsRef.current.send(
      JSON.stringify({
        code,
        timeout: 30,
      })
    )
  }

  const resetCode = () => {
    setCode(INITIAL_CODE)
    setOutput('')
    setProblemDescription(DEFAULT_PROBLEM_DESCRIPTION)
    setExpectedOutput('')
    saveTutorContext({
      problem_description: DEFAULT_PROBLEM_DESCRIPTION,
      student_code: INITIAL_CODE,
      current_lesson: 'python-basics',
      level: 'beginner',
      source: 'editor',
    })
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

  const askTutorAboutCode = () => {
    persistTutorContext()
    navigate('/tutor')
  }

  useEffect(() => {
    persistTutorContext()
  }, [code, problemDescription, expectedOutput]) // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    persistTutorContext()
  }, [output]) // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      <div className="bg-white border-b border-slate-200 p-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-semibold text-slate-900">Editor de Codigo</h1>
          <div className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-500' : 'bg-red-500'}`} />
          <span className="text-sm text-slate-500">{wsConnected ? 'Conectado' : 'Desconectado'}</span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={runCode}
            disabled={isRunning || !wsConnected}
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

          <button
            onClick={askTutorAboutCode}
            className="btn-secondary"
            title="Enviar codigo actual al tutor"
          >
            <MessageSquare className="h-4 w-4 mr-2" />
            Preguntar al tutor
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
            Enunciado del ejercicio
          </label>
          <textarea
            value={problemDescription}
            onChange={(e) => setProblemDescription(e.target.value)}
            placeholder="Describe que se supone que debe hacer tu codigo..."
            className="w-full p-3 border border-slate-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white"
            rows={4}
          />
        </div>

        <div className="p-4">
          <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide mb-2">
            Salida esperada o criterio correcto
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
              El tutor recibira el enunciado, tu codigo, la salida actual y la salida esperada cuando uses <strong>Preguntar al tutor</strong>.
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
    </div>
  )
}

export default CodeEditor
