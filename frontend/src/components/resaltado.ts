import type { Element, ElementContent, Root, RootContent } from 'hast'
import { createLowlight } from 'lowlight'
import python from 'highlight.js/lib/languages/python'

/**
 * Resaltado de sintaxis para react-markdown, solo con los lenguajes que usa el
 * contenido.
 *
 * Sustituye a rehype-highlight, que importa siempre las 37 gramaticas `common`
 * de lowlight aunque le pases otras: el chunk de Markdown pesaba 180 kB para
 * resaltar un unico lenguaje. Los bloques del temario son `python` (186) o sin
 * etiqueta (274, que se quedan sin resaltar, igual que con rehype-highlight).
 *
 * Para anadir un lenguaje: importar su gramatica de `highlight.js/lib/languages`
 * y registrarla abajo.
 */
const lowlight = createLowlight({ python })
lowlight.registerAlias({ python: ['py'] })

function lenguajeDe(code: Element): string | null {
  const clases = code.properties?.className
  const lista = Array.isArray(clases) ? clases : []
  for (const clase of lista) {
    const valor = String(clase)
    if (valor === 'no-highlight' || valor === 'nohighlight') return null
    if (valor.startsWith('language-')) return valor.slice('language-'.length)
  }
  return null
}

function textoDe(nodo: ElementContent): string {
  if (nodo.type === 'text') return nodo.value
  if (nodo.type === 'element') return nodo.children.map(textoDe).join('')
  return ''
}

function recorrer(nodo: Root | RootContent, padre: Root | Element | null) {
  if (nodo.type === 'element' && nodo.tagName === 'code' && padre && 'tagName' in padre && padre.tagName === 'pre') {
    const lenguaje = lenguajeDe(nodo)
    if (lenguaje && lowlight.registered(lenguaje)) {
      const resultado = lowlight.highlight(lenguaje, nodo.children.map(textoDe).join(''))
      const clases = Array.isArray(nodo.properties.className) ? nodo.properties.className : []
      nodo.properties.className = ['hljs', ...clases]
      nodo.children = resultado.children as ElementContent[]
    }
    return
  }
  if ('children' in nodo) {
    for (const hijo of nodo.children) recorrer(hijo, nodo.type === 'root' || nodo.type === 'element' ? nodo : padre)
  }
}

export default function resaltarCodigo() {
  return (arbol: Root) => {
    recorrer(arbol, null)
  }
}
