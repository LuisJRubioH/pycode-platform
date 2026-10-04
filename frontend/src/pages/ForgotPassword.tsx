import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { KeyRound, Mail, MailCheck } from 'lucide-react'

const ForgotPassword: React.FC = () => {
  const [email, setEmail] = useState('')
  const [enviado, setEnviado] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const respuesta = await fetch('/api/v1/auth/password-reset/request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      })
      if (respuesta.status === 429) {
        setError(
          'Has pedido el enlace demasiadas veces seguidas. Espera un rato y vuelve a intentarlo.'
        )
        return
      }
      // Cualquier otra respuesta lleva al mismo acuse: el backend responde 204
      // exista o no la cuenta, y el front no puede decir más de lo que sabe.
      setEnviado(true)
    } catch {
      setError('No se pudo conectar. Revisa tu conexión e inténtalo de nuevo.')
    } finally {
      setIsLoading(false)
    }
  }

  if (enviado) {
    return (
      <div className="max-w-md mx-auto">
        <div className="card p-8 text-center">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-green-100 rounded-full mb-4">
            <MailCheck className="h-6 w-6 text-green-600" />
          </div>
          <h1 className="text-2xl font-bold">Revisa tu correo</h1>
          <p className="text-slate-600 mt-3">
            Si hay una cuenta registrada con <strong>{email}</strong>, acabas de
            recibir un enlace para elegir una contraseña nueva.
          </p>
          <p className="text-sm text-slate-500 mt-3">
            El enlace caduca en una hora y solo se puede usar una vez. Si no lo
            ves, mira en la carpeta de spam.
          </p>
          <Link to="/login" className="btn-primary inline-block mt-6">
            Volver a iniciar sesión
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-md mx-auto">
      <div className="card p-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 rounded-full mb-4">
            <KeyRound className="h-6 w-6 text-primary-600" />
          </div>
          <h1 className="text-2xl font-bold">Recuperar contraseña</h1>
          <p className="text-slate-600 mt-2">
            Escribe el email con el que te registraste y te mandamos un enlace
            para elegir una nueva.
          </p>
        </div>

        {error && (
          <div
            role="alert"
            className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6"
          >
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-slate-700 mb-2"
            >
              <span className="flex items-center gap-2">
                <Mail className="h-4 w-4" />
                Email
              </span>
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input"
              placeholder="tu@email.com"
              required
              autoComplete="email"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full btn-primary disabled:opacity-50"
          >
            {isLoading ? 'Enviando...' : 'Enviarme el enlace'}
          </button>
        </form>

        <p className="text-center text-sm text-slate-600 mt-6">
          ¿Te acordaste?{' '}
          <Link to="/login" className="text-primary-600 hover:text-primary-500 font-medium">
            Inicia sesión
          </Link>
        </p>
      </div>
    </div>
  )
}

export default ForgotPassword
