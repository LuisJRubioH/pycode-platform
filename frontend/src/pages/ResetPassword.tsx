import React, { useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { Lock, ShieldCheck, Check, X } from 'lucide-react'
import { errorDesdeRespuesta, ErrorDeApi } from '../services/erroresApi'

const PASSWORD_MIN = 8

function validarPassword(valor: string): string | null {
  if (!valor) return 'Escribe una contraseña'
  if (valor.length < PASSWORD_MIN)
    return `Debe tener al menos ${PASSWORD_MIN} caracteres`
  if (!/\d/.test(valor)) return 'Debe contener al menos un número'
  if (!/[a-zA-Z]/.test(valor)) return 'Debe contener al menos una letra'
  return null
}

const Requisito: React.FC<{ cumplido: boolean; children: React.ReactNode }> = ({
  cumplido,
  children,
}) => (
  <li className={`flex items-center gap-2 ${cumplido ? 'text-green-700' : 'text-slate-500'}`}>
    {cumplido ? (
      <Check className="h-3.5 w-3.5 shrink-0" aria-hidden="true" />
    ) : (
      <X className="h-3.5 w-3.5 shrink-0" aria-hidden="true" />
    )}
    <span>{children}</span>
    <span className="sr-only">{cumplido ? '(cumplido)' : '(pendiente)'}</span>
  </li>
)

const ResetPassword: React.FC = () => {
  const [parametros] = useSearchParams()
  const token = parametros.get('token') ?? ''
  const navigate = useNavigate()

  const [password, setPassword] = useState('')
  const [confirmacion, setConfirmacion] = useState('')
  const [errorPassword, setErrorPassword] = useState('')
  const [errorConfirmacion, setErrorConfirmacion] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  // Sin token no hay nada que hacer aquí: pasa si alguien entra a la URL a
  // pelo, o si el cliente de correo partió el enlace en dos líneas al copiarlo.
  if (!token) {
    return (
      <div className="max-w-md mx-auto">
        <div className="card p-8 text-center space-y-4">
          <h1 className="text-2xl font-bold">Enlace incompleto</h1>
          <p className="text-slate-600">
            Este enlace de recuperación no trae el código. Copia la dirección
            entera desde el correo, o pide uno nuevo.
          </p>
          <Link to="/forgot-password" className="btn-primary inline-block">
            Pedir un enlace nuevo
          </Link>
        </div>
      </div>
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const fallo = validarPassword(password)
    const falloConfirmacion =
      password !== confirmacion ? 'Las dos contraseñas no coinciden' : ''
    setErrorPassword(fallo ?? '')
    setErrorConfirmacion(falloConfirmacion)
    if (fallo || falloConfirmacion) return

    setIsLoading(true)
    setError('')

    try {
      const respuesta = await fetch('/api/v1/auth/password-reset/confirm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, password }),
      })

      if (!respuesta.ok) {
        const fallo = await errorDesdeRespuesta(
          respuesta,
          'No se pudo cambiar la contraseña.'
        )
        if (fallo instanceof ErrorDeApi && fallo.campos.password) {
          setErrorPassword(fallo.campos.password)
        } else {
          setError(fallo.message)
        }
        return
      }

      // Las sesiones anteriores quedaron revocadas en el backend, así que
      // toca entrar de nuevo con la contraseña recién elegida.
      navigate('/login', { replace: true })
    } catch {
      setError('No se pudo conectar. Revisa tu conexión e inténtalo de nuevo.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <div className="card p-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 rounded-full mb-4">
            <ShieldCheck className="h-6 w-6 text-primary-600" />
          </div>
          <h1 className="text-2xl font-bold">Elige una contraseña nueva</h1>
          <p className="text-slate-600 mt-2">
            Al guardarla se cerrarán las sesiones abiertas en otros
            dispositivos.
          </p>
        </div>

        {error && (
          <div
            role="alert"
            className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6 space-y-2"
          >
            <p>{error}</p>
            <Link to="/forgot-password" className="underline font-medium">
              Pedir un enlace nuevo
            </Link>
          </div>
        )}

        <form onSubmit={handleSubmit} noValidate className="space-y-6">
          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-slate-700 mb-2"
            >
              <span className="flex items-center gap-2">
                <Lock className="h-4 w-4" />
                Contraseña nueva
              </span>
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value)
                setErrorPassword('')
              }}
              className={`input ${errorPassword ? 'border-red-400' : ''}`}
              placeholder="••••••••"
              autoComplete="new-password"
              aria-invalid={Boolean(errorPassword)}
              aria-describedby="requisitos-password"
            />
            <ul id="requisitos-password" className="mt-2 space-y-1 text-xs">
              <Requisito cumplido={password.length >= PASSWORD_MIN}>
                Al menos {PASSWORD_MIN} caracteres
              </Requisito>
              <Requisito cumplido={/[a-zA-Z]/.test(password)}>
                Al menos una letra
              </Requisito>
              <Requisito cumplido={/\d/.test(password)}>
                Al menos un número
              </Requisito>
            </ul>
            {errorPassword && (
              <p role="alert" className="mt-2 text-sm text-red-700">
                {errorPassword}
              </p>
            )}
          </div>

          <div>
            <label
              htmlFor="confirmacion"
              className="block text-sm font-medium text-slate-700 mb-2"
            >
              <span className="flex items-center gap-2">
                <Lock className="h-4 w-4" />
                Repite la contraseña
              </span>
            </label>
            <input
              id="confirmacion"
              type="password"
              value={confirmacion}
              onChange={(e) => {
                setConfirmacion(e.target.value)
                setErrorConfirmacion('')
              }}
              className={`input ${errorConfirmacion ? 'border-red-400' : ''}`}
              placeholder="••••••••"
              autoComplete="new-password"
              aria-invalid={Boolean(errorConfirmacion)}
              aria-describedby={errorConfirmacion ? 'error-confirm' : undefined}
            />
            {errorConfirmacion && (
              <p id="error-confirm" role="alert" className="mt-2 text-sm text-red-700">
                {errorConfirmacion}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full btn-primary disabled:opacity-50"
          >
            {isLoading ? 'Guardando...' : 'Guardar contraseña'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default ResetPassword
