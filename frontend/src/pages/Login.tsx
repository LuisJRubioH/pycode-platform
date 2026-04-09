import React from 'react'

const Login: React.FC = () => {
  return (
    <div className="max-w-md mx-auto">
      <div className="card p-8">
        <h1 className="text-2xl font-bold text-center mb-8">Iniciar Sesión</h1>
        
        <form className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Email
            </label>
            <input
              type="email"
              className="input"
              placeholder="tu@email.com"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Contraseña
            </label>
            <input
              type="password"
              className="input"
              placeholder="••••••••"
            />
          </div>
          
          <button type="submit" className="w-full btn-primary">
            Iniciar Sesión
          </button>
        </form>
        
        <p className="text-center text-sm text-slate-600 mt-6">
          ¿No tienes cuenta?{' '}
          <a href="/register" className="text-primary-600 hover:text-primary-500">
            Regístrate aquí
          </a>
        </p>
      </div>
    </div>
  )
}

export default Login
