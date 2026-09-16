import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import EvaluacionSocratica from './EvaluacionSocratica'
import { partirVeredicto, tonoDeNota } from './evaluacionSecciones'

// Veredicto real de openai/gpt-oss-120b, con el Markdown tal cual lo escribe.
const VEREDICTO = `**CALIFICACIÓN:**
- Lógica: **95/100** - La función produce la lista correcta.
- Solución General: **80/100** - El código es legible.

---

### ANÁLISIS DETALLADO

#### PUNTOS FUERTES
1. **Implementación correcta del algoritmo** - Detectas los casos de 3, 5 y 15.
2. **Uso de \`str(number)\`** - Cumple con devolver siempre strings.

#### ÁREAS DE MEJORA
1. **Orden de las condiciones** - Puede simplificarse usando \`number % 15 == 0\`.

#### RECOMENDACIONES
1. **Pregunta socrática:** ¿qué pasaría con n = 0?
`

// El texto de reserva del backend: sin Markdown y sin tildes.
const VEREDICTO_PLANO = `CALIFICACION:
- Logica: 75/100 (estimacion inicial)
- Solucion General: 78/100 (estimacion inicial)

ANALISIS DETALLADO:

PUNTOS FUERTES:
- Ya hay una propuesta concreta.

AREAS DE MEJORA:
- Revisa cada parte del codigo.

RECOMENDACIONES:
- Que pasaria con un caso extremo?
`

describe('partirVeredicto', () => {
  it('reconoce las cabeceras con Markdown (##, **) y sin el', () => {
    const tipos = partirVeredicto(VEREDICTO).map((b) => b.tipo)
    expect(tipos).toContain('calificacion')
    expect(tipos).toContain('fuertes')
    expect(tipos).toContain('mejora')
    expect(tipos).toContain('recomendaciones')

    const planos = partirVeredicto(VEREDICTO_PLANO).map((b) => b.tipo)
    expect(planos).toContain('fuertes')
    expect(planos).toContain('mejora')
    expect(planos).toContain('recomendaciones')
  })

  it('no abre bloque con una linea de contenido que mencione un titulo', () => {
    const raw = 'PUNTOS FUERTES\n- Aqui hablamos de las areas de mejora del bucle interno y de por que importan.'
    const bloques = partirVeredicto(raw)
    expect(bloques).toHaveLength(1)
    expect(bloques[0].tipo).toBe('fuertes')
  })

  it('conserva el texto que llega antes de la primera cabecera', () => {
    const bloques = partirVeredicto('Hola, vengo sin formato.\n\nPUNTOS FUERTES\n- algo')
    expect(bloques[0].tipo).toBe('normal')
    expect(bloques[0].cuerpo).toContain('vengo sin formato')
  })

  it('ignora una cabecera dentro de un bloque de codigo', () => {
    const raw = 'PUNTOS FUERTES\n```python\n# RECOMENDACIONES\nx = 1\n```\n'
    const tipos = partirVeredicto(raw).map((b) => b.tipo)
    expect(tipos).toEqual(['fuertes'])
  })
})

describe('tonoDeNota', () => {
  it('reparte por tramos y distingue el caso sin nota', () => {
    expect(tonoDeNota(95)).toBe('excelente')
    expect(tonoDeNota(85)).toBe('excelente')
    expect(tonoDeNota(80)).toBe('bien')
    expect(tonoDeNota(55)).toBe('regular')
    expect(tonoDeNota(20)).toBe('flojo')
    expect(tonoDeNota(null)).toBe('sin-nota')
  })
})

describe('EvaluacionSocratica', () => {
  it('renderiza el Markdown en vez de mostrar los asteriscos', () => {
    render(
      <EvaluacionSocratica raw={VEREDICTO} logicScore={95} generalScore={80} />
    )
    expect(screen.queryByText(/\*\*/)).toBeNull()
    expect(screen.getByText('Implementación correcta del algoritmo')).toBeInTheDocument()
  })

  it('pone cada bloque bajo su titulo propio', () => {
    render(
      <EvaluacionSocratica raw={VEREDICTO} logicScore={95} generalScore={80} />
    )
    expect(screen.getByText('Lo que ya hiciste bien')).toBeInTheDocument()
    expect(screen.getByText('Qué mejorar')).toBeInTheDocument()
    expect(screen.getByText('Para pensar')).toBeInTheDocument()
  })

  it('muestra las dos notas con su tramo', () => {
    render(
      <EvaluacionSocratica raw={VEREDICTO} logicScore={95} generalScore={80} />
    )
    expect(screen.getByText('95')).toBeInTheDocument()
    expect(screen.getByText('80')).toBeInTheDocument()
    expect(screen.getByLabelText('95 de 100')).toBeInTheDocument()
    expect(screen.getByText('Excelente')).toBeInTheDocument()
    expect(screen.getByText('Bien')).toBeInTheDocument()
  })

  it('con las dos notas extraidas no repite el desglose de la calificacion', () => {
    render(
      <EvaluacionSocratica raw={VEREDICTO} logicScore={95} generalScore={80} />
    )
    expect(screen.queryByText('Calificación')).toBeNull()
  })

  it('si una nota no se pudo extraer, el desglose en texto no se pierde', () => {
    render(
      <EvaluacionSocratica raw={VEREDICTO} logicScore={null} generalScore={null} />
    )
    expect(screen.getByText('Calificación')).toBeInTheDocument()
    expect(screen.getAllByText('—').length).toBeGreaterThan(0)
  })

  it('en modo compacto no repite las fichas de nota', () => {
    render(
      <EvaluacionSocratica raw={VEREDICTO} logicScore={95} generalScore={80} compacto />
    )
    expect(screen.queryByText('Solución general')).toBeNull()
    expect(screen.getByText('Lo que ya hiciste bien')).toBeInTheDocument()
  })
})
