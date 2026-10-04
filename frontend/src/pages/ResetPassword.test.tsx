import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Routes, Route } from 'react-router-dom'

import ResetPassword from './ResetPassword'
import ForgotPassword from './ForgotPassword'

function montar(ruta: string) {
  return render(
    <MemoryRouter initialEntries={[ruta]}>
      <Routes>
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/login" element={<p>pantalla de login</p>} />
      </Routes>
    </MemoryRouter>
  )
}

describe('ResetPassword', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn())
  })
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('sin token en la URL ofrece pedir otro enlace en vez de un formulario', () => {
    montar('/reset-password')
    expect(screen.getByText(/enlace incompleto/i)).toBeInTheDocument()
    expect(
      screen.getByRole('link', { name: /pedir un enlace nuevo/i })
    ).toBeInTheDocument()
  })

  it('manda el token junto a la contraseña nueva y lleva al login', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, status: 204 })
    vi.stubGlobal('fetch', fetchMock)
    const usuario = userEvent.setup()
    montar('/reset-password?token=abc123')

    await usuario.type(screen.getByLabelText(/contraseña nueva/i), 'ClaveNueva123')
    await usuario.type(screen.getByLabelText(/repite la contraseña/i), 'ClaveNueva123')
    await usuario.click(screen.getByRole('button', { name: /guardar contraseña/i }))

    await waitFor(() => expect(fetchMock).toHaveBeenCalled())
    const [url, opciones] = fetchMock.mock.calls[0]
    expect(url).toBe('/api/v1/auth/password-reset/confirm')
    expect(JSON.parse(opciones.body)).toEqual({
      token: 'abc123',
      password: 'ClaveNueva123',
    })
    expect(await screen.findByText(/pantalla de login/i)).toBeInTheDocument()
  })

  it('valida la contraseña en el cliente antes de gastar una llamada', async () => {
    const fetchMock = vi.fn()
    vi.stubGlobal('fetch', fetchMock)
    const usuario = userEvent.setup()
    montar('/reset-password?token=abc123')

    await usuario.type(screen.getByLabelText(/contraseña nueva/i), 'sinnumeros')
    await usuario.type(screen.getByLabelText(/repite la contraseña/i), 'sinnumeros')
    await usuario.click(screen.getByRole('button', { name: /guardar contraseña/i }))

    expect(await screen.findByRole('alert')).toHaveTextContent(/al menos un número/i)
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('con un token caducado explica el motivo y ofrece pedir otro', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: false,
        status: 400,
        json: async () => ({
          detail: 'El enlace de recuperación no es válido, ya se usó o caducó.',
        }),
      })
    )
    const usuario = userEvent.setup()
    montar('/reset-password?token=caducado')

    await usuario.type(screen.getByLabelText(/contraseña nueva/i), 'ClaveNueva123')
    await usuario.type(screen.getByLabelText(/repite la contraseña/i), 'ClaveNueva123')
    await usuario.click(screen.getByRole('button', { name: /guardar contraseña/i }))

    expect(await screen.findByText(/ya se usó o caducó/i)).toBeInTheDocument()
    expect(
      screen.getByRole('link', { name: /pedir un enlace nuevo/i })
    ).toBeInTheDocument()
  })
})

describe('ForgotPassword', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, status: 204 }))
  })
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('acusa recibo sin confirmar si la cuenta existe', async () => {
    const usuario = userEvent.setup()
    montar('/forgot-password')

    await usuario.type(screen.getByLabelText(/email/i), 'alguien@example.com')
    await usuario.click(screen.getByRole('button', { name: /enviarme el enlace/i }))

    // "Si hay una cuenta..." — nunca "te hemos enviado": el backend responde
    // igual exista o no, para no convertir el formulario en un detector de
    // emails registrados.
    expect(await screen.findByText(/si hay una cuenta registrada/i)).toBeInTheDocument()
  })
})
