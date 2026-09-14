import { describe, it, expect } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import { LessonIndex, LessonSections } from './LessonContent'
import { partirEnSecciones, slugSeccion } from './lessonSecciones'

const LECCION = [
  'Texto antes de la primera seccion.',
  '',
  '## Por que Pandas',
  'Porque si.',
  '',
  '## Indexación: tres formas',
  '```python',
  '## esto es un comentario, no una seccion',
  'df.loc[0]',
  '```',
  '',
  '## Errores comunes',
  '- uno',
  '',
  '## Resumen',
  '- dos',
].join('\n')

describe('partirEnSecciones', () => {
  it('parte por ## sin confundir los ## de dentro del codigo', () => {
    const { intro, secciones } = partirEnSecciones(LECCION)
    expect(intro).toBe('Texto antes de la primera seccion.')
    expect(secciones.map((s) => s.titulo)).toEqual([
      'Por que Pandas',
      'Indexación: tres formas',
      'Errores comunes',
      'Resumen',
    ])
    expect(secciones[1].cuerpo).toContain('## esto es un comentario, no una seccion')
  })

  it('marca los bloques semanticos por su titulo', () => {
    const tipos = partirEnSecciones(LECCION).secciones.map((s) => s.tipo)
    expect(tipos).toEqual(['objetivo', 'normal', 'errores', 'resumen'])
  })

  it('anclas sin tildes y sin repetirse', () => {
    expect(slugSeccion('Indexación: tres formas (no las mezcles)')).toBe(
      'indexacion-tres-formas-no-las-mezcles'
    )
    const { secciones } = partirEnSecciones('## Ejemplo\na\n## Ejemplo\nb')
    expect(secciones.map((s) => s.id)).toEqual(['ejemplo', 'ejemplo-2'])
  })
})

describe('LessonSections e indice', () => {
  it('cada entrada del indice apunta a una seccion que existe', () => {
    const { intro, secciones } = partirEnSecciones(LECCION)
    const { container } = render(
      <>
        <LessonIndex entradas={secciones.map((s) => ({ id: s.id, titulo: s.titulo }))} />
        <LessonSections intro={intro} secciones={secciones} />
      </>
    )
    // El indice de escritorio (el desplegable movil repite los mismos enlaces).
    const nav = screen.getByRole('navigation', { name: 'Indice de la leccion' })
    const hrefs = Array.from(nav.querySelectorAll('a')).map((a) => a.getAttribute('href'))
    expect(new Set(hrefs)).toEqual(new Set(secciones.map((s) => `#${s.id}`)))
    for (const href of hrefs) {
      expect(container.querySelector(href!)).not.toBeNull()
    }
  })

  it('las secciones semanticas llevan su tipo y su titulo como encabezado', () => {
    const { intro, secciones } = partirEnSecciones(LECCION)
    render(<LessonSections intro={intro} secciones={secciones} />)
    const errores = screen.getByRole('region', { name: 'Errores comunes' })
    expect(errores).toHaveAttribute('data-tipo', 'errores')
    expect(within(errores).getByRole('heading', { level: 2 })).toHaveTextContent('Errores comunes')
    // El comentario del bloque de codigo no se convirtio en encabezado.
    expect(screen.queryByRole('heading', { name: /esto es un comentario/ })).not.toBeInTheDocument()
  })
})
