import { Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import CodeEditor from './pages/CodeEditor'
import Lessons from './pages/Lessons'
import LessonDetail from './pages/LessonDetail'
import Competencies from './pages/Competencies'
import CapstoneDetail from './pages/CapstoneDetail'
import CertificateVerify from './pages/CertificateVerify'
import TutorChat from './pages/TutorChat'
import Challenges from './pages/Challenges'
import Puzzles from './pages/Puzzles'
import InterviewProblems from './pages/InterviewProblems'
import './index.css'

function App() {
  return (
    <>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="login" element={<Login />} />
          <Route path="register" element={<Register />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="editor" element={<CodeEditor />} />
          <Route path="lessons" element={<Lessons />} />
          <Route path="lessons/:lessonId" element={<LessonDetail />} />
          <Route path="competencias" element={<Competencies />} />
          <Route path="capstones/:slug" element={<CapstoneDetail />} />
          <Route path="verify/:code" element={<CertificateVerify />} />
          <Route path="challenges" element={<Challenges />} />
          <Route path="puzzles" element={<Puzzles />} />
          <Route path="interview" element={<InterviewProblems />} />
          <Route path="tutor" element={<TutorChat />} />
        </Route>
      </Routes>
    </>
  )
}

export default App
