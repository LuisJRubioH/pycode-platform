import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { UserPlus, Mail, Lock, User, Check, X } from 'lucide-react'
import { useAuthStore } from '../stores/authStore'
import { ErrorDeApi, type ErroresPorCampo } from '../services/erroresApi'

// Las mismas reglas que valida el backend (`backend/app/schemas/auth.py`).
// Se repiten aquí a propósito: el objetivo es que el alumno vea por qué falla
// ANTES de enviar, no que se entere por un 422. El backend sigue siendo quien
// decide — esto es ayuda, no validación.
const USERNAME_RE = /^[a-zA-Z0-9_-]+$/
const USERNAME_MIN = 3
const USERNAME_MAX = 32
const PASSWORD_MIN = 8

function validarUsername(valor: string): string | null {
  if (!valor) return 'Escribe un nombre de usuario'
  if (valor.length < USERNAME_MIN)
    return `Debe tener al menos ${USERNAME_MIN} caracteres`
  if (valor.length > USERNAME_MAX)
    return `No puede pasar de ${USERNAME_MAX} caracteres`
  if (!USERNAME_RE.test(valor))
    return 'Solo letras sin tilde, números, guion bajo (_) y guion (-): no se permiten espacios, puntos, tildes ni la ñ'
  return null
}

function validarPassword(valor: string): string | null {
  if (!valor) return 'Escribe una contraseña'
  if (valor.length < PASSWORD_MIN)
    return `Debe tener al menos ${PASSWORD_MIN} caracteres`
  if (!/\d/.test(valor)) return 'Debe contener al menos un número'
  if (!/[a-zA-Z]/.test(valor)) return 'Debe contener al menos una letra'
  return null
}

/** Una regla de la contraseña con su palomita en vivo mientras se escribe. */
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

const Register: React.FC = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  })
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [errores, setErrores] = useState<ErroresPorCampo>({})
  const navigate = useNavigate()
  const register = useAuthStore((state) => state.register)

  const actualizar = (campo: keyof typeof formData, valor: string) => {
    setFormData((previo) => ({ ...previo, [campo]: valor }))
    // Al corregir un campo se borra su error: dejarlo puesto mientras el
    // alumno reescribe es lo que hace dudar de cuál era el que fallaba.
    setErrores((previos) => {
      if (!previos[campo]) return previos
      const siguiente = { ...previos }
      delete siguiente[campo]
      return siguiente
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const locales: ErroresPorCampo = {}
    const errorUsuario = validarUsername(formData.username)
    if (errorUsuario) locales.username = errorUsuario
    const errorPassword = validarPassword(formData.password)
    if (errorPassword) locales.password = errorPassword
    if (formData.password !== formData.confirmPassword) {
      locales.confirmPassword = 'Las dos contraseñas no coinciden'
    }

    if (Object.keys(locales).length > 0) {
      setErrores(locales)
      setError('')
      return
    }

    setIsLoading(true)
    setError('')
    setErrores({})

    try {
      await register(formData.username, formData.email, formData.password)
      navigate('/login')
    } catch (err: unknown) {
      if (err instanceof ErrorDeApi && Object.keys(err.campos).length > 0) {
        // El 422 dice en `loc` qué campo falló: cada mensaje va a su sitio.
        setErrores(err.campos)
      } else if (err instanceof Error) {
        setError(err.message)
      } else {
        setError('Error de conexión')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const password = formData.password

  return (
    <div className="max-w-md mx-auto">
      <div className="card p-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 rounded-full mb-4">
            <UserPlus className="h-6 w-6 text-primary-600" />
          </div>
          <h1 className="text-2xl font-bold">Crear Cuenta</h1>
          <p className="text-slate-600 mt-2">
            Comienza tu viaje de aprendizaje Python
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

        <form onSubmit={handleSubmit} noValidate className="space-y-6">
          <div>
            <label
              htmlFor="username"
              className="block text-sm font-medium text-slate-700 mb-2"
            >
              <span className="flex items-center gap-2">
                <User className="h-4 w-4" />
                Nombre de usuario
              </span>
            </label>
            <input
              id="username"
              type="text"
              value={formData.username}
              onChange={(e) => actualizar('username', e.target.value)}
              className={`input ${errores.username ? 'border-red-400' : ''}`}
              placeholder="tu_usuario"
              aria-invalid={Boolean(errores.username)}
              aria-describedby={
                errores.username ? 'error-username' : 'ayuda-username'
              }
            />
            {errores.username ? (
              <p id="error-username" role="alert" className="mt-2 text-sm text-red-700">
                {errores.username}
              </p>
            ) : (
              <p id="ayuda-username" className="mt-2 text-xs text-slate-500">
                Entre {USERNAME_MIN} y {USERNAME_MAX} caracteres. Solo letras sin
                tilde, números, guion bajo (_) y guion (-).
              </p>
            )}
          </div>

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
              value={formData.email}
              onChange={(e) => actualizar('email', e.target.value)}
              className={`input ${errores.email ? 'border-red-400' : ''}`}
              placeholder="tu@email.com"
              required
              aria-invalid={Boolean(errores.email)}
              aria-describedby={errores.email ? 'error-email' : undefined}
            />
            {errores.email && (
              <p id="error-email" role="alert" className="mt-2 text-sm text-red-700">
                {errores.email}
              </p>
            )}
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-slate-700 mb-2"
            >
              <span className="flex items-center gap-2">
                <Lock className="h-4 w-4" />
                Contraseña
              </span>
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => actualizar('password', e.target.value)}
              className={`input ${errores.password ? 'border-red-400' : ''}`}
              placeholder="••••••••"
              aria-invalid={Boolean(errores.password)}
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
            {errores.password && (
              <p role="alert" className="mt-2 text-sm text-red-700">
                {errores.password}
              </p>
            )}
          </div>

          <div>
            <label
              htmlFor="confirmPassword"
              className="block text-sm font-medium text-slate-700 mb-2"
            >
              <span className="flex items-center gap-2">
                <Lock className="h-4 w-4" />
                Confirmar contraseña
              </span>
            </label>
            <input
              id="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={(e) => actualizar('confirmPassword', e.target.value)}
              className={`input ${errores.confirmPassword ? 'border-red-400' : ''}`}
              placeholder="••••••••"
              aria-invalid={Boolean(errores.confirmPassword)}
              aria-describedby={
                errores.confirmPassword ? 'error-confirm' : undefined
              }
            />
            {errores.confirmPassword && (
              <p id="error-confirm" role="alert" className="mt-2 text-sm text-red-700">
                {errores.confirmPassword}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full btn-primary disabled:opacity-50"
          >
            {isLoading ? 'Creando cuenta...' : 'Crear Cuenta'}
          </button>
        </form>

        <p className="text-center text-sm text-slate-600 mt-6">
          ¿Ya tienes cuenta?{' '}
          <Link to="/login" className="text-primary-600 hover:text-primary-500 font-medium">
            Inicia sesión aquí
          </Link>
        </p>
      </div>
    </div>
  )
}

export default Register
