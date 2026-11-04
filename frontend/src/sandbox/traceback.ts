/**
 * Quita del traceback los frames internos de Pyodide.
 *
 * Pyodide ejecuta el codigo del alumno a traves de su propia maquinaria
 * (`/lib/python312.zip/_pyodide/_base.py`: `eval_code_async`, `CodeRunner`,
 * `_parse_and_compile_gen`...) y esos frames encabezan cada traceback. Para
 * un `SyntaxError` eran ~12 lineas que no tienen nada que ver con su codigo,
 * y el error real quedaba al final, debajo de rutas largas (incidente
 * 2026-11-03: `def factorial(n:int) -->int:` parecia un fallo del editor).
 *
 * Solo se quitan los frames de `_pyodide`. Los del alumno (`<exec>`, los
 * archivos de un capstone), los de la libreria estandar y los de paquetes
 * como numpy o pandas se quedan, igual que en un Python normal. El mensaje
 * final del error no se toca nunca.
 */
const CABECERA = 'Traceback (most recent call last):'
const FRAME = /^ {2}File "([^"]*)", line \d+/

function esInternoDePyodide(archivo: string): boolean {
  return archivo.includes('/_pyodide/')
}

export function limpiarTraceback(mensaje: string): string {
  const lineas = mensaje.split('\n')
  const inicio = lineas.findIndex((l) => l.startsWith(CABECERA))
  if (inicio < 0) return mensaje

  const salida = lineas.slice(0, inicio + 1)
  let i = inicio + 1
  while (i < lineas.length) {
    const frame = FRAME.exec(lineas[i])
    if (!frame) {
      // Fin de los frames: lo que queda es el error en si (incluido el
      // bloque `File "<exec>", line N` + caret de un SyntaxError).
      salida.push(...lineas.slice(i))
      break
    }
    // Un frame es su linea `File ...` mas las lineas sangradas que le siguen
    // (codigo fuente y marcas ^^^).
    let fin = i + 1
    while (fin < lineas.length && lineas[fin].startsWith('    ')) fin++
    if (!esInternoDePyodide(frame[1])) salida.push(...lineas.slice(i, fin))
    i = fin
  }
  return salida.join('\n')
}
