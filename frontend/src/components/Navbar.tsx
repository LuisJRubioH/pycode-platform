import React from 'react'
import { Link } from 'react-router-dom'
import { Code2, Menu, X } from 'lucide-react'

const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = React.useState(false)

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
            <Link to="/editor" className="text-slate-600 hover:text-slate-900">
              Editor
            </Link>
            <Link to="/tutor" className="text-slate-600 hover:text-slate-900">
              Tutor IA
            </Link>
            <Link to="/dashboard" className="text-slate-600 hover:text-slate-900">
              Dashboard
            </Link>
            <Link to="/login" className="btn-primary">
              Iniciar Sesión
            </Link>
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
              <Link to="/lessons" className="text-slate-600 hover:text-slate-900">
                Lecciones
              </Link>
              <Link to="/editor" className="text-slate-600 hover:text-slate-900">
                Editor
              </Link>
              <Link to="/tutor" className="text-slate-600 hover:text-slate-900">
                Tutor IA
              </Link>
              <Link to="/dashboard" className="text-slate-600 hover:text-slate-900">
                Dashboard
              </Link>
              <Link to="/login" className="btn-primary">
                Iniciar Sesión
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar
