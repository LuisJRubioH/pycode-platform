import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Code2, Menu, X, LogOut } from 'lucide-react'
import { useAuthStore } from '../stores/authStore'

const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = React.useState(false)
  const { isAuthenticated, user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
    setIsOpen(false)
  }

  return (
    <nav className="bg-white shadow-sm border-b border-slate-200">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <Code2 className="h-8 w-8 text-primary-600" />
            <span className="text-xl font-bold text-slate-900">PyCode</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/lessons" className="text-slate-600 hover:text-slate-900">
              Lecciones
            </Link>
            <Link to="/competencias" className="text-slate-600 hover:text-slate-900">
              Competencias
            </Link>
            <Link to="/editor" className="text-slate-600 hover:text-slate-900">
              Editor
            </Link>
            <Link to="/challenges" className="text-slate-600 hover:text-slate-900">
              Retos
            </Link>
            <Link to="/puzzles" className="text-slate-600 hover:text-slate-900">
              Puzzles
            </Link>
            <Link to="/interview" className="text-slate-600 hover:text-slate-900">
              Entrevista
            </Link>
            <Link to="/tutor" className="text-slate-600 hover:text-slate-900">
              Tutor IA
            </Link>
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="text-slate-600 hover:text-slate-900">
                  Dashboard
                </Link>
                <span className="text-sm text-slate-500">
                  {user?.username}
                </span>
                <button onClick={handleLogout} className="flex items-center gap-1 text-slate-600 hover:text-red-600">
                  <LogOut className="h-4 w-4" />
                  Salir
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-slate-600 hover:text-slate-900">
                  Iniciar Sesión
                </Link>
                <Link to="/register" className="btn-primary">
                  Registrarse
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 text-slate-600 hover:text-slate-900"
          >
            {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden py-4 border-t border-slate-200">
            <div className="flex flex-col space-y-4">
              <Link to="/lessons" className="text-slate-600 hover:text-slate-900" onClick={() => setIsOpen(false)}>
                Lecciones
              </Link>
              <Link to="/competencias" className="text-slate-600 hover:text-slate-900" onClick={() => setIsOpen(false)}>
                Competencias
              </Link>
              <Link to="/editor" className="text-slate-600 hover:text-slate-900" onClick={() => setIsOpen(false)}>
                Editor
              </Link>
              <Link to="/challenges" className="text-slate-600 hover:text-slate-900" onClick={() => setIsOpen(false)}>
                Retos
              </Link>
              <Link to="/puzzles" className="text-slate-600 hover:text-slate-900" onClick={() => setIsOpen(false)}>
                Puzzles
              </Link>
              <Link to="/interview" className="text-slate-600 hover:text-slate-900" onClick={() => setIsOpen(false)}>
                Entrevista
              </Link>
              <Link to="/tutor" className="text-slate-600 hover:text-slate-900" onClick={() => setIsOpen(false)}>
                Tutor IA
              </Link>
              {isAuthenticated ? (
                <>
                  <Link to="/dashboard" className="text-slate-600 hover:text-slate-900" onClick={() => setIsOpen(false)}>
                    Dashboard
                  </Link>
                  <button onClick={handleLogout} className="flex items-center gap-1 text-slate-600 hover:text-red-600 text-left">
                    <LogOut className="h-4 w-4" />
                    Cerrar Sesión
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="text-slate-600 hover:text-slate-900" onClick={() => setIsOpen(false)}>
                    Iniciar Sesión
                  </Link>
                  <Link to="/register" className="btn-primary text-center" onClick={() => setIsOpen(false)}>
                    Registrarse
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar
