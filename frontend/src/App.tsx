import { Component, lazy, Suspense, type ErrorInfo, type ReactNode } from 'react'
import { Routes, Route, useLocation } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout'
import './index.css'

// Cada pagina se descarga al visitarla. Antes todo iba en un unico JS de
// 1,1 MB: quien entraba a /login descargaba tambien recharts (Dashboard),
// react-markdown con highlight.js (lecciones, retos) y el resto de paginas.
const Home = lazy(() => import('./pages/Home'))
const Login = lazy(() => import('./pages/Login'))
const Register = lazy(() => import('./pages/Register'))
const Dashboard = lazy(() => import('./pages/Dashboard'))
const CodeEditor = lazy(() => import('./pages/CodeEditor'))
const Lessons = lazy(() => import('./pages/Lessons'))
const LessonDetail = lazy(() => import('./pages/LessonDetail'))
const Competencies = lazy(() => import('./pages/Competencies'))
const CapstoneDetail = lazy(() => import('./pages/CapstoneDetail'))
const CertificateVerify = lazy(() => import('./pages/CertificateVerify'))
const TutorChat = lazy(() => import('./pages/TutorChat'))
const Challenges = lazy(() => import('./pages/Challenges'))
const Puzzles = lazy(() => import('./pages/Puzzles'))
const InterviewProblems = lazy(() => import('./pages/InterviewProblems'))

function CargandoPagina() {
  return (
    <div role="status" className="card p-6 text-sm text-slate-500">
      Cargando...
    </div>
  )
}

// Si el chunk de una pagina no llega (sin red, o un deploy lo borro y la
// recarga automatica de main.tsx ya se intento), React.lazy lanza. Sin este
// limite, el error desmontaba la app entera y quedaba la pantalla en blanco.
class LimiteDePagina extends Component<{ children: ReactNode }, { error: boolean }> {
  state = { error: false }

  static getDerivedStateFromError() {
    return { error: true }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('No se pudo mostrar la pagina:', error, info.componentStack)
  }

  render() {
    if (!this.state.error) return this.props.children
    return (
      <div role="alert" className="card p-6 space-y-3">
        <p className="font-semibold text-slate-900">No se pudo cargar esta pagina.</p>
        <p className="text-sm text-slate-600">
          Puede que se haya publicado una version nueva de PyCode o que falle la conexion.
        </p>
        <button onClick={() => window.location.reload()} className="btn-primary">
          Recargar
        </button>
      </div>
    )
  }
}

// React reutiliza el limite al cambiar de ruta (mismo tipo, misma posicion) y
// con el su estado de error: sin la clave, tras un fallo todas las paginas
// seguian mostrando el aviso. Se usa el pathname y no la URL entera para que el
// editor, que cambia de ejercicio con ?lesson=, no se remonte.
function LimiteConRuta({ children }: { children: ReactNode }) {
  const { pathname } = useLocation()
  return <LimiteDePagina key={pathname}>{children}</LimiteDePagina>
}

// El Suspense va dentro de cada ruta y no alrededor de <Routes>: asi la barra
// de navegacion (Layout) se queda en pantalla mientras llega la pagina.
const pagina = (Pagina: React.ComponentType) => (
  <LimiteConRuta>
    <Suspense fallback={<CargandoPagina />}>
      <Pagina />
    </Suspense>
  </LimiteConRuta>
)

function App() {
  return (
    <>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={pagina(Home)} />
          <Route path="login" element={pagina(Login)} />
          <Route path="register" element={pagina(Register)} />
          <Route path="dashboard" element={pagina(Dashboard)} />
          <Route path="editor" element={pagina(CodeEditor)} />
          <Route path="lessons" element={pagina(Lessons)} />
          <Route path="lessons/:lessonId" element={pagina(LessonDetail)} />
          <Route path="competencias" element={pagina(Competencies)} />
          <Route path="capstones/:slug" element={pagina(CapstoneDetail)} />
          <Route path="verify/:code" element={pagina(CertificateVerify)} />
          <Route path="challenges" element={pagina(Challenges)} />
          <Route path="puzzles" element={pagina(Puzzles)} />
          <Route path="interview" element={pagina(InterviewProblems)} />
          <Route path="tutor" element={pagina(TutorChat)} />
        </Route>
      </Routes>
    </>
  )
}

export default App
