import React, { useState, useEffect, useRef } from 'react'
import Editor from '@monaco-editor/react'
import { Play, RotateCcw, Save, Share2, Terminal, Settings } from 'lucide-react'

const CodeEditor: React.FC = () => {
  const [code, setCode] = useState(`# Escribe tu código Python aquí
print("¡Hola, Mundo!")

# Prueba con variables
nombre = "Python"
print(f"Estoy aprendiendo {nombre}")
`)
  const [output, setOutput] = useState('')
  const [isRunning, setIsRunning] = useState(false)
  const [wsConnected, setWsConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    // Connect to WebSocket for code execution
    const ws = new WebSocket('ws://localhost:8000/ws/code')
    
    ws.onopen = () => {
      setWsConnected(true)
    }
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'output') {
        setOutput(prev => prev + data.content)
      } else if (data.type === 'done') {
        setIsRunning(false)
      } else if (data.type === 'error') {
        setOutput(prev => prev + `Error: ${data.content}\n`)
        setIsRunning(false)
      }
    }
    
    ws.onclose = () => {
      setWsConnected(false)
    }
    
    wsRef.current = ws
    
    return () => {
      ws.close()
    }
  }, [])

  const runCode = () => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      setOutput('Error: No hay conexión con el servidor\n')
      return
    }
    
    setOutput('')
    setIsRunning(true)
    
    wsRef.current.send(JSON.stringify({
      code: code,
      timeout: 30
    }))
  }

  const resetCode = () => {
    setCode(`# Escribe tu código Python aquí\nprint("¡Hola, Mundo!")\n`)
    setOutput('')
  }

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      {/* Toolbar */}
      <div className="bg-white border-b border-slate-200 p-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-semibold text-slate-900">Editor de Código</h1>
          <div className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-500' : 'bg-red-500'}`} />
          <span className="text-sm text-slate-500">
            {wsConnected ? 'Conectado' : 'Desconectado'}
          </span>
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
          
          <button
            onClick={resetCode}
            className="btn-secondary"
            title="Reiniciar código"
          >
            <RotateCcw className="h-4 w-4" />
          </button>
          
          <button
            className="btn-secondary"
            title="Guardar"
          >
            <Save className="h-4 w-4" />
          </button>
          
          <button
            className="btn-secondary"
            title="Compartir"
          >
            <Share2 className="h-4 w-4" />
          </button>
          
          <button
            className="btn-secondary"
            title="Configuración"
          >
            <Settings className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Editor and Output */}
      <div className="flex-1 flex">
        {/* Code Editor */}
        <div className="flex-1">
          <Editor
            height="100%"
            defaultLanguage="python"
            value={code}
            onChange={(value) => setCode(value || '')}
            theme="vs-dark"
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              fontFamily: 'JetBrains Mono, monospace',
              lineNumbers: 'on',
              roundedSelection: false,
              scrollBeyondLastLine: false,
              automaticLayout: true,
              padding: { top: 16 },
            }}
          />
        </div>

        {/* Output Panel */}
        <div className="w-96 bg-slate-900 text-white flex flex-col">
          <div className="p-3 bg-slate-800 border-b border-slate-700 flex items-center gap-2">
            <Terminal className="h-4 w-4" />
            <span className="text-sm font-medium">Salida</span>
          </div>
          
          <div className="flex-1 p-4 overflow-auto">
            {output ? (
              <pre className="text-sm font-mono whitespace-pre-wrap">{output}</pre>
            ) : (
              <p className="text-slate-400 text-sm">
                La salida aparecerá aquí después de ejecutar el código...
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