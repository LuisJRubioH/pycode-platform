/**
 * Lectura de los errores que devuelve FastAPI.
 *
 * Un 422 de validación trae `detail` como lista de objetos con `loc` (la ruta
 * del campo que falló) y `msg`. Hasta ahora el front se quedaba solo con el
 * `msg` del primero y tiraba el `loc`, así que el aviso aparecía en un banner
 * genérico encima del formulario sin decir de qué campo hablaba: un alumno leyó
 * un error del nombre de usuario como si fuera de la contraseña y estuvo
 * cambiándola intento tras intento. Conservar `loc` es lo que permite pintar
 * cada mensaje dentro de su campo.
 */

export type ErroresPorCampo = Record<string, string>

interface ErrorDeValidacion {
  loc?: unknown
  msg?: unknown
}

/** El último segmento de `loc` es el nombre del campo: ['body', 'username']. */
function campoDe(loc: unknown): string | null {
  if (!Array.isArray(loc) || loc.length === 0) return null
  const ultimo = loc[loc.length - 1]
  return typeof ultimo === 'string' ? ultimo : null
}

/**
 * Agrupa un `detail` de 422 por campo. Si un campo falla por varios motivos,
 * se queda el primero: encadenar mensajes en un input estrecho no se lee.
 */
export function erroresPorCampo(detail: unknown): ErroresPorCampo {
  if (!Array.isArray(detail)) return {}

  const errores: ErroresPorCampo = {}
  for (const entrada of detail as ErrorDeValidacion[]) {
    if (!entrada || typeof entrada !== 'object') continue
    const campo = campoDe(entrada.loc)
    const mensaje = typeof entrada.msg === 'string' ? entrada.msg : null
    if (campo && mensaje && !errores[campo]) {
      errores[campo] = mensaje
    }
  }
  return errores
}

/**
 * Un mensaje suelto para los errores que no cuelgan de un campo concreto
 * (los `HTTPException` del backend, donde `detail` es un string).
 */
export function mensajeDeError(detail: unknown, respaldo: string): string {
  if (typeof detail === 'string' && detail.trim()) return detail
  const errores = erroresPorCampo(detail)
  const primero = Object.values(errores)[0]
  return primero ?? respaldo
}

/** Error de API que además sabe qué campos del formulario fallaron. */
export class ErrorDeApi extends Error {
  readonly campos: ErroresPorCampo
  readonly status: number

  constructor(mensaje: string, campos: ErroresPorCampo = {}, status = 0) {
    super(mensaje)
    this.name = 'ErrorDeApi'
    this.campos = campos
    this.status = status
  }
}

/** Construye el ErrorDeApi a partir de una respuesta fallida. */
export async function errorDesdeRespuesta(
  respuesta: Response,
  respaldo: string
): Promise<ErrorDeApi> {
  const cuerpo = await respuesta.json().catch(() => ({}))
  const detail = (cuerpo as { detail?: unknown }).detail
  return new ErrorDeApi(
    mensajeDeError(detail, respaldo),
    erroresPorCampo(detail),
    respuesta.status
  )
}
