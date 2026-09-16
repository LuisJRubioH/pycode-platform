import { slugSeccion } from './lessonSecciones'

export type TipoBloque =
  | 'calificacion'
  | 'analisis'
  | 'fuertes'
  | 'mejora'
  | 'recomendaciones'
  | 'normal'

export interface BloqueVeredicto {
  tipo: TipoBloque
  titulo: string
  cuerpo: string
}

// El veredicto siempre trae las mismas cabeceras porque el prompt evaluador las
// impone, pero NO siempre con el mismo Markdown: el modelo escribe
// `**CALIFICACIÓN:**`, `### ANÁLISIS DETALLADO` o `#### PUNTOS FUERTES`, y el
// texto de reserva del backend las escribe a pelo y sin tildes. Por eso se
// reconocen por el slug de la linea, no por su formato.
const CABECERAS: { tipo: TipoBloque; prefijo: string }[] = [
  { tipo: 'calificacion', prefijo: 'calificacion' },
  { tipo: 'fuertes', prefijo: 'puntos-fuertes' },
  { tipo: 'mejora', prefijo: 'areas-de-mejora' },
  { tipo: 'recomendaciones', prefijo: 'recomendaciones' },
  { tipo: 'analisis', prefijo: 'analisis-detallado' },
]

/** Quita el adorno de Markdown de una linea para quedarse con su texto. */
function desnudar(linea: string): string {
  return linea
    .replace(/^[\s>]*[-*+]?\s*/, '')
    .replace(/[#*_`:~]/g, '')
    .trim()
}

/**
 * Una linea es cabecera si, desnuda, empieza por uno de los titulos conocidos.
 *
 * El tope de longitud evita que una linea de contenido que MENCIONE el titulo
 * abra un bloque; las cabeceras reales son cortas.
 */
function cabeceraDe(linea: string): TipoBloque | null {
  const texto = desnudar(linea)
  if (!texto || texto.length > 40) return null
  const slug = slugSeccion(texto)
  return CABECERAS.find((c) => slug.startsWith(c.prefijo))?.tipo ?? null
}

/**
 * Parte el veredicto crudo del tutor en sus bloques.
 *
 * Lo que aparece antes de la primera cabecera se devuelve como bloque
 * `normal`: nunca se descarta texto, porque si el modelo se sale del formato
 * el alumno tiene que seguir viendo su retroalimentacion entera.
 */
export function partirVeredicto(raw: string): BloqueVeredicto[] {
  const bloques: BloqueVeredicto[] = []
  let actual: BloqueVeredicto | null = null
  let enCodigo = false
  const previo: string[] = []

  for (const linea of raw.split('\n')) {
    if (/^\s*(```|~~~)/.test(linea)) enCodigo = !enCodigo

    const tipo = enCodigo ? null : cabeceraDe(linea)
    if (tipo) {
      if (actual) bloques.push(actual)
      actual = { tipo, titulo: desnudar(linea), cuerpo: '' }
      continue
    }

    if (actual) actual.cuerpo += `${linea}\n`
    else previo.push(linea)
  }
  if (actual) bloques.push(actual)

  const intro = previo.join('\n').trim()
  if (intro) bloques.unshift({ tipo: 'normal', titulo: '', cuerpo: intro })

  return bloques
    .map((b) => ({ ...b, cuerpo: b.cuerpo.trim() }))
    // "ANALISIS DETALLADO" es solo un paraguas sobre los tres bloques
    // siguientes: sin cuerpo propio, una tarjeta vacia solo mete ruido.
    .filter((b) => b.cuerpo !== '' || b.tipo === 'normal')
}

export type Tono = 'excelente' | 'bien' | 'regular' | 'flojo' | 'sin-nota'

/**
 * Tramo de la nota. Los cortes son los de siempre en la plataforma: 85 es
 * "ya esta", 70 "va encaminado", 50 "funciona pero hay trabajo".
 */
export function tonoDeNota(nota: number | null): Tono {
  if (nota === null) return 'sin-nota'
  if (nota >= 85) return 'excelente'
  if (nota >= 70) return 'bien'
  if (nota >= 50) return 'regular'
  return 'flojo'
}

export const ETIQUETA_TONO: Record<Tono, string> = {
  excelente: 'Excelente',
  bien: 'Bien',
  regular: 'Aceptable',
  flojo: 'A revisar',
  'sin-nota': 'Sin nota',
}
