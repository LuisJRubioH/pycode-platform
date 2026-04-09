import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import CodeEditor from './pages/CodeEditor'
import Lessons from './pages/Lessons'
import TutorChat from './pages/TutorChat'
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
          <Route path="tutor" element={<TutorChat />} />
        </Route>
      </Routes>
    </>
  )
}

export default App
