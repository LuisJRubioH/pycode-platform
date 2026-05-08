import React, { useEffect, useRef, useState } from 'react'
import { Send, Bot, User, Sparkles, Lightbulb, HelpCircle } from 'lucide-react'
import { loadTutorContext } from '../services/tutorContext'

const EVAL_REQUEST_PATTERN =
  /\b(evalua|evaluar|evaluacion|califica|calificar|revision|revisar|retroalimentacion|feedback)\b/i

const TutorChat: React.FC = () => {
  const preloadedContext = loadTutorContext()
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content:
        'Hola. Soy tu tutor evaluador de Python para principiantes. Si me compartes el enunciado del ejercicio, tu codigo y lo que esperabas que pasara, puedo darte una retroalimentacion socratica con fortalezas, areas de mejora y preguntas guia sin darte la solucion completa.',
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [wsConnected, setWsConnected] = useState(false)
  const [showContext, setShowContext] = useState(false)
  const [showContextEditor, setShowContextEditor] = useState(false)
  const [focusEvaluation, setFocusEvaluation] = useState(false)
  const [context, setContext] = useState(() => ({
    current_lesson: preloadedContext?.current_lesson || 'variables',
    level: preloadedContext?.level || 'beginner',
    problem_description: preloadedContext?.problem_description || '',
    student_code: preloadedContext?.student_code || '',
    actual_output: preloadedContext?.actual_output || '',
    expected_output: preloadedContext?.expected_output || '',
    recent_errors: preloadedContext?.recent_errors || [],
  }))
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    let reconnectTimeout: ReturnType<typeof setTimeout>

    const connect = () => {
      // Vercel Hobby tier no proxea WebSockets de forma confiable;
      // en prod conectamos directamente al backend.
      const wsUrl = import.meta.env.PROD
        ? 'wss://pycode-backend.onrender.com/ws/tutor'
        : `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws/tutor`
      const ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        setWsConnected(true)
      }

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (data.type === 'message') {
          setMessages((prev) => [
            ...prev,
            {
              id: Date.now(),
              type: 'bot',
              content: data.content,
              timestamp: new Date(),
            },
          ])
          setIsTyping(false)
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

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    if (!preloadedContext?.student_code && !preloadedContext?.problem_description) {
      return
    }

    setMessages((prev) => {
      const alreadyNotified = prev.some(
        (message) => message.type === 'bot' && message.content.includes('He recibido contexto del editor')
      )
      if (alreadyNotified) {
        return prev
      }

      return [
        ...prev,
        {
          id: Date.now(),
          type: 'bot',
          content:
            'He recibido contexto del editor. Ya tengo tu codigo actual y la salida disponible, asi que puedes pedirme una evaluacion mas precisa.',
          timestamp: new Date(),
        },
      ]
    })
  }, [preloadedContext])

  const sendMessage = () => {
    if (!input.trim() || !wsRef.current) return
    const normalizedInput = input.trim()
    const shouldFocusEvaluation = EVAL_REQUEST_PATTERN.test(normalizedInput)

    if (shouldFocusEvaluation) {
      setFocusEvaluation(true)
      setShowContext(false)
      setShowContextEditor(false)
    }

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: normalizedInput,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setIsTyping(true)

    wsRef.current.send(
      JSON.stringify({
        message: normalizedInput,
        context,
      })
    )

    setInput('')
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const quickQuestions = [
    'Evalua mi solucion paso a paso',
    'Tengo este error, ayudame a entenderlo',
    'Que parte de mi logica esta fallando?',
    'Como puedo mejorar la claridad de mi codigo?',
  ]

  const hasContext = Boolean(context.problem_description || context.student_code || context.actual_output)

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      <div className="bg-white border-b border-slate-200 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-purple-600 rounded-full flex items-center justify-center">
              <Bot className="h-5 w-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-semibold text-slate-900">Tutor IA</h1>
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-500' : 'bg-red-500'}`} />
                <span className="text-xs text-slate-500">{wsConnected ? 'En linea' : 'Desconectado'}</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2 text-xs text-slate-500">
            {focusEvaluation && (
              <button
                onClick={() => setFocusEvaluation(false)}
                className="px-2 py-1 rounded-md border border-slate-300 bg-slate-50 text-slate-600 hover:bg-slate-100"
              >
                Salir de foco
              </button>
            )}
            <Lightbulb className="h-4 w-4" />
            <span>Modo evaluador socratico</span>
          </div>
        </div>
      </div>

      <div className="flex-1 min-h-0 overflow-y-auto p-4 space-y-4">
        {hasContext && !focusEvaluation && (
          <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
            <p className="text-xs font-semibold text-amber-900 uppercase tracking-wide">Contexto activo</p>
            <div className="mt-2 flex items-center gap-2">
              <button
                onClick={() => setShowContext((prev) => !prev)}
                className="text-xs px-2 py-1 rounded-md bg-white border border-amber-200 text-amber-900 hover:bg-amber-100"
              >
                {showContext ? 'Ocultar contexto' : 'Ver contexto'}
              </button>
              <button
                onClick={() => setShowContextEditor((prev) => !prev)}
                className="text-xs px-2 py-1 rounded-md bg-white border border-amber-200 text-amber-900 hover:bg-amber-100"
              >
                {showContextEditor ? 'Cerrar edicion' : 'Editar contexto'}
              </button>
            </div>

            {showContext && (
              <>
                {context.problem_description && (
                  <p className="text-sm text-amber-900 mt-3 whitespace-pre-wrap">
                    <strong>Enunciado:</strong> {context.problem_description}
                  </p>
                )}
                {context.student_code && (
                  <pre className="mt-3 max-h-40 text-xs bg-white border border-amber-100 rounded-lg p-3 overflow-auto whitespace-pre-wrap text-slate-800">
                    {context.student_code}
                  </pre>
                )}
                {context.actual_output && (
                  <p className="text-xs text-amber-800 mt-3 whitespace-pre-wrap">
                    <strong>Salida actual:</strong> {context.actual_output}
                  </p>
                )}
              </>
            )}
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`flex items-start gap-3 max-w-[80%] ${
                message.type === 'user' ? 'flex-row-reverse' : ''
              }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                  message.type === 'user'
                    ? 'bg-primary-600'
                    : 'bg-gradient-to-br from-primary-500 to-purple-600'
                }`}
              >
                {message.type === 'user' ? (
                  <User className="h-4 w-4 text-white" />
                ) : (
                  <Bot className="h-4 w-4 text-white" />
                )}
              </div>

              <div
                className={`p-3 rounded-lg ${
                  message.type === 'user'
                    ? 'bg-primary-600 text-white'
                    : 'bg-slate-100 text-slate-900'
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                <span
                  className={`text-xs mt-1 block ${
                    message.type === 'user' ? 'text-primary-100' : 'text-slate-400'
                  }`}
                >
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="flex justify-start">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-purple-600 rounded-full flex items-center justify-center">
                <Bot className="h-4 w-4 text-white" />
              </div>
              <div className="bg-slate-100 p-3 rounded-lg">
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-100" />
                  <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-200" />
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {messages.length < 3 && !focusEvaluation && (
        <div className="p-4 border-t border-slate-200 bg-slate-50">
          <p className="text-xs text-slate-500 mb-2 flex items-center gap-1">
            <HelpCircle className="h-3 w-3" />
            Preguntas sugeridas:
          </p>
          <div className="flex flex-wrap gap-2">
            {quickQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => {
                  setInput(question)
                }}
                className="text-xs bg-white border border-slate-200 text-slate-700 px-3 py-1.5 rounded-full hover:bg-slate-100 transition-colors"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="p-4 border-t border-slate-200 bg-white">
        {showContextEditor && !focusEvaluation && (
          <div className="grid gap-3 mb-3">
            <textarea
              value={context.problem_description}
              onChange={(e) =>
                setContext((prev) => ({ ...prev, problem_description: e.target.value }))
              }
              placeholder="Enunciado del ejercicio o que se supone que debe hacer tu codigo..."
              className="w-full p-3 border border-slate-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows={2}
              disabled={!wsConnected}
            />
            <textarea
              value={context.expected_output}
              onChange={(e) =>
                setContext((prev) => ({ ...prev, expected_output: e.target.value }))
              }
              placeholder="Salida esperada o criterio correcto opcional..."
              className="w-full p-3 border border-slate-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows={2}
              disabled={!wsConnected}
            />
          </div>
        )}

        <div className="flex items-center gap-2">
          <div className="flex-1 relative">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Pega aqui tu ejercicio, tu codigo o tu duda concreta..."
              className="w-full p-3 pr-12 border border-slate-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows={1}
              disabled={!wsConnected}
            />
            <Sparkles className="absolute right-3 top-3 h-5 w-5 text-slate-400" />
          </div>

          <button
            onClick={sendMessage}
            disabled={!input.trim() || !wsConnected}
            className="btn-primary h-auto py-3 px-4 disabled:opacity-50"
          >
            <Send className="h-5 w-5" />
          </button>
        </div>

        <p className="text-xs text-slate-400 mt-2 text-center">
          El tutor evalua como principiante, resalta fortalezas y te guia con preguntas en lugar de darte la solucion completa
        </p>
      </div>
    </div>
  )
}

export default TutorChat
