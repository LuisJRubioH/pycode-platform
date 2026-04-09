import React, { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Sparkles, Lightbulb, HelpCircle } from 'lucide-react'

const TutorChat: React.FC = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: '¡Hola! Soy tu tutor de Python. Estoy aquí para ayudarte a aprender de manera socrática - te haré preguntas para guiarte a las respuestas en lugar de darte soluciones directas. ¿En qué puedo ayudarte hoy?',
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [wsConnected, setWsConnected] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/tutor')
    
    ws.onopen = () => {
      setWsConnected(true)
    }
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'message') {
        setMessages(prev => [...prev, {
          id: Date.now(),
          type: 'bot',
          content: data.content,
          timestamp: new Date()
        }])
        setIsTyping(false)
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

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = () => {
    if (!input.trim() || !wsRef.current) return
    
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: input,
      timestamp: new Date()
    }
    
    setMessages(prev => [...prev, userMessage])
    setIsTyping(true)
    
    wsRef.current.send(JSON.stringify({
      message: input,
      context: {
        currentLesson: 'variables',
        level: 'beginner'
      }
    }))
    
    setInput('')
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const quickQuestions = [
    '¿Qué es una variable?',
    '¿Cómo funciona print()?',
    '¿Qué tipo de datos existen?',
    'Explícame los operadores'
  ]

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      {/* Header */}
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
                <span className="text-xs text-slate-500">
                  {wsConnected ? 'En línea' : 'Desconectado'}
                </span>
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-2 text-xs text-slate-500">
            <Lightbulb className="h-4 w-4" />
            <span>Modo Socrático</span>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`flex items-start gap-3 max-w-[80%] ${
              message.type === 'user' ? 'flex-row-reverse' : ''
            }`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                message.type === 'user' 
                  ? 'bg-primary-600' 
                  : 'bg-gradient-to-br from-primary-500 to-purple-600'
              }`}>
                {message.type === 'user' ? (
                  <User className="h-4 w-4 text-white" />
                ) : (
                  <Bot className="h-4 w-4 text-white" />
                )}
              </div>
              
              <div className={`p-3 rounded-lg ${
                message.type === 'user'
                  ? 'bg-primary-600 text-white'
                  : 'bg-slate-100 text-slate-900'
              }`}>
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                <span className={`text-xs mt-1 block ${
                  message.type === 'user' ? 'text-primary-100' : 'text-slate-400'
                }`}>
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

      {/* Quick Questions */}
      {messages.length < 3 && (
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

      {/* Input */}
      <div className="p-4 border-t border-slate-200 bg-white">
        <div className="flex items-center gap-2">
          <div className="flex-1 relative">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Escribe tu pregunta aquí..."
              className="w-full p-3 pr-12 border border-slate-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows={2}
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
          El tutor utiliza el método socrático - te guiará con preguntas para ayudarte a pensar
        </p>
      </div>
    </div>
  )
}

export default TutorChat