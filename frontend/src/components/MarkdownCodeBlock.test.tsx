import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import MarkdownCodeBlock from './MarkdownCodeBlock'

const writeText = vi.fn()

describe('MarkdownCodeBlock', () => {
  beforeEach(() => {
    writeText.mockReset().mockResolvedValue(undefined)
  })

  // `userEvent.setup()` instala su propio stub de navigator.clipboard como
  // getter, asi que el mock tiene que ponerse DESPUES y con defineProperty
  // (Object.assign lanza TypeError sobre una propiedad de solo lectura).
  function setupConPortapapeles() {
    const user = userEvent.setup()
    Object.defineProperty(navigator, 'clipboard', {
      value: { writeText },
      configurable: true,
    })
    return user
  }

  it('copia el codigo plano, sin las marcas del resaltado', async () => {
    const user = setupConPortapapeles()
    // Asi es como llega tras rehype-highlight: tokens envueltos en spans.
    render(
      <MarkdownCodeBlock>
        <code className="hljs language-python">
          <span className="hljs-keyword">import</span> pandas
        </code>
      </MarkdownCodeBlock>
    )

    await user.click(screen.getByRole('button', { name: /Copiar codigo/ }))

    expect(writeText).toHaveBeenCalledWith('import pandas')
  })

  it('confirma visualmente tras copiar', async () => {
    const user = setupConPortapapeles()
    render(
      <MarkdownCodeBlock>
        <code>print(1)</code>
      </MarkdownCodeBlock>
    )

    expect(screen.getByRole('button', { name: /Copiar codigo/ })).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: /Copiar codigo/ }))
    expect(
      await screen.findByRole('button', { name: /Codigo copiado/ })
    ).toBeInTheDocument()
  })
})
