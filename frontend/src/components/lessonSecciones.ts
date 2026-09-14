import { useEffect, useState } from 'react'

export type TipoSeccion = 'objetivo' | 'errores' | 'resumen' | 'normal'

export interface Seccion {
  id: string
  titulo: string
  cuerpo: string
  tipo: TipoSeccion
}

/**
 * Ancla estable para un titulo: sin tildes, en minusculas y con guiones.
 * "Indexacion: tres formas (no las mezcles)" -> "indexacion-tres-formas-no-las-mezcles".
 */
export function slugSeccion(titulo: string): string {
  return (
    titulo
      .normalize('NFD')
      .replace(/[̀-ͯ]/g, '')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '') || 'seccion'
  )
}

// Las lecciones no traen etiquetas "Objetivo" o "Teoria": lo que si traen,
// siempre con el mismo titulo, es la apertura ("Por que ..."), "Errores
// comunes" (36 de 40) y "Resumen" (40 de 40). Los bloques semanticos salen de ahi.
function tipoDe(titulo: string): TipoSeccion {
  const t = slugSeccion(titulo)
  if (t.startsWith('por-que')) return 'objetivo'
  if (t.startsWith('errores-comunes')) return 'errores'
  if (t.startsWith('resumen')) return 'resumen'
  return 'normal'
}

/**
 * Parte el Markdown de una leccion en sus secciones `##`.
 *
 * Un `##` dentro de un bloque de codigo (un comentario de Python, por ejemplo)
 * no abre seccion. Lo que va antes del primer `##` queda en `intro`.
 */
export function partirEnSecciones(markdown: string): { intro: string; secciones: Seccion[] } {
  const intro: string[] = []
  const secciones: Seccion[] = []
  const usados = new Map<string, number>()
  let actual: { titulo: string; lineas: string[] } | null = null
  let enCodigo = false

  const cerrar = () => {
    if (!actual) return
    const base = slugSeccion(actual.titulo)
    const repeticiones = usados.get(base) ?? 0
    usados.set(base, repeticiones + 1)
    secciones.push({
      id: repeticiones ? `${base}-${repeticiones + 1}` : base,
      titulo: actual.titulo,
      cuerpo: actual.lineas.join('\n').trim(),
      tipo: tipoDe(actual.titulo),
    })
  }

  for (const linea of markdown.split('\n')) {
    if (/^\s*(```|~~~)/.test(linea)) enCodigo = !enCodigo
    const titulo = !enCodigo && /^## (?!#)(.+)$/.exec(linea)
    if (titulo) {
      cerrar()
      actual = { titulo: titulo[1].trim(), lineas: [] }
    } else if (actual) {
      actual.lineas.push(linea)
    } else {
      intro.push(linea)
    }
  }
  cerrar()
  return { intro: intro.join('\n').trim(), secciones }
}

/**
 * Id de la seccion que se esta leyendo, para marcarla en el indice. Sin
 * IntersectionObserver (jsdom, navegadores muy viejos) simplemente no marca.
 */
export function useSeccionVisible(ids: string[]): string | null {
  const [visible, setVisible] = useState<string | null>(null)
  const clave = ids.join('|')

  useEffect(() => {
    if (typeof IntersectionObserver === 'undefined') return
    const elementos = clave
      .split('|')
      .map((id) => document.getElementById(id))
      .filter((el): el is HTMLElement => el !== null)
    if (elementos.length === 0) return
    // La franja superior de la ventana decide cual es "la actual".
    const observer = new IntersectionObserver(
      (entradas) => {
        const arriba = entradas
          .filter((e) => e.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0]
        if (arriba) setVisible(arriba.target.id)
      },
      { rootMargin: '0px 0px -70% 0px' }
    )
    elementos.forEach((el) => observer.observe(el))
    return () => observer.disconnect()
  }, [clave])

  return visible
}
