/**
 * Limite duro para el codigo del alumno (issue #32).
 *
 * El worker corre en un solo hilo: mientras Python gira en codigo sincrono
 * (`while True:`), su event loop no avanza y ningun `setTimeout` de dentro
 * puede dispararse. El unico hilo libre es el principal, asi que el limite
 * tiene que vivir aqui y la unica forma de cortar es `worker.terminate()`.
 *
 * El reloj no arranca con la llamada sino con el primer latido: cargar numpy o
 * pandas desde el CDN tarda lo suyo y no es culpa del alumno. Cada latido lo
 * reinicia, de modo que el limite es "tiempo sin dar senales de vida", no
 * "tiempo total": una tanda de tests lentos de sklearn late entre test y test y
 * no la matamos, mientras que un bucle infinito deja de latir para siempre.
 */

export class SandboxTimeoutError extends Error {
  readonly limitMs: number;

  constructor(limitMs: number) {
    super(
      `Tu codigo lleva mas de ${Math.round(limitMs / 1000)} s sin terminar y se ha ` +
        `detenido. La causa mas comun es un bucle que nunca acaba: revisa que la ` +
        `condicion del while llegue a ser falsa. El sandbox se ha reiniciado, ` +
        `puedes volver a ejecutar.`,
    );
    this.name = "SandboxTimeoutError";
    this.limitMs = limitMs;
  }
}

export class SandboxAbortedError extends Error {
  constructor() {
    super(
      "Ejecucion detenida. El sandbox se ha reiniciado y puedes volver a ejecutar.",
    );
    this.name = "SandboxAbortedError";
  }
}

/**
 * Corre `operacion` vigilada por un limite duro que se rearma con cada latido.
 *
 * @param operacion recibe el `latido` que el worker debe llamar antes de cada
 *   tramo de codigo sincrono.
 * @param limiteMs milisegundos permitidos entre dos latidos.
 * @param alExpirar se llama antes de rechazar: aqui es donde se mata el worker.
 */
export async function conWatchdog<T>(
  operacion: (latido: () => void) => Promise<T>,
  limiteMs: number,
  alExpirar: () => void,
): Promise<T> {
  let temporizador: ReturnType<typeof setTimeout> | undefined;
  let expirado = false;
  let rechazar: ((e: Error) => void) | null = null;

  const limite = new Promise<never>((_, reject) => {
    rechazar = reject;
  });

  const latido = () => {
    if (expirado) return;
    if (temporizador !== undefined) clearTimeout(temporizador);
    temporizador = setTimeout(() => {
      expirado = true;
      alExpirar();
      rechazar?.(new SandboxTimeoutError(limiteMs));
    }, limiteMs);
  };

  try {
    return await Promise.race([operacion(latido), limite]);
  } finally {
    if (temporizador !== undefined) clearTimeout(temporizador);
  }
}
