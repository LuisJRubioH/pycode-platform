import React from 'react'
import { Link } from 'react-router-dom'
import { Code2, BookOpen, MessageSquare, Trophy } from 'lucide-react'
import PuzzleOfTheDay from '../components/PuzzleOfTheDay'

const Home: React.FC = () => {
  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center py-16">
        <h1 className="text-5xl font-bold text-slate-900 mb-6">
          Aprende Python con un
          <span className="text-primary-600"> Tutor IA</span>
        </h1>
        <p className="text-xl text-slate-600 max-w-3xl mx-auto mb-8">
          Plataforma de aprendizaje interactiva con ejecución de código en tiempo real, 
          lecciones personalizadas y tutoría IA socrática que se adapta a tu nivel.
        </p>
        <div className="flex justify-center gap-4">
          <Link to="/register" className="btn-primary text-lg px-8 py-3">
            Comenzar Gratis
          </Link>
          <Link to="/editor" className="btn-secondary text-lg px-8 py-3">
            Probar Editor
          </Link>
        </div>
      </section>

      {/* Puzzle del día (público) */}
      <PuzzleOfTheDay />

      {/* Features */}
      <section className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
        <FeatureCard
          icon={<Code2 className="h-8 w-8" />}
          title="Editor en Vivo"
          description="Ejecuta código Python directamente en el navegador con ejecución segura en Docker."
        />
        <FeatureCard
          icon={<BookOpen className="h-8 w-8" />}
          title="Lecciones Estructuradas"
          description="Desde básico hasta avanzado, con lecciones que se adaptan a tu ritmo de aprendizaje."
        />
        <FeatureCard
          icon={<MessageSquare className="h-8 w-8" />}
          title="Tutor IA Socrático"
          description="Recibe guía personalizada que te ayuda a pensar, no solo a encontrar respuestas."
        />
        <FeatureCard
          icon={<Trophy className="h-8 w-8" />}
          title="Progreso Gamificado"
          description="Gana puntos, insignias y sigue tu evolución con estadísticas detalladas."
        />
      </section>

      {/* CTA */}
      <section className="bg-primary-600 rounded-2xl p-12 text-center text-white">
        <h2 className="text-3xl font-bold mb-4">
          ¿Listo para comenzar tu viaje en Python?
        </h2>
        <p className="text-primary-100 mb-8 max-w-2xl mx-auto">
          Únete a miles de estudiantes que están mejorando sus habilidades de programación 
          con nuestra plataforma open source.
        </p>
        <Link 
          to="/register" 
          className="inline-block bg-white text-primary-600 font-semibold px-8 py-3 rounded-lg hover:bg-primary-50 transition-colors"
        >
          Crear Cuenta Gratis
        </Link>
      </section>
    </div>
  )
}

const FeatureCard: React.FC<{ icon: React.ReactNode; title: string; description: string }> = ({ 
  icon, 
  title, 
  description 
}) => (
  <div className="card p-6 text-center hover:shadow-md transition-shadow">
    <div className="text-primary-600 mb-4 flex justify-center">{icon}</div>
    <h3 className="text-lg font-semibold text-slate-900 mb-2">{title}</h3>
    <p className="text-slate-600 text-sm">{description}</p>
  </div>
)

export default Home
