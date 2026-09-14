/**
 * Tipos compartidos de los ejercicios de Track 0 (los que no se ejecutan).
 *
 * El contrato de un tipo de ejercicio es pequeño a propósito: recibe su `spec`
 * (el enunciado estructurado que manda el backend) y un par valor/onChange con
 * la respuesta del alumno. No sabe nada de HTTP ni de progreso: de eso se
 * ocupa `ExerciseRunner`, así que añadir un tipo es escribir un componente y
 * registrarlo en el mapa.
 */

/** Lo que el alumno ha respondido. Su forma depende del tipo. */
export type Respuesta = Record<string, unknown>

/** Dónde falla la respuesta, para marcarlo en la UI. */
export interface Detalle {
  fila?: number
  columna?: number
  linea?: number
}

export interface PropsTipo<Spec = Record<string, unknown>> {
  spec: Spec
  valor: Respuesta
  onChange: (valor: Respuesta) => void
  /** Señalado por el backend tras un intento fallido. */
  detalle?: Detalle
  /** Ya aprobado: se deja ver, pero no se toca. */
  deshabilitado?: boolean
}

export interface SpecTraceTable {
  pseudocodigo?: string
  columnas: string[]
  filas: { etiqueta: string; fijas?: (string | null)[] }[]
  ayuda?: string
}

export interface SpecPredictOutput {
  pseudocodigo?: string
  ayuda?: string
}

export interface SpecMcq {
  pregunta?: string
  pseudocodigo?: string
  opciones: string[]
}
