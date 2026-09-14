import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import CapstoneDetail from './CapstoneDetail'

const getMock = vi.fn()
vi.mock('../services/api', () => ({
  api: {
    get: (...args: unknown[]) => getMock(...args),
    post: vi.fn(),
  },
}))
vi.mock('../sandbox/PyodideSandbox', () => ({ getSandbox: vi.fn() }))

const detalle = {
  id: 5,
  slug: 'track-5-nebula-rag',
  track: 'track-5',
  title: 'Nebula RAG: el asistente completo',
  short_description: 'Asistente completo.',
  description: '## Contexto\n\nTodas reciben `llm_fn`.',
  requirements: [{ id: 'R4', text: 'Devuelve `NO_SE` **sin llamar al LLM**.' }],
  starter_files: [{ path: 'nebula.py', editable: true, content: 'pass\n' }],
  tests_total: 10,
  estimated_hours: 14,
  difficulty: 'advanced',
  order_index: 5,
}

describe('CapstoneDetail — Markdown en enunciado y requisitos', () => {
  it('renderiza el codigo y las negritas en vez de mostrar los signos', async () => {
    getMock.mockImplementation((path: string) =>
      Promise.resolve(
        path.endsWith('/my-submission')
          ? { ok: false, status: 404, json: async () => ({}) }
          : { ok: true, json: async () => detalle },
      ),
    )
    render(
      <MemoryRouter initialEntries={['/capstones/track-5-nebula-rag']}>
        <Routes>
          <Route path="/capstones/:slug" element={<CapstoneDetail />} />
        </Routes>
      </MemoryRouter>,
    )

    expect(await screen.findByRole('heading', { name: 'Contexto' })).toBeInTheDocument()
    expect(screen.getByText('llm_fn').tagName).toBe('CODE')
    // Requisito: sin Markdown se veia "`NO_SE` **sin llamar al LLM**" literal.
    expect(screen.getByText('NO_SE').tagName).toBe('CODE')
    expect(screen.getByText('sin llamar al LLM').tagName).toBe('STRONG')
    expect(screen.queryByText(/\*\*/)).not.toBeInTheDocument()
  })
})
