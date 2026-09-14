import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Link, MemoryRouter } from 'react-router-dom'

// Puzzles falla al cargar (como un chunk borrado por un deploy); Retos no.
vi.mock('./pages/Puzzles', () => {
  throw new Error('Failed to fetch dynamically imported module')
})
vi.mock('./pages/Challenges', () => ({ default: () => <p>Pagina de retos</p> }))
vi.mock('./components/Layout', async () => {
  const { Outlet } = await import('react-router-dom')
  return {
    default: () => (
      <div>
        <Link to="/puzzles">Puzzles</Link>
        <Link to="/challenges">Retos</Link>
        <Outlet />
      </div>
    ),
  }
})

import App from './App'

describe('App — paginas en chunks', () => {
  beforeEach(() => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
  })

  it('si una pagina no carga, avisa sin tumbar la app y las demas siguen funcionando', async () => {
    const user = userEvent.setup()
    render(
      <MemoryRouter initialEntries={['/puzzles']}>
        <App />
      </MemoryRouter>
    )

    expect(await screen.findByText('No se pudo cargar esta pagina.')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Recargar' })).toBeInTheDocument()
    // La navegacion sigue en pantalla...
    expect(screen.getByRole('link', { name: 'Retos' })).toBeInTheDocument()

    // ...y otra pagina carga sin arrastrar el error de la anterior.
    await user.click(screen.getByRole('link', { name: 'Retos' }))
    expect(await screen.findByText('Pagina de retos')).toBeInTheDocument()
    expect(screen.queryByText('No se pudo cargar esta pagina.')).not.toBeInTheDocument()
  })
})
