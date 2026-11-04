import { describe, expect, it } from 'vitest'
import { limpiarTraceback } from './traceback'

// Copiado de la Salida real del editor (2026-11-03).
const SYNTAX_ERROR = `Traceback (most recent call last):
  File "/lib/python312.zip/_pyodide/_base.py", line 597, in eval_code_async
    await CodeRunner(
          ^^^^^^^^^^^
  File "/lib/python312.zip/_pyodide/_base.py", line 285, in __init__
    self.ast = next(self._gen)
               ^^^^^^^^^^^^^^^
  File "/lib/python312.zip/_pyodide/_base.py", line 149, in _parse_and_compile_gen
    mod = compile(source, filename, mode, flags | ast.PyCF_ONLY_AST)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<exec>", line 1
    def factorial(n:int) -->int :
                         ^
SyntaxError: expected ':'`

const ASSERTION_ERROR = `Traceback (most recent call last):
  File "/lib/python312.zip/_pyodide/_base.py", line 597, in eval_code_async
    await CodeRunner(
  File "/lib/python312.zip/_pyodide/_base.py", line 411, in run_async
    coroutine = eval(self.code, globals, locals)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<exec>", line 10, in <module>
AssertionError`

describe('limpiarTraceback', () => {
  it('un SyntaxError queda en la linea del alumno, el caret y el mensaje', () => {
    expect(limpiarTraceback(SYNTAX_ERROR)).toBe(`Traceback (most recent call last):
  File "<exec>", line 1
    def factorial(n:int) -->int :
                         ^
SyntaxError: expected ':'`)
  })

  it('un error en ejecucion conserva el frame del alumno y el error', () => {
    expect(limpiarTraceback(ASSERTION_ERROR)).toBe(`Traceback (most recent call last):
  File "<exec>", line 10, in <module>
AssertionError`)
  })

  it('no toca los frames de librerias ni de archivos del alumno', () => {
    const tb = `Traceback (most recent call last):
  File "/lib/python312.zip/_pyodide/_base.py", line 597, in eval_code_async
    await CodeRunner(
  File "/home/pyodide/capstone/datos.py", line 3, in <module>
    df = pd.read_csv(ruta)
  File "/lib/python3.12/site-packages/pandas/io/parsers.py", line 912, in read_csv
    return _read(filepath_or_buffer, kwds)
FileNotFoundError: no existe ventas.csv`
    expect(limpiarTraceback(tb)).toBe(`Traceback (most recent call last):
  File "/home/pyodide/capstone/datos.py", line 3, in <module>
    df = pd.read_csv(ruta)
  File "/lib/python3.12/site-packages/pandas/io/parsers.py", line 912, in read_csv
    return _read(filepath_or_buffer, kwds)
FileNotFoundError: no existe ventas.csv`)
  })

  it('lo que va antes del traceback (warnings) se conserva', () => {
    const tb = `FutureWarning: algo va a cambiar\n${ASSERTION_ERROR}`
    expect(limpiarTraceback(tb).startsWith('FutureWarning: algo va a cambiar\nTraceback')).toBe(true)
  })

  it('sin traceback devuelve el mensaje tal cual', () => {
    expect(limpiarTraceback('Timeout (5000ms)')).toBe('Timeout (5000ms)')
  })
})
