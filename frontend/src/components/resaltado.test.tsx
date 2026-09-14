import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import Markdown from './Markdown'

describe('resaltado de codigo', () => {
  it('resalta los bloques python con clases hljs', () => {
    const { container } = render(<Markdown>{'```python\nimport pandas as pd\nx = 1  # nota\n```'}</Markdown>)
    const code = container.querySelector('pre code')!
    expect(code.className).toContain('hljs')
    expect(code.className).toContain('language-python')
    expect(code.querySelector('.hljs-keyword')?.textContent).toBe('import')
    expect(code.querySelector('.hljs-comment')?.textContent).toBe('# nota')
    // El texto del codigo no cambia, solo se envuelve en spans.
    expect(code.textContent).toBe('import pandas as pd\nx = 1  # nota\n')
  })

  it('acepta el alias py', () => {
    const { container } = render(<Markdown>{'```py\ndef f():\n    pass\n```'}</Markdown>)
    expect(container.querySelector('pre code .hljs-keyword')?.textContent).toBe('def')
  })

  it('bloques sin etiqueta y codigo inline quedan sin resaltar', () => {
    const { container } = render(<Markdown>{'Usa `print(1)`.\n\n```\nsalida esperada\n```'}</Markdown>)
    expect(container.querySelector('pre code')!.className).not.toContain('hljs')
    expect(container.querySelector('pre code span')).toBeNull()
    expect(container.querySelector('p code span')).toBeNull()
  })
})
