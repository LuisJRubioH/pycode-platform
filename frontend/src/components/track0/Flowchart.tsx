import React from 'react'

/**
 * Diagrama de flujo dibujado en SVG a partir de datos, sin dependencias.
 *
 * El doc del track pedia Mermaid por cuatro razones —texto versionable,
 * editable, accesible y con tema— y las cuatro las cumple esto igual: el
 * diagrama es una lista de nodos en el `spec`, se lee en el diff, se colorea
 * con las clases de siempre y lleva su descripcion para lectores de pantalla.
 * A cambio no arrastra 122 MB ni el aviso de `lodash-es`, y sobre todo permite
 * lo que hace falta en `flowchart_fill`: sustituir el texto de un nodo por lo
 * que el alumno elige y volver a dibujar, que con una cadena de Mermaid seria
 * dar rodeos.
 *
 * Los diagramas de Track 0 son lineales con, como mucho, una bifurcacion y una
 * vuelta atras, asi que el trazado es una columna de nodos: cada uno debajo del
 * anterior, con su flecha. Los `rama` cuelgan a la derecha y el `volver` dibuja
 * la flecha de retorno del bucle.
 */

export type FormaNodo = 'inicio' | 'fin' | 'proceso' | 'decision' | 'entrada' | 'salida'

export interface NodoDiagrama {
  /** Identificador para las flechas de retorno. */
  id?: string
  forma: FormaNodo
  /** Texto del nodo. Si es null, es un hueco que rellena el alumno. */
  texto: string | null
  /** Etiqueta de la flecha que sale (por ejemplo, "si" / "no"). */
  etiqueta?: string
  /** Texto que cuelga a la derecha, para la rama corta de un Si. */
  rama?: string
  /** Etiqueta de la flecha que sale hacia la rama (por ejemplo, "si"). */
  etiquetaRama?: string
  /** El flujo vuelve a este id (bucle). */
  volver?: string
}

const ANCHO = 260
const ALTO_NODO = 48
const SEPARACION = 34

const RELLENO: Record<FormaNodo, string> = {
  inicio: '#0f766e',
  fin: '#0f766e',
  proceso: '#1e293b',
  decision: '#7c2d12',
  entrada: '#1e3a8a',
  salida: '#1e3a8a',
}

/** Cuantos huecos hay hasta el nodo `i` incluido; -1 si ese nodo no es hueco. */
function huecoIndice(nodos: NodoDiagrama[], i: number): number {
  if (nodos[i]?.texto !== null) return -1
  let n = 0
  for (let k = 0; k < i; k++) if (nodos[k].texto === null) n++
  return n
}

interface Props {
  nodos: NodoDiagrama[]
  /** Indice del nodo hueco que hay que resaltar (el que el backend señalo). */
  resaltado?: number | null
  descripcion?: string
}

