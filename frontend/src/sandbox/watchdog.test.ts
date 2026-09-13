import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { conWatchdog, SandboxTimeoutError } from './watchdog'

// Una operacion que no termina nunca: es lo que ve el hilo principal cuando
// el worker esta atrapado en un `while True:`.
const nuncaTermina = () => new Promise<never>(() => {})

describe('conWatchdog (issue #32)', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })
  afterEach(() => {
    vi.useRealTimers()
  })

  it('corta y avisa si el worker deja de latir', async () => {
    const alExpirar = vi.fn()
    const p = conWatchdog(
      (latido) => {
        latido()
        return nuncaTermina()
      },
      1_000,
      alExpirar,
    )
    const verificacion = expect(p).rejects.toBeInstanceOf(SandboxTimeoutError)

    await vi.advanceTimersByTimeAsync(999)
    expect(alExpirar).not.toHaveBeenCalled()
    await vi.advanceTimersByTimeAsync(1)
    expect(alExpirar).toHaveBeenCalledTimes(1)
    await verificacion
  })

  it('no arranca el reloj hasta el primer latido (la carga de paquetes no cuenta)', async () => {
    const alExpirar = vi.fn()
    let latir!: () => void
    void conWatchdog(
      (latido) => {
        latir = latido
        return nuncaTermina()
      },
      1_000,
      alExpirar,
    ).catch(() => {})

    // Simula numpy bajando del CDN: mucho tiempo sin latido y sin corte.
    await vi.advanceTimersByTimeAsync(10_000)
    expect(alExpirar).not.toHaveBeenCalled()

    latir()
    await vi.advanceTimersByTimeAsync(1_000)
    expect(alExpirar).toHaveBeenCalledTimes(1)
  })

  it('cada latido rearma el limite: una tanda larga que avanza no se mata', async () => {
    const alExpirar = vi.fn()
    let latir!: () => void
    let terminar!: (v: string) => void
    const p = conWatchdog(
      (latido) => {
        latir = latido
        return new Promise<string>((resolve) => {
          terminar = resolve
        })
      },
      1_000,
      alExpirar,
    )

    // Cinco tests de 800 ms: 4 s en total, pero nunca 1 s sin latir.
    for (let i = 0; i < 5; i++) {
      latir()
      await vi.advanceTimersByTimeAsync(800)
    }
    terminar('ok')

    await expect(p).resolves.toBe('ok')
    expect(alExpirar).not.toHaveBeenCalled()
  })

  it('al terminar limpia el temporizador: no mata un worker que ya acabo', async () => {
    const alExpirar = vi.fn()
    const p = conWatchdog(
      async (latido) => {
        latido()
        return 42
      },
      1_000,
      alExpirar,
    )

    await expect(p).resolves.toBe(42)
    await vi.advanceTimersByTimeAsync(5_000)
    expect(alExpirar).not.toHaveBeenCalled()
  })

  it('el mensaje de corte esta escrito para el alumno', () => {
    const err = new SandboxTimeoutError(33_000)
    expect(err.message).toContain('33 s')
    expect(err.message).toContain('bucle')
    expect(err.message).toContain('puedes volver a ejecutar')
  })
})
