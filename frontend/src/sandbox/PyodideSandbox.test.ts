import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'

// Kernel falso: `run` late (como el worker real antes de entrar al codigo del
// alumno) y no termina nunca, que es lo que produce un `while True:`.
const kernels: Array<{ setAuthToken: (token: string) => Promise<void> }> = []
vi.mock('comlink', () => ({
  proxy: <T,>(fn: T) => fn,
  wrap: () => {
    const kernel = {
      init: vi.fn(async () => ({})),
      setAuthToken: vi.fn(async () => {}),
      run: vi.fn((_req: unknown, latido?: () => void) => {
        latido?.()
        return new Promise(() => {})
      }),
    }
    kernels.push(kernel)
    return kernel
  },
}))

const terminados: FakeWorker[] = []
class FakeWorker {
  terminate() {
    terminados.push(this)
  }
}

import { PyodideSandbox } from './PyodideSandbox'
import { SandboxAbortedError, SandboxTimeoutError } from './watchdog'

describe('PyodideSandbox — limite duro (issue #32)', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    vi.stubGlobal('Worker', FakeWorker)
    kernels.length = 0
    terminados.length = 0
  })
  afterEach(() => {
    vi.useRealTimers()
    vi.unstubAllGlobals()
  })

  it('un bucle infinito mata el worker, rechaza con timeout y la siguiente ejecucion levanta otro', async () => {
    const sandbox = new PyodideSandbox()
    const p = sandbox.run('while True: pass', 1_000)
    const verificacion = expect(p).rejects.toBeInstanceOf(SandboxTimeoutError)

    await vi.advanceTimersByTimeAsync(1_000 + 3_000)
    await verificacion
    expect(terminados).toHaveLength(1)
    expect(sandbox.status).toBe('error')

    void sandbox.run('print(1)', 1_000).catch(() => {})
    await vi.advanceTimersByTimeAsync(0)
    expect(kernels).toHaveLength(2)
  })

  it('"Detener" rechaza TODAS las ejecuciones en vuelo, no solo la ultima', async () => {
    const sandbox = new PyodideSandbox()
    const a = sandbox.run('while True: pass')
    const b = sandbox.run('while True: pass')
    const va = expect(a).rejects.toBeInstanceOf(SandboxAbortedError)
    const vb = expect(b).rejects.toBeInstanceOf(SandboxAbortedError)
    await vi.advanceTimersByTimeAsync(0)

    sandbox.abortRun()

    await va
    await vb
    expect(terminados).toHaveLength(1)
    // Detener no es un fallo: la cabecera no debe quedar en rojo.
    expect(sandbox.status).toBe('ready')
  })

  it('el temporizador de un worker ya abortado no mata al worker nuevo', async () => {
    const sandbox = new PyodideSandbox()
    const vieja = sandbox.run('while True: pass', 1_000)
    void vieja.catch(() => {})
    await vi.advanceTimersByTimeAsync(0)
    sandbox.abortRun()

    // Nueva ejecucion larga (30 s de limite) en un worker nuevo.
    const nueva = sandbox.run('while True: pass', 30_000)
    void nueva.catch(() => {})
    await vi.advanceTimersByTimeAsync(0)
    expect(terminados).toHaveLength(1)

    // Pasa de sobra el limite de la ejecucion vieja: el nuevo sigue vivo.
    await vi.advanceTimersByTimeAsync(10_000)
    expect(terminados).toHaveLength(1)
  })

  it('el worker nuevo recibe el token de sesion que tenia el anterior', async () => {
    const sandbox = new PyodideSandbox()
    await sandbox.setAuthToken('tok-123')
    void sandbox.run('while True: pass').catch(() => {})
    await vi.advanceTimersByTimeAsync(0)
    sandbox.abortRun()

    await sandbox.init()
    expect(kernels[1].setAuthToken).toHaveBeenCalledWith('tok-123')
  })
})
