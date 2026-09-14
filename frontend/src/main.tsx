import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App.tsx'
import './index.css'

// Con las paginas en chunks separados (React.lazy), un deploy nuevo borra los
// chunks del anterior: una pestana abierta de antes falla al navegar a una
// pagina que aun no habia cargado. Vite avisa con este evento; se recarga para
// traer el index.html nuevo. Como mucho una recarga por minuto: si el fallo
// fuera otro (sin red, por ejemplo), no entra en un bucle de recargas.
window.addEventListener('vite:preloadError', (event) => {
  const CLAVE = 'pycode_recarga_por_chunk'
  try {
    const ultima = Number(sessionStorage.getItem(CLAVE) || 0)
    if (Date.now() - ultima < 60_000) return
    sessionStorage.setItem(CLAVE, String(Date.now()))
  } catch {
    return
  }
  event.preventDefault()
  window.location.reload()
})

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>,
)
