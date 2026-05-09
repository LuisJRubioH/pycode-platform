import React, { useEffect, useRef, useState } from 'react'
import { Send, Bot, User, HelpCircle } from 'lucide-react'
import { useAuthStore } from '../stores/authStore'

interface ChatMessage {
  id: number
  role: 'user' | 'bot'
  content: string
  timestamp: Date
}

interface ServerMessage {
  type: 'history' | 'message' | 'error'
  content?: string
  messages?: Array<{ role: string; content: string; ts?: string }>
}

const QUICK_QUESTIONS = [
  '¿Qué es una variable en Python?',
  '¿Cuál es la diferencia entre una lista y una tupla?',
  '¿Cómo funcionan los bucles for?',
  'Explícame qué es una función con un ejemplo',
]

const greetingMessage: ChatMessage = {
  id: 0,
  role: 'bot',
  content:
    'Hola. Soy tu tutor de Python para preguntas conceptuales. Pregúntame lo que quieras aprender; si quieres que califique tu código, vuelve al editor y usa el botón "Evaluar mi código".',
  timestamp: new Date(),
}

const TutorChat: React.FC = () => {
  const accessToken = useAuthStore((state) => state.accessToken)
  const [messages, setMessages] = useState<ChatMessage[]>([greetingMessage])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [wsConnected, setWsConnected] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    if (!accessToken) return
    let reconnectTimeout: ReturnType<typeof setTimeout>

    const connect = () => {
      const baseUrl = import.meta.env.PROD
        ? 'wss://pycode-backend.onrender.com'
        : `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}`
      const ws = new WebSocket(`${baseUrl}/ws/tutor?token=${encodeURIComponent(accessToken)}`)

      ws.onopen = () => setWsConnected(true)

      ws.onmessage = (event) => {
        let data: ServerMessage
        try {
          data = JSON.parse(event.data)
        } catch {
          return
        }

        if (data.type === 'history' && Array.isArray(data.messages)) {
          const restored: ChatMessage[] = data.messages
            .filter((m) => m.role === 'user' || m.role === 'bot')
            .map((m, idx) => ({
              id: -(idx + 1),
              role: m.role as 'user' | 'bot',
              content: m.content,
              timestamp: m.ts ? new Date(m.ts) : new Date(),
            }))
          if (restored.length > 0) {
            setMessages([greetingMessage, ...restored])
          }
        } else if (data.type === 'message' && typeof data.content === 'string') {
          setMessages((prev) => [
            ...prev,
            {
              id: Date.now(),
              role: 'bot',
              content: data.content as string,
              timestamp: new Date(),
            },
          ])
          setIsTyping(false)
        } else if (data.type === 'error' && typeof data.content === 'string') {
          setMessages((prev) => [
            ...prev,
            {
              id: Date.now(),
              role: 'bot',
              content: `[error] ${data.content}`,
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
  }, [accessToken])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = () => {
    const trimmed = input.trim()
    if (!trimmed || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return

    setMessages((prev) => [
      ...prev,
      {
        id: Date.now(),
        role: 'user',
        content: trimmed,
        timestamp: new Date(),
      },
    ])
    setIsTyping(true)
    wsRef.current.send(JSON.stringify({ message: trimmed }))
    setInput('')
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

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

          <div className="text-xs text-slate-500">
            Modo: preguntas conceptuales · ¿Quieres evaluar código? Usa el editor.
          </div>
        </div>
      </div>

      <div className="flex-1 min-h-0 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`flex items-start gap-3 max-w-[80%] ${
                message.role === 'user' ? 'flex-row-reverse' : ''
              }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                  message.role === 'user'
                    ? 'bg-primary-600'
                    : 'bg-gradient-to-br from-primary-500 to-purple-600'
                }`}
              >
                {message.role === 'user' ? (
                  <User className="h-4 w-4 text-white" />
                ) : (
                  <Bot className="h-4 w-4 text-white" />
                )}
              </div>

              <div
                className={`p-3 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-primary-600 text-white'
                    : 'bg-slate-100 text-slate-900'
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                <span
                  className={`text-xs mt-1 block ${
                    message.role === 'user' ? 'text-primary-100' : 'text-slate-400'
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

      {messages.length < 3 && (
        <div className="p-4 border-t border-slate-200 bg-slate-50">
          <p className="text-xs text-slate-500 mb-2 flex items-center gap-1">
            <HelpCircle className="h-3 w-3" />
            Preguntas sugeridas:
          </p>
          <div className="flex flex-wrap gap-2">
            {QUICK_QUESTIONS.map((question, index) => (
              <button
                key={index}
                onClick={() => setInput(question)}
                className="text-xs px-3 py-1 rounded-full border border-slate-300 bg-white text-slate-700 hover:bg-slate-100"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="p-4 border-t border-slate-200 bg-white">
        <div className="flex items-end gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Pregunta lo que quieras aprender de Python..."
            rows={2}
            className="flex-1 p-3 border border-slate-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled={!wsConnected}
          />
          <button
            onClick={sendMessage}
            disabled={!input.trim() || !wsConnected}
            className="btn-primary disabled:opacity-50"
            aria-label="Enviar"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
        <p className="text-xs text-slate-400 mt-2">
          El tutor responde dudas conceptuales. Para calificar tu código, vuelve al editor.
        </p>
      </div>
    </div>
  )
}

export default TutorChat