const Flowchart: React.FC<Props> = ({ nodos, resaltado, descripcion }) => {
  const margen = 16
  const conRama = nodos.some((n) => n.rama)
  const conVuelta = nodos.some((n) => n.volver)
  const anchoTotal = ANCHO + margen * 2 + (conRama ? 150 : 0) + (conVuelta ? 40 : 0)
  const izquierda = margen + (conVuelta ? 40 : 0)
  const altoTotal = nodos.length * ALTO_NODO + (nodos.length - 1) * SEPARACION + margen * 2

  const y = (i: number) => margen + i * (ALTO_NODO + SEPARACION)
  const centroX = izquierda + ANCHO / 2

  return (
    <div className="mt-3 overflow-x-auto">
      <svg
        width={anchoTotal}
        height={altoTotal}
        viewBox={`0 0 ${anchoTotal} ${altoTotal}`}
        role="img"
        aria-label={descripcion || 'Diagrama de flujo'}
        className="max-w-full"
      >
        <defs>
          <marker id="punta" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
            <path d="M0,0 L8,4 L0,8 z" fill="#64748b" />
          </marker>
        </defs>

        {nodos.map((nodo, i) => {
          const arriba = y(i)
          const siguiente = i < nodos.length - 1 ? y(i + 1) : null
          const destino = nodo.volver ? nodos.findIndex((n) => n.id === nodo.volver) : -1
          const esHueco = nodo.texto === null
          const marcado = resaltado != null && resaltado === huecoIndice(nodos, i)

          return (
            <g key={i}>
              {/* flecha al siguiente */}
              {siguiente != null && (
                <line
                  x1={centroX}
                  y1={arriba + ALTO_NODO}
                  x2={centroX}
                  y2={siguiente}
                  stroke="#64748b"
                  strokeWidth="1.5"
                  markerEnd="url(#punta)"
                />
              )}
              {siguiente != null && nodo.etiqueta && (
                <text
                  x={centroX + 8}
                  y={arriba + ALTO_NODO + SEPARACION / 2 + 4}
                  fontSize="11"
                  fill="#475569"
                >
                  {nodo.etiqueta}
                </text>
              )}

              {/* rama corta a la derecha */}
              {nodo.rama && (
                <g>
                  <line
                    x1={izquierda + ANCHO}
                    y1={arriba + ALTO_NODO / 2}
                    x2={izquierda + ANCHO + 40}
                    y2={arriba + ALTO_NODO / 2}
                    stroke="#64748b"
                    strokeWidth="1.5"
                    markerEnd="url(#punta)"
                  />
                  {nodo.etiquetaRama && (
                    <text
                      x={izquierda + ANCHO + 6}
                      y={arriba + ALTO_NODO / 2 - 6}
                      fontSize="11"
                      fill="#475569"
                    >
                      {nodo.etiquetaRama}
                    </text>
                  )}
                  <rect
                    x={izquierda + ANCHO + 44}
                    y={arriba + ALTO_NODO / 2 - 16}
                    width={100}
                    height={32}
                    rx={6}
                    fill="#1e293b"
                  />
                  <text
                    x={izquierda + ANCHO + 94}
                    y={arriba + ALTO_NODO / 2 + 4}
                    fontSize="11"
                    fill="#f8fafc"
                    textAnchor="middle"
                  >
                    {nodo.rama}
                  </text>
                </g>
              )}

              {/* vuelta atras del bucle */}
              {destino >= 0 && (
                <path
                  d={`M ${izquierda} ${arriba + ALTO_NODO / 2} H ${izquierda - 24} V ${
                    y(destino) + ALTO_NODO / 2
                  } H ${izquierda - 4}`}
                  fill="none"
                  stroke="#64748b"
                  strokeWidth="1.5"
                  strokeDasharray="4 3"
                  markerEnd="url(#punta)"
                />
              )}

              {/* el nodo */}
              {nodo.forma === 'decision' ? (
                <polygon
                  points={`${centroX},${arriba} ${izquierda + ANCHO},${arriba + ALTO_NODO / 2} ${centroX},${
                    arriba + ALTO_NODO
                  } ${izquierda},${arriba + ALTO_NODO / 2}`}
                  fill={esHueco ? '#f8fafc' : RELLENO.decision}
                  stroke={marcado ? '#e11d48' : esHueco ? '#94a3b8' : 'none'}
                  strokeWidth={marcado ? 2 : 1}
                  strokeDasharray={esHueco && !marcado ? '5 4' : undefined}
                />
              ) : (
                <rect
                  x={izquierda}
                  y={arriba}
                  width={ANCHO}
                  height={ALTO_NODO}
                  rx={nodo.forma === 'inicio' || nodo.forma === 'fin' ? 22 : 8}
                  fill={esHueco ? '#f8fafc' : RELLENO[nodo.forma]}
                  stroke={marcado ? '#e11d48' : esHueco ? '#94a3b8' : 'none'}
                  strokeWidth={marcado ? 2 : 1}
                  strokeDasharray={esHueco && !marcado ? '5 4' : undefined}
                />
              )}
              <text
                x={centroX}
                y={arriba + ALTO_NODO / 2 + 4}
                fontSize="12"
                fill={esHueco ? '#94a3b8' : '#f8fafc'}
                textAnchor="middle"
                fontFamily="ui-monospace, SFMono-Regular, Menlo, monospace"
              >
                {nodo.texto ?? '?'}
              </text>
            </g>
          )
        })}
      </svg>
    </div>
  )
}

export default Flowchart
