import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { UserPlus, Mail, Lock, User } from 'lucide-react'

const Register: React.FC = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (formData.password !== formData.confirmPassword) {
      setError('Las contraseñas no coinciden')
      return
    }
    
    setIsLoading(true)
    setError('')
    
    try {
      const response = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password
        })
      })
      
      if (response.ok) {
        navigate('/login')
      } else {
        const data = await response.json()
        setError(data.detail || 'Error al registrar')
      }
    } catch {
      setError('Error de conexión')
    } finally {
      setIsLoading(false)
    }
  }

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
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6">
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              <div className="flex items-center gap-2">
                <User className="h-4 w-4" />
                Nombre de usuario
              </div>
            </label>
            <input
              type="text"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              className="input"
              placeholder="Tu nombre de usuario"
              required
              minLength={3}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              <div className="flex items-center gap-2">
                <Mail className="h-4 w-4" />
                Email
              </div>
            </label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="input"
              placeholder="tu@email.com"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              <div className="flex items-center gap-2">
                <Lock className="h-4 w-4" />
                Contraseña
              </div>
            </label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              className="input"
              placeholder="••••••••"
              required
              minLength={8}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              <div className="flex items-center gap-2">
                <Lock className="h-4 w-4" />
                Confirmar contraseña
              </div>
            </label>
            <input
              type="password"
              value={formData.confirmPassword}
              onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
              className="input"
              placeholder="••••••••"
              required
            />
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