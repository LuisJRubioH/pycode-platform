"""
Seed theory-first Python lessons and guided exercises.
"""

# flake8: noqa: E501 -- archivo de contenido curado: enunciados y starters de ejercicios en espanol.

from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.learning import Exercise, Lesson


@dataclass(frozen=True)
class ExerciseTemplate:
    title: str
    description: str
    instructions: str
    starter_code: str
    hints: list[str] = field(default_factory=list)
    points: int = 10
    difficulty: str = "easy"
    hidden_tests: list[dict] = field(default_factory=list)


@dataclass(frozen=True)
class LessonTemplate:
    title: str
    description: str
    content: str
    difficulty: str
    category: str
    order: int
    estimated_duration: int
    prerequisites_titles: list[str] = field(default_factory=list)
    exercises: list[ExerciseTemplate] = field(default_factory=list)
    track: str = "track-1"


LESSON_TEMPLATES: list[LessonTemplate] = [
    LessonTemplate(
        title="Python desde Cero",
        description=(
            "Tu primer programa: print, variables, f-strings y como se lee un "
            "error. No hace falta saber nada de programacion."
        ),
        content=(
            "## Por que empezar por aqui\n"
            "Esta es la primera leccion del camino, y esta escrita para alguien\n"
            "que no ha programado nunca. Al terminarla vas a haber escrito y\n"
            "ejecutado programas de verdad: cosas que guardan datos, los\n"
            "combinan y los muestran. Lo que viene despues -bucles, funciones,\n"
            "datos, machine learning- son variaciones sobre lo que aprendes hoy.\n\n"
            "El codigo lo escribes en el editor y lo corres con el boton de\n"
            "ejecutar: se ejecuta **dentro de tu navegador**, asi que no tienes\n"
            "que instalar nada ni puedes romper nada.\n\n"
            "## print: hacer que el programa hable\n"
            "Un programa que no muestra nada parece un programa que no funciona.\n"
            "`print` es como le pides que te ensene algo:\n"
            "```python\n"
            "print('Hola')            # Hola\n"
            "print('Hola', 'mundo')   # Hola mundo  -> la coma mete un espacio\n"
            "print(3 + 4)             # 7   -> sin comillas es una cuenta, no un texto\n"
            "print('3 + 4')           # 3 + 4  -> con comillas es texto tal cual\n"
            "print()                  # una linea en blanco\n"
            "```\n"
            "Lo que va entre comillas es **texto** y sale tal cual. Lo que va sin\n"
            "comillas, Python intenta entenderlo: `3 + 4` lo resuelve antes de\n"
            "imprimirlo. Las comillas pueden ser simples o dobles, pero la que\n"
            "abre y la que cierra tienen que ser la misma.\n\n"
            "## Un programa se lee de arriba abajo\n"
            "Cada linea es una instruccion, y se ejecutan en orden, una detras de\n"
            "otra:\n"
            "```python\n"
            "print('primero')     # esto sale antes\n"
            "print('segundo')     # y esto despues\n"
            "print('tercero')     # el orden lo decides tu escribiendo\n"
            "```\n"
            "Parece obvio, pero es la regla que explica la mitad de los errores\n"
            "del principio: si usas algo antes de la linea donde lo creas, para\n"
            "Python todavia no existe.\n\n"
            "## Variables: ponerle nombre a un dato\n"
            "Una variable es un nombre para un dato, para no repetirlo cada vez:\n"
            "```python\n"
            "nombre = 'Ana'       # el = guarda lo de la derecha con el nombre de la izquierda\n"
            "print(nombre)        # Ana     -> sin comillas: imprime lo GUARDADO\n"
            "print('nombre')      # nombre  -> con comillas: el texto literal\n\n"
            "nombre = 'Luis'      # se puede reasignar: ahora vale otra cosa\n"
            "print(nombre)        # Luis    -> se quedo con lo ultimo\n\n"
            "precio = 3           # los numeros van sin comillas\n"
            "total = precio * 4   # y se pueden operar: * es multiplicar\n"
            "print(total)         # 12\n"
            "```\n"
            "El `=` no es el de las matematicas: no dice que las dos partes sean\n"
            "iguales, dice **guarda esto ahi**. Por eso `total = precio * 4`\n"
            "primero hace la cuenta y despues guarda el resultado.\n\n"
            "En la proxima leccion vas a ver los tipos de dato en serio (texto,\n"
            "enteros, decimales); por ahora basta con distinguir lo que lleva\n"
            "comillas de lo que no.\n\n"
            "## f-strings: meter un dato dentro de un texto\n"
            "Casi nunca quieres imprimir el dato solo, sino dentro de una frase.\n"
            "Para eso se pone una `f` delante de la comilla y el dato entre\n"
            "llaves:\n"
            "```python\n"
            "nombre = 'Ana'\n"
            "edad = 30\n"
            "print(f'Hola, {nombre}')            # Hola, Ana\n"
            "print(f'{nombre} tiene {edad}')     # Ana tiene 30  -> puedes meter varios\n"
            "print(f'El ano que viene, {edad + 1}')   # El ano que viene, 31\n"
            "print('Hola, {nombre}')             # Hola, {nombre}  -> sin la f no sustituye\n"
            "```\n"
            "Dentro de las llaves va lo que quieras que Python resuelva: una\n"
            "variable o una cuenta. Fuera de las llaves, todo es texto.\n\n"
            "## Comentarios: notas para el que lee\n"
            "```python\n"
            "# Esta linea entera la ignora Python.\n"
            "print('hola')   # y esto tambien, desde la almohadilla hasta el final\n"
            "```\n"
            "Los comentarios no cambian lo que hace el programa. Sirven para\n"
            "explicar **por que** haces algo, no para repetir lo que ya dice el\n"
            "codigo: `precio = 3  # asigna 3 a precio` no le aporta nada a nadie.\n\n"
            "## Los espacios del principio de la linea importan\n"
            "En muchos lenguajes la sangria es decoracion. En Python es sintaxis:\n"
            "```python\n"
            "print('linea uno')\n"
            "print('linea dos')   # las dos empiezan pegadas al margen: sin espacios\n"
            "```\n"
            "Si le pones un espacio delante a la segunda linea, Python corta con\n"
            "`IndentationError: unexpected indent`. Mas adelante habra sitios\n"
            "donde la sangria es obligatoria (dentro de un `if`, de un bucle);\n"
            "por ahora la regla es: todo pegado al margen izquierdo.\n\n"
            "## Cuando algo falla, leelo de abajo hacia arriba\n"
            "Los errores de Python asustan porque son varias lineas, pero **la\n"
            "ultima es la que dice que paso** y las de arriba dicen donde:\n"
            "```python\n"
            "print('antes del error')      # esto SI se ejecuta\n"
            "# print(nombre_que_no_existe) # esto daria NameError\n"
            "print('el programa sigue')    # porque la linea de arriba es un comentario\n"
            "```\n"
            "Los tres que vas a ver mil veces:\n\n"
            "- `NameError: name 'x' is not defined` -> usaste un nombre que no\n"
            "  existe todavia, o lo escribiste distinto al crearlo.\n"
            "- `SyntaxError` -> la frase no es Python valido: casi siempre una\n"
            "  comilla o un parentesis sin cerrar.\n"
            "- `IndentationError` -> espacios de mas o de menos al principio de\n"
            "  una linea.\n\n"
            "Un error no es un castigo: es el interprete diciendote donde mirar.\n\n"
            "## Errores comunes\n"
            "- Escribir `Print` o `PRINT`. Python distingue mayusculas de\n"
            "  minusculas: solo existe `print`, y lo demas es `NameError`.\n"
            "- Olvidar una comilla o un parentesis. `print('hola)` no llega ni a\n"
            "  ejecutarse: `SyntaxError`. Cuenta que cada cosa que abres se\n"
            "  cierra.\n"
            "- Olvidar la `f` delante del texto: `print('Hola, {nombre}')`\n"
            "  imprime las llaves tal cual en vez del valor. Si ves llaves en la\n"
            "  salida, te falta la `f`.\n"
            "- Usar una variable antes de crearla. El programa se lee de arriba\n"
            "  abajo: si el `print(total)` esta encima de la linea que calcula\n"
            "  `total`, es `NameError`.\n"
            "- Confundir el nombre con el texto: `print(nombre)` imprime el dato\n"
            "  guardado, `print('nombre')` imprime la palabra nombre.\n\n"
            "## Resumen\n"
            "- `print(...)` muestra cosas; con comillas es texto literal, sin\n"
            "  comillas Python lo resuelve primero.\n"
            "- El programa se ejecuta de arriba abajo, una linea por instruccion.\n"
            "- `nombre = valor` guarda un dato con un nombre, y se puede\n"
            "  reasignar.\n"
            "- `f'Hola, {nombre}'` mete el valor dentro del texto; sin la `f` no\n"
            "  sustituye nada.\n"
            "- `#` empieza un comentario, que Python ignora.\n"
            "- Las lineas van pegadas al margen mientras no estemos dentro de un\n"
            "  bloque.\n"
            "- El mensaje de error se lee por la ultima linea: `NameError`,\n"
            "  `SyntaxError` e `IndentationError` son los tres del principio.\n"
        ),
        difficulty="beginner",
        category="fundamentos",
        order=1,
        estimated_duration=40,
        exercises=[
            ExerciseTemplate(
                title="Hola Python",
                description="Tu primer programa: una variable y un saludo.",
                instructions=(
                    "Guarda tu nombre en la variable `nombre` y muestra "
                    "`Hola, <tu nombre>` usando una f-string.\n\n"
                    "Con `nombre = 'Ana'` la salida tiene que ser exactamente "
                    "`Hola, Ana`: una sola linea, con la coma y el espacio."
                ),
                starter_code="nombre = ''\n# TODO\n",
                hints=[
                    "Primero pon tu nombre entre comillas: nombre = 'Ana'.",
                    "Despues: print(f'Hola, {nombre}')  -- la f va pegada a la comilla.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "imprime 'Hola, <nombre>' con f-string",
                        "code": (
                            "assert nombre, 'define nombre con tu nombre'\n"
                            "assert _salida.strip() == f'Hola, {nombre}', _salida"
                        ),
                    },
                    {
                        "name": "es una sola linea",
                        "code": (
                            "lineas = [l for l in _salida.strip().split(chr(10)) if l.strip()]\n"
                            "assert len(lineas) == 1, ('esperaba una sola linea', lineas)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Mini presentación",
                description="Dos prints, dos lineas, en orden.",
                instructions=(
                    "Pon tu ciudad en `ciudad` e imprime **dos lineas**: primero "
                    "la ciudad y despues el lenguaje.\n\n"
                    "Cada `print` muestra solo el valor de la variable, sin texto "
                    "alrededor. Con `ciudad = 'Lima'` la salida es `Lima` y debajo "
                    "`Python`."
                ),
                starter_code="ciudad = ''\nlenguaje = 'Python'\n# TODO\n",
                hints=[
                    "Pon tu ciudad entre comillas: ciudad = 'Lima'.",
                    "Dos prints, uno debajo del otro: print(ciudad) y print(lenguaje).",
                    "Sin comillas dentro del print: print(ciudad) imprime el dato, "
                    "print('ciudad') imprime la palabra.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "imprime dos lineas (incluye 'Python')",
                        "code": (
                            "lineas = [l for l in _salida.strip().split(chr(10)) if l.strip()]\n"
                            "assert len(lineas) == 2, ('esperaba 2 lineas', lineas)\n"
                            "assert 'Python' in _salida, _salida"
                        ),
                    },
                    {
                        "name": "primero la ciudad, despues el lenguaje, y sin texto de adorno",
                        "code": (
                            "assert ciudad, 'define ciudad con tu ciudad'\n"
                            "lineas = [l for l in _salida.strip().split(chr(10)) if l.strip()]\n"
                            "assert lineas == [ciudad, lenguaje], "
                            "f'esperaba [{ciudad!r}, {lenguaje!r}] y salio {lineas}'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="La cuenta del kiosco",
                description="Una variable que sale de otras dos.",
                instructions=(
                    "Con el precio y la cantidad que ya estan en el starter, "
                    "calcula el total y guardalo en una variable llamada `total`.\n\n"
                    "Despues imprime exactamente `Total: 12 euros` usando una "
                    "f-string con `total` dentro. La cuenta la hace Python, no tu: "
                    "no escribas el 12 a mano."
                ),
                starter_code=(
                    "precio_unitario = 3\n"
                    "cantidad = 4\n"
                    "# TODO: calcula total y luego imprimelo\n"
                ),
                hints=[
                    "Multiplicar es *: total = precio_unitario * cantidad.",
                    "La linea del total va ANTES del print que lo usa.",
                    "print(f'Total: {total} euros')",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "la variable total vale 12",
                        "code": (
                            "assert 'total' in dir() or True\n"
                            "assert total == 12, f'total vale {total!r}'"
                        ),
                    },
                    {
                        "name": "imprime la linea exacta",
                        "code": (
                            "assert _salida.strip() == 'Total: 12 euros', "
                            "f'salio {_salida.strip()!r}'"
                        ),
                    },
                    {
                        "name": "el total sale de la multiplicacion, no escrito a mano",
                        "code": (
                            "assert total == precio_unitario * cantidad, "
                            "'total no coincide con precio_unitario * cantidad'\n"
                            "assert precio_unitario == 3 and cantidad == 4, "
                            "'no cambies el precio ni la cantidad del starter'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Intercambio",
                description="Reasignar es pisar lo que habia.",
                instructions=(
                    "`a` vale `'sol'` y `b` vale `'luna'`. Intercambia sus valores "
                    "para que al final `a` valga `'luna'` y `b` valga `'sol'`.\n\n"
                    "Usa una tercera variable llamada `temporal` para no perder "
                    "ninguno por el camino, y al final imprime una linea con "
                    "`a` y `b` separados por un espacio."
                ),
                starter_code=(
                    "a = 'sol'\n"
                    "b = 'luna'\n"
                    "# TODO: intercambia usando temporal, despues imprime\n"
                ),
                hints=[
                    "Si escribes a = b lo primero, el valor viejo de a se pierde "
                    "para siempre: por eso hace falta guardarlo antes.",
                    "temporal = a  -> ahora 'sol' esta a salvo.",
                    "Despues a = b, y por ultimo b = temporal.",
                    "Para imprimir: print(f'{a} {b}') o print(a, b).",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "los valores quedaron intercambiados",
                        "code": (
                            "assert a == 'luna', f'a vale {a!r}'\n"
                            "assert b == 'sol', f'b vale {b!r}'"
                        ),
                    },
                    {
                        "name": "no se perdio ninguno por el camino",
                        "code": (
                            "assert temporal == 'sol', "
                            "f'temporal vale {temporal!r}: guarda en el la copia de a antes de pisarla'"
                        ),
                    },
                    {
                        "name": "imprime los dos en una linea",
                        "code": (
                            "assert _salida.strip() == 'luna sol', "
                            "f'salio {_salida.strip()!r} y se esperaba luna sol'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Tarjeta de presentacion",
                description="Varias variables, una cuenta y tres lineas con formato.",
                instructions=(
                    "Rellena `nombre`, `ciudad` y `edad` con tus datos (la edad es "
                    "un numero, sin comillas). Calcula en `anio_nacimiento` el ano "
                    "aproximado en que naciste restandole tu edad a 2026, y "
                    "imprime estas tres lineas, en este orden:\n\n"
                    "```\n"
                    "Nombre: Ana\n"
                    "Ciudad: Lima\n"
                    "Nacio en 1996\n"
                    "```\n\n"
                    "Con tus datos, claro. Usa f-strings."
                ),
                starter_code=(
                    "nombre = ''\n"
                    "ciudad = ''\n"
                    "edad = 0\n"
                    "# TODO: calcula anio_nacimiento y imprime las tres lineas\n"
                ),
                hints=[
                    "La edad va sin comillas: edad = 30, no edad = '30'.",
                    "anio_nacimiento = 2026 - edad",
                    "La primera linea es print(f'Nombre: {nombre}').",
                    "La tercera lleva la cuenta ya hecha: print(f'Nacio en {anio_nacimiento}').",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "los datos estan rellenados",
                        "code": (
                            "assert nombre and ciudad, 'rellena nombre y ciudad'\n"
                            "assert edad > 0, 'pon tu edad como numero, sin comillas'"
                        ),
                    },
                    {
                        "name": "el ano de nacimiento sale de la resta",
                        "code": (
                            "assert anio_nacimiento == 2026 - edad, "
                            "f'anio_nacimiento vale {anio_nacimiento!r} y con tu edad deberia ser "
                            "{2026 - edad}'"
                        ),
                    },
                    {
                        "name": "las tres lineas, en orden y con su etiqueta",
                        "code": (
                            "lineas = [l for l in _salida.strip().split(chr(10)) if l.strip()]\n"
                            "esperado = [f'Nombre: {nombre}', f'Ciudad: {ciudad}', "
                            "f'Nacio en {anio_nacimiento}']\n"
                            "assert lineas == esperado, f'esperaba {esperado} y salio {lineas}'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="El recibo del kiosco",
                description="El pipeline: varias variables, varias cuentas y una salida con formato.",
                instructions=(
                    "El starter trae el precio y la cantidad de tres productos. "
                    "Calcula el total de cada uno y el total general, y guardalos "
                    "en las variables `total_cuaderno`, `total_lapiz`, "
                    "`total_goma` y `total`.\n\n"
                    "Despues imprime exactamente estas cuatro lineas:\n\n"
                    "```\n"
                    "cuaderno x3 = 12\n"
                    "lapiz x5 = 5\n"
                    "goma x2 = 4\n"
                    "TOTAL = 21\n"
                    "```\n\n"
                    "Todos los numeros salen de las variables del starter: no "
                    "escribas ninguno a mano."
                ),
                starter_code=(
                    "cuaderno_precio = 4\n"
                    "cuaderno_cantidad = 3\n"
                    "lapiz_precio = 1\n"
                    "lapiz_cantidad = 5\n"
                    "goma_precio = 2\n"
                    "goma_cantidad = 2\n"
                    "# TODO: los tres totales, el total general y las cuatro lineas\n"
                ),
                hints=[
                    "Cada total es su precio por su cantidad: "
                    "total_cuaderno = cuaderno_precio * cuaderno_cantidad.",
                    "El total general es la suma de los tres, y va DESPUES de ellos.",
                    "La primera linea: print(f'cuaderno x{cuaderno_cantidad} = {total_cuaderno}').",
                    "La ultima lleva TOTAL en mayusculas: print(f'TOTAL = {total}').",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "los tres totales por producto",
                        "code": (
                            "assert total_cuaderno == 12, f'total_cuaderno vale {total_cuaderno!r}'\n"
                            "assert total_lapiz == 5, f'total_lapiz vale {total_lapiz!r}'\n"
                            "assert total_goma == 4, f'total_goma vale {total_goma!r}'"
                        ),
                    },
                    {
                        "name": "el total general es la suma de los tres",
                        "code": (
                            "assert total == 21, f'total vale {total!r}'\n"
                            "assert total == total_cuaderno + total_lapiz + total_goma, "
                            "'el total no coincide con la suma de los tres'"
                        ),
                    },
                    {
                        "name": "las cuatro lineas exactas",
                        "code": (
                            "lineas = [l for l in _salida.strip().split(chr(10)) if l.strip()]\n"
                            "esperado = ['cuaderno x3 = 12', 'lapiz x5 = 5', 'goma x2 = 4', "
                            "'TOTAL = 21']\n"
                            "assert lineas == esperado, f'esperaba {esperado} y salio {lineas}'"
                        ),
                    },
                    {
                        "name": "las cuentas salen de las variables del starter",
                        "code": (
                            "assert total_cuaderno == cuaderno_precio * cuaderno_cantidad\n"
                            "assert total_lapiz == lapiz_precio * lapiz_cantidad\n"
                            "assert total_goma == goma_precio * goma_cantidad\n"
                            "assert cuaderno_precio == 4 and lapiz_cantidad == 5, "
                            "'no cambies los datos del starter'"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Variables y Tipos",
        description=(
            "int, float, str y bool: que puede hacer cada uno, como se convierte "
            "de uno a otro y por que el mismo + a veces suma y a veces pega."
        ),
        content=(
            "## Por que el tipo importa\n"
            "En la leccion anterior guardaste datos en variables sin preguntarte\n"
            "de que estaban hechos. Ahora si: `2 + 3` da `5`, pero `'2' + '3'` da\n"
            "`'23'`. El mismo simbolo hace cosas distintas segun el **tipo** de lo\n"
            "que tiene al lado, y la mayoria de los errores de los primeros dias\n"
            "salen justo de ahi: un numero que en realidad era texto.\n\n"
            "## Los cuatro tipos que vas a usar\n"
            "```python\n"
            "edad = 18             # int: numero entero, sin decimales\n"
            "altura = 1.72         # float: decimal, y se escribe con PUNTO\n"
            "nombre = 'Ana'        # str: texto, siempre entre comillas\n"
            "activo = True         # bool: solo True o False, con mayuscula\n\n"
            "print(type(edad))     # <class 'int'>\n"
            "print(type(altura))   # <class 'float'>\n"
            "print(type(nombre))   # <class 'str'>\n"
            "print(type(activo))   # <class 'bool'>\n"
            "```\n"
            "`type(x)` te dice de que es cada cosa. Lo vas a usar sobre todo\n"
            "cuando algo no funcione y sospeches que tienes un texto donde\n"
            "creias tener un numero.\n\n"
            "## El tipo decide lo que hace el operador\n"
            "```python\n"
            "print(2 + 3)          # 5      -> con numeros, + suma\n"
            "print('2' + '3')      # 23     -> con textos, + pega uno detras del otro\n"
            "print('ab' * 3)       # ababab -> y * repite el texto\n"
            "print(2 * 3)          # 6      -> con numeros, * multiplica\n"
            "# print('2' + 3)      # TypeError: no se puede pegar un texto con un numero\n"
            "```\n"
            "Ese `TypeError` es de los que mas vas a ver, y casi siempre significa\n"
            "lo mismo: te falta una conversion.\n\n"
            "## Convertir de un tipo a otro\n"
            "```python\n"
            "print(int('12'))      # 12    -> texto a entero\n"
            "print(int('12') + 3)  # 15    -> ya convertido, suma de verdad\n"
            "print(str(25))        # 25    -> numero a texto (ahora es '25')\n"
            "print(float('3'))     # 3.0   -> a decimal, aunque venga sin decimales\n"
            "print(int(3.9))       # 3     -> TRUNCA: se come los decimales\n"
            "print(round(3.9))     # 4     -> esto SI redondea\n"
            "```\n"
            "`int(...)` corta, no redondea: `int(3.9)` es 3, no 4. Y ojo con\n"
            "`int('3.5')`, que revienta con `ValueError`: hay que pasar primero\n"
            "por `float('3.5')` y despues, si quieres, por `int(...)`.\n\n"
            "## Numeros: las cuatro operaciones menos obvias\n"
            "```python\n"
            "print(7 / 2)          # 3.5  -> / SIEMPRE da float, aunque salga exacto\n"
            "print(6 / 2)          # 3.0  -> ves? con punto\n"
            "print(7 // 2)         # 3    -> // divide y se queda con la parte entera\n"
            "print(7 % 2)          # 1    -> % da el RESTO de esa division\n"
            "print(2 ** 3)         # 8    -> ** es elevar a\n"
            "```\n"
            "`//` y `%` van juntos y resuelven mas de lo que parece: repartir 17\n"
            "caramelos entre 5 ninos es `17 // 5` para cada uno y `17 % 5` para\n"
            "los que sobran. Y `n % 2 == 0` es como se pregunta si un numero es\n"
            "par.\n\n"
            "## Texto: lo que se le puede pedir a un str\n"
            "```python\n"
            "entrada = '  Ana Perez  '\n"
            "print(len(entrada))              # 13   -> cuenta TODO, espacios incluidos\n"
            "print(entrada.strip())           # Ana Perez  -> quita los espacios de los lados\n"
            "print(entrada.strip().upper())   # ANA PEREZ  -> y se pueden encadenar\n"
            "print('Ana Perez'.split())       # ['Ana', 'Perez']  -> parte por los espacios\n"
            "print('ana' == 'Ana')            # False  -> distingue mayusculas de minusculas\n"
            "```\n"
            "`.strip()` y `.upper()` **no cambian** el texto original: devuelven\n"
            "uno nuevo. Si quieres quedartelo, tienes que guardarlo:\n"
            "`nombre = entrada.strip()`.\n\n"
            "## Booleanos: el resultado de preguntar\n"
            "```python\n"
            "edad = 18\n"
            "mayor = edad >= 18          # una comparacion DEVUELVE un bool\n"
            "print(mayor)                # True\n"
            "print(type(mayor))          # <class 'bool'>\n"
            "print(edad == 20)           # False  -> == compara, = asigna\n"
            "print(int(True), int(False))    # 1 0  -> por dentro son 1 y 0\n"
            "```\n"
            "No hace falta escribir `if` para tener un booleano: cualquier\n"
            "comparacion ya lo es, y se puede guardar en una variable como\n"
            "cualquier otro dato. En la proxima leccion los usaras para decidir.\n\n"
            "## Errores comunes\n"
            "- Sumar texto con numero: `'2' + 3` es `TypeError`. Convierte antes:\n"
            "  `int('2') + 3`. Si el dato viene de fuera (un archivo, un\n"
            "  formulario), casi siempre llega como texto.\n"
            "- Escribir los decimales con coma: `altura = 1,72` no da error, pero\n"
            "  **no es un numero**: la coma crea una tupla `(1, 72)`. En Python el\n"
            "  decimal se escribe con punto.\n"
            "- `int('3.5')` lanza `ValueError`. `int` solo entiende textos que ya\n"
            "  son numeros enteros; para lo demas, `float('3.5')` primero.\n"
            "- Escribir `true` o `TRUE`. En Python son `True` y `False`, con la\n"
            "  primera letra en mayuscula y sin comillas: con comillas serian\n"
            "  texto.\n"
            "- Esperar que `int(3.9)` redondee. Trunca. Si quieres el 4, es\n"
            "  `round(3.9)`.\n"
            "- Llamar a un metodo de texto y no guardar el resultado:\n"
            "  `entrada.strip()` a secas no cambia `entrada`, y te preguntas por\n"
            "  que siguen los espacios.\n\n"
            "## Resumen\n"
            "- Cuatro tipos base: `int` (entero), `float` (decimal con punto),\n"
            "  `str` (texto entre comillas) y `bool` (`True`/`False`).\n"
            "- `type(x)` dice de que tipo es algo; util cuando algo no cuadra.\n"
            "- El tipo decide lo que hace el operador: `+` suma numeros y pega\n"
            "  textos.\n"
            "- `int()`, `float()` y `str()` convierten; `int()` trunca y `round()`\n"
            "  redondea.\n"
            "- `/` da decimal, `//` da la parte entera, `%` da el resto y `**`\n"
            "  eleva.\n"
            "- Del texto: `len`, `.strip()`, `.upper()`, `.split()`, y que\n"
            "  devuelven uno nuevo en vez de cambiar el original.\n"
            "- Una comparacion (`>=`, `==`) devuelve un booleano que puedes\n"
            "  guardar.\n"
        ),
        difficulty="beginner",
        category="fundamentos",
        order=2,
        estimated_duration=45,
        prerequisites_titles=["Python desde Cero"],
        exercises=[
            ExerciseTemplate(
                title="Conversor simple",
                description="Un texto que parece numero no es un numero.",
                instructions=(
                    "`texto_numero` vale `'12'`, con comillas: es texto, no un "
                    "numero. Conviertelo a entero, calcula su doble e imprime "
                    "solo el resultado.\n\n"
                    "La salida tiene que ser exactamente `24`. Si te sale `1212`, "
                    "es que multiplicaste el texto sin convertirlo."
                ),
                starter_code="texto_numero = '12'\n# TODO\n",
                hints=[
                    "int(texto_numero) te da el 12 como numero.",
                    "Guardalo en una variable y multiplicalo por 2 antes de imprimir.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "imprime el doble (24)",
                        "code": "assert '24' in _salida, ('esperaba 24 en la salida', _salida)",
                    },
                    {
                        "name": "imprime el numero solo, sin texto alrededor",
                        "code": (
                            "assert _salida.strip() == '24', "
                            "f'salio {_salida.strip()!r} y se esperaba 24'"
                        ),
                    },
                    {
                        "name": "no multiplicaste el texto",
                        "code": (
                            "assert '24' in _salida, ('esperaba 24 en la salida', _salida)\n"
                            "assert '1212' not in _salida, "
                            "'multiplicaste el texto sin convertirlo: te falta el int()'\n"
                            "assert texto_numero == '12', 'no cambies el valor del starter'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Chequeo de tipos",
                description="Mirar de que esta hecho cada dato.",
                instructions=(
                    "Imprime el tipo de `edad`, `altura` y `activo`, en ese orden "
                    "y uno por linea, usando `type(...)`.\n\n"
                    "La primera linea sera `<class 'int'>`."
                ),
                starter_code="edad = 18\naltura = 1.72\nactivo = True\n# TODO\n",
                hints=[
                    "print(type(edad)) imprime el tipo de edad.",
                    "Son tres prints, uno por variable y en el orden del enunciado.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "muestra int, float y bool",
                        "code": (
                            "assert 'int' in _salida and 'float' in _salida and 'bool' in _salida, _salida"
                        ),
                    },
                    {
                        "name": "tres lineas, en el orden del enunciado",
                        "code": (
                            "lineas = [l for l in _salida.strip().split(chr(10)) if l.strip()]\n"
                            "assert len(lineas) == 3, ('esperaba 3 lineas', lineas)\n"
                            "assert 'int' in lineas[0] and 'float' in lineas[1] "
                            "and 'bool' in lineas[2], f'el orden no cuadra: {lineas}'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="De dias a horas",
                description="Convertir el texto y operar con el resultado.",
                instructions=(
                    "`dias_texto` es el numero de dias, pero como texto. "
                    "Conviertelo a entero en una variable llamada `dias`, calcula "
                    "las horas que son en una variable `horas` (24 por dia) e "
                    "imprime exactamente:\n\n"
                    "    15 dias son 360 horas\n\n"
                    "Los dos numeros salen de las variables, con una f-string."
                ),
                starter_code="dias_texto = '15'\n# TODO: dias, horas y la linea\n",
                hints=[
                    "dias = int(dias_texto)",
                    "horas = dias * 24",
                    "print(f'{dias} dias son {horas} horas')",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "dias es un entero de verdad",
                        "code": (
                            "assert dias == 15, f'dias vale {dias!r}'\n"
                            "assert isinstance(dias, int), "
                            "f'dias sigue siendo {type(dias).__name__}: te falta el int()'"
                        ),
                    },
                    {
                        "name": "las horas salen de la multiplicacion",
                        "code": (
                            "assert horas == 360, f'horas vale {horas!r}'\n"
                            "assert horas == dias * 24, 'horas no coincide con dias * 24'"
                        ),
                    },
                    {
                        "name": "la linea exacta",
                        "code": (
                            "assert _salida.strip() == '15 dias son 360 horas', "
                            "f'salio {_salida.strip()!r}'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Limpiar un nombre",
                description="Los metodos de texto devuelven uno nuevo.",
                instructions=(
                    "`entrada` viene con espacios de sobra y en minusculas. "
                    "Guarda en `nombre` el texto sin los espacios de los lados y "
                    "en mayusculas, guarda en `letras` su longitud, e imprime:\n\n"
                    "    Hola, ANA PEREZ (9)\n\n"
                    "El 9 es `letras`: la longitud del nombre ya limpio, espacio "
                    "del medio incluido."
                ),
                starter_code="entrada = '  ana perez  '\n# TODO: nombre, letras y la linea\n",
                hints=[
                    ".strip() quita los espacios de los lados y .upper() pasa a mayusculas.",
                    "Se pueden encadenar: entrada.strip().upper().",
                    "Hay que GUARDARLO: nombre = entrada.strip().upper(), si no, entrada sigue igual.",
                    "letras = len(nombre), y despues print(f'Hola, {nombre} ({letras})').",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "el nombre queda limpio y en mayusculas",
                        "code": (
                            "assert nombre == 'ANA PEREZ', f'nombre vale {nombre!r}'"
                        ),
                    },
                    {
                        "name": "letras cuenta el nombre ya limpio",
                        "code": (
                            "assert letras == 9, "
                            "f'letras vale {letras!r}: son las del nombre limpio, no las de entrada'"
                        ),
                    },
                    {
                        "name": "la linea exacta",
                        "code": (
                            "assert _salida.strip() == 'Hola, ANA PEREZ (9)', "
                            "f'salio {_salida.strip()!r}'"
                        ),
                    },
                    {
                        "name": "entrada no se toca",
                        "code": (
                            "assert entrada == '  ana perez  ', "
                            "'entrada deberia seguir igual: los metodos devuelven un texto nuevo'\n"
                            "assert nombre == 'ANA PEREZ'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Reparto de caramelos",
                description="Division entera, resto y un booleano.",
                instructions=(
                    "Hay que repartir `caramelos` entre `ninos` a partes iguales, "
                    "sin partir ninguno.\n\n"
                    "Calcula `cada_uno` (cuantos le tocan a cada uno), `sobran` "
                    "(los que quedan sin repartir) y `exacto` (un booleano: True "
                    "si no sobra ninguno). Despues imprime estas tres lineas:\n\n"
                    "    Cada uno: 3\n"
                    "    Sobran: 2\n"
                    "    Exacto: False"
                ),
                starter_code=(
                    "caramelos = 17\n"
                    "ninos = 5\n"
                    "# TODO: cada_uno, sobran, exacto y las tres lineas\n"
                ),
                hints=[
                    "cada_uno = caramelos // ninos  -> la division que se queda con la parte entera.",
                    "sobran = caramelos % ninos  -> el resto de esa misma division.",
                    "exacto es una comparacion, no un if: exacto = sobran == 0.",
                    "Tres prints con f-string, en el orden del enunciado.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "el reparto y el resto",
                        "code": (
                            "assert cada_uno == 3, f'cada_uno vale {cada_uno!r}'\n"
                            "assert sobran == 2, f'sobran vale {sobran!r}'"
                        ),
                    },
                    {
                        "name": "exacto es un booleano, no un texto",
                        "code": (
                            "assert exacto is False, f'exacto vale {exacto!r}'\n"
                            "assert isinstance(exacto, bool), "
                            "f'exacto es {type(exacto).__name__}: sale de una comparacion'"
                        ),
                    },
                    {
                        "name": "las cuentas salen de caramelos y ninos",
                        "code": (
                            "assert cada_uno == caramelos // ninos\n"
                            "assert sobran == caramelos % ninos\n"
                            "assert caramelos == 17 and ninos == 5, 'no cambies el starter'"
                        ),
                    },
                    {
                        "name": "las tres lineas exactas",
                        "code": (
                            "lineas = [l for l in _salida.strip().split(chr(10)) if l.strip()]\n"
                            "esperado = ['Cada uno: 3', 'Sobran: 2', 'Exacto: False']\n"
                            "assert lineas == esperado, f'esperaba {esperado} y salio {lineas}'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="El ticket del cine",
                description="El pipeline: convertir, calcular, limpiar texto y comparar.",
                instructions=(
                    "Los tres datos llegan como texto, que es como suelen llegar "
                    "los datos de fuera. Prepara el ticket:\n\n"
                    "- `precio`: `precio_texto` convertido a decimal.\n"
                    "- `entradas`: `entradas_texto` convertido a entero.\n"
                    "- `total`: precio por entradas, redondeado a 2 decimales con "
                    "`round(x, 2)`.\n"
                    "- `cliente`: `nombre_texto` sin espacios de los lados y en "
                    "mayusculas.\n"
                    "- `es_grupo`: booleano, True si hay 3 entradas o mas.\n\n"
                    "Y despues imprime exactamente:\n\n"
                    "    Cliente: ANA\n"
                    "    Entradas: 3\n"
                    "    Total: 29.97\n"
                    "    Grupo: True"
                ),
                starter_code=(
                    "precio_texto = '9.99'\n"
                    "entradas_texto = '3'\n"
                    "nombre_texto = '  ana  '\n"
                    "# TODO: precio, entradas, total, cliente, es_grupo y las cuatro lineas\n"
                ),
                hints=[
                    "precio = float(precio_texto) y entradas = int(entradas_texto): "
                    "uno lleva decimales y el otro no.",
                    "total = round(precio * entradas, 2)  -> sin el round te saldrian "
                    "decimales de mas por como se guardan los float.",
                    "cliente = nombre_texto.strip().upper()",
                    "es_grupo = entradas >= 3, y las cuatro lineas con f-strings en el orden dado.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "las conversiones dejan el tipo correcto",
                        "code": (
                            "assert precio == 9.99 and isinstance(precio, float), "
                            "f'precio vale {precio!r} ({type(precio).__name__})'\n"
                            "assert entradas == 3 and isinstance(entradas, int), "
                            "f'entradas vale {entradas!r} ({type(entradas).__name__})'"
                        ),
                    },
                    {
                        "name": "el total esta calculado y redondeado",
                        "code": (
                            "assert total == 29.97, f'total vale {total!r}'\n"
                            "assert total == round(precio * entradas, 2), "
                            "'total no coincide con round(precio * entradas, 2)'"
                        ),
                    },
                    {
                        "name": "el nombre queda limpio y en mayusculas",
                        "code": (
                            "assert cliente == 'ANA', f'cliente vale {cliente!r}'\n"
                            "assert nombre_texto == '  ana  ', 'no cambies el starter'"
                        ),
                    },
                    {
                        "name": "es_grupo es un booleano que sale de comparar",
                        "code": (
                            "assert es_grupo is True, f'es_grupo vale {es_grupo!r}'\n"
                            "assert isinstance(es_grupo, bool), "
                            "f'es_grupo es {type(es_grupo).__name__}'"
                        ),
                    },
                    {
                        "name": "las cuatro lineas exactas",
                        "code": (
                            "lineas = [l for l in _salida.strip().split(chr(10)) if l.strip()]\n"
                            "esperado = ['Cliente: ANA', 'Entradas: 3', 'Total: 29.97', "
                            "'Grupo: True']\n"
                            "assert lineas == esperado, f'esperaba {esperado} y salio {lineas}'"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Condicionales y Logica",
        description=(
            "if, elif y else para que el programa decida, con comparadores, "
            "and/or/not y lo que Python considera verdadero."
        ),
        content=(
            "## Por que decidir\n"
            "Hasta ahora tus programas hacen siempre lo mismo, pase lo que pase\n"
            "con los datos. Un programa util no: cobra distinto a un socio, avisa\n"
            "solo si el saldo esta bajo, deja pasar al que tiene entrada. Todo eso\n"
            "es **una condicion**, y es lo que separa un guion de un programa.\n\n"
            "## if: hacer algo solo si se cumple algo\n"
            "```python\n"
            "edad = 20                      # el dato que se va a mirar\n"
            "if edad >= 18:                 # la condicion da True o False\n"
            "    print('mayor de edad')     # SOLO corre si dio True\n"
            "print('esto sale siempre')     # fuera del if: no depende de nada\n"
            "```\n"
            "La forma es fija: `if`, la condicion, **dos puntos**, y debajo el\n"
            "bloque **indentado** cuatro espacios. Aqui es donde la sangria que\n"
            "viste en la primera leccion deja de ser estetica: es como Python sabe\n"
            "que lineas van dentro del `if` y cuales no.\n\n"
            "## else y elif: los otros caminos\n"
            "```python\n"
            "nota = 4\n"
            "if nota >= 9:                 # se prueba primero\n"
            "    print('sobresaliente')     # no llega: 4 no es >= 9\n"
            "elif nota >= 5:            # solo se mira si la de arriba fue False\n"
            "    print('aprobado')          # tampoco: 4 no es >= 5\n"
            "else:                      # si no se cumplio ninguna\n"
            "    print('suspenso')      # suspenso  <- lo que sale con nota = 4\n"
            "```\n"
            "Python las prueba **en orden y se para en la primera que se cumple**.\n"
            "Por eso el orden importa: si pones `nota >= 5` arriba del todo, un 10\n"
            "tambien entra por ahi y nunca llegas a `sobresaliente`. De lo general\n"
            "a lo particular no; de lo particular a lo general si.\n\n"
            "## Los comparadores\n"
            "```python\n"
            "print(5 == 5)          # True   -> == compara, = asigna\n"
            "print(5 != 3)          # True   -> != es 'distinto de'\n"
            "print(3 < 5, 5 <= 5)   # True True\n"
            "print('ana' == 'Ana')  # False  -> el texto distingue mayusculas\n"
            "print(18 <= 20 <= 65)  # True   -> se pueden encadenar dos de golpe\n"
            "```\n"
            "Cuidado con los bordes: `edad > 18` deja fuera al que tiene\n"
            "exactamente 18. Si el 18 cuenta, es `>=`. La mitad de los fallos de\n"
            "logica de un programa estan en esa diferencia.\n\n"
            "## and, or, not: combinar preguntas\n"
            "```python\n"
            "tiene_pase = True                  # ya es un booleano\n"
            "edad = 19                          # esto todavia no lo es\n"
            "print(tiene_pase and edad >= 18)   # True  -> and: tienen que cumplirse LAS DOS\n"
            "print(tiene_pase and edad >= 65)   # False -> una falla, y ya\n"
            "print(tiene_pase or edad >= 65)    # True  -> or: basta con una\n"
            "print(not tiene_pase)              # False -> not le da la vuelta\n"
            "```\n"
            "Cada lado tiene que ser una pregunta completa:\n"
            "`edad >= 5 and edad <= 9`, repitiendo el nombre. `edad >= 5 and <= 9`\n"
            "no es Python y da `SyntaxError`.\n\n"
            "## Lo que Python considera falso\n"
            "Una condicion no tiene por que ser una comparacion: cualquier valor\n"
            "sirve, y Python decide si cuenta como verdadero:\n"
            "```python\n"
            "nombre = ''                     # vacio, pero es un texto\n"
            "if nombre:                      # un texto vacio cuenta como False\n"
            "    print('hay nombre')         # asi que esta rama no entra\n"
            "else:                           # y se va por aqui\n"
            "    print('falta el nombre')    # falta el nombre  <- lo que sale\n\n"
            "print(bool(''), bool('ana'))    # False True  -> texto vacio es falso\n"
            "print(bool(0), bool(5))         # False True  -> el cero es falso\n"
            "```\n"
            "Por eso `if nombre:` se lee como *si hay nombre*. Es comodo, pero\n"
            "solo cuando lo que quieres preguntar es de verdad *esta vacio o no*;\n"
            "si lo que quieres saber es si vale cero, dilo: `if total == 0:`.\n\n"
            "## Anidar: un if dentro de otro\n"
            "```python\n"
            "edad = 20                        # cumple el primer if\n"
            "tiene_entrada = False            # pero no el de dentro\n"
            "if edad >= 18:                   # nivel 1\n"
            "    if tiene_entrada:                     # solo se mira si el de fuera fue True\n"
            "        print('pasa')                     # nivel 2: no entra\n"
            "    else:                                 # el else del if de dentro\n"
            "        print('mayor, pero sin entrada')  # <- lo que sale\n"
            "else:                            # el del de fuera: ni se mira\n"
            "    print('menor de edad')\n"
            "```\n"
            "Cada nivel son cuatro espacios mas. Y una regla practica: si te sale\n"
            "un tercer nivel, casi siempre se puede aplanar juntando las dos\n"
            "condiciones con `and`.\n\n"
            "## Errores comunes\n"
            "- Escribir `=` donde va `==`: `if edad = 18:` es `SyntaxError`. El de\n"
            "  uno solo asigna, el de dos compara.\n"
            "- Olvidar los dos puntos al final del `if`, del `elif` o del `else`.\n"
            "  `SyntaxError` en esa misma linea.\n"
            "- No indentar el bloque de debajo: `IndentationError: expected an\n"
            "  indented block`. Despues de los dos puntos **siempre** viene algo\n"
            "  indentado.\n"
            "- Poner la condicion general antes que la concreta. Con\n"
            "  `if nota >= 5` primero, un 10 ya nunca llega al `elif nota >= 9`:\n"
            "  esa rama se vuelve inalcanzable y no hay ningun error que te avise.\n"
            "- Confundir `>` con `>=` en el borde. Con `edad > 18`, el de 18 anos\n"
            "  se queda fuera.\n"
            "- Encadenar mal: `if edad >= 5 and <= 9:`. Hay que repetir el nombre:\n"
            "  `edad >= 5 and edad <= 9` (o `5 <= edad <= 9`).\n\n"
            "## Resumen\n"
            "- `if condicion:` + bloque indentado ejecuta ese bloque solo si la\n"
            "  condicion es verdadera.\n"
            "- `elif` anade otro camino y `else` recoge todo lo demas; se prueban\n"
            "  en orden y gana el primero que se cumple.\n"
            "- Comparadores: `==`, `!=`, `<`, `>`, `<=`, `>=`, y se pueden\n"
            "  encadenar (`18 <= edad <= 65`).\n"
            "- `and` pide las dos, `or` se conforma con una, `not` invierte.\n"
            "- El texto vacio y el cero cuentan como falsos: por eso funciona\n"
            "  `if nombre:`.\n"
            "- Anidar es meter un `if` dentro de otro; mas de dos niveles suele\n"
            "  ser un `and` disfrazado.\n"
        ),
        difficulty="beginner",
        category="control-flujo",
        order=3,
        estimated_duration=45,
        prerequisites_titles=["Variables y Tipos"],
        exercises=[
            ExerciseTemplate(
                title="Clasificador de edad",
                description="Tu primera cadena if/elif/else.",
                instructions=(
                    "Con la `edad` del starter, guarda en una variable `etapa` el "
                    "texto que corresponda e imprimelo:\n\n"
                    "- `menor` si es menor de 18,\n"
                    "- `adulto` si tiene 18 o mas pero menos de 65,\n"
                    "- `senior` si tiene 65 o mas.\n\n"
                    "Con `edad = 17` la salida es `menor`."
                ),
                starter_code="edad = 17\n# TODO: etapa, con if/elif/else, y despues imprimela\n",
                hints=[
                    "Empieza por el caso mas concreto: if edad < 18: etapa = 'menor'.",
                    "El de en medio es elif edad < 65, que solo se mira si no era menor.",
                    "El ultimo es else: etapa = 'senior'. Y el print va fuera, al final.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "edad 17 -> menor",
                        "code": "assert 'menor' in _salida.lower(), _salida",
                    },
                    {
                        "name": "la etapa queda guardada en su variable",
                        "code": (
                            "assert etapa == 'menor', f'etapa vale {etapa!r}'\n"
                            "assert _salida.strip() == 'menor', "
                            "f'salio {_salida.strip()!r}: imprime solo la etapa'"
                        ),
                    },
                    {
                        "name": "no se imprimieron las otras ramas",
                        "code": (
                            "assert 'menor' in _salida, ('esperaba menor en la salida', _salida)\n"
                            "assert 'adulto' not in _salida and 'senior' not in _salida, "
                            "f'salieron varias ramas: {_salida!r}'\n"
                            "assert edad == 17, 'no cambies la edad del starter'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Acceso permitido",
                description="Dos condiciones que se tienen que cumplir a la vez.",
                instructions=(
                    "Imprime `Acceso permitido` si `tiene_pase` es verdadero **y** "
                    "`edad` es 18 o mas. En cualquier otro caso, imprime "
                    "`Acceso denegado`.\n\n"
                    "Una sola linea de salida, y las dos condiciones en el mismo "
                    "`if`, unidas por `and`."
                ),
                starter_code="tiene_pase = True\nedad = 19\n# TODO\n",
                hints=[
                    "La condicion es tiene_pase and edad >= 18.",
                    "tiene_pase ya es un booleano: no hace falta escribir "
                    "tiene_pase == True.",
                    "El else imprime 'Acceso denegado'.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "pase + mayor de edad -> permitido",
                        "code": "assert 'permitido' in _salida.lower(), _salida",
                    },
                    {
                        "name": "la linea exacta y sin la otra rama",
                        "code": (
                            "assert _salida.strip() == 'Acceso permitido', "
                            "f'salio {_salida.strip()!r}'\n"
                            "assert 'denegado' not in _salida.lower(), "
                            "'se imprimieron las dos ramas'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Descuento de socio",
                description="Una condicion que decide una cuenta.",
                instructions=(
                    "En esta tienda hay un 10% de descuento, pero solo para socios "
                    "y solo a partir de 50 euros de compra.\n\n"
                    "Guarda en `precio_final` lo que hay que pagar: el 90% del "
                    "precio si se cumplen las dos cosas, y el precio entero si no. "
                    "Despues imprime exactamente `Pagas 72.0`."
                ),
                starter_code=(
                    "precio = 80\n"
                    "es_socio = True\n"
                    "# TODO: precio_final y la linea\n"
                ),
                hints=[
                    "Las dos condiciones van juntas: if es_socio and precio >= 50:",
                    "Quitar un 10% es quedarse con el 90%: precio * 0.9.",
                    "En el else, precio_final = precio, sin tocar nada.",
                    "print(f'Pagas {precio_final}')",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "aplica el descuento",
                        "code": (
                            "assert precio_final == 72.0, f'precio_final vale {precio_final!r}'"
                        ),
                    },
                    {
                        "name": "el precio sale de la cuenta, no escrito a mano",
                        "code": (
                            "assert precio_final == precio * 0.9, "
                            "'precio_final no coincide con precio * 0.9'\n"
                            "assert precio == 80 and es_socio is True, "
                            "'no cambies los datos del starter'"
                        ),
                    },
                    {
                        "name": "la linea exacta",
                        "code": (
                            "assert _salida.strip() == 'Pagas 72.0', "
                            "f'salio {_salida.strip()!r}'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="La nota en palabras",
                description="Una cadena de tres ramas, en el orden correcto.",
                instructions=(
                    "Guarda en `resultado` la palabra que le toca a la `nota` e "
                    "imprimela:\n\n"
                    "- `sobresaliente` con 9 o mas,\n"
                    "- `aprobado` con 5 o mas (pero menos de 9),\n"
                    "- `suspenso` con menos de 5.\n\n"
                    "Ojo al orden de las ramas: si empiezas por la de 5, un 10 "
                    "entra por ahi y nunca llega a sobresaliente."
                ),
                starter_code="nota = 7\n# TODO: resultado y su print\n",
                hints=[
                    "La primera rama es la mas exigente: if nota >= 9.",
                    "Despues elif nota >= 5, que ya solo ve las que no llegaron a 9.",
                    "El else recoge el resto: no hace falta comprobar nada mas.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "un 7 es aprobado",
                        "code": (
                            "assert resultado == 'aprobado', f'resultado vale {resultado!r}'\n"
                            "assert _salida.strip() == 'aprobado', "
                            "f'salio {_salida.strip()!r}'"
                        ),
                    },
                    {
                        "name": "la palabra corresponde a la nota",
                        "code": (
                            "esperado = 'sobresaliente' if nota >= 9 else ("
                            "'aprobado' if nota >= 5 else 'suspenso')\n"
                            "assert resultado == esperado, "
                            "f'con nota {nota} tocaba {esperado!r} y hay {resultado!r}'"
                        ),
                    },
                    {
                        "name": "solo se imprimio una rama",
                        "code": (
                            "assert 'aprobado' in _salida, ('esperaba aprobado en la salida', _salida)\n"
                            "assert 'suspenso' not in _salida and 'sobresaliente' not in _salida, "
                            "f'salio mas de una rama: {_salida!r}'\n"
                            "assert nota == 7, 'no cambies la nota del starter'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Tarifa del parking",
                description="Varias condiciones encadenadas sobre la misma cuenta.",
                instructions=(
                    "La hora del parking cuesta 2 euros. Ademas:\n\n"
                    "- los festivos se cobra un 50% mas,\n"
                    "- los abonados no pagan nada, sea festivo o no.\n\n"
                    "Calcula `base` (lo que costaria antes de mirar el abono, "
                    "recargo de festivo incluido) y `total` (lo que se paga de "
                    "verdad). Despues imprime dos lineas:\n\n"
                    "    Base: 9.0\n"
                    "    Total: 9.0"
                ),
                starter_code=(
                    "horas = 3\n"
                    "es_festivo = True\n"
                    "abonado = False\n"
                    "# TODO: base, total y las dos lineas\n"
                ),
                hints=[
                    "Empieza siempre igual: base = horas * 2.",
                    "Y despues, si es festivo, la subes: base = base * 1.5.",
                    "El abono decide el total: if abonado: total = 0, else: total = base.",
                    "Dos prints con f-string, primero Base y despues Total.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "la base lleva el recargo de festivo",
                        "code": (
                            "assert base == 9.0, f'base vale {base!r}'\n"
                            "assert base == horas * 2 * 1.5, "
                            "'la base no coincide con horas * 2 mas el 50% de festivo'"
                        ),
                    },
                    {
                        "name": "sin abono se paga la base entera",
                        "code": (
                            "assert total == 9.0, f'total vale {total!r}'\n"
                            "assert total == base, "
                            "'este cliente no es abonado: deberia pagar la base'"
                        ),
                    },
                    {
                        "name": "las dos lineas exactas",
                        "code": (
                            "lineas = [l for l in _salida.strip().split(chr(10)) if l.strip()]\n"
                            "assert lineas == ['Base: 9.0', 'Total: 9.0'], "
                            "f'salio {lineas}'"
                        ),
                    },
                    {
                        "name": "no cambiaste los datos del starter",
                        "code": (
                            "assert horas == 3 and es_festivo is True and abonado is False, "
                            "'los datos del starter tienen que quedarse como estan'\n"
                            "assert base == 9.0 and total == 9.0"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Matricula del curso",
                description="El pipeline: un booleano compuesto, una cadena de ramas y un texto vacio.",
                instructions=(
                    "Para matricularse hacen falta tres cosas a la vez: media de 5 "
                    "o mas, 30 creditos o mas, y no estar sancionado.\n\n"
                    "- `apto`: un booleano con esas tres condiciones combinadas. "
                    "No uses `if`: guarda directamente la comparacion.\n"
                    "- `estado`: `honor` si ademas la media es 9 o mas, `apto` si "
                    "solo cumple lo basico, y `no apto` si no cumple.\n"
                    "- `mensaje_beca`: si `beca` tiene algo escrito, "
                    "`con beca: <lo que ponga>`; si esta vacia, `sin beca`. "
                    "Aprovecha que un texto vacio cuenta como falso.\n\n"
                    "Y despues imprime tres lineas:\n\n"
                    "    Apto: True\n"
                    "    Estado: apto\n"
                    "    sin beca"
                ),
                starter_code=(
                    "nota_media = 6.5\n"
                    "creditos = 42\n"
                    "sancionado = False\n"
                    "beca = ''\n"
                    "# TODO: apto, estado, mensaje_beca y las tres lineas\n"
                ),
                hints=[
                    "apto = nota_media >= 5 and creditos >= 30 and not sancionado  "
                    "-> una sola linea, sin if.",
                    "Para estado, la rama mas exigente primero: "
                    "if apto and nota_media >= 9.",
                    "Para la beca: if beca: mensaje_beca = f'con beca: {beca}' "
                    "y en el else, 'sin beca'.",
                    "Las tres lineas: Apto y Estado con etiqueta, y la de la beca "
                    "es el mensaje tal cual.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "apto es un booleano con las tres condiciones",
                        "code": (
                            "assert apto is True, f'apto vale {apto!r}'\n"
                            "assert isinstance(apto, bool), "
                            "f'apto es {type(apto).__name__}: sale de comparar, no de un texto'\n"
                            "assert apto == (nota_media >= 5 and creditos >= 30 and not sancionado)"
                        ),
                    },
                    {
                        "name": "el estado corresponde a la media",
                        "code": (
                            "assert estado == 'apto', "
                            "f'estado vale {estado!r}: con 6.5 no hay honor, pero si apto'"
                        ),
                    },
                    {
                        "name": "la beca vacia da 'sin beca'",
                        "code": (
                            "assert mensaje_beca == 'sin beca', "
                            "f'mensaje_beca vale {mensaje_beca!r}'\n"
                            "assert beca == '', 'no cambies el starter: la beca esta vacia a proposito'"
                        ),
                    },
                    {
                        "name": "las tres lineas exactas",
                        "code": (
                            "lineas = [l for l in _salida.strip().split(chr(10)) if l.strip()]\n"
                            "esperado = ['Apto: True', 'Estado: apto', 'sin beca']\n"
                            "assert lineas == esperado, f'esperaba {esperado} y salio {lineas}'"
                        ),
                    },
                    {
                        "name": "el estado sale de las reglas, no escrito a mano",
                        "code": (
                            "esperado = 'honor' if (apto and nota_media >= 9) else ("
                            "'apto' if apto else 'no apto')\n"
                            "assert estado == esperado, "
                            "f'con media {nota_media} tocaba {esperado!r} y hay {estado!r}'\n"
                            "assert 'honor' not in _salida and 'no apto' not in _salida, "
                            "f'se colo otra rama en la salida: {_salida!r}'"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Bucles for y while",
        description=(
            "Repetir trabajo con for y while, generar numeros con range, "
            "acumular resultados y cortar o saltar vueltas con break y continue."
        ),
        content=(
            "## Por que los bucles\n"
            "Sin bucles, procesar 500 ventas significa escribir 500 lineas casi\n"
            "identicas. Con un bucle escribes **una vez** la instruccion y le\n"
            "dices a Python cuantas veces repetirla. Es la diferencia entre un\n"
            "programa que sirve para un caso y uno que sirve para cualquier\n"
            "cantidad de datos.\n\n"
            "## for: recorrer una secuencia\n"
            "`for` toma los elementos de algo que se puede recorrer (una lista,\n"
            "un texto) y ejecuta el cuerpo una vez por elemento:\n"
            "```python\n"
            "notas = [7, 9, 4]\n"
            "for nota in notas:       # 'nota' vale 7, luego 9, luego 4\n"
            "    print(nota * 10)     # imprime 70, luego 90, luego 40\n\n"
            "for letra in 'sol':      # un string se recorre caracter a caracter\n"
            "    print(letra)         # imprime s, luego o, luego l\n"
            "```\n"
            "La variable del bucle (`nota`, `letra`) la creas tu ahi mismo y\n"
            "cambia en cada vuelta. El cuerpo va **indentado**: la indentacion es\n"
            "lo que marca que una linea esta dentro del bucle.\n\n"
            "## range: fabricar numeros\n"
            "Cuando quieres repetir N veces o recorrer numeros, `range` los\n"
            "genera sin que tengas que escribirlos:\n"
            "```python\n"
            "range(5)          # 0, 1, 2, 3, 4  -> arranca en 0, NO incluye el 5\n"
            "range(2, 6)       # 2, 3, 4, 5     -> desde 2 hasta 5\n"
            "range(0, 10, 3)   # 0, 3, 6, 9     -> de 3 en 3\n"
            "range(5, 0, -1)   # 5, 4, 3, 2, 1  -> paso negativo, cuenta al reves\n\n"
            "for i in range(3):\n"
            "    print(i)      # imprime 0, luego 1, luego 2\n"
            "```\n"
            "El final **nunca se incluye**. Los numeros del 1 al 10 son\n"
            "`range(1, 11)`, no `range(1, 10)`.\n\n"
            "## Acumuladores: el patron que mas vas a usar\n"
            "Para sumar, contar o juntar cosas se usa siempre la misma forma: una\n"
            "variable **antes** del bucle y una actualizacion **dentro**.\n"
            "```python\n"
            "total = 0                    # 1) arranca FUERA del bucle\n"
            "for precio in [10, 25, 8]:\n"
            "    total = total + precio   # 2) se actualiza en cada vuelta\n"
            "print(total)                 # 43\n\n"
            "pares = []                   # tambien sirve para juntar en una lista\n"
            "for n in range(1, 7):\n"
            "    if n % 2 == 0:           # solo los pares\n"
            "        pares.append(n)      # append agrega al final\n"
            "print(pares)                 # [2, 4, 6]\n"
            "```\n"
            "`total += precio` es una forma corta de escribir\n"
            "`total = total + precio`.\n\n"
            "## while: repetir mientras se cumpla una condicion\n"
            "`for` sirve cuando sabes cuantas vueltas son. `while` sirve cuando lo\n"
            "que sabes es la **condicion de parada**:\n"
            "```python\n"
            "saldo = 100\n"
            "retiros = 0\n"
            "while saldo >= 30:        # se comprueba ANTES de cada vuelta\n"
            "    saldo = saldo - 30    # sin esta linea saldo nunca bajaria\n"
            "    retiros = retiros + 1\n"
            "print(saldo, retiros)     # 10 3  (baja 30 tres veces: 70, 40, 10)\n"
            "```\n"
            "La linea que cambia la condicion es **obligatoria**. Sin ella el bucle\n"
            "no termina jamas:\n"
            "```python\n"
            "# bucle infinito: nunca termina\n"
            "saldo = 100\n"
            "while saldo >= 30:\n"
            "    print('retirando...')   # falta la linea que baja el saldo,\n"
            "                            # asi que la condicion es True para siempre\n"
            "```\n"
            "Si ejecutas un bucle infinito en PyCode no se rompe nada: aparece el\n"
            "boton **Detener** para cortarlo, y si no lo pulsas el editor lo corta\n"
            "solo tras unos 30 segundos y te avisa. Fuera de PyCode, en tu\n"
            "ordenador, se queda girando hasta que lo mates tu. Antes de ejecutar\n"
            "un `while`, busca con el dedo la linea que acerca la condicion a ser\n"
            "falsa. Si no la encuentras, es que no esta.\n\n"
            "## break: cortar el bucle\n"
            "`break` sale del bucle inmediatamente, sin mirar los elementos que\n"
            "quedaban:\n"
            "```python\n"
            "for n in [4, 7, -2, 9]:\n"
            "    if n < 0:                   # dato invalido para esta funcion\n"
            "        print('negativo encontrado')  # se imprime una sola vez\n"
            "        break                         # corta aqui: el 9 no se mira\n"
            "    print(n)                          # imprime 4, luego 7\n"
            "```\n"
            "Es el patron de 'busca el primero que cumpla X y para': en cuanto lo\n"
            "encuentras no tiene sentido seguir recorriendo.\n\n"
            "## continue: saltar a la siguiente vuelta\n"
            "`continue` **no** sale del bucle: se salta el resto del cuerpo y pasa\n"
            "al siguiente elemento.\n"
            "```python\n"
            "suma = 0\n"
            "for n in [5, -1, 3, -8]:\n"
            "    if n < 0:\n"
            "        continue        # ignora este y sigue con el siguiente\n"
            "    suma = suma + n     # NO se ejecuta para -1 ni para -8\n"
            "print(suma)             # 8  (solo sumo 5 y 3)\n"
            "```\n"
            "Regla practica: `break` es 'ya termine'; `continue` es 'este no me\n"
            "sirve, siguiente'.\n\n"
            "## Errores comunes\n"
            "- Esperar que `range(1, 5)` incluya el 5. No lo incluye: son 1, 2, 3\n"
            "  y 4. Para llegar al 5 se escribe `range(1, 6)`.\n"
            "- Poner el acumulador DENTRO del bucle (`total = 0` indentado). Se\n"
            "  reinicia en cada vuelta y al final vale solo lo ultimo. Va fuera.\n"
            "- `while` cuya condicion nunca cambia: bucle infinito. Antes de\n"
            "  ejecutar, comprueba que en el cuerpo hay una linea que acerca la\n"
            "  condicion a ser falsa.\n"
            "- Usar `break` cuando querias `continue`. Con `break` descartas\n"
            "  tambien todo lo que venia despues, no solo el elemento actual.\n"
            "- Modificar una lista mientras la recorres con `for`. Los indices se\n"
            "  desplazan y acabas saltandote elementos; construye una lista nueva.\n\n"
            "## Resumen\n"
            "- `for` recorre una secuencia elemento a elemento; `while` repite\n"
            "  mientras una condicion sea verdadera.\n"
            "- `range(inicio, fin, paso)` fabrica numeros y **nunca incluye** el\n"
            "  final.\n"
            "- Acumulador: variable fuera del bucle, actualizacion dentro.\n"
            "- `break` corta el bucle entero; `continue` salta solo esta vuelta.\n"
            "- Todo `while` necesita una linea que acerque la condicion al final.\n"
        ),
        difficulty="beginner",
        category="control-flujo",
        order=4,
        estimated_duration=45,
        prerequisites_titles=["Condicionales y Logica"],
        exercises=[
            ExerciseTemplate(
                title="Tabla del 7",
                description="Genera una tabla de multiplicar con for y range.",
                instructions=(
                    "Usando un `for` con `range`, construye la lista `tabla` con "
                    "los diez primeros multiplos de 7: del 7x1 al 7x10. Debe "
                    "quedar [7, 14, 21, ..., 70]."
                ),
                starter_code=(
                    "tabla = []\n\n"
                    "# TODO: recorre range(1, 11) y ve agregando cada multiplo\n"
                ),
                hints=[
                    "range(1, 11) da los numeros del 1 al 10 (el 11 no entra).",
                    "Dentro del bucle: tabla.append(7 * i)",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "tabla tiene los 10 multiplos, en orden",
                        "code": (
                            "assert tabla == [7, 14, 21, 28, 35, 42, 49, 56, 63, 70], "
                            "f'tabla vale {tabla}'"
                        ),
                    },
                    {
                        "name": "son numeros, no texto",
                        "code": (
                            "assert len(tabla) == 10, "
                            "f'tabla tiene {len(tabla)} elementos, esperaba 10'\n"
                            "assert all(isinstance(x, int) for x in tabla), "
                            "'los elementos deben ser enteros, no strings'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Cuenta atras con while",
                description="Repite mientras se cumpla una condicion.",
                instructions=(
                    "Con un bucle `while` (no uses `for`), construye la lista "
                    "`cuenta` con los numeros del 5 al 1 en ese orden: "
                    "[5, 4, 3, 2, 1]. Empieza en 5 y ve bajando."
                ),
                starter_code=(
                    "cuenta = []\n"
                    "n = 5\n\n"
                    "# TODO: mientras n sea mayor o igual que 1, agrega n y bajalo\n"
                ),
                hints=[
                    "La condicion del while es n >= 1.",
                    "Dentro del bucle, despues de agregar, resta: n = n - 1. Sin esa "
                    "linea el bucle no termina nunca.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "cuenta baja de 5 a 1",
                        "code": "assert cuenta == [5, 4, 3, 2, 1], f'cuenta vale {cuenta}'",
                    },
                    {
                        "name": "el bucle termino de verdad",
                        "code": (
                            "assert n <= 0, 'n deberia haber bajado hasta salir del while'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Descartar lecturas invalidas",
                description="Salta los elementos que no sirven con continue.",
                instructions=(
                    "El sensor guarda un -1 cuando falla la medicion. Recorre "
                    "`lecturas` con un `for` y usa `continue` para saltarte los -1. "
                    "Deja en `total` la suma de las lecturas validas y en "
                    "`descartadas` cuantos -1 te encontraste."
                ),
                starter_code=(
                    "lecturas = [12, -1, 8, 20, -1, 5]\n"
                    "total = 0\n"
                    "descartadas = 0\n\n"
                    "# TODO: recorre lecturas; si vale -1, cuenta y salta con continue\n"
                ),
                hints=[
                    "El if va dentro del for: if lectura == -1:",
                    "Suma 1 a descartadas ANTES del continue, o no lo contaras.",
                    "Tras el continue, la linea que suma a total ya no se ejecuta en "
                    "esa vuelta.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "total suma solo las lecturas validas",
                        "code": "assert total == 45, f'total vale {total}, esperaba 45'",
                    },
                    {
                        "name": "cuenta bien las descartadas",
                        "code": (
                            "assert descartadas == 2, "
                            "f'descartadas vale {descartadas}, esperaba 2'"
                        ),
                    },
                    {
                        "name": "no se colaron los -1 en la suma",
                        "code": (
                            "assert total != 0, "
                            "'total sigue en 0: el bucle todavia no suma nada'\n"
                            "assert total != 43, "
                            "'sumaste tambien los -1: revisa donde pones el continue'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Parar en el primer negativo",
                description="Corta el recorrido en cuanto encuentras lo que buscas.",
                instructions=(
                    "Recorre `movimientos` sumando en `total`, pero para con `break` "
                    "en cuanto encuentres un numero negativo. Guarda en `posicion` el "
                    "indice de ese negativo. Si no hubiera ninguno, `posicion` se "
                    "queda en -1."
                ),
                starter_code=(
                    "movimientos = [10, 25, 8, -3, 40, 12]\n"
                    "total = 0\n"
                    "posicion = -1\n\n"
                    "# TODO: recorre con range(len(movimientos)) para tener el indice\n"
                ),
                hints=[
                    "range(len(movimientos)) te da 0, 1, 2, ... y con i accedes a "
                    "movimientos[i].",
                    "Comprueba si es negativo ANTES de sumarlo al total.",
                    "Guarda posicion = i y justo despues break.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "total suma solo hasta antes del negativo",
                        "code": "assert total == 43, f'total vale {total}, esperaba 43'",
                    },
                    {
                        "name": "posicion apunta al negativo",
                        "code": (
                            "assert posicion == 3, f'posicion vale {posicion}, esperaba 3'"
                        ),
                    },
                    {
                        "name": "el break corto de verdad",
                        "code": (
                            "assert total != 0, "
                            "'total sigue en 0: el bucle todavia no suma nada'\n"
                            "assert total != 92, "
                            "'seguiste sumando despues del negativo: falta el break'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Buscar el primer multiplo comun",
                description="Combina while con break para buscar sin saber cuantas vueltas son.",
                instructions=(
                    "Encuentra el primer numero mayor que 0 divisible a la vez por 6 "
                    "y por 8. Usa un `while True` y sal con `break` cuando lo "
                    "encuentres. Deja el numero en `encontrado` y en `intentos` "
                    "cuantos numeros probaste, contando el bueno."
                ),
                starter_code=(
                    "encontrado = 0\n"
                    "intentos = 0\n"
                    "n = 1\n\n"
                    "# TODO: while True, prueba n; si cumple guarda y break, si no sube n\n"
                ),
                hints=[
                    "Divisible por 6 y por 8 es: n % 6 == 0 and n % 8 == 0",
                    "Suma 1 a intentos al principio del cuerpo, en cada vuelta.",
                    "Si no cumple: n = n + 1 y el while vuelve a empezar.",
                    "Sin el break, un while True no termina nunca.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "encuentra el 24",
                        "code": "assert encontrado == 24, f'encontrado vale {encontrado}'",
                    },
                    {
                        "name": "cuenta los intentos",
                        "code": (
                            "assert intentos == 24, "
                            "f'intentos vale {intentos}: probaste del 1 al 24, son 24'"
                        ),
                    },
                    {
                        "name": "es divisible por los dos",
                        "code": (
                            "assert encontrado % 6 == 0 and encontrado % 8 == 0\n"
                            "assert encontrado > 0"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Resumen de temperaturas",
                description="Encadena for, continue y acumuladores en un solo recorrido.",
                instructions=(
                    "`temperaturas` trae mediciones y algunos -999, que son fallos "
                    "del sensor. En UN solo recorrido con `for`:\n\n"
                    "- salta los -999 con `continue`;\n"
                    "- junta las validas en la lista `validas`;\n"
                    "- deja en `maxima` la mayor y en `minima` la menor.\n\n"
                    "No uses `max()` ni `min()`: la gracia es llevar los "
                    "acumuladores a mano."
                ),
                starter_code=(
                    "temperaturas = [18, -999, 24, 31, -999, 12, 27]\n"
                    "validas = []\n"
                    "maxima = None\n"
                    "minima = None\n\n"
                    "# TODO: un solo for sobre temperaturas\n"
                ),
                hints=[
                    "Primero el if t == -999: continue; asi el resto del cuerpo solo "
                    "ve lecturas validas.",
                    "Arrancan en None porque todavia no sabes que valores hay: el "
                    "primero valido sera a la vez el maximo y el minimo.",
                    "Para el maximo: if maxima is None or t > maxima: maxima = t",
                    "El minimo es el mismo patron cambiando > por <.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "validas excluye los -999",
                        "code": (
                            "assert validas == [18, 24, 31, 12, 27], f'validas vale {validas}'"
                        ),
                    },
                    {
                        "name": "maxima y minima son correctas",
                        "code": (
                            "assert maxima == 31, f'maxima vale {maxima}'\n"
                            "assert minima == 12, f'minima vale {minima}'"
                        ),
                    },
                    {
                        "name": "maxima y minima son lecturas reales, no inventadas",
                        "code": (
                            "assert maxima in validas, 'maxima no es ninguna de las lecturas'\n"
                            "assert minima in validas, 'minima no es ninguna de las lecturas'"
                        ),
                    },
                    {
                        "name": "los -999 no contaminaron ningun acumulador",
                        "code": (
                            "assert minima != -999, 'el -999 se colo en minima'\n"
                            "assert len(validas) == 5, "
                            "f'validas tiene {len(validas)} elementos, esperaba 5'"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Funciones y Parametros",
        description=(
            "Definir funciones con def, devolver resultados con return, "
            "parametros, argumentos por defecto y alcance de las variables."
        ),
        content=(
            "## Por que las funciones\n"
            "En la leccion anterior escribiste bucles que resolvian UN caso\n"
            "concreto. Una **funcion** empaqueta esa logica bajo un nombre para\n"
            "poder usarla con datos distintos, tantas veces como quieras, sin\n"
            "copiar y pegar. Y si mañana cambia la regla, la cambias en un solo\n"
            "sitio en vez de en las quince copias que habias repartido.\n\n"
            "## def: definir y llamar\n"
            "Definir una funcion es darle nombre a un bloque de codigo. Llamarla\n"
            "es ejecutarlo:\n"
            "```python\n"
            "def saludar():              # def, nombre, parentesis y dos puntos\n"
            "    print('Hola')           # el cuerpo va indentado, como en un bucle\n\n"
            "saludar()                   # imprime Hola\n"
            "saludar()                   # imprime Hola otra vez\n"
            "```\n"
            "Definir **no ejecuta nada**: Python solo toma nota de que la funcion\n"
            "existe. El cuerpo corre cuando la llamas, y una sola definicion vale\n"
            "para infinitas llamadas.\n\n"
            "Justo debajo del `def` puedes poner un **docstring**, un texto entre\n"
            "triples comillas que explica que hace la funcion:\n"
            "```python\n"
            "def saludar():\n"
            "    '''Imprime un saludo por pantalla.'''   # docstring, para quien lea\n"
            "    print('Hola')\n\n"
            "print(saludar.__doc__)      # Imprime un saludo por pantalla.\n"
            "```\n\n"
            "## return: devolver no es imprimir\n"
            "`print` muestra algo en pantalla. `return` **entrega un valor** a\n"
            "quien llamo la funcion, para poder guardarlo y seguir operando:\n"
            "```python\n"
            "def doble_print(n):\n"
            "    print(n * 2)            # muestra el resultado y no devuelve nada\n\n"
            "def doble_return(n):\n"
            "    return n * 2            # ENTREGA el resultado\n\n"
            "x = doble_print(5)          # imprime 10\n"
            "print(x)                    # None  <- la funcion no devolvio nada\n"
            "y = doble_return(5)         # no imprime nada\n"
            "print(y + 1)                # 11    <- y vale 10 y se puede operar\n"
            "```\n"
            "Una funcion sin `return` devuelve `None`. Confundir `print` con\n"
            "`return` es **el** error numero uno al empezar con funciones.\n\n"
            "`return` ademas **termina** la funcion: lo que venga despues no se\n"
            "ejecuta.\n"
            "```python\n"
            "def primer_positivo(numeros):\n"
            "    for n in numeros:\n"
            "        if n > 0:\n"
            "            return n        # sale en cuanto encuentra uno\n"
            "    return 0                # solo llega aqui si no hubo ninguno\n\n"
            "print(primer_positivo([-3, -1, 7, 9]))   # 7\n"
            "print(primer_positivo([-3, -1]))         # 0\n"
            "```\n\n"
            "## Parametros: la entrada de la funcion\n"
            "Los **parametros** son los nombres que la funcion usa para sus datos\n"
            "de entrada. Los **argumentos** son los valores concretos con los que\n"
            "la llamas:\n"
            "```python\n"
            "def area_rectangulo(base, altura):   # base y altura son PARAMETROS\n"
            "    return base * altura\n\n"
            "print(area_rectangulo(3, 4))         # 12  <- 3 y 4 son ARGUMENTOS\n"
            "print(area_rectangulo(10, 2))        # 20  <- otros argumentos\n"
            "```\n"
            "El orden importa: el primer valor va al primer parametro.\n\n"
            "## Argumentos por defecto y por nombre\n"
            "Un parametro puede traer un valor por defecto, que se usa cuando no\n"
            "pasas ese argumento:\n"
            "```python\n"
            "def saludar(nombre, prefijo='Hola'):       # prefijo tiene defecto\n"
            "    return f'{prefijo}, {nombre}!'         # f-string: mete valores\n\n"
            "print(saludar('Ana'))                      # Hola, Ana!\n"
            "print(saludar('Ana', 'Buenas'))            # Buenas, Ana!\n"
            "print(saludar(nombre='Ana', prefijo='Ey')) # Ey, Ana!  <- por nombre\n"
            "```\n"
            "Los parametros con valor por defecto van **siempre al final** de la\n"
            "lista. Si no, Python no sabria a cual asignar cada argumento.\n\n"
            "## Variables locales: lo de dentro se queda dentro\n"
            "Las variables que creas dentro de una funcion existen solo mientras\n"
            "la funcion se ejecuta:\n"
            "```python\n"
            "# FALLA A PROPOSITO en la ultima linea\n"
            "def calcular():\n"
            "    resultado = 42          # variable LOCAL de calcular\n"
            "    return resultado\n\n"
            "print(calcular())           # 42\n"
            "print(resultado)            # NameError: aqui fuera no existe\n"
            "```\n"
            "Por eso una funcion se comunica con el exterior por dos sitios: los\n"
            "parametros por donde entra la informacion, y el `return` por donde\n"
            "sale.\n\n"
            "## Errores comunes\n"
            "- Usar `print` donde hacia falta `return`. La funcion muestra el\n"
            "  numero pero devuelve `None`, y al operar con el resultado salta un\n"
            "  `TypeError`. Si necesitas el valor para algo, devuelvelo.\n"
            "- Olvidar los parentesis al llamar: `saludar` es la funcion como\n"
            "  objeto; `saludar()` la ejecuta. Sin parentesis no pasa nada.\n"
            "- Poner codigo despues de un `return` esperando que corra. En cuanto\n"
            "  se ejecuta el `return`, la funcion termina ahi mismo.\n"
            "- Escribir un parametro con defecto antes de uno normal, como\n"
            "  `def f(a=1, b)`: es un SyntaxError. Los que tienen defecto al final.\n"
            "- Intentar leer fuera una variable creada dentro: `NameError`. Si la\n"
            "  necesitas fuera, sacala con `return`.\n\n"
            "## Resumen\n"
            "- `def nombre(parametros):` define la funcion; `nombre(argumentos)`\n"
            "  la ejecuta.\n"
            "- `return` entrega un valor y termina la funcion; sin `return` una\n"
            "  funcion devuelve `None`.\n"
            "- `print` muestra por pantalla, `return` devuelve: no son lo mismo.\n"
            "- Los parametros con valor por defecto van al final y permiten\n"
            "  llamadas mas cortas.\n"
            "- Lo que se crea dentro de la funcion no existe fuera de ella.\n"
        ),
        difficulty="beginner",
        category="funciones",
        order=5,
        estimated_duration=50,
        prerequisites_titles=["Bucles for y while"],
        exercises=[
            ExerciseTemplate(
                title="Area de rectangulo",
                description="Tu primera funcion que devuelve un valor.",
                instructions=(
                    "Define `area_rectangulo(base, altura)` que **devuelva** el "
                    "area (base por altura). Cuidado: tiene que devolverla con "
                    "`return`, no imprimirla."
                ),
                starter_code=(
                    "def area_rectangulo(base, altura):\n"
                    "    # TODO: devuelve el area\n"
                    "    ...\n"
                ),
                hints=[
                    "El area de un rectangulo es base * altura.",
                    "Usa return, no print: los tests necesitan el valor de vuelta.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "calcula el area de varios rectangulos",
                        "code": (
                            "assert area_rectangulo(3, 4) == 12\n"
                            "assert area_rectangulo(10, 2) == 20\n"
                            "assert area_rectangulo(1, 1) == 1"
                        ),
                    },
                    {
                        "name": "devuelve el valor en vez de imprimirlo",
                        "code": (
                            "r = area_rectangulo(5, 5)\n"
                            "assert r is not None, "
                            "'la funcion devuelve None: usaste print en vez de return'\n"
                            "assert r == 25"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Saludo configurable",
                description="Un parametro con valor por defecto.",
                instructions=(
                    "Define `saludar(nombre, prefijo='Hola')` que devuelva el texto "
                    "formado por el prefijo, una coma, un espacio, el nombre y un "
                    "signo de exclamacion. Por ejemplo `saludar('Ana')` devuelve "
                    "`Hola, Ana!` y `saludar('Ana', 'Buenas')` devuelve `Buenas, Ana!`."
                ),
                starter_code=(
                    "def saludar(nombre, prefijo='Hola'):\n"
                    "    # TODO: devuelve el saludo completo\n"
                    "    ...\n"
                ),
                hints=[
                    "Con f-string: f'{prefijo}, {nombre}!'",
                    "Fijate en la coma, el espacio y el signo de exclamacion final.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "usa el prefijo por defecto",
                        "code": (
                            "obtenido = saludar('Ana')\n"
                            "assert obtenido == 'Hola, Ana!', f'devolvio {obtenido!r}'"
                        ),
                    },
                    {
                        "name": "acepta un prefijo distinto",
                        "code": (
                            "assert saludar('Ana', 'Buenas') == 'Buenas, Ana!'\n"
                            "assert saludar('Beto', 'Ey') == 'Ey, Beto!'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Precio con descuento",
                description="Un valor por defecto que hace opcional el segundo argumento.",
                instructions=(
                    "Define `precio_final(precio, descuento=0)` que devuelva el "
                    "precio tras aplicarle ese porcentaje de descuento, redondeado "
                    "a dos decimales con `round(x, 2)`. Sin descuento devuelve el "
                    "precio tal cual: `precio_final(100)` es 100.0, y "
                    "`precio_final(100, 20)` es 80.0."
                ),
                starter_code=(
                    "def precio_final(precio, descuento=0):\n"
                    "    # TODO: aplica el descuento y redondea a 2 decimales\n"
                    "    ...\n"
                ),
                hints=[
                    "Un 20% de descuento deja el 80%: precio * (100 - descuento) / 100",
                    "Envuelve el resultado en round(..., 2).",
                    "Con descuento=0 la formula ya devuelve el precio original: no "
                    "necesitas un if.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "sin descuento devuelve el precio",
                        "code": "assert precio_final(100) == 100.0",
                    },
                    {
                        "name": "aplica el porcentaje",
                        "code": (
                            "assert precio_final(100, 20) == 80.0\n"
                            "assert precio_final(50, 50) == 25.0"
                        ),
                    },
                    {
                        "name": "redondea a dos decimales",
                        "code": (
                            "obtenido = precio_final(59.99, 10)\n"
                            "assert obtenido == 53.99, f'devolvio {obtenido}'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Contar palabras",
                description="Una funcion que resuelve tambien el caso borde.",
                instructions=(
                    "Define `contar_palabras(texto)` que devuelva cuantas palabras "
                    "tiene el texto. Las palabras van separadas por espacios y los "
                    "espacios de sobra no cuentan. Un texto vacio tiene 0 palabras."
                ),
                starter_code=(
                    "def contar_palabras(texto):\n"
                    "    # TODO: devuelve el numero de palabras\n"
                    "    ...\n"
                ),
                hints=[
                    "texto.split() parte por espacios y descarta los sobrantes.",
                    "len() de esa lista es el numero de palabras.",
                    "Con el texto vacio, split() devuelve una lista vacia y su len "
                    "ya es 0: no hace falta un caso especial.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "cuenta palabras normales",
                        "code": (
                            "assert contar_palabras('hola mundo') == 2\n"
                            "assert contar_palabras('una sola frase de cinco') == 5"
                        ),
                    },
                    {
                        "name": "los espacios de sobra no cuentan",
                        "code": (
                            "obtenido = contar_palabras('   espacios    raros   ')\n"
                            "assert obtenido == 2, f'devolvio {obtenido}'"
                        ),
                    },
                    {
                        "name": "el texto vacio tiene 0 palabras",
                        "code": (
                            "vacio = str()\n"
                            "assert contar_palabras(vacio) == 0\n"
                            "assert contar_palabras('    ') == 0"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Resumen de notas",
                description="Recorre una lista dentro de una funcion y devuelve varios datos.",
                instructions=(
                    "Define `resumen(notas)` que recorra la lista y devuelva una "
                    "tupla con tres valores en este orden: la nota **minima**, la "
                    "**maxima** y cuantas notas estan **aprobadas** (5 o mas).\n\n"
                    "Si la lista viene vacia, devuelve `(None, None, 0)`.\n\n"
                    "No uses `max()`, `min()` ni `sum()`: llevalos a mano como en "
                    "la leccion de bucles."
                ),
                starter_code=(
                    "def resumen(notas):\n"
                    "    # TODO: recorre notas y devuelve (minima, maxima, aprobadas)\n"
                    "    ...\n"
                ),
                hints=[
                    "Empieza con minima = None, maxima = None y aprobadas = 0.",
                    "Si la lista esta vacia el bucle no da ni una vuelta, asi que "
                    "esos valores iniciales ya son la respuesta correcta.",
                    "Para el maximo: if maxima is None or n > maxima: maxima = n",
                    "Devolver varios valores es return minima, maxima, aprobadas",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "devuelve minima, maxima y aprobadas",
                        "code": (
                            "obtenido = resumen([3, 7, 5, 9, 2])\n"
                            "assert obtenido == (2, 9, 3), f'devolvio {obtenido}'"
                        ),
                    },
                    {
                        "name": "cuenta como aprobado el 5 justo",
                        "code": (
                            "assert resumen([5])[2] == 1, 'un 5 esta aprobado'\n"
                            "assert resumen([4, 4, 4])[2] == 0"
                        ),
                    },
                    {
                        "name": "la lista vacia no rompe la funcion",
                        "code": (
                            "obtenido = resumen([])\n"
                            "assert obtenido == (None, None, 0), f'devolvio {obtenido}'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Normalizar una lista de nombres",
                description="Encadena parametro por defecto, bucle, continue y return.",
                instructions=(
                    "Define `normalizar(nombres, mayusculas=False)` que devuelva "
                    "una lista NUEVA donde cada nombre:\n\n"
                    "- pierde los espacios de los lados (`.strip()`);\n"
                    "- se salta con `continue` si al quitarle los espacios no queda "
                    "nada;\n"
                    "- queda con la primera letra en mayuscula (`.title()`), o "
                    "entero en mayusculas (`.upper()`) si `mayusculas` es True.\n\n"
                    "La lista original no se toca."
                ),
                starter_code=(
                    "def normalizar(nombres, mayusculas=False):\n"
                    "    # TODO: construye y devuelve una lista nueva\n"
                    "    ...\n"
                ),
                hints=[
                    "Crea la lista de salida dentro de la funcion, antes del bucle.",
                    "limpio = nombre.strip(); si len(limpio) == 0, continue.",
                    "El if de mayusculas decide entre limpio.upper() y limpio.title().",
                    "Devuelve la lista nueva al final, fuera del bucle.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "limpia espacios y descarta los vacios",
                        "code": (
                            "obtenido = normalizar(['  ana ', '   ', 'BETO'])\n"
                            "assert obtenido == ['Ana', 'Beto'], f'devolvio {obtenido}'"
                        ),
                    },
                    {
                        "name": "el parametro por defecto pone solo la inicial",
                        "code": (
                            "assert normalizar(['carla']) == ['Carla']\n"
                            "assert normalizar(['DIEGO']) == ['Diego']"
                        ),
                    },
                    {
                        "name": "con mayusculas=True devuelve todo en mayusculas",
                        "code": (
                            "obtenido = normalizar(['  ana ', 'BETO'], mayusculas=True)\n"
                            "assert obtenido == ['ANA', 'BETO'], f'devolvio {obtenido}'"
                        ),
                    },
                    {
                        "name": "no modifica la lista original",
                        "code": (
                            "original = ['  ana ', '   ', 'BETO']\n"
                            "nueva = normalizar(original)\n"
                            "assert isinstance(nueva, list) and nueva is not original, "
                            "'normalizar tiene que devolver una lista nueva'\n"
                            "assert original == ['  ana ', '   ', 'BETO'], "
                            "'modificaste la lista que te pasaron; construye una nueva'"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Listas, Tuplas y Diccionarios",
        description=(
            "Las tres estructuras que guardan muchos datos a la vez: listas para "
            "lo que cambia, tuplas para lo que no, diccionarios para buscar por nombre."
        ),
        content=(
            "## Por que estas tres estructuras\n"
            "Una variable guarda un dato. Treinta alumnos no caben en treinta\n"
            "variables: caben en **una** lista. Y una vez que tienes muchos datos\n"
            "juntos, la pregunta deja de ser como guardarlos y pasa a ser como\n"
            "llegar a uno concreto. Esta leccion son las tres respuestas de\n"
            "Python, y elegir bien entre ellas te ahorra la mitad del codigo.\n\n"
            "## Listas: la coleccion que cambia\n"
            "Ya las viste en los bucles. Una lista guarda cosas en orden y se\n"
            "puede modificar despues de creada:\n"
            "```python\n"
            "notas = [7, 9, 4]        # los corchetes son la lista\n"
            "print(len(notas))        # 3   -> cuantos elementos tiene\n"
            "notas.append(10)         # agrega al final\n"
            "print(notas)             # [7, 9, 4, 10]\n"
            "notas[0] = 8             # se puede cambiar un elemento\n"
            "print(notas)             # [8, 9, 4, 10]\n"
            "```\n"
            "Los elementos no tienen que ser numeros, ni siquiera del mismo tipo,\n"
            "pero una lista donde cada posicion significa una cosa distinta suele\n"
            "ser una senal de que ahi hacia falta un diccionario.\n\n"
            "## Indexado y slicing: llegar a un trozo\n"
            "Cada elemento tiene una posicion, y **se empieza a contar en 0**:\n"
            "```python\n"
            "dias = ['lun', 'mar', 'mie', 'jue', 'vie']\n"
            "print(dias[0])           # lun   -> el primero es el 0, no el 1\n"
            "print(dias[2])           # mie\n"
            "print(dias[-1])          # vie   -> negativo cuenta desde el final\n"
            "print(dias[1:3])         # ['mar', 'mie']  -> desde 1 hasta ANTES de 3\n"
            "print(dias[:2])          # ['lun', 'mar']  -> sin inicio: desde el principio\n"
            "print(dias[3:])          # ['jue', 'vie']  -> sin fin: hasta el final\n"
            "```\n"
            "El corte `[a:b]` incluye `a` y **excluye** `b`, igual que `range`. Un\n"
            "corte siempre devuelve una lista nueva: `dias[:2]` no toca `dias`.\n\n"
            "## Metodos de lista que vas a usar\n"
            "```python\n"
            "cola = ['ana', 'luis']\n"
            "cola.append('eva')       # agrega al final -> ['ana', 'luis', 'eva']\n"
            "cola.remove('luis')      # quita por VALOR -> ['ana', 'eva']\n"
            "print(cola.pop(0))       # ana   -> saca por POSICION y lo devuelve\n"
            "print(cola)              # ['eva']\n"
            "print('eva' in cola)     # True  -> `in` pregunta si esta\n\n"
            "precios = [30, 10, 20]\n"
            "print(sorted(precios))               # [10, 20, 30]  -> lista NUEVA ordenada\n"
            "print(sorted(precios, reverse=True)) # [30, 20, 10]  -> de mayor a menor\n"
            "print(precios)                       # [30, 10, 20]  -> el original intacto\n"
            "```\n"
            "`sorted(...)` devuelve una lista nueva; `precios.sort()` ordena la\n"
            "original y devuelve `None`. Confundirlas es el clasico\n"
            "`precios = precios.sort()` que deja `precios` valiendo `None`.\n\n"
            "## Tuplas: el par que no se toca\n"
            "Una tupla es como una lista, pero **inmutable**: una vez creada no se\n"
            "le cambia nada. Se escribe con parentesis:\n"
            "```python\n"
            "punto = (3, 8)           # una tupla de dos elementos\n"
            "print(punto[0])          # 3    -> se indexa igual que una lista\n"
            "print(len(punto))        # 2\n\n"
            "x, y = punto             # desempaquetado: cada valor a su variable\n"
            "print(x, y)              # 3 8\n\n"
            "ventas = [('pan', 2), ('leche', 3)]   # lista de pares\n"
            "for nombre, precio in ventas:         # desempaqueta en cada vuelta\n"
            "    print(nombre, precio)             # pan 2, luego leche 3\n"
            "```\n"
            "La usas cuando el numero de elementos es fijo y cada posicion\n"
            "significa siempre lo mismo: un par `(nombre, precio)`, una coordenada\n"
            "`(x, y)`. Que no se pueda modificar es la ventaja, no el defecto:\n"
            "nadie te va a meter un tercer elemento a medio programa.\n\n"
            "## Diccionarios: buscar por nombre\n"
            "En una lista buscas por posicion; en un diccionario, por **clave**:\n"
            "```python\n"
            "edades = {'ana': 30, 'luis': 25}   # llaves, y clave: valor\n"
            "print(edades['ana'])               # 30\n"
            "edades['eva'] = 41                 # agregar es asignar una clave nueva\n"
            "edades['ana'] = 31                 # y con una que ya existe, la pisa\n"
            "print(edades)                      # {'ana': 31, 'luis': 25, 'eva': 41}\n"
            "print(len(edades))                 # 3\n"
            "print('luis' in edades)            # True  -> `in` mira las CLAVES\n"
            "```\n"
            "Pedir una clave que no existe con `edades['nadie']` revienta con\n"
            "`KeyError`. Casi siempre quieres `.get`, que devuelve un valor por\n"
            "defecto en vez de romper:\n"
            "```python\n"
            "edades = {'ana': 31, 'luis': 25}   # el mismo diccionario de arriba\n"
            "print(edades.get('nadie'))         # None  -> sin valor por defecto\n"
            "print(edades.get('nadie', 0))      # 0     -> el que tu elijas\n\n"
            "conteo = {}                        # el patron de contar\n"
            "for letra in 'banana':\n"
            "    conteo[letra] = conteo.get(letra, 0) + 1   # 0 la primera vez\n"
            "print(conteo)                      # {'b': 1, 'a': 3, 'n': 2}\n"
            "```\n"
            "Ese `conteo.get(letra, 0) + 1` es de los patrones que mas vas a\n"
            "escribir en tu vida: contar cuantas veces aparece cada cosa.\n\n"
            "## Recorrer un diccionario\n"
            "El `for` a secas te da las claves; `.items()` te da los pares:\n"
            "```python\n"
            "edades = {'ana': 31, 'luis': 25}\n"
            "for clave in edades:                 # el for da las CLAVES\n"
            "    print(clave)                     # ana, luego luis\n\n"
            "for nombre, edad in edades.items():  # .items() da pares (clave, valor)\n"
            "    print(nombre, edad)              # ana 31, luego luis 25\n\n"
            "print(list(edades.keys()))           # ['ana', 'luis']\n"
            "print(list(edades.values()))         # [31, 25]\n"
            "print(sum(edades.values()))          # 56  -> los valores se suman\n"
            "```\n"
            "`.items()` devuelve tuplas, por eso funciona el desempaquetado\n"
            "`for nombre, edad in ...`: es el mismo de la seccion anterior.\n\n"
            "## Cual elijo\n"
            "- **Lista**: muchos datos del mismo tipo, en orden, y la cosa cambia.\n"
            "  Recorrer, agregar, ordenar.\n"
            "- **Tupla**: un grupo fijo de datos donde cada posicion significa\n"
            "  algo. Un registro que viaja junto y no se toca.\n"
            "- **Diccionario**: cuando lo que tienes para buscar es un nombre y no\n"
            "  una posicion. Contar, agrupar, configurar.\n\n"
            "## Errores comunes\n"
            "- Contar desde 1. El primer elemento es `lista[0]`, y el ultimo de\n"
            "  una lista de 5 es `lista[4]`: `lista[5]` lanza `IndexError`.\n"
            "- Esperar que `[a:b]` incluya `b`. `dias[1:3]` devuelve dos\n"
            "  elementos, no tres. Igual que `range`, el final se excluye.\n"
            "- `precios = precios.sort()`. `.sort()` ordena la lista y devuelve\n"
            "  `None`, asi que te quedas sin lista. O usas `precios.sort()` sola,\n"
            "  o `precios = sorted(precios)`.\n"
            "- Leer una clave que puede no estar con `d['clave']` y comerte un\n"
            "  `KeyError`. Si no estas seguro de que exista, `d.get('clave', 0)`.\n"
            "- Intentar modificar una tupla (`punto[0] = 5`): `TypeError`. Si el\n"
            "  dato tiene que cambiar, ahi hacia falta una lista.\n"
            "- Usar una lista de listas para lo que es un diccionario. Si te\n"
            "  descubres recorriendo la lista entera para encontrar 'ana', esa\n"
            "  busqueda es la que hace un diccionario en un paso.\n\n"
            "## Resumen\n"
            "- Lista `[...]`: ordenada y mutable. `len`, `append`, `remove`,\n"
            "  `pop`, `in`, `sorted`.\n"
            "- Indexado desde 0, negativo desde el final, y `[a:b]` corta\n"
            "  incluyendo `a` y excluyendo `b`.\n"
            "- Tupla `(...)`: inmutable, de longitud fija, y se desempaqueta con\n"
            "  `x, y = punto` o en el propio `for`.\n"
            "- Diccionario `{clave: valor}`: acceso por nombre. `d[c]` revienta si\n"
            "  no esta, `d.get(c, 0)` no.\n"
            "- `conteo[x] = conteo.get(x, 0) + 1` es el patron para contar.\n"
            "- Se recorre con `for clave in d` o con `for k, v in d.items()`.\n"
        ),
        difficulty="intermediate",
        category="estructuras-datos",
        order=6,
        estimated_duration=50,
        prerequisites_titles=["Funciones y Parametros"],
        exercises=[
            ExerciseTemplate(
                title="Promedio de notas",
                description="Recorre una lista y saca su promedio.",
                instructions=(
                    "Calcula el promedio de la lista `notas` redondeado a 2 "
                    "decimales e imprimelo. Tiene que salir `4.38`.\n\n"
                    "Puedes sumar con un bucle acumulador o con `sum(notas)`, y "
                    "`len(notas)` te da cuantas son."
                ),
                starter_code="notas = [4.5, 3.8, 5.0, 4.2]\n# TODO\n",
                hints=[
                    "El promedio es la suma dividida entre la cantidad: sum(notas) / len(notas).",
                    "round(valor, 2) redondea a dos decimales.",
                    "No olvides el print del resultado.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "imprime el promedio (~4.38)",
                        "code": "assert '4.3' in _salida, ('esperaba ~4.38', _salida)",
                    },
                    {
                        "name": "esta redondeado a 2 decimales",
                        "code": (
                            "assert '4.38' in _salida, "
                            "('esperaba 4.38 redondeado, y salio', _salida)"
                        ),
                    },
                    {
                        "name": "no toca la lista original",
                        "code": (
                            "assert _salida.strip(), 'no imprimiste nada'\n"
                            "assert notas == [4.5, 3.8, 5.0, 4.2], "
                            "f'la lista quedo como {notas}'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Agenda minima",
                description="Tu primer diccionario: agregar y leer.",
                instructions=(
                    "Agrega a `agenda` el contacto `'ana'` con el numero `'123'` e "
                    "imprime su numero.\n\n"
                    "El numero va como texto, con comillas: `'123'`, no `123`."
                ),
                starter_code="agenda = {}\n# TODO\n",
                hints=[
                    "Agregar una clave es asignarla: agenda['ana'] = '123'.",
                    "Para leerla, agenda['ana'] entre el print.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "agrega 'ana':'123' y lo imprime",
                        "code": (
                            "assert agenda.get('ana') == '123', ('agenda debe tener ana:123', agenda)\n"
                            "assert '123' in _salida, _salida"
                        ),
                    },
                    {
                        "name": "el numero es texto, no un entero",
                        "code": (
                            "assert isinstance(agenda['ana'], str), "
                            "f\"el numero quedo como {type(agenda['ana']).__name__}, y se pedia texto\""
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Los tres mejores",
                description="Ordenar y cortar: sorted mas slicing.",
                instructions=(
                    "Define `top_tres(numeros)` que devuelva una lista con los tres "
                    "valores mas grandes, **de mayor a menor**.\n\n"
                    "- Con `[5, 9, 1, 7, 3]` devuelve `[9, 7, 5]`.\n"
                    "- Si hay menos de tres, devuelve los que haya (tambien "
                    "ordenados de mayor a menor).\n"
                    "- La lista que te pasan no se puede modificar."
                ),
                starter_code=(
                    "def top_tres(numeros):\n"
                    "    # TODO: ordena de mayor a menor y quedate con los tres primeros\n"
                    "    ...\n"
                ),
                hints=[
                    "sorted(numeros, reverse=True) devuelve una lista NUEVA de mayor a menor.",
                    "El corte [:3] se queda con los tres primeros.",
                    "Si la lista tiene menos de tres, [:3] devuelve lo que haya: no hace falta un if.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "devuelve los tres mayores de mayor a menor",
                        "code": (
                            "obtenido = top_tres([5, 9, 1, 7, 3])\n"
                            "assert obtenido == [9, 7, 5], f'devolvio {obtenido!r}'"
                        ),
                    },
                    {
                        "name": "con menos de tres devuelve los que hay",
                        "code": (
                            "assert top_tres([4, 8]) == [8, 4], top_tres([4, 8])\n"
                            "assert top_tres([]) == [], top_tres([])"
                        ),
                    },
                    {
                        "name": "no modifica la lista que recibe",
                        "code": (
                            "datos = [5, 9, 1, 7, 3]\n"
                            "assert top_tres(datos) == [9, 7, 5]\n"
                            "assert datos == [5, 9, 1, 7, 3], "
                            "f'usaste .sort() sobre la original: quedo {datos}'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Contar palabras",
                description="El patron de conteo con get.",
                instructions=(
                    "Define `contar_palabras(texto)` que devuelva un diccionario "
                    "con cuantas veces aparece cada palabra.\n\n"
                    "- Con `'sol luna sol'` devuelve `{'sol': 2, 'luna': 1}`.\n"
                    "- Con el texto vacio devuelve `{}`.\n"
                    "- `texto.split()` parte por espacios y te da la lista de "
                    "palabras."
                ),
                starter_code=(
                    "def contar_palabras(texto):\n"
                    "    # TODO: recorre texto.split() y ve contando en un diccionario\n"
                    "    ...\n"
                ),
                hints=[
                    "Arranca con un diccionario vacio: conteo = {}.",
                    "Recorre con for palabra in texto.split():",
                    "Dentro: conteo[palabra] = conteo.get(palabra, 0) + 1.",
                    "Devuelve el diccionario al final, fuera del bucle.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "cuenta las repeticiones",
                        "code": (
                            "obtenido = contar_palabras('sol luna sol')\n"
                            "assert obtenido == {'sol': 2, 'luna': 1}, f'devolvio {obtenido!r}'"
                        ),
                    },
                    {
                        "name": "el texto vacio da un diccionario vacio",
                        "code": (
                            "obtenido = contar_palabras('')\n"
                            "assert obtenido == {}, f'devolvio {obtenido!r}'"
                        ),
                    },
                    {
                        "name": "aguanta un texto mas largo",
                        "code": (
                            "obtenido = contar_palabras('a b a c b a')\n"
                            "assert obtenido == {'a': 3, 'b': 2, 'c': 1}, f'devolvio {obtenido!r}'"
                        ),
                    },
                    {
                        "name": "distingue mayusculas de minusculas",
                        "code": (
                            "obtenido = contar_palabras('Sol sol')\n"
                            "assert obtenido == {'Sol': 1, 'sol': 1}, "
                            "f'devolvio {obtenido!r}: no hay que normalizar nada'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="El mejor vendedor",
                description="Desempaqueta tuplas y agrupa en un diccionario.",
                instructions=(
                    "`ventas` es una lista de pares `(nombre, monto)`, y un mismo "
                    "vendedor puede aparecer varias veces.\n\n"
                    "Define `mejor_vendedor(ventas)` que devuelva la tupla "
                    "`(nombre, total)` de quien mas vendio sumando todas sus "
                    "ventas. Con la lista vacia devuelve `None`.\n\n"
                    "Puedes suponer que no hay empate en el primer puesto."
                ),
                starter_code=(
                    "def mejor_vendedor(ventas):\n"
                    "    # TODO: suma por nombre en un diccionario y quedate con el mayor\n"
                    "    ...\n"
                ),
                hints=[
                    "Recorre con for nombre, monto in ventas: y desempaquetas cada par.",
                    "Acumula: totales[nombre] = totales.get(nombre, 0) + monto.",
                    "Para elegir el mayor puedes recorrer totales.items() guardando el "
                    "mejor visto hasta ahora.",
                    "El primer if es el de la lista vacia: si no hay ventas, return None.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "suma las ventas de cada uno y devuelve el mayor",
                        "code": (
                            "ventas = [('ana', 100), ('luis', 80), ('ana', 50)]\n"
                            "obtenido = mejor_vendedor(ventas)\n"
                            "assert obtenido == ('ana', 150), f'devolvio {obtenido!r}'"
                        ),
                    },
                    {
                        "name": "gana el total, no la venta mas grande",
                        "code": (
                            "ventas = [('ana', 40), ('ana', 40), ('ana', 40), ('luis', 100)]\n"
                            "obtenido = mejor_vendedor(ventas)\n"
                            "assert obtenido == ('ana', 120), "
                            "f'devolvio {obtenido!r}: hay que sumar por vendedor'"
                        ),
                    },
                    {
                        "name": "con la lista vacia devuelve None",
                        "code": (
                            "assert mejor_vendedor([('eva', 10)]) == ('eva', 10)\n"
                            "obtenido = mejor_vendedor([])\n"
                            "assert obtenido is None, f'devolvio {obtenido!r}'"
                        ),
                    },
                    {
                        "name": "devuelve una tupla de dos elementos",
                        "code": (
                            "obtenido = mejor_vendedor([('eva', 10)])\n"
                            "assert isinstance(obtenido, tuple) and len(obtenido) == 2, "
                            "f'devolvio {obtenido!r} y se pedia (nombre, total)'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Boletin de la clase",
                description="El pipeline: lista de tuplas, diccionario, orden y corte.",
                instructions=(
                    "`registros` es una lista de pares `(alumno, nota)`, uno por "
                    "alumno. Define `boletin(registros)` que devuelva un "
                    "diccionario con estas tres claves:\n\n"
                    "- `'aprobados'`: lista de los nombres con nota mayor o igual a "
                    "5, **ordenada alfabeticamente**.\n"
                    "- `'promedio'`: promedio de todas las notas redondeado a 1 "
                    "decimal con `round(x, 1)`. Con la lista vacia, `0`.\n"
                    "- `'podio'`: lista de los **dos** mejores nombres, de mayor a "
                    "menor nota. Si hay menos de dos alumnos, los que haya.\n\n"
                    "Con `[('ana', 9), ('luis', 4), ('eva', 7)]` sale "
                    "`{'aprobados': ['ana', 'eva'], 'promedio': 6.7, 'podio': "
                    "['ana', 'eva']}`."
                ),
                starter_code=(
                    "def boletin(registros):\n"
                    "    # TODO: aprobados, promedio y podio, en un diccionario\n"
                    "    ...\n"
                ),
                hints=[
                    "Para aprobados: recorre con for nombre, nota in registros: y "
                    "junta los que pasan en una lista; sorted(lista) la ordena alfabeticamente.",
                    "Para el promedio necesitas la lista de notas: recorre otra vez o "
                    "juntala en el mismo bucle. Cuidado con dividir entre cero si no hay nadie.",
                    "Para el podio, sorted(registros, reverse=True) no sirve: ordena por "
                    "nombre porque el nombre va primero en la tupla. Junta pares (nota, nombre) "
                    "y ordena esos.",
                    "Del podio ordenado te quedas con [:2] y sacas solo los nombres.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "el ejemplo del enunciado",
                        "code": (
                            "obtenido = boletin([('ana', 9), ('luis', 4), ('eva', 7)])\n"
                            "esperado = {'aprobados': ['ana', 'eva'], 'promedio': 6.7, "
                            "'podio': ['ana', 'eva']}\n"
                            "assert obtenido == esperado, f'devolvio {obtenido!r}'"
                        ),
                    },
                    {
                        "name": "los aprobados van ordenados alfabeticamente",
                        "code": (
                            "obtenido = boletin([('zoe', 8), ('ana', 6), ('beto', 5)])\n"
                            "assert obtenido['aprobados'] == ['ana', 'beto', 'zoe'], "
                            "f\"aprobados devolvio {obtenido['aprobados']!r}\""
                        ),
                    },
                    {
                        "name": "el podio va por nota, de mayor a menor",
                        "code": (
                            "obtenido = boletin([('ana', 3), ('luis', 10), ('eva', 6)])\n"
                            "assert obtenido['podio'] == ['luis', 'eva'], "
                            "f\"podio devolvio {obtenido['podio']!r}\"\n"
                            "assert obtenido['aprobados'] == ['eva', 'luis'], "
                            "'un suspenso se colo en aprobados'"
                        ),
                    },
                    {
                        "name": "el promedio cuenta a todos y se redondea a 1 decimal",
                        "code": (
                            "obtenido = boletin([('ana', 10), ('luis', 1)])\n"
                            "assert obtenido['promedio'] == 5.5, "
                            "f\"promedio devolvio {obtenido['promedio']!r}\"\n"
                            "otro = boletin([('a', 5), ('b', 6), ('c', 8)])\n"
                            "assert otro['promedio'] == 6.3, "
                            "f\"promedio devolvio {otro['promedio']!r}\""
                        ),
                    },
                    {
                        "name": "con la lista vacia no revienta",
                        "code": (
                            "obtenido = boletin([])\n"
                            "assert obtenido == {'aprobados': [], 'promedio': 0, 'podio': []}, "
                            "f'devolvio {obtenido!r}'"
                        ),
                    },
                    {
                        "name": "con un solo alumno el podio tiene uno",
                        "code": (
                            "obtenido = boletin([('ana', 7)])\n"
                            "assert obtenido['podio'] == ['ana'], "
                            "f\"podio devolvio {obtenido['podio']!r}\""
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Comprensiones y Manejo de Errores",
        description=(
            "Comprensiones de lista para construir colecciones en una linea, y "
            "try/except, raise y with para que el programa aguante los datos malos."
        ),
        content=(
            "## Por que estas dos herramientas\n"
            "Esta leccion trae dos cosas que vas a usar a diario y que no se\n"
            "parecen en nada. Las **comprensiones** te dejan escribir en una\n"
            "linea el bucle que construye una lista. El **manejo de errores** es\n"
            "lo que separa un script que se cae con el primer dato raro de un\n"
            "programa que sigue funcionando y te dice que paso.\n\n"
            "## Comprensiones de lista: un bucle en una linea\n"
            "Ya sabes construir listas con un bucle y un acumulador. Una\n"
            "comprension hace lo mismo en una linea:\n"
            "```python\n"
            "dobles = []                     # la forma que ya conoces\n"
            "for n in [1, 2, 3]:            # el for da los elementos, uno a uno\n"
            "    dobles.append(n * 2)       # y tu decides en que se convierte\n"
            "print(dobles)                   # [2, 4, 6]\n\n"
            "dobles = [n * 2 for n in [1, 2, 3]]   # exactamente lo mismo\n"
            "print(dobles)                   # [2, 4, 6]\n"
            "```\n"
            "Se lee de dentro hacia fuera: primero el `for`, que da los\n"
            "elementos, y despues la expresion de la izquierda, que dice en que\n"
            "se convierte cada uno.\n\n"
            "## Comprensiones con filtro\n"
            "Anadiendo un `if` al final te quedas solo con los que cumplen algo:\n"
            "```python\n"
            "numeros = [4, 7, 10, 3, 8]                     # datos de partida\n"
            "pares = [n for n in numeros if n % 2 == 0]     # solo los pares\n"
            "print(pares)                                   # [4, 10, 8]\n\n"
            "cuadrados = [n * n for n in range(1, 6)]       # transforma\n"
            "print(cuadrados)                               # [1, 4, 9, 16, 25]\n\n"
            "largos = [p for p in ['ana', 'bernardo'] if len(p) > 4]   # filtra\n"
            "print(largos)                                  # ['bernardo']\n"
            "```\n"
            "Regla practica: si la comprension no te cabe comoda en una linea,\n"
            "escribe el bucle normal. Compacto no es lo mismo que legible.\n\n"
            "## try/except: capturar lo que puede fallar\n"
            "Algunas operaciones fallan por causas que no controlas: un dato mal\n"
            "escrito, una division por cero. `try/except` te deja intentarlo y\n"
            "decidir que hacer si sale mal, en vez de que el programa se corte:\n"
            "```python\n"
            "try:                            # intenta ejecutar este bloque\n"
            "    resultado = 10 / 0          # esto lanza ZeroDivisionError\n"
            "except ZeroDivisionError:       # y si falla POR ESTA razon...\n"
            "    resultado = None            # plan B\n"
            "print(resultado)                # None, y el programa sigue vivo\n\n"
            "try:                            # el try rodea SOLO lo que puede fallar\n"
            "    numero = int('cuarenta')    # int() no sabe leer eso\n"
            "except ValueError:              # asi avisa int() con un texto no numerico\n"
            "    numero = 0                  # valor de respaldo\n"
            "print(numero)                   # 0\n"
            "```\n"
            "Captura **el error concreto** que esperas (`ValueError`,\n"
            "`ZeroDivisionError`). Un `except:` a secas se traga tambien los\n"
            "errores que no habias previsto, incluidos tus propios fallos de\n"
            "escritura, y te deja sin pistas para depurar.\n\n"
            "## raise: lanzar tu propio error\n"
            "A veces el que detecta que algo esta mal eres tu. `raise` levanta un\n"
            "error para avisar a quien llamo tu funcion:\n"
            "```python\n"
            "def raiz(n):                    # tu decides que entradas aceptas\n"
            "    if n < 0:\n"
            "        raise ValueError('no hay raiz real de un negativo')  # y lo dices\n"
            "    return n ** 0.5             # solo llega aqui si el dato valia\n\n"
            "print(raiz(9))                  # 3.0\n\n"
            "try:                            # asi lo captura quien te llama\n"
            "    raiz(-4)                    # lanza el ValueError de arriba\n"
            "except ValueError as e:         # `as e` guarda el error para leerlo\n"
            "    print('fallo:', e)          # fallo: no hay raiz real de un negativo\n"
            "```\n"
            "Devolver `None` ante un dato invalido lo esconde: quien te llama\n"
            "sigue como si nada y el fallo aparece diez lineas mas abajo.\n"
            "`raise` para el problema donde se origina y explica por que.\n\n"
            "## with: cerrar siempre, pase lo que pase\n"
            "Cuando abres un archivo hay que cerrarlo. Si en medio salta un\n"
            "error, el `close()` no llega a ejecutarse. `with` lo cierra por ti\n"
            "aunque el bloque falle:\n"
            "```python\n"
            "with open('notas.txt', 'w') as f:   # 'w' crea o sobrescribe\n"
            "    f.write('8\\n')                  # dentro del bloque, f esta abierto\n"
            "    f.write('6\\n')                  # una segunda linea\n"
            "# al salir del with, el archivo queda cerrado y guardado\n\n"
            "with open('notas.txt') as f:        # sin modo, abre para leer\n"
            "    contenido = f.read()            # lee todo el archivo de una vez\n"
            "print(contenido.split())            # ['8', '6']\n"
            "```\n"
            "La variable de despues del `as` solo tiene sentido dentro del\n"
            "bloque. Fuera, el archivo ya esta cerrado.\n\n"
            "## Errores comunes\n"
            "- Usar `except:` sin decir que error esperas. Se traga tambien los\n"
            "  `NameError` por escribir mal un nombre, y te pasas la tarde\n"
            "  buscando un bug que el `except` estaba ocultando.\n"
            "- Meter dentro del `try` mucho mas codigo del que puede fallar. El\n"
            "  `try` rodea la linea arriesgada, no la funcion entera.\n"
            "- Devolver `None` cuando el dato es invalido en vez de lanzar un\n"
            "  error. El programa sigue con un `None` dentro y revienta despues,\n"
            "  lejos de donde estaba el problema real.\n"
            "- Escribir comprensiones de tres pisos con dos `for` y dos `if`.\n"
            "  Si no se lee de un vistazo, el bucle normal es mejor codigo.\n"
            "- Abrir un archivo sin `with` y confiar en llamar a `close()`. Si\n"
            "  algo falla antes, el archivo se queda abierto.\n\n"
            "## Resumen\n"
            "- `[expresion for x in coleccion]` construye una lista; con un `if`\n"
            "  al final, filtra.\n"
            "- `try/except ErrorConcreto` captura fallos esperables y deja el\n"
            "  programa vivo.\n"
            "- `raise ValueError('motivo')` avisa de un dato invalido donde se\n"
            "  detecta, en vez de esconderlo.\n"
            "- `with open(...) as f:` cierra el archivo siempre, incluso si el\n"
            "  bloque lanza un error.\n"
        ),
        difficulty="intermediate",
        category="python-moderno",
        order=7,
        estimated_duration=50,
        prerequisites_titles=["Listas, Tuplas y Diccionarios"],
        exercises=[
            ExerciseTemplate(
                title="Filtrado par",
                description="Tu primera comprension con filtro.",
                instructions=(
                    "Con UNA comprension de lista, guarda en `resultado` los "
                    "cuadrados de los numeros pares del 1 al 20. Debe empezar por "
                    "4, 16, 36 y terminar en 400."
                ),
                starter_code=(
                    "# TODO: resultado = [ ... for n in range(1, 21) if ... ]\n"
                    "resultado = []\n"
                ),
                hints=[
                    "range(1, 21) llega hasta el 20 incluido.",
                    "El cuadrado es n * n, y el filtro es if n % 2 == 0.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "son los cuadrados de los pares del 1 al 20",
                        "code": (
                            "esperado = [4, 16, 36, 64, 100, 144, 196, 256, 324, 400]\n"
                            "assert resultado == esperado, f'resultado vale {resultado}'"
                        ),
                    },
                    {
                        "name": "no se colo ningun impar",
                        "code": (
                            "assert len(resultado) == 10, "
                            "f'esperaba 10 valores y hay {len(resultado)}'\n"
                            "assert 1 not in resultado and 9 not in resultado, "
                            "'hay cuadrados de numeros impares'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Division segura",
                description="Captura el error en vez de dejar que rompa el programa.",
                instructions=(
                    "Define `division_segura(a, b)` que devuelva `a / b`, pero que "
                    "devuelva `None` si `b` es 0. Hazlo con `try/except "
                    "ZeroDivisionError`, no con un `if`: la idea es practicar la "
                    "captura del error."
                ),
                starter_code=(
                    "def division_segura(a, b):\n"
                    "    # TODO: intenta dividir y captura ZeroDivisionError\n"
                    "    ...\n"
                ),
                hints=[
                    "Dentro del try va el return a / b.",
                    "En el except ZeroDivisionError, devuelve None.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "divide normalmente",
                        "code": (
                            "assert division_segura(10, 2) == 5.0\n"
                            "assert division_segura(9, 3) == 3.0"
                        ),
                    },
                    {
                        "name": "dividir por cero devuelve None y no revienta",
                        "code": (
                            "assert division_segura(4, 2) == 2.0, "
                            "'primero tiene que dividir: con b distinto de 0 devuelve a / b'\n"
                            "obtenido = division_segura(1, 0)\n"
                            "assert obtenido is None, f'devolvio {obtenido!r}'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Convertir lo que se pueda",
                description="Un try/except dentro de un bucle.",
                instructions=(
                    "Define `a_enteros(textos)` que recorra la lista y devuelva "
                    "otra lista solo con los que se pueden convertir a entero con "
                    "`int()`. Los que fallan se descartan.\n\n"
                    "Por ejemplo, con `['3', 'x', '7', '4.5']` devuelve `[3, 7]`: "
                    "ni la letra ni el decimal sobreviven a `int()`."
                ),
                starter_code=(
                    "def a_enteros(textos):\n"
                    "    # TODO: recorre, intenta convertir y descarta lo que falle\n"
                    "    ...\n"
                ),
                hints=[
                    "El try/except va DENTRO del bucle, rodeando solo el int().",
                    "int() sobre algo que no es numero lanza ValueError.",
                    "En el except no hagas nada: continue, y sigue con el siguiente.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "conserva solo lo convertible",
                        "code": (
                            "obtenido = a_enteros(['3', 'x', '7', '4.5'])\n"
                            "assert obtenido == [3, 7], f'devolvio {obtenido}'"
                        ),
                    },
                    {
                        "name": "devuelve enteros de verdad, no textos",
                        "code": (
                            "obtenido = a_enteros(['10', '20'])\n"
                            "assert obtenido == [10, 20]\n"
                            "assert all(isinstance(x, int) for x in obtenido), "
                            "'te falto convertir: siguen siendo strings'"
                        ),
                    },
                    {
                        "name": "si no se puede convertir nada, lista vacia",
                        "code": (
                            "assert a_enteros(['a', 'b']) == []\n"
                            "assert a_enteros([]) == []"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Validar edad",
                description="Lanza tu propio error cuando el dato no tiene sentido.",
                instructions=(
                    "Define `validar_edad(edad)` que devuelva la edad si esta entre "
                    "0 y 120 incluidos. Si no lo esta, **lanza** un `ValueError` "
                    "cuyo mensaje contenga la palabra rango.\n\n"
                    "No devuelvas None ni imprimas nada: el aviso tiene que ser el "
                    "error."
                ),
                starter_code=(
                    "def validar_edad(edad):\n"
                    "    # TODO: si esta fuera de rango, raise ValueError(...)\n"
                    "    ...\n"
                ),
                hints=[
                    "El if comprueba edad < 0 or edad > 120.",
                    "raise ValueError('edad fuera de rango')",
                    "Si pasa la comprobacion, devuelve la edad tal cual.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "deja pasar las edades validas",
                        "code": (
                            "assert validar_edad(30) == 30\n"
                            "assert validar_edad(0) == 0\n"
                            "assert validar_edad(120) == 120"
                        ),
                    },
                    {
                        "name": "lanza ValueError con las invalidas",
                        "code": (
                            "for mala in (-1, 121, 500):\n"
                            "    try:\n"
                            "        validar_edad(mala)\n"
                            "    except ValueError:\n"
                            "        pass\n"
                            "    else:\n"
                            "        raise AssertionError(str(mala) + ' deberia lanzar ValueError')"
                        ),
                    },
                    {
                        "name": "el mensaje del error explica el motivo",
                        "code": (
                            "try:\n"
                            "    validar_edad(-5)\n"
                            "except ValueError as e:\n"
                            "    assert 'rango' in str(e), 'el mensaje no menciona el rango'\n"
                            "else:\n"
                            "    raise AssertionError('validar_edad(-5) deberia lanzar ValueError')"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Promedio de aprobados",
                description="Combina una comprension con filtro y un raise.",
                instructions=(
                    "Define `promedio_aprobados(notas)` que calcule el promedio de "
                    "las notas mayores o iguales a 5.\n\n"
                    "- Usa una comprension con filtro para quedarte con las "
                    "aprobadas.\n"
                    "- Si no hay ninguna aprobada, **lanza** un `ValueError` cuyo "
                    "mensaje contenga la palabra aprobadas.\n"
                    "- Devuelve el promedio redondeado a un decimal con "
                    "`round(x, 1)`."
                ),
                starter_code=(
                    "def promedio_aprobados(notas):\n"
                    "    # TODO: filtra con una comprension, valida y promedia\n"
                    "    ...\n"
                ),
                hints=[
                    "aprobadas = [n for n in notas if n >= 5]",
                    "Si len(aprobadas) == 0, raise ValueError con tu mensaje.",
                    "El promedio es sum(aprobadas) / len(aprobadas).",
                    "El raise va ANTES de dividir: si no, revientas con "
                    "ZeroDivisionError en vez de con tu mensaje.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "promedia solo las aprobadas",
                        "code": (
                            "obtenido = promedio_aprobados([5, 3, 7, 9, 2])\n"
                            "assert obtenido == 7.0, f'devolvio {obtenido}'"
                        ),
                    },
                    {
                        "name": "redondea a un decimal",
                        "code": (
                            "obtenido = promedio_aprobados([5, 6, 8])\n"
                            "assert obtenido == 6.3, f'devolvio {obtenido}'"
                        ),
                    },
                    {
                        "name": "sin aprobadas lanza ValueError, no ZeroDivisionError",
                        "code": (
                            "try:\n"
                            "    promedio_aprobados([1, 2, 3])\n"
                            "except ValueError as e:\n"
                            "    assert 'aprobadas' in str(e), 'el mensaje no lo explica'\n"
                            "except ZeroDivisionError:\n"
                            "    raise AssertionError('valida ANTES de dividir')\n"
                            "else:\n"
                            "    raise AssertionError('deberia haber lanzado ValueError')"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Guardar un informe",
                description="Encadena comprension, validacion con raise y escritura con with.",
                instructions=(
                    "Define `guardar_informe(ruta, lineas)` que:\n\n"
                    "- se quede solo con las lineas que tienen algo escrito, usando "
                    "una comprension y `.strip()` (las que son solo espacios se "
                    "descartan);\n"
                    "- si no queda ninguna, **lanza** un `ValueError` cuyo mensaje "
                    "contenga la palabra vacio;\n"
                    "- escriba cada linea limpia en el archivo `ruta` usando "
                    "`with open(ruta, 'w')`, una por linea;\n"
                    "- devuelva cuantas lineas escribio."
                ),
                starter_code=(
                    "def guardar_informe(ruta, lineas):\n"
                    "    # TODO: limpiar, validar, escribir con with y devolver el total\n"
                    "    ...\n"
                ),
                hints=[
                    "limpias = [l.strip() for l in lineas if len(l.strip()) > 0]",
                    "Valida con el raise antes de abrir el archivo.",
                    "Dentro del with, un for que haga f.write(linea + chr(10)).",
                    "Devuelve len(limpias) al final, fuera del with.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "escribe las lineas limpias y devuelve cuantas",
                        "code": (
                            "from pathlib import Path\n"
                            "Path('informe_test.txt').unlink(missing_ok=True)\n"
                            "n = guardar_informe('informe_test.txt', "
                            "['  hola ', '   ', 'mundo'])\n"
                            "assert n == 2, f'devolvio {n}'\n"
                            "with open('informe_test.txt') as f:\n"
                            "    contenido = f.read()\n"
                            "assert contenido.split() == ['hola', 'mundo'], "
                            "f'el archivo contiene {contenido!r}'"
                        ),
                    },
                    {
                        "name": "cada linea va en su propia linea del archivo",
                        "code": (
                            "from pathlib import Path\n"
                            "Path('informe_test2.txt').unlink(missing_ok=True)\n"
                            "guardar_informe('informe_test2.txt', ['a', 'b', 'c'])\n"
                            "with open('informe_test2.txt') as f:\n"
                            "    lineas = f.read().splitlines()\n"
                            "assert lineas == ['a', 'b', 'c'], f'quedo {lineas}'"
                        ),
                    },
                    {
                        "name": "sin lineas utiles lanza ValueError",
                        "code": (
                            "try:\n"
                            "    guardar_informe('no_deberia.txt', ['  ', '   '])\n"
                            "except ValueError as e:\n"
                            "    assert 'vacio' in str(e), 'el mensaje no lo explica'\n"
                            "else:\n"
                            "    raise AssertionError('deberia haber lanzado ValueError')"
                        ),
                    },
                    {
                        "name": "no crea el archivo cuando no hay nada que escribir",
                        "code": (
                            "from pathlib import Path\n"
                            "Path('si_deberia.txt').unlink(missing_ok=True)\n"
                            "guardar_informe('si_deberia.txt', ['hola'])\n"
                            "assert Path('si_deberia.txt').exists(), "
                            "'con lineas utiles tiene que crear el archivo'\n"
                            "Path('no_deberia.txt').unlink(missing_ok=True)\n"
                            "try:\n"
                            "    guardar_informe('no_deberia.txt', ['   '])\n"
                            "except ValueError:\n"
                            "    pass\n"
                            "assert not Path('no_deberia.txt').exists(), "
                            "'validaste despues de abrir el archivo'"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="POO en Python",
        description=(
            "Clases y objetos: juntar los datos con las funciones que los cuidan, "
            "con self, __init__, metodos y encapsulacion basica."
        ),
        content=(
            "## Por que las clases\n"
            "Hasta ahora tus datos van por un lado y las funciones que los tocan\n"
            "por otro: una lista de saldos aqui, una funcion\n"
            "`retirar(saldos, i, monto)` alla. Con tres datos se aguanta; con\n"
            "treinta ya nadie recuerda que funcion puede tocar que dato ni quien\n"
            "comprobo que el saldo no quedara negativo. Una **clase** junta los\n"
            "datos y las funciones que los cuidan en una sola pieza, y deja una\n"
            "unica puerta para cambiarlos.\n\n"
            "## class e __init__: el molde y las copias\n"
            "La clase es el molde y se escribe una vez. Cada objeto que creas con\n"
            "ese molde tiene sus propios datos:\n"
            "```python\n"
            "class Perro:                     # el molde: se escribe una sola vez\n"
            "    def __init__(self, nombre):  # corre al crear CADA perro\n"
            "        self.nombre = nombre     # guarda el dato dentro del objeto\n\n"
            "firulais = Perro('Firulais')     # aqui corre __init__ con 'Firulais'\n"
            "laika = Perro('Laika')           # otro objeto, con su propio nombre\n"
            "print(firulais.nombre)           # Firulais\n"
            "print(laika.nombre)              # Laika\n"
            "```\n"
            "`Perro` es la clase; `firulais` y `laika` son **objetos** (o\n"
            "instancias) de esa clase. `__init__` no lo llamas tu: Python lo\n"
            "ejecuta solo al escribir `Perro('Firulais')`, y su trabajo es dejar\n"
            "el objeto listo para usarse.\n\n"
            "## self: el objeto que esta hablando\n"
            "`self` es el primer parametro de todo metodo y representa al objeto\n"
            "concreto sobre el que lo llamas:\n"
            "```python\n"
            "class Contador:\n"
            "    def __init__(self):\n"
            "        self.valor = 0           # cada contador arranca en SU cero\n\n"
            "    def sumar(self):             # self va siempre primero\n"
            "        self.valor = self.valor + 1   # cambia el estado de ESTE objeto\n"
            "        return self.valor        # y devuelve como quedo\n\n"
            "a = Contador()                   # dos objetos independientes\n"
            "b = Contador()                   # cada uno con su propio valor\n"
            "a.sumar()                        # Python pasa `a` como self; tu no lo escribes\n"
            "print(a.sumar())                 # 2\n"
            "print(b.valor)                   # 0  -> b ni se entero\n"
            "```\n"
            "`self` no es una palabra reservada, es una convencion: se llama asi\n"
            "en todo el Python del mundo y cambiarle el nombre solo consigue que\n"
            "nadie entienda tu codigo. Lo que escribes como `a.sumar()` Python lo\n"
            "traduce a `Contador.sumar(a)`, y por eso el metodo recibe un\n"
            "parametro que tu no pusiste en la llamada.\n\n"
            "## Metodos con parametros: el objeto se defiende\n"
            "Despues de `self` van tus propios parametros. Y como el metodo es la\n"
            "unica puerta al estado, es el sitio natural para validar:\n"
            "```python\n"
            "class Termostato:\n"
            "    def __init__(self, grados):\n"
            "        self.grados = grados     # el estado inicial llega por parametro\n\n"
            "    def subir(self, cuanto):     # self primero, tus parametros despues\n"
            "        if cuanto <= 0:          # el metodo cuida su propio estado\n"
            "            raise ValueError('cuanto debe ser positivo')   # corta aqui\n"
            "        self.grados = self.grados + cuanto   # solo si paso la validacion\n"
            "        return self.grados       # el metodo dice como quedo el objeto\n\n"
            "t = Termostato(18)\n"
            "print(t.subir(3))                # 21\n"
            "print(t.grados)                  # 21, el objeto se quedo asi\n"
            "```\n"
            "Fijate en el orden: primero valida, y solo despues toca\n"
            "`self.grados`. Al reves dejarias el objeto ya modificado y ademas\n"
            "lanzarias el error, que es la peor combinacion posible.\n\n"
            "## Un objeto puede guardar una coleccion\n"
            "Un atributo no tiene por que ser un numero suelto. Puede ser una\n"
            "lista que el objeto va llenando:\n"
            "```python\n"
            "class Cesta:\n"
            "    def __init__(self):\n"
            "        self.items = []                  # cada cesta con SU lista vacia\n\n"
            "    def agregar(self, nombre, precio):   # dos parametros ademas de self\n"
            "        self.items.append((nombre, precio))   # guarda el par como tupla\n\n"
            "    def total(self):\n"
            "        precios = [precio for nombre, precio in self.items]  # desempaqueta cada par\n"
            "        return sum(precios)              # y los suma\n\n"
            "c = Cesta()\n"
            "c.agregar('pan', 2)                      # se acumulan en la lista del objeto\n"
            "c.agregar('leche', 3)\n"
            "print(c.items)                           # [('pan', 2), ('leche', 3)]\n"
            "print(c.total())                         # 5\n"
            "```\n"
            "O un diccionario, cuando lo que necesitas es buscar por nombre:\n"
            "```python\n"
            "class Stock:\n"
            "    def __init__(self):\n"
            "        self.unidades = {}                     # nombre -> cantidad\n\n"
            "    def agregar(self, nombre, cantidad):\n"
            "        actual = self.unidades.get(nombre, 0)  # 0 si aun no existe\n"
            "        self.unidades[nombre] = actual + cantidad   # guarda la suma\n\n"
            "s = Stock()\n"
            "s.agregar('lapiz', 3)                          # la clave aun no existia\n"
            "s.agregar('lapiz', 2)                          # suma sobre lo que habia\n"
            "print(s.unidades)                              # {'lapiz': 5}\n"
            "print(s.unidades.get('goma', 0))               # 0, sin reventar\n"
            "```\n"
            "La lista sirve para acumular en orden; el diccionario, para llegar a\n"
            "un dato por su nombre sin recorrer nada. `.get(clave, 0)` te da un\n"
            "valor por defecto en vez del `KeyError` que darias con\n"
            "`self.unidades[clave]`.\n\n"
            "## Encapsulacion: una sola puerta\n"
            "Si cualquiera puede escribir `cuenta.saldo = -999`, tus validaciones\n"
            "no valen nada. La convencion de Python es un guion bajo delante:\n"
            "```python\n"
            "class Cuenta:\n"
            "    def __init__(self):\n"
            "        self._saldo = 0                  # el _ dice: no me toques desde fuera\n\n"
            "    def depositar(self, monto):\n"
            "        if monto <= 0:                   # la validacion vive en el metodo\n"
            "            raise ValueError('el deposito debe ser positivo')\n"
            "        self._saldo = self._saldo + monto   # la unica forma de moverlo\n\n"
            "    def consultar(self):                 # la puerta de lectura\n"
            "        return self._saldo\n\n"
            "c = Cuenta()\n"
            "c.depositar(50)                          # se pasa por la puerta\n"
            "print(c.consultar())                     # 50\n"
            "```\n"
            "Python no tiene atributos privados de verdad: `c._saldo = -999`\n"
            "funciona igual. El guion bajo es una senal, no un candado, y sirve\n"
            "para lo mismo que sirve una puerta con un cartel: quien la salta ya\n"
            "sabe que va por su cuenta.\n\n"
            "## __str__: como se ve tu objeto al imprimirlo\n"
            "Si imprimes un objeto sin mas, Python te ensena algo tan util como\n"
            "`<Punto object at 0x7f3a...>`. `__str__` decide que se ve:\n"
            "```python\n"
            "class Punto:\n"
            "    def __init__(self, x, y):\n"
            "        self.x = x                       # un atributo por coordenada\n"
            "        self.y = y\n\n"
            "    def __str__(self):                   # Python lo llama al hacer print()\n"
            "        return f'Punto({self.x}, {self.y})'   # devuelve un texto, no imprime\n\n"
            "p = Punto(2, 5)                          # sin __str__ veras <Punto object at 0x...>\n"
            "print(p)                                 # Punto(2, 5)\n"
            "print(str(p) + ' listo')                 # Punto(2, 5) listo\n"
            "```\n"
            "`__str__` **devuelve** el texto con `return`; el `print` lo hace\n"
            "quien te llama. Si dentro pones un `print` en vez de un `return`,\n"
            "veras la linea y ademas un `None`.\n\n"
            "## Errores comunes\n"
            "- Olvidar `self` al definir el metodo (`def subir(cuanto):`). Al\n"
            "  llamar `t.subir(3)` Python pasa el objeto como primer argumento y\n"
            "  salta `TypeError: Termostato.subir() takes 1 positional argument\n"
            "  but 2 were given`. El primer parametro de un metodo es siempre\n"
            "  `self`, y el objeto va ahi.\n"
            "- Guardar el resultado en una variable local en vez de en `self.`:\n"
            "  `grados = self.grados + cuanto` dentro de `subir` calcula bien y\n"
            "  **no lanza ningun error**, pero la variable muere al terminar el\n"
            "  metodo y el objeto se queda como estaba. Si el estado no cambia y\n"
            "  no hay error, mira si te falta el `self.` de la izquierda.\n"
            "- Crear la lista fuera de `__init__`, pegada a la clase\n"
            "  (`class Cesta:` y debajo `items = []`). Esa lista es **una sola\n"
            "  para todas las instancias**, y lo que agregas en una cesta aparece\n"
            "  en la otra. Las colecciones se crean dentro de `__init__`.\n"
            "- Llamar al metodo sin parentesis: `c.consultar` te devuelve el\n"
            "  metodo (`<bound method ...>`), `c.consultar()` te devuelve el\n"
            "  saldo. Si al imprimir sale algo raro con la palabra `method`, te\n"
            "  faltan los parentesis.\n"
            "- Poner un `return` con valor dentro de `__init__`. Su trabajo es\n"
            "  rellenar el objeto, no devolverlo; devolver algo distinto de\n"
            "  `None` lanza `TypeError`.\n\n"
            "## Resumen\n"
            "- `class Nombre:` define el molde; `Nombre(...)` crea un objeto y\n"
            "  ejecuta su `__init__`.\n"
            "- `__init__(self, ...)` guarda el estado inicial en `self.atributo`.\n"
            "- `self` es el objeto sobre el que llamas el metodo; va siempre como\n"
            "  primer parametro y nunca se pasa en la llamada.\n"
            "- Un metodo valida antes de tocar el estado: `raise` primero,\n"
            "  `self.x = ...` despues.\n"
            "- Un atributo puede ser una lista (acumular en orden) o un\n"
            "  diccionario (buscar por nombre, con `.get(clave, 0)`).\n"
            "- El guion bajo (`self._saldo`) marca lo que no se toca desde fuera;\n"
            "  los metodos son la unica puerta.\n"
            "- `__str__` devuelve el texto que se ve al imprimir el objeto.\n"
        ),
        difficulty="advanced",
        category="oop",
        order=8,
        estimated_duration=55,
        prerequisites_titles=["Comprensiones y Manejo de Errores"],
        exercises=[
            ExerciseTemplate(
                title="Tu primera clase",
                description="Un molde con __init__ y dos atributos.",
                instructions=(
                    "Define una clase `Libro` cuyo `__init__` reciba `titulo` y "
                    "`paginas` y los guarde en `self.titulo` y `self.paginas`.\n\n"
                    "No necesita ningun metodo mas: con crear `Libro('Rayuela', 600)` "
                    "y poder leer `.titulo` y `.paginas` esta resuelto."
                ),
                starter_code=(
                    "# TODO: define la clase Libro con su __init__\n"
                    "class Libro:\n"
                    "    ...\n"
                ),
                hints=[
                    "Debajo de `class Libro:`, indentado, va `def __init__(self, titulo, paginas):`.",
                    "Dentro del __init__: self.titulo = titulo y self.paginas = paginas.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "guarda titulo y paginas",
                        "code": (
                            "libro = Libro('Rayuela', 600)\n"
                            "assert libro.titulo == 'Rayuela', f'titulo vale {libro.titulo!r}'\n"
                            "assert libro.paginas == 600, f'paginas vale {libro.paginas!r}'"
                        ),
                    },
                    {
                        "name": "cada libro tiene sus propios datos",
                        "code": (
                            "uno = Libro('Rayuela', 600)\n"
                            "otro = Libro('Ficciones', 200)\n"
                            "assert uno.titulo == 'Rayuela' and otro.titulo == 'Ficciones', "
                            "'los dos libros comparten el mismo titulo'\n"
                            "assert uno.paginas == 600 and otro.paginas == 200"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Metodo area",
                description="Anade un metodo que calcula a partir del estado.",
                instructions=(
                    "La clase `Rectangulo` ya guarda `base` y `altura`. Anade el "
                    "metodo `area(self)` que **devuelva** base por altura.\n\n"
                    "Devolver, no imprimir: quien llame `r.area()` tiene que "
                    "recibir el numero."
                ),
                starter_code=(
                    "class Rectangulo:\n"
                    "    def __init__(self, base, altura):\n"
                    "        self.base = base\n"
                    "        self.altura = altura\n\n"
                    "    # TODO: def area(self): ...\n"
                ),
                hints=[
                    "El metodo va indentado dentro de la clase, al mismo nivel que __init__.",
                    "No lleva parametros ademas de self: los datos ya estan en el objeto.",
                    "return self.base * self.altura",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "devuelve el area",
                        "code": (
                            "r = Rectangulo(3, 4)\n"
                            "obtenido = r.area()\n"
                            "assert obtenido == 12, f'devolvio {obtenido!r}'"
                        ),
                    },
                    {
                        "name": "funciona con decimales y con otras medidas",
                        "code": (
                            "assert Rectangulo(2.5, 2).area() == 5.0\n"
                            "assert Rectangulo(10, 7).area() == 70"
                        ),
                    },
                    {
                        "name": "devuelve el numero, no lo imprime",
                        "code": (
                            "obtenido = Rectangulo(1, 1).area()\n"
                            "assert obtenido is not None, "
                            "'area() no devuelve nada: te falta el return'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Clase Producto",
                description="Un metodo que modifica el estado del objeto.",
                instructions=(
                    "Agrega a `Producto` el metodo `aplicar_descuento(pct)` que "
                    "reduzca `self.precio` en `pct` por ciento.\n\n"
                    "Modifica el precio del objeto; no hace falta que devuelva "
                    "nada. Con un producto de 100 y `aplicar_descuento(20)`, "
                    "`precio` queda en 80."
                ),
                starter_code=(
                    "class Producto:\n"
                    "    def __init__(self, nombre: str, precio: float):\n"
                    "        self.nombre = nombre\n"
                    "        self.precio = precio\n\n"
                    "    # TODO: def aplicar_descuento(self, pct): ...\n"
                ),
                hints=[
                    "El metodo recibe self y pct: def aplicar_descuento(self, pct):",
                    "Quitar un 20% es quedarse con el 80%: precio * (100 - pct) / 100.",
                    "Guarda el resultado en self.precio, si no el objeto no cambia.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "descuento 20% sobre 100 -> 80",
                        "code": (
                            "p = Producto('lapiz', 100)\n"
                            "p.aplicar_descuento(20)\n"
                            "assert abs(p.precio - 80) < 1e-9, p.precio"
                        ),
                    },
                    {
                        "name": "descuento 50% sobre 200 -> 100",
                        "code": (
                            "p = Producto('mochila', 200)\n"
                            "p.aplicar_descuento(50)\n"
                            "assert abs(p.precio - 100) < 1e-9, p.precio"
                        ),
                    },
                    {
                        "name": "dos descuentos se aplican sobre el precio ya rebajado",
                        "code": (
                            "p = Producto('silla', 100)\n"
                            "p.aplicar_descuento(10)\n"
                            "p.aplicar_descuento(10)\n"
                            "assert abs(p.precio - 81) < 1e-9, "
                            "f'esperaba 81 y quedo {p.precio}'"
                        ),
                    },
                    {
                        "name": "rebajar uno no toca al otro",
                        "code": (
                            "a = Producto('a', 100)\n"
                            "b = Producto('b', 100)\n"
                            "a.aplicar_descuento(25)\n"
                            "assert abs(b.precio - 100) < 1e-9, "
                            "'el descuento afecto a los dos productos'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Cuenta bancaria",
                description="Estado que se mueve y un metodo que lo defiende.",
                instructions=(
                    "Implementa en `Cuenta` dos metodos:\n\n"
                    "- `depositar(monto)`: suma `monto` a `self.saldo`.\n"
                    "- `retirar(monto)`: resta `monto` si hay saldo suficiente; si "
                    "no lo hay, **lanza** un `ValueError`.\n\n"
                    "Cuando el retiro no se puede hacer, el saldo tiene que quedar "
                    "como estaba: valida antes de restar."
                ),
                starter_code=(
                    "class Cuenta:\n"
                    "    def __init__(self):\n"
                    "        self.saldo = 0\n\n"
                    "    # TODO: depositar y retirar\n"
                ),
                hints=[
                    "Los dos metodos empiezan por self: def depositar(self, monto):",
                    "Depositar es self.saldo = self.saldo + monto.",
                    "En retirar, primero: if monto > self.saldo: raise ValueError('saldo insuficiente').",
                    "La resta va despues del if, no antes: si no, dejas la cuenta en negativo y ademas lanzas el error.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "depositar/retirar actualiza saldo; retiro invalido lanza ValueError",
                        "code": (
                            "c = Cuenta()\n"
                            "c.depositar(100)\n"
                            "c.retirar(30)\n"
                            "assert c.saldo == 70, c.saldo\n"
                            "try:\n"
                            "    c.retirar(1000)\n"
                            "    raise AssertionError('retiro > saldo debio lanzar ValueError')\n"
                            "except ValueError:\n"
                            "    pass"
                        ),
                    },
                    {
                        "name": "se puede retirar todo y queda en cero",
                        "code": (
                            "c = Cuenta()\n"
                            "c.depositar(50)\n"
                            "c.retirar(50)\n"
                            "assert c.saldo == 0, f'quedo en {c.saldo}'"
                        ),
                    },
                    {
                        "name": "el retiro fallido no toca el saldo",
                        "code": (
                            "c = Cuenta()\n"
                            "c.depositar(40)\n"
                            "try:\n"
                            "    c.retirar(41)\n"
                            "except ValueError:\n"
                            "    pass\n"
                            "assert c.saldo == 40, "
                            "f'restaste antes de validar: el saldo quedo en {c.saldo}'"
                        ),
                    },
                    {
                        "name": "cada cuenta lleva su propio saldo",
                        "code": (
                            "a = Cuenta()\n"
                            "b = Cuenta()\n"
                            "a.depositar(10)\n"
                            "assert b.saldo == 0, 'las dos cuentas comparten el saldo'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Cesta de la compra",
                description="Un objeto que acumula en una lista y valida lo que entra.",
                instructions=(
                    "Define la clase `Cesta`, que se crea vacia (`Cesta()`, sin "
                    "argumentos) y guarda lo que le agregan en `self.items`.\n\n"
                    "- `agregar(nombre, precio)`: si `precio` es 0 o negativo, "
                    "**lanza** un `ValueError` cuyo mensaje contenga la palabra "
                    "precio y no guarda nada. Si es valido, guarda el par "
                    "`(nombre, precio)` en la lista.\n"
                    "- `total()`: devuelve la suma de los precios (0 si la cesta "
                    "esta vacia).\n"
                    "- `nombres()`: devuelve la lista de los nombres, en el orden "
                    "en que se agregaron. Usa una comprension."
                ),
                starter_code=(
                    "class Cesta:\n"
                    "    def __init__(self):\n"
                    "        # TODO: arranca con la lista vacia\n"
                    "        ...\n\n"
                    "    # TODO: agregar, total y nombres\n"
                ),
                hints=[
                    "self.items = [] va DENTRO de __init__, nunca pegado a la clase.",
                    "Guardar el par: self.items.append((nombre, precio)).",
                    "total: precios = [p for n, p in self.items] y devuelve sum(precios).",
                    "En agregar, el raise va antes del append: si validas despues, el dato malo ya entro.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "una cesta nueva esta vacia",
                        "code": (
                            "c = Cesta()\n"
                            "assert c.total() == 0, f'total() devolvio {c.total()!r}'\n"
                            "assert c.nombres() == [], f'nombres() devolvio {c.nombres()!r}'"
                        ),
                    },
                    {
                        "name": "suma los precios y conserva el orden de los nombres",
                        "code": (
                            "c = Cesta()\n"
                            "c.agregar('pan', 2)\n"
                            "c.agregar('leche', 3)\n"
                            "c.agregar('cafe', 5)\n"
                            "assert c.total() == 10, f'total() devolvio {c.total()!r}'\n"
                            "assert c.nombres() == ['pan', 'leche', 'cafe'], "
                            "f'nombres() devolvio {c.nombres()!r}'"
                        ),
                    },
                    {
                        "name": "un precio invalido lanza ValueError",
                        "code": (
                            "c = Cesta()\n"
                            "for malo in (0, -5):\n"
                            "    try:\n"
                            "        c.agregar('gratis', malo)\n"
                            "    except ValueError as e:\n"
                            "        assert 'precio' in str(e), "
                            "'el mensaje no menciona el precio'\n"
                            "    else:\n"
                            "        raise AssertionError(str(malo) + ' deberia lanzar ValueError')"
                        ),
                    },
                    {
                        "name": "el item invalido no se guarda",
                        "code": (
                            "c = Cesta()\n"
                            "c.agregar('pan', 2)\n"
                            "try:\n"
                            "    c.agregar('gratis', -1)\n"
                            "except ValueError:\n"
                            "    pass\n"
                            "assert c.total() == 2, "
                            "f'el item invalido entro en la cesta: total() = {c.total()}'\n"
                            "assert c.nombres() == ['pan'], f'nombres() devolvio {c.nombres()!r}'"
                        ),
                    },
                    {
                        "name": "dos cestas no comparten los items",
                        "code": (
                            "a = Cesta()\n"
                            "b = Cesta()\n"
                            "a.agregar('pan', 2)\n"
                            "assert b.total() == 0, "
                            "'las dos cestas comparten la lista: creala dentro de __init__'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Inventario de la tienda",
                description="El pipeline: diccionario interno, dos validaciones, comprension y __str__.",
                instructions=(
                    "Define la clase `Inventario`, que se crea vacia "
                    "(`Inventario()`) y guarda las unidades de cada producto en un "
                    "diccionario interno `self._stock` (el guion bajo avisa de que "
                    "nadie lo toca desde fuera).\n\n"
                    "- `agregar(nombre, cantidad)`: si `cantidad` es 0 o negativa, "
                    "**lanza** `ValueError` con la palabra cantidad en el mensaje. "
                    "Si ya habia unidades de ese producto, se suman.\n"
                    "- `consultar(nombre)`: devuelve las unidades que hay, o 0 si "
                    "ese producto no esta.\n"
                    "- `retirar(nombre, cantidad)`: resta las unidades; si no hay "
                    "suficientes, **lanza** `ValueError` con la palabra suficiente "
                    "en el mensaje y deja el stock como estaba.\n"
                    "- `total_unidades()`: devuelve la suma de todas las unidades "
                    "del inventario. Usa una comprension.\n"
                    "- `__str__`: devuelve el texto `Inventario: N unidades`, con "
                    "`N` igual a `total_unidades()`."
                ),
                starter_code=(
                    "class Inventario:\n"
                    "    def __init__(self):\n"
                    "        # TODO: arranca con el diccionario vacio\n"
                    "        ...\n\n"
                    "    # TODO: agregar, consultar, retirar, total_unidades y __str__\n"
                ),
                hints=[
                    "self._stock = {} dentro de __init__.",
                    "consultar es una linea: return self._stock.get(nombre, 0), que da 0 si no existe.",
                    "Usa consultar dentro de agregar y retirar en vez de repetir el .get: "
                    "self._stock[nombre] = self.consultar(nombre) + cantidad.",
                    "total_unidades: sum([u for u in self._stock.values()]). "
                    "Y __str__ devuelve f'Inventario: {self.total_unidades()} unidades'.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "agregar acumula y consultar lee",
                        "code": (
                            "inv = Inventario()\n"
                            "inv.agregar('lapiz', 3)\n"
                            "inv.agregar('lapiz', 2)\n"
                            "inv.agregar('goma', 1)\n"
                            "assert inv.consultar('lapiz') == 5, "
                            "f\"consultar('lapiz') devolvio {inv.consultar('lapiz')!r}\"\n"
                            "assert inv.consultar('goma') == 1"
                        ),
                    },
                    {
                        "name": "consultar algo que no esta devuelve 0",
                        "code": (
                            "inv = Inventario()\n"
                            "assert inv.consultar('fantasma') == 0, "
                            "'usa .get(nombre, 0) para no reventar con un KeyError'"
                        ),
                    },
                    {
                        "name": "cantidad invalida al agregar lanza ValueError",
                        "code": (
                            "inv = Inventario()\n"
                            "for mala in (0, -3):\n"
                            "    try:\n"
                            "        inv.agregar('lapiz', mala)\n"
                            "    except ValueError as e:\n"
                            "        assert 'cantidad' in str(e), "
                            "'el mensaje no menciona la cantidad'\n"
                            "    else:\n"
                            "        raise AssertionError(str(mala) + ' deberia lanzar ValueError')\n"
                            "assert inv.consultar('lapiz') == 0, 'la cantidad invalida entro igual'"
                        ),
                    },
                    {
                        "name": "retirar resta, y si no alcanza lanza ValueError sin tocar el stock",
                        "code": (
                            "inv = Inventario()\n"
                            "inv.agregar('lapiz', 10)\n"
                            "inv.retirar('lapiz', 4)\n"
                            "assert inv.consultar('lapiz') == 6, "
                            "f\"quedaron {inv.consultar('lapiz')} lapices\"\n"
                            "try:\n"
                            "    inv.retirar('lapiz', 7)\n"
                            "except ValueError as e:\n"
                            "    assert 'suficiente' in str(e), 'el mensaje no lo explica'\n"
                            "else:\n"
                            "    raise AssertionError('retirar de mas deberia lanzar ValueError')\n"
                            "assert inv.consultar('lapiz') == 6, "
                            "'restaste antes de validar: el stock cambio igual'"
                        ),
                    },
                    {
                        "name": "total_unidades suma todo el inventario",
                        "code": (
                            "inv = Inventario()\n"
                            "assert inv.total_unidades() == 0, 'un inventario vacio suma 0'\n"
                            "inv.agregar('lapiz', 3)\n"
                            "inv.agregar('goma', 4)\n"
                            "inv.agregar('regla', 1)\n"
                            "assert inv.total_unidades() == 8, "
                            "f'devolvio {inv.total_unidades()!r}'"
                        ),
                    },
                    {
                        "name": "__str__ muestra el total",
                        "code": (
                            "inv = Inventario()\n"
                            "inv.agregar('lapiz', 3)\n"
                            "inv.agregar('goma', 4)\n"
                            "assert str(inv) == 'Inventario: 7 unidades', "
                            "f'str(inv) devolvio {str(inv)!r}'"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Modulos, Paquetes y Entornos",
        description=(
            "Partir el codigo en archivos: import, modulos propios, paquetes, la "
            "libreria estandar, el guard de __main__ y los entornos virtuales."
        ),
        content=(
            "## Por que partir el codigo en archivos\n"
            "Todo lo que has escrito hasta ahora cabia en un archivo. Un proyecto\n"
            "de verdad no: acabas con mil lineas donde no encuentras nada y donde\n"
            "no puedes reutilizar una funcion sin copiarla. Un **modulo** es la\n"
            "unidad para partir eso, y `import` es como se juntan otra vez las\n"
            "piezas.\n\n"
            "## import, from ... import y as\n"
            "Empecemos por lo que ya viene con Python. `math` y `json` son\n"
            "modulos de la **libreria estandar**: estan instalados de fabrica.\n"
            "```python\n"
            "import math                     # trae el modulo entero\n"
            "print(math.sqrt(16))            # 4.0  -> el nombre del modulo delante\n"
            "print(math.floor(3.7))          # 3\n\n"
            "from math import sqrt, pi       # trae SOLO esos dos nombres\n"
            "print(sqrt(25), round(pi, 2))   # 5.0 3.14  -> ya sin el math. delante\n\n"
            "import json as j                # alias, para nombres largos\n"
            "print(j.dumps({'a': 1}))        # {\"a\": 1}  -> el dict como texto JSON\n"
            "```\n"
            "Las tres formas hacen lo mismo por dentro. `import modulo` deja claro\n"
            "de donde sale cada cosa y es la opcion por defecto; `from ... import`\n"
            "acorta cuando usas un nombre muchas veces. Los `import` van todos\n"
            "arriba del archivo, juntos.\n\n"
            "## Un modulo es un archivo .py tuyo\n"
            "No hay nada especial en los modulos de Python: cualquier archivo\n"
            "`.py` lo es. Aqui, como no tienes un explorador de archivos, lo\n"
            "escribimos desde el propio codigo:\n"
            "```python\n"
            "from pathlib import Path        # para escribir el archivo\n"
            "import sys                      # para tocar sys.path y sys.modules\n\n"
            "sys.modules.pop('saludos', None)      # olvida la version anterior (ver abajo)\n"
            "Path('saludos.py').write_text(        # crea el archivo, con su codigo dentro\n"
            '    "def hola(nombre):\\n"\n'
            "    \"    return f'Hola, {nombre}'\\n\"\n"
            ")\n"
            "if '.' not in sys.path:               # solo si no estaba ya\n"
            "    sys.path.insert(0, '.')           # busca modulos tambien en esta carpeta\n\n"
            "import saludos                        # ahora ya existe y se puede importar\n"
            "print(saludos.hola('Ana'))            # Hola, Ana\n"
            "```\n"
            "Fijate en `sys.path`: es la lista de sitios donde Python busca lo que\n"
            "le pides importar. Si tu archivo no esta en ninguno, el import falla\n"
            "con `ModuleNotFoundError` por mucho que el archivo exista.\n\n"
            "Y `sys.modules.pop('saludos', None)` esta por otra razon: Python\n"
            "**cachea** los modulos ya importados. Si corriges `saludos.py` y\n"
            "vuelves a ejecutar sin borrar el cache, sigues usando la version\n"
            "vieja y te vuelves loco. Pasa aqui, y pasa igual en un notebook.\n\n"
            "## Un paquete es una carpeta con __init__.py\n"
            "Cuando los modulos crecen, se agrupan en carpetas. Una carpeta con un\n"
            "archivo `__init__.py` dentro es un **paquete**:\n"
            "```python\n"
            "from pathlib import Path        # crea carpetas y archivos\n"
            "import sys\n\n"
            "Path('tienda').mkdir(exist_ok=True)          # la carpeta: el paquete\n"
            "Path('tienda/__init__.py').write_text('')    # este archivo la convierte en uno\n"
            "Path('tienda/precios.py').write_text('IVA = 0.21\\n')   # un modulo dentro\n\n"
            "if '.' not in sys.path:\n"
            "    sys.path.insert(0, '.')                  # otra vez, la carpeta actual\n"
            "from tienda import precios                   # paquete.modulo\n"
            "print(precios.IVA)                           # 0.21\n"
            "```\n"
            "`__init__.py` puede estar vacio: su trabajo es decir *esta carpeta es\n"
            "un paquete, no una carpeta cualquiera*. Con eso, `tienda.precios` es\n"
            "una ruta de import como cualquier otra.\n\n"
            "## El guard `if __name__ == '__main__'`\n"
            "Cuando Python ejecuta un archivo directamente le pone a la variable\n"
            "`__name__` el valor `'__main__'`. Cuando ese mismo archivo se\n"
            "importa desde otro, `__name__` pasa a ser el nombre del modulo\n"
            "(`'utils'`). Por eso el codigo de prueba se protege:\n\n"
            "```python\n"
            "def normalizar(texto):                 # lo util del modulo: esto se importa\n"
            "    return texto.strip().lower()\n\n"
            "if __name__ == '__main__':             # True solo si ejecutas ESTE archivo\n"
            "    # solo corre si ejecutas ESTE archivo, no al importarlo\n"
            "    print(normalizar('  HOLA  '))\n"
            "```\n"
            "Sin el guard, importar `utils` ejecutaria tambien sus pruebas.\n\n"
            "> **Nota honesta sobre el editor de PyCode**: este patron no lo\n"
            "> puedes comprobar aqui. El editor ejecuta tu codigo en un namespace\n"
            "> propio donde `__name__` vale `'builtins'`, asi que el bloque del\n"
            "> guard nunca entra. Es una limitacion del sandbox del navegador, no\n"
            "> de tu codigo: en un Python normal funciona como esta descrito.\n"
            "> Preferimos decirtelo a que te vuelvas loco buscando por que no\n"
            "> imprime nada.\n\n"
            "## Entornos virtuales y pip\n"
            "La libreria estandar no lo trae todo: pandas, requests o pytest se\n"
            "instalan con `pip`. El problema es que instalarlos *en el sistema*\n"
            "mezcla las dependencias de todos tus proyectos, y un dia uno necesita\n"
            "una version que rompe a otro. La solucion es un **entorno virtual**:\n"
            "una carpeta con su propio Python y sus propios paquetes.\n\n"
            "```\n"
            "python -m venv .venv          # crea el entorno en la carpeta .venv\n"
            ".venv\\Scripts\\activate        # activarlo en Windows\n"
            "source .venv/bin/activate     # activarlo en Linux o Mac\n"
            "pip install pandas            # ya solo afecta a ESTE proyecto\n"
            "pip freeze > requirements.txt # deja escrito que versiones usas\n"
            "pip install -r requirements.txt   # y otro reproduce tu entorno con eso\n"
            "```\n"
            "Esas lineas no son Python: van en la terminal, no en el editor. Aqui\n"
            "no las puedes probar -el navegador no tiene terminal ni pip-, pero\n"
            "son el primer paso de cualquier proyecto real, y `requirements.txt`\n"
            "es lo que hace que tu codigo funcione tambien en el ordenador de\n"
            "otro.\n\n"
            "## Errores comunes\n"
            "- `ModuleNotFoundError` con un archivo que existe: no esta en\n"
            "  `sys.path`. O lo anades, o ejecutas desde la carpeta que lo\n"
            "  contiene.\n"
            "- Llamar a tu archivo como uno del estandar (`math.py`, `json.py`,\n"
            "  `random.py`). El tuyo gana y tapa al de verdad, con errores\n"
            "  absurdos despues.\n"
            "- Editar un modulo y no ver el cambio: es el cache de `sys.modules`.\n"
            "  `sys.modules.pop('nombre', None)` antes de volver a importar.\n"
            "- `from modulo import *`. Trae todos los nombres de golpe y pisa los\n"
            "  tuyos sin avisar; ademas, quien lea el codigo no sabe de donde sale\n"
            "  cada cosa.\n"
            "- Instalar con `pip` sin entorno virtual. Funciona hoy y rompe el mes\n"
            "  que viene, cuando otro proyecto necesite otra version.\n"
            "- Poner los `import` en mitad del archivo. Van arriba, todos juntos:\n"
            "  asi se ve de un vistazo de que depende el modulo.\n\n"
            "## Resumen\n"
            "- Un modulo es un archivo `.py`; `import modulo` lo trae entero y\n"
            "  `from modulo import nombre` trae una pieza.\n"
            "- `import modulo as alias` renombra; los import van arriba.\n"
            "- `sys.path` es donde Python busca, y `sys.modules` es lo que ya\n"
            "  tiene cargado (y cachea).\n"
            "- Un paquete es una carpeta con `__init__.py`, y se importa como\n"
            "  `paquete.modulo`.\n"
            "- `__name__` vale `'__main__'` solo si ejecutas el archivo\n"
            "  directamente; por eso el guard protege el codigo de prueba.\n"
            "- Un entorno virtual (`python -m venv .venv`) aisla las dependencias\n"
            "  del proyecto, y `requirements.txt` las deja reproducibles.\n"
        ),
        difficulty="advanced",
        category="tooling",
        order=9,
        estimated_duration=50,
        prerequisites_titles=["POO en Python"],
        exercises=[
            ExerciseTemplate(
                title="Importar de la libreria estandar",
                description="Usar un modulo que ya viene con Python.",
                instructions=(
                    "Importa el modulo `math` y guarda:\n\n"
                    "- `raiz`: la raiz cuadrada de 144 con `math.sqrt`.\n"
                    "- `entero`: el 7.9 redondeado hacia abajo con `math.floor`.\n\n"
                    "Despues imprime los dos, en ese orden y uno por linea."
                ),
                starter_code="# TODO: importa math y calcula raiz y entero\n",
                hints=[
                    "El import va en la primera linea: import math.",
                    "raiz = math.sqrt(144) y entero = math.floor(7.9).",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "raiz y entero salen de math",
                        "code": (
                            "assert raiz == 12.0, f'raiz vale {raiz!r}'\n"
                            "assert entero == 7, f'entero vale {entero!r}'"
                        ),
                    },
                    {
                        "name": "se importo el modulo, no se escribio el numero",
                        "code": (
                            "import types\n"
                            "assert isinstance(math, types.ModuleType), "
                            "'falta el import math'\n"
                            "assert raiz == math.sqrt(144) and entero == math.floor(7.9)"
                        ),
                    },
                    {
                        "name": "imprime los dos valores",
                        "code": (
                            "lineas = [l for l in _salida.strip().split(chr(10)) if l.strip()]\n"
                            "assert lineas == ['12.0', '7'], f'salio {lineas}'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="from, import y alias",
                description="Las otras dos formas de importar.",
                instructions=(
                    "Sin usar `import math` a secas:\n\n"
                    "- trae solo `pi` con `from math import pi` y guarda en "
                    "`area` el area de un circulo de radio 2 (`pi * radio ** 2`), "
                    "redondeada a 2 decimales;\n"
                    "- importa `json` con el alias `j` y guarda en `texto` el "
                    "resultado de `j.dumps({'ok': True})`.\n\n"
                    "Imprime `area` y `texto`, uno por linea."
                ),
                starter_code="radio = 2\n# TODO: los dos imports, area y texto\n",
                hints=[
                    "from math import pi trae el nombre pi directamente, sin math. delante.",
                    "area = round(pi * radio ** 2, 2)",
                    "import json as j, y despues texto = j.dumps({'ok': True}).",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "el area usa pi y sale redondeada",
                        "code": (
                            "assert area == 12.57, f'area vale {area!r}'\n"
                            "from math import pi as _pi\n"
                            "assert area == round(_pi * radio ** 2, 2)"
                        ),
                    },
                    {
                        "name": "pi entro por from ... import",
                        "code": (
                            "assert 'pi' in globals(), "
                            "'usa from math import pi: el nombre pi tiene que quedar disponible'"
                        ),
                    },
                    {
                        "name": "json entro con alias y produjo el texto",
                        "code": (
                            "import types\n"
                            "assert isinstance(j, types.ModuleType), "
                            "'falta import json as j'\n"
                            "assert texto == '{\"ok\": true}', f'texto vale {texto!r}'"
                        ),
                    },
                    {
                        "name": "imprime los dos, en orden",
                        "code": (
                            "lineas = [l for l in _salida.strip().split(chr(10)) if l.strip()]\n"
                            "assert lineas == ['12.57', '{\"ok\": true}'], f'salio {lineas}'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Tu primer modulo",
                description="Escribir un archivo .py y usarlo desde otro.",
                instructions=(
                    "Escribe un modulo `saludos.py` que contenga UNA funcion, "
                    "`hola(nombre)`, que devuelva `Hola, <nombre>!`.\n\n"
                    "El starter ya prepara el terreno (borra el cache y anade la "
                    "carpeta a `sys.path`): tu pones el contenido del archivo y el "
                    "`import saludos` al final. Despues imprime "
                    "`saludos.hola('Ana')`.\n\n"
                    "La funcion tiene que vivir dentro de `saludos.py`, no aqui."
                ),
                starter_code=(
                    "from pathlib import Path\n"
                    "import sys\n\n"
                    "sys.modules.pop('saludos', None)   # olvida la version anterior\n\n"
                    "Path('saludos.py').write_text(\n"
                    "    # TODO: el contenido del modulo, como texto\n"
                    "    ''\n"
                    ")\n\n"
                    "if '.' not in sys.path:\n"
                    "    sys.path.insert(0, '.')\n\n"
                    "# TODO: importa saludos y usa hola('Ana')\n"
                ),
                hints=[
                    "El contenido es un texto con el codigo dentro: "
                    "\"def hola(nombre):\\n    return f'Hola, {nombre}!'\\n\".",
                    "Cuidado con los saltos de linea (\\n) y con la indentacion de las "
                    "cuatro espacios dentro del texto.",
                    "Al final: import saludos y despues print(saludos.hola('Ana')).",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "saludos.py existe",
                        "code": (
                            "from pathlib import Path\n"
                            "assert Path('saludos.py').exists(), 'no creaste saludos.py'\n"
                            "assert 'def hola' in Path('saludos.py').read_text(), "
                            "'saludos.py esta vacio: el contenido del modulo va dentro del write_text'"
                        ),
                    },
                    {
                        "name": "la funcion vive en el modulo y saluda",
                        "code": (
                            "assert saludos.hola('Ana') == 'Hola, Ana!', "
                            "f\"hola('Ana') devolvio {saludos.hola('Ana')!r}\"\n"
                            "assert saludos.hola('Luis') == 'Hola, Luis!'"
                        ),
                    },
                    {
                        "name": "hola no esta suelta en el archivo principal",
                        "code": (
                            "assert callable(saludos.hola), 'saludos.hola no es una funcion'\n"
                            "assert 'hola' not in globals(), "
                            "'hola tiene que vivir dentro de saludos.py'"
                        ),
                    },
                    {
                        "name": "imprime el saludo",
                        "code": (
                            "assert _salida.strip() == 'Hola, Ana!', "
                            "f'salio {_salida.strip()!r}'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Traer solo una funcion",
                description="from tu_modulo import lo_que_necesitas.",
                instructions=(
                    "Escribe `medidas.py` con dos funciones, `area(base, altura)` "
                    "(base por altura) y `perimetro(base, altura)` (el doble de la "
                    "suma).\n\n"
                    "Despues traelas con `from medidas import area, perimetro` -sin "
                    "`import medidas`- y guarda `a = area(3, 4)` y "
                    "`p = perimetro(3, 4)`."
                ),
                starter_code=(
                    "from pathlib import Path\n"
                    "import sys\n\n"
                    "sys.modules.pop('medidas', None)\n\n"
                    "Path('medidas.py').write_text(\n"
                    "    # TODO: las dos funciones, como texto\n"
                    "    ''\n"
                    ")\n\n"
                    "if '.' not in sys.path:\n"
                    "    sys.path.insert(0, '.')\n\n"
                    "# TODO: from medidas import area, perimetro  y despues a y p\n"
                ),
                hints=[
                    "Las dos funciones van en el mismo texto, separadas por un salto de linea.",
                    "El perimetro es 2 * (base + altura).",
                    "Con from ... import, las funciones quedan disponibles por su nombre: "
                    "area(3, 4), sin medidas. delante.",
                    "a = area(3, 4) y p = perimetro(3, 4).",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "el modulo existe y tiene las dos funciones",
                        "code": (
                            "import importlib\n"
                            "m = importlib.import_module('medidas')\n"
                            "assert m.area(3, 4) == 12, 'area no calcula base por altura'\n"
                            "assert m.perimetro(3, 4) == 14, 'perimetro no es 2 * (base + altura)'"
                        ),
                    },
                    {
                        "name": "los nombres se trajeron con from ... import",
                        "code": (
                            "assert 'area' in globals() and 'perimetro' in globals(), "
                            "'usa from medidas import area, perimetro'\n"
                            "assert callable(area) and callable(perimetro)"
                        ),
                    },
                    {
                        "name": "a y p tienen los valores del enunciado",
                        "code": (
                            "assert a == 12, f'a vale {a!r}'\n"
                            "assert p == 14, f'p vale {p!r}'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Refactor a modulo",
                description="Saca las funciones a su propio modulo y consumelas importandolas.",
                instructions=(
                    "Crea un modulo `utils.py` con dos funciones y usalo desde "
                    "este archivo:\n\n"
                    "- `normalizar(texto)`: devuelve el texto sin espacios a los "
                    "lados y en minusculas.\n"
                    "- `es_valido(texto)`: devuelve True si el texto normalizado "
                    "no esta vacio.\n\n"
                    "Escribe el archivo con `Path('utils.py').write_text(...)`, "
                    "anade `'.'` a `sys.path` e importalo con `import utils`. Las "
                    "funciones deben vivir DENTRO de utils.py: aqui solo se "
                    "importan, no se definen."
                ),
                starter_code=(
                    "from pathlib import Path\n"
                    "import sys\n\n"
                    "# Python cachea en sys.modules los modulos ya importados. Sin\n"
                    "# esta linea, si corriges utils.py y vuelves a ejecutar,\n"
                    "# seguirias usando la version vieja.\n"
                    "sys.modules.pop('utils', None)\n\n"
                    "Path('utils.py').write_text(\n"
                    "    # TODO: el contenido de utils.py, como texto\n"
                    "    ''\n"
                    ")\n\n"
                    "if '.' not in sys.path:\n"
                    "    sys.path.insert(0, '.')\n\n"
                    "import utils\n"
                ),
                hints=[
                    "El contenido de utils.py es un string; cuida los saltos de linea.",
                    "sys.path.insert(0, '.') hace que Python busque modulos en el directorio actual.",
                    "es_valido puede apoyarse en normalizar: las dos viven en el mismo modulo.",
                    "Si editas utils.py y no ves el cambio, es el cache: sys.modules.pop('utils', None).",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "utils.py existe en el sistema de archivos",
                        "code": (
                            "from pathlib import Path\n"
                            "assert Path('utils.py').exists(), 'no creaste el archivo utils.py'\n"
                            "assert 'def normalizar' in Path('utils.py').read_text(), "
                            "'utils.py esta vacio: el codigo va dentro del write_text'"
                        ),
                    },
                    {
                        "name": "utils es un modulo de verdad, cargado desde tu archivo",
                        "code": (
                            "import types\n"
                            "assert isinstance(utils, types.ModuleType), "
                            "'utils deberia ser un modulo importado'\n"
                            "assert utils.__file__.endswith('utils.py'), "
                            "f'utils viene de {utils.__file__}'\n"
                            "assert hasattr(utils, 'normalizar') and hasattr(utils, 'es_valido'), "
                            "'el modulo se importa pero esta vacio'"
                        ),
                    },
                    {
                        "name": "normalizar y es_valido viven dentro del modulo",
                        "code": (
                            "assert utils.normalizar('  HOLA  ') == 'hola'\n"
                            "assert utils.es_valido('x') is True\n"
                            "assert utils.es_valido('   ') is False"
                        ),
                    },
                    {
                        "name": "las funciones NO estan sueltas en el archivo principal",
                        "code": (
                            "assert callable(utils.normalizar), 'utils.normalizar no es una funcion'\n"
                            "assert 'normalizar' not in globals(), "
                            "'normalizar debe vivir en utils.py, no en el archivo principal'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Un paquete de verdad",
                description="El pipeline: una carpeta, __init__.py, dos modulos y sus imports.",
                instructions=(
                    "Monta un paquete llamado `tienda` con esta forma:\n\n"
                    "    tienda/__init__.py    (vacio)\n"
                    "    tienda/precios.py     IVA = 0.21 y con_iva(precio)\n"
                    "    tienda/textos.py      etiqueta(nombre, precio)\n\n"
                    "- `con_iva(precio)`: devuelve el precio con el IVA aplicado, "
                    "redondeado a 2 decimales. Usa la constante `IVA` del propio "
                    "modulo.\n"
                    "- `etiqueta(nombre, precio)`: devuelve el texto "
                    "`<nombre>: <precio> EUR`.\n\n"
                    "Despues importa los dos modulos del paquete, guarda "
                    "`total = precios.con_iva(100)` y "
                    "`linea = textos.etiqueta('mesa', total)`, e imprime `linea`."
                ),
                starter_code=(
                    "from pathlib import Path\n"
                    "import sys\n\n"
                    "for _m in ('tienda', 'tienda.precios', 'tienda.textos'):\n"
                    "    sys.modules.pop(_m, None)   # el cache tambien afecta a los paquetes\n\n"
                    "Path('tienda').mkdir(exist_ok=True)\n"
                    "# TODO: __init__.py, precios.py y textos.py\n\n"
                    "if '.' not in sys.path:\n"
                    "    sys.path.insert(0, '.')\n\n"
                    "# TODO: importa los dos modulos, calcula total y linea, e imprime\n"
                ),
                hints=[
                    "El __init__.py va vacio: Path('tienda/__init__.py').write_text('').",
                    "En precios.py: primero IVA = 0.21 y debajo "
                    "def con_iva(precio): return round(precio * (1 + IVA), 2).",
                    "En textos.py: def etiqueta(nombre, precio): return f'{nombre}: {precio} EUR'.",
                    "Para importarlos: from tienda import precios, textos.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "la carpeta tiene la forma de un paquete",
                        "code": (
                            "from pathlib import Path\n"
                            "assert Path('tienda/__init__.py').exists(), "
                            "'sin __init__.py la carpeta no es un paquete'\n"
                            "assert Path('tienda/precios.py').exists() and "
                            "Path('tienda/textos.py').exists(), 'faltan modulos dentro'"
                        ),
                    },
                    {
                        "name": "precios.con_iva usa la constante IVA del modulo",
                        "code": (
                            "import importlib\n"
                            "p = importlib.import_module('tienda.precios')\n"
                            "assert p.IVA == 0.21, f'IVA vale {p.IVA!r}'\n"
                            "assert p.con_iva(100) == 121.0, f'con_iva(100) dio {p.con_iva(100)!r}'\n"
                            "assert p.con_iva(9.99) == 12.09, f'con_iva(9.99) dio {p.con_iva(9.99)!r}'"
                        ),
                    },
                    {
                        "name": "textos.etiqueta arma la linea",
                        "code": (
                            "import importlib\n"
                            "t = importlib.import_module('tienda.textos')\n"
                            "assert t.etiqueta('mesa', 121.0) == 'mesa: 121.0 EUR', "
                            "f\"devolvio {t.etiqueta('mesa', 121.0)!r}\""
                        ),
                    },
                    {
                        "name": "total y linea salen de los modulos del paquete",
                        "code": (
                            "assert total == 121.0, f'total vale {total!r}'\n"
                            "assert linea == 'mesa: 121.0 EUR', f'linea vale {linea!r}'"
                        ),
                    },
                    {
                        "name": "imprime la etiqueta",
                        "code": (
                            "assert _salida.strip() == 'mesa: 121.0 EUR', "
                            "f'salio {_salida.strip()!r}'"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Testing con pytest",
        description=(
            "Escribir pruebas que de verdad detecten bugs: assert, casos borde, "
            "pytest.raises y como saber si un test sirve para algo."
        ),
        content=(
            "## Por que escribir tests\n"
            "Un test no esta para demostrar que tu codigo funciona hoy: esta para\n"
            "que puedas **cambiarlo manana sin miedo**. Sin tests, tocar una\n"
            "funcion que ya funcionaba es una apuesta; con tests, el programa te\n"
            "avisa en dos segundos de lo que has roto. Es la diferencia entre un\n"
            "proyecto que crece y uno que se congela porque nadie se atreve a\n"
            "tocarlo.\n\n"
            "## Un test es una funcion que afirma\n"
            "```python\n"
            "def doble(n):                 # la funcion que queremos probar\n"
            "    return n * 2\n\n"
            "def test_doble():             # por convencion, el nombre empieza por test_\n"
            "    assert doble(3) == 6      # si la afirmacion es falsa, el test falla\n"
            "    assert doble(0) == 0      # varios asserts en el mismo test: perfecto\n\n"
            "test_doble()                  # aqui lo llamamos a mano...\n"
            "print('paso')                 # paso  -> si llega aqui, no salto ningun assert\n"
            "```\n"
            "En un proyecto de verdad no los llamas tu: `pytest` recorre los\n"
            "archivos, encuentra las funciones que empiezan por `test_` y las\n"
            "ejecuta todas. En este editor no hay terminal, asi que los llamamos a\n"
            "mano; lo que escribes es exactamente igual.\n\n"
            "## assert, y el mensaje que te ahorra el rato\n"
            "```python\n"
            "valor = 5                            # el dato que vamos a afirmar\n"
            "assert valor == 5                    # pasa en silencio: no imprime nada\n\n"
            "try:                                 # solo para poder ensenar el fallo\n"
            "    assert valor == 6, f'valor era {valor}'   # el mensaje explica el fallo\n"
            "except AssertionError as e:\n"
            "    print('fallo:', e)               # fallo: valor era 5\n"
            "```\n"
            "`assert condicion, mensaje` es todo lo que hace falta. El mensaje es\n"
            "opcional pero se agradece: cuando un test falla dentro de seis meses,\n"
            "`valor era 5` te dice mas que un `AssertionError` pelado.\n\n"
            "## Casos borde: donde se rompen los programas\n"
            "```python\n"
            "def descuento(precio, pct):          # el codigo a probar\n"
            "    return precio * (100 - pct) / 100\n\n"
            "def test_descuento():                # un test, tres casos\n"
            "    assert descuento(100, 10) == 90.0    # el caso normal\n"
            "    assert descuento(100, 0) == 100.0    # borde: sin descuento\n"
            "    assert descuento(100, 100) == 0.0    # borde: todo gratis\n\n"
            "test_descuento()                     # si algun assert falla, salta aqui\n"
            "print('paso')                            # paso\n"
            "```\n"
            "El caso normal casi nunca es el que falla. Los que fallan son el\n"
            "cero, la lista vacia, el numero negativo, el maximo y el minimo. Al\n"
            "escribir un test, la pregunta util es *cual es el valor mas raro que\n"
            "esto puede recibir*.\n\n"
            "## pytest.raises: comprobar que algo falla\n"
            "A veces lo correcto **es** fallar: si le pides la raiz de un\n"
            "negativo, quieres un error, no un resultado inventado.\n"
            "```python\n"
            "import pytest                         # raises vive en pytest\n\n"
            "def raiz(n):\n"
            "    if n < 0:                         # el caso que no aceptamos\n"
            "        raise ValueError('no hay raiz real de un negativo')\n"
            "    return n ** 0.5                   # y el que si\n\n"
            "def test_raiz_negativa():             # probamos que falle como debe\n"
            "    with pytest.raises(ValueError):   # este bloque DEBE lanzar ese error\n"
            "        raiz(-1)                      # si no lanza, el test falla\n\n"
            "test_raiz_negativa()                  # pasa: raiz(-1) lanzo ValueError\n"
            "print('paso')                         # paso\n"
            "```\n"
            "Sin `pytest.raises` tendrias que montar un `try/except` con un `else`\n"
            "que lance `AssertionError`. Hace lo mismo, en una linea y leyendose.\n\n"
            "## Un test que no puede fallar no sirve de nada\n"
            "```python\n"
            "def suma(a, b):                # la funcion, correcta\n"
            "    return a + b\n\n"
            "def test_flojo():              # el test, inutil\n"
            "    suma(2, 3)                 # llama, pero no afirma nada: pasa SIEMPRE\n\n"
            "def test_bueno():              # el test, util\n"
            "    assert suma(2, 3) == 5     # este si se entera si suma se rompe\n\n"
            "test_flojo()                   # pasa\n"
            "test_bueno()                   # pasa, pero por un motivo distinto\n"
            "print('los dos pasan')         # los dos pasan  <- y uno de ellos miente\n"
            "```\n"
            "La forma de saber si un test sirve es **romper la funcion a\n"
            "proposito** y comprobar que el test se entera. Si sigue pasando, el\n"
            "test no comprueba nada. Eso tiene nombre -*mutation testing*- y es\n"
            "exactamente lo que hacen los tests ocultos de esta leccion con tu\n"
            "codigo.\n\n"
            "## Como se organiza en un proyecto de verdad\n"
            "Los tests viven en archivos `test_*.py`, al lado del codigo o en una\n"
            "carpeta `tests/`, y se lanzan con `pytest -q` desde la terminal.\n"
            "Cuando el mismo test se repite con datos distintos, se parametriza:\n"
            "```python\n"
            "import pytest\n\n"
            "@pytest.mark.parametrize('entrada,esperado', [(1, 2), (0, 0), (-3, -6)])   # tres pares de datos\n"
            "def test_doble_param(entrada, esperado):   # pytest lo corre 3 veces\n"
            "    assert entrada * 2 == esperado         # una por cada par de la lista\n"
            "```\n"
            "> **Nota honesta sobre el editor**: este es de los pocos ejemplos que\n"
            "> aqui no puedes ejecutar. Un test parametrizado no se puede llamar a\n"
            "> mano -le faltan los argumentos que le inyecta pytest-, y en este\n"
            "> sandbox no hay terminal donde correr `pytest -q`. Se ensena porque\n"
            "> lo vas a ver en cualquier proyecto real, pero los ejercicios de\n"
            "> abajo usan tests normales.\n\n"
            "## Errores comunes\n"
            "- Un test sin `assert`. Llama a la funcion, no comprueba nada y pasa\n"
            "  siempre. Es peor que no tener test: da confianza falsa.\n"
            "- Probar solo el caso bonito. `sumar(2, 3)` funciona en todas las\n"
            "  implementaciones rotas imaginables; el cero y los negativos no.\n"
            "- Comprobar un error con `try/except` y olvidar el `else`. Si la\n"
            "  funcion **no** lanza, el `except` no entra y el test pasa igual.\n"
            "  Por eso existe `pytest.raises`.\n"
            "- Que un test dependa de otro (o del orden). Cada test se levanta\n"
            "  solo: si necesita datos, se los prepara el.\n"
            "- Tests que repiten el bug del codigo. Si calculas el resultado\n"
            "  esperado con la misma formula que usa la funcion, el test aprueba\n"
            "  la formula equivocada. Los numeros esperados se escriben a mano.\n"
            "- No ejecutar nunca el test viendolo fallar. Un test que solo has\n"
            "  visto en verde puede estar comprobando otra cosa.\n\n"
            "## Resumen\n"
            "- Un test es una funcion `test_*` con uno o varios `assert`.\n"
            "- `assert condicion, mensaje` -el mensaje se lee cuando falla.\n"
            "- Los casos borde (cero, vacio, negativo, maximo) son los que pillan\n"
            "  los bugs.\n"
            "- `with pytest.raises(ValueError):` comprueba que algo falla como\n"
            "  debe.\n"
            "- Un test que pasa aunque rompas la funcion no comprueba nada:\n"
            "  rompela a proposito para saberlo.\n"
            "- En un proyecto real, archivos `test_*.py`, `pytest -q`, y\n"
            "  `@pytest.mark.parametrize` para repetir el mismo test con datos\n"
            "  distintos.\n"
        ),
        difficulty="advanced",
        category="testing",
        order=10,
        estimated_duration=55,
        prerequisites_titles=["Modulos, Paquetes y Entornos"],
        exercises=[
            ExerciseTemplate(
                title="Tu primer test",
                description="Una funcion que ya funciona y un test que lo comprueba.",
                instructions=(
                    "`triple(n)` ya esta escrita. Escribe `test_triple()` con "
                    "**dos** asserts -uno con un numero cualquiera y otro con el "
                    "0- y llamalo al final para verlo pasar.\n\n"
                    "Los tests ocultos van a romper `triple` a proposito: si tu "
                    "test no se entera, no cuenta."
                ),
                starter_code=(
                    "def triple(n):\n"
                    "    return n * 3\n\n\n"
                    "def test_triple():\n"
                    "    # TODO: dos asserts sobre triple, uno de ellos con el 0\n"
                    "    ...\n\n\n"
                    "# TODO: llama a test_triple()\n"
                ),
                hints=[
                    "Un assert compara el resultado con el numero que esperas: "
                    "assert triple(2) == 6.",
                    "El otro es el caso del cero: assert triple(0) == 0.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "test_triple existe y pasa",
                        "code": (
                            "assert callable(test_triple), 'falta la funcion test_triple'\n"
                            "import dis\n"
                            "def _comprueba_algo(f):\n"
                            "    ops = {i.opname for i in dis.get_instructions(f)}\n"
                            "    return 'LOAD_ASSERTION_ERROR' in ops or 'BEFORE_WITH' in ops\n"
                            "assert _comprueba_algo(test_triple), "
                            "'test_triple no comprueba nada: le falta el assert'\n"
                            "test_triple()"
                        ),
                    },
                    {
                        "name": "tu test detecta que triple se rompa",
                        "code": (
                            "def triple(n):\n"
                            "    return 0\n"
                            "try:\n"
                            "    test_triple()\n"
                            "except BaseException:\n"
                            "    pass\n"
                            "else:\n"
                            "    raise AssertionError('test_triple pasa aunque triple "
                            "devuelva siempre 0: no comprueba nada')"
                        ),
                    },
                    {
                        "name": "tu test tambien cubre el caso del cero",
                        "code": (
                            "def triple(n):\n"
                            "    return n * 3 if n != 0 else 99\n"
                            "try:\n"
                            "    test_triple()\n"
                            "except BaseException:\n"
                            "    pass\n"
                            "else:\n"
                            "    raise AssertionError('test_triple pasa con una triple "
                            "que devuelve 99 para el 0: falta el assert del cero')"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Casos borde",
                description="El cero y los negativos son los que pillan los bugs.",
                instructions=(
                    "`es_par(n)` ya esta escrita y es correcta. Escribe "
                    "`test_es_par()` que la compruebe **incluyendo el cero y "
                    "algun negativo**, y llamalo.\n\n"
                    "Los tests ocultos la van a sustituir por una version que "
                    "solo acierta con los positivos. Si tu test solo prueba 2 y "
                    "3, no lo vas a pillar."
                ),
                starter_code=(
                    "def es_par(n):\n"
                    "    return n % 2 == 0\n\n\n"
                    "def test_es_par():\n"
                    "    # TODO: casos normales, el cero y algun negativo\n"
                    "    ...\n\n\n"
                    "# TODO: llama a test_es_par()\n"
                ),
                hints=[
                    "es_par(4) es True y es_par(7) es False.",
                    "El cero es par: assert es_par(0) is True.",
                    "Y los negativos tambien cuentan: es_par(-2) es True.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "test_es_par existe y pasa",
                        "code": (
                            "assert callable(test_es_par), 'falta la funcion test_es_par'\n"
                            "import dis\n"
                            "def _comprueba_algo(f):\n"
                            "    ops = {i.opname for i in dis.get_instructions(f)}\n"
                            "    return 'LOAD_ASSERTION_ERROR' in ops or 'BEFORE_WITH' in ops\n"
                            "assert _comprueba_algo(test_es_par), "
                            "'test_es_par no comprueba nada: le falta el assert'\n"
                            "test_es_par()"
                        ),
                    },
                    {
                        "name": "tu test pilla la version que falla con el cero y los negativos",
                        "code": (
                            "def es_par(n):\n"
                            "    return n > 0 and n % 2 == 0\n"
                            "try:\n"
                            "    test_es_par()\n"
                            "except BaseException:\n"
                            "    pass\n"
                            "else:\n"
                            "    raise AssertionError('tu test pasa con una es_par que "
                            "falla en el 0 y en los negativos: prueba esos casos')"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Comprobar que falla",
                description="pytest.raises para los casos en los que lo correcto es un error.",
                instructions=(
                    "`edad_valida(edad)` devuelve la edad si esta entre 0 y 120, y "
                    "lanza `ValueError` si no.\n\n"
                    "Escribe dos tests y llamalos:\n\n"
                    "- `test_edad_valida()`: comprueba con asserts que las edades "
                    "buenas se devuelven tal cual.\n"
                    "- `test_edad_invalida()`: comprueba con "
                    "`with pytest.raises(ValueError):` que una edad de -1 lanza el "
                    "error."
                ),
                starter_code=(
                    "import pytest\n\n\n"
                    "def edad_valida(edad):\n"
                    "    if edad < 0 or edad > 120:\n"
                    "        raise ValueError('edad fuera de rango')\n"
                    "    return edad\n\n\n"
                    "def test_edad_valida():\n"
                    "    ...\n\n\n"
                    "def test_edad_invalida():\n"
                    "    ...\n\n\n"
                    "# TODO: llama a los dos tests\n"
                ),
                hints=[
                    "El primero es un assert normal: assert edad_valida(30) == 30.",
                    "Prueba tambien los bordes que SI valen: 0 y 120.",
                    "El segundo lleva dentro:\n"
                    "    with pytest.raises(ValueError):\n"
                    "        edad_valida(-1)",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "los dos tests existen y pasan",
                        "code": (
                            "assert callable(test_edad_valida) and callable(test_edad_invalida), "
                            "'faltan tests'\n"
                            "import dis\n"
                            "def _comprueba_algo(f):\n"
                            "    ops = {i.opname for i in dis.get_instructions(f)}\n"
                            "    return 'LOAD_ASSERTION_ERROR' in ops or 'BEFORE_WITH' in ops\n"
                            "assert _comprueba_algo(test_edad_valida), "
                            "'test_edad_valida no comprueba nada: le falta el assert'\n"
                            "assert _comprueba_algo(test_edad_invalida), "
                            "'test_edad_invalida no comprueba nada: usa with pytest.raises'\n"
                            "test_edad_valida()\n"
                            "test_edad_invalida()"
                        ),
                    },
                    {
                        "name": "test_edad_valida se entera si deja de devolver la edad",
                        "code": (
                            "def edad_valida(edad):\n"
                            "    return 0\n"
                            "try:\n"
                            "    test_edad_valida()\n"
                            "except BaseException:\n"
                            "    pass\n"
                            "else:\n"
                            "    raise AssertionError('test_edad_valida pasa aunque la "
                            "funcion devuelva siempre 0')"
                        ),
                    },
                    {
                        "name": "test_edad_invalida se entera si deja de lanzar",
                        "code": (
                            "def edad_valida(edad):\n"
                            "    return edad\n"
                            "try:\n"
                            "    test_edad_invalida()\n"
                            "except BaseException:\n"
                            "    pass\n"
                            "else:\n"
                            "    raise AssertionError('test_edad_invalida pasa aunque la "
                            "funcion ya no lance ValueError: usa pytest.raises')"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="El test manda",
                description="Aqui el test ya esta escrito: la funcion la pones tu.",
                instructions=(
                    "Le damos la vuelta al ejercicio. `test_iniciales()` ya esta "
                    "escrito y no se toca: es la **especificacion** de lo que "
                    "tiene que hacer `iniciales(nombre_completo)`.\n\n"
                    "Leelo, escribe la funcion que lo hace pasar y llama al test "
                    "al final. Asi es como se trabaja cuando el test llega antes "
                    "que el codigo."
                ),
                starter_code=(
                    "def iniciales(nombre_completo):\n"
                    "    # TODO: hazlo pasar\n"
                    "    ...\n\n\n"
                    "def test_iniciales():\n"
                    "    assert iniciales('ana perez') == 'A.P.'\n"
                    "    assert iniciales('  luis  gomez  ') == 'L.G.'\n"
                    "    assert iniciales('Sol') == 'S.'\n\n\n"
                    "# TODO: llama a test_iniciales()\n"
                ),
                hints=[
                    "nombre_completo.split() parte por espacios y se come los de sobra.",
                    "De cada palabra necesitas la primera letra en mayuscula: "
                    "palabra[0].upper().",
                    "Recorre las palabras con un for y ve juntando letra + '.'.",
                    "Con 'Sol' solo hay una palabra, asi que sale 'S.': la misma "
                    "logica sirve, no hace falta un caso aparte.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "el test que te dimos pasa",
                        "code": (
                            "assert callable(test_iniciales), 'no borres test_iniciales'\n"
                            "test_iniciales()"
                        ),
                    },
                    {
                        "name": "la funcion aguanta otros nombres",
                        "code": (
                            "assert iniciales('maria jose ruiz') == 'M.J.R.', "
                            "f\"devolvio {iniciales('maria jose ruiz')!r}\"\n"
                            "assert iniciales('ZOE') == 'Z.', "
                            "f\"devolvio {iniciales('ZOE')!r}\""
                        ),
                    },
                    {
                        "name": "no te saltaste el .strip() implicito de split()",
                        "code": (
                            "assert iniciales('   pedro   luis   ') == 'P.L.', "
                            "'los espacios de sobra no deberian afectar'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Prueba de calculadora",
                description="Escribe las funciones y los tests que las verifican.",
                instructions=(
                    "En el mismo archivo, define la calculadora y sus pruebas.\n\n"
                    "Funciones: `sumar(a, b)`, `restar(a, b)` y `dividir(a, b)`. "
                    "`dividir` debe lanzar `ValueError` si `b` es 0.\n\n"
                    "Tests, con el nombre exacto: `test_sumar`, `test_restar` y "
                    "`test_dividir_por_cero`. Cada uno comprueba su funcion con "
                    "`assert`; para el error usa `pytest.raises(ValueError)`.\n\n"
                    "Ojo: un test que pasa siempre no vale. Los tests ocultos "
                    "rompen tus funciones a proposito y comprueban que TUS tests "
                    "se dan cuenta."
                ),
                starter_code=(
                    "import pytest\n\n\n"
                    "def sumar(a, b):\n"
                    "    ...\n\n\n"
                    "def restar(a, b):\n"
                    "    ...\n\n\n"
                    "def dividir(a, b):\n"
                    "    # lanza ValueError si b == 0\n"
                    "    ...\n\n\n"
                    "def test_sumar():\n"
                    "    ...\n\n\n"
                    "def test_restar():\n"
                    "    ...\n\n\n"
                    "def test_dividir_por_cero():\n"
                    "    # with pytest.raises(ValueError):\n"
                    "    ...\n"
                ),
                hints=[
                    "Un test es una funcion normal que empieza por test_ y usa assert.",
                    "Para comprobar que algo lanza: with pytest.raises(ValueError): dividir(1, 0)",
                    "Si tu test pasa aunque rompas la funcion, es que no comprueba nada.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "las tres funciones se comportan",
                        "code": (
                            "assert sumar(2, 3) == 5, 'sumar(2, 3) deberia dar 5'\n"
                            "assert restar(5, 2) == 3, 'restar(5, 2) deberia dar 3'\n"
                            "assert dividir(6, 3) == 2.0, 'dividir(6, 3) deberia dar 2.0'"
                        ),
                    },
                    {
                        "name": "dividir por cero lanza ValueError",
                        "code": (
                            "try:\n"
                            "    dividir(1, 0)\n"
                            "except ValueError:\n"
                            "    pass\n"
                            "else:\n"
                            "    raise AssertionError('dividir(1, 0) deberia lanzar ValueError')"
                        ),
                    },
                    {
                        "name": "escribiste los tres tests con prefijo test_",
                        "code": (
                            "faltan = [n for n in ('test_sumar', 'test_restar', "
                            "'test_dividir_por_cero') if not callable(globals().get(n))]\n"
                            "assert not faltan, f'faltan estos tests: {faltan}'\n"
                            "import dis\n"
                            "def _comprueba_algo(f):\n"
                            "    ops = {i.opname for i in dis.get_instructions(f)}\n"
                            "    return 'LOAD_ASSERTION_ERROR' in ops or 'BEFORE_WITH' in ops\n"
                            "vacios = [n for n in ('test_sumar', 'test_restar', "
                            "'test_dividir_por_cero') if not _comprueba_algo(globals()[n])]\n"
                            "assert not vacios, f'estos tests no comprueban nada: {vacios}'"
                        ),
                    },
                    {
                        "name": "tus tests pasan con tu implementacion",
                        "code": (
                            "import dis\n"
                            "for _n in ('test_sumar', 'test_restar', 'test_dividir_por_cero'):\n"
                            "    _ops = {i.opname for i in dis.get_instructions(globals()[_n])}\n"
                            "    assert 'LOAD_ASSERTION_ERROR' in _ops or 'BEFORE_WITH' in _ops, \\\n"
                            "        f'{_n} esta vacio'\n"
                            "test_sumar()\n"
                            "test_restar()\n"
                            "test_dividir_por_cero()"
                        ),
                    },
                    {
                        "name": "tu test detecta un bug: sumar rota",
                        "code": (
                            "def sumar(a, b):\n"
                            "    return 0\n"
                            "try:\n"
                            "    test_sumar()\n"
                            "except BaseException:\n"
                            "    pass\n"
                            "else:\n"
                            "    raise AssertionError('test_sumar pasa aunque sumar "
                            "este rota: no comprueba nada')"
                        ),
                    },
                    {
                        "name": "tu test detecta un bug: dividir deja de lanzar",
                        "code": (
                            "def dividir(a, b):\n"
                            "    return 0\n"
                            "try:\n"
                            "    test_dividir_por_cero()\n"
                            "except BaseException:\n"
                            "    pass\n"
                            "else:\n"
                            "    raise AssertionError('test_dividir_por_cero pasa aunque "
                            "dividir ya no lance ValueError')"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="La suite del carrito",
                description="El pipeline: una funcion con validacion y tres tests que la aprietan.",
                instructions=(
                    "Escribe `total(items)`, donde `items` es una lista de pares "
                    "`(precio, cantidad)`:\n\n"
                    "- devuelve la suma de `precio * cantidad` de todos;\n"
                    "- con la lista vacia devuelve 0;\n"
                    "- si alguna cantidad es 0 o negativa, lanza `ValueError`, y "
                    "lo hace **antes** de sumar nada.\n\n"
                    "Y escribe sus tres tests, con estos nombres exactos: "
                    "`test_total`, `test_total_vacio` y `test_total_cantidad_mala` "
                    "(este ultimo con `pytest.raises`). Llamalos al final.\n\n"
                    "Los tests ocultos rompen tu funcion de tres maneras distintas "
                    "y comprueban que cada uno de tus tests pilla la suya."
                ),
                starter_code=(
                    "import pytest\n\n\n"
                    "def total(items):\n"
                    "    # TODO: valida primero, suma despues\n"
                    "    ...\n\n\n"
                    "def test_total():\n"
                    "    ...\n\n\n"
                    "def test_total_vacio():\n"
                    "    ...\n\n\n"
                    "def test_total_cantidad_mala():\n"
                    "    ...\n\n\n"
                    "# TODO: llama a los tres tests\n"
                ),
                hints=[
                    "Recorre con for precio, cantidad in items: y desempaquetas cada par.",
                    "La validacion va en su propio recorrido, antes del que suma: "
                    "asi no dejas medio total calculado.",
                    "test_total puede usar [(10, 2), (5, 3)], que suman 35.",
                    "test_total_cantidad_mala: with pytest.raises(ValueError): "
                    "total([(10, 0)]).",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "total suma, aguanta la lista vacia y valida",
                        "code": (
                            "assert total([(10, 2), (5, 3)]) == 35, "
                            "f'devolvio {total([(10, 2), (5, 3)])!r}'\n"
                            "assert total([]) == 0, f'con lista vacia devolvio {total([])!r}'\n"
                            "try:\n"
                            "    total([(10, 0)])\n"
                            "except ValueError:\n"
                            "    pass\n"
                            "else:\n"
                            "    raise AssertionError('cantidad 0 deberia lanzar ValueError')"
                        ),
                    },
                    {
                        "name": "los tres tests existen y pasan",
                        "code": (
                            "faltan = [n for n in ('test_total', 'test_total_vacio', "
                            "'test_total_cantidad_mala') if not callable(globals().get(n))]\n"
                            "assert not faltan, f'faltan estos tests: {faltan}'\n"
                            "import dis\n"
                            "def _comprueba_algo(f):\n"
                            "    ops = {i.opname for i in dis.get_instructions(f)}\n"
                            "    return 'LOAD_ASSERTION_ERROR' in ops or 'BEFORE_WITH' in ops\n"
                            "vacios = [n for n in ('test_total', 'test_total_vacio', "
                            "'test_total_cantidad_mala') if not _comprueba_algo(globals()[n])]\n"
                            "assert not vacios, f'estos tests no comprueban nada: {vacios}'\n"
                            "test_total()\n"
                            "test_total_vacio()\n"
                            "test_total_cantidad_mala()"
                        ),
                    },
                    {
                        "name": "test_total pilla una suma rota",
                        "code": (
                            "def total(items):\n"
                            "    return 0\n"
                            "try:\n"
                            "    test_total()\n"
                            "except BaseException:\n"
                            "    pass\n"
                            "else:\n"
                            "    raise AssertionError('test_total pasa aunque total "
                            "devuelva siempre 0')"
                        ),
                    },
                    {
                        "name": "test_total_vacio pilla que la lista vacia reviente",
                        "code": (
                            "def total(items):\n"
                            "    return items[0][0] * items[0][1]\n"
                            "try:\n"
                            "    test_total_vacio()\n"
                            "except BaseException:\n"
                            "    pass\n"
                            "else:\n"
                            "    raise AssertionError('test_total_vacio pasa aunque total "
                            "reviente con la lista vacia')"
                        ),
                    },
                    {
                        "name": "test_total_cantidad_mala pilla que deje de validar",
                        "code": (
                            "def total(items):\n"
                            "    suma = 0\n"
                            "    for precio, cantidad in items:\n"
                            "        suma = suma + precio * cantidad\n"
                            "    return suma\n"
                            "try:\n"
                            "    test_total_cantidad_mala()\n"
                            "except BaseException:\n"
                            "    pass\n"
                            "else:\n"
                            "    raise AssertionError('test_total_cantidad_mala pasa aunque "
                            "total ya no valide las cantidades')"
                        ),
                    },
                ],
            ),
        ],
    ),
    # -----------------------------------------------------------------------
    # Track 2 - Data Science Foundations (piloto)
    # -----------------------------------------------------------------------
    LessonTemplate(
        title="NumPy esencial: arrays y broadcasting",
        description="Crear arrays, indexar, hacer slicing y aprovechar broadcasting para operar vectorizado.",
        content=(
            "## Por que NumPy importa\n"
            "Python puro es lento haciendo loops sobre numeros porque cada\n"
            "operacion pasa por el interprete. NumPy guarda los numeros en un\n"
            "buffer contiguo de memoria y opera en bloque con codigo C/Fortran:\n"
            "un loop de 1 millon de sumas pasa de segundos a milisegundos.\n"
            "Toda la pila de Data Science y ML (Pandas, scikit-learn, PyTorch)\n"
            "esta construida encima de arrays NumPy o de sus equivalentes.\n\n"
            "## Crear arrays\n"
            "```python\n"
            "import numpy as np\n\n"
            "a = np.array([1, 2, 3, 4])        # desde lista\n"
            "ceros = np.zeros(5)               # [0. 0. 0. 0. 0.]\n"
            "unos = np.ones((2, 3))            # matriz 2x3 de unos\n"
            "rango = np.arange(0, 10, 2)       # [0 2 4 6 8]\n"
            "lin = np.linspace(0, 1, 5)        # 5 numeros equiespaciados\n"
            "```\n"
            "Cada array tiene **shape** (forma), **dtype** (tipo numerico) y\n"
            "**ndim** (numero de dimensiones). Inspeccionalos con `a.shape`,\n"
            "`a.dtype`, `a.ndim`.\n\n"
            "## Indexacion y slicing\n"
            "```python\n"
            "a = np.array([10, 20, 30, 40, 50])\n"
            "a[0]       # 10\n"
            "a[-1]      # 50\n"
            "a[1:4]     # [20 30 40]  (vista, no copia)\n"
            "a[a > 20]  # [30 40 50]  (mascara booleana)\n"
            "a[[0, 2, 4]]  # [10 30 50] (fancy indexing)\n"
            "```\n"
            "Las **vistas** comparten memoria con el array original: modificar la\n"
            "vista modifica el original. `a[1:4].copy()` te da una copia\n"
            "independiente. En matrices la regla es la misma por eje:\n"
            "`m[1, 2]` es fila 1 columna 2, `m[:, 0]` es la primera columna entera.\n\n"
            "## Broadcasting\n"
            "Operaciones entre arrays de shapes distintas funcionan si las\n"
            "dimensiones son compatibles: NumPy 'estira' la mas pequeña\n"
            "siguiendo la regla **de derecha a izquierda**, las dimensiones\n"
            "deben ser iguales o una de ellas debe ser 1.\n\n"
            "```python\n"
            "matriz = np.array([[1, 2, 3], [4, 5, 6]])  # shape (2, 3)\n"
            "matriz + 10                                # suma 10 a todo\n"
            "matriz + np.array([10, 20, 30])            # suma fila a fila\n"
            "matriz - matriz.mean(axis=0)               # centra por columna\n"
            "```\n"
            "Esto reemplaza loops anidados y deja el codigo legible.\n\n"
            "## Operaciones vectorizadas vs loop Python\n"
            "Cuando alguien escribe `for i in range(n): a[i] = a[i] * 2` en\n"
            "NumPy, esta tirando a la basura todo lo que NumPy ofrece. La\n"
            "forma idiomatica es `a = a * 2`. Lo mismo con condiciones:\n"
            "en vez de un `for` con `if`, usa una mascara booleana:\n\n"
            "```python\n"
            "negativos = a < 0\n"
            "a[negativos] = 0   # ReLU sin loops\n"
            "```\n\n"
            "## Errores comunes\n"
            "- Confundir `a[i, j]` (NumPy multidim) con `a[i][j]` (Python\n"
            "  encadenado): el primero es mas rapido y aplica slicing real.\n"
            "- Modificar una **vista** pensando que es copia: si despues lees\n"
            "  el original encontraras los cambios.\n"
            "- Olvidar el `axis=` en agregados: `mean()` sin axis colapsa a un\n"
            "  escalar; con `axis=0` colapsa filas (devuelve una fila), con\n"
            "  `axis=1` colapsa columnas (devuelve una columna).\n\n"
            "## Resumen\n"
            "- NumPy = memoria contigua + operaciones en C. Velocidad real.\n"
            "- Crea con `array`, `zeros`, `ones`, `arange`, `linspace`.\n"
            "- Indexa con enteros, slices, mascaras booleanas o fancy indexing.\n"
            "- Vectoriza: si vas a escribir un `for` para mutar un array,\n"
            "  primero piensa si broadcasting o una mascara lo hacen mejor.\n"
        ),
        difficulty="intermediate",
        category="numpy",
        order=11,
        track="track-2",
        estimated_duration=45,
        prerequisites_titles=["Comprensiones y Manejo de Errores"],
        exercises=[
            ExerciseTemplate(
                title="Pares hasta 20",
                description="Crea un array con los pares del 0 al 20 inclusive.",
                instructions=(
                    "Define `pares` como un array NumPy de los enteros pares desde 0 "
                    "hasta 20 inclusive. Usa `np.arange` con el paso adecuado en una "
                    "sola linea. No uses loops."
                ),
                starter_code=(
                    "import numpy as np\n\n" "# Define `pares` aqui:\n" "pares = None\n"
                ),
                hints=[
                    "np.arange(start, stop, step) -- stop es exclusivo, asi que apunta a 21.",
                    "Los pares empiezan en 0 y van de 2 en 2.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "es un ndarray de NumPy",
                        "code": (
                            "import numpy as np\n"
                            "assert isinstance(pares, np.ndarray), "
                            "'pares debe ser np.ndarray'"
                        ),
                    },
                    {
                        "name": "contiene los pares de 0 a 20",
                        "code": (
                            "import numpy as np\n"
                            "assert np.array_equal(pares, np.arange(0, 21, 2))"
                        ),
                    },
                    {
                        "name": "tiene 11 elementos",
                        "code": "assert len(pares) == 11",
                    },
                ],
            ),
            ExerciseTemplate(
                title="Centrar una matriz por columna",
                description="Resta a cada columna su media para que cada columna quede con media cero.",
                instructions=(
                    "Implementa `centrar(matriz)` que recibe un array 2D y devuelve "
                    "una matriz del mismo shape donde a cada columna se le resto su "
                    "media. Usa broadcasting, no loops."
                ),
                starter_code=(
                    "import numpy as np\n\n"
                    "def centrar(matriz: np.ndarray) -> np.ndarray:\n"
                    "    # TODO: calcula la media por columna y restala usando broadcasting.\n"
                    "    pass\n"
                ),
                hints=[
                    "matriz.mean(axis=0) te da un vector con la media de cada columna.",
                    "Restar ese vector a la matriz aprovecha broadcasting fila por fila.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "preserva el shape original",
                        "code": (
                            "import numpy as np\n"
                            "m = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])\n"
                            "assert centrar(m).shape == (3, 2)"
                        ),
                    },
                    {
                        "name": "deja media cero por columna",
                        "code": (
                            "import numpy as np\n"
                            "m = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])\n"
                            "assert np.allclose(centrar(m).mean(axis=0), 0)"
                        ),
                    },
                    {
                        "name": "matriz constante queda en ceros",
                        "code": (
                            "import numpy as np\n"
                            "m = np.full((4, 3), 7.0)\n"
                            "assert np.allclose(centrar(m), 0)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="ReLU sin loops",
                description="Aplica una mascara booleana para poner en cero los valores negativos.",
                instructions=(
                    "Implementa `relu(arr)` que recibe un array NumPy de cualquier "
                    "shape y devuelve un array del mismo shape donde los valores "
                    "negativos quedan en 0 y los positivos se preservan. No uses "
                    "loops ni list comprehensions; usa indexacion booleana o "
                    "`np.maximum`."
                ),
                starter_code=(
                    "import numpy as np\n\n"
                    "def relu(arr: np.ndarray) -> np.ndarray:\n"
                    "    # TODO: devolver una copia con los negativos en 0.\n"
                    "    pass\n"
                ),
                hints=[
                    "Una opcion: out = arr.copy(); out[out < 0] = 0; return out",
                    "Otra opcion mas idiomatica: np.maximum(arr, 0)",
                    "No mutes el array de entrada; haz copia o crea uno nuevo.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "preserva el shape",
                        "code": (
                            "import numpy as np\n"
                            "x = np.array([[-1.0, 2.0, -3.0], [4.0, -5.0, 6.0]])\n"
                            "assert relu(x).shape == x.shape"
                        ),
                    },
                    {
                        "name": "no quedan negativos",
                        "code": (
                            "import numpy as np\n"
                            "x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])\n"
                            "assert (relu(x) >= 0).all()"
                        ),
                    },
                    {
                        "name": "valores positivos quedan iguales",
                        "code": (
                            "import numpy as np\n"
                            "x = np.array([-2.0, 5.0, -1.0, 7.0])\n"
                            "out = relu(x)\n"
                            "assert out[1] == 5.0 and out[3] == 7.0"
                        ),
                    },
                    {
                        "name": "no muta el array de entrada",
                        "code": (
                            "import numpy as np\n"
                            "x = np.array([-1.0, 2.0, -3.0])\n"
                            "original = x.copy()\n"
                            "out = relu(x)\n"
                            "assert isinstance(out, np.ndarray), 'relu tiene que devolver un array'\n"
                            "assert np.array_equal(x, original), 'relu modifico el array de entrada'"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Pandas esencial: Series, DataFrame e indexing",
        description="Estructuras tabulares con etiquetas: Series, DataFrame, loc/iloc, filtros booleanos y exploracion rapida con head/info/describe.",
        content=(
            "## Por que Pandas\n"
            "NumPy es perfecto para numeros homogeneos en arrays sin etiquetas.\n"
            "El mundo real llega con **columnas heterogeneas** (un string, dos\n"
            "floats, una fecha) y filas que conviene identificar por id o\n"
            "fecha. Pandas envuelve NumPy con dos estructuras etiquetadas:\n"
            "**Series** (1D) y **DataFrame** (2D). Toda la pila de Data\n"
            "Science y casi todo scikit-learn aceptan DataFrames como input.\n\n"
            "## Series — vector con etiquetas\n"
            "```python\n"
            "import pandas as pd\n\n"
            "ventas = pd.Series([120, 80, 95, 200], index=['lun','mar','mie','jue'])\n"
            "ventas['mar']        # 80\n"
            "ventas.mean()        # 123.75\n"
            "ventas > 100         # mascara booleana por dia\n"
            "```\n"
            "Por dentro, `ventas.values` es un array NumPy y `ventas.index`\n"
            "es el indice etiquetado. Las operaciones vectorizadas que viste\n"
            "en NumPy (`* 2`, `+ otra`, broadcasting) funcionan igual.\n\n"
            "## DataFrame — tabla con columnas\n"
            "```python\n"
            "data = {\n"
            "    'nombre': ['Ana','Beto','Carla','David'],\n"
            "    'curso':  ['mate','mate','lengua','lengua'],\n"
            "    'nota':   [4.5, 3.8, 5.0, 2.9],\n"
            "}\n"
            "df = pd.DataFrame(data)\n"
            "```\n"
            "`df` tiene un **indice de filas** (0..3 por defecto), columnas\n"
            "nombradas (`nombre`, `curso`, `nota`) y dtypes por columna\n"
            "(object/float64). Inspeccionalo con:\n\n"
            "```python\n"
            "df.shape       # (4, 3)\n"
            "df.dtypes      # tipo por columna\n"
            "df.head(2)     # primeras 2 filas\n"
            "df.tail()      # ultimas 5 (default)\n"
            "df.info()      # tipos + nulos + memoria\n"
            "df.describe()  # estadisticas de columnas numericas\n"
            "```\n\n"
            "## Indexacion: tres formas (no las mezcles)\n"
            "1. **Por columna** — `df['nota']` devuelve la Serie 'nota'.\n"
            "2. **Por etiqueta** — `df.loc[2, 'nota']` (fila etiqueta 2,\n"
            "   columna 'nota'). Slicing inclusivo: `df.loc[1:3]` trae\n"
            "   filas 1,2,3.\n"
            "3. **Por posicion** — `df.iloc[0, 2]` (primera fila, tercera\n"
            "   columna). Slicing exclusivo: `df.iloc[0:2]` trae 2 filas.\n\n"
            "Si tu indice ya es 0..N-1, `loc` e `iloc` parecen iguales pero\n"
            "dejan de serlo apenas pones `df.set_index('nombre')`.\n\n"
            "## Filtros booleanos\n"
            "```python\n"
            "aprobados = df[df['nota'] >= 4]\n"
            "df[(df['nota'] >= 4) & (df['curso'] == 'mate')]\n"
            "```\n"
            "**Cuidado con `and`/`or`**: en pandas se usan los operadores\n"
            "bit a bit `&` y `|` (con parentesis obligatorios), no las\n"
            "palabras `and`/`or`. Confundirlos da un `ValueError`.\n\n"
            "## Cargar desde CSV\n"
            "Lo mas comun en la vida real es leer un archivo:\n"
            "```python\n"
            "df = pd.read_csv('iris.csv')\n"
            "```\n"
            "En PyCode tenes datasets curados accesibles via:\n"
            "```python\n"
            "import pycode\n"
            "df = await pycode.load_dataset('iris')\n"
            "```\n"
            "(el `await` es porque corre en navegador y la red es asincronica)\n\n"
            "## Errores comunes\n"
            "- Mezclar `loc` e `iloc`. Si tu indice es entero pero no es 0..N-1\n"
            "  (porque hiciste `drop` o `query`), `df.loc[0]` puede no existir\n"
            "  aunque la primera fila si.\n"
            "- Usar `and`/`or` en filtros: rompe con\n"
            "  `The truth value of a Series is ambiguous`.\n"
            "- Modificar una vista con `df[df.col > X].col = ...`: pandas avisa con\n"
            "  `SettingWithCopyWarning`. Lo correcto: `df.loc[df.col > X, 'col'] = ...`.\n"
            "- Olvidar que `read_csv` infiere dtypes y a veces convierte tu id\n"
            "  numerico a float si hay un NaN. Mira `df.dtypes` primero.\n\n"
            "## Resumen\n"
            "- Series = vector con etiquetas. DataFrame = tabla con columnas.\n"
            "- Tres indexadores: por columna, `loc` (etiqueta), `iloc` (posicion).\n"
            "- Filtros con `&`/`|` y parentesis.\n"
            "- `head`/`info`/`describe` son tu primer reflejo al recibir un\n"
            "  dataset desconocido.\n"
        ),
        difficulty="intermediate",
        category="pandas",
        order=12,
        track="track-2",
        estimated_duration=50,
        prerequisites_titles=["NumPy esencial: arrays y broadcasting"],
        exercises=[
            ExerciseTemplate(
                title="Series desde diccionario",
                description="Crea una Series de pandas a partir de un dict.",
                instructions=(
                    "Define `ventas` como una `pd.Series` cuyos valores sean "
                    "[120, 80, 95, 200] con indice ['lun','mar','mie','jue']. "
                    "No uses pd.DataFrame; la respuesta es una Series."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "# Define `ventas` aqui:\n"
                    "ventas = None\n"
                ),
                hints=[
                    "pd.Series acepta una lista de valores y un parametro `index=`.",
                    "Tambien podes pasarle un dict directamente: pd.Series({'lun': 120, ...}).",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "es una pandas Series",
                        "code": (
                            "import pandas as pd\n"
                            "assert isinstance(ventas, pd.Series), 'debe ser pd.Series'"
                        ),
                    },
                    {
                        "name": "tiene los 4 valores correctos",
                        "code": ("assert list(ventas.values) == [120, 80, 95, 200]"),
                    },
                    {
                        "name": "indice por dia de la semana",
                        "code": (
                            "assert list(ventas.index) == ['lun','mar','mie','jue']"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Filtrar aprobados",
                description="Funcion que devuelve solo las filas con nota >= 4.",
                instructions=(
                    "Implementa `filtrar_aprobados(df)` que recibe un DataFrame "
                    "con una columna 'nota' y devuelve un DataFrame con solo "
                    "las filas donde nota >= 4. Usa filtro booleano, no loops."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def filtrar_aprobados(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: filtro booleano sobre la columna 'nota'.\n"
                    "    pass\n"
                ),
                hints=[
                    "df[df['nota'] >= 4] devuelve un DataFrame con esas filas.",
                    "Recorda que el indice de las filas se preserva (no se reinicia).",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "devuelve un DataFrame",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'nombre': ['A','B','C'], 'nota': [4.5, 2.9, 5.0]})\n"
                            "out = filtrar_aprobados(df)\n"
                            "assert isinstance(out, pd.DataFrame)"
                        ),
                    },
                    {
                        "name": "no incluye notas menores a 4",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'nombre': ['A','B','C'], 'nota': [4.5, 2.9, 5.0]})\n"
                            "out = filtrar_aprobados(df)\n"
                            "assert (out['nota'] >= 4).all()"
                        ),
                    },
                    {
                        "name": "incluye las notas correctas",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'nombre': ['A','B','C','D'], 'nota': [4.5, 2.9, 5.0, 3.9]})\n"
                            "out = filtrar_aprobados(df)\n"
                            "assert sorted(out['nombre'].tolist()) == ['A','C']"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Promedio por curso (groupby)",
                description="Agrupa por curso y calcula el promedio de notas.",
                instructions=(
                    "Implementa `promedio_por_curso(df)` que devuelve una Series "
                    "donde el indice es el nombre del curso y el valor es el "
                    "promedio de notas en ese curso. Usa groupby + mean, no loops."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def promedio_por_curso(df: pd.DataFrame) -> pd.Series:\n"
                    "    # TODO: df.groupby('curso')['nota'].mean()\n"
                    "    pass\n"
                ),
                hints=[
                    "df.groupby('curso') agrupa por la columna 'curso'.",
                    "['nota'].mean() selecciona la columna y aplica la agregacion.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "devuelve una Series",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'curso': ['mate','mate','lengua','lengua'],\n"
                            "    'nota': [4.5, 3.5, 5.0, 3.0],\n"
                            "})\n"
                            "out = promedio_por_curso(df)\n"
                            "assert isinstance(out, pd.Series)"
                        ),
                    },
                    {
                        "name": "promedio de mate = 4.0, lengua = 4.0",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'curso': ['mate','mate','lengua','lengua'],\n"
                            "    'nota': [4.5, 3.5, 5.0, 3.0],\n"
                            "})\n"
                            "out = promedio_por_curso(df)\n"
                            "assert abs(out['mate'] - 4.0) < 1e-9\n"
                            "assert abs(out['lengua'] - 4.0) < 1e-9"
                        ),
                    },
                    {
                        "name": "funciona con 3 cursos",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'curso': ['a','a','b','c','c','c'],\n"
                            "    'nota': [2.0, 4.0, 5.0, 3.0, 3.0, 3.0],\n"
                            "})\n"
                            "out = promedio_por_curso(df)\n"
                            "assert sorted(out.index.tolist()) == ['a','b','c']\n"
                            "assert abs(out['a'] - 3.0) < 1e-9\n"
                            "assert abs(out['c'] - 3.0) < 1e-9"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Pandas: groupby, agregaciones y pivot",
        description="Agrupacion con multiples claves, agg multi-metrica, transform vs apply, y reshape con pivot_table.",
        content=(
            "## Por que importa\n"
            "El 80% del trabajo de un analista DS es **agrupar y agregar**.\n"
            "Pandas tiene un set de herramientas para hacerlo en una sola\n"
            "linea y de forma vectorizada. Sin esto terminas con loops sobre\n"
            "filas y matas la performance.\n\n"
            "## groupby — el patron split-apply-combine\n"
            "```python\n"
            "import pandas as pd\n\n"
            "df = pd.DataFrame({\n"
            "    'sucursal': ['centro','centro','norte','norte','sur'],\n"
            "    'producto': ['cafe','te','cafe','te','cafe'],\n"
            "    'ingreso':  [120,    80,  90,    70,   60],\n"
            "})\n"
            "df.groupby('sucursal')['ingreso'].sum()\n"
            "# sucursal\n"
            "# centro    200\n"
            "# norte     160\n"
            "# sur        60\n"
            "```\n"
            "El objeto `df.groupby(...)` no calcula nada hasta que aplicas\n"
            "una agregacion (`.sum`, `.mean`, `.count`, etc.).\n\n"
            "## Agrupar por varias columnas\n"
            "```python\n"
            "df.groupby(['sucursal','producto'])['ingreso'].sum()\n"
            "```\n"
            "Devuelve una Serie con **MultiIndex**: cada fila esta indexada\n"
            "por la tupla (sucursal, producto). Para volver a DataFrame\n"
            "plano usa `.reset_index()`.\n\n"
            "## agg — varias metricas a la vez\n"
            "```python\n"
            "df.groupby('sucursal')['ingreso'].agg(['sum','mean','count'])\n"
            "```\n"
            "Devuelve un DataFrame con una columna por metrica. Tambien acepta\n"
            "un dict para metricas por columna:\n"
            "```python\n"
            "df.groupby('sucursal').agg({\n"
            "    'ingreso': 'sum',\n"
            "    'producto': 'nunique',\n"
            "})\n"
            "```\n\n"
            "## transform — agregar al original\n"
            "`groupby().agg(...)` colapsa filas. `transform(...)` devuelve\n"
            "un Series del **mismo largo** que el DataFrame, util para\n"
            "agregar una columna calculada por grupo:\n"
            "```python\n"
            "df['ingreso_total_sucursal'] = df.groupby('sucursal')['ingreso'].transform('sum')\n"
            "```\n"
            "Ahora cada fila tiene el total de su sucursal al lado. Esto\n"
            "permite calcular porcentajes (`fila['ingreso'] / total_sucursal`)\n"
            "sin merge manual.\n\n"
            "## pivot_table — reshape facil\n"
            "Cuando tu data esta en formato 'largo' (cada fila es una observacion)\n"
            "y la queres en formato 'ancho' (filas y columnas con sus combinaciones):\n"
            "```python\n"
            "df.pivot_table(\n"
            "    index='sucursal',\n"
            "    columns='producto',\n"
            "    values='ingreso',\n"
            "    aggfunc='sum',\n"
            "    fill_value=0,\n"
            ")\n"
            "# producto    cafe   te\n"
            "# sucursal\n"
            "# centro       120   80\n"
            "# norte         90   70\n"
            "# sur           60    0\n"
            "```\n"
            "Es el equivalente a una tabla dinamica de Excel pero programable.\n\n"
            "## Errores comunes\n"
            "- Olvidar `reset_index()` despues de un groupby cuando necesitas\n"
            "  pasar el resultado a otra funcion que espera DataFrame plano.\n"
            "- Usar `groupby().apply(lambda x: ...)` para algo que ya hace\n"
            "  `agg` o `transform`. `apply` es la opcion mas lenta y mas\n"
            "  flexible — usala cuando las otras dos no alcancen.\n"
            "- En `pivot_table`, olvidar `fill_value` deja NaN en combinaciones\n"
            "  inexistentes (sur no vendio te → NaN). Casi siempre queres 0.\n"
            "- Confundir `groupby` con `pivot_table`: `groupby` colapsa filas\n"
            "  manteniendo el orden tabular; `pivot_table` reshapea filas a\n"
            "  columnas.\n\n"
            "## Resumen\n"
            "- `groupby` divide en grupos; las agregaciones colapsan filas.\n"
            "- `agg` permite multiples metricas / columnas en una llamada.\n"
            "- `transform` mantiene el largo original — util para columnas\n"
            "  derivadas por grupo.\n"
            "- `pivot_table` reshapea largo → ancho con agregaciones.\n"
        ),
        difficulty="intermediate",
        category="pandas",
        order=13,
        track="track-2",
        estimated_duration=50,
        prerequisites_titles=["Pandas esencial: Series, DataFrame e indexing"],
        exercises=[
            ExerciseTemplate(
                title="Total por sucursal y producto",
                description="Suma de ingresos agrupando por dos columnas.",
                instructions=(
                    "Implementa `total_por_sucursal_producto(df)` que recibe un "
                    "DataFrame con columnas 'sucursal', 'producto' e 'ingreso' "
                    "y devuelve una Series con MultiIndex (sucursal, producto) "
                    "y la suma de ingresos. Usa groupby con lista de columnas."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def total_por_sucursal_producto(df: pd.DataFrame) -> pd.Series:\n"
                    "    # TODO: df.groupby([col1, col2])['ingreso'].sum()\n"
                    "    pass\n"
                ),
                hints=[
                    "groupby acepta una lista de columnas: df.groupby(['sucursal','producto']).",
                    "El resultado es una Series con MultiIndex.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "es una pandas Series",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['centro','centro','norte','norte','sur'],\n"
                            "    'producto':['cafe','te','cafe','te','cafe'],\n"
                            "    'ingreso':[120,80,90,70,60],\n"
                            "})\n"
                            "out = total_por_sucursal_producto(df)\n"
                            "assert isinstance(out, pd.Series)"
                        ),
                    },
                    {
                        "name": "MultiIndex con 2 niveles",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['centro','centro','norte','norte','sur'],\n"
                            "    'producto':['cafe','te','cafe','te','cafe'],\n"
                            "    'ingreso':[120,80,90,70,60],\n"
                            "})\n"
                            "out = total_por_sucursal_producto(df)\n"
                            "assert isinstance(out.index, pd.MultiIndex)\n"
                            "assert out.index.nlevels == 2"
                        ),
                    },
                    {
                        "name": "totales correctos",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['centro','centro','norte','norte','sur'],\n"
                            "    'producto':['cafe','te','cafe','te','cafe'],\n"
                            "    'ingreso':[120,80,90,70,60],\n"
                            "})\n"
                            "out = total_por_sucursal_producto(df)\n"
                            "assert out[('centro','cafe')] == 120\n"
                            "assert out[('centro','te')] == 80\n"
                            "assert out[('sur','cafe')] == 60"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Multiples metricas por sucursal",
                description="Agregar varias estadisticas en una llamada usando agg.",
                instructions=(
                    "Implementa `metricas_sucursal(df)` que devuelve un "
                    "DataFrame indexado por 'sucursal' con tres columnas: "
                    "'total_ingreso' (suma), 'venta_promedio' (mean) y "
                    "'cantidad' (count) de la columna 'ingreso'. Una sola "
                    "llamada con agg + named aggregation."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def metricas_sucursal(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: df.groupby('sucursal').agg(total_ingreso=('ingreso','sum'), ...)\n"
                    "    pass\n"
                ),
                hints=[
                    "Named aggregation: agg(col_nueva=('col_origen','funcion')).",
                    "Devolves un DataFrame con sucursal como indice y las 3 columnas.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "es un DataFrame con las 3 columnas",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['c','c','n','n'],\n"
                            "    'ingreso':[100,50,80,20],\n"
                            "})\n"
                            "out = metricas_sucursal(df)\n"
                            "assert isinstance(out, pd.DataFrame)\n"
                            "assert set(out.columns) == {'total_ingreso','venta_promedio','cantidad'}"
                        ),
                    },
                    {
                        "name": "valores correctos para 2 sucursales",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['c','c','n','n'],\n"
                            "    'ingreso':[100,50,80,20],\n"
                            "})\n"
                            "out = metricas_sucursal(df)\n"
                            "assert out.loc['c','total_ingreso'] == 150\n"
                            "assert out.loc['n','venta_promedio'] == 50\n"
                            "assert out.loc['c','cantidad'] == 2"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Pivot ventas por sucursal y producto",
                description="Reshape de formato largo a ancho con pivot_table.",
                instructions=(
                    "Implementa `pivot_ventas(df)` que devuelve un DataFrame "
                    "con sucursal como indice, producto como columnas, y suma "
                    "de 'ingreso' como valores. Combinaciones inexistentes "
                    "deben quedar en 0, no en NaN."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def pivot_ventas(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: pd.pivot_table(df, index=..., columns=..., values=..., aggfunc='sum', fill_value=0)\n"
                    "    pass\n"
                ),
                hints=[
                    "Usa pd.pivot_table o df.pivot_table — la API es igual.",
                    "fill_value=0 reemplaza los NaN de las combinaciones que no existen.",
                    "aggfunc='sum' especifica que agregamos sumando los ingresos.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "es DataFrame con sucursal de index",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['c','c','n','sur'],\n"
                            "    'producto':['cafe','te','cafe','cafe'],\n"
                            "    'ingreso':[100,50,80,60],\n"
                            "})\n"
                            "out = pivot_ventas(df)\n"
                            "assert isinstance(out, pd.DataFrame)\n"
                            "assert out.index.name == 'sucursal'"
                        ),
                    },
                    {
                        "name": "combinacion inexistente queda en 0 (no NaN)",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['c','c','n','sur'],\n"
                            "    'producto':['cafe','te','cafe','cafe'],\n"
                            "    'ingreso':[100,50,80,60],\n"
                            "})\n"
                            "out = pivot_ventas(df)\n"
                            "# sur no vendio te → debe ser 0, no NaN\n"
                            "assert out.loc['sur','te'] == 0"
                        ),
                    },
                    {
                        "name": "sumas correctas en celdas con datos",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['c','c','c','n'],\n"
                            "    'producto':['cafe','cafe','te','cafe'],\n"
                            "    'ingreso':[100,50,80,90],\n"
                            "})\n"
                            "out = pivot_ventas(df)\n"
                            "# c-cafe = 100 + 50 = 150\n"
                            "assert out.loc['c','cafe'] == 150\n"
                            "assert out.loc['c','te'] == 80\n"
                            "assert out.loc['n','cafe'] == 90"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Pandas: merge, join y fechas",
        description="Unir tablas con merge (inner/left/right/outer), parsear fechas con to_datetime y extraer componentes con el accessor .dt.",
        content=(
            "## Por que merge\n"
            "Casi ningun dataset llega completo. La info que necesitas suele\n"
            "estar **separada en varias tablas** (ventas + productos + clientes)\n"
            "y la juntas por una clave comun. Es la operacion equivalente a un\n"
            "JOIN en SQL, pero sintaxis Python.\n\n"
            "## merge basico\n"
            "```python\n"
            "import pandas as pd\n\n"
            "ventas = pd.DataFrame({\n"
            "    'producto_id': [1, 2, 1, 3],\n"
            "    'unidades':    [5, 2, 3, 1],\n"
            "})\n"
            "productos = pd.DataFrame({\n"
            "    'producto_id': [1, 2, 3, 4],\n"
            "    'nombre':      ['cafe','te','torta','sandwich'],\n"
            "    'precio':      [3.5, 2.5, 4.5, 6.0],\n"
            "})\n\n"
            "df = ventas.merge(productos, on='producto_id')\n"
            "```\n"
            "Por defecto, `merge` hace un **inner join**: solo filas con clave\n"
            "presente en ambas tablas. Los `producto_id=4` (sandwich) y filas\n"
            "huerfanas en ventas desaparecen.\n\n"
            "## El parametro how — controla el tipo de join\n"
            "```python\n"
            "# Quiero TODAS las ventas, aunque el producto no exista en el catalogo\n"
            "ventas.merge(productos, on='producto_id', how='left')\n\n"
            "# Quiero TODOS los productos, aunque no se hayan vendido\n"
            "ventas.merge(productos, on='producto_id', how='right')\n\n"
            "# Quiero TODO (ventas huerfanas + productos sin ventas)\n"
            "ventas.merge(productos, on='producto_id', how='outer')\n"
            "```\n"
            "Las filas sin match del otro lado quedan con NaN en las columnas\n"
            "que aporta la tabla ausente.\n\n"
            "## Claves con nombres distintos\n"
            "Cuando las columnas se llaman distinto en cada tabla, usa\n"
            "`left_on` y `right_on`:\n"
            "```python\n"
            "ventas.merge(productos, left_on='producto_id', right_on='id')\n"
            "```\n\n"
            "## pd.to_datetime — parsear fechas en serio\n"
            "Pandas no infiere fechas por defecto: una columna `'2026-06-14'`\n"
            "queda como `object` (string). Convertir explicitamente:\n"
            "```python\n"
            "df['fecha'] = pd.to_datetime(df['fecha'])  # detecta el formato\n"
            "df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y')  # explicit\n"
            "```\n"
            "Despues de esto, `df['fecha'].dtype` es `datetime64[ns]` y\n"
            "podes hacer aritmetica de fechas y comparaciones.\n\n"
            "## El accessor .dt — extraer componentes\n"
            "Sobre una columna datetime, `.dt` expone propiedades:\n"
            "```python\n"
            "df['mes'] = df['fecha'].dt.month        # 1..12\n"
            "df['dia_semana'] = df['fecha'].dt.day_name()  # 'Monday', ...\n"
            "df['anio'] = df['fecha'].dt.year\n"
            "df['es_fin_de_semana'] = df['fecha'].dt.dayofweek >= 5\n"
            "```\n\n"
            "## resample — agregar por ventana temporal\n"
            "Si la fecha es indice del DataFrame, `resample(...)` agrupa por\n"
            "ventana de tiempo (similar a `groupby` pero para series temporales):\n"
            "```python\n"
            "df2 = df.set_index('fecha')\n"
            "df2['ingreso'].resample('W').sum()  # suma por semana\n"
            "df2['ingreso'].resample('M').mean() # promedio por mes\n"
            "```\n\n"
            "## Errores comunes\n"
            "- Hacer merge sin especificar `on=`: pandas adivina por columnas\n"
            "  con el mismo nombre, lo que puede mezclar columnas\n"
            "  irrelevantes (`fecha` por ejemplo) o fallar silenciosamente.\n"
            "  **Siempre se explicito con `on=` o `left_on/right_on`**.\n"
            "- Olvidar `how=` cuando queres preservar filas sin match: te\n"
            "  perdes data sin darte cuenta.\n"
            "- Hacer `.dt.year` sobre una columna que sigue siendo string:\n"
            "  da AttributeError. Llamar `pd.to_datetime` primero.\n"
            "- Mergear con duplicados en la clave: el resultado tiene\n"
            "  **producto cartesiano** de los duplicados — el numero de filas\n"
            "  explota. Revisa `df['clave'].duplicated().sum()` antes.\n\n"
            "## Resumen\n"
            "- `merge(on=, how=)` une tablas; inner es default. Usa left/right/\n"
            "  outer cuando necesitas preservar filas sin match.\n"
            "- `pd.to_datetime` antes de operar sobre fechas. Sin esto, son strings.\n"
            "- `.dt` expone month/year/day_name/dayofweek/... sobre columnas datetime.\n"
            "- `resample` agrega por ventana temporal cuando el indice es datetime.\n"
        ),
        difficulty="intermediate",
        category="pandas",
        order=14,
        track="track-2",
        estimated_duration=55,
        prerequisites_titles=["Pandas: groupby, agregaciones y pivot"],
        exercises=[
            ExerciseTemplate(
                title="Join ventas con catalogo (inner)",
                description="Unir dos DataFrames por producto_id con inner join.",
                instructions=(
                    "Implementa `unir_con_catalogo(ventas, productos)` que "
                    "merge ventas con productos por 'producto_id' con inner join. "
                    "Devuelve el DataFrame combinado."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def unir_con_catalogo(ventas: pd.DataFrame, productos: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: merge por 'producto_id', how='inner'.\n"
                    "    pass\n"
                ),
                hints=[
                    "ventas.merge(productos, on='producto_id') hace inner por defecto.",
                    "Las filas sin match en ambas tablas desaparecen.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "devuelve un DataFrame",
                        "code": (
                            "import pandas as pd\n"
                            "v = pd.DataFrame({'producto_id':[1,2,1], 'unidades':[5,2,3]})\n"
                            "p = pd.DataFrame({'producto_id':[1,2], 'nombre':['cafe','te']})\n"
                            "out = unir_con_catalogo(v, p)\n"
                            "assert isinstance(out, pd.DataFrame)"
                        ),
                    },
                    {
                        "name": "incluye la columna 'nombre' del catalogo",
                        "code": (
                            "import pandas as pd\n"
                            "v = pd.DataFrame({'producto_id':[1,2,1], 'unidades':[5,2,3]})\n"
                            "p = pd.DataFrame({'producto_id':[1,2], 'nombre':['cafe','te']})\n"
                            "out = unir_con_catalogo(v, p)\n"
                            "assert 'nombre' in out.columns\n"
                            "assert 'unidades' in out.columns"
                        ),
                    },
                    {
                        "name": "huerfanas en ventas no aparecen (inner)",
                        "code": (
                            "import pandas as pd\n"
                            "v = pd.DataFrame({'producto_id':[1,2,99], 'unidades':[5,2,1]})\n"
                            "p = pd.DataFrame({'producto_id':[1,2], 'nombre':['cafe','te']})\n"
                            "out = unir_con_catalogo(v, p)\n"
                            "assert 99 not in out['producto_id'].tolist()\n"
                            "assert len(out) == 2"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Extraer mes de una fecha",
                description="Parsear fechas y agregar columna con el mes.",
                instructions=(
                    "Implementa `con_mes(df)` que recibe un DataFrame con "
                    "columna 'fecha' (strings tipo '2026-06-14') y devuelve el "
                    "mismo DataFrame con una nueva columna 'mes' (int 1..12). "
                    "No modifiques el DataFrame original — devuelve una copia."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def con_mes(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: copia, parsea fecha con pd.to_datetime, usa .dt.month.\n"
                    "    pass\n"
                ),
                hints=[
                    "df_copy = df.copy() para no mutar el original.",
                    "pd.to_datetime(df_copy['fecha']).dt.month da int 1..12.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "no muta el DataFrame original",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'fecha': ['2026-01-15', '2026-06-30']})\n"
                            "out = con_mes(df)\n"
                            "assert out is not None and 'mes' in out.columns, "
                            "'con_mes tiene que devolver una copia con la columna mes'\n"
                            "assert 'mes' not in df.columns, 'no muta el original'"
                        ),
                    },
                    {
                        "name": "agrega columna mes con valores correctos",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'fecha': ['2026-01-15', '2026-06-30', '2026-12-01']})\n"
                            "out = con_mes(df)\n"
                            "assert 'mes' in out.columns\n"
                            "assert out['mes'].tolist() == [1, 6, 12]"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Ingresos por semana (resample)",
                description="Join + parseo de fechas + resample semanal de ingresos.",
                instructions=(
                    "Implementa `ingresos_semanales(ventas, productos)` que: "
                    "(1) mergea por 'producto_id', (2) calcula 'ingreso' = "
                    "unidades * precio, (3) parsea 'fecha' a datetime, (4) "
                    "devuelve una Serie con la suma de ingresos por semana, "
                    "indexada por fecha de fin de semana. Usa resample('W')."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def ingresos_semanales(ventas: pd.DataFrame, productos: pd.DataFrame) -> pd.Series:\n"
                    "    # TODO: merge, calcular ingreso, to_datetime, set_index, resample('W').sum()\n"
                    "    pass\n"
                ),
                hints=[
                    "df['ingreso'] = df['unidades'] * df['precio'] (vectorizado).",
                    "df = df.set_index('fecha') antes de resamplear.",
                    "df['ingreso'].resample('W').sum() agrupa por semana terminando en domingo.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "devuelve una pandas Series",
                        "code": (
                            "import pandas as pd\n"
                            "v = pd.DataFrame({\n"
                            "    'fecha':['2026-01-05','2026-01-06','2026-01-13'],\n"
                            "    'producto_id':[1,2,1],\n"
                            "    'unidades':[2,3,1],\n"
                            "})\n"
                            "p = pd.DataFrame({'producto_id':[1,2], 'precio':[10.0, 5.0]})\n"
                            "out = ingresos_semanales(v, p)\n"
                            "assert isinstance(out, pd.Series)"
                        ),
                    },
                    {
                        "name": "indice es datetime",
                        "code": (
                            "import pandas as pd\n"
                            "v = pd.DataFrame({\n"
                            "    'fecha':['2026-01-05','2026-01-06','2026-01-13'],\n"
                            "    'producto_id':[1,2,1],\n"
                            "    'unidades':[2,3,1],\n"
                            "})\n"
                            "p = pd.DataFrame({'producto_id':[1,2], 'precio':[10.0, 5.0]})\n"
                            "out = ingresos_semanales(v, p)\n"
                            "assert pd.api.types.is_datetime64_any_dtype(out.index)"
                        ),
                    },
                    {
                        "name": "ingresos sumados correctamente por semana",
                        "code": (
                            "import pandas as pd\n"
                            "# 5-ene (lun) y 6-ene (mar) caen en la misma semana W (term. domingo 11)\n"
                            "# 13-ene (mar) cae en la semana terminando domingo 18\n"
                            "v = pd.DataFrame({\n"
                            "    'fecha':['2026-01-05','2026-01-06','2026-01-13'],\n"
                            "    'producto_id':[1,2,1],\n"
                            "    'unidades':[2,3,1],\n"
                            "})\n"
                            "p = pd.DataFrame({'producto_id':[1,2], 'precio':[10.0, 5.0]})\n"
                            "out = ingresos_semanales(v, p)\n"
                            "# semana 1: 2*10 + 3*5 = 35\n"
                            "# semana 2: 1*10 = 10\n"
                            "assert sorted(out.values.tolist()) == [10.0, 35.0]"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Pandas: limpieza de datos y missing values",
        description="Detectar y manejar NaN con isna/fillna/dropna, eliminar duplicados, convertir tipos con errors=coerce, y limpiar strings con el accessor .str.",
        content=(
            "## Por que limpiar\n"
            "Los datos reales tienen problemas: celdas vacias, espacios al\n"
            "principio de strings, fechas en formato mixto, numeros guardados\n"
            "como texto, duplicados. La regla general en DS: **70% del tiempo\n"
            "es limpieza, 30% es modelado**. Esta leccion es la caja de\n"
            "herramientas que vas a usar todos los dias.\n\n"
            "## Detectar missing values\n"
            "```python\n"
            "df.isna()           # DataFrame booleano del mismo shape\n"
            "df.isna().sum()     # cuantos NaN por columna\n"
            "df['col'].notna()   # mascara inversa\n"
            "df.isna().any(axis=1).sum()  # cuantas FILAS tienen al menos un NaN\n"
            "```\n"
            "Recorda: en pandas `NaN` vale `float('nan')` y `None` vale\n"
            "`np.nan` cuando entra en una columna numerica. `isna` detecta\n"
            "ambos sin distinguir.\n\n"
            "## fillna — rellenar NaN\n"
            "```python\n"
            "df['edad'].fillna(0)                  # con escalar\n"
            "df['edad'].fillna(df['edad'].mean())  # con la media\n"
            "df['edad'].fillna(method='ffill')     # propaga el ultimo valido\n"
            "df.fillna({'edad': 0, 'plan': 'basico'})  # distinto por columna\n"
            "```\n"
            "**Decisiones de imputacion**:\n"
            "- Numerico no critico: media o mediana.\n"
            "- Series temporales: `ffill` o `bfill`.\n"
            "- Categorico: una categoria nueva tipo `'desconocido'`.\n"
            "- Critico (target del modelo): mejor `dropna`.\n\n"
            "## dropna — eliminar filas/columnas con NaN\n"
            "```python\n"
            "df.dropna()                       # filas con CUALQUIER NaN\n"
            "df.dropna(subset=['edad'])        # solo si 'edad' es NaN\n"
            "df.dropna(axis=1, how='all')      # columnas que son TODAS NaN\n"
            "df.dropna(thresh=3)               # filas con al menos 3 no-NaN\n"
            "```\n\n"
            "## drop_duplicates — quitar filas repetidas\n"
            "```python\n"
            "df.drop_duplicates()                              # filas identicas\n"
            "df.drop_duplicates(subset=['email'])              # por una columna\n"
            "df.drop_duplicates(subset=['id'], keep='last')    # quedate con la ultima\n"
            "```\n"
            "Verifica antes con `df.duplicated().sum()` cuantas hay.\n\n"
            "## astype — convertir tipos\n"
            "```python\n"
            "df['edad'] = df['edad'].astype(int)          # falla si hay NaN\n"
            "df['edad'] = df['edad'].astype('Int64')      # int nullable de pandas\n"
            "df['precio'] = df['precio'].astype(float)\n"
            "df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')\n"
            "```\n"
            "`errors='coerce'` convierte lo que no parsea a NaN en vez de crashear.\n"
            "Util para datasets sucios.\n\n"
            "## El accessor .str — limpiar texto\n"
            "Sobre columnas string, `.str` expone metodos vectorizados:\n"
            "```python\n"
            "df['email'] = df['email'].str.strip().str.lower()\n"
            "df['telefono'] = df['telefono'].str.replace(r'[^0-9]', '', regex=True)\n"
            "df['pais'] = df['pais'].str.title()  # 'argentina' -> 'Argentina'\n"
            "df['valida'] = df['email'].str.contains('@', na=False)\n"
            "```\n"
            "Sin `.str` estarias usando un loop Python sobre cada fila — lento\n"
            "y feo.\n\n"
            "## Errores comunes\n"
            "- Llamar `df.fillna(0)` sobre TODO el DataFrame cuando solo una\n"
            "  columna lo necesita. Eso reemplaza NaN de strings con 0 (string\n"
            "  inconsistente) y oculta problemas en otras columnas. Usa dict.\n"
            "- `df.dropna()` sin `subset=`: borra cualquier fila con UN NaN.\n"
            "  Si tu dataset tiene una columna con muchos NaN no criticos\n"
            "  puede quedarse con cero filas.\n"
            "- `astype(int)` con NaN presente: ValueError. Usar `'Int64'`\n"
            "  (mayuscula) o llenar NaN antes.\n"
            "- Usar `.str` sobre una columna que tiene NaN: la mayoria de\n"
            "  metodos `.str` propagan NaN correctamente, pero `.str.contains`\n"
            "  devuelve NaN como tercer estado. Pasar `na=False`.\n\n"
            "## Resumen\n"
            "- `isna().sum()` te dice donde estan los NaN, columna por columna.\n"
            "- `fillna` decide la estrategia de imputacion; `dropna` borra.\n"
            "- `drop_duplicates(subset=)` quita repetidos por clave.\n"
            "- `astype` + `errors='coerce'` convierte tipos sin crashear.\n"
            "- `.str` aplica metodos de string vectorizados sobre toda la columna.\n"
        ),
        difficulty="intermediate",
        category="pandas",
        order=15,
        track="track-2",
        estimated_duration=55,
        prerequisites_titles=["Pandas: merge, join y fechas"],
        exercises=[
            ExerciseTemplate(
                title="Contar nulos por columna",
                description="Devolver una Serie con la cantidad de NaN por columna.",
                instructions=(
                    "Implementa `nulos_por_columna(df)` que recibe un DataFrame "
                    "y devuelve una Serie indexada por nombre de columna con la "
                    "cantidad de NaN en cada una. Las columnas sin NaN deben "
                    "aparecer con valor 0."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def nulos_por_columna(df: pd.DataFrame) -> pd.Series:\n"
                    "    # TODO: df.isna().sum() devuelve exactamente eso.\n"
                    "    pass\n"
                ),
                hints=[
                    "df.isna() es un DataFrame booleano.",
                    ".sum() por defecto suma por columna (axis=0).",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "es una pandas Series",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({'a':[1,np.nan,3], 'b':[4,5,6]})\n"
                            "out = nulos_por_columna(df)\n"
                            "assert isinstance(out, pd.Series)"
                        ),
                    },
                    {
                        "name": "cuenta los NaN correctamente",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({\n"
                            "    'a':[1,np.nan,3,np.nan],\n"
                            "    'b':[4,5,6,7],\n"
                            "    'c':[np.nan,np.nan,np.nan,1],\n"
                            "})\n"
                            "out = nulos_por_columna(df)\n"
                            "assert out['a'] == 2\n"
                            "assert out['b'] == 0\n"
                            "assert out['c'] == 3"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Rellenar edad con la media",
                description="fillna con la media de la columna, preservando dtype.",
                instructions=(
                    "Implementa `rellenar_edad_con_media(df)` que devuelve una "
                    "copia de df donde los NaN en la columna 'edad' fueron "
                    "reemplazados por la media de 'edad' (calculada sin contar "
                    "los NaN). No modifiques el DataFrame original."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def rellenar_edad_con_media(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: copia, calcula media, fillna en columna edad.\n"
                    "    pass\n"
                ),
                hints=[
                    "df.copy() para no mutar el original.",
                    "media = df['edad'].mean() — pandas ignora NaN automaticamente.",
                    "out['edad'] = out['edad'].fillna(media)",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "no muta el original",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({'edad':[20.0, np.nan, 40.0]})\n"
                            "out = rellenar_edad_con_media(df)\n"
                            "assert out is not None and not out['edad'].isna().any(), "
                            "'la copia que devuelves tiene que venir sin NaN en edad'\n"
                            "assert df['edad'].isna().any(), 'no muta el original'"
                        ),
                    },
                    {
                        "name": "rellena con la media correcta",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({'edad':[20.0, np.nan, 40.0]})\n"
                            "out = rellenar_edad_con_media(df)\n"
                            "# media de [20, 40] = 30\n"
                            "assert out['edad'].isna().sum() == 0\n"
                            "assert abs(out['edad'].iloc[1] - 30.0) < 1e-9"
                        ),
                    },
                    {
                        "name": "preserva valores no nulos sin cambios",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({'edad':[25.0, np.nan, 35.0, 45.0]})\n"
                            "out = rellenar_edad_con_media(df)\n"
                            "assert out['edad'].iloc[0] == 25.0\n"
                            "assert out['edad'].iloc[2] == 35.0\n"
                            "assert out['edad'].iloc[3] == 45.0"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Pipeline de limpieza completo",
                description="Strip + lower + drop_duplicates + fillna en una funcion.",
                instructions=(
                    "Implementa `limpiar_clientes(df)` que recibe un DataFrame "
                    "con columnas 'email' (string posiblemente con espacios y "
                    "mayusculas mixtas) y 'edad' (float con NaN). Devuelve una "
                    "copia donde: (1) 'email' fue strip + lower, (2) NaN de "
                    "'edad' rellenados con la mediana, (3) duplicados por "
                    "'email' eliminados (queda la primera ocurrencia)."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def limpiar_clientes(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: copia, .str.strip().str.lower() en email,\n"
                    "    # fillna con mediana de edad, drop_duplicates por email.\n"
                    "    pass\n"
                ),
                hints=[
                    "out['email'] = out['email'].str.strip().str.lower()",
                    "mediana = out['edad'].median()",
                    "out = out.drop_duplicates(subset=['email'])",
                    "El orden de los pasos importa: limpia email ANTES de quitar duplicados.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "no muta el DataFrame original",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({\n"
                            "    'email':['  A@x.com','b@x.com'],\n"
                            "    'edad':[30.0, np.nan],\n"
                            "})\n"
                            "out = limpiar_clientes(df)\n"
                            "assert out is not None and out['email'].iloc[0] == 'a@x.com', "
                            "'la copia que devuelves tiene que traer el email normalizado'\n"
                            "assert df['email'].iloc[0] == '  A@x.com', 'modificaste el DataFrame original'"
                        ),
                    },
                    {
                        "name": "emails normalizados (strip + lower)",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({\n"
                            "    'email':['  A@x.com','B@X.com '],\n"
                            "    'edad':[30.0, 40.0],\n"
                            "})\n"
                            "out = limpiar_clientes(df)\n"
                            "assert set(out['email']) == {'a@x.com','b@x.com'}"
                        ),
                    },
                    {
                        "name": "edad rellenada con mediana",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({\n"
                            "    'email':['a@x.com','b@x.com','c@x.com'],\n"
                            "    'edad':[20.0, np.nan, 40.0],\n"
                            "})\n"
                            "out = limpiar_clientes(df)\n"
                            "# mediana de [20, 40] = 30\n"
                            "assert out['edad'].isna().sum() == 0\n"
                            "assert 30.0 in out['edad'].tolist()"
                        ),
                    },
                    {
                        "name": "duplicados por email eliminados despues de normalizar",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "df = pd.DataFrame({\n"
                            "    'email':['A@x.com','a@x.com  ','b@x.com'],\n"
                            "    'edad':[30.0, 35.0, 40.0],\n"
                            "})\n"
                            "out = limpiar_clientes(df)\n"
                            "assert len(out) == 2\n"
                            "assert set(out['email']) == {'a@x.com','b@x.com'}"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Visualizacion 1: matplotlib esencial",
        description="Histograma, scatter, lineas y bar charts con matplotlib. Decidir que tipo de plot usar segun la pregunta que quieres responder.",
        content=(
            "## Que es matplotlib\n"
            "matplotlib es la libreria base de visualizacion en Python. Casi\n"
            "todas las demas (seaborn, pandas.plot, plotly Express) la usan\n"
            "por dentro o la imitan. Dominar la API te da control total.\n\n"
            "En PyCode, cuando llames `plt.show()` el plot aparece inline\n"
            "en el panel de salida del editor — el worker captura la figura\n"
            "como PNG y la renderiza ahi mismo.\n\n"
            "## La estructura: Figure y Axes\n"
            "```python\n"
            "import matplotlib.pyplot as plt\n\n"
            "fig, ax = plt.subplots()       # crea figura + 1 eje\n"
            "ax.plot([1, 2, 3], [10, 20, 15])\n"
            "ax.set_title('Demo')\n"
            "ax.set_xlabel('x'); ax.set_ylabel('y')\n"
            "plt.show()\n"
            "```\n"
            "`Figure` es el lienzo. `Axes` es donde dibujas. Una figura puede\n"
            "tener varios axes (subplots). El API tiene dos modos:\n"
            "- **Funcional**: `plt.plot`, `plt.title`, `plt.show` (mas corto,\n"
            "  bueno para exploracion).\n"
            "- **Orientado a objetos**: `ax.plot`, `ax.set_title` (mas explicito,\n"
            "  necesario cuando hay multiples subplots).\n\n"
            "## Cuatro plots que cubren el 80% de los casos\n\n"
            "### 1. Linea — evolucion temporal\n"
            "```python\n"
            "plt.plot(fechas, ventas, marker='o')\n"
            "```\n"
            "Pregunta: '¿como cambia X a lo largo del tiempo?'.\n\n"
            "### 2. Scatter — relacion entre dos variables\n"
            "```python\n"
            "plt.scatter(altura, peso, alpha=0.6)\n"
            "```\n"
            "Pregunta: '¿hay correlacion entre X e Y?'. `alpha` evita que los\n"
            "puntos densos tapen lo que hay debajo.\n\n"
            "### 3. Histograma — distribucion de una variable\n"
            "```python\n"
            "plt.hist(notas, bins=10)\n"
            "```\n"
            "Pregunta: '¿como se distribuyen los valores de X? ¿hay outliers?'.\n"
            "Mas bins = mas detalle pero mas ruido.\n\n"
            "### 4. Barra — comparar categorias\n"
            "```python\n"
            "plt.bar(['cafe','te','torta'], [120, 80, 95])\n"
            "```\n"
            "Pregunta: '¿que categoria tiene mas X?'. Cuidado: no uses barras\n"
            "para variables continuas (eso es histograma).\n\n"
            "## Decorar el plot\n"
            "```python\n"
            "plt.title('Notas del trimestre')\n"
            "plt.xlabel('Estudiante'); plt.ylabel('Nota')\n"
            "plt.grid(True, alpha=0.3)\n"
            "plt.legend(['mate', 'lengua'])\n"
            "plt.tight_layout()  # evita que las labels se corten\n"
            "```\n\n"
            "## Multiples plots en una figura (subplots)\n"
            "```python\n"
            "fig, axes = plt.subplots(1, 2, figsize=(10, 4))\n"
            "axes[0].hist(notas_mate, bins=10); axes[0].set_title('Mate')\n"
            "axes[1].hist(notas_leng, bins=10); axes[1].set_title('Lengua')\n"
            "plt.tight_layout()\n"
            "plt.show()\n"
            "```\n\n"
            "## Plot directo desde pandas\n"
            "Series y DataFrame tienen `.plot()` que delega a matplotlib:\n"
            "```python\n"
            "df['ingreso'].plot(kind='line')\n"
            "df['ingreso'].plot(kind='hist', bins=20)\n"
            "df.plot.scatter(x='altura', y='peso')\n"
            "```\n"
            "Para algo rapido es ideal. Para control fino vuelve a `ax.plot`.\n\n"
            "## Errores comunes\n"
            "- Olvidar `plt.show()`: en PyCode el plot no aparece. En un\n"
            "  notebook Jupyter se muestra solo, pero aca explicitamente lo\n"
            "  necesitas para emitir el PNG.\n"
            "- Mezclar modo funcional con orientado a objetos en el mismo plot:\n"
            "  decidi uno y manteneo. Si usas `subplots`, casi obligatorio el\n"
            "  modo OO.\n"
            "- Hacer barras con muchas categorias (>15): se vuelve ilegible.\n"
            "  Mejor un horizontal bar (`plt.barh`) o un boxplot.\n"
            "- Usar `bins=` muy grande en histograma con pocos datos: cada bin\n"
            "  tiene 1-2 valores y el histograma se ve como ruido.\n\n"
            "## Resumen\n"
            "- 4 plots cubren el 80%: linea (tiempo), scatter (correlacion),\n"
            "  histograma (distribucion), barra (categorias).\n"
            "- API funcional para algo rapido; OO para subplots o control fino.\n"
            "- Siempre `plt.title`, `xlabel`, `ylabel`. Un plot sin etiquetas\n"
            "  es invendible.\n"
            "- `plt.show()` para emitir el PNG en PyCode.\n"
        ),
        difficulty="intermediate",
        category="visualizacion",
        order=16,
        track="track-2",
        estimated_duration=50,
        prerequisites_titles=["Pandas: limpieza de datos y missing values"],
        exercises=[
            ExerciseTemplate(
                title="Histograma de notas",
                description="Plot de distribucion con plt.hist.",
                instructions=(
                    "Implementa `plot_hist_notas(notas)` que recibe una lista o "
                    "Serie de notas, dibuja un histograma con 10 bins, agrega "
                    "titulo 'Distribucion de notas' y label de eje y 'Frecuencia'. "
                    "La funcion debe devolver el objeto Axes que uso para que "
                    "podamos verificar el plot."
                ),
                starter_code=(
                    "import matplotlib.pyplot as plt\n\n"
                    "def plot_hist_notas(notas):\n"
                    "    # TODO: fig, ax = plt.subplots(); ax.hist(...); ax.set_title(...)\n"
                    "    # return ax\n"
                    "    pass\n"
                ),
                hints=[
                    "fig, ax = plt.subplots(); luego ax.hist(notas, bins=10).",
                    "ax.set_title('Distribucion de notas'); ax.set_ylabel('Frecuencia').",
                    "Devolve ax al final para que los tests puedan inspeccionar el plot.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "devuelve un objeto Axes de matplotlib",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "ax = plot_hist_notas([3.0, 4.0, 4.5, 5.0, 2.5, 3.5])\n"
                            "assert hasattr(ax, 'patches'), 'debe devolver un Axes'\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "tiene 10 bins",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "ax = plot_hist_notas([3.0, 4.0, 4.5, 5.0, 2.5, 3.5])\n"
                            "assert len(ax.patches) == 10\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "tiene titulo y label correctos",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "ax = plot_hist_notas([3.0, 4.0, 4.5, 5.0, 2.5, 3.5])\n"
                            "assert 'distribucion' in ax.get_title().lower()\n"
                            "assert 'frecuencia' in ax.get_ylabel().lower()\n"
                            "plt.close('all')"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Bar chart de ventas por sucursal",
                description="Agregar con groupby y graficar con plt.bar.",
                instructions=(
                    "Implementa `plot_ventas_por_sucursal(df)` que recibe un "
                    "DataFrame con columnas 'sucursal' e 'ingreso', calcula la "
                    "suma de ingresos por sucursal con groupby, y dibuja un bar "
                    "chart con esas sucursales en el eje X. Devuelve el Axes."
                ),
                starter_code=(
                    "import matplotlib.pyplot as plt\n\n"
                    "def plot_ventas_por_sucursal(df):\n"
                    "    # TODO: groupby + ax.bar(sucursales, totales)\n"
                    "    pass\n"
                ),
                hints=[
                    "totales = df.groupby('sucursal')['ingreso'].sum()",
                    "ax.bar(totales.index, totales.values) usa el indice como categorias.",
                    "Las series de pandas tienen .plot(kind='bar', ax=ax) tambien.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "devuelve un Axes con barras",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['c','c','n','n','sur'],\n"
                            "    'ingreso':[100,50,80,20,60],\n"
                            "})\n"
                            "ax = plot_ventas_por_sucursal(df)\n"
                            "assert hasattr(ax, 'patches')\n"
                            "assert len(ax.patches) == 3, '3 sucursales = 3 barras'\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "alturas corresponden a las sumas",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sucursal':['c','c','n','n','sur'],\n"
                            "    'ingreso':[100,50,80,20,60],\n"
                            "})\n"
                            "ax = plot_ventas_por_sucursal(df)\n"
                            "alturas = sorted(p.get_height() for p in ax.patches)\n"
                            "# centro=150, norte=100, sur=60\n"
                            "assert alturas == [60.0, 100.0, 150.0]\n"
                            "plt.close('all')"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Scatter coloreado por categoria",
                description="Scatter con un color por especie usando un loop sobre groupby.",
                instructions=(
                    "Implementa `plot_iris_scatter(df)` que recibe un DataFrame "
                    "con columnas 'sepal_length', 'petal_length' y 'species'. "
                    "Dibuja un scatter con sepal_length en X, petal_length en Y, "
                    "y un color distinto por especie usando groupby + ax.scatter "
                    "en un loop. Agrega legend con los nombres de especies. "
                    "Devuelve el Axes."
                ),
                starter_code=(
                    "import matplotlib.pyplot as plt\n\n"
                    "def plot_iris_scatter(df):\n"
                    "    # TODO: fig, ax = plt.subplots()\n"
                    "    # for nombre, grupo in df.groupby('species'):\n"
                    "    #     ax.scatter(grupo['sepal_length'], grupo['petal_length'], label=nombre)\n"
                    "    # ax.legend(); return ax\n"
                    "    pass\n"
                ),
                hints=[
                    "df.groupby('species') itera devolviendo (nombre, sub_df).",
                    "ax.scatter(..., label=nombre) prepara la leyenda; ax.legend() la dibuja.",
                    "matplotlib elige los colores automaticamente al haber multiples llamadas a scatter.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "devuelve un Axes",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sepal_length':[5.1, 5.5, 6.3, 6.5, 7.0, 6.7],\n"
                            "    'petal_length':[1.4, 4.0, 6.0, 4.5, 4.7, 5.8],\n"
                            "    'species':['setosa','versicolor','virginica','versicolor','versicolor','virginica'],\n"
                            "})\n"
                            "ax = plot_iris_scatter(df)\n"
                            "assert hasattr(ax, 'collections')\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "3 grupos = 3 colecciones de puntos",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sepal_length':[5.1, 5.5, 6.3, 6.5, 7.0, 6.7],\n"
                            "    'petal_length':[1.4, 4.0, 6.0, 4.5, 4.7, 5.8],\n"
                            "    'species':['setosa','versicolor','virginica','versicolor','versicolor','virginica'],\n"
                            "})\n"
                            "ax = plot_iris_scatter(df)\n"
                            "# Cada ax.scatter(...) crea una PathCollection\n"
                            "assert len(ax.collections) == 3, '3 especies = 3 scatter calls'\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "tiene legend con las 3 especies",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'sepal_length':[5.1, 5.5, 6.3, 6.5, 7.0, 6.7],\n"
                            "    'petal_length':[1.4, 4.0, 6.0, 4.5, 4.7, 5.8],\n"
                            "    'species':['setosa','versicolor','virginica','versicolor','versicolor','virginica'],\n"
                            "})\n"
                            "ax = plot_iris_scatter(df)\n"
                            "leg = ax.get_legend()\n"
                            "assert leg is not None, 'falta legend'\n"
                            "labels = {t.get_text() for t in leg.get_texts()}\n"
                            "assert labels == {'setosa','versicolor','virginica'}\n"
                            "plt.close('all')"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Visualizacion 2: subplots, estilos y anotaciones",
        description="Layouts con multiples axes, ejes compartidos, dual y-axis con twinx, estilos globales, y anotaciones sobre el plot.",
        content=(
            "## Cuando un plot no alcanza\n"
            "Muchos analisis requieren comparar **distribuciones lado a lado**\n"
            "o ver **dos variables con escalas distintas** en el mismo grafico.\n"
            "matplotlib resuelve los dos con la misma idea: combinar Axes.\n\n"
            "## subplots — grid de plots\n"
            "```python\n"
            "import matplotlib.pyplot as plt\n\n"
            "fig, axes = plt.subplots(2, 2, figsize=(10, 8))\n"
            "axes[0, 0].plot(x1, y1)\n"
            "axes[0, 1].scatter(x2, y2)\n"
            "axes[1, 0].hist(z1, bins=20)\n"
            "axes[1, 1].bar(cat, vals)\n"
            "plt.tight_layout()\n"
            "plt.show()\n"
            "```\n"
            "`axes` es un array 2D — accedelo con `axes[fila, columna]`. Si\n"
            "solo hay una fila o columna, es 1D.\n\n"
            "## Compartir ejes — sharex / sharey\n"
            "Cuando comparas series temporales o distribuciones con la misma\n"
            "escala, compartir ejes evita ambiguedad visual:\n"
            "```python\n"
            "fig, axes = plt.subplots(2, 1, sharex=True, figsize=(8, 6))\n"
            "axes[0].plot(fechas, ventas_a); axes[0].set_title('Sucursal A')\n"
            "axes[1].plot(fechas, ventas_b); axes[1].set_title('Sucursal B')\n"
            "```\n"
            "Hacer zoom en uno ajusta el otro. El xlabel solo aparece en el de\n"
            "abajo automaticamente.\n\n"
            "## twinx — dos escalas en Y\n"
            "Cuando dos variables con unidades muy distintas (ventas en pesos\n"
            "vs unidades vendidas) viven en el mismo plot:\n"
            "```python\n"
            "fig, ax1 = plt.subplots()\n"
            "ax1.plot(fechas, ingresos, color='tab:blue', label='ingresos')\n"
            "ax1.set_ylabel('Ingresos $', color='tab:blue')\n\n"
            "ax2 = ax1.twinx()  # eje Y derecho compartiendo X\n"
            "ax2.plot(fechas, unidades, color='tab:orange', label='unidades')\n"
            "ax2.set_ylabel('Unidades', color='tab:orange')\n"
            "```\n"
            "**Cuidado**: twinx puede engaiar visualmente porque la escala\n"
            "doble esconde correlaciones reales. Usar con criterio y siempre\n"
            "con ejes coloreados a juego.\n\n"
            "## Estilos globales — plt.style.use\n"
            "Cambia el look de todos los plots con una linea:\n"
            "```python\n"
            "plt.style.use('seaborn-v0_8-darkgrid')  # fondo gris con grid\n"
            "plt.style.use('ggplot')                  # estilo R/ggplot2\n"
            "plt.style.use('default')                 # vuelve al default\n"
            "```\n"
            "Lista los disponibles con `plt.style.available`. Para presentaciones,\n"
            "`seaborn-v0_8-whitegrid` queda profesional.\n\n"
            "## Anotaciones — ax.annotate / ax.text\n"
            "Apuntar a un valor especifico vale mas que mil ejes:\n"
            "```python\n"
            "max_val = vals.max()\n"
            "idx_max = vals.argmax()\n"
            "ax.annotate(\n"
            "    f'Pico: {max_val}',\n"
            "    xy=(idx_max, max_val),       # punto donde apunta\n"
            "    xytext=(idx_max + 1, max_val + 5),  # donde va el texto\n"
            "    arrowprops={'arrowstyle': '->'},\n"
            ")\n"
            "```\n"
            "Para textos sin flecha: `ax.text(x, y, 'mensaje', fontsize=10)`.\n\n"
            "## Anotar valores sobre cada barra\n"
            "Pattern util para bar charts ejecutivos:\n"
            "```python\n"
            "bars = ax.bar(categorias, valores)\n"
            "for bar in bars:\n"
            "    h = bar.get_height()\n"
            "    ax.text(bar.get_x() + bar.get_width()/2, h + 0.5,\n"
            "            f'{h:.0f}', ha='center', va='bottom')\n"
            "```\n\n"
            "## Errores comunes\n"
            "- `subplots(1, 2)` devuelve `axes` como ARRAY 1D, no matriz 2D.\n"
            "  Indexalo `axes[0]`, no `axes[0, 0]` — el segundo da IndexError.\n"
            "- Olvidar `plt.tight_layout()` cuando los titulos se solapan o\n"
            "  los labels se cortan en la imagen final.\n"
            "- Usar twinx para variables que SI tienen la misma escala — confunde\n"
            "  al lector. Si comparten unidad, mejor ponelas en el mismo eje.\n"
            "- Aplicar `plt.style.use` despues de crear los axes: no afecta\n"
            "  retroactivamente. Llamalo al inicio del script o celda.\n\n"
            "## Resumen\n"
            "- `subplots(filas, cols)` crea un grid de Axes. 2D si filas y cols > 1.\n"
            "- `sharex`/`sharey` sincronizan ejes cuando compares lo mismo.\n"
            "- `twinx` agrega un eje Y derecho — usar con cuidado.\n"
            "- `plt.style.use` cambia look global; `ax.annotate` para anotaciones\n"
            "  apuntadas; `ax.text` para texto libre.\n"
        ),
        difficulty="intermediate",
        category="visualizacion",
        order=17,
        track="track-2",
        estimated_duration=45,
        prerequisites_titles=["Visualizacion 1: matplotlib esencial"],
        exercises=[
            ExerciseTemplate(
                title="2x1 subplots con eje X compartido",
                description="Dos plots verticales que comparten el eje X.",
                instructions=(
                    "Implementa `plot_dos_series(x, y1, y2)` que crea una figura "
                    "con 2 axes apilados verticalmente (2 filas, 1 columna) "
                    "compartiendo el eje X. En el de arriba grafica (x, y1) y en "
                    "el de abajo (x, y2). Devuelve la tupla (fig, axes)."
                ),
                starter_code=(
                    "import matplotlib.pyplot as plt\n\n"
                    "def plot_dos_series(x, y1, y2):\n"
                    "    # TODO: plt.subplots(2, 1, sharex=True)\n"
                    "    pass\n"
                ),
                hints=[
                    "fig, axes = plt.subplots(2, 1, sharex=True)",
                    "axes[0].plot(x, y1) — axes es array 1D porque hay una sola columna.",
                    "Devolve (fig, axes).",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "devuelve fig y array de 2 axes",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "fig, axes = plot_dos_series([1,2,3], [4,5,6], [10,20,30])\n"
                            "assert fig is not None\n"
                            "assert len(axes) == 2\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "ambos axes tienen una linea cada uno",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "fig, axes = plot_dos_series([1,2,3], [4,5,6], [10,20,30])\n"
                            "assert len(axes[0].lines) == 1\n"
                            "assert len(axes[1].lines) == 1\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "comparten el eje X (sharex)",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "fig, axes = plot_dos_series([1,2,3], [4,5,6], [10,20,30])\n"
                            "# Cuando sharex=True, los Axes apuntan a la misma instancia de eje X.\n"
                            "assert axes[0].get_shared_x_axes().joined(axes[0], axes[1])\n"
                            "plt.close('all')"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Bar chart con valores anotados",
                description="Bar con texto encima de cada barra mostrando el valor.",
                instructions=(
                    "Implementa `plot_bar_con_valores(categorias, valores)` que "
                    "dibuja un bar chart y agrega texto centrado encima de cada "
                    "barra con el valor numerico (formato entero). Devuelve el "
                    "Axes."
                ),
                starter_code=(
                    "import matplotlib.pyplot as plt\n\n"
                    "def plot_bar_con_valores(categorias, valores):\n"
                    "    # TODO: fig, ax = plt.subplots(); bars = ax.bar(...)\n"
                    "    # for bar in bars:\n"
                    "    #     h = bar.get_height()\n"
                    "    #     ax.text(bar.get_x() + bar.get_width()/2, h, f'{h:.0f}',\n"
                    "    #             ha='center', va='bottom')\n"
                    "    pass\n"
                ),
                hints=[
                    "ax.bar devuelve un BarContainer iterable de Rectangulos.",
                    "bar.get_x() + bar.get_width()/2 da la X central de la barra.",
                    "ha='center' centra horizontalmente el texto.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "tiene tantas barras como categorias",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "ax = plot_bar_con_valores(['a','b','c'], [10, 20, 15])\n"
                            "assert len(ax.patches) == 3\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "hay 3 textos (uno por barra)",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "ax = plot_bar_con_valores(['a','b','c'], [10, 20, 15])\n"
                            "textos = [t.get_text() for t in ax.texts]\n"
                            "assert len(textos) == 3\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "los textos muestran los valores correctos",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "ax = plot_bar_con_valores(['a','b','c'], [10, 20, 15])\n"
                            "textos = sorted(int(t.get_text()) for t in ax.texts)\n"
                            "assert textos == [10, 15, 20]\n"
                            "plt.close('all')"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Dual y-axis: ingresos vs unidades",
                description="Mismo X (tiempo), dos escalas Y (ingresos $ y unidades).",
                instructions=(
                    "Implementa `plot_dual_y(fechas, ingresos, unidades)` que "
                    "crea una figura con un Axes principal (ax1) graficando "
                    "(fechas, ingresos) y un Axes secundario via twinx (ax2) "
                    "graficando (fechas, unidades). Cada eje Y debe tener un "
                    "label distinto: 'Ingresos' y 'Unidades'. Devuelve "
                    "(fig, ax1, ax2)."
                ),
                starter_code=(
                    "import matplotlib.pyplot as plt\n\n"
                    "def plot_dual_y(fechas, ingresos, unidades):\n"
                    "    # TODO: fig, ax1 = plt.subplots()\n"
                    "    # ax1.plot(fechas, ingresos); ax1.set_ylabel('Ingresos')\n"
                    "    # ax2 = ax1.twinx(); ax2.plot(...); ax2.set_ylabel('Unidades')\n"
                    "    pass\n"
                ),
                hints=[
                    "ax1.twinx() devuelve un nuevo Axes que comparte X con ax1.",
                    "Cada axes mantiene sus propias lineas y label de Y.",
                    "Devolve la tupla (fig, ax1, ax2) en ese orden.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "devuelve fig, ax1, ax2",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "fig, ax1, ax2 = plot_dual_y([1,2,3], [100,150,200], [10,12,15])\n"
                            "assert fig is not None and ax1 is not None and ax2 is not None\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "cada axes tiene su linea",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "fig, ax1, ax2 = plot_dual_y([1,2,3], [100,150,200], [10,12,15])\n"
                            "assert len(ax1.lines) == 1\n"
                            "assert len(ax2.lines) == 1\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "ylabels son 'Ingresos' y 'Unidades'",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "fig, ax1, ax2 = plot_dual_y([1,2,3], [100,150,200], [10,12,15])\n"
                            "assert ax1.get_ylabel() == 'Ingresos'\n"
                            "assert ax2.get_ylabel() == 'Unidades'\n"
                            "plt.close('all')"
                        ),
                    },
                    {
                        "name": "ax2 comparte el eje X con ax1 (twinx)",
                        "code": (
                            "import matplotlib\n"
                            "matplotlib.use('Agg')\n"
                            "import matplotlib.pyplot as plt\n"
                            "fig, ax1, ax2 = plot_dual_y([1,2,3], [100,150,200], [10,12,15])\n"
                            "# twinx comparte el eje X\n"
                            "assert ax1.get_shared_x_axes().joined(ax1, ax2)\n"
                            "plt.close('all')"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="EDA: exploracion sistematica de un dataset",
        description="Pipeline reproducible para entender un dataset nuevo: shape/info/describe, distribuciones, outliers via IQR, correlaciones bivariadas.",
        content=(
            "## Que es EDA\n"
            "**Exploratory Data Analysis** es la fase de investigacion previa\n"
            "al modelado. El objetivo es responder cinco preguntas antes de\n"
            "entrenar nada:\n"
            "1. ¿Cuantas filas y columnas hay?\n"
            "2. ¿Que tipo es cada columna y cuantos NaN?\n"
            "3. ¿Como se distribuye cada variable?\n"
            "4. ¿Hay outliers? ¿Son errores o casos reales?\n"
            "5. ¿Que variables estan relacionadas entre si?\n\n"
            "Cuanto mejor hagas EDA, menos sorpresas en produccion.\n\n"
            "## Pipeline en cinco lineas\n"
            "```python\n"
            "df.shape       # 1. tamano\n"
            "df.info()      # 2. dtypes + nulos por columna\n"
            "df.head(5)     # primeras filas para sanity check\n"
            "df.describe()  # 3. distribucion (count/mean/std/min/quartiles/max)\n"
            "df.duplicated().sum()  # ¿hay filas repetidas?\n"
            "```\n"
            "Esto te da el 70% de la radiografia. Si algo te llama la atencion\n"
            "(una columna con 80% NaN, un max absurdo), profundizas ahi.\n\n"
            "## Distribuciones — histogramas y boxplots\n"
            "Para variables numericas:\n"
            "```python\n"
            "df['edad'].hist(bins=20)        # forma de la distribucion\n"
            "df.boxplot(column='edad')       # outliers visibles como puntos\n"
            "```\n"
            "El **boxplot** es perfecto para detectar outliers: la caja es Q1-Q3,\n"
            "la linea del medio es la mediana, los 'bigotes' van hasta 1.5*IQR,\n"
            "y los puntos fuera son candidatos a outlier.\n\n"
            "Para variables categoricas:\n"
            "```python\n"
            "df['pais'].value_counts()\n"
            "df['pais'].value_counts(normalize=True)  # porcentajes\n"
            "```\n\n"
            "## Detectar outliers con IQR\n"
            "La regla **1.5 * IQR** es el clasico:\n"
            "```python\n"
            "q1 = df['precio'].quantile(0.25)\n"
            "q3 = df['precio'].quantile(0.75)\n"
            "iqr = q3 - q1\n"
            "bajos = df['precio'] < q1 - 1.5 * iqr\n"
            "altos = df['precio'] > q3 + 1.5 * iqr\n"
            "outliers = df[bajos | altos]\n"
            "```\n"
            "Recordatorio importante: **no eliminar outliers automaticamente**.\n"
            "Algunas veces son los casos mas interesantes (fraude, errores de\n"
            "captura, segmentos especiales). Investigarlos primero.\n\n"
            "## Correlaciones — variables que se mueven juntas\n"
            "```python\n"
            "df.corr(numeric_only=True)\n"
            "```\n"
            "Devuelve una matriz simetrica con coeficientes de Pearson\n"
            "(-1 a +1):\n"
            "- **+1**: cuando una sube, la otra sube en la misma proporcion.\n"
            "- **0**: no hay relacion lineal.\n"
            "- **-1**: cuando una sube, la otra baja en la misma proporcion.\n\n"
            "Cuidado: Pearson solo captura relaciones **lineales**. Una relacion\n"
            "cuadratica puede dar correlacion casi cero y aun ser fuerte.\n\n"
            "Para visualizar la matriz, un heatmap:\n"
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "fig, ax = plt.subplots()\n"
            "im = ax.imshow(df.corr(numeric_only=True), cmap='coolwarm', vmin=-1, vmax=1)\n"
            "plt.colorbar(im)\n"
            "```\n\n"
            "## Crosstab — relacion entre categoricas\n"
            "```python\n"
            "pd.crosstab(df['pais'], df['plan'])\n"
            "pd.crosstab(df['pais'], df['plan'], normalize='index')  # % por fila\n"
            "```\n\n"
            "## Errores comunes\n"
            "- Saltarse el EDA por apuro: terminas entrenando con NaN, leaks\n"
            "  o columnas inutiles. **30 minutos de EDA ahorran horas de debug**.\n"
            "- Tirar outliers sin investigarlos: muchas veces son el problema\n"
            "  que queres modelar.\n"
            "- Interpretar correlacion como causalidad. Una correlacion alta\n"
            "  entre 'ventas de helado' y 'ahogamientos' no significa que el\n"
            "  helado cause ahogamientos (hay una variable de confusion: verano).\n"
            "- Olvidar `numeric_only=True` en `df.corr()`: en pandas modernos\n"
            "  esto avisa con un FutureWarning porque las columnas string no\n"
            "  tienen correlacion definida.\n\n"
            "## Resumen\n"
            "- EDA responde 5 preguntas antes de modelar.\n"
            "- 5 lineas (shape/info/head/describe/duplicated) dan el 70% del\n"
            "  panorama.\n"
            "- Histogramas para forma de distribucion, boxplots para outliers,\n"
            "  IQR como regla numerica.\n"
            "- `.corr(numeric_only=True)` para correlaciones; crosstab para\n"
            "  categoricas.\n"
            "- Correlacion no implica causalidad.\n"
        ),
        difficulty="intermediate",
        category="eda",
        order=18,
        track="track-2",
        estimated_duration=55,
        prerequisites_titles=["Visualizacion 2: subplots, estilos y anotaciones"],
        exercises=[
            ExerciseTemplate(
                title="Resumen estadistico de columnas numericas",
                description="Filtrar las columnas numericas y devolver describe().",
                instructions=(
                    "Implementa `resumen_numerico(df)` que devuelve el DataFrame "
                    "resultado de aplicar describe() SOLO a las columnas numericas. "
                    "Si una columna es de tipo object o categorico, excluirla. "
                    "Usa select_dtypes."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def resumen_numerico(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: df.select_dtypes(include='number').describe()\n"
                    "    pass\n"
                ),
                hints=[
                    "df.select_dtypes(include='number') filtra columnas numericas.",
                    "Sobre el resultado, .describe() devuelve el resumen estadistico.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "es un DataFrame",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'a':[1.0,2.0,3.0],\n"
                            "    'b':[10,20,30],\n"
                            "    'c':['x','y','z'],\n"
                            "})\n"
                            "out = resumen_numerico(df)\n"
                            "assert isinstance(out, pd.DataFrame)"
                        ),
                    },
                    {
                        "name": "excluye columnas no numericas",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'a':[1.0,2.0,3.0],\n"
                            "    'b':[10,20,30],\n"
                            "    'c':['x','y','z'],\n"
                            "})\n"
                            "out = resumen_numerico(df)\n"
                            "assert 'c' not in out.columns\n"
                            "assert set(out.columns) == {'a','b'}"
                        ),
                    },
                    {
                        "name": "incluye las metricas tipicas de describe",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'a':[1.0,2.0,3.0]})\n"
                            "out = resumen_numerico(df)\n"
                            "for metric in ['mean','std','min','25%','50%','75%','max']:\n"
                            "    assert metric in out.index"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Detectar outliers con regla IQR",
                description="Devolver las filas con valores fuera de Q1-1.5IQR / Q3+1.5IQR.",
                instructions=(
                    "Implementa `outliers_iqr(df, columna)` que recibe un "
                    "DataFrame y el nombre de una columna numerica. Calcula "
                    "Q1, Q3 y IQR. Devuelve el subset de filas cuyo valor en "
                    "esa columna es < Q1 - 1.5*IQR o > Q3 + 1.5*IQR."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def outliers_iqr(df: pd.DataFrame, columna: str) -> pd.DataFrame:\n"
                    "    # TODO: q1, q3 = quantile(0.25), quantile(0.75); iqr = q3-q1\n"
                    "    # mascara = (df[columna] < q1 - 1.5*iqr) | (df[columna] > q3 + 1.5*iqr)\n"
                    "    pass\n"
                ),
                hints=[
                    "df[columna].quantile(0.25) da el Q1 ignorando NaN.",
                    "Combina las dos condiciones con | (or bit a bit) y parentesis.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "devuelve DataFrame",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[10,12,11,13,12,500]})\n"
                            "out = outliers_iqr(df, 'precio')\n"
                            "assert isinstance(out, pd.DataFrame)"
                        ),
                    },
                    {
                        "name": "detecta outlier alto evidente",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[10,12,11,13,12,500]})\n"
                            "out = outliers_iqr(df, 'precio')\n"
                            "assert 500 in out['precio'].tolist()"
                        ),
                    },
                    {
                        "name": "no marca filas en rango normal",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[10,12,11,13,12,500]})\n"
                            "out = outliers_iqr(df, 'precio')\n"
                            "# Los valores 10-13 NO deben aparecer como outliers\n"
                            "assert 11 not in out['precio'].tolist()\n"
                            "assert 12 not in out['precio'].tolist()"
                        ),
                    },
                    {
                        "name": "detecta outlier bajo extremo",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[100, 102, 101, 99, 100, -50]})\n"
                            "out = outliers_iqr(df, 'precio')\n"
                            "assert -50 in out['precio'].tolist()"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Par mas correlacionado",
                description="Encontrar las dos columnas con mayor correlacion absoluta.",
                instructions=(
                    "Implementa `par_mas_correlacionado(df)` que calcula la "
                    "matriz de correlacion entre columnas numericas y devuelve "
                    "una tupla (col_a, col_b, correlacion) con las dos columnas "
                    "DISTINTAS que tienen la mayor correlacion absoluta. "
                    "(col_a, col_b) ordenadas alfabeticamente."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def par_mas_correlacionado(df: pd.DataFrame) -> tuple:\n"
                    "    # TODO: corr = df.corr(numeric_only=True)\n"
                    "    # Ignorar la diagonal (col consigo misma = 1).\n"
                    "    # Encontrar el max de |corr| en off-diagonal.\n"
                    "    pass\n"
                ),
                hints=[
                    "corr.abs() te da magnitudes sin signo.",
                    "Para evitar la diagonal: mascara `corr.values[i, i] = 0` o usar `corr.where(...)`.",
                    "Una vez encontradas col_a y col_b, devolve `(a, b, corr.loc[a, b])` con a, b ordenados.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "devuelve una tupla de 3 elementos",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "x = rng.normal(size=100)\n"
                            "df = pd.DataFrame({\n"
                            "    'a': x,\n"
                            "    'b': 2*x + rng.normal(scale=0.1, size=100),  # casi perfecta\n"
                            "    'c': rng.normal(size=100),  # ruido\n"
                            "})\n"
                            "out = par_mas_correlacionado(df)\n"
                            "assert isinstance(out, tuple) and len(out) == 3"
                        ),
                    },
                    {
                        "name": "identifica el par mas correlacionado correcto",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "x = rng.normal(size=100)\n"
                            "df = pd.DataFrame({\n"
                            "    'a': x,\n"
                            "    'b': 2*x + rng.normal(scale=0.1, size=100),\n"
                            "    'c': rng.normal(size=100),\n"
                            "})\n"
                            "out = par_mas_correlacionado(df)\n"
                            "assert set(out[:2]) == {'a','b'}"
                        ),
                    },
                    {
                        "name": "ordena el par alfabeticamente",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "x = rng.normal(size=100)\n"
                            "df = pd.DataFrame({\n"
                            "    'zeta': x,\n"
                            "    'alpha': 2*x + rng.normal(scale=0.1, size=100),\n"
                            "    'beta': rng.normal(size=100),\n"
                            "})\n"
                            "out = par_mas_correlacionado(df)\n"
                            "assert out[0] < out[1], 'columnas no estan ordenadas'\n"
                            "assert out[0] == 'alpha' and out[1] == 'zeta'"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="EDA 2: feature engineering basico",
        description="Codificar categoricas con one-hot, agrupar continuas en bins, y normalizar variables para que un modelo las trate por igual.",
        content=(
            "## Por que feature engineering\n"
            "Los modelos de ML no entienden 'Argentina' ni 'plan premium': solo\n"
            "numeros. Y dentro de los numeros tampoco les es indiferente que\n"
            "una variable este en miles y otra en decimales — los algoritmos\n"
            "basados en distancia (kNN, SVM, redes) se van a quedar mirando\n"
            "solo la variable de mayor escala.\n\n"
            "Feature engineering es **transformar las columnas crudas en algo\n"
            "que el modelo pueda usar**. En esta leccion: encoding, binning y\n"
            "normalizacion.\n\n"
            "## One-hot encoding — categorias a columnas binarias\n"
            "```python\n"
            "import pandas as pd\n\n"
            "df = pd.DataFrame({'pais': ['AR','MX','AR','CO']})\n"
            "dummies = pd.get_dummies(df['pais'])\n"
            "#    AR     CO     MX\n"
            "# 0   1      0      0\n"
            "# 1   0      0      1\n"
            "# 2   1      0      0\n"
            "# 3   0      1      0\n"
            "```\n"
            "Cada categoria pasa a una columna binaria (0/1). Para integrar al\n"
            "DataFrame original, `pd.get_dummies(df, columns=['pais'])` lo hace\n"
            "directo y agrega las dummies en lugar de la columna original.\n\n"
            "**`drop_first=True`** quita la primera categoria para evitar\n"
            "multicolinealidad (importante para regresion lineal):\n"
            "```python\n"
            "pd.get_dummies(df['pais'], drop_first=True)  # 2 columnas en vez de 3\n"
            "```\n\n"
            "## Label encoding — orden manual\n"
            "Cuando hay orden natural (ordinal), no uses one-hot — perdes la\n"
            "informacion del orden. Mapea a numeros con `map`:\n"
            "```python\n"
            "orden_plan = {'basico': 0, 'pro': 1, 'enterprise': 2}\n"
            "df['plan_num'] = df['plan'].map(orden_plan)\n"
            "```\n\n"
            "## Binning — convertir continuo en categorico\n"
            "Para histogramas, segmentar usuarios o variables 'edad → grupo etario':\n\n"
            "**`pd.cut`** con limites definidos:\n"
            "```python\n"
            "rangos = [0, 18, 30, 50, 100]\n"
            "labels = ['menor', 'joven', 'adulto', 'mayor']\n"
            "df['grupo'] = pd.cut(df['edad'], bins=rangos, labels=labels)\n"
            "```\n\n"
            "**`pd.qcut`** con cuantiles (cada bin tiene la misma cantidad de\n"
            "puntos):\n"
            "```python\n"
            "df['quintil'] = pd.qcut(df['ingreso'], q=5, labels=['Q1','Q2','Q3','Q4','Q5'])\n"
            "```\n"
            "`qcut` es ideal cuando los datos estan sesgados (long tail): los\n"
            "limites se adaptan a la distribucion.\n\n"
            "## Transformaciones — comprimir/expandir escalas\n"
            "Si una variable es muy sesgada hacia la derecha (precios, ingresos),\n"
            "el log la simetriza:\n"
            "```python\n"
            "import numpy as np\n"
            "df['log_precio'] = np.log1p(df['precio'])  # log(1 + x), maneja 0\n"
            "```\n"
            "`log1p` se usa en vez de `log` porque acepta 0 (log(0) = -inf).\n\n"
            "## Normalizacion min-max — escala 0 a 1\n"
            "```python\n"
            "def min_max(s):\n"
            "    return (s - s.min()) / (s.max() - s.min())\n\n"
            "df['edad_norm'] = min_max(df['edad'])\n"
            "```\n"
            "Util cuando importa la **forma** de la distribucion mas que la\n"
            "escala (kNN, redes con sigmoid).\n\n"
            "## Estandarizacion z-score — media 0, std 1\n"
            "```python\n"
            "def zscore(s):\n"
            "    return (s - s.mean()) / s.std()\n\n"
            "df['edad_z'] = zscore(df['edad'])\n"
            "```\n"
            "Mas comun en regresion lineal / logistica y para detectar outliers\n"
            "(|z| > 3 suele considerarse outlier).\n\n"
            "## Errores comunes\n"
            "- Hacer one-hot a una columna con miles de categorias: explosion\n"
            "  de columnas. Mejor usar target encoding o agrupar las raras en\n"
            "  'otros'.\n"
            "- Normalizar TODO el dataset junto incluyendo el target: leak.\n"
            "  Normaliza features, no el target.\n"
            "- Calcular la normalizacion sobre el dataset COMPLETO y despues\n"
            "  hacer split train/test: leak temporal. Lo correcto es fitear\n"
            "  los stats en train y aplicarlos a test.\n"
            "- Usar log sobre una columna con ceros sin log1p: -inf en la\n"
            "  primera fila, modelo roto.\n\n"
            "## Resumen\n"
            "- One-hot para nominales (sin orden); label/map para ordinales.\n"
            "- `pd.cut` con limites fijos; `pd.qcut` con cuantiles.\n"
            "- Log para distribuciones sesgadas (`log1p` si hay ceros).\n"
            "- Min-max para distancias (kNN); z-score para regresion lineal.\n"
            "- Calcula los parametros de normalizacion en train, no en todo el\n"
            "  dataset.\n"
        ),
        difficulty="intermediate",
        category="eda",
        order=19,
        track="track-2",
        estimated_duration=55,
        prerequisites_titles=["EDA: exploracion sistematica de un dataset"],
        exercises=[
            ExerciseTemplate(
                title="One-hot encoding de pais",
                description="Convertir una columna categorica en columnas binarias.",
                instructions=(
                    "Implementa `one_hot_pais(df)` que devuelve un DataFrame "
                    "agregando columnas one-hot por cada valor unico de la "
                    "columna 'pais', con el prefijo 'pais_' (ej. 'pais_AR'). "
                    "Devuelve el DataFrame con las columnas originales MAS las "
                    "nuevas; NO drop_first."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def one_hot_pais(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: pd.get_dummies(df, columns=['pais'], prefix='pais')\n"
                    "    pass\n"
                ),
                hints=[
                    "pd.get_dummies(df, columns=['pais'], prefix='pais') hace todo en una linea.",
                    "Sin drop_first quedan tantas columnas dummy como categorias distintas.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "devuelve DataFrame con las dummies",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'pais':['AR','MX','CO','AR']})\n"
                            "out = one_hot_pais(df)\n"
                            "assert 'pais_AR' in out.columns\n"
                            "assert 'pais_MX' in out.columns\n"
                            "assert 'pais_CO' in out.columns"
                        ),
                    },
                    {
                        "name": "los valores son 0/1 correctos",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'pais':['AR','MX','CO','AR']})\n"
                            "out = one_hot_pais(df)\n"
                            "assert int(out['pais_AR'].iloc[0]) == 1\n"
                            "assert int(out['pais_AR'].iloc[1]) == 0\n"
                            "assert int(out['pais_MX'].iloc[1]) == 1\n"
                            "assert int(out['pais_AR'].iloc[3]) == 1"
                        ),
                    },
                    {
                        "name": "la columna original pais ya no esta",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'pais':['AR','MX','CO','AR']})\n"
                            "out = one_hot_pais(df)\n"
                            "# get_dummies con columns= drop la original.\n"
                            "assert 'pais' not in out.columns"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Binning de edad en grupos",
                description="Convertir edad numerica en categorias etarias con pd.cut.",
                instructions=(
                    "Implementa `grupos_etarios(df)` que recibe un DataFrame con "
                    "columna 'edad'. Devuelve el mismo DataFrame con una nueva "
                    "columna 'grupo' usando los bins [0, 18, 30, 50, 100] y "
                    "labels ['menor', 'joven', 'adulto', 'mayor']. No mutar "
                    "el original."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def grupos_etarios(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: copia, df['grupo'] = pd.cut(df['edad'], bins=..., labels=...)\n"
                    "    pass\n"
                ),
                hints=[
                    "pd.cut(serie, bins=[0,18,30,50,100], labels=['menor','joven','adulto','mayor'])",
                    "Devolve una copia: out = df.copy(); out['grupo'] = ...",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "no muta el original",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'edad':[10, 25, 40, 60]})\n"
                            "out = grupos_etarios(df)\n"
                            "assert out is not None and 'grupo' in out.columns, "
                            "'grupos_etarios tiene que devolver una copia con la columna grupo'\n"
                            "assert 'grupo' not in df.columns, 'modificaste el DataFrame original'"
                        ),
                    },
                    {
                        "name": "asigna el grupo correcto a cada edad",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'edad':[10, 25, 40, 60]})\n"
                            "out = grupos_etarios(df)\n"
                            "assert str(out['grupo'].iloc[0]) == 'menor'\n"
                            "assert str(out['grupo'].iloc[1]) == 'joven'\n"
                            "assert str(out['grupo'].iloc[2]) == 'adulto'\n"
                            "assert str(out['grupo'].iloc[3]) == 'mayor'"
                        ),
                    },
                    {
                        "name": "preserva las columnas originales",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'edad':[10, 25, 40, 60], 'extra': [1,2,3,4]})\n"
                            "out = grupos_etarios(df)\n"
                            "assert 'edad' in out.columns\n"
                            "assert 'extra' in out.columns"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Normalizar con min-max y z-score",
                description="Devolver el DataFrame con dos columnas extra normalizadas.",
                instructions=(
                    "Implementa `normalizar_precio(df)` que recibe un DataFrame "
                    "con columna 'precio'. Devuelve una copia con dos columnas "
                    "extra: 'precio_norm' (min-max a [0, 1]) y 'precio_z' "
                    "(z-score). No mutar el original."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def normalizar_precio(df: pd.DataFrame) -> pd.DataFrame:\n"
                    "    # TODO: copia, calcula min/max y mean/std,\n"
                    "    # crea precio_norm y precio_z.\n"
                    "    pass\n"
                ),
                hints=[
                    "min-max: (s - s.min()) / (s.max() - s.min())",
                    "z-score: (s - s.mean()) / s.std()",
                    "Calcula los stats sobre la columna del DataFrame copiado, no de pasos intermedios.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "no muta el original",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[10.0, 20.0, 30.0]})\n"
                            "out = normalizar_precio(df)\n"
                            "assert out is not None and {'precio_norm', 'precio_z'} <= set(out.columns), "
                            "'normalizar_precio tiene que devolver una copia con precio_norm y precio_z'\n"
                            "assert 'precio_norm' not in df.columns\n"
                            "assert 'precio_z' not in df.columns"
                        ),
                    },
                    {
                        "name": "min-max queda en rango [0, 1]",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[10.0, 20.0, 30.0, 40.0]})\n"
                            "out = normalizar_precio(df)\n"
                            "assert abs(out['precio_norm'].min() - 0.0) < 1e-9\n"
                            "assert abs(out['precio_norm'].max() - 1.0) < 1e-9"
                        ),
                    },
                    {
                        "name": "z-score tiene media cercana a 0",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[10.0, 20.0, 30.0, 40.0]})\n"
                            "out = normalizar_precio(df)\n"
                            "assert abs(out['precio_z'].mean()) < 1e-9"
                        ),
                    },
                    {
                        "name": "preserva la columna original 'precio'",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({'precio':[10.0, 20.0, 30.0]})\n"
                            "out = normalizar_precio(df)\n"
                            "assert 'precio' in out.columns\n"
                            "assert out['precio'].tolist() == [10.0, 20.0, 30.0]"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Estadistica descriptiva: resumir un dataset",
        description="Tendencia central y dispersion, cuando usar media vs mediana, forma de la distribucion con skewness y kurtosis.",
        content=(
            "## Por que estadistica descriptiva\n"
            "Antes de cualquier modelo, necesitas **comunicar** que hay en\n"
            "tus datos. La estadistica descriptiva resume con pocos numeros\n"
            "lo que veria un humano mirando miles de filas:\n"
            "- ¿Donde esta el 'centro' de la variable?\n"
            "- ¿Que tan dispersos estan los valores?\n"
            "- ¿La distribucion es simetrica o sesgada?\n\n"
            "## Medidas de tendencia central\n\n"
            "### Media (promedio)\n"
            "```python\n"
            "df['edad'].mean()  # suma / n\n"
            "```\n"
            "Sensible a outliers: un valor extremo arrastra el promedio.\n\n"
            "### Mediana (valor central)\n"
            "```python\n"
            "df['edad'].median()  # el del medio cuando ordenas\n"
            "```\n"
            "**Resistente a outliers**. Si tu distribucion tiene cola larga\n"
            "(salarios, vistas en YouTube), usa mediana.\n\n"
            "### Moda (valor mas frecuente)\n"
            "```python\n"
            "df['plan'].mode()  # puede haber varias modas si hay empate\n"
            "```\n"
            "Util para categoricas. En numericas continuas rara vez tiene sentido.\n\n"
            "**Cuando usar cual**:\n"
            "- **Media** — distribucion simetrica sin outliers (notas, alturas).\n"
            "- **Mediana** — distribucion sesgada o con outliers (precios, ingresos).\n"
            "- **Moda** — categoricas, o discretas donde 'el caso mas comun' importa.\n\n"
            "## Medidas de dispersion\n\n"
            "### Varianza y desviacion estandar\n"
            "```python\n"
            "df['edad'].var()   # promedio de (x - mean)^2\n"
            "df['edad'].std()   # raiz cuadrada de la varianza\n"
            "```\n"
            "La std esta en las mismas unidades que la variable (edades en\n"
            "anios, std en anios). Por eso se prefiere para reportar.\n\n"
            "### Rango intercuartil (IQR)\n"
            "```python\n"
            "iqr = df['edad'].quantile(0.75) - df['edad'].quantile(0.25)\n"
            "```\n"
            "**Resistente a outliers**. Si usas mediana como centro, IQR es la\n"
            "dispersion natural a reportar (no std).\n\n"
            "## Forma de la distribucion\n\n"
            "### Skewness (asimetria)\n"
            "```python\n"
            "df['precio'].skew()\n"
            "```\n"
            "- **0**: simetrica.\n"
            "- **>0**: cola a la derecha (salarios, precios).\n"
            "- **<0**: cola a la izquierda (edad de jubilacion).\n"
            "- **|skew| > 1**: muy sesgada — considera transformacion log.\n\n"
            "### Kurtosis (peso de las colas)\n"
            "```python\n"
            "df['precio'].kurt()\n"
            "```\n"
            "- **0** (Fisher): igual a una normal.\n"
            "- **>0**: leptokurtic — colas mas pesadas que normal, mas outliers.\n"
            "- **<0**: platykurtic — distribucion mas plana.\n\n"
            "## Regla 68-95-99.7 (solo para distribuciones casi normales)\n"
            "Si tu variable es ~normal:\n"
            "- 68% de los valores caen dentro de mean ± 1 std.\n"
            "- 95% dentro de mean ± 2 std.\n"
            "- 99.7% dentro de mean ± 3 std.\n\n"
            "Esta regla es como detectas outliers via z-score: |z| > 3 implica\n"
            "<0.3% de probabilidad si fuera realmente normal.\n\n"
            "## Cuidado: estadisticas mienten con poca data\n"
            "Calcular media y std sobre 3 puntos no te dice nada. Reglas\n"
            "practicas:\n"
            "- **n < 30**: usa mediana y rango, no media y std.\n"
            "- **n < 5**: no calcules nada, mira los valores uno por uno.\n"
            "- Siempre acompaña el resumen con n (count) para que el lector\n"
            "  pondere la confianza.\n\n"
            "## Errores comunes\n"
            "- Reportar 'el promedio de salario es 80k' cuando hay un CEO de\n"
            "  10M en la muestra: la mediana puede ser 45k. Usa mediana cuando\n"
            "  hay outliers grandes.\n"
            "- Confundir n (sample size) con la cantidad de valores unicos.\n"
            "  `df['edad'].nunique()` no es lo mismo que `len(df)`.\n"
            "- Aplicar la regla 68-95-99.7 a distribuciones que no son normales.\n"
            "  Hace falta verificar primero (skew, qq-plot, Shapiro-Wilk).\n"
            "- `df.mean()` ignora NaN automaticamente. Util, pero verificar\n"
            "  `df.isna().sum()` para saber sobre cuantos valores realmente se\n"
            "  promedio.\n\n"
            "## Resumen\n"
            "- Media/mediana/moda: tendencia central. Mediana resiste outliers.\n"
            "- std/var/IQR: dispersion. IQR resiste outliers.\n"
            "- skew indica asimetria; kurt indica colas pesadas.\n"
            "- Si distribucion casi normal, regla 68-95-99.7 para z-score.\n"
            "- Siempre reportar n junto con el resumen.\n"
        ),
        difficulty="intermediate",
        category="estadistica",
        order=20,
        track="track-2",
        estimated_duration=50,
        prerequisites_titles=["EDA 2: feature engineering basico"],
        exercises=[
            ExerciseTemplate(
                title="Resumen de una columna",
                description="Devolver un dict con mean, median, std y count.",
                instructions=(
                    "Implementa `resumir(serie)` que recibe una pd.Series numerica "
                    "y devuelve un dict con keys 'mean', 'median', 'std', 'count'. "
                    "Los NaN deben ignorarse en mean/median/std (que es el default "
                    "de pandas), pero count debe ser el numero de NO-NaN."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def resumir(serie: pd.Series) -> dict:\n"
                    "    # TODO: {'mean': ..., 'median': ..., 'std': ..., 'count': ...}\n"
                    "    pass\n"
                ),
                hints=[
                    "serie.mean(), serie.median(), serie.std() ignoran NaN.",
                    "serie.count() devuelve la cantidad de no-NaN.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "devuelve dict con las 4 keys",
                        "code": (
                            "import pandas as pd\n"
                            "out = resumir(pd.Series([1.0, 2.0, 3.0, 4.0]))\n"
                            "assert isinstance(out, dict)\n"
                            "assert set(out.keys()) == {'mean','median','std','count'}"
                        ),
                    },
                    {
                        "name": "calcula media y mediana correctas",
                        "code": (
                            "import pandas as pd\n"
                            "out = resumir(pd.Series([1.0, 2.0, 3.0, 4.0, 5.0]))\n"
                            "assert abs(out['mean'] - 3.0) < 1e-9\n"
                            "assert abs(out['median'] - 3.0) < 1e-9"
                        ),
                    },
                    {
                        "name": "count ignora NaN",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "out = resumir(pd.Series([1.0, 2.0, np.nan, 4.0]))\n"
                            "assert out['count'] == 3"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Detectar distribucion sesgada",
                description="Devolver True si |skew| > 1 (regla practica de sesgo fuerte).",
                instructions=(
                    "Implementa `esta_sesgada(serie)` que recibe una pd.Series "
                    "y devuelve True si el skew absoluto es mayor a 1 (regla "
                    "comun para sesgo 'fuerte'). En otro caso False."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def esta_sesgada(serie: pd.Series) -> bool:\n"
                    "    # TODO: abs(serie.skew()) > 1\n"
                    "    pass\n"
                ),
                hints=[
                    "serie.skew() devuelve el coeficiente de asimetria (float).",
                    "Usa abs() y compara con 1.",
                    "Devolve un bool, no un numpy bool. bool(serie.skew()) si hace falta.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "distribucion simetrica devuelve False",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "# Normal: skew ~ 0\n"
                            "s = pd.Series(rng.normal(0, 1, 1000))\n"
                            "assert esta_sesgada(s) is False"
                        ),
                    },
                    {
                        "name": "distribucion muy sesgada devuelve True",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "# Exponencial: skew muy positivo\n"
                            "s = pd.Series(rng.exponential(1.0, 1000))\n"
                            "assert esta_sesgada(s) is True"
                        ),
                    },
                    {
                        "name": "negativamente sesgada tambien devuelve True",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "# Exp invertida: skew muy negativo\n"
                            "s = pd.Series(-rng.exponential(1.0, 1000))\n"
                            "assert esta_sesgada(s) is True"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Comparar dos grupos numericamente",
                description="Resumen comparado entre dos grupos: diferencia de medias normalizada por std combinado.",
                instructions=(
                    "Implementa `comparar(grupo_a, grupo_b)` que recibe dos "
                    "pd.Series numericas y devuelve un dict con: "
                    "(1) 'mean_a' y 'mean_b' (medias), (2) 'std_pooled' "
                    "(desviacion estandar combinada = sqrt((var_a + var_b)/2)), "
                    "(3) 'cohen_d' (diferencia de medias / std_pooled). "
                    "Cohen's d es una medida estandar de tamano del efecto."
                ),
                starter_code=(
                    "import pandas as pd\n"
                    "import numpy as np\n\n"
                    "def comparar(grupo_a: pd.Series, grupo_b: pd.Series) -> dict:\n"
                    "    # TODO: calcular mean_a, mean_b, var_a, var_b,\n"
                    "    # std_pooled = sqrt((var_a + var_b) / 2),\n"
                    "    # cohen_d = (mean_a - mean_b) / std_pooled.\n"
                    "    pass\n"
                ),
                hints=[
                    "grupo_a.var() y grupo_b.var() dan las varianzas.",
                    "np.sqrt((var_a + var_b) / 2) es la formula de pooled std (version simple).",
                    "Devolve floats convencionales, no numpy scalars (usa float(...) si necesario).",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "devuelve las 4 keys esperadas",
                        "code": (
                            "import pandas as pd\n"
                            "a = pd.Series([1.0, 2.0, 3.0, 4.0])\n"
                            "b = pd.Series([2.0, 3.0, 4.0, 5.0])\n"
                            "out = comparar(a, b)\n"
                            "assert set(out.keys()) == {'mean_a','mean_b','std_pooled','cohen_d'}"
                        ),
                    },
                    {
                        "name": "medias correctas",
                        "code": (
                            "import pandas as pd\n"
                            "a = pd.Series([1.0, 2.0, 3.0, 4.0])\n"
                            "b = pd.Series([2.0, 3.0, 4.0, 5.0])\n"
                            "out = comparar(a, b)\n"
                            "assert abs(out['mean_a'] - 2.5) < 1e-9\n"
                            "assert abs(out['mean_b'] - 3.5) < 1e-9"
                        ),
                    },
                    {
                        "name": "grupos identicos dan cohen_d 0",
                        "code": (
                            "import pandas as pd\n"
                            "a = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])\n"
                            "b = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])\n"
                            "out = comparar(a, b)\n"
                            "assert abs(out['cohen_d']) < 1e-9"
                        ),
                    },
                    {
                        "name": "cohen_d tiene el signo correcto",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "a = pd.Series(rng.normal(10.0, 1.0, 200))\n"
                            "b = pd.Series(rng.normal(5.0, 1.0, 200))\n"
                            "out = comparar(a, b)\n"
                            "# a > b en media -> cohen_d > 0\n"
                            "assert out['cohen_d'] > 0"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="Correlacion, probabilidad y bootstrap",
        description="Pearson vs Spearman, simular probabilidades con Monte Carlo y estimar intervalos de confianza con bootstrap.",
        content=(
            "## Tres ideas que necesitas\n"
            "1. **Correlacion sirve para describir relaciones, pero hay dos\n"
            "   tipos** segun la forma de esa relacion.\n"
            "2. **Cuando no podes derivar una probabilidad analiticamente,\n"
            "   simulala** con muestreo (Monte Carlo).\n"
            "3. **Tus estimaciones tienen incertidumbre**; reportar un\n"
            "   intervalo en vez de un numero solo es lo profesional.\n\n"
            "## Correlacion Pearson vs Spearman\n\n"
            "### Pearson — relacion lineal\n"
            "```python\n"
            "df['x'].corr(df['y'])              # default Pearson\n"
            "df['x'].corr(df['y'], method='pearson')\n"
            "```\n"
            "Mide que tan bien una **linea recta** ajusta los datos. Va de -1\n"
            "a +1. Si la relacion entre X e Y es cuadratica (Y = X^2), Pearson\n"
            "puede dar casi cero — y aun asi habria una relacion fortisima.\n\n"
            "### Spearman — relacion monotona\n"
            "```python\n"
            "df['x'].corr(df['y'], method='spearman')\n"
            "```\n"
            "Mide si, al ordenar X, Y tambien queda ordenado. **Captura\n"
            "relaciones no lineales monotonas** (Y = X^3, Y = log(X)).\n\n"
            "**Cuando usar cual**:\n"
            "- Pearson: variables continuas con relacion aparentemente lineal.\n"
            "- Spearman: ordinales, distribuciones sesgadas, o cuando sospechas\n"
            "  relacion no lineal pero monotona.\n"
            "- Si tenes outliers, Spearman es mas robusto (usa rankings).\n\n"
            "## Probabilidad — vocabulario minimo\n"
            "Para una variable aleatoria X:\n"
            "- **P(A)**: probabilidad del evento A.\n"
            "- **P(A ∩ B)**: probabilidad de que pasen A Y B.\n"
            "- **P(A | B)**: probabilidad de A **dado que** ya paso B (condicional).\n"
            "- **Bayes**: P(A | B) = P(B | A) * P(A) / P(B).\n\n"
            "## Monte Carlo — simular probabilidades\n"
            "Cuando no podes deducir una probabilidad analiticamente:\n"
            "1. Simulas N experimentos.\n"
            "2. Contas cuantas veces ocurrio el evento.\n"
            "3. P(evento) ≈ ocurrencias / N.\n\n"
            "Ejemplo: ¿que chance hay de que la suma de 2 dados sea 7?\n"
            "```python\n"
            "import numpy as np\n\n"
            "rng = np.random.default_rng(42)\n"
            "N = 100_000\n"
            "d1 = rng.integers(1, 7, size=N)\n"
            "d2 = rng.integers(1, 7, size=N)\n"
            "p = (d1 + d2 == 7).mean()  # ~0.167 (real: 6/36 = 0.1667)\n"
            "```\n"
            "Cuanto mayor N, mas estable la estimacion. La regla heuristica:\n"
            "el error escala con `1/sqrt(N)`, asi que 100x mas muestras = 10x\n"
            "menos error.\n\n"
            "## Bootstrap — intervalos de confianza para cualquier estadistica\n"
            "El bootstrap responde: '¿que tan confiable es mi estimacion?'.\n"
            "Estrategia:\n"
            "1. Resampleas tu sample con reemplazo (mismo tamano).\n"
            "2. Calculas la estadistica (media, mediana, etc.) sobre cada\n"
            "   resample.\n"
            "3. Despues de muchos resamples (1000-10000), tomas los percentiles\n"
            "   2.5 y 97.5 — eso es el IC del 95%.\n\n"
            "```python\n"
            "def ic_bootstrap_media(datos, n_resamples=2000, ci=0.95, seed=0):\n"
            "    rng = np.random.default_rng(seed)\n"
            "    medias = np.empty(n_resamples)\n"
            "    n = len(datos)\n"
            "    for i in range(n_resamples):\n"
            "        muestra = rng.choice(datos, size=n, replace=True)\n"
            "        medias[i] = muestra.mean()\n"
            "    alpha = 1 - ci\n"
            "    bajo = np.percentile(medias, 100 * alpha / 2)\n"
            "    alto = np.percentile(medias, 100 * (1 - alpha / 2))\n"
            "    return bajo, alto\n"
            "```\n"
            "Salida: '(IC 95%): [4.8, 5.3]' es mas util que 'la media es 5.1'.\n\n"
            "## Errores comunes\n"
            "- Reportar solo Pearson sin haber visto el scatter: si la relacion\n"
            "  es no lineal, Pearson puede esconder algo importante.\n"
            "- Confundir P(A | B) con P(B | A). Caso clasico: test medico con\n"
            "  positivo no significa enfermedad alta probabilidad si la\n"
            "  enfermedad es rara (paradoja de la base).\n"
            "- Hacer Monte Carlo con N muy chico (1000) y reportar 3 decimales:\n"
            "  esos decimales son ruido.\n"
            "- Bootstrap mal: resamplear SIN reemplazo (te queda el mismo sample\n"
            "  cada vez), o no fijar la seed para reproducibilidad.\n\n"
            "## Resumen\n"
            "- Pearson: relacion lineal. Spearman: relacion monotona (mas\n"
            "  robusta).\n"
            "- Monte Carlo: simulas N veces y contas para estimar P. Error\n"
            "  ~ 1/sqrt(N).\n"
            "- Bootstrap: resample con reemplazo y calcula percentiles para\n"
            "  obtener IC sin asumir distribucion.\n"
            "- Siempre acompaña una estimacion con su incertidumbre.\n"
        ),
        difficulty="advanced",
        category="estadistica",
        order=21,
        track="track-2",
        estimated_duration=60,
        prerequisites_titles=["Estadistica descriptiva: resumir un dataset"],
        exercises=[
            ExerciseTemplate(
                title="Pearson vs Spearman",
                description="Detectar cuando una relacion no es lineal pero si monotona.",
                instructions=(
                    "Implementa `comparar_correlaciones(x, y)` que recibe dos "
                    "pd.Series numericas y devuelve un dict con keys 'pearson' "
                    "y 'spearman' con cada correlacion. Ambas son floats entre "
                    "-1 y 1."
                ),
                starter_code=(
                    "import pandas as pd\n\n"
                    "def comparar_correlaciones(x: pd.Series, y: pd.Series) -> dict:\n"
                    "    # TODO: {'pearson': x.corr(y), 'spearman': x.corr(y, method='spearman')}\n"
                    "    pass\n"
                ),
                hints=[
                    "x.corr(y) sin method= devuelve Pearson.",
                    "x.corr(y, method='spearman') usa rankings.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "devuelve dict con las dos keys",
                        "code": (
                            "import pandas as pd\n"
                            "x = pd.Series([1.0, 2.0, 3.0, 4.0])\n"
                            "y = pd.Series([2.0, 4.0, 6.0, 8.0])\n"
                            "out = comparar_correlaciones(x, y)\n"
                            "assert set(out.keys()) == {'pearson','spearman'}"
                        ),
                    },
                    {
                        "name": "relacion lineal: pearson cercano a 1",
                        "code": (
                            "import pandas as pd\n"
                            "x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])\n"
                            "y = pd.Series([2.0, 4.0, 6.0, 8.0, 10.0])\n"
                            "out = comparar_correlaciones(x, y)\n"
                            "assert abs(out['pearson'] - 1.0) < 1e-9"
                        ),
                    },
                    {
                        "name": "relacion cubica: spearman > pearson",
                        "code": (
                            "import pandas as pd\n"
                            "import numpy as np\n"
                            "x = pd.Series(np.linspace(-5, 5, 50))\n"
                            "# y = x^3 es monotona pero no lineal\n"
                            "y = pd.Series(x.values ** 3)\n"
                            "out = comparar_correlaciones(x, y)\n"
                            "# Spearman captura monotonia perfecta\n"
                            "assert abs(out['spearman'] - 1.0) < 1e-9\n"
                            "# Pearson es alto pero no perfecto\n"
                            "assert out['pearson'] < 1.0"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Monte Carlo: suma de dos dados",
                description="Simular N tiradas y estimar P(suma == valor_objetivo).",
                instructions=(
                    "Implementa `prob_suma_dados(valor_objetivo, n=100_000, seed=0)` "
                    "que simula `n` tiradas de dos dados (cada uno 1..6 inclusive) "
                    "y devuelve la probabilidad estimada (float) de que la suma "
                    "sea igual a `valor_objetivo`. Usa np.random.default_rng(seed)."
                ),
                starter_code=(
                    "import numpy as np\n\n"
                    "def prob_suma_dados(valor_objetivo: int, n: int = 100_000, seed: int = 0) -> float:\n"
                    "    # TODO: rng = np.random.default_rng(seed)\n"
                    "    # d1 = rng.integers(1, 7, size=n)  # 7 exclusivo\n"
                    "    # d2 = rng.integers(1, 7, size=n)\n"
                    "    # return float((d1 + d2 == valor_objetivo).mean())\n"
                    "    pass\n"
                ),
                hints=[
                    "rng.integers(low, high, size=n) — high es EXCLUSIVO. Para 1..6 usar (1, 7).",
                    "(d1 + d2 == valor).mean() te da la proporcion en un solo paso.",
                    "Devolve un float Python (usa float(...) si pandas/numpy te devuelve scalar).",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "devuelve un float",
                        "code": (
                            "p = prob_suma_dados(7, n=1000, seed=0)\n"
                            "assert isinstance(p, float)"
                        ),
                    },
                    {
                        "name": "suma 7 da probabilidad cercana a 0.167",
                        "code": (
                            "# 6/36 combinaciones (1+6, 2+5, ..., 6+1) → 0.1667\n"
                            "p = prob_suma_dados(7, n=200_000, seed=0)\n"
                            "assert abs(p - 6/36) < 0.01, f'esperaba ~0.167, obtuve {p}'"
                        ),
                    },
                    {
                        "name": "suma 2 da probabilidad cercana a 0.028",
                        "code": (
                            "# 1/36 combinaciones (1+1)\n"
                            "p = prob_suma_dados(2, n=200_000, seed=0)\n"
                            "assert abs(p - 1/36) < 0.01, f'esperaba ~0.028, obtuve {p}'"
                        ),
                    },
                    {
                        "name": "suma imposible da 0 (suma 13)",
                        "code": (
                            "p = prob_suma_dados(13, n=10_000, seed=0)\n"
                            "assert p == 0.0"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="IC 95% de la media con bootstrap",
                description="Resamplear con reemplazo y devolver percentiles 2.5/97.5 de las medias.",
                instructions=(
                    "Implementa `ic_media_bootstrap(datos, n_resamples=2000, "
                    "seed=0)` que recibe un array/lista de numeros y devuelve "
                    "una tupla (lim_inferior, lim_superior) del IC del 95% de "
                    "la media estimado por bootstrap. Usar "
                    "`np.random.default_rng(seed)` y `np.percentile`."
                ),
                starter_code=(
                    "import numpy as np\n\n"
                    "def ic_media_bootstrap(datos, n_resamples: int = 2000, seed: int = 0) -> tuple:\n"
                    "    # TODO: rng = np.random.default_rng(seed)\n"
                    "    # medias = np.empty(n_resamples)\n"
                    "    # for i in range(n_resamples):\n"
                    "    #     muestra = rng.choice(datos, size=len(datos), replace=True)\n"
                    "    #     medias[i] = muestra.mean()\n"
                    "    # bajo = np.percentile(medias, 2.5); alto = np.percentile(medias, 97.5)\n"
                    "    # return (bajo, alto)\n"
                    "    pass\n"
                ),
                hints=[
                    "rng.choice(datos, size=n, replace=True) es el resampleo con reemplazo.",
                    "np.percentile(medias, 2.5) y np.percentile(medias, 97.5) dan los limites.",
                    "Devolve una tupla (float, float), no un array.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "devuelve una tupla de 2 floats",
                        "code": (
                            "out = ic_media_bootstrap([1.0,2.0,3.0,4.0,5.0], seed=0)\n"
                            "assert isinstance(out, tuple) and len(out) == 2\n"
                            "assert isinstance(float(out[0]), float)\n"
                            "assert isinstance(float(out[1]), float)"
                        ),
                    },
                    {
                        "name": "el intervalo contiene la media muestral",
                        "code": (
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "datos = rng.normal(10.0, 2.0, 200)\n"
                            "bajo, alto = ic_media_bootstrap(datos, seed=42)\n"
                            "media = float(datos.mean())\n"
                            "assert bajo <= media <= alto"
                        ),
                    },
                    {
                        "name": "ancho razonable (no demasiado grande ni cero)",
                        "code": (
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "datos = rng.normal(10.0, 2.0, 200)\n"
                            "bajo, alto = ic_media_bootstrap(datos, seed=42)\n"
                            "ancho = alto - bajo\n"
                            "# para normal(10, 2) con n=200, IC tipico ~ +/- 0.28\n"
                            "assert 0.0 < ancho < 1.5"
                        ),
                    },
                    {
                        "name": "reproducibilidad con misma seed",
                        "code": (
                            "out1 = ic_media_bootstrap([1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0], seed=7)\n"
                            "out2 = ic_media_bootstrap([1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0], seed=7)\n"
                            "assert isinstance(out1, tuple) and len(out1) == 2, "
                            "'ic_media_bootstrap tiene que devolver una tupla (bajo, alto)'\n"
                            "assert out1 == out2, 'con la misma seed el intervalo tiene que repetirse'"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 1 · Tu primer clasificador con scikit-learn",
        description=(
            "Aprendizaje supervisado en 3 ideas: features vs target, "
            "train/test split y el API fit/predict. Entrena un LogisticRegression "
            "y un KNN sobre iris."
        ),
        content=(
            "# ML 1: tu primer clasificador con scikit-learn\n\n"
            "Los tracks anteriores te dieron Python solido y la caja de "
            "herramientas de Data Science (NumPy, Pandas, matplotlib, "
            "estadistica). En este bloque empieza el Track 3: **Machine "
            "Learning clasico** con `scikit-learn`.\n\n"
            "## Tres ideas para empezar\n\n"
            "### 1. Aprendizaje supervisado = mapear X a y\n\n"
            "Un problema de aprendizaje supervisado tiene dos piezas:\n\n"
            "- **X** (features / caracteristicas): una matriz `n_samples x n_features` "
            "con lo que **observas** de cada ejemplo. En iris: 4 columnas numericas "
            "(largo y ancho del sepalo y del petalo).\n"
            "- **y** (target / etiqueta): un vector de longitud `n_samples` con "
            "lo que **quieres predecir**. Puede ser una categoria (clasificacion) "
            "o un numero (regresion). En iris: la especie (setosa / versicolor / "
            "virginica).\n\n"
            "Un modelo de ML es una funcion `f` tal que `y_estimado = f(X)`. El "
            "**entrenamiento** aprende los parametros de `f` a partir de datos "
            "vistos.\n\n"
            "> Regla mental: si no puedes describir X e y en una frase, no tienes "
            "un problema de ML todavia — tienes un problema de definicion de "
            "producto.\n\n"
            "### 2. Train / test split evita autoengano\n\n"
            "Si evaluas el modelo sobre los mismos datos con los que lo "
            "entrenaste, el modelo puede memorizar y darte 100% de accuracy sin "
            "haber aprendido nada generalizable. Por eso se separa el dataset:\n\n"
            "- **train**: 70-80% del dataset. El modelo lo ve y ajusta sus "
            "parametros.\n"
            "- **test**: 20-30% del dataset. Se guarda escondido; solo se usa al "
            "final para medir performance.\n\n"
            "```python\n"
            "from sklearn.model_selection import train_test_split\n\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y,\n"
            "    test_size=0.3,       # 30% para test\n"
            "    random_state=42,     # reproducible\n"
            "    stratify=y,          # mantiene proporcion de clases\n"
            ")\n"
            "```\n\n"
            "**Notas clave:**\n\n"
            "- `random_state=42` fija la semilla del RNG interno; sin esto cada "
            "corrida da un split distinto y no puedes reproducir resultados.\n"
            "- `stratify=y` es crucial en clasificacion desbalanceada: garantiza "
            "que la proporcion de cada clase en train y test sea la misma que en "
            "el dataset original. Sin esto, un split puede dejarte con 0 muestras "
            "de una clase en test.\n\n"
            "### 3. sklearn expone una API uniforme fit/predict\n\n"
            "Cualquier modelo de sklearn (`LogisticRegression`, `KNeighborsClassifier`, "
            "`DecisionTreeClassifier`, `RandomForestClassifier`, ...) implementa el "
            "mismo trio de metodos:\n\n"
            "1. `modelo.fit(X_train, y_train)` — aprende parametros.\n"
            "2. `modelo.predict(X_test)` — genera predicciones.\n"
            "3. `modelo.score(X_test, y_test)` — retorna la metrica por defecto "
            "(accuracy para clasificadores).\n\n"
            "Esta uniformidad es la que hace potente a sklearn: cambiar de modelo "
            "es literalmente cambiar una linea.\n\n"
            "## Tu primer clasificador: LogisticRegression\n\n"
            "A pesar del nombre, `LogisticRegression` es un **clasificador** — "
            "modela la probabilidad de cada clase con una funcion sigmoide sobre "
            "una combinacion lineal de features.\n\n"
            "```python\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.metrics import accuracy_score\n\n"
            "modelo = LogisticRegression(random_state=42, max_iter=500)\n"
            "modelo.fit(X_train, y_train)\n"
            "predicciones = modelo.predict(X_test)\n"
            "acc = accuracy_score(y_test, predicciones)\n"
            "print(f'accuracy = {acc:.3f}')\n"
            "```\n\n"
            "**Por que `max_iter=500`?** El default es 100; para datasets pequenos "
            "o mal escalados el optimizador puede no converger en 100 iteraciones "
            "y te sale un `ConvergenceWarning`. Subirlo es mas simple que "
            "estandarizar features en este primer contacto.\n\n"
            "## Otro modelo con la misma API: KNN\n\n"
            "`KNeighborsClassifier` no aprende parametros — memoriza el train y "
            "para cada punto de test busca los `k` vecinos mas cercanos, votando "
            "la clase mayoritaria.\n\n"
            "```python\n"
            "from sklearn.neighbors import KNeighborsClassifier\n\n"
            "knn = KNeighborsClassifier(n_neighbors=3)\n"
            "knn.fit(X_train, y_train)\n"
            "acc_knn = knn.score(X_test, y_test)\n"
            "```\n\n"
            "**Elegir `k`:**\n\n"
            "- `k=1`: sensible al ruido (memoriza un solo vecino).\n"
            "- `k` grande: promedia mucho, puede perder patrones locales.\n"
            "- Regla intuitiva: `k` impar y pequeno (3, 5, 7). En produccion se "
            "elige con cross-validation.\n\n"
            "## Metrica: accuracy\n\n"
            "`accuracy = predicciones correctas / total`. Es la metrica default "
            "de `score()` en clasificadores. Es simple e intuitiva pero **enganosa "
            "en desbalance**: si el 95% de los datos son de una clase, predecir "
            "siempre esa clase te da 95% de accuracy sin haber aprendido nada. "
            "Para esos casos existen precision, recall y f1 — los veras en la "
            "proxima leccion.\n\n"
            "## Errores comunes de la primera semana en ML\n\n"
            "1. **Entrenar y evaluar sobre el mismo split** — el clasico "
            '"tengo 100% de accuracy". Casi siempre significa que estas '
            "midiendo sobre train, o que la variable objetivo se filtro en X "
            "(data leakage).\n"
            "2. **Olvidar `random_state`** — sin semilla, cada corrida da un "
            "resultado distinto y no puedes comparar experimentos.\n"
            "3. **No estratificar** — con clases desbalanceadas o datasets "
            "pequenos, `stratify=y` puede ser la diferencia entre un split "
            "aprovechable y uno inutil.\n"
            "4. **Confundir `predict` con `predict_proba`** — el primero devuelve "
            "la clase (0/1/2 en iris), el segundo la probabilidad de cada clase "
            "(matriz n x n_clases).\n"
            "5. **Comparar accuracies sin test comun** — LogReg 0.90 y KNN 0.88 "
            "no significa nada si se corrieron sobre splits distintos. Fija "
            "`X_train, X_test, y_train, y_test` una vez y reusalos.\n\n"
            "## Resumen\n\n"
            "- ML supervisado = `f(X) -> y`, entrenada sobre datos historicos.\n"
            "- `train_test_split(random_state=42, stratify=y)` es tu punto de "
            "partida siempre. Sin split limpio no hay conclusion valida.\n"
            "- sklearn expone `fit`, `predict` y `score` en todos sus modelos. "
            "Cambiar de LogReg a KNN son 2 imports y una linea.\n"
            "- accuracy es el primer contacto con metricas de clasificacion; en "
            "la proxima leccion apareceran precision, recall y confusion matrix "
            "para escenarios reales.\n"
        ),
        difficulty="intermediate",
        category="ml-fundamentos",
        order=22,
        track="track-3",
        estimated_duration=55,
        prerequisites_titles=[
            "Estadistica descriptiva",
        ],
        exercises=[
            ExerciseTemplate(
                title="Split de iris estratificado",
                description=(
                    "Divide el dataset iris en train/test manteniendo la "
                    "proporcion de clases."
                ),
                instructions=(
                    "Implementa `preparar_iris_split(df)` que recibe el DataFrame "
                    "de iris (columnas `sepal_length, sepal_width, petal_length, "
                    "petal_width, species`) y devuelve la tupla `(X_train, X_test, "
                    "y_train, y_test)` con `test_size=0.3`, `random_state=42` y "
                    "`stratify=y`. X debe ser un DataFrame con las 4 features; y "
                    "una Series con la columna `species`."
                ),
                starter_code=(
                    "from sklearn.model_selection import train_test_split\n"
                    "\n"
                    "\n"
                    "def preparar_iris_split(df):\n"
                    "    # TODO: separa features (X) del target (y)\n"
                    "    # TODO: llama a train_test_split con test_size=0.3,\n"
                    "    #       random_state=42 y stratify=y\n"
                    "    # TODO: retorna (X_train, X_test, y_train, y_test)\n"
                    "    ...\n"
                ),
                hints=[
                    "X = df[['sepal_length','sepal_width','petal_length','petal_width']]; y = df['species'].",
                    "train_test_split retorna 4 objetos: X_train, X_test, y_train, y_test en ese orden.",
                    "stratify=y garantiza 3 muestras de cada clase en test (dataset 30 filas, 30% => 9).",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "tamanos correctos 21 train / 9 test",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n'\n"
                            "for i, sp in enumerate(['setosa']*10 + ['versicolor']*10 + ['virginica']*10):\n"
                            "    csv += f'{5.0+0.1*i},{3.0+0.05*i},{1.5+0.2*i},{0.3+0.1*i},{sp}\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X_train, X_test, y_train, y_test = preparar_iris_split(df)\n"
                            "assert len(X_train) == 21, len(X_train)\n"
                            "assert len(X_test) == 9, len(X_test)\n"
                            "assert len(y_train) == 21\n"
                            "assert len(y_test) == 9"
                        ),
                    },
                    {
                        "name": "X mantiene las 4 columnas de features",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n'\n"
                            "for i, sp in enumerate(['setosa']*10 + ['versicolor']*10 + ['virginica']*10):\n"
                            "    csv += f'{5.0+0.1*i},{3.0+0.05*i},{1.5+0.2*i},{0.3+0.1*i},{sp}\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X_train, X_test, _, _ = preparar_iris_split(df)\n"
                            "esperado = ['sepal_length','sepal_width','petal_length','petal_width']\n"
                            "assert list(X_train.columns) == esperado, list(X_train.columns)\n"
                            "assert list(X_test.columns) == esperado"
                        ),
                    },
                    {
                        "name": "stratify preserva 3 por clase en test",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n'\n"
                            "for i, sp in enumerate(['setosa']*10 + ['versicolor']*10 + ['virginica']*10):\n"
                            "    csv += f'{5.0+0.1*i},{3.0+0.05*i},{1.5+0.2*i},{0.3+0.1*i},{sp}\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "_, _, _, y_test = preparar_iris_split(df)\n"
                            "conteo = y_test.value_counts().to_dict()\n"
                            "assert conteo == {'setosa': 3, 'versicolor': 3, 'virginica': 3}, conteo"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Primer LogisticRegression sobre iris",
                description=(
                    "Entrena un modelo LogisticRegression y devuelve accuracy en test."
                ),
                instructions=(
                    "Implementa `entrenar_logreg(X_train, y_train, X_test, y_test)` "
                    "que crea un `LogisticRegression(random_state=42, max_iter=500)`, "
                    "lo entrena con `fit`, predice sobre `X_test` y devuelve la "
                    "accuracy como `float` (usa `accuracy_score` o `.score`)."
                ),
                starter_code=(
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.metrics import accuracy_score\n"
                    "\n"
                    "\n"
                    "def entrenar_logreg(X_train, y_train, X_test, y_test):\n"
                    "    # TODO: crea LogisticRegression(random_state=42, max_iter=500)\n"
                    "    # TODO: fit sobre X_train, y_train\n"
                    "    # TODO: retorna float(accuracy_score(y_test, modelo.predict(X_test)))\n"
                    "    ...\n"
                ),
                hints=[
                    "El API es tres pasos: instanciar, fit, predict.",
                    "random_state=42 es lo que garantiza que tu resultado sea reproducible.",
                    "En iris con solo 30 filas y clases muy separables, LogReg puede llegar a 1.0.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "retorna un float en [0, 1]",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc = entrenar_logreg(X_train, y_train, X_test, y_test)\n"
                            "assert isinstance(acc, float), type(acc)\n"
                            "assert 0.0 <= acc <= 1.0, acc"
                        ),
                    },
                    {
                        "name": "accuracy = 1.0 sobre iris con seed 42",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc = entrenar_logreg(X_train, y_train, X_test, y_test)\n"
                            "assert acc == 1.0, acc"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Comparar KNN con distintos k",
                description=(
                    "Escribe una funcion que entrene KNN para varios valores de k "
                    "y devuelva el mapa k -> accuracy."
                ),
                instructions=(
                    "Implementa `comparar_knn(X_train, y_train, X_test, y_test, ks)` "
                    "que recibe una lista `ks` de enteros (p.ej. [3, 5, 7]) y "
                    "devuelve un `dict` `{k: accuracy_float}` entrenando un "
                    "`KNeighborsClassifier(n_neighbors=k)` distinto para cada k. "
                    "Usa la accuracy sobre `X_test`."
                ),
                starter_code=(
                    "from sklearn.neighbors import KNeighborsClassifier\n"
                    "from sklearn.metrics import accuracy_score\n"
                    "\n"
                    "\n"
                    "def comparar_knn(X_train, y_train, X_test, y_test, ks):\n"
                    "    # TODO: recorre ks, entrena un KNeighborsClassifier(n_neighbors=k),\n"
                    "    #       calcula accuracy en X_test y guarda en un dict\n"
                    "    ...\n"
                ),
                hints=[
                    "Cada k necesita su propio modelo entrenado — no reuses el mismo objeto entre iteraciones.",
                    "float(accuracy_score(y_test, modelo.predict(X_test))) o modelo.score(X_test, y_test).",
                    "En iris con 30 filas, k=3 y k=5 dan accuracies parecidos porque las clases estan muy separadas.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "devuelve dict con las k pedidas",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "res = comparar_knn(X_train, y_train, X_test, y_test, [3, 5])\n"
                            "assert isinstance(res, dict), type(res)\n"
                            "assert set(res.keys()) == {3, 5}, res.keys()\n"
                            "for v in res.values():\n"
                            "    assert isinstance(v, float), type(v)\n"
                            "    assert 0.0 <= v <= 1.0, v"
                        ),
                    },
                    {
                        "name": "accuracies iguales a 0.8889 para k=3 y k=5",
                        "code": (
                            "import io\n"
                            "import math\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "res = comparar_knn(X_train, y_train, X_test, y_test, [3, 5])\n"
                            "assert math.isclose(res[3], 8/9, abs_tol=1e-4), res[3]\n"
                            "assert math.isclose(res[5], 8/9, abs_tol=1e-4), res[5]"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 2 · Metricas mas alla de accuracy",
        description=(
            "Confusion matrix, precision, recall y f1. Cuando accuracy "
            "engana y como leer un clasificador bajo desbalance real."
        ),
        content=(
            "# ML 2: metricas mas alla de accuracy\n\n"
            "En la leccion anterior mediste tu primer clasificador con "
            "`accuracy_score`. En iris con 3 clases perfectamente "
            "balanceadas y muy separables, accuracy es informativa. En "
            "problemas reales (fraude, deteccion medica, spam, churn) "
            "accuracy casi siempre miente. Aqui aprendes las metricas que "
            "usan los equipos de ML en produccion.\n\n"
            "## Tres ideas para entender clasificacion real\n\n"
            "### 1. Accuracy engana con desbalance\n\n"
            "Ejemplo canonico: un dataset de fraude bancario donde el 99% "
            "de las transacciones son legitimas. Un modelo que **siempre "
            "predice legitimo** tiene 99% de accuracy y detecta 0 fraudes. "
            "En terminos de valor de negocio, ese modelo es peor que un "
            "generador aleatorio.\n\n"
            "Con clases desbalanceadas la clase mayoritaria domina la "
            'cuenta. Accuracy no distingue entre "acerto todos los '
            'faciles" y "acerto lo dificil".\n\n'
            "### 2. La confusion matrix te da la verdad completa\n\n"
            "Para clasificacion binaria (positivo/negativo), toda la "
            "informacion sobre las predicciones cabe en una matriz 2x2:\n\n"
            "```\n"
            "                predijo=0    predijo=1\n"
            "actual=0           TN           FP\n"
            "actual=1           FN           TP\n"
            "```\n\n"
            "- **TP (True Positive)**: real=1, predijo=1. Aciertos "
            "positivos.\n"
            "- **TN (True Negative)**: real=0, predijo=0. Aciertos "
            "negativos.\n"
            "- **FP (False Positive)**: real=0, predijo=1. Falsa alarma. "
            "Ej: usuario marcado como fraudulento cuando no lo era.\n"
            "- **FN (False Negative)**: real=1, predijo=0. Pase por alto. "
            "Ej: fraude no detectado, tumor no diagnosticado.\n\n"
            "sklearn lo devuelve con:\n\n"
            "```python\n"
            "from sklearn.metrics import confusion_matrix\n"
            "cm = confusion_matrix(y_true, y_pred)\n"
            "# cm[0, 0] = TN,  cm[0, 1] = FP\n"
            "# cm[1, 0] = FN,  cm[1, 1] = TP\n"
            "```\n\n"
            "> **Ordena importa:** el default de sklearn es "
            "`labels=sorted(unique)`, asi que para 0/1 el orden es "
            '"actual 0" arriba, "actual 1" abajo — coincide con la '
            'convencion academica. Para etiquetas string ("spam"/"ham") '
            "el orden alfabetico puede sorprenderte; siempre pasa `labels=` "
            "explicito.\n\n"
            "### 3. Precision, recall y f1: tres angulos del mismo problema\n\n"
            "A partir de la confusion matrix salen las tres metricas "
            "canonicas de clasificacion binaria:\n\n"
            "**Precision** = `TP / (TP + FP)`. De todo lo que predije como "
            "positivo, cuanto lo era. Optimizala cuando el costo de un "
            "**falso positivo** es alto — ej: acusar de fraude a un "
            "cliente inocente le genera friccion; queremos estar seguros "
            "antes de senalar.\n\n"
            "**Recall** (o sensibilidad) = `TP / (TP + FN)`. De todos los "
            "positivos reales, cuantos atrape. Optimizala cuando el costo "
            "de un **falso negativo** es alto — ej: no detectar un tumor "
            "cuando lo hay puede matar al paciente; preferimos falsas "
            "alarmas.\n\n"
            "**F1-score** = media armonica de precision y recall = "
            "`2 * P * R / (P + R)`. Un solo numero que penaliza dejar "
            "cualquiera de las dos en cero. Es el default cuando no tienes "
            "una razon fuerte para priorizar precision sobre recall.\n\n"
            "sklearn los expone en un solo call:\n\n"
            "```python\n"
            "from sklearn.metrics import (\n"
            "    precision_score, recall_score, f1_score,\n"
            "    classification_report,\n"
            ")\n"
            "print('precision:', precision_score(y_true, y_pred))\n"
            "print('recall:',    recall_score(y_true, y_pred))\n"
            "print('f1:',        f1_score(y_true, y_pred))\n"
            "\n"
            "# Todo junto (por clase + weighted):\n"
            "print(classification_report(y_true, y_pred))\n"
            "```\n\n"
            "## El tradeoff precision-recall\n\n"
            "Casi todos los clasificadores devuelven una **probabilidad** "
            "(via `predict_proba`) y aplican un **umbral** por defecto de "
            "0.5 para pasar a 0/1. Ese umbral es un dial:\n\n"
            "- **Umbral alto** (ej: 0.9): solo llamas positivo cuando el "
            "modelo esta muy seguro. Precision sube, recall baja.\n"
            "- **Umbral bajo** (ej: 0.2): llamas positivo con poca "
            "evidencia. Recall sube, precision baja.\n\n"
            "En produccion casi nunca usas el 0.5 default; eliges el "
            "umbral segun el costo relativo de FP vs FN en tu caso de uso.\n\n"
            "## Ejemplo con desbalance real: por que f1 es tu red\n\n"
            "Imagina un dataset de churn con 90 clientes que no se van y "
            '10 que si. Un modelo que predice "nadie se va":\n\n'
            "- accuracy = 90/100 = **0.90**  <- se ve genial\n"
            "- precision = indefinida (division por 0)\n"
            "- recall = 0/10 = **0.0**  <- no atrapo un solo churn\n"
            "- f1 = **0.0**  <- la metrica te grita que el modelo es "
            "inutil\n\n"
            "Un modelo decente que detecta 5 de 10 churns sin falsas "
            "alarmas:\n\n"
            "- accuracy = 95/100 = 0.95\n"
            "- precision = 5/5 = 1.00\n"
            "- recall = 5/10 = 0.50\n"
            "- f1 = 0.667\n\n"
            "El salto real (0 a 0.667 en f1) refleja el valor de negocio "
            "que accuracy no captura (subio de 0.90 a 0.95, apenas 5 "
            "puntos).\n\n"
            "## Errores comunes\n\n"
            "1. **Reportar solo accuracy en clasificacion binaria** — la "
            "audiencia tecnica pedira precision y recall en el siguiente "
            "mensaje.\n"
            "2. **Optimizar la metrica equivocada** — si tu problema es "
            '"encontrar todos los fraudes" (recall) pero reportas y '
            "optimizas accuracy, terminaras con un modelo elegante que no "
            "sirve.\n"
            "3. **Confundir precision (metrica) con precision (numero de "
            "decimales)** — precision de un clasificador es un ratio 0-1, "
            "no tiene nada que ver con float precision.\n"
            "4. **Comparar f1 entre modelos entrenados con distinto split** "
            "— fija `random_state` y reusa el mismo `X_test`, `y_test`.\n"
            "5. **`zero_division` warnings** — cuando no hay positivos "
            "predichos, sklearn levanta `UndefinedMetricWarning`. Pasa "
            "`zero_division=0` explicito para tratarlo como 0 en pipelines "
            "reales.\n\n"
            "## Resumen\n\n"
            "- Accuracy es la metrica de entrada; para clasificacion real "
            "reporta al menos precision, recall y f1.\n"
            "- La confusion matrix es la fuente de verdad: TP, TN, FP, FN "
            "definen todas las demas.\n"
            "- Precision minimiza falsas alarmas; recall minimiza casos "
            "perdidos; f1 los balancea.\n"
            "- Bajo desbalance, accuracy alta puede coexistir con f1 = 0. "
            "Siempre revisa la confusion matrix antes de celebrar.\n"
        ),
        difficulty="intermediate",
        category="ml-evaluacion",
        order=23,
        track="track-3",
        estimated_duration=50,
        prerequisites_titles=[
            "ML 1 · Tu primer clasificador con scikit-learn",
        ],
        exercises=[
            ExerciseTemplate(
                title="Extraer TN/FP/FN/TP de la confusion matrix",
                description=(
                    "Escribe una funcion que devuelva los 4 componentes de "
                    "la confusion matrix binaria como dict."
                ),
                instructions=(
                    "Implementa `desglose_confusion(y_true, y_pred)` que "
                    "usa `sklearn.metrics.confusion_matrix` sobre etiquetas "
                    "binarias 0/1 y devuelve un `dict` con las claves "
                    "`tn`, `fp`, `fn`, `tp` (todos ints). Recuerda: "
                    "`cm[0,0]=tn`, `cm[0,1]=fp`, `cm[1,0]=fn`, `cm[1,1]=tp`."
                ),
                starter_code=(
                    "from sklearn.metrics import confusion_matrix\n"
                    "\n"
                    "\n"
                    "def desglose_confusion(y_true, y_pred):\n"
                    "    # TODO: cm = confusion_matrix(y_true, y_pred, labels=[0, 1])\n"
                    "    # TODO: retorna dict {'tn': int(cm[0,0]), ...}\n"
                    "    ...\n"
                ),
                hints=[
                    "Pasa labels=[0, 1] explicito para que el orden sea determinista.",
                    "int(cm[i, j]) para asegurar que cada valor sea Python int, no numpy int64.",
                    "El dict debe tener exactamente las 4 claves tn, fp, fn, tp.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "caso balanceado 4-4-1-1",
                        "code": (
                            "res = desglose_confusion(\n"
                            "    [1, 0, 1, 1, 0, 1, 0, 0, 1, 0],\n"
                            "    [1, 0, 1, 0, 0, 1, 1, 0, 1, 0],\n"
                            ")\n"
                            "assert isinstance(res, dict), type(res)\n"
                            "assert set(res.keys()) == {'tn','fp','fn','tp'}, res.keys()\n"
                            "assert res == {'tn': 4, 'fp': 1, 'fn': 1, 'tp': 4}, res"
                        ),
                    },
                    {
                        "name": "todos correctos (FP=FN=0)",
                        "code": (
                            "res = desglose_confusion([0, 0, 1, 1], [0, 0, 1, 1])\n"
                            "assert res == {'tn': 2, 'fp': 0, 'fn': 0, 'tp': 2}, res"
                        ),
                    },
                    {
                        "name": "modelo dummy predice todo 0 con desbalance",
                        "code": (
                            "y_true = [0]*90 + [1]*10\n"
                            "y_pred = [0]*100\n"
                            "res = desglose_confusion(y_true, y_pred)\n"
                            "assert res == {'tn': 90, 'fp': 0, 'fn': 10, 'tp': 0}, res"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Precision, recall y f1 de un clasificador",
                description=("Devuelve un dict con las tres metricas usando sklearn."),
                instructions=(
                    "Implementa `metricas_binarias(y_true, y_pred)` que "
                    "retorna un `dict` con las claves `precision`, "
                    "`recall`, `f1` (floats en [0, 1]). Usa "
                    "`precision_score`, `recall_score` y `f1_score` de "
                    "`sklearn.metrics` con `zero_division=0` para "
                    "manejar el caso sin positivos predichos."
                ),
                starter_code=(
                    "from sklearn.metrics import precision_score, recall_score, f1_score\n"
                    "\n"
                    "\n"
                    "def metricas_binarias(y_true, y_pred):\n"
                    "    # TODO: retorna dict con 'precision', 'recall', 'f1'\n"
                    "    # TODO: usa zero_division=0 en cada score\n"
                    "    ...\n"
                ),
                hints=[
                    "float(precision_score(...)) evita numpy.float64 en el dict.",
                    "zero_division=0 devuelve 0.0 cuando no hay positivos predichos, en vez de lanzar warning.",
                    "El caso balanceado del ejercicio anterior (TP=4, FP=1, FN=1) da 0.8 en las tres metricas.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "caso balanceado da 0.8 en las 3",
                        "code": (
                            "import math\n"
                            "res = metricas_binarias(\n"
                            "    [1, 0, 1, 1, 0, 1, 0, 0, 1, 0],\n"
                            "    [1, 0, 1, 0, 0, 1, 1, 0, 1, 0],\n"
                            ")\n"
                            "assert set(res.keys()) == {'precision','recall','f1'}, res.keys()\n"
                            "for v in res.values():\n"
                            "    assert isinstance(v, float), type(v)\n"
                            "assert math.isclose(res['precision'], 0.8, abs_tol=1e-4), res\n"
                            "assert math.isclose(res['recall'], 0.8, abs_tol=1e-4), res\n"
                            "assert math.isclose(res['f1'], 0.8, abs_tol=1e-4), res"
                        ),
                    },
                    {
                        "name": "modelo dummy todo 0: precision=recall=f1=0",
                        "code": (
                            "res = metricas_binarias([0]*90 + [1]*10, [0]*100)\n"
                            "assert res['precision'] == 0.0, res\n"
                            "assert res['recall'] == 0.0, res\n"
                            "assert res['f1'] == 0.0, res"
                        ),
                    },
                    {
                        "name": "prediccion perfecta da 1.0 en las 3",
                        "code": (
                            "res = metricas_binarias([0, 1, 0, 1, 1], [0, 1, 0, 1, 1])\n"
                            "assert res['precision'] == 1.0, res\n"
                            "assert res['recall'] == 1.0, res\n"
                            "assert res['f1'] == 1.0, res"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Accuracy vs f1 bajo desbalance",
                description=(
                    "Demuestra por que accuracy sola no basta: compara "
                    "las metricas de un modelo dummy y uno decente sobre "
                    "un dataset 90/10."
                ),
                instructions=(
                    "Implementa `comparar_dummy_vs_decente(y_true, "
                    "pred_dummy, pred_decente)` que recibe tres listas de "
                    "0/1 y retorna un `dict` con dos entradas: `'dummy'` y "
                    "`'decente'`. Cada entrada es a su vez un dict con "
                    "`accuracy` y `f1` (floats con `zero_division=0`). "
                    "La idea es que el caller vea de un vistazo que la "
                    "diferencia real esta en f1, no en accuracy."
                ),
                starter_code=(
                    "from sklearn.metrics import accuracy_score, f1_score\n"
                    "\n"
                    "\n"
                    "def comparar_dummy_vs_decente(y_true, pred_dummy, pred_decente):\n"
                    "    # TODO: para cada prediccion calcula accuracy y f1\n"
                    "    # TODO: retorna {'dummy': {'accuracy': ..., 'f1': ...},\n"
                    "    #                'decente': {'accuracy': ..., 'f1': ...}}\n"
                    "    ...\n"
                ),
                hints=[
                    "Reutiliza accuracy_score(y_true, pred) y f1_score(y_true, pred, zero_division=0).",
                    "El dummy sobre 90/10 con todo 0 da accuracy=0.9 y f1=0.0.",
                    "El modelo decente con 5 TP, 0 FP, 5 FN sobre 90/10 da accuracy=0.95 y f1=0.6667.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "dummy y decente correctamente calculados",
                        "code": (
                            "import math\n"
                            "y_true = [0]*90 + [1]*10\n"
                            "pred_dummy = [0]*100\n"
                            "pred_decente = [0]*90 + [1]*5 + [0]*5\n"
                            "res = comparar_dummy_vs_decente(y_true, pred_dummy, pred_decente)\n"
                            "assert set(res.keys()) == {'dummy','decente'}, res.keys()\n"
                            "assert math.isclose(res['dummy']['accuracy'], 0.9, abs_tol=1e-4), res\n"
                            "assert math.isclose(res['dummy']['f1'], 0.0, abs_tol=1e-4), res\n"
                            "assert math.isclose(res['decente']['accuracy'], 0.95, abs_tol=1e-4), res\n"
                            "assert math.isclose(res['decente']['f1'], 2/3, abs_tol=1e-3), res"
                        ),
                    },
                    {
                        "name": "moraleja: f1 discrimina, accuracy no",
                        "code": (
                            "y_true = [0]*90 + [1]*10\n"
                            "res = comparar_dummy_vs_decente(y_true, [0]*100, [0]*90 + [1]*5 + [0]*5)\n"
                            "# accuracy sube apenas 0.05 (0.90 -> 0.95)\n"
                            "assert res['decente']['accuracy'] - res['dummy']['accuracy'] < 0.10\n"
                            "# f1 salta drasticamente (0.0 -> 0.667)\n"
                            "assert res['decente']['f1'] - res['dummy']['f1'] > 0.60"
                        ),
                    },
                    {
                        "name": "cada sub-entrada tiene exactamente accuracy y f1",
                        "code": (
                            "res = comparar_dummy_vs_decente([0,1,1], [0,0,0], [0,1,1])\n"
                            "for label in ('dummy', 'decente'):\n"
                            "    sub = res[label]\n"
                            "    assert set(sub.keys()) == {'accuracy', 'f1'}, sub.keys()\n"
                            "    for v in sub.values():\n"
                            "        assert isinstance(v, float), type(v)"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 3 · Features escaladas y Pipelines",
        description=(
            "StandardScaler, OneHotEncoder y Pipeline. Como preparar "
            "features numericas y categoricas sin data leakage."
        ),
        content=(
            "# ML 3: features escaladas y pipelines\n\n"
            "Ya tienes el flujo `split -> fit -> predict -> metricas`. En "
            "un dataset real, entre `split` y `fit` hay un paso crucial "
            "que decide si tu modelo funciona: **preprocesar las features** "
            "(escalar numericas, codificar categoricas). Hacerlo mal es la "
            "causa mas comun de resultados enganosamente buenos en "
            "notebooks que se desmoronan en produccion.\n\n"
            "## Tres ideas para preprocesar bien\n\n"
            "### 1. La mayoria de modelos asumen features 'razonables'\n\n"
            '"Razonables" significa: en escalas comparables y sin '
            "categorias como strings crudas. Si dejas los defaults del "
            "dataset:\n\n"
            "- **LogisticRegression** con features de escalas muy "
            "distintas (ej: edad 0-100 y ingreso 0-100000) puede no "
            "converger en `max_iter` iteraciones o quedar dominada por "
            "la feature de mayor magnitud.\n"
            "- **KNN** calcula distancias euclideas — una feature 1000x "
            "mas grande que otra la vuelve invisible.\n"
            "- **SVM con kernel RBF** es extremadamente sensible a la "
            "escala; sin escalar es casi inutil.\n"
            "- **Arboles de decision y Random Forest** son la excepcion: "
            "no les afecta la escala (particionan por umbral en cada "
            "feature individual). Pero siguen necesitando categoricas "
            "codificadas numericamente.\n\n"
            "**Regla de dedo:** casi siempre `StandardScaler` (media 0, "
            "desviacion 1) para numericas y `OneHotEncoder` para "
            "categoricas. Ahi arrancas.\n\n"
            "### 2. Pipeline evita el data leakage clasico\n\n"
            "El error mas comun del primer mes en ML es escalar antes de "
            "hacer split:\n\n"
            "```python\n"
            "# ANTI-PATTERN: data leakage\n"
            "scaler = StandardScaler()\n"
            "X_all = scaler.fit_transform(X)      # usa mean/std de TODO\n"
            "X_train, X_test = train_test_split(X_all, ...)\n"
            "```\n\n"
            "Por que es un problema: `mean` y `std` de `X_all` incluyen "
            "las filas de test. El modelo, al entrenarse, esta viendo "
            "indirectamente la distribucion de test — informacion que "
            "**en produccion no vas a tener**.\n\n"
            "La solucion correcta es aprender los parametros del "
            "preprocesador **solo con train** y aplicarlos igual sobre "
            "test:\n\n"
            "```python\n"
            "X_train, X_test = train_test_split(X, ...)\n"
            "scaler = StandardScaler()\n"
            "X_train_s = scaler.fit_transform(X_train)  # calcula + aplica\n"
            "X_test_s  = scaler.transform(X_test)       # SOLO aplica\n"
            "```\n\n"
            "Escribirlo asi cada vez es tedioso y facil de romper. "
            "`Pipeline` de sklearn lo automatiza:\n\n"
            "```python\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.linear_model import LogisticRegression\n\n"
            "pipe = Pipeline([\n"
            "    ('sc', StandardScaler()),\n"
            "    ('lr', LogisticRegression(random_state=42, max_iter=500)),\n"
            "])\n"
            "pipe.fit(X_train, y_train)         # escala + entrena\n"
            "acc = pipe.score(X_test, y_test)   # escala test con params de train + evalua\n"
            "```\n\n"
            "El pipeline garantiza que `StandardScaler.fit` solo ve "
            "`X_train`. Es lo que usan los equipos serios.\n\n"
            "### 3. ColumnTransformer maneja columnas heterogeneas\n\n"
            "Los datasets reales tienen una mezcla: `edad` (numerica), "
            "`plan` (categorica), `pais` (categorica), `ingreso` "
            "(numerica). No puedes aplicar `StandardScaler` a un string. "
            "`ColumnTransformer` es el switch:\n\n"
            "```python\n"
            "from sklearn.compose import ColumnTransformer\n"
            "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n\n"
            "preproc = ColumnTransformer([\n"
            "    ('num', StandardScaler(),                 ['edad', 'ingreso']),\n"
            "    ('cat', OneHotEncoder(sparse_output=False), ['plan']),\n"
            "])\n"
            "```\n\n"
            "El resultado es una matriz numerica lista para el modelo. "
            "Cada categoria se vuelve una columna 0/1: `plan` con valores "
            "`{basico, pro, enterprise}` da 3 columnas.\n\n"
            "**Flags utiles de OneHotEncoder:**\n"
            "- `sparse_output=False`: devuelve `np.ndarray` denso en vez "
            "de matriz sparse (mas facil de inspeccionar con pandas).\n"
            "- `handle_unknown='ignore'`: si en produccion aparece una "
            "categoria nueva, no crashea (la ignora en vez de lanzar).\n"
            "- `drop='first'`: elimina la primera categoria para evitar "
            "colinealidad (necesario en regresion lineal, opcional en "
            "arboles/redes).\n\n"
            "Se combina con Pipeline igual de facil:\n\n"
            "```python\n"
            "pipe = Pipeline([\n"
            "    ('prep', preproc),\n"
            "    ('lr', LogisticRegression(max_iter=500)),\n"
            "])\n"
            "pipe.fit(X_train, y_train)\n"
            "```\n\n"
            "## Debug: entender los nombres de features generadas\n\n"
            "Despues del preprocesador es dificil saber que columna es "
            "que. Usa `get_feature_names_out()` para verlo:\n\n"
            "```python\n"
            "preproc.fit(X_train)\n"
            "print(preproc.get_feature_names_out())\n"
            "# ['num__edad', 'num__ingreso', 'cat__plan_basico',\n"
            "#  'cat__plan_enterprise', 'cat__plan_pro']\n"
            "```\n\n"
            "El prefijo `num__` / `cat__` viene del nombre del "
            "transformador; despues del `__` va el nombre original y, "
            "para OHE, la categoria.\n\n"
            "## Errores comunes\n\n"
            "1. **`fit_transform` sobre el dataset completo** — data "
            "leakage. Escala/PCA/imputer siempre despues del split o "
            "dentro de un Pipeline.\n"
            "2. **`.fit` sobre test** — nunca. Test solo recibe "
            "`.transform` con los parametros aprendidos de train.\n"
            "3. **Escalar arboles/random forest** — no hace dano pero es "
            "trabajo inutil.\n"
            "4. **One-hot encodear una feature con miles de categorias** "
            "— genera miles de columnas. Para alta cardinalidad usa "
            "target encoding o embeddings; OHE es para 3-30 categorias.\n"
            "5. **Olvidar `handle_unknown='ignore'`** — en produccion un "
            "usuario con plan `enterprise-plus` que no vio train hara "
            "crashear la API entera.\n\n"
            "## Resumen\n\n"
            "- Escala numericas con `StandardScaler`; codifica "
            "categoricas con `OneHotEncoder(sparse_output=False, "
            "handle_unknown='ignore')`.\n"
            "- Envuelve todo en un `Pipeline` para que el preprocesador "
            "aprenda solo de train — sin leakage por defecto.\n"
            "- `ColumnTransformer` combina scalers y encoders segun el "
            "tipo de columna.\n"
            "- `.get_feature_names_out()` para inspeccionar la salida.\n"
            "- Arboles no necesitan escalado, pero si necesitan que las "
            "categoricas ya sean numericas.\n"
        ),
        difficulty="intermediate",
        category="ml-features",
        order=24,
        track="track-3",
        estimated_duration=50,
        prerequisites_titles=[
            "ML 2 · Metricas mas alla de accuracy",
        ],
        exercises=[
            ExerciseTemplate(
                title="Escalar train/test con StandardScaler",
                description=(
                    "Aprende los parametros del scaler SOLO con train y "
                    "aplicalos igual sobre test."
                ),
                instructions=(
                    "Implementa `escalar_train_test(X_train, X_test)` "
                    "que crea un `StandardScaler`, hace `fit_transform` "
                    "sobre `X_train`, hace `transform` sobre `X_test` "
                    "(NO fit) y devuelve la tupla `(X_train_s, X_test_s)` "
                    "como `np.ndarray`."
                ),
                starter_code=(
                    "from sklearn.preprocessing import StandardScaler\n"
                    "\n"
                    "\n"
                    "def escalar_train_test(X_train, X_test):\n"
                    "    # TODO: sc = StandardScaler()\n"
                    "    # TODO: X_train_s = sc.fit_transform(X_train)\n"
                    "    # TODO: X_test_s  = sc.transform(X_test)  # NO fit\n"
                    "    # TODO: retorna (X_train_s, X_test_s)\n"
                    "    ...\n"
                ),
                hints=[
                    "fit_transform SOLO sobre X_train — es la esencia de no leakage.",
                    "transform (sin fit) sobre X_test aplica media/std aprendidas.",
                    "El resultado es np.ndarray; los tests no asumen DataFrame.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "X_train_s tiene media 0 y std 1 por columna",
                        "code": (
                            "import numpy as np\n"
                            "X_train = np.array([[1.0, 100.0], [2.0, 200.0], [3.0, 300.0], [4.0, 400.0]])\n"
                            "X_test = np.array([[2.5, 250.0]])\n"
                            "X_train_s, X_test_s = escalar_train_test(X_train, X_test)\n"
                            "assert np.allclose(X_train_s.mean(axis=0), [0.0, 0.0], atol=1e-9), X_train_s.mean(axis=0)\n"
                            "assert np.allclose(X_train_s.std(axis=0), [1.0, 1.0], atol=1e-9), X_train_s.std(axis=0)"
                        ),
                    },
                    {
                        "name": "X_test se transforma con params de train (2.5,250 -> 0,0)",
                        "code": (
                            "import numpy as np\n"
                            "X_train = np.array([[1.0, 100.0], [2.0, 200.0], [3.0, 300.0], [4.0, 400.0]])\n"
                            "X_test = np.array([[2.5, 250.0]])\n"
                            "_, X_test_s = escalar_train_test(X_train, X_test)\n"
                            "assert np.allclose(X_test_s, [[0.0, 0.0]], atol=1e-9), X_test_s"
                        ),
                    },
                    {
                        "name": "no filtra info de test al scaler (leakage guard)",
                        "code": (
                            "import numpy as np\n"
                            "X_train = np.array([[1.0], [2.0], [3.0], [4.0]])\n"
                            "X_test  = np.array([[1000.0]])  # outlier extremo\n"
                            "X_train_s, _ = escalar_train_test(X_train, X_test)\n"
                            "# si el scaler se hubiera fitteado con test, el std seria enorme\n"
                            "# y X_train_s tendria valores minusculos. Aqui debe seguir teniendo std=1.\n"
                            "assert np.allclose(X_train_s.std(axis=0), [1.0], atol=1e-9), X_train_s.std(axis=0)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Pipeline con StandardScaler + LogisticRegression",
                description=(
                    "Envuelve el preprocesador y el modelo en un Pipeline "
                    "para evitar leakage por default."
                ),
                instructions=(
                    "Implementa `pipeline_logreg(X_train, y_train, "
                    "X_test, y_test)` que crea un `Pipeline` con dos "
                    "pasos: `('sc', StandardScaler())` y "
                    "`('lr', LogisticRegression(random_state=42, "
                    "max_iter=500))`. Entrena con `fit`, retorna la "
                    "accuracy sobre `X_test` como `float`."
                ),
                starter_code=(
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "\n"
                    "\n"
                    "def pipeline_logreg(X_train, y_train, X_test, y_test):\n"
                    "    # TODO: pipe = Pipeline([('sc', StandardScaler()),\n"
                    "    #                        ('lr', LogisticRegression(random_state=42, max_iter=500))])\n"
                    "    # TODO: pipe.fit(X_train, y_train)\n"
                    "    # TODO: return float(pipe.score(X_test, y_test))\n"
                    "    ...\n"
                ),
                hints=[
                    "Pipeline([(nombre, estimador), ...]) — orden importa: primero preproc, ultimo modelo.",
                    "pipe.fit escala con train y entrena; pipe.score escala test con params de train y evalua.",
                    "Sobre iris con random_state=42 y stratify=y, el pipeline llega a 1.0.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "pipeline retorna float 1.0 sobre iris seed 42",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc = pipeline_logreg(X_train, y_train, X_test, y_test)\n"
                            "assert isinstance(acc, float), type(acc)\n"
                            "assert acc == 1.0, acc"
                        ),
                    },
                    {
                        "name": "el pipeline corre y retorna accuracy valida",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc = pipeline_logreg(X_train, y_train, X_test, y_test)\n"
                            "assert 0.0 <= acc <= 1.0"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="ColumnTransformer con numericas + categoricas",
                description=(
                    "Preprocesa un DataFrame heterogeneo mezclando "
                    "StandardScaler para numericas y OneHotEncoder para "
                    "categoricas en un solo objeto."
                ),
                instructions=(
                    "Implementa `preprocess_mixto(df, num_cols, cat_cols)` "
                    "que crea un `ColumnTransformer` con dos "
                    "transformadores: `('num', StandardScaler(), "
                    "num_cols)` y `('cat', OneHotEncoder(sparse_output="
                    "False, handle_unknown='ignore'), cat_cols)`. Hace "
                    "`fit_transform` sobre `df` y devuelve la matriz "
                    "resultante como `np.ndarray`."
                ),
                starter_code=(
                    "from sklearn.compose import ColumnTransformer\n"
                    "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
                    "\n"
                    "\n"
                    "def preprocess_mixto(df, num_cols, cat_cols):\n"
                    "    # TODO: ct = ColumnTransformer([\n"
                    "    #     ('num', StandardScaler(), num_cols),\n"
                    "    #     ('cat', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), cat_cols),\n"
                    "    # ])\n"
                    "    # TODO: retorna ct.fit_transform(df)\n"
                    "    ...\n"
                ),
                hints=[
                    "El orden en la lista define el orden de columnas de salida: primero numericas.",
                    "sparse_output=False evita tener que llamar .toarray() para inspeccionar el resultado.",
                    "handle_unknown='ignore' es la variante que no crashea con categorias nuevas.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "shape correcto (5, 5) = 2 num + 3 cat",
                        "code": (
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'edad': [25, 40, 30, 55, 22],\n"
                            "    'ingreso': [30000, 60000, 45000, 90000, 25000],\n"
                            "    'plan': ['basico', 'pro', 'basico', 'enterprise', 'basico'],\n"
                            "})\n"
                            "out = preprocess_mixto(df, ['edad', 'ingreso'], ['plan'])\n"
                            "assert out.shape == (5, 5), out.shape"
                        ),
                    },
                    {
                        "name": "columnas numericas escaladas a media 0 std 1",
                        "code": (
                            "import numpy as np\n"
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'edad': [25, 40, 30, 55, 22],\n"
                            "    'ingreso': [30000, 60000, 45000, 90000, 25000],\n"
                            "    'plan': ['basico', 'pro', 'basico', 'enterprise', 'basico'],\n"
                            "})\n"
                            "out = preprocess_mixto(df, ['edad', 'ingreso'], ['plan'])\n"
                            "assert abs(out[:, 0].mean()) < 1e-9, out[:, 0].mean()\n"
                            "assert abs(out[:, 0].std() - 1.0) < 1e-9, out[:, 0].std()\n"
                            "assert abs(out[:, 1].mean()) < 1e-9\n"
                            "assert abs(out[:, 1].std() - 1.0) < 1e-9"
                        ),
                    },
                    {
                        "name": "one-hot: cada fila tiene exactamente un 1 en las cols categoricas",
                        "code": (
                            "import numpy as np\n"
                            "import pandas as pd\n"
                            "df = pd.DataFrame({\n"
                            "    'edad': [25, 40, 30, 55, 22],\n"
                            "    'ingreso': [30000, 60000, 45000, 90000, 25000],\n"
                            "    'plan': ['basico', 'pro', 'basico', 'enterprise', 'basico'],\n"
                            "})\n"
                            "out = preprocess_mixto(df, ['edad', 'ingreso'], ['plan'])\n"
                            "one_hot = out[:, 2:5]\n"
                            "assert np.array_equal(one_hot.sum(axis=1), [1, 1, 1, 1, 1]), one_hot.sum(axis=1)\n"
                            "# alfabetico: 3 basico + 1 enterprise + 1 pro\n"
                            "assert one_hot.sum(axis=0).tolist() == [3.0, 1.0, 1.0], one_hot.sum(axis=0)"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 4 · Regresion: LinearRegression, MSE, RMSE y R2",
        description=(
            "Predecir un numero (no una clase): regresion lineal, "
            "metricas MSE/RMSE/R2 y Ridge para casos con "
            "multicolinealidad."
        ),
        content=(
            "# ML 4: regresion con LinearRegression\n\n"
            "Hasta aqui todo fue **clasificacion**: predecir una categoria "
            "(iris = setosa/versicolor/virginica, churn = 0/1). Este "
            "bloque cambia el juego: predecir un **numero continuo** — "
            "el precio de una casa, la demanda del proximo mes, el "
            "tiempo hasta el primer pago. Es **regresion**.\n\n"
            "## Tres ideas para regresion\n\n"
            "### 1. Clasificacion vs regresion: no es lo mismo\n\n"
            "El shape del problema cambia todo:\n\n"
            "| Aspecto             | Clasificacion         | Regresion             |\n"
            "|---------------------|-----------------------|-----------------------|\n"
            "| Target              | Categoria (0/1, A/B)  | Numero real           |\n"
            "| Modelo base         | LogisticRegression    | LinearRegression      |\n"
            "| Metrica intuitiva   | accuracy, f1          | MSE, RMSE, R2         |\n"
            "| `.score()` default  | accuracy              | R2                    |\n"
            '| Error tipico        | "clase mal predicha" | "me equivoque por X"  |\n\n'
            "El API de sklearn es identico: `fit`, `predict`, `score`. "
            "Solo cambian los estimadores y las metricas.\n\n"
            "### 2. LinearRegression aprende una combinacion lineal\n\n"
            "El modelo mas simple de regresion asume que:\n\n"
            "```\n"
            "y = w_1 * x_1 + w_2 * x_2 + ... + w_n * x_n + b\n"
            "```\n\n"
            "El entrenamiento encuentra los pesos `w_i` y el intercepto "
            "`b` que **minimizan el error cuadratico** sobre train.\n\n"
            "```python\n"
            "from sklearn.linear_model import LinearRegression\n\n"
            "modelo = LinearRegression()\n"
            "modelo.fit(X_train, y_train)\n\n"
            "# inspeccion\n"
            "print('coefs:', modelo.coef_)         # array de w_i\n"
            "print('intercept:', modelo.intercept_) # b\n\n"
            "y_pred = modelo.predict(X_test)       # array de floats\n"
            "```\n\n"
            "**Interpretacion:** si `coef_[0] == 3.0`, significa que "
            "cuando la feature 0 sube 1 unidad, `y` sube 3.0 unidades "
            "(manteniendo el resto constante). Este es el gran atractivo "
            "de LinReg: es **directamente interpretable**.\n\n"
            "### 3. Tres metricas para regresion\n\n"
            "**MSE (Mean Squared Error)** = media de `(y_true - y_pred)^2`. "
            "Penaliza mucho errores grandes (el cuadrado los "
            "amplifica). El problema: sus unidades son las del target "
            "**al cuadrado** — si predices precios en euros, MSE esta "
            "en euros^2, dificil de interpretar.\n\n"
            "**RMSE (Root Mean Squared Error)** = `sqrt(MSE)`. Vuelve a "
            "las unidades del target: RMSE=1500 sobre precios de casas "
            'significa "me equivoco tipicamente en 1500 euros". Es la '
            "metrica que reportas a un stakeholder.\n\n"
            "**R2 (coeficiente de determinacion)** = fraccion de la "
            "varianza de `y` que el modelo captura. Va de -inf a 1.0:\n"
            "- **R2 = 1.0**: predicciones perfectas.\n"
            "- **R2 = 0.0**: el modelo no mejora sobre predecir la "
            "media de `y`.\n"
            "- **R2 < 0**: el modelo es **peor** que predecir la media. "
            "Casi siempre significa que tienes un bug o un problema muy "
            "no-lineal para LinReg.\n\n"
            "```python\n"
            "from sklearn.metrics import mean_squared_error, r2_score\n"
            "import numpy as np\n\n"
            "mse  = mean_squared_error(y_test, y_pred)\n"
            "rmse = np.sqrt(mse)\n"
            "r2   = r2_score(y_test, y_pred)\n"
            "```\n\n"
            "> Alternativa reciente: `root_mean_squared_error` te da "
            "RMSE directo. El viejo flag `mean_squared_error(..., "
            "squared=False)` esta deprecado en sklearn 1.6+; usa "
            "`sqrt(mse)` o la nueva funcion.\n\n"
            "## Ridge: regresion con regularizacion\n\n"
            "Cuando dos features son casi identicas (**multicolinealidad**), "
            "LinearRegression puede asignar pesos absurdos (uno "
            "positivo enorme y el otro negativo enorme que se "
            "cancelan). Es matematicamente correcto pero pesimo para "
            "generalizar.\n\n"
            "**Ridge** agrega una penalizacion al tamano de los coefs "
            "(`alpha * ||w||^2` al costo). Los pesos quedan mas "
            "chicos y balanceados:\n\n"
            "```python\n"
            "from sklearn.linear_model import Ridge\n\n"
            "modelo = Ridge(alpha=1.0)  # alpha=0 == LinReg; alpha grande == mas penalizacion\n"
            "modelo.fit(X_train, y_train)\n"
            "```\n\n"
            "**Regla de dedo:** si tienes features correlacionadas o "
            "notas coefs raros, cambia `LinearRegression()` por "
            "`Ridge(alpha=1.0)` como default. La perdida en R2 sobre "
            "train es minima y ganas robustez.\n\n"
            "**Lasso** (`Lasso(alpha=0.1)`) es similar pero manda "
            "algunos coefs a exactamente **cero** — util para feature "
            "selection automatica. Ridge y Lasso son las dos formas "
            "canonicas de regularizacion lineal (L2 y L1 "
            "respectivamente).\n\n"
            "## El pipeline completo de regresion\n\n"
            "Combinando lo de leccion anterior:\n\n"
            "```python\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.linear_model import Ridge\n\n"
            "pipe = Pipeline([\n"
            "    ('sc', StandardScaler()),   # escalar es importante para Ridge/Lasso\n"
            "    ('reg', Ridge(alpha=1.0)),\n"
            "])\n"
            "pipe.fit(X_train, y_train)\n"
            "rmse = np.sqrt(mean_squared_error(y_test, pipe.predict(X_test)))\n"
            "```\n\n"
            "**Ridge y Lasso SI necesitan escalado**: la penalizacion es "
            "sobre `||w||`, y una feature en escala grande naturalmente "
            "tiene coef pequeno — la regularizacion la castigaria menos "
            "sin escalar. StandardScaler nivela el terreno.\n\n"
            "## Errores comunes\n\n"
            "1. **Reportar R2 sin contexto** — un R2 de 0.6 puede ser "
            "excelente en un dominio ruidoso (finanzas) y terrible en "
            "otro (fisica de laboratorio). Siempre comparalo contra un "
            "baseline trivial (predecir la media).\n"
            '2. **RMSE sin unidades** — "mi modelo tiene RMSE=1500" '
            'no significa nada; "me equivoco tipicamente en 1500 euros '
            'sobre precios que van de 50k a 500k" es una frase util.\n'
            "3. **LinReg sobre datos no-lineales** — si el patron real "
            "es `y = x^2`, LinReg tendra R2 mediocre por diseno. Prueba "
            "PolynomialFeatures o un modelo no-lineal (arbol, RF).\n"
            "4. **Regularizar sin escalar** — Ridge y Lasso asumen "
            "features en escala similar. Sin StandardScaler la "
            "regularizacion pesa mas a features de escala pequena.\n"
            "5. **Ignorar residuos** — R2 alto no significa que los "
            "errores esten uniformemente distribuidos. Grafica "
            "`y_pred vs residuos` para detectar patrones no capturados.\n\n"
            "## Resumen\n\n"
            "- Regresion predice un numero: `LinearRegression` es el "
            "modelo base, mismo API (`fit`, `predict`, `score`) que "
            "clasificacion.\n"
            "- Metricas: MSE (unidades^2), RMSE (unidades del target, "
            "el que reportas), R2 (fraccion de varianza explicada, "
            "compare-friendly).\n"
            "- Con multicolinealidad o riesgo de overfitting, usa "
            "`Ridge(alpha=1.0)` como default. Escala las features "
            "antes.\n"
            "- Interpretabilidad: `coef_` te dice cuanto sube `y` por "
            "unidad de cada feature; `intercept_` es el valor esperado "
            "cuando todas las features son 0.\n"
        ),
        difficulty="intermediate",
        category="ml-regresion",
        order=25,
        track="track-3",
        estimated_duration=55,
        prerequisites_titles=[
            "ML 3 · Features escaladas y Pipelines",
        ],
        exercises=[
            ExerciseTemplate(
                title="Evaluar LinearRegression con MSE y R2",
                description=(
                    "Entrena un modelo lineal y devuelve las metricas "
                    "clasicas de regresion como dict."
                ),
                instructions=(
                    "Implementa `evaluar_regresion(X_train, y_train, "
                    "X_test, y_test)` que entrena un `LinearRegression`, "
                    "predice sobre test y retorna un `dict` con las "
                    "claves `mse`, `rmse`, `r2` (todos floats). "
                    "Usa `mean_squared_error` para MSE, "
                    "`math.sqrt(mse)` o `numpy.sqrt(mse)` para RMSE y "
                    "`r2_score` para R2."
                ),
                starter_code=(
                    "import math\n"
                    "from sklearn.linear_model import LinearRegression\n"
                    "from sklearn.metrics import mean_squared_error, r2_score\n"
                    "\n"
                    "\n"
                    "def evaluar_regresion(X_train, y_train, X_test, y_test):\n"
                    "    # TODO: entrena LinearRegression().fit(X_train, y_train)\n"
                    "    # TODO: y_pred = modelo.predict(X_test)\n"
                    "    # TODO: retorna dict con 'mse', 'rmse' (=sqrt(mse)), 'r2'\n"
                    "    ...\n"
                ),
                hints=[
                    "float(mean_squared_error(y_test, y_pred)) evita numpy.float64.",
                    "rmse = math.sqrt(mse). No hay que llamar mean_squared_error dos veces.",
                    "Sobre y = 2x + 1 exacto, MSE deberia ser 0 y R2 igual a 1.0.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "y = 2x + 1 exacto: mse=0, rmse=0, r2=1",
                        "code": (
                            "import math\n"
                            "import numpy as np\n"
                            "X_tr = np.array([[1.0],[2.0],[3.0],[4.0],[5.0]])\n"
                            "y_tr = np.array([3.0, 5.0, 7.0, 9.0, 11.0])\n"
                            "X_te = np.array([[6.0],[7.0]])\n"
                            "y_te = np.array([13.0, 15.0])\n"
                            "res = evaluar_regresion(X_tr, y_tr, X_te, y_te)\n"
                            "assert set(res.keys()) == {'mse','rmse','r2'}, res.keys()\n"
                            "assert math.isclose(res['mse'], 0.0, abs_tol=1e-9), res\n"
                            "assert math.isclose(res['rmse'], 0.0, abs_tol=1e-9), res\n"
                            "assert math.isclose(res['r2'], 1.0, abs_tol=1e-9), res"
                        ),
                    },
                    {
                        "name": "todas las metricas son floats",
                        "code": (
                            "import numpy as np\n"
                            "X_tr = np.array([[1.0],[2.0],[3.0]])\n"
                            "y_tr = np.array([2.0, 4.0, 7.0])\n"
                            "X_te = np.array([[4.0],[5.0]])\n"
                            "y_te = np.array([8.0, 10.0])\n"
                            "res = evaluar_regresion(X_tr, y_tr, X_te, y_te)\n"
                            "for v in res.values():\n"
                            "    assert isinstance(v, float), type(v)"
                        ),
                    },
                    {
                        "name": "rmse = sqrt(mse) siempre",
                        "code": (
                            "import math\n"
                            "import numpy as np\n"
                            "X_tr = np.array([[1.0],[2.0],[3.0]])\n"
                            "y_tr = np.array([2.0, 4.0, 7.0])  # no lineal\n"
                            "X_te = np.array([[4.0],[5.0]])\n"
                            "y_te = np.array([8.0, 10.0])\n"
                            "res = evaluar_regresion(X_tr, y_tr, X_te, y_te)\n"
                            "assert math.isclose(res['rmse'], math.sqrt(res['mse']), abs_tol=1e-9), res"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Predecir valores nuevos",
                description=(
                    "Entrena un LinearRegression y usalo para predecir "
                    "puntos que no vio."
                ),
                instructions=(
                    "Implementa `predecir_lineal(X_train, y_train, "
                    "X_nuevo)` que entrena un `LinearRegression` sobre "
                    "train y devuelve `model.predict(X_nuevo)` como "
                    "`np.ndarray`. Los tests pasan datos exactos y "
                    "verifican predicciones conocidas."
                ),
                starter_code=(
                    "from sklearn.linear_model import LinearRegression\n"
                    "\n"
                    "\n"
                    "def predecir_lineal(X_train, y_train, X_nuevo):\n"
                    "    # TODO: modelo = LinearRegression().fit(X_train, y_train)\n"
                    "    # TODO: return modelo.predict(X_nuevo)\n"
                    "    ...\n"
                ),
                hints=[
                    "predict acepta una matriz 2D — para un solo punto pasa [[x1, x2, ...]].",
                    "Sobre y = 2x + 1, pred(10) = 21 y pred(20) = 41.",
                    "El return de predict es np.ndarray; no lo conviertas a lista.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "y = 2x+1 exacto: pred(10)=21, pred(20)=41",
                        "code": (
                            "import numpy as np\n"
                            "X_tr = np.array([[1.0],[2.0],[3.0],[4.0],[5.0]])\n"
                            "y_tr = np.array([3.0, 5.0, 7.0, 9.0, 11.0])\n"
                            "X_new = np.array([[10.0],[20.0]])\n"
                            "pred = predecir_lineal(X_tr, y_tr, X_new)\n"
                            "assert isinstance(pred, np.ndarray), type(pred)\n"
                            "assert np.allclose(pred, [21.0, 41.0], atol=1e-9), pred"
                        ),
                    },
                    {
                        "name": "regresion multivariable: y = 3*x1 + 2*x2 + 1",
                        "code": (
                            "import numpy as np\n"
                            "X_tr = np.array([\n"
                            "    [0.0, 0.0], [1.0, 0.0], [0.0, 1.0],\n"
                            "    [1.0, 1.0], [2.0, 3.0], [4.0, 2.0],\n"
                            "])\n"
                            "y_tr = np.array([1.0, 4.0, 3.0, 6.0, 13.0, 17.0])  # 3*x1 + 2*x2 + 1\n"
                            "X_new = np.array([[5.0, 5.0], [10.0, 0.0]])\n"
                            "pred = predecir_lineal(X_tr, y_tr, X_new)\n"
                            "assert np.allclose(pred, [26.0, 31.0], atol=1e-9), pred"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Ridge vs LinearRegression con multicolinealidad",
                description=(
                    "Demuestra el valor de la regularizacion: Ridge "
                    "reparte los coefs entre features colineales "
                    "manteniendo R2 competitivo."
                ),
                instructions=(
                    "Implementa `comparar_lin_vs_ridge(X_train, "
                    "y_train, X_test, y_test, alpha)` que entrena un "
                    "`LinearRegression` y un `Ridge(alpha=alpha, "
                    "random_state=42)` sobre el mismo train, y devuelve "
                    "un `dict` con las claves `lin_r2`, `ridge_r2`, "
                    "`lin_coefs_norm`, `ridge_coefs_norm`. Usa "
                    "`numpy.linalg.norm(model.coef_)` para la norma L2 "
                    "de los coefs."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "from sklearn.linear_model import LinearRegression, Ridge\n"
                    "from sklearn.metrics import r2_score\n"
                    "\n"
                    "\n"
                    "def comparar_lin_vs_ridge(X_train, y_train, X_test, y_test, alpha):\n"
                    "    # TODO: entrena LinReg y Ridge(alpha=alpha, random_state=42)\n"
                    "    # TODO: retorna dict con 'lin_r2', 'ridge_r2',\n"
                    "    #       'lin_coefs_norm', 'ridge_coefs_norm'\n"
                    "    ...\n"
                ),
                hints=[
                    "np.linalg.norm(model.coef_) es la norma L2 (sqrt(sum(w_i^2))).",
                    "float(np.linalg.norm(...)) para asegurar Python float en el dict.",
                    "Con features casi identicas, ||coefs_ridge|| < ||coefs_lin|| casi siempre.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "estructura del dict y tipos",
                        "code": (
                            "import numpy as np\n"
                            "X_tr = np.array([[1.0, 1.0],[2.0, 2.0],[3.0, 3.0],[4.0, 4.0]])\n"
                            "y_tr = np.array([2.0, 4.0, 6.0, 8.0])\n"
                            "X_te = np.array([[5.0, 5.0],[6.0, 6.0]])\n"
                            "y_te = np.array([10.0, 12.0])\n"
                            "res = comparar_lin_vs_ridge(X_tr, y_tr, X_te, y_te, alpha=1.0)\n"
                            "assert set(res.keys()) == {'lin_r2','ridge_r2','lin_coefs_norm','ridge_coefs_norm'}, res.keys()\n"
                            "for v in res.values():\n"
                            "    assert isinstance(v, float), type(v)"
                        ),
                    },
                    {
                        "name": "Ridge reduce ||coefs|| bajo multicolinealidad",
                        "code": (
                            "import numpy as np\n"
                            "# features casi identicas (x1 ~ x2)\n"
                            "X_tr = np.array([\n"
                            "    [1.0, 1.01],[2.0, 2.02],[3.0, 3.01],\n"
                            "    [4.0, 4.02],[5.0, 5.03],[6.0, 6.01],[7.0, 7.02],\n"
                            "])\n"
                            "y_tr = np.array([3.0, 5.0, 7.0, 9.0, 11.0, 13.0, 15.0])\n"
                            "X_te = np.array([[8.0, 8.03],[9.0, 9.01],[10.0, 10.02]])\n"
                            "y_te = np.array([17.0, 19.0, 21.0])\n"
                            "res = comparar_lin_vs_ridge(X_tr, y_tr, X_te, y_te, alpha=1.0)\n"
                            "assert res['ridge_coefs_norm'] < res['lin_coefs_norm'], res\n"
                            "# ambos deben tener r2 razonables\n"
                            "assert res['lin_r2'] > 0.9, res\n"
                            "assert res['ridge_r2'] > 0.9, res"
                        ),
                    },
                    {
                        "name": "alpha minusculo hace que Ridge tienda a LinReg",
                        "code": (
                            "import numpy as np\n"
                            "X_tr = np.array([[1.0, 1.01],[2.0, 2.02],[3.0, 3.01],[4.0, 4.02]])\n"
                            "y_tr = np.array([3.0, 5.0, 7.0, 9.0])\n"
                            "X_te = np.array([[5.0, 5.02]])\n"
                            "y_te = np.array([11.0])\n"
                            "res = comparar_lin_vs_ridge(X_tr, y_tr, X_te, y_te, alpha=1e-6)\n"
                            "# con alpha minusculo, las normas casi coinciden\n"
                            "assert abs(res['lin_coefs_norm'] - res['ridge_coefs_norm']) < 0.1, res"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 5 · Arboles y Random Forest",
        description=(
            "Primer modelo no-lineal: DecisionTree y RandomForest. "
            "Interpretabilidad via feature_importances_ y por que "
            "RF suele ser el mejor baseline en tabular."
        ),
        content=(
            "# ML 5: arboles de decision y Random Forest\n\n"
            "Todos los modelos que has visto (LogReg, LinReg, Ridge) son "
            "**lineales**: buscan una combinacion lineal de features + "
            "un umbral. Con relaciones no-lineales o interacciones "
            "entre features, no dan la talla. Este bloque presenta los "
            "**arboles de decision** y su ensamble estrella: **Random "
            "Forest** — el default no-lineal que casi siempre te da un "
            "baseline competitivo en datos tabulares.\n\n"
            "## Tres ideas para entender arboles\n\n"
            "### 1. Un arbol es una serie de if-then sobre features\n\n"
            "Un DecisionTree divide el espacio en rectangulos. En cada "
            "nodo elige una feature y un umbral que **maximiza la "
            "pureza** de los grupos resultantes (usa Gini o entropia "
            "para clasificacion, MSE para regresion).\n\n"
            "```\n"
            "raiz:  petal_width <= 0.8 ?\n"
            "  si  -> setosa                        # nodo hoja puro\n"
            "  no  -> petal_length <= 4.75 ?\n"
            "        si -> versicolor                # nodo hoja\n"
            "        no -> virginica                 # nodo hoja\n"
            "```\n\n"
            "Ventajas frente a modelos lineales:\n\n"
            "- **No-linealidad**: aprende umbrales, no combinaciones "
            "lineales.\n"
            "- **Sin escalado**: cada split usa una feature aislada; "
            "escalar no cambia nada.\n"
            "- **Sin one-hot obligatorio** para ordinales: puede "
            "particionar por umbral en enteros (0/1/2/3).\n"
            "- **Interpretabilidad**: puedes imprimir el arbol y ver "
            "cada regla.\n\n"
            "Desventaja: **overfittean facil**. Sin restriccion, un "
            "arbol memoriza el train con hojas de una sola muestra. Por "
            "eso siempre se usa con `max_depth` o `min_samples_leaf`.\n\n"
            "```python\n"
            "from sklearn.tree import DecisionTreeClassifier\n\n"
            "arbol = DecisionTreeClassifier(max_depth=3, random_state=42)\n"
            "arbol.fit(X_train, y_train)\n"
            "acc = arbol.score(X_test, y_test)\n"
            "```\n\n"
            "**Parametros que casi siempre tocas:**\n"
            "- `max_depth`: limite duro de profundidad. 3-10 es lo "
            "tipico.\n"
            "- `min_samples_leaf`: minimo de muestras por hoja. "
            "Valores 5-20 evitan hojas ruidosas.\n"
            "- `random_state`: reproducibilidad — sklearn desempata "
            "features iguales al azar.\n\n"
            "### 2. Random Forest promedia muchos arboles\n\n"
            "Un arbol solo es de alta varianza (cambias 3 filas y sale "
            "otro arbol distinto). La idea de **Random Forest** es "
            "entrenar N arboles independientes con dos tipos de "
            "aleatoriedad y promediar sus predicciones:\n\n"
            "1. **Bootstrap sampling**: cada arbol ve un subset "
            "aleatorio de las filas (con reemplazo).\n"
            "2. **Feature subsampling**: en cada split, solo puede "
            "elegir entre `sqrt(n_features)` features (para "
            "clasificacion; `n_features/3` para regresion).\n\n"
            "El promedio reduce varianza sin subir el sesgo. Resultado: "
            "**mismo bias que un arbol solo, mucho menos varianza**.\n\n"
            "```python\n"
            "from sklearn.ensemble import RandomForestClassifier\n\n"
            "rf = RandomForestClassifier(n_estimators=100, random_state=42)\n"
            "rf.fit(X_train, y_train)\n"
            "acc = rf.score(X_test, y_test)\n"
            "```\n\n"
            "**Parametros clave:**\n"
            "- `n_estimators`: cuantos arboles. 100 es el default; "
            "500 rara vez es peor pero tarda mas. Nunca es "
            '"demasiados".\n'
            "- `max_depth`, `min_samples_leaf`: se aplican por arbol.\n"
            "- `n_jobs=-1`: paraleliza el entrenamiento en todos los "
            "cores.\n\n"
            "### 3. feature_importances_: que features usa el modelo\n\n"
            "Tanto DecisionTree como RandomForest exponen "
            "`feature_importances_`: un array de floats en [0, 1] que "
            "suman 1, indicando cuanto contribuye cada feature a las "
            "decisiones del modelo (medido por la reduccion de "
            "impureza que trae al agregarla).\n\n"
            "```python\n"
            "importances = dict(zip(feature_names, rf.feature_importances_))\n"
            "# {'sepal_length': 0.12, 'sepal_width': 0.04,\n"
            "#  'petal_length': 0.40, 'petal_width': 0.44}\n"
            "```\n\n"
            "Interpretacion sobre iris: `petal_width` y `petal_length` "
            "son las que discriminan las especies; `sepal_width` casi "
            "no aporta. Esto **matchea** lo que sabemos del dataset — "
            "un buen indicador de que el modelo aprendio patrones "
            "reales.\n\n"
            "**Uso en la practica:**\n"
            "- Debugging: si una feature que crees importante aparece "
            "con importancia 0, algo esta raro (bug en pipeline, "
            "leakage, feature constante).\n"
            "- Feature selection: entrenas un RF con todas, tiras las "
            "importances=0, reentrenas con menos features (mismo "
            "score, mas rapido).\n"
            "- Storytelling: reportar al stakeholder que features "
            "guian las predicciones (interpretabilidad de alto nivel).\n\n"
            "**Cuidado:** `feature_importances_` esta **sesgada hacia "
            "features de alta cardinalidad** (numericas continuas o "
            "categoricas con muchos niveles) y hacia features "
            "correlacionadas (comparten importancia). Para "
            "interpretabilidad seria, usa `permutation_importance` o "
            "SHAP.\n\n"
            "## Cuando usar cada uno\n\n"
            "| Escenario                              | Modelo         |\n"
            "|----------------------------------------|----------------|\n"
            "| Necesitas explicar cada decision       | DecisionTree   |\n"
            "| Datos tabulares, primer baseline       | RandomForest   |\n"
            "| Muchas features numericas correladas   | RF > LinReg    |\n"
            "| Interacciones no-lineales entre features | RF, no LinReg  |\n"
            "| Fronteras suaves (imagenes, senales)   | Redes neuronales|\n"
            "| Dataset gigante (>10M filas)           | GradientBoosting/LightGBM |\n\n"
            "## Errores comunes\n\n"
            "1. **Arbol sin `max_depth`** — memoriza el train, R2 en "
            "test bajo. Empieza siempre con `max_depth=3-10`.\n"
            "2. **Escalar antes de un arbol** — no rompe nada pero es "
            "trabajo inutil. RF es invariante a la escala.\n"
            "3. **`n_estimators=10`** — ahorra segundos y sacrifica "
            "estabilidad. 100 es el minimo razonable en produccion.\n"
            "4. **Interpretar `feature_importances_` como causalidad** "
            '— importancia no es causa; solo dice "el modelo se '
            'apoyo en esta feature".\n'
            "5. **Olvidar `random_state`** — dos RF con distinta "
            "semilla pueden dar accuracies ligeramente distintas por "
            "el bootstrap. Fijala para experimentos comparables.\n\n"
            "## Resumen\n\n"
            "- `DecisionTree` particiona el espacio con if-then; es "
            "no-lineal, interpretable, no necesita escalado. "
            "Regularizalo con `max_depth`.\n"
            "- `RandomForest` = promedio de muchos arboles con "
            "bootstrap + feature subsampling. Reduce varianza. Baseline "
            "por defecto en tabular.\n"
            "- `feature_importances_` te dice que features usa el "
            "modelo (utilidad grande para debug + storytelling; ojo con "
            "sesgos hacia alta cardinalidad).\n"
            "- Cuando quieras un modelo lineal-interpretable, usa "
            "LogReg/LinReg + coefs; cuando quieras potencia sin tunear, "
            "usa RandomForest con `n_estimators=100`.\n"
        ),
        difficulty="intermediate",
        category="ml-arboles",
        order=26,
        track="track-3",
        estimated_duration=55,
        prerequisites_titles=[
            "ML 4 · Regresion: LinearRegression, MSE, RMSE y R2",
        ],
        exercises=[
            ExerciseTemplate(
                title="DecisionTree con max_depth sobre iris",
                description=(
                    "Entrena un arbol de decision con profundidad "
                    "limitada y devuelve accuracy."
                ),
                instructions=(
                    "Implementa `entrenar_arbol(X_train, y_train, "
                    "X_test, y_test, max_depth)` que crea un "
                    "`DecisionTreeClassifier(max_depth=max_depth, "
                    "random_state=42)`, lo entrena con `fit` y devuelve "
                    "la accuracy sobre `X_test` como `float`."
                ),
                starter_code=(
                    "from sklearn.tree import DecisionTreeClassifier\n"
                    "\n"
                    "\n"
                    "def entrenar_arbol(X_train, y_train, X_test, y_test, max_depth):\n"
                    "    # TODO: dt = DecisionTreeClassifier(max_depth=max_depth, random_state=42)\n"
                    "    # TODO: dt.fit(X_train, y_train)\n"
                    "    # TODO: return float(dt.score(X_test, y_test))\n"
                    "    ...\n"
                ),
                hints=[
                    "random_state=42 es imprescindible para reproducibilidad en split-ties.",
                    "score() en clasificadores devuelve accuracy por default.",
                    "Sobre iris con seed 42 + stratify, max_depth=3 llega a 1.0.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "acc = 1.0 en iris con max_depth=3",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc = entrenar_arbol(X_tr, y_tr, X_te, y_te, max_depth=3)\n"
                            "assert isinstance(acc, float), type(acc)\n"
                            "assert acc == 1.0, acc"
                        ),
                    },
                    {
                        "name": "max_depth=1 da accuracy menor (arbol subajustado)",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc_1 = entrenar_arbol(X_tr, y_tr, X_te, y_te, max_depth=1)\n"
                            "# depth=1 solo separa una clase => acc <= 0.75\n"
                            "assert acc_1 <= 0.75, acc_1"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="RandomForest con n_estimators",
                description=(
                    "Entrena un Random Forest y compara accuracy con " "un arbol solo."
                ),
                instructions=(
                    "Implementa `entrenar_rf(X_train, y_train, X_test, "
                    "y_test, n_estimators)` que crea un "
                    "`RandomForestClassifier(n_estimators=n_estimators, "
                    "random_state=42)`, lo entrena y devuelve la "
                    "accuracy sobre `X_test` como `float`."
                ),
                starter_code=(
                    "from sklearn.ensemble import RandomForestClassifier\n"
                    "\n"
                    "\n"
                    "def entrenar_rf(X_train, y_train, X_test, y_test, n_estimators):\n"
                    "    # TODO: rf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)\n"
                    "    # TODO: rf.fit(X_train, y_train)\n"
                    "    # TODO: return float(rf.score(X_test, y_test))\n"
                    "    ...\n"
                ),
                hints=[
                    "n_estimators es el numero de arboles del bosque.",
                    "random_state=42 fija el bootstrap y feature subsampling para reproducibilidad.",
                    "Sobre iris seed 42, RF con 100 arboles llega a 1.0.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "RF con 100 arboles = 1.0 sobre iris seed 42",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc = entrenar_rf(X_tr, y_tr, X_te, y_te, n_estimators=100)\n"
                            "assert isinstance(acc, float), type(acc)\n"
                            "assert acc == 1.0, acc"
                        ),
                    },
                    {
                        "name": "RF con n_estimators=1 (basicamente un arbol) da acc menor con datos ruidosos",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "# datos con ruido para que RF-100 supere a RF-1\n"
                            "rng = np.random.default_rng(42)\n"
                            "X = rng.uniform(0, 10, size=(200, 4))\n"
                            "y = (X[:, 0] + X[:, 1] > 10).astype(int)\n"
                            "# meter ruido en 20 filas\n"
                            "flip = rng.choice(200, size=20, replace=False)\n"
                            "y[flip] = 1 - y[flip]\n"
                            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc_1 = entrenar_rf(X_tr, y_tr, X_te, y_te, n_estimators=1)\n"
                            "acc_100 = entrenar_rf(X_tr, y_tr, X_te, y_te, n_estimators=100)\n"
                            "# El promedio de 100 arboles reduce varianza -> acc_100 >= acc_1\n"
                            "assert acc_100 >= acc_1, (acc_1, acc_100)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="feature_importances_ ordenadas",
                description=(
                    "Extrae las importancias de features de un "
                    "RandomForest y ordenalas descendentemente."
                ),
                instructions=(
                    "Implementa `importancias_ordenadas(X_train, "
                    "y_train, feature_names)` que entrena un "
                    "`RandomForestClassifier(n_estimators=100, "
                    "random_state=42)` sobre train, extrae "
                    "`feature_importances_` y devuelve una `list` de "
                    "tuplas `(nombre, importancia_float)` ordenada "
                    "**descendentemente** por importancia."
                ),
                starter_code=(
                    "from sklearn.ensemble import RandomForestClassifier\n"
                    "\n"
                    "\n"
                    "def importancias_ordenadas(X_train, y_train, feature_names):\n"
                    "    # TODO: entrena RF con n_estimators=100 y random_state=42\n"
                    "    # TODO: pares = list(zip(feature_names, rf.feature_importances_))\n"
                    "    # TODO: retorna sorted(pares, key=..., reverse=True)\n"
                    "    ...\n"
                ),
                hints=[
                    "sorted(pares, key=lambda t: t[1], reverse=True) ordena por importancia desc.",
                    "float(imp) en la tupla para evitar numpy.float64.",
                    "feature_importances_ suman ~1.0 en RF (con tolerancia de flotante).",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "importancias suman ~1.0 y estan ordenadas desc",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "res = importancias_ordenadas(X_tr, y_tr, list(X.columns))\n"
                            "assert isinstance(res, list), type(res)\n"
                            "assert len(res) == 4, len(res)\n"
                            "# ordenadas desc\n"
                            "vals = [imp for _, imp in res]\n"
                            "assert vals == sorted(vals, reverse=True), vals\n"
                            "# suman aprox 1.0\n"
                            "assert abs(sum(vals) - 1.0) < 1e-6, sum(vals)"
                        ),
                    },
                    {
                        "name": "top feature es petal_width o petal_length en iris seed 42",
                        "code": (
                            "import io\n"
                            "import pandas as pd\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "csv = 'sepal_length,sepal_width,petal_length,petal_width,species\\n5.1,3.5,1.4,0.2,setosa\\n4.9,3.0,1.4,0.2,setosa\\n4.7,3.2,1.3,0.2,setosa\\n4.6,3.1,1.5,0.2,setosa\\n5.0,3.6,1.4,0.2,setosa\\n5.4,3.9,1.7,0.4,setosa\\n4.6,3.4,1.4,0.3,setosa\\n5.0,3.4,1.5,0.2,setosa\\n4.4,2.9,1.4,0.2,setosa\\n4.9,3.1,1.5,0.1,setosa\\n7.0,3.2,4.7,1.4,versicolor\\n6.4,3.2,4.5,1.5,versicolor\\n6.9,3.1,4.9,1.5,versicolor\\n5.5,2.3,4.0,1.3,versicolor\\n6.5,2.8,4.6,1.5,versicolor\\n5.7,2.8,4.5,1.3,versicolor\\n6.3,3.3,4.7,1.6,versicolor\\n4.9,2.4,3.3,1.0,versicolor\\n6.6,2.9,4.6,1.3,versicolor\\n5.2,2.7,3.9,1.4,versicolor\\n6.3,3.3,6.0,2.5,virginica\\n5.8,2.7,5.1,1.9,virginica\\n7.1,3.0,5.9,2.1,virginica\\n6.3,2.9,5.6,1.8,virginica\\n6.5,3.0,5.8,2.2,virginica\\n7.6,3.0,6.6,2.1,virginica\\n4.9,2.5,4.5,1.7,virginica\\n7.3,2.9,6.3,1.8,virginica\\n6.7,2.5,5.8,1.8,virginica\\n7.2,3.6,6.1,2.5,virginica\\n'\n"
                            "df = pd.read_csv(io.StringIO(csv))\n"
                            "X = df[['sepal_length','sepal_width','petal_length','petal_width']]\n"
                            "y = df['species']\n"
                            "X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "res = importancias_ordenadas(X_tr, y_tr, list(X.columns))\n"
                            "top_name, top_imp = res[0]\n"
                            "assert top_name in {'petal_width', 'petal_length'}, top_name\n"
                            "# sepal_width debe ser el ultimo con importancia muy chica\n"
                            "last_name, last_imp = res[-1]\n"
                            "assert last_imp < 0.1, res"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 6 · Cross-validation y GridSearchCV",
        description=(
            "Evaluar modelos de forma honesta con K-Fold y encontrar "
            "hiperparametros con GridSearchCV. Fin de la ilusion de "
            "una sola accuracy."
        ),
        content=(
            "# ML 6: cross-validation y GridSearchCV\n\n"
            "Un solo `train_test_split` te da **una** accuracy. Suena "
            "razonable, pero esa accuracy depende de que muestras "
            "cayeron en el test — cambia el `random_state` y sale otra. "
            "Peor: si eliges hiperparametros mirando ese test, te "
            "**enganas a ti mismo** (data leakage sutil). Este bloque "
            "resuelve ambos problemas con **cross-validation** y "
            "**GridSearchCV**.\n\n"
            "## Tres ideas para entender CV\n\n"
            "### 1. K-Fold: promediar sobre varios splits\n\n"
            "En vez de un split unico, divide el dataset en **K partes** "
            "(folds). Entrena K veces: cada fold es el test una vez, y "
            "los otros K-1 folds son el train. Al final tienes K "
            "accuracies — su **media** es una estimacion mucho mas "
            "estable que un solo split.\n\n"
            "```\n"
            "K=5:\n"
            "  fold 1: [test][train][train][train][train]\n"
            "  fold 2: [train][test][train][train][train]\n"
            "  fold 3: [train][train][test][train][train]\n"
            "  fold 4: [train][train][train][test][train]\n"
            "  fold 5: [train][train][train][train][test]\n"
            "  scores = [0.96, 1.00, 0.93, 0.96, 1.00]\n"
            "  mean = 0.97, std = 0.025\n"
            "```\n\n"
            "```python\n"
            "from sklearn.model_selection import cross_val_score\n"
            "from sklearn.linear_model import LogisticRegression\n\n"
            "lr = LogisticRegression(max_iter=1000, random_state=42)\n"
            "scores = cross_val_score(lr, X, y, cv=5)\n"
            "print(scores.mean(), scores.std())\n"
            "```\n\n"
            "**Que te da CV que un split no te da:**\n\n"
            "- **Estimacion estable**: promedio de K medidas independientes.\n"
            "- **Desviacion**: `scores.std()` te dice cuanto varia el "
            "modelo entre folds. Std alta = modelo inestable.\n"
            "- **Usa todo el dataset**: cada fila aparece en train Y en "
            "test (en folds distintos). Sin desperdicio.\n\n"
            "**Reglas practicas para K:**\n\n"
            "- `cv=5` o `cv=10` son los estandares. 5 mas rapido; 10 "
            "mas robusto.\n"
            "- Con datasets pequenos, sube K (K=10, incluso "
            "leave-one-out K=N).\n"
            "- Con datasets grandes, baja K (K=3 o incluso 2) — cada "
            "fold ya es grande.\n\n"
            "### 2. StratifiedKFold: preserva la proporcion de clases\n\n"
            "Por default, `cross_val_score` con un clasificador usa "
            "`StratifiedKFold`: cada fold mantiene la misma proporcion "
            "de clases que el dataset completo. Esto es **imprescindible** "
            "en clasificacion desbalanceada — sin stratify, un fold "
            "podria quedar con 0% de la clase minoritaria y las metricas "
            "explotan.\n\n"
            "```python\n"
            "from sklearn.model_selection import StratifiedKFold\n\n"
            "skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n"
            "scores = cross_val_score(lr, X, y, cv=skf)\n"
            "```\n\n"
            "Para regresion no hay clases que estratificar; se usa "
            "`KFold` normal.\n\n"
            "### 3. GridSearchCV: probar combinaciones de hiperparametros\n\n"
            "Elegir `max_depth=3` a ojo es adivinar. `GridSearchCV` "
            "prueba **todas las combinaciones** de un `param_grid` con "
            "CV interno y te devuelve la mejor:\n\n"
            "```python\n"
            "from sklearn.model_selection import GridSearchCV\n"
            "from sklearn.tree import DecisionTreeClassifier\n\n"
            "param_grid = {'max_depth': [1, 2, 3, 5, 10]}\n"
            "gs = GridSearchCV(\n"
            "    DecisionTreeClassifier(random_state=42),\n"
            "    param_grid,\n"
            "    cv=5,\n"
            ")\n"
            "gs.fit(X, y)\n"
            "print(gs.best_params_)   # {'max_depth': 3}\n"
            "print(gs.best_score_)    # 0.9733 (media CV del mejor)\n"
            "print(gs.best_estimator_)  # DecisionTreeClassifier(max_depth=3, ...)\n"
            "```\n\n"
            "**Que hace GridSearchCV por dentro:**\n\n"
            "1. Genera todas las combinaciones del `param_grid` "
            "(producto cartesiano).\n"
            "2. Para cada combinacion, corre `cross_val_score(cv=5)`.\n"
            "3. Selecciona la combinacion con la media mas alta.\n"
            "4. **Reentrena** el mejor modelo con **todo** el dataset "
            "de entrada (por eso `best_estimator_` esta listo para "
            "predecir).\n\n"
            "**Multiples hiperparametros = producto cartesiano:**\n\n"
            "```python\n"
            "param_grid = {\n"
            "    'max_depth': [3, 5, 10],\n"
            "    'min_samples_leaf': [1, 5, 10],\n"
            "}\n"
            "# GridSearchCV probara 3 * 3 = 9 combinaciones\n"
            "```\n\n"
            "Cuando el grid se pone grande (>50 combinaciones) usa "
            "`RandomizedSearchCV` — muestrea N combinaciones al azar en "
            "vez de exhaustivo. Casi tan bueno, mucho mas rapido.\n\n"
            "## Nested CV: el estandar de oro\n\n"
            "Si usas GridSearchCV para elegir hiperparametros **y** "
            "reportas `best_score_` como tu accuracy final, estas "
            "**contaminando** — elegiste el hiperparametro mirando el "
            "mismo CV que ahora reportas. El estandar riguroso es "
            "**nested CV**: un CV externo para estimar performance y "
            "un CV interno (dentro de GridSearchCV) para tunear.\n\n"
            "```python\n"
            "from sklearn.model_selection import cross_val_score, GridSearchCV\n\n"
            "gs = GridSearchCV(DecisionTreeClassifier(random_state=42),\n"
            "                  {'max_depth': [3, 5, 10]}, cv=5)\n"
            "final = cross_val_score(gs, X, y, cv=5)  # nested\n"
            "print(final.mean())  # accuracy honesta\n"
            "```\n\n"
            "En la practica esto es 25x mas costoso. Muchos proyectos "
            "se conforman con un `train / val / test` clasico: tunean "
            "con GridSearchCV sobre train+val, y reportan sobre el test "
            "intocado.\n\n"
            "## Errores comunes\n\n"
            "1. **Reportar `best_score_` como accuracy de produccion** "
            "— es optimista; usa un test set separado o nested CV.\n"
            "2. **CV sin stratify en desbalanceado** — folds sin la "
            "clase minoritaria = metricas rotas. `cross_val_score` "
            "con clasificador ya lo hace por default; con "
            "regresion/pipeline custom, verificalo.\n"
            "3. **Escalar antes de CV** — data leakage: el scaler ve "
            "medias del test. Solucion: envolver el modelo en un "
            "`Pipeline` y pasar el pipeline a `cross_val_score`.\n"
            "4. **Grid gigante sin sentido** — probar 500 combinaciones "
            "cuando 20 dan la misma respuesta. Empieza pequeno, "
            "expande solo si el mejor esta en el borde del grid.\n"
            "5. **K muy alto con datasets grandes** — leave-one-out en "
            "1M filas = 1M entrenamientos. Con datasets grandes, K=3 "
            "sobra.\n\n"
            "## Resumen\n\n"
            "- `cross_val_score(modelo, X, y, cv=5)` devuelve un array "
            "de K accuracies. Reporta `mean` y `std`.\n"
            "- Para clasificadores, `cv=5` ya estratifica; para "
            "regresion o pipelines custom, pasa un `KFold`/`StratifiedKFold`.\n"
            "- `GridSearchCV(estimator, param_grid, cv=5)` prueba "
            "todas las combinaciones y expone `best_params_`, "
            "`best_score_`, `best_estimator_`.\n"
            "- El mejor `best_score_` **no es** la accuracy que veras "
            "en produccion — usa un test set aparte o nested CV para "
            "reportar honestamente.\n"
        ),
        difficulty="intermediate",
        category="ml-tuning",
        order=27,
        track="track-3",
        estimated_duration=55,
        prerequisites_titles=[
            "ML 5 · Arboles y Random Forest",
        ],
        exercises=[
            ExerciseTemplate(
                title="cross_val_score sobre LogisticRegression",
                description=(
                    "Corre 5-fold cross-validation sobre un modelo "
                    "LogReg y devuelve el array de scores."
                ),
                instructions=(
                    "Implementa `cv_score_logreg(X, y, cv=5)` que crea "
                    "`LogisticRegression(max_iter=1000, random_state=42)`, "
                    "corre `cross_val_score` con `cv=cv` y devuelve el "
                    "array de scores (`np.ndarray`) tal cual."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.model_selection import cross_val_score\n"
                    "\n"
                    "\n"
                    "def cv_score_logreg(X, y, cv=5):\n"
                    "    # TODO: lr = LogisticRegression(max_iter=1000, random_state=42)\n"
                    "    # TODO: return cross_val_score(lr, X, y, cv=cv)\n"
                    "    ...\n"
                ),
                hints=[
                    "cross_val_score devuelve np.ndarray de shape (cv,).",
                    "Con cv=5 sobre iris (150 filas) tienes 30 filas por fold.",
                    "No hagas .mean() aqui — devuelve el array completo.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "cv=5 sobre iris devuelve array de 5 scores con mean > 0.95",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "scores = cv_score_logreg(X, y, cv=5)\n"
                            "assert isinstance(scores, np.ndarray), type(scores)\n"
                            "assert scores.shape == (5,), scores.shape\n"
                            "assert (scores >= 0).all() and (scores <= 1).all(), scores\n"
                            "assert scores.mean() > 0.95, scores.mean()"
                        ),
                    },
                    {
                        "name": "cv=3 devuelve array de 3 scores",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "scores = cv_score_logreg(X, y, cv=3)\n"
                            "assert scores.shape == (3,), scores.shape\n"
                            "assert scores.mean() > 0.9, scores.mean()"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Elegir el mejor k para KNN via CV",
                description=(
                    "Compara varios valores de k con cross-validation "
                    "y devuelve el que da mejor media."
                ),
                instructions=(
                    "Implementa `mejor_k_knn(X, y, ks)` que, para cada "
                    "`k` en la lista `ks`, entrena "
                    "`KNeighborsClassifier(n_neighbors=k)`, calcula la "
                    "media de `cross_val_score(cv=5)` y devuelve el `k` "
                    "con la media mas alta como `int`. En caso de empate, "
                    "prefiere el `k` mas chico (el primero en aparecer "
                    "con el maximo)."
                ),
                starter_code=(
                    "from sklearn.neighbors import KNeighborsClassifier\n"
                    "from sklearn.model_selection import cross_val_score\n"
                    "\n"
                    "\n"
                    "def mejor_k_knn(X, y, ks):\n"
                    "    # TODO: para cada k en ks, calcular mean = cross_val_score(...).mean()\n"
                    "    # TODO: retornar el k con la media mas alta (empate -> primero)\n"
                    "    ...\n"
                ),
                hints=[
                    "max con key=lambda k: score_de(k) devuelve el primer maximo.",
                    "cross_val_score(...).mean() te da la accuracy promedio.",
                    "Sobre iris con ks=[1,3,5,7,9], gana k=7 con score 0.98.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "iris con ks=[1,3,5,7,9] -> k=7 gana",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "k = mejor_k_knn(X, y, [1, 3, 5, 7, 9])\n"
                            "assert isinstance(k, int), type(k)\n"
                            "assert k == 7, k"
                        ),
                    },
                    {
                        "name": "k devuelto pertenece a ks y no rompe con lista de 1 elemento",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "k = mejor_k_knn(X, y, [5])\n"
                            "assert k == 5, k\n"
                            "k2 = mejor_k_knn(X, y, [3, 11])\n"
                            "assert k2 in {3, 11}, k2"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="GridSearchCV sobre DecisionTree",
                description=(
                    "Encuentra el mejor max_depth para un DecisionTree "
                    "con GridSearchCV."
                ),
                instructions=(
                    "Implementa `grid_search_dt(X, y, depths)` que corre "
                    "`GridSearchCV` con "
                    "`DecisionTreeClassifier(random_state=42)`, "
                    "`param_grid={'max_depth': depths}` y `cv=5`. "
                    "Devuelve una tupla `(best_depth: int, best_score: float)` "
                    "con `best_params_['max_depth']` y "
                    "`best_score_`."
                ),
                starter_code=(
                    "from sklearn.tree import DecisionTreeClassifier\n"
                    "from sklearn.model_selection import GridSearchCV\n"
                    "\n"
                    "\n"
                    "def grid_search_dt(X, y, depths):\n"
                    "    # TODO: gs = GridSearchCV(DT(random_state=42), {'max_depth': depths}, cv=5)\n"
                    "    # TODO: gs.fit(X, y)\n"
                    "    # TODO: return (int(gs.best_params_['max_depth']), float(gs.best_score_))\n"
                    "    ...\n"
                ),
                hints=[
                    "gs.best_params_ es un dict; gs.best_score_ es la media CV del mejor.",
                    "Envuelve en int() y float() para evitar numpy types.",
                    "Sobre iris con depths=[1,2,3,5] gana max_depth=3 con ~0.9733.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "iris depths=[1,2,3,5] -> best_depth=3, best_score ~0.9733",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "best_depth, best_score = grid_search_dt(X, y, [1, 2, 3, 5])\n"
                            "assert isinstance(best_depth, int), type(best_depth)\n"
                            "assert isinstance(best_score, float), type(best_score)\n"
                            "assert best_depth == 3, best_depth\n"
                            "assert abs(best_score - 0.9733) < 0.01, best_score"
                        ),
                    },
                    {
                        "name": "depths=[1] fuerza best_depth=1 y best_score coincide con cross_val_score",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "from sklearn.tree import DecisionTreeClassifier\n"
                            "from sklearn.model_selection import cross_val_score\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "best_depth, best_score = grid_search_dt(X, y, [1])\n"
                            "assert best_depth == 1, best_depth\n"
                            "esperado = cross_val_score(\n"
                            "    DecisionTreeClassifier(max_depth=1, random_state=42), X, y, cv=5\n"
                            ").mean()\n"
                            "assert abs(best_score - esperado) < 1e-6, (best_score, esperado)"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 7 · Clustering con KMeans y metodo del codo",
        description=(
            "Primer modelo no supervisado: KMeans para agrupar sin "
            "labels. Metodo del codo y silhouette para elegir k."
        ),
        content=(
            "# ML 7: clustering con KMeans\n\n"
            "Hasta ahora todo fue **supervisado**: dabas `X` y `y`, el "
            "modelo aprendia el mapeo. En **clustering** solo tienes "
            "`X` — el modelo debe encontrar grupos naturales sin que "
            "nadie le diga cuales son las clases. Aplicaciones clasicas: "
            "segmentacion de clientes, deteccion de anomalias, "
            "compresion de datos, exploracion de datasets nuevos.\n\n"
            "## Tres ideas para entender KMeans\n\n"
            "### 1. KMeans busca K centroides que minimizan la inercia\n\n"
            "**Inercia** = suma de distancias al cuadrado de cada punto "
            "a su centroide asignado. KMeans reparte los puntos en K "
            "grupos y ajusta los centros iterativamente para que la "
            "inercia sea la menor posible.\n\n"
            "```\n"
            "algoritmo:\n"
            "  1. Elige K centros iniciales (KMeans++ los pone bien).\n"
            "  2. Repite hasta convergencia:\n"
            "     a. Asigna cada punto al centro mas cercano.\n"
            "     b. Recalcula cada centro como la media de sus puntos.\n"
            "```\n\n"
            "```python\n"
            "from sklearn.cluster import KMeans\n\n"
            "km = KMeans(n_clusters=3, random_state=42, n_init=10)\n"
            "km.fit(X)                # aprende centroides\n"
            "labels = km.labels_      # cluster de cada fila (0..K-1)\n"
            "centers = km.cluster_centers_  # shape (K, n_features)\n"
            "print(km.inertia_)       # suma de dist^2 al centro asignado\n"
            "```\n\n"
            "**Cuidados clave:**\n\n"
            "- **`random_state`** — KMeans depende de la inicializacion. "
            "Fijarlo hace el resultado reproducible.\n"
            "- **`n_init=10`** — corre KMeans 10 veces con diferentes "
            "inicializaciones y se queda con la mejor. Sin esto, un "
            "arranque malo te da clusters horribles.\n"
            "- **Escalado obligatorio** — KMeans usa distancia "
            "euclideana; una feature en dolares (0-1000000) dominara a "
            "una en anios (20-80). Aplica `StandardScaler` antes.\n\n"
            "### 2. Metodo del codo: como elegir K\n\n"
            "A diferencia del supervisado, no hay accuracy que "
            "maximizar. La inercia siempre baja al subir K (con K=N "
            "cada punto es su propio cluster e inercia=0). Necesitas un "
            "criterio externo. El **metodo del codo** grafica inercia "
            "vs K y busca el punto donde deja de bajar rapido.\n\n"
            "```python\n"
            "inertias = []\n"
            "for k in range(1, 8):\n"
            "    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X)\n"
            "    inertias.append(km.inertia_)\n"
            "# grafico inertias vs k, buscar el 'codo'\n"
            "```\n\n"
            "```\n"
            "iris:\n"
            "  k=1: inertia=681.37\n"
            "  k=2: inertia=152.35  <- brutal caida\n"
            "  k=3: inertia= 78.85\n"
            "  k=4: inertia= 57.23  <- caidas cada vez mas chicas\n"
            "  k=5: inertia= 46.46\n"
            "```\n\n"
            "El codo esta entre k=2 y k=3: despues de k=3 los "
            "beneficios marginales caen. Es una decision **visual** — "
            "no hay formula matematica que devuelva 'el K correcto'. "
            "Complementalo con conocimiento del dominio.\n\n"
            "### 3. Silhouette: metrica cuantitativa para K\n\n"
            "El **silhouette score** mide, para cada punto, que tan "
            "cerca esta de su cluster vs que tan lejos del cluster mas "
            "cercano ajeno. Rango [-1, +1]:\n\n"
            "- **+1**: punto muy dentro de su cluster.\n"
            "- **0**: en la frontera entre dos clusters.\n"
            "- **-1**: probablemente asignado al cluster equivocado.\n\n"
            "```python\n"
            "from sklearn.metrics import silhouette_score\n\n"
            "score = silhouette_score(X, km.labels_)\n"
            "```\n\n"
            "El K con mejor silhouette suele ser un buen punto de "
            "partida objetivo:\n\n"
            "```\n"
            "iris escalado:\n"
            "  k=2: silhouette=0.582  <- gana!\n"
            "  k=3: silhouette=0.460\n"
            "  k=4: silhouette=0.387\n"
            "```\n\n"
            "**Sorpresa pedagogica:** iris tiene 3 especies "
            "conocidas, pero silhouette dice k=2 es mejor. La razon: "
            "setosa es muy distinta, pero versicolor y virginica se "
            "**solapan** en el espacio de features. Clustering "
            "encuentra la estructura geometrica, no las etiquetas — "
            "si no coinciden, el problema puede ser que las features "
            "no discriminan las clases reales.\n\n"
            "## Cuando NO usar KMeans\n\n"
            "KMeans asume que los clusters son **esferas de tamano "
            "similar** en el espacio de features. Falla feo cuando:\n\n"
            "- Los clusters tienen **densidades muy distintas** — usa "
            "`DBSCAN`.\n"
            "- Los clusters tienen **formas raras** (medialunas, "
            "espirales) — usa clustering jerarquico o DBSCAN.\n"
            "- **No sabes cuantos clusters** hay y no quieres asumir "
            "un K — DBSCAN los descubre solo (usa densidad, no "
            "cantidad fija).\n"
            "- Tienes **outliers extremos** — mueven los centroides y "
            "estropean el resultado. Limpialos antes o usa "
            "clustering robusto.\n\n"
            "## Errores comunes\n\n"
            "1. **No escalar** — feature con rango 0-1M domina a otras "
            "con rango 0-1. Siempre `StandardScaler` antes de KMeans.\n"
            "2. **`n_init=1`** — un arranque malo da clusters malos. "
            "El default nuevo de sklearn ya es `n_init='auto'`, pero "
            "en versiones viejas es 1. Ponlo explicito en 10.\n"
            "3. **Elegir K por inercia sola** — inercia siempre baja "
            "con K. Usa codo + silhouette + dominio.\n"
            "4. **Interpretar labels como etiquetas reales** — el "
            "cluster 0 no es 'setosa'; es solo un ID interno. Si "
            "quieres etiquetar los clusters, hazlo despues mirando "
            "sus centroides o promedios.\n"
            "5. **KMeans en categoricas one-hot** — la distancia "
            "euclideana en one-hot no tiene sentido pleno; usa "
            "KModes o algoritmos especificos para categoricas.\n\n"
            "## Resumen\n\n"
            "- `KMeans(n_clusters=K, random_state=42, n_init=10)` "
            "agrupa `X` en K clusters minimizando la inercia.\n"
            "- **Escala** siempre las features antes con "
            "`StandardScaler`.\n"
            "- Para elegir K: **codo** (visual, inercia vs K) + "
            "**silhouette** (cuantitativo, [-1, +1]) + dominio.\n"
            "- KMeans es tu default no-supervisado; para densidades "
            "raras o clusters no esfericos, mira DBSCAN o clustering "
            "jerarquico.\n"
        ),
        difficulty="intermediate",
        category="ml-clustering",
        order=28,
        track="track-3",
        estimated_duration=55,
        prerequisites_titles=[
            "ML 6 · Cross-validation y GridSearchCV",
        ],
        exercises=[
            ExerciseTemplate(
                title="Entrenar KMeans y devolver inertia",
                description=(
                    "Entrena un modelo KMeans y devuelve la inertia "
                    "final y las labels."
                ),
                instructions=(
                    "Implementa `entrenar_kmeans(X, k)` que crea "
                    "`KMeans(n_clusters=k, random_state=42, n_init=10)`, "
                    "lo entrena con `fit(X)` y devuelve una tupla "
                    "`(inertia: float, labels: np.ndarray)` con "
                    "`km.inertia_` (envuelto en `float`) y `km.labels_`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "from sklearn.cluster import KMeans\n"
                    "\n"
                    "\n"
                    "def entrenar_kmeans(X, k):\n"
                    "    # TODO: km = KMeans(n_clusters=k, random_state=42, n_init=10)\n"
                    "    # TODO: km.fit(X)\n"
                    "    # TODO: return (float(km.inertia_), km.labels_)\n"
                    "    ...\n"
                ),
                hints=[
                    "n_init=10 evita quedarte con una inicializacion mala.",
                    "km.labels_ tiene shape (n_samples,) con valores en 0..k-1.",
                    "float(km.inertia_) evita numpy.float64 en la salida.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "iris k=3 -> inertia ~78.85, labels con 3 valores unicos",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.datasets import load_iris\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "inertia, labels = entrenar_kmeans(X, 3)\n"
                            "assert isinstance(inertia, float), type(inertia)\n"
                            "assert isinstance(labels, np.ndarray), type(labels)\n"
                            "assert labels.shape == (150,), labels.shape\n"
                            "assert set(labels.tolist()) == {0, 1, 2}, set(labels.tolist())\n"
                            "assert abs(inertia - 78.85) < 0.5, inertia"
                        ),
                    },
                    {
                        "name": "k=1 da inertia = suma total de dist^2 al centro global",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.datasets import load_iris\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "inertia, labels = entrenar_kmeans(X, 1)\n"
                            "# con k=1 todas las labels son 0 y la inertia es la varianza total\n"
                            "assert set(labels.tolist()) == {0}, set(labels.tolist())\n"
                            "centro = X.mean(axis=0)\n"
                            "esperado = float(((X - centro) ** 2).sum())\n"
                            "assert abs(inertia - esperado) < 1e-3, (inertia, esperado)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Metodo del codo: inertias para varios K",
                description=(
                    "Corre KMeans para distintos valores de K y "
                    "devuelve la lista de inertias."
                ),
                instructions=(
                    "Implementa `metodo_del_codo(X, ks)` que, para cada "
                    "`k` en `ks`, entrena "
                    "`KMeans(n_clusters=k, random_state=42, n_init=10)` "
                    "y devuelve una `list[float]` con las inercias en el "
                    "mismo orden que `ks`."
                ),
                starter_code=(
                    "from sklearn.cluster import KMeans\n"
                    "\n"
                    "\n"
                    "def metodo_del_codo(X, ks):\n"
                    "    # TODO: para cada k en ks, entrenar KMeans y appendear km.inertia_\n"
                    "    # TODO: retornar la lista de inercias\n"
                    "    ...\n"
                ),
                hints=[
                    "La inertia baja monotonicamente al subir k.",
                    "float(km.inertia_) para evitar numpy.float64 en la lista.",
                    "El 'codo' se busca visualmente en un plot inertia vs k.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "iris ks=[1,2,3,4,5] -> inertias decrecientes",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "inertias = metodo_del_codo(X, [1, 2, 3, 4, 5])\n"
                            "assert isinstance(inertias, list), type(inertias)\n"
                            "assert len(inertias) == 5, len(inertias)\n"
                            "# monotonicamente decreciente\n"
                            "for i in range(len(inertias) - 1):\n"
                            "    assert inertias[i] >= inertias[i + 1], inertias\n"
                            "# k=1 muy alta, k=3 baja\n"
                            "assert inertias[0] > 600, inertias[0]\n"
                            "assert 70 < inertias[2] < 90, inertias[2]"
                        ),
                    },
                    {
                        "name": "respeta el orden de ks (aunque este desordenado)",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "inertias = metodo_del_codo(X, [3, 1, 2])\n"
                            "assert len(inertias) == 3, len(inertias)\n"
                            "# ks=[3,1,2] -> inertias en ese orden\n"
                            "assert inertias[1] > inertias[2] > inertias[0], inertias"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Mejor K por silhouette score",
                description=("Elige el mejor K comparando silhouette scores."),
                instructions=(
                    "Implementa `mejor_k_silhouette(X, ks)` que, para "
                    "cada `k` en `ks` (asumir `k >= 2`), entrena "
                    "`KMeans(n_clusters=k, random_state=42, n_init=10)`, "
                    "calcula `silhouette_score(X, labels)` y devuelve "
                    "el `k` con el score mas alto como `int`. En empate, "
                    "prefiere el `k` mas chico."
                ),
                starter_code=(
                    "from sklearn.cluster import KMeans\n"
                    "from sklearn.metrics import silhouette_score\n"
                    "\n"
                    "\n"
                    "def mejor_k_silhouette(X, ks):\n"
                    "    # TODO: para cada k en ks, fit_predict con KMeans y calcular silhouette\n"
                    "    # TODO: retornar k con mayor silhouette (empate -> primero)\n"
                    "    ...\n"
                ),
                hints=[
                    "silhouette_score requiere >=2 clusters distintos.",
                    "KMeans.fit_predict(X) devuelve labels en un paso.",
                    "En blobs sinteticos con 4 centros bien separados, gana k=4.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "make_blobs 4 centros -> mejor k=4",
                        "code": (
                            "from sklearn.datasets import make_blobs\n"
                            "X, _ = make_blobs(\n"
                            "    n_samples=200, centers=4, cluster_std=0.5, random_state=42\n"
                            ")\n"
                            "k = mejor_k_silhouette(X, [2, 3, 4, 5])\n"
                            "assert isinstance(k, int), type(k)\n"
                            "assert k == 4, k"
                        ),
                    },
                    {
                        "name": "iris escalado -> silhouette prefiere k=2 (versicolor+virginica se solapan)",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "from sklearn.preprocessing import StandardScaler\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "Xs = StandardScaler().fit_transform(X)\n"
                            "k = mejor_k_silhouette(Xs, [2, 3, 4])\n"
                            "assert k == 2, k"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 8 · PCA para reducir dimensionalidad",
        description=(
            "Principal Component Analysis: comprimir features "
            "preservando varianza. Visualizacion 2D y aceleracion de "
            "modelos."
        ),
        content=(
            "# ML 8: reduccion de dimensionalidad con PCA\n\n"
            "Cuando tienes 64 features (o 10.000), pasan tres cosas "
            "molestas: es dificil visualizar los datos, los modelos "
            "tardan mas en entrenar, y muchas features estan "
            "**correlacionadas** entre si (informacion redundante). "
            "**PCA (Principal Component Analysis)** ataca las tres: "
            "encuentra un espacio nuevo de menor dimension que "
            "**preserva la mayor varianza posible** de los datos "
            "originales.\n\n"
            "## Tres ideas para entender PCA\n\n"
            "### 1. PCA encuentra los ejes con mayor varianza\n\n"
            "Imagina una nube de puntos alargada en el plano (X, Y). "
            "PCA rota los ejes para que **el primer eje nuevo (PC1) "
            "vaya a lo largo de la nube** (direccion de maxima "
            "varianza), y el segundo (PC2) sea perpendicular a PC1 y "
            "capture la varianza restante. Cada componente principal es "
            "una **combinacion lineal** de las features originales.\n\n"
            "```\n"
            "features originales -> ejes rotados por PCA\n"
            "  X (sepal_length)         PC1 (0.52*sl + 0.27*sw + 0.58*pl + 0.56*pw)\n"
            "  Y (sepal_width)     ->   PC2 (-0.38*sl + 0.92*sw - 0.02*pl - 0.07*pw)\n"
            "  Z (petal_length)         PC3 (...)\n"
            "  W (petal_width)          PC4 (...)\n"
            "```\n\n"
            "Las componentes estan **ordenadas por varianza explicada** "
            "de mayor a menor. Si te quedas con las primeras K, "
            "conservas la mayor parte de la informacion en menos "
            "dimensiones.\n\n"
            "```python\n"
            "from sklearn.decomposition import PCA\n\n"
            "pca = PCA(n_components=2, random_state=42)\n"
            "X2 = pca.fit_transform(X)   # shape (n_samples, 2)\n"
            "print(pca.explained_variance_ratio_)\n"
            "# [0.7296, 0.2285]  -> las 2 primeras PC explican 95.8% de la varianza\n"
            "```\n\n"
            "### 2. Cuantas componentes usar\n\n"
            "Dos estrategias tipicas:\n\n"
            "**A. Fijar un umbral de varianza explicada** (ej. 95%):\n"
            "```python\n"
            "pca = PCA(n_components=0.95, random_state=42).fit(X)\n"
            "print(pca.n_components_)  # cuantas necesito para llegar a 95%\n"
            "```\n\n"
            "**B. Scree plot**: grafica varianza explicada acumulada vs "
            "K y buscas el codo (igual que en KMeans):\n\n"
            "```\n"
            "iris:\n"
            "  1 PC:  72.96%\n"
            "  2 PC:  95.81%  <- ya cerca del 100%\n"
            "  3 PC:  99.48%\n"
            "  4 PC: 100.00%\n"
            "```\n\n"
            "Con 4 features originales, la ganancia de dimensionalidad "
            "es minima. PCA brilla cuando tienes **muchas** features:\n\n"
            "```\n"
            "digits (64 features):\n"
            "  para conservar 90% de varianza -> 31 componentes\n"
            "  reduces ~50% las columnas sin perder informacion util\n"
            "```\n\n"
            "### 3. Escalado obligatorio (otra vez)\n\n"
            "PCA usa **varianza**, y la varianza depende de la escala. "
            "Una feature en dolares (0-1M) tendra varianza millones de "
            "veces mayor que una en 0-1: dominara PC1 aunque sea "
            "irrelevante. Aplica siempre `StandardScaler` antes de PCA "
            "(salvo que todas tus features ya esten en la misma "
            "escala fisica).\n\n"
            "```python\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler\n\n"
            "pipe = Pipeline([\n"
            "    ('sc', StandardScaler()),\n"
            "    ('pca', PCA(n_components=2, random_state=42)),\n"
            "    ('lr', LogisticRegression(max_iter=1000)),\n"
            "])\n"
            "```\n\n"
            "## Cuando usar PCA\n\n"
            "**Casos donde PCA es la herramienta correcta:**\n\n"
            "- **Visualizacion**: reducir a 2 o 3 componentes para "
            "plotear datos de alta dimension.\n"
            "- **Compresion**: cientos/miles de features ->\n"
            "  decenas conservando 95% de la varianza.\n"
            "- **Denoising**: al descartar componentes de baja varianza "
            "eliminas ruido idiosincratico.\n"
            "- **Multicolinealidad**: features muy correlacionadas "
            "confunden a la regresion lineal; PCA las combina en "
            "componentes ortogonales.\n\n"
            "**Casos donde PCA es mala idea:**\n\n"
            "- **Necesitas interpretabilidad por feature** — los PCs "
            "son combinaciones lineales, no features originales. "
            'Explicar "el modelo depende de 0.5*X1 - 0.3*X2 + '
            '0.8*X3" no vende.\n'
            "- **Features categoricas o binarias** — PCA es lineal y "
            "asume continuidad; en categoricas usa MCA o embeddings.\n"
            "- **Relaciones no lineales** en los datos — PCA solo "
            "captura estructura lineal. Para manifolds curvos usa "
            "t-SNE o UMAP (solo para visualizacion) o autoencoders.\n"
            "- **Dataset gigante** — PCA calcula la matriz de "
            "covarianza (O(n * d^2)); con d>10.000 se pone lento. Usa "
            "`TruncatedSVD` o `IncrementalPCA`.\n\n"
            "## Precio a pagar: casi siempre pierdes algo de accuracy\n\n"
            "Reducir dimensionalidad tiene un costo. Sobre iris "
            "escalado con LogReg:\n\n"
            "```\n"
            "  features originales (4):  CV accuracy = 0.96\n"
            "  PCA a 2 componentes:      CV accuracy = 0.91\n"
            "```\n\n"
            "Perder 0.05 puede o no valer la pena — depende del "
            "problema. Si eres mucho mas rapido, visualizas datos, "
            "y el modelo sigue siendo aceptable, PCA gana. Si cada "
            "punto de accuracy vale plata, PCA no es tu amigo.\n\n"
            "## Errores comunes\n\n"
            "1. **No escalar antes** — features con rangos muy "
            "distintos dominan PCs. `StandardScaler` primero.\n"
            "2. **Aplicar PCA a train + test juntos** — data leakage. "
            "`fit` solo en train; `transform` en test.\n"
            "3. **Usar todos los PCs pensando que 'ayuda'** — PCA con "
            "n_components = n_features solo rota; no reduce ni "
            "acelera nada.\n"
            "4. **Interpretar PC1 como una feature real** — es una "
            "combinacion; puedes mirar `pca.components_` para ver los "
            "coeficientes, pero rara vez tiene un nombre claro.\n"
            "5. **Aplicar PCA a arboles/RF** — no ayuda: los arboles "
            "no sufren de multicolinealidad ni les molesta la escala. "
            "PCA solo agrega complejidad y tira interpretabilidad.\n\n"
            "## Resumen\n\n"
            "- `PCA(n_components=K)` proyecta X a un espacio de K "
            "dimensiones que **preserva la mayor varianza posible**.\n"
            "- Elige K por umbral (`n_components=0.95`) o scree plot.\n"
            "- `pca.explained_variance_ratio_` te dice que fraccion de "
            "varianza captura cada componente.\n"
            "- **Escala siempre** antes con `StandardScaler`, y "
            "envuelve todo en un `Pipeline` para evitar leakage.\n"
            "- Usa PCA para visualizar, comprimir, denoisar; NO para "
            "categoricas, arboles, o cuando necesites interpretabilidad "
            "por feature.\n"
        ),
        difficulty="intermediate",
        category="ml-dim-reduction",
        order=29,
        track="track-3",
        estimated_duration=55,
        prerequisites_titles=[
            "ML 7 · Clustering con KMeans y metodo del codo",
        ],
        exercises=[
            ExerciseTemplate(
                title="PCA a n componentes",
                description=(
                    "Aplica PCA para reducir features y devuelve la "
                    "transformacion + varianza explicada."
                ),
                instructions=(
                    "Implementa `pca_reducir(X_scaled, n)` que crea "
                    "`PCA(n_components=n, random_state=42)`, lo entrena "
                    "con `fit_transform(X_scaled)` y devuelve una tupla "
                    "`(X_reducido: np.ndarray, ratios: np.ndarray)` con "
                    "el X transformado (shape `(n_samples, n)`) y el "
                    "atributo `explained_variance_ratio_`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "from sklearn.decomposition import PCA\n"
                    "\n"
                    "\n"
                    "def pca_reducir(X_scaled, n):\n"
                    "    # TODO: pca = PCA(n_components=n, random_state=42)\n"
                    "    # TODO: X_red = pca.fit_transform(X_scaled)\n"
                    "    # TODO: return (X_red, pca.explained_variance_ratio_)\n"
                    "    ...\n"
                ),
                hints=[
                    "fit_transform hace fit + transform en un paso.",
                    "explained_variance_ratio_ suma <=1 (=1 solo si n = n_features).",
                    "Escala X antes con StandardScaler para que PCA sea significativo.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "iris escalado n=2 -> shape (150,2) y ~95.8% varianza",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.datasets import load_iris\n"
                            "from sklearn.preprocessing import StandardScaler\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "Xs = StandardScaler().fit_transform(X)\n"
                            "X2, ratios = pca_reducir(Xs, 2)\n"
                            "assert isinstance(X2, np.ndarray), type(X2)\n"
                            "assert X2.shape == (150, 2), X2.shape\n"
                            "assert ratios.shape == (2,), ratios.shape\n"
                            "# PC1 ~0.73, PC2 ~0.23\n"
                            "assert abs(ratios[0] - 0.7296) < 0.01, ratios\n"
                            "assert abs(ratios.sum() - 0.9581) < 0.01, ratios.sum()"
                        ),
                    },
                    {
                        "name": "n=4 = n_features -> ratios suman 1.0",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "from sklearn.preprocessing import StandardScaler\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "Xs = StandardScaler().fit_transform(X)\n"
                            "X4, ratios = pca_reducir(Xs, 4)\n"
                            "assert X4.shape == (150, 4), X4.shape\n"
                            "assert abs(ratios.sum() - 1.0) < 1e-6, ratios.sum()"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Componentes necesarias para X% de varianza",
                description=(
                    "Cuenta cuantas componentes necesitas para llegar "
                    "a un umbral de varianza explicada."
                ),
                instructions=(
                    "Implementa `n_componentes_para(X_scaled, "
                    "var_explicada)` que entrena "
                    "`PCA(n_components=var_explicada, random_state=42)` "
                    "sobre `X_scaled` y devuelve `pca.n_components_` "
                    "como `int` (numero minimo de componentes que "
                    "alcanzan al menos ese umbral). `var_explicada` "
                    "debe estar entre 0 y 1 (fraccion, no porcentaje)."
                ),
                starter_code=(
                    "from sklearn.decomposition import PCA\n"
                    "\n"
                    "\n"
                    "def n_componentes_para(X_scaled, var_explicada):\n"
                    "    # TODO: pca = PCA(n_components=var_explicada, random_state=42)\n"
                    "    # TODO: pca.fit(X_scaled)\n"
                    "    # TODO: return int(pca.n_components_)\n"
                    "    ...\n"
                ),
                hints=[
                    "PCA acepta n_components como float en (0,1) = umbral de varianza.",
                    "pca.n_components_ es el numero final elegido (int).",
                    "digits (64 features) escalado con umbral 0.9 -> 31 componentes.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "iris escalado 0.95 -> 2 componentes",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "from sklearn.preprocessing import StandardScaler\n"
                            "X, _ = load_iris(return_X_y=True)\n"
                            "Xs = StandardScaler().fit_transform(X)\n"
                            "n = n_componentes_para(Xs, 0.95)\n"
                            "assert isinstance(n, int), type(n)\n"
                            "assert n == 2, n"
                        ),
                    },
                    {
                        "name": "digits escalado 0.9 -> 31 componentes",
                        "code": (
                            "from sklearn.datasets import load_digits\n"
                            "from sklearn.preprocessing import StandardScaler\n"
                            "X, _ = load_digits(return_X_y=True)\n"
                            "Xs = StandardScaler().fit_transform(X)\n"
                            "n = n_componentes_para(Xs, 0.9)\n"
                            "assert n == 31, n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Pipeline PCA + LogReg: costo en accuracy",
                description=(
                    "Compara accuracy de LogReg con features originales "
                    "vs con PCA aplicado antes."
                ),
                instructions=(
                    "Implementa `pca_conserva_accuracy(X, y, "
                    "n_components)` que arma DOS pipelines y devuelve "
                    "un dict `{'full': acc_full, 'pca': acc_pca}` con "
                    "las accuracies medias de `cross_val_score(cv=5)`:\n"
                    "- `full`: `StandardScaler` + "
                    "`LogisticRegression(max_iter=1000, random_state=42)`.\n"
                    "- `pca`: `StandardScaler` + "
                    "`PCA(n_components=n_components, random_state=42)` "
                    "+ `LogisticRegression(max_iter=1000, "
                    "random_state=42)`.\n\n"
                    "Ambas accuracies como `float` (no numpy)."
                ),
                starter_code=(
                    "from sklearn.decomposition import PCA\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.model_selection import cross_val_score\n"
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "\n"
                    "\n"
                    "def pca_conserva_accuracy(X, y, n_components):\n"
                    "    # TODO: pipe_full = Pipeline([('sc', ...), ('lr', ...)])\n"
                    "    # TODO: pipe_pca = Pipeline([('sc', ...), ('pca', ...), ('lr', ...)])\n"
                    "    # TODO: acc_full = cross_val_score(pipe_full, X, y, cv=5).mean()\n"
                    "    # TODO: acc_pca = cross_val_score(pipe_pca, X, y, cv=5).mean()\n"
                    "    # TODO: return {'full': float(acc_full), 'pca': float(acc_pca)}\n"
                    "    ...\n"
                ),
                hints=[
                    "Pipeline garantiza que el scaler se ajusta solo en train por fold.",
                    "En iris con n_components=2, acc_full ~0.96 y acc_pca ~0.91.",
                    "float(acc) en la salida para que el dict no tenga numpy.float64.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "iris n=2 -> ambos > 0.9, full >= pca, dict shape correcta",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "res = pca_conserva_accuracy(X, y, 2)\n"
                            "assert isinstance(res, dict), type(res)\n"
                            "assert set(res.keys()) == {'full', 'pca'}, res.keys()\n"
                            "assert isinstance(res['full'], float), type(res['full'])\n"
                            "assert isinstance(res['pca'], float), type(res['pca'])\n"
                            "assert res['full'] > 0.9, res\n"
                            "assert res['pca'] > 0.9, res\n"
                            "assert res['full'] >= res['pca'], res"
                        ),
                    },
                    {
                        "name": "iris n=4 -> pca deberia igualar full (mismas dimensiones = sin perdida)",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "res = pca_conserva_accuracy(X, y, 4)\n"
                            "assert abs(res['full'] - res['pca']) < 0.02, res"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 9 · Support Vector Machines (SVM)",
        description=(
            "Margen maximo, kernel trick (linear vs rbf), y por que "
            "el escalado y los support vectors importan."
        ),
        content=(
            "# ML 9: Support Vector Machines\n\n"
            "Una **SVM** busca la frontera que separa las clases dejando "
            "el **margen mas ancho posible** entre ellas. No cualquier "
            "recta que separe: la que queda mas lejos de los puntos de "
            "ambos lados. Esos puntos criticos que tocan el margen son "
            "los **support vectors**, y son los unicos que definen la "
            "frontera (si mueves un punto lejano, la frontera no cambia).\n\n"
            "## Tres ideas clave\n\n"
            "### 1. Margen maximo\n\n"
            "Entre todas las fronteras que separan las clases, la SVM "
            "elige la de mayor margen. Un margen ancho generaliza mejor: "
            "deja mas 'colchon' antes de equivocarse con datos nuevos.\n\n"
            "```python\n"
            "from sklearn.svm import SVC\n"
            "clf = SVC(kernel='linear', C=1.0, random_state=42)\n"
            "clf.fit(X_train, y_train)\n"
            "print(clf.support_vectors_.shape)  # cuantos SV definen la frontera\n"
            "```\n\n"
            "### 2. El kernel trick: separar lo no separable\n\n"
            "Muchos datos **no** se separan con una recta. El kernel "
            "**rbf** proyecta los datos a un espacio de mas dimensiones "
            "donde si son linealmente separables, sin calcularlo "
            "explicitamente. Sobre datos con forma de lunas o circulos, "
            "`kernel='rbf'` supera claramente a `kernel='linear'`:\n\n"
            "```\n"
            "make_moons (no lineal):\n"
            "  kernel linear:  CV accuracy ~0.85\n"
            "  kernel rbf:     CV accuracy ~0.96\n"
            "```\n\n"
            "### 3. C y gamma\n\n"
            "- **C** controla el trade-off margen vs errores. C grande = "
            "menos tolerante a errores (margen estrecho, riesgo de "
            "overfit); C pequeno = margen ancho, mas tolerante.\n"
            "- **gamma** (solo rbf) controla el alcance de cada punto. "
            "Gamma grande = fronteras muy locales (overfit); `gamma="
            "'scale'` es el default sensato.\n\n"
            "## Escalado obligatorio\n\n"
            "La SVM mide **distancias**, asi que es sensible a la escala "
            "igual que KNN. **Siempre** `StandardScaler` antes (dentro de "
            "un `Pipeline`), o una feature de rango grande dominara.\n\n"
            "```python\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "pipe = Pipeline([('sc', StandardScaler()),\n"
            "                 ('svc', SVC(kernel='rbf', gamma='scale'))])\n"
            "```\n\n"
            "## Cuando usar SVM\n\n"
            "- **Datasets pequenos/medianos** con frontera compleja: rbf "
            "brilla.\n"
            "- **Muchas features, pocas muestras** (texto, genomica): SVM "
            "lineal es fuerte.\n"
            "- **Evitala** en datasets enormes (millones de filas): "
            "escala mal con n (usa modelos lineales o arboles).\n"
            "- **No da probabilidades** de forma natural (necesita "
            "`probability=True`, que la hace mas lenta).\n\n"
            "## Resumen\n\n"
            "- SVM maximiza el margen; solo los **support vectors** "
            "cuentan.\n"
            "- `kernel='rbf'` separa datos no lineales; `linear` para "
            "alta dimension.\n"
            "- **Escala siempre** antes con `StandardScaler`.\n"
            "- Ajusta `C` (y `gamma` en rbf); usa `gamma='scale'` de "
            "base.\n"
        ),
        difficulty="intermediate",
        category="ml-svm",
        order=30,
        track="track-3",
        estimated_duration=50,
        prerequisites_titles=[
            "ML 8 · PCA para reducir dimensionalidad",
        ],
        exercises=[
            ExerciseTemplate(
                title="Entrenar una SVM con kernel configurable",
                description=(
                    "Entrena una SVC con kernel y C dados y devuelve la "
                    "accuracy en test."
                ),
                instructions=(
                    "Implementa `entrenar_svm(X_train, y_train, X_test, "
                    "y_test, kernel='rbf', C=1.0)` que crea "
                    "`SVC(kernel=kernel, C=C, gamma='scale', "
                    "random_state=42)`, la entrena con train y devuelve "
                    "la accuracy sobre test como `float`. Asume que X ya "
                    "viene escalado."
                ),
                starter_code=(
                    "from sklearn.svm import SVC\n"
                    "\n"
                    "\n"
                    "def entrenar_svm(X_train, y_train, X_test, y_test, kernel='rbf', C=1.0):\n"
                    "    # TODO: clf = SVC(kernel=kernel, C=C, gamma='scale', random_state=42)\n"
                    "    # TODO: clf.fit(X_train, y_train)\n"
                    "    # TODO: return float(clf.score(X_test, y_test))\n"
                    "    ...\n"
                ),
                hints=[
                    "clf.score(X, y) ya devuelve la accuracy.",
                    "gamma='scale' es el default sensato para rbf.",
                    "En datos no lineales, rbf supera a linear.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "moons escalado: rbf >0.9 y rbf >= linear",
                        "code": (
                            "from sklearn.datasets import make_moons\n"
                            "from sklearn.preprocessing import StandardScaler\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "X, y = make_moons(n_samples=200, noise=0.2, random_state=42)\n"
                            "Xs = StandardScaler().fit_transform(X)\n"
                            "Xtr, Xte, ytr, yte = train_test_split(Xs, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "rbf = entrenar_svm(Xtr, ytr, Xte, yte, kernel='rbf')\n"
                            "lin = entrenar_svm(Xtr, ytr, Xte, yte, kernel='linear')\n"
                            "assert isinstance(rbf, float), type(rbf)\n"
                            "assert rbf > 0.9, rbf\n"
                            "assert lin > 0.8, lin\n"
                            "assert rbf >= lin, (rbf, lin)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Comparar kernels linear vs rbf",
                description=(
                    "Compara la accuracy CV de un kernel lineal contra "
                    "uno rbf sobre datos no lineales."
                ),
                instructions=(
                    "Implementa `comparar_kernels(X, y)` que, para cada "
                    "kernel en `['linear', 'rbf']`, arma un "
                    "`Pipeline([StandardScaler, SVC(kernel=..., "
                    "gamma='scale', random_state=42)])`, calcula "
                    "`cross_val_score(pipe, X, y, cv=5).mean()` y devuelve "
                    "un dict `{'linear': media, 'rbf': media}` con floats."
                ),
                starter_code=(
                    "from sklearn.svm import SVC\n"
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "from sklearn.model_selection import cross_val_score\n"
                    "\n"
                    "\n"
                    "def comparar_kernels(X, y):\n"
                    "    # TODO: para cada kernel arma pipeline con StandardScaler + SVC\n"
                    "    # TODO: media = cross_val_score(pipe, X, y, cv=5).mean()\n"
                    "    # TODO: return {'linear': ..., 'rbf': ...}\n"
                    "    ...\n"
                ),
                hints=[
                    "Un dict comprehension sobre los dos kernels es suficiente.",
                    "cross_val_score devuelve un array; usa .mean().",
                    "En make_moons el rbf gana con holgura.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "moons: rbf supera a linear, ambos floats",
                        "code": (
                            "from sklearn.datasets import make_moons\n"
                            "X, y = make_moons(n_samples=200, noise=0.2, random_state=42)\n"
                            "res = comparar_kernels(X, y)\n"
                            "assert set(res.keys()) == {'linear', 'rbf'}, res.keys()\n"
                            "assert isinstance(res['rbf'], float), type(res['rbf'])\n"
                            "assert res['rbf'] > res['linear'], res\n"
                            "assert res['rbf'] > 0.9, res['rbf']"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Contar support vectors",
                description=(
                    "Cuenta cuantos puntos de entrenamiento terminan "
                    "siendo support vectors."
                ),
                instructions=(
                    "Implementa `n_support_vectors(X_train, y_train, "
                    "kernel='linear')` que entrena "
                    "`SVC(kernel=kernel, gamma='scale', random_state=42)` "
                    "y devuelve el numero total de support vectors "
                    "(`clf.support_vectors_.shape[0]`) como `int`."
                ),
                starter_code=(
                    "from sklearn.svm import SVC\n"
                    "\n"
                    "\n"
                    "def n_support_vectors(X_train, y_train, kernel='linear'):\n"
                    "    # TODO: clf = SVC(kernel=kernel, gamma='scale', random_state=42)\n"
                    "    # TODO: clf.fit(X_train, y_train)\n"
                    "    # TODO: return int(clf.support_vectors_.shape[0])\n"
                    "    ...\n"
                ),
                hints=[
                    "support_vectors_ es un array (n_sv, n_features).",
                    "Los SV son un subconjunto del train, nunca mas que len(y_train).",
                    "La frontera depende SOLO de esos puntos.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "moons: 0 < n_sv < n_train",
                        "code": (
                            "from sklearn.datasets import make_moons\n"
                            "from sklearn.preprocessing import StandardScaler\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "X, y = make_moons(n_samples=200, noise=0.2, random_state=42)\n"
                            "Xs = StandardScaler().fit_transform(X)\n"
                            "Xtr, Xte, ytr, yte = train_test_split(Xs, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "n = n_support_vectors(Xtr, ytr, kernel='linear')\n"
                            "assert isinstance(n, int), type(n)\n"
                            "assert 0 < n < len(ytr), (n, len(ytr))"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 10 · Naive Bayes",
        description=(
            "Clasificador probabilistico basado en el teorema de Bayes "
            "y la suposicion 'naive' de independencia. Rapido y buen "
            "baseline."
        ),
        content=(
            "# ML 10: Naive Bayes\n\n"
            "**Naive Bayes** es un clasificador probabilistico que aplica "
            "el **teorema de Bayes** asumiendo que las features son "
            "**independientes entre si** dada la clase. Esa suposicion "
            "casi nunca es literalmente cierta (por eso 'naive', "
            "ingenua), pero funciona sorprendentemente bien y es "
            "**rapidisimo** de entrenar.\n\n"
            "## La idea\n\n"
            "Para cada clase, calcula la probabilidad de que la muestra "
            "pertenezca a ella y elige la mayor:\n\n"
            "```\n"
            "P(clase | features) proporcional a P(clase) * prod P(feature_i | clase)\n"
            "```\n\n"
            "El termino `prod P(feature_i | clase)` es donde entra la "
            "suposicion naive: multiplica las probabilidades de cada "
            "feature como si fueran independientes.\n\n"
            "## Variantes\n\n"
            "- **GaussianNB**: features continuas; asume que cada feature "
            "sigue una normal por clase. Es la que usaras con datos como "
            "iris.\n"
            "- **MultinomialNB**: conteos (bolsa de palabras en texto).\n"
            "- **BernoulliNB**: features binarias (presencia/ausencia).\n\n"
            "```python\n"
            "from sklearn.naive_bayes import GaussianNB\n"
            "clf = GaussianNB()\n"
            "clf.fit(X_train, y_train)\n"
            "print(clf.predict_proba(X_test)[:3])  # probabilidades por clase\n"
            "```\n\n"
            "## Da probabilidades calibradas-ish\n\n"
            "A diferencia de la SVM, Naive Bayes entrega `predict_proba` "
            "de forma natural: cada fila suma 1 (una distribucion sobre "
            "las clases). Util cuando necesitas confianza, no solo la "
            "etiqueta.\n\n"
            "## Baseline fuerte y barato\n\n"
            "Sobre iris, GaussianNB (~0.95 CV) queda a un pelo de "
            "LogisticRegression (~0.97), sin tuning y entrenando en "
            "milisegundos:\n\n"
            "```\n"
            "iris (CV 5-fold):\n"
            "  GaussianNB:          ~0.953\n"
            "  LogisticRegression:  ~0.973\n"
            "```\n\n"
            "Por eso Naive Bayes es un **baseline** que deberias probar "
            "antes de sacar la artilleria: si tu modelo complejo no lo "
            "supera, algo esta mal.\n\n"
            "## Cuando usar Naive Bayes\n\n"
            "- **Clasificacion de texto / spam** — MultinomialNB es un "
            "clasico que sigue vigente.\n"
            "- **Baseline rapido** en cualquier problema de "
            "clasificacion.\n"
            "- **Muchisimas features** — como asume independencia, no "
            "sufre tanto la maldicion de la dimensionalidad.\n"
            "- **Evitalo** cuando las features estan muy correlacionadas "
            "(la suposicion naive se rompe) y necesitas exprimir "
            "accuracy.\n\n"
            "## Resumen\n\n"
            "- Aplica Bayes asumiendo independencia entre features.\n"
            "- `GaussianNB` para continuas, `MultinomialNB` para conteos.\n"
            "- Entrega `predict_proba` (filas suman 1).\n"
            "- Rapido, sin hiperparametros, gran baseline.\n"
        ),
        difficulty="intermediate",
        category="ml-naive-bayes",
        order=31,
        track="track-3",
        estimated_duration=45,
        prerequisites_titles=[
            "ML 9 · Support Vector Machines (SVM)",
        ],
        exercises=[
            ExerciseTemplate(
                title="Entrenar GaussianNB",
                description=(
                    "Entrena un GaussianNB y devuelve la accuracy en " "test."
                ),
                instructions=(
                    "Implementa `entrenar_gnb(X_train, y_train, X_test, "
                    "y_test)` que crea `GaussianNB()`, la entrena con "
                    "train y devuelve la accuracy sobre test como "
                    "`float`."
                ),
                starter_code=(
                    "from sklearn.naive_bayes import GaussianNB\n"
                    "\n"
                    "\n"
                    "def entrenar_gnb(X_train, y_train, X_test, y_test):\n"
                    "    # TODO: clf = GaussianNB(); clf.fit(X_train, y_train)\n"
                    "    # TODO: return float(clf.score(X_test, y_test))\n"
                    "    ...\n"
                ),
                hints=[
                    "GaussianNB no lleva hiperparametros.",
                    "clf.score(X, y) devuelve la accuracy.",
                    "GaussianNB ni siquiera necesita escalado.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "iris split 0.3 -> accuracy > 0.85",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "acc = entrenar_gnb(Xtr, ytr, Xte, yte)\n"
                            "assert isinstance(acc, float), type(acc)\n"
                            "assert acc > 0.85, acc"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Probabilidades por clase",
                description=(
                    "Devuelve la matriz de probabilidades predichas y "
                    "verifica que cada fila es una distribucion."
                ),
                instructions=(
                    "Implementa `proba_gnb(X_train, y_train, X_test)` que "
                    "entrena `GaussianNB` con train y devuelve "
                    "`clf.predict_proba(X_test)` (un `np.ndarray` de shape "
                    "`(n_test, n_clases)` donde cada fila suma 1)."
                ),
                starter_code=(
                    "from sklearn.naive_bayes import GaussianNB\n"
                    "\n"
                    "\n"
                    "def proba_gnb(X_train, y_train, X_test):\n"
                    "    # TODO: clf = GaussianNB(); clf.fit(X_train, y_train)\n"
                    "    # TODO: return clf.predict_proba(X_test)\n"
                    "    ...\n"
                ),
                hints=[
                    "predict_proba devuelve una fila por muestra.",
                    "Cada fila es una distribucion: suma 1.",
                    "iris tiene 3 clases -> 3 columnas.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "iris: shape (n,3), filas suman 1, valores en [0,1]",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.datasets import load_iris\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)\n"
                            "P = np.asarray(proba_gnb(Xtr, ytr, Xte))\n"
                            "assert P.shape == (45, 3), P.shape\n"
                            "assert np.allclose(P.sum(axis=1), 1.0), P.sum(axis=1)[:5]\n"
                            "assert (P >= 0).all() and (P <= 1).all()"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Naive Bayes vs Logistic Regression",
                description=(
                    "Compara CV de GaussianNB contra LogisticRegression "
                    "como baseline."
                ),
                instructions=(
                    "Implementa `nb_vs_logreg(X, y)` que calcula "
                    "`cross_val_score(clf, X, y, cv=5).mean()` para "
                    "`GaussianNB()` y para "
                    "`LogisticRegression(max_iter=1000)`, y devuelve un "
                    "dict `{'nb': media_nb, 'logreg': media_logreg}` con "
                    "floats."
                ),
                starter_code=(
                    "from sklearn.naive_bayes import GaussianNB\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.model_selection import cross_val_score\n"
                    "\n"
                    "\n"
                    "def nb_vs_logreg(X, y):\n"
                    "    # TODO: nb = cross_val_score(GaussianNB(), X, y, cv=5).mean()\n"
                    "    # TODO: lr = cross_val_score(LogisticRegression(max_iter=1000), X, y, cv=5).mean()\n"
                    "    # TODO: return {'nb': float(nb), 'logreg': float(lr)}\n"
                    "    ...\n"
                ),
                hints=[
                    "Naive Bayes suele quedar competitivo, no muy por debajo.",
                    "Ambos deberian superar 0.9 en iris.",
                    "NB entrena mucho mas rapido que LogReg.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "iris: ambos > 0.9, keys correctas",
                        "code": (
                            "from sklearn.datasets import load_iris\n"
                            "X, y = load_iris(return_X_y=True)\n"
                            "res = nb_vs_logreg(X, y)\n"
                            "assert set(res.keys()) == {'nb', 'logreg'}, res.keys()\n"
                            "assert isinstance(res['nb'], float), type(res['nb'])\n"
                            "assert res['nb'] > 0.9, res\n"
                            "assert res['logreg'] > 0.9, res"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="ML 11 · Curva ROC, AUC y umbral de decision",
        description=(
            "Evaluar clasificadores binarios de forma agnostica al "
            "umbral: TPR vs FPR, AUC y como mover el umbral cambia "
            "precision/recall."
        ),
        content=(
            "# ML 11: Curva ROC, AUC y umbral\n\n"
            "Un clasificador binario no solo dice 0 o 1: internamente "
            "calcula una **probabilidad** (o score) y la compara contra "
            "un **umbral** (por defecto 0.5). Cambiar ese umbral cambia "
            "el balance entre atrapar positivos y evitar falsas alarmas. "
            "La **curva ROC** y el **AUC** miden que tan bueno es el "
            "modelo **independientemente del umbral que elijas**.\n\n"
            "## La curva ROC\n\n"
            "Barre todos los umbrales posibles y grafica:\n\n"
            "- **TPR** (recall, eje Y): de los positivos reales, cuantos "
            "atrapo.\n"
            "- **FPR** (eje X): de los negativos reales, cuantos marco "
            "por error.\n\n"
            "```python\n"
            "from sklearn.metrics import roc_curve\n"
            "proba = pipe.predict_proba(X_test)[:, 1]\n"
            "fpr, tpr, thresholds = roc_curve(y_test, proba)\n"
            "```\n\n"
            "Un modelo perfecto pasa por la esquina superior izquierda "
            "(TPR=1, FPR=0). La diagonal es el azar.\n\n"
            "## AUC: un numero para resumir la curva\n\n"
            "El **AUC** (area bajo la ROC) resume la curva en un valor "
            "entre 0.5 (azar) y 1.0 (perfecto). Interpretacion elegante: "
            "es la probabilidad de que el modelo asigne mayor score a un "
            "positivo aleatorio que a un negativo aleatorio.\n\n"
            "```python\n"
            "from sklearn.metrics import roc_auc_score\n"
            "auc = roc_auc_score(y_test, proba)   # ~0.995 en breast_cancer\n"
            "```\n\n"
            "**Clave**: AUC usa las **probabilidades**, no las etiquetas "
            "0/1. No depende del umbral, por eso compara modelos de forma "
            "mas justa que la accuracy.\n\n"
            "## Mover el umbral: precision vs recall\n\n"
            "El umbral 0.5 no es sagrado. **Bajarlo** marca mas cosas "
            "como positivas: sube el **recall** (atrapas mas positivos) "
            "pero baja la **precision** (mas falsas alarmas). Subirlo "
            "hace lo contrario.\n\n"
            "```\n"
            "breast_cancer (clase benigno):\n"
            "  umbral 0.5:  precision 0.99, recall 0.99\n"
            "  umbral 0.3:  precision 0.97, recall 1.00   <- no se escapa ninguno\n"
            "```\n\n"
            "En medicina o fraude, muchas veces prefieres **recall alto** "
            "(no perder un caso) aunque cueste precision. Eliges el "
            "umbral segun el costo de cada tipo de error, no por "
            "defecto.\n\n"
            "## Cuando mirar ROC/AUC\n\n"
            "- **Clasificacion binaria** donde el umbral es ajustable.\n"
            "- **Clases desbalanceadas**: AUC es mas informativo que "
            "accuracy (recuerda ML 2).\n"
            "- **Comparar modelos** sin fijar un umbral arbitrario.\n"
            "- **Ojo**: con desbalance extremo, la curva "
            "**precision-recall** (PR) puede ser mas honesta que la ROC.\n\n"
            "## Resumen\n\n"
            "- `roc_curve` da (fpr, tpr, thresholds); graficala para ver "
            "el trade-off.\n"
            "- `roc_auc_score` resume la calidad en [0.5, 1.0], usando "
            "**probabilidades**.\n"
            "- El **umbral** es una decision de negocio: bajalo para mas "
            "recall, subelo para mas precision.\n"
        ),
        difficulty="intermediate",
        category="ml-roc",
        order=32,
        track="track-3",
        estimated_duration=50,
        prerequisites_titles=[
            "ML 10 · Naive Bayes",
        ],
        exercises=[
            ExerciseTemplate(
                title="Calcular el AUC de un modelo",
                description=(
                    "Entrena un pipeline y devuelve el ROC AUC usando "
                    "probabilidades."
                ),
                instructions=(
                    "Implementa `auc_modelo(X_train, y_train, X_test, "
                    "y_test)` que arma un "
                    "`Pipeline([StandardScaler, "
                    "LogisticRegression(max_iter=5000, "
                    "random_state=42)])`, lo entrena, saca "
                    "`predict_proba(X_test)[:, 1]` y devuelve "
                    "`roc_auc_score(y_test, proba)` como `float`."
                ),
                starter_code=(
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.metrics import roc_auc_score\n"
                    "\n"
                    "\n"
                    "def auc_modelo(X_train, y_train, X_test, y_test):\n"
                    "    # TODO: arma y entrena el pipeline\n"
                    "    # TODO: proba = pipe.predict_proba(X_test)[:, 1]\n"
                    "    # TODO: return float(roc_auc_score(y_test, proba))\n"
                    "    ...\n"
                ),
                hints=[
                    "AUC usa las probabilidades de la clase positiva (columna 1).",
                    "roc_auc_score(y_true, y_score) NO recibe etiquetas 0/1.",
                    "En breast_cancer el AUC pasa de 0.99.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "breast_cancer: AUC > 0.98",
                        "code": (
                            "from sklearn.datasets import load_breast_cancer\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "X, y = load_breast_cancer(return_X_y=True)\n"
                            "Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\n"
                            "auc = auc_modelo(Xtr, ytr, Xte, yte)\n"
                            "assert isinstance(auc, float), type(auc)\n"
                            "assert 0.98 < auc <= 1.0, auc"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Puntos de la curva ROC",
                description=(
                    "Devuelve fpr, tpr y thresholds y verifica sus " "propiedades."
                ),
                instructions=(
                    "Implementa `curva_roc(X_train, y_train, X_test, "
                    "y_test)` que entrena el mismo pipeline (StandardScaler "
                    "+ LogisticRegression max_iter=5000, random_state=42), "
                    "saca las probabilidades de la clase 1 y devuelve la "
                    "tupla `(fpr, tpr, thresholds)` de "
                    "`roc_curve(y_test, proba)`."
                ),
                starter_code=(
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.metrics import roc_curve\n"
                    "\n"
                    "\n"
                    "def curva_roc(X_train, y_train, X_test, y_test):\n"
                    "    # TODO: entrena el pipeline y saca proba de clase 1\n"
                    "    # TODO: return roc_curve(y_test, proba)\n"
                    "    ...\n"
                ),
                hints=[
                    "roc_curve devuelve tres arrays alineados.",
                    "fpr y tpr son monotonos no decrecientes.",
                    "La curva arranca en fpr=0 y termina en tpr=1.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "breast_cancer: fpr/tpr monotonos, arranca 0 termina 1",
                        "code": (
                            "import numpy as np\n"
                            "from sklearn.datasets import load_breast_cancer\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "X, y = load_breast_cancer(return_X_y=True)\n"
                            "Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\n"
                            "fpr, tpr, thr = curva_roc(Xtr, ytr, Xte, yte)\n"
                            "fpr = np.asarray(fpr); tpr = np.asarray(tpr)\n"
                            "assert len(fpr) == len(tpr), (len(fpr), len(tpr))\n"
                            "assert fpr[0] == 0.0, fpr[0]\n"
                            "assert tpr[-1] == 1.0, tpr[-1]\n"
                            "assert np.all(np.diff(fpr) >= 0), 'fpr no monotona'\n"
                            "assert np.all(np.diff(tpr) >= 0), 'tpr no monotona'"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Metricas segun el umbral",
                description=(
                    "Calcula precision y recall a un umbral dado y "
                    "comprueba el trade-off."
                ),
                instructions=(
                    "Implementa `metricas_umbral(X_train, y_train, "
                    "X_test, y_test, umbral)` que entrena el pipeline "
                    "(StandardScaler + LogisticRegression max_iter=5000, "
                    "random_state=42), predice positivo cuando "
                    "`predict_proba` de la clase 1 es `>= umbral`, y "
                    "devuelve un dict `{'precision': ..., 'recall': ...}` "
                    "con floats (usa `zero_division=0`)."
                ),
                starter_code=(
                    "from sklearn.pipeline import Pipeline\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.metrics import precision_score, recall_score\n"
                    "\n"
                    "\n"
                    "def metricas_umbral(X_train, y_train, X_test, y_test, umbral):\n"
                    "    # TODO: entrena pipeline, proba = predict_proba(X_test)[:, 1]\n"
                    "    # TODO: pred = (proba >= umbral).astype(int)\n"
                    "    # TODO: return {'precision': ..., 'recall': ...}\n"
                    "    ...\n"
                ),
                hints=[
                    "Bajar el umbral atrapa mas positivos: sube el recall.",
                    "zero_division=0 evita warnings si no marcas ningun positivo.",
                    "Compara 0.5 vs 0.3 para ver el trade-off.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "breast_cancer: bajar umbral 0.5->0.3 no baja el recall",
                        "code": (
                            "from sklearn.datasets import load_breast_cancer\n"
                            "from sklearn.model_selection import train_test_split\n"
                            "X, y = load_breast_cancer(return_X_y=True)\n"
                            "Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\n"
                            "m5 = metricas_umbral(Xtr, ytr, Xte, yte, 0.5)\n"
                            "m3 = metricas_umbral(Xtr, ytr, Xte, yte, 0.3)\n"
                            "assert set(m5.keys()) == {'precision', 'recall'}, m5.keys()\n"
                            "assert isinstance(m5['recall'], float), type(m5['recall'])\n"
                            "assert m3['recall'] >= m5['recall'], (m5, m3)\n"
                            "assert m5['precision'] >= m3['precision'] - 1e-9, (m5, m3)"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="DL 1 · La neurona: forward pass y activaciones",
        description=(
            "Arranca Deep Learning desde cero con numpy: que es una "
            "neurona, el forward pass (X @ W + b) y por que las "
            "funciones de activacion dan no-linealidad."
        ),
        content=(
            "# DL 1: la neurona y el forward pass\n\n"
            "Bienvenido al **Track 4 (Deep Learning)**. Antes de tocar "
            "PyTorch vas a entender que hace una red neuronal por "
            "dentro, y lo vas a construir con **numpy puro** (el mismo "
            "que ya usaste en Data Science). Una red no es magia: es "
            "multiplicacion de matrices + una funcion no lineal, "
            "repetido en capas.\n\n"
            "## La neurona\n\n"
            "Una **neurona** toma un vector de entradas `x`, lo combina "
            "linealmente con unos **pesos** `w` y un **sesgo** `b`, y "
            "pasa el resultado por una **funcion de activacion** `f`:\n\n"
            "```\n"
            "z = w . x + b        (combinacion lineal, un escalar)\n"
            "a = f(z)             (activacion)\n"
            "```\n\n"
            "Con varias neuronas en paralelo (una **capa**), los pesos "
            "pasan a ser una matriz `W` y el calculo se vectoriza para "
            "un **batch** de muestras `X` de una sola vez:\n\n"
            "```python\n"
            "import numpy as np\n"
            "Z = X @ W + b        # X: (n_muestras, n_features)\n"
            "                     # W: (n_features, n_units)\n"
            "                     # b: (n_units,)  -> broadcasting\n"
            "                     # Z: (n_muestras, n_units)\n"
            "A = f(Z)\n"
            "```\n\n"
            "El operador `@` es el producto matricial. Ese `X @ W + b` "
            "es **el forward pass de una capa densa**, la operacion mas "
            "repetida en todo el deep learning.\n\n"
            "## Funciones de activacion\n\n"
            "Sin activacion, apilar capas seria inutil: la composicion "
            "de funciones lineales es otra funcion lineal. La "
            "**no-linealidad** es lo que permite a la red aprender "
            "relaciones complejas.\n\n"
            "### Sigmoid\n\n"
            "Aplasta cualquier numero al rango `(0, 1)`. Util para "
            "probabilidades en la capa de salida.\n\n"
            "```\n"
            "sigmoid(z) = 1 / (1 + e^-z)\n"
            "  sigmoid(0)   = 0.5\n"
            "  sigmoid(+inf) -> 1\n"
            "  sigmoid(-inf) -> 0\n"
            "```\n\n"
            "```python\n"
            "def sigmoid(z):\n"
            "    return 1.0 / (1.0 + np.exp(-z))\n"
            "```\n\n"
            "### ReLU\n\n"
            "`relu(z) = max(0, z)`. Cero para negativos, identidad para "
            "positivos. Es la activacion por defecto en las capas "
            "ocultas modernas: barata y no satura para valores "
            "positivos.\n\n"
            "```python\n"
            "def relu(z):\n"
            "    return np.maximum(0.0, z)\n"
            "```\n\n"
            "### tanh\n\n"
            "Parecida a sigmoid pero centrada en 0, rango `(-1, 1)`. "
            "`np.tanh(z)` ya viene en numpy.\n\n"
            "## Por que numpy y no PyTorch (todavia)\n\n"
            "PyTorch automatiza el calculo de gradientes (lo veras "
            "pronto), pero **el forward pass es exactamente esto**: "
            "`X @ W + b` y una activacion. Construirlo a mano en numpy "
            "te da la intuicion que despues PyTorch te esconde. Cuando "
            "pasemos al framework, no sera una caja negra.\n\n"
            "## Errores comunes\n\n"
            "1. **Dimensiones de W al reves** — si `X` es `(n, features)`, "
            "entonces `W` debe ser `(features, units)`. Si las inviertes, "
            "`@` lanza un error de shapes.\n"
            "2. **Olvidar el sesgo** — `b` se suma por broadcasting sobre "
            "cada muestra del batch; su shape es `(units,)`.\n"
            "3. **Aplicar la activacion antes de sumar b** — el orden es "
            "`f(X @ W + b)`, no `f(X @ W) + b`.\n"
            "4. **Creer que sin activacion la red es mas potente** — sin "
            "no-linealidad, 10 capas equivalen a 1.\n\n"
            "## Resumen\n\n"
            "- Una neurona: `a = f(w . x + b)`.\n"
            "- Una capa densa vectorizada: `A = f(X @ W + b)`.\n"
            "- `sigmoid` -> (0,1), `relu` -> max(0, z), `tanh` -> "
            "(-1,1).\n"
            "- La activacion aporta la no-linealidad; sin ella apilar "
            "capas no sirve.\n"
        ),
        difficulty="intermediate",
        category="dl-fundamentos",
        order=33,
        track="track-4",
        estimated_duration=50,
        prerequisites_titles=[
            "ML 11 · Curva ROC, AUC y umbral de decision",
        ],
        exercises=[
            ExerciseTemplate(
                title="Funcion sigmoid",
                description=(
                    "Implementa la activacion sigmoid, vectorizada con " "numpy."
                ),
                instructions=(
                    "Implementa `sigmoid(z)` que devuelve "
                    "`1 / (1 + e^-z)` usando numpy, funcionando tanto "
                    "para escalares como para arrays (vectorizada). "
                    "Convierte la entrada con `np.asarray(z, dtype=float)` "
                    "y usa `np.exp`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def sigmoid(z):\n"
                    "    # TODO: z = np.asarray(z, dtype=float)\n"
                    "    # TODO: return 1.0 / (1.0 + np.exp(-z))\n"
                    "    ...\n"
                ),
                hints=[
                    "np.exp aplica e^x elemento a elemento.",
                    "sigmoid(0) debe dar exactamente 0.5.",
                    "El resultado siempre queda entre 0 y 1.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "sigmoid(0)=0.5, rango (0,1), monotona, vectorizada",
                        "code": (
                            "import numpy as np\n"
                            "assert abs(float(sigmoid(0.0)) - 0.5) < 1e-9\n"
                            "z = np.array([-20.0, -1.0, 0.0, 1.0, 20.0])\n"
                            "s = np.asarray(sigmoid(z))\n"
                            "assert s.shape == (5,), s.shape\n"
                            "assert np.all((s > 0) & (s < 1)), s\n"
                            "assert np.all(np.diff(s) > 0), 'no monotona'\n"
                            "assert s[0] < 1e-6 and s[-1] > 0.999999, s"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Funcion ReLU",
                description=(
                    "Implementa la activacion ReLU con numpy, " "vectorizada."
                ),
                instructions=(
                    "Implementa `relu(z)` que devuelve `max(0, z)` "
                    "elemento a elemento usando `np.maximum`. Debe "
                    "preservar la shape de la entrada (escalares, "
                    "vectores o matrices)."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def relu(z):\n"
                    "    # TODO: z = np.asarray(z, dtype=float)\n"
                    "    # TODO: return np.maximum(0.0, z)\n"
                    "    ...\n"
                ),
                hints=[
                    "np.maximum compara elemento a elemento (no confundir con np.max).",
                    "Los negativos van a 0; los positivos quedan igual.",
                    "La shape de salida es la misma que la de entrada.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "relu: negativos->0, positivos igual, preserva shape",
                        "code": (
                            "import numpy as np\n"
                            "z = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])\n"
                            "r = np.asarray(relu(z))\n"
                            "assert r.shape == (5,), r.shape\n"
                            "assert np.allclose(r, [0, 0, 0, 1, 2]), r\n"
                            "Z = np.array([[-1.0, 3.0], [2.0, -5.0]])\n"
                            "assert np.asarray(relu(Z)).shape == (2, 2)\n"
                            "assert np.all(np.asarray(relu(Z)) >= 0)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Forward pass de una capa densa",
                description=(
                    "Combina producto matricial, sesgo y activacion en "
                    "el forward de una capa."
                ),
                instructions=(
                    "Implementa `forward_capa(X, W, b, activacion)` que "
                    "calcula `activacion(X @ W + b)`, donde `X` es "
                    "`(n_muestras, n_features)`, `W` es "
                    "`(n_features, n_units)`, `b` es `(n_units,)` y "
                    "`activacion` es una funcion (p.ej. `relu` o "
                    "`sigmoid`). Devuelve un array `(n_muestras, "
                    "n_units)`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def forward_capa(X, W, b, activacion):\n"
                    "    # TODO: z = np.asarray(X, float) @ np.asarray(W, float) + np.asarray(b, float)\n"
                    "    # TODO: return activacion(z)\n"
                    "    ...\n"
                ),
                hints=[
                    "El orden importa: primero X @ W + b, luego la activacion.",
                    "b se suma por broadcasting sobre cada fila del batch.",
                    "Si las shapes no cuadran, revisa que W sea (features, units).",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "forward_capa: shape (n,units) + valores con relu/sigmoid/lineal",
                        "code": (
                            "import numpy as np\n"
                            "# El test define sus propias activaciones (namespace aislado)\n"
                            "_relu = lambda x: np.maximum(0.0, x)\n"
                            "_sig = lambda x: 1.0 / (1.0 + np.exp(-x))\n"
                            "X = np.array([[1.0, 2.0]])\n"
                            "W = np.array([[0.5], [-0.5]])\n"
                            "b = np.array([0.0])\n"
                            "out_lin = np.asarray(forward_capa(X, W, b, lambda x: x))\n"
                            "assert out_lin.shape == (1, 1), out_lin.shape\n"
                            "assert abs(float(out_lin[0, 0]) - (-0.5)) < 1e-9, out_lin\n"
                            "out_relu = np.asarray(forward_capa(X, W, b, _relu))\n"
                            "assert abs(float(out_relu[0, 0]) - 0.0) < 1e-9, out_relu\n"
                            "out_sig = np.asarray(forward_capa(X, W, b, _sig))\n"
                            "assert abs(float(out_sig[0, 0]) - 0.37754067) < 1e-6, out_sig\n"
                            "Xb = np.ones((3, 2))\n"
                            "Wb = np.ones((2, 4))\n"
                            "bb = np.zeros(4)\n"
                            "assert np.asarray(forward_capa(Xb, Wb, bb, _relu)).shape == (3, 4)"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="DL 2 · Funciones de perdida y gradiente numerico",
        description=(
            "Como mide una red que tan mal lo hace (MSE, cross-entropy) "
            "y como se aproxima un gradiente por diferencias finitas."
        ),
        content=(
            "# DL 2: funciones de perdida y gradiente numerico\n\n"
            "En DL 1 hiciste el forward pass: la red produce una "
            "prediccion. Ahora falta lo mas importante para "
            "**aprender**: medir que tan equivocada esta esa prediccion "
            "y en que direccion mover los pesos para mejorarla. Eso son "
            "la **funcion de perdida** y el **gradiente**.\n\n"
            "## La funcion de perdida\n\n"
            "Una **perdida** (loss) es un numero que resume el error: "
            "grande cuando la red se equivoca, cero cuando acierta "
            "perfecto. Entrenar = **minimizar** la perdida. Cual usar "
            "depende del problema.\n\n"
            "### MSE (error cuadratico medio) — regresion\n\n"
            "Para predecir numeros continuos:\n\n"
            "```\n"
            "MSE = promedio( (y_pred - y_true)^2 )\n"
            "```\n\n"
            "Eleva al cuadrado para (a) penalizar mas los errores "
            "grandes y (b) que el signo no importe. MSE = 0 solo si la "
            "prediccion es exacta.\n\n"
            "```python\n"
            "import numpy as np\n"
            "def mse(y_true, y_pred):\n"
            "    y_true = np.asarray(y_true, float)\n"
            "    y_pred = np.asarray(y_pred, float)\n"
            "    return float(np.mean((y_pred - y_true) ** 2))\n"
            "```\n\n"
            "### Binary cross-entropy (BCE) — clasificacion binaria\n\n"
            "Cuando la red predice una **probabilidad** `p` (0 a 1, la "
            "salida de un sigmoid) y la verdad es 0 o 1:\n\n"
            "```\n"
            "BCE = -promedio( y*log(p) + (1-y)*log(1-p) )\n"
            "```\n\n"
            "Castiga con fuerza la confianza equivocada: si `y=1` y "
            "predices `p=0.01`, `-log(0.01)=4.6` (perdida enorme); si "
            "predices `p=0.99`, `-log(0.99)=0.01` (casi cero).\n\n"
            "**Gotcha del clip:** `log(0)` es `-inf`. Si la red predice "
            "exactamente 0 o 1, la perdida explota. Se evita recortando "
            "`p` a `[eps, 1-eps]` con `np.clip` antes del `log`:\n\n"
            "```python\n"
            "def bce(y_true, y_pred):\n"
            "    y_true = np.asarray(y_true, float)\n"
            "    p = np.clip(np.asarray(y_pred, float), 1e-12, 1 - 1e-12)\n"
            "    return float(-np.mean(y_true*np.log(p) + (1-y_true)*np.log(1-p)))\n"
            "```\n\n"
            "## El gradiente: en que direccion mejorar\n\n"
            "El **gradiente** de la perdida respecto a un peso te dice "
            "cuanto cambia la perdida si mueves ese peso un poquito. Es "
            "la **pendiente**. Para minimizar, das un paso en direccion "
            "**opuesta** al gradiente (descenso de gradiente, DL 4).\n\n"
            "Analiticamente el gradiente se calcula con backprop (DL 3), "
            "pero primero conviene la version conceptual: el **gradiente "
            "numerico** por diferencias finitas centradas.\n\n"
            "```\n"
            "df/dx ~= ( f(x+h) - f(x-h) ) / (2h)     con h pequeno\n"
            "```\n\n"
            "```python\n"
            "def gradiente_numerico(f, x, h=1e-5):\n"
            "    x = np.asarray(x, float)\n"
            "    return (f(x + h) - f(x - h)) / (2 * h)\n"
            "```\n\n"
            "Para `f(x)=x^2` en `x=3`, deberia dar ~6 (la derivada "
            "`2x`). Es **lento** (no sirve para entrenar redes reales, "
            "requiere 2 forward por parametro), pero es la mejor forma "
            "de **verificar** que tu backprop analitico esta bien: se "
            "llama *gradient checking*.\n\n"
            "## La diferencia central es mas precisa\n\n"
            "Podrias usar `(f(x+h) - f(x)) / h` (diferencia hacia "
            "adelante), pero la **centrada** `(f(x+h)-f(x-h))/(2h)` "
            "cancela mas error y da una aproximacion mucho mejor para el "
            "mismo `h`.\n\n"
            "## Errores comunes\n\n"
            "1. **MSE sin promediar** — sumar en vez de promediar hace "
            "la perdida dependiente del tamano del batch.\n"
            "2. **BCE sin clip** — un `p` de 0 o 1 mete un `-inf` y todo "
            "el entrenamiento se vuelve `nan`.\n"
            "3. **h demasiado chico en el gradiente numerico** — con "
            "`h=1e-12` el error de redondeo de floats domina; `1e-5` es "
            "un buen punto medio.\n"
            "4. **Confundir perdida con accuracy** — la perdida es "
            "continua y derivable (por eso entrena); la accuracy es un "
            "conteo, no sirve para el gradiente.\n\n"
            "## Resumen\n\n"
            "- La **perdida** mide el error; entrenar = minimizarla.\n"
            "- `MSE` para regresion, `BCE` para clasificacion binaria "
            "(con `clip` para evitar `log(0)`).\n"
            "- El **gradiente** es la pendiente de la perdida; se avanza "
            "en su direccion opuesta.\n"
            "- El **gradiente numerico** `(f(x+h)-f(x-h))/(2h)` aproxima "
            "la derivada; util para *verificar* backprop, no para "
            "entrenar.\n"
        ),
        difficulty="intermediate",
        category="dl-fundamentos",
        order=34,
        track="track-4",
        estimated_duration=50,
        prerequisites_titles=[
            "DL 1 · La neurona: forward pass y activaciones",
        ],
        exercises=[
            ExerciseTemplate(
                title="Error cuadratico medio (MSE)",
                description=(
                    "Implementa la perdida MSE para regresion, " "vectorizada."
                ),
                instructions=(
                    "Implementa `mse(y_true, y_pred)` que devuelve el "
                    "promedio de `(y_pred - y_true) ** 2` como `float`. "
                    "Convierte ambas entradas con `np.asarray(..., "
                    "float)`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def mse(y_true, y_pred):\n"
                    "    # TODO: y_true = np.asarray(y_true, float); y_pred = np.asarray(y_pred, float)\n"
                    "    # TODO: return float(np.mean((y_pred - y_true) ** 2))\n"
                    "    ...\n"
                ),
                hints=[
                    "np.mean promedia todos los elementos.",
                    "Elevar al cuadrado elimina el signo del error.",
                    "MSE de una prediccion perfecta es 0.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "mse: casos conocidos, simetria, float",
                        "code": (
                            "import numpy as np\n"
                            "assert mse([1, 2, 3], [1, 2, 3]) == 0\n"
                            "assert abs(mse([0, 0], [1, 1]) - 1.0) < 1e-12\n"
                            "assert abs(mse([3.0], [0.0]) - 9.0) < 1e-12\n"
                            "assert isinstance(mse([1.0], [2.0]), float)\n"
                            "a = [1.0, 2.0, 3.0]\n"
                            "b = [2.0, 0.0, 5.0]\n"
                            "assert abs(mse(a, b) - mse(b, a)) < 1e-12"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Binary cross-entropy (BCE)",
                description=(
                    "Implementa la perdida de clasificacion binaria con "
                    "clip para evitar log(0)."
                ),
                instructions=(
                    "Implementa `bce(y_true, y_pred)` = "
                    "`-promedio(y*log(p) + (1-y)*log(1-p))`. Recorta "
                    "`y_pred` a `[1e-12, 1 - 1e-12]` con `np.clip` antes "
                    "de los logaritmos para no obtener `-inf`. Devuelve "
                    "un `float`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def bce(y_true, y_pred):\n"
                    "    # TODO: y_true = np.asarray(y_true, float)\n"
                    "    # TODO: p = np.clip(np.asarray(y_pred, float), 1e-12, 1 - 1e-12)\n"
                    "    # TODO: return float(-np.mean(y_true*np.log(p) + (1-y_true)*np.log(1-p)))\n"
                    "    ...\n"
                ),
                hints=[
                    "El clip es lo que evita log(0) = -inf.",
                    "Predecir p cercano a la verdad da perdida cercana a 0.",
                    "Predecir con confianza lo contrario da perdida alta.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "bce: valores conocidos, clip finito, peor > mejor",
                        "code": (
                            "import numpy as np\n"
                            "assert abs(bce([1], [0.9]) - 0.105360516) < 1e-5, bce([1], [0.9])\n"
                            "assert abs(bce([0], [0.1]) - 0.105360516) < 1e-5\n"
                            "assert bce([1, 0], [0.999, 0.001]) < 0.01\n"
                            "assert bce([1], [0.01]) > bce([1], [0.99])\n"
                            "assert np.isfinite(bce([1], [1.0]))\n"
                            "assert np.isfinite(bce([0], [0.0]))"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Gradiente numerico",
                description=(
                    "Aproxima la derivada de una funcion por diferencias "
                    "finitas centradas."
                ),
                instructions=(
                    "Implementa `gradiente_numerico(f, x, h=1e-5)` que "
                    "devuelve `(f(x + h) - f(x - h)) / (2 * h)`. Funciona "
                    "para `x` escalar o array (vectorizado con numpy). "
                    "`f` es una funcion que recibe un numero/array y "
                    "devuelve lo mismo."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def gradiente_numerico(f, x, h=1e-5):\n"
                    "    # TODO: x = np.asarray(x, float)\n"
                    "    # TODO: return (f(x + h) - f(x - h)) / (2 * h)\n"
                    "    ...\n"
                ),
                hints=[
                    "La diferencia centrada es mas precisa que la de adelante.",
                    "Para f(x)=x^2, la derivada en x es 2x.",
                    "Como usa numpy, funciona elemento a elemento sobre un array.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "gradiente: x^2->2x, x^3->3x^2, vectorizado",
                        "code": (
                            "import numpy as np\n"
                            "g = gradiente_numerico(lambda x: x**2, 3.0)\n"
                            "assert abs(float(g) - 6.0) < 1e-3, g\n"
                            "gv = np.asarray(gradiente_numerico(lambda x: x**2, np.array([1.0, 2.0, 3.0])))\n"
                            "assert np.allclose(gv, [2, 4, 6], atol=1e-3), gv\n"
                            "g3 = gradiente_numerico(lambda x: x**3, 2.0)\n"
                            "assert abs(float(g3) - 12.0) < 1e-2, g3"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="DL 3 · Backpropagation: la regla de la cadena",
        description=(
            "Como fluye el gradiente hacia atras por la red: derivada "
            "local de la activacion, backward de la capa lineal, y "
            "gradient checking contra el gradiente numerico."
        ),
        content=(
            "# DL 3: backpropagation\n\n"
            "Ya sabes hacer el forward (DL 1) y medir el error (DL 2). "
            "**Backpropagation** es el algoritmo que calcula el "
            "gradiente de la perdida respecto a **cada** peso de forma "
            "eficiente, para poder ajustarlos. No es mas que la **regla "
            "de la cadena** del calculo, aplicada capa por capa de la "
            "salida hacia la entrada.\n\n"
            "## La regla de la cadena\n\n"
            "Si `L` depende de `a`, y `a` depende de `z`, y `z` depende "
            "de `W`, entonces:\n\n"
            "```\n"
            "dL/dW = dL/da * da/dz * dz/dW\n"
            "```\n\n"
            "Backprop calcula esto de derecha a izquierda: parte del "
            "**gradiente que llega de arriba** (`dL/da`, el *upstream "
            "gradient*), lo multiplica por la **derivada local** de cada "
            "operacion, y propaga el resultado hacia atras. Cada nodo "
            "solo necesita saber su derivada local.\n\n"
            "## Backward de una activacion\n\n"
            "Para el sigmoid hay un truco precioso: si `a = sigmoid(z)`, "
            "su derivada local se escribe en terminos de la **propia "
            "salida**:\n\n"
            "```\n"
            "da/dz = a * (1 - a)\n"
            "```\n\n"
            "Asi que el gradiente que sale hacia atras es el que entra "
            "multiplicado elemento a elemento por la derivada local:\n\n"
            "```python\n"
            "def grad_sigmoid(a, grad_out):   # a = salida del sigmoid\n"
            "    return grad_out * a * (1 - a)\n"
            "```\n\n"
            "(Para ReLU la derivada local es `1` donde `z > 0` y `0` "
            "donde `z <= 0`.)\n\n"
            "## Backward de una capa lineal\n\n"
            "El forward era `z = X @ W + b`. Dado el gradiente que llega "
            "`grad_z = dL/dz`, la regla de la cadena da las tres "
            "derivadas locales (esto se deduce, pero conviene "
            "memorizarlo):\n\n"
            "```\n"
            "dW = X.T @ grad_z        # como cambiar los pesos\n"
            "db = grad_z.sum(axis=0)  # el sesgo suma sobre el batch\n"
            "dX = grad_z @ W.T        # gradiente que sigue hacia atras\n"
            "```\n\n"
            "```python\n"
            "def backward_lineal(X, W, grad_z):\n"
            "    dW = X.T @ grad_z\n"
            "    db = grad_z.sum(axis=0)\n"
            "    dX = grad_z @ W.T\n"
            "    return dW, db, dX\n"
            "```\n\n"
            "Fijate en las **transpuestas**: hacen que las shapes "
            "cuadren. `dW` tiene la shape de `W`, `dX` la de `X`. Si "
            "algo no cuadra, casi siempre es una transpuesta mal "
            "puesta.\n\n"
            "## Gradient checking: no te fies, verifica\n\n"
            "El backprop analitico es facil de equivocar (un signo, una "
            "transpuesta). La forma estandar de verificarlo es "
            "compararlo contra el **gradiente numerico** de DL 2: "
            "perturbas cada peso un `h` y mides como cambia la perdida. "
            "Si el analitico y el numerico coinciden (hasta ~1e-4), tu "
            "backprop esta bien.\n\n"
            "```\n"
            "para cada peso W[i,j]:\n"
            "  num[i,j] = ( L(W con W[i,j]+h) - L(W con W[i,j]-h) ) / (2h)\n"
            "comparar num  vs  gradiente analitico   -> deben coincidir\n"
            "```\n\n"
            "Esta es la mejor red de seguridad al implementar backprop a "
            "mano. PyTorch lo hace por ti con autograd (lo veras "
            "despues), pero ahora entiendes que hay debajo.\n\n"
            "## Errores comunes\n\n"
            "1. **Transpuesta olvidada** — `dW = X @ grad_z` en vez de "
            "`X.T @ grad_z`: las shapes no cuadran o el gradiente es "
            "erroneo.\n"
            "2. **Usar z en vez de a en grad_sigmoid** — la formula "
            "`a*(1-a)` usa la **salida** del sigmoid, no la entrada.\n"
            "3. **No sumar el sesgo sobre el batch** — `db` es "
            "`grad_z.sum(axis=0)`; el bias se comparte entre muestras.\n"
            "4. **Saltarse el gradient checking** — implementar backprop "
            "sin verificarlo numericamente es pedir un bug silencioso.\n\n"
            "## Resumen\n\n"
            "- Backprop = regla de la cadena aplicada de la salida hacia "
            "la entrada.\n"
            "- Cada operacion aporta su **derivada local**; se multiplica "
            "por el gradiente *upstream*.\n"
            "- Capa lineal: `dW = X.T @ grad_z`, `db = grad_z.sum(0)`, "
            "`dX = grad_z @ W.T`.\n"
            "- Sigmoid: `da/dz = a*(1-a)`.\n"
            "- **Verifica** siempre con gradient checking contra el "
            "gradiente numerico.\n"
        ),
        difficulty="advanced",
        category="dl-fundamentos",
        order=35,
        track="track-4",
        estimated_duration=60,
        prerequisites_titles=[
            "DL 2 · Funciones de perdida y gradiente numerico",
        ],
        exercises=[
            ExerciseTemplate(
                title="Backward del sigmoid",
                description=(
                    "Propaga el gradiente a traves de un sigmoid usando "
                    "su derivada local a*(1-a)."
                ),
                instructions=(
                    "Implementa `grad_sigmoid(a, grad_out)` donde `a` es "
                    "la **salida** del sigmoid y `grad_out` es el "
                    "gradiente que llega de arriba (`dL/da`). Devuelve "
                    "`grad_out * a * (1 - a)` (elemento a elemento)."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def grad_sigmoid(a, grad_out):\n"
                    "    # a = salida del sigmoid; grad_out = dL/da\n"
                    "    # TODO: a = np.asarray(a, float); grad_out = np.asarray(grad_out, float)\n"
                    "    # TODO: return grad_out * a * (1 - a)\n"
                    "    ...\n"
                ),
                hints=[
                    "La derivada local del sigmoid es a*(1-a), con a la SALIDA.",
                    "En a=0.5 la derivada local vale 0.25 (el maximo).",
                    "Multiplica elemento a elemento por grad_out.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "grad_sigmoid: a(1-a) y coincide con derivada numerica",
                        "code": (
                            "import numpy as np\n"
                            "assert abs(float(grad_sigmoid(0.5, 1.0)) - 0.25) < 1e-12\n"
                            "assert abs(float(grad_sigmoid(0.8, 2.0)) - 0.32) < 1e-12\n"
                            "out = np.asarray(grad_sigmoid(np.array([0.5, 0.8]), np.array([1.0, 1.0])))\n"
                            "assert out.shape == (2,), out.shape\n"
                            "sig = lambda z: 1.0 / (1.0 + np.exp(-z))\n"
                            "z0 = 0.7\n"
                            "a = sig(z0)\n"
                            "h = 1e-5\n"
                            "analitico = float(grad_sigmoid(a, 1.0))\n"
                            "numerico = (sig(z0 + h) - sig(z0 - h)) / (2 * h)\n"
                            "assert abs(analitico - numerico) < 1e-4, (analitico, numerico)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Backward de la capa lineal",
                description=(
                    "Calcula los gradientes dW, db y dX de una capa " "z = X @ W + b."
                ),
                instructions=(
                    "Implementa `backward_lineal(X, W, grad_z)` que, "
                    "dado el gradiente `grad_z = dL/dz`, devuelve la "
                    "tupla `(dW, db, dX)` con `dW = X.T @ grad_z`, "
                    "`db = grad_z.sum(axis=0)` y `dX = grad_z @ W.T`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def backward_lineal(X, W, grad_z):\n"
                    "    # TODO: dW = X.T @ grad_z\n"
                    "    # TODO: db = grad_z.sum(axis=0)\n"
                    "    # TODO: dX = grad_z @ W.T\n"
                    "    # TODO: return dW, db, dX\n"
                    "    ...\n"
                ),
                hints=[
                    "dW tiene la misma shape que W; dX la misma que X.",
                    "Las transpuestas son las que hacen cuadrar las shapes.",
                    "db suma el gradiente sobre las muestras del batch (axis=0).",
                ],
                difficulty="advanced",
                points=25,
                hidden_tests=[
                    {
                        "name": "backward_lineal: shapes y valores (dW, db, dX)",
                        "code": (
                            "import numpy as np\n"
                            "X = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])\n"
                            "W = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])\n"
                            "grad_z = np.array([[1.0, 0.0], [0.0, 1.0]])\n"
                            "dW, db, dX = backward_lineal(X, W, grad_z)\n"
                            "dW = np.asarray(dW)\n"
                            "db = np.asarray(db)\n"
                            "dX = np.asarray(dX)\n"
                            "assert dW.shape == (3, 2), dW.shape\n"
                            "assert db.shape == (2,), db.shape\n"
                            "assert dX.shape == (2, 3), dX.shape\n"
                            "assert np.allclose(dW, X.T @ grad_z)\n"
                            "assert np.allclose(db, [1.0, 1.0])\n"
                            "assert np.allclose(dX, grad_z @ W.T)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Gradient checking de una capa lineal + MSE",
                description=(
                    "Calcula el gradiente analitico de la perdida MSE "
                    "respecto a W y verifica que coincide con el "
                    "numerico."
                ),
                instructions=(
                    "Para una capa `z = X @ W + b` con perdida "
                    "`L = mean((z - y_true) ** 2)`, implementa "
                    "`grad_W(X, W, b, y_true)` que devuelve `dL/dW`. "
                    "Pista: `dL/dz = 2 * (z - y_true) / z.size` y "
                    "`dL/dW = X.T @ dL/dz`. El test compara tu resultado "
                    "contra el gradiente numerico (gradient checking)."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def grad_W(X, W, b, y_true):\n"
                    "    # TODO: z = X @ W + b\n"
                    "    # TODO: dz = 2.0 * (z - y_true) / z.size\n"
                    "    # TODO: return X.T @ dz\n"
                    "    ...\n"
                ),
                hints=[
                    "El factor 2 y el /z.size vienen de derivar la media de cuadrados.",
                    "dL/dW = X.T @ dL/dz, igual que en backward_lineal.",
                    "Si coincide con el numerico hasta 1e-4, tu gradiente esta bien.",
                ],
                difficulty="advanced",
                points=25,
                hidden_tests=[
                    {
                        "name": "grad_W coincide con el gradiente numerico",
                        "code": (
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "X = rng.normal(size=(5, 3))\n"
                            "W = rng.normal(size=(3, 1))\n"
                            "b = np.array([0.5])\n"
                            "y = rng.normal(size=(5, 1))\n"
                            "g = np.asarray(grad_W(X, W, b, y))\n"
                            "assert g.shape == W.shape, g.shape\n"
                            "def loss(Wm):\n"
                            "    z = X @ Wm + b\n"
                            "    return float(np.mean((z - y) ** 2))\n"
                            "h = 1e-5\n"
                            "num = np.zeros_like(W)\n"
                            "for i in range(W.shape[0]):\n"
                            "    for j in range(W.shape[1]):\n"
                            "        Wp = W.copy(); Wp[i, j] += h\n"
                            "        Wm = W.copy(); Wm[i, j] -= h\n"
                            "        num[i, j] = (loss(Wp) - loss(Wm)) / (2 * h)\n"
                            "assert np.allclose(g, num, atol=1e-4), (g.ravel(), num.ravel())"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="DL 4 · Training loop: entrenar con descenso de gradiente",
        description=(
            "Junta forward, perdida, backward y actualizacion de pesos "
            "en un bucle que entrena de verdad: regresion y clasificacion "
            "logistica desde cero, viendo bajar la perdida."
        ),
        content=(
            "# DL 4: el bucle de entrenamiento\n\n"
            "Ya tienes todas las piezas: forward (DL 1), perdida (DL 2) "
            "y gradientes (DL 3). **Entrenar** es repetirlas en un bucle "
            "y, en cada vuelta, empujar los pesos un pasito en la "
            "direccion que reduce la perdida. Eso es el **descenso de "
            "gradiente**.\n\n"
            "## El paso de descenso\n\n"
            "El gradiente apunta hacia donde la perdida **crece**. Para "
            "minimizar, te mueves en direccion **contraria**, escalado "
            "por el **learning rate** `lr`:\n\n"
            "```\n"
            "W <- W - lr * dW\n"
            "```\n\n"
            "```python\n"
            "def paso_sgd(param, grad, lr):\n"
            "    return param - lr * grad\n"
            "```\n\n"
            "- `lr` muy chico -> entrena lentisimo.\n"
            "- `lr` muy grande -> la perdida oscila o **diverge** (se "
            "va a infinito).\n"
            "- El punto justo hace bajar la perdida de forma estable.\n\n"
            "## El bucle completo\n\n"
            "Un entrenamiento no es mas que esto, repetido N **epocas**:\n\n"
            "```\n"
            "inicializa W, b\n"
            "repite epocas veces:\n"
            "    z = forward(X, W, b)          # 1. forward\n"
            "    perdida = loss(z, y)          # 2. medir error\n"
            "    dW, db = backward(...)        # 3. gradientes\n"
            "    W = W - lr * dW               # 4. actualizar\n"
            "    b = b - lr * db\n"
            "```\n\n"
            "Para **regresion lineal** (`z = X @ W + b`, perdida MSE) el "
            "gradiente ya lo dedujiste en DL 3:\n\n"
            "```python\n"
            "z = X @ W + b\n"
            "dz = 2 * (z - y) / z.size\n"
            "W = W - lr * (X.T @ dz)\n"
            "b = b - lr * dz.sum(axis=0)\n"
            "```\n\n"
            "Si guardas la perdida de cada epoca, veras una curva que "
            "**baja** hasta estabilizarse. Esa curva es tu mejor amiga "
            "para diagnosticar el entrenamiento.\n\n"
            "## El mismo bucle sirve para clasificar\n\n"
            "Cambia la activacion y la perdida y ya tienes **regresion "
            "logistica**: `p = sigmoid(X @ W + b)`, perdida BCE. Y aqui "
            "pasa algo precioso: al combinar sigmoid + BCE, el gradiente "
            "se simplifica al **mismo** que en regresion lineal:\n\n"
            "```\n"
            "dz = (p - y) / N        # p = sigmoid(z), N = numero de muestras\n"
            "```\n\n"
            "Es decir: **el bucle es identico**, solo cambian la "
            "activacion del forward y la formula de la perdida que "
            "registras. Esa uniformidad es lo que hace que las redes "
            "escalen a arquitecturas enormes.\n\n"
            "## Errores comunes\n\n"
            "1. **Learning rate mal elegido** — si la perdida sube o se "
            "vuelve `nan`, bajalo (prueba /10). Si baja lentisimo, "
            "subelo.\n"
            "2. **No normalizar las features** — con features de escalas "
            "muy distintas, un `lr` unico no sirve para todas; el "
            "descenso zigzaguea (recuerda `StandardScaler` de Track 3).\n"
            "3. **Actualizar W usando el z ya actualizado** — calcula "
            "todos los gradientes con los pesos actuales, *despues* "
            "actualiza.\n"
            "4. **Olvidar sumar el bias sobre el batch** — `db` es "
            "`dz.sum(axis=0)`, no `dz`.\n\n"
            "## Resumen\n\n"
            "- Descenso de gradiente: `W <- W - lr * dW`, repetido por "
            "epocas.\n"
            "- El bucle es forward -> perdida -> backward -> "
            "actualizar.\n"
            "- La **curva de perdida** debe bajar; si sube, el `lr` es "
            "muy grande.\n"
            "- El mismo bucle entrena regresion (MSE) y clasificacion "
            "(sigmoid + BCE); en ambos `dz` termina siendo `(pred - y)` "
            "normalizado.\n"
        ),
        difficulty="advanced",
        category="dl-fundamentos",
        order=36,
        track="track-4",
        estimated_duration=60,
        prerequisites_titles=[
            "DL 3 · Backpropagation: la regla de la cadena",
        ],
        exercises=[
            ExerciseTemplate(
                title="Paso de descenso de gradiente",
                description=(
                    "Implementa la actualizacion de un parametro en "
                    "direccion opuesta al gradiente."
                ),
                instructions=(
                    "Implementa `paso_sgd(param, grad, lr)` que devuelve "
                    "`param - lr * grad` (funciona para escalares o "
                    "arrays). Convierte con `np.asarray(..., float)`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def paso_sgd(param, grad, lr):\n"
                    "    # TODO: return np.asarray(param, float) - lr * np.asarray(grad, float)\n"
                    "    ...\n"
                ),
                hints=[
                    "Se resta porque el gradiente apunta hacia donde la perdida crece.",
                    "lr escala el tamano del paso.",
                    "Funciona elemento a elemento sobre arrays.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "paso_sgd resta lr*grad",
                        "code": (
                            "import numpy as np\n"
                            "out = np.asarray(paso_sgd(np.array([1.0, 2.0]), np.array([0.5, -1.0]), 0.1))\n"
                            "assert np.allclose(out, [0.95, 2.1]), out\n"
                            "assert abs(float(paso_sgd(5.0, 2.0, 0.5)) - 4.0) < 1e-12"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Entrenar regresion lineal",
                description=(
                    "Escribe el bucle de entrenamiento completo para "
                    "regresion lineal con MSE."
                ),
                instructions=(
                    "Implementa `entrenar_regresion(X, y, lr=0.1, "
                    "epocas=500)` que inicializa `W = zeros((n_features, "
                    "1))` y `b = zeros(1)`, y en cada epoca: calcula "
                    "`z = X @ W + b`, guarda la perdida MSE en una lista, "
                    "computa `dz = 2*(z - y)/z.size`, y actualiza "
                    "`W -= lr*(X.T @ dz)` y `b -= lr*dz.sum(axis=0)`. "
                    "`y` puede venir como `(n,)` o `(n,1)` (usa "
                    "`.reshape(-1, 1)`). Devuelve `(W, b, historial)`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def entrenar_regresion(X, y, lr=0.1, epocas=500):\n"
                    "    X = np.asarray(X, float)\n"
                    "    y = np.asarray(y, float).reshape(-1, 1)\n"
                    "    W = np.zeros((X.shape[1], 1))\n"
                    "    b = np.zeros((1,))\n"
                    "    historial = []\n"
                    "    # TODO: bucle de epocas: forward, guardar MSE, dz, actualizar W y b\n"
                    "    return W, b, historial\n"
                ),
                hints=[
                    "Guarda la perdida ANTES de actualizar los pesos de esa epoca.",
                    "dz = 2*(z - y)/z.size; dW = X.T @ dz; db = dz.sum(axis=0).",
                    "En un problema convexo la perdida baja de forma monotona.",
                ],
                difficulty="advanced",
                points=25,
                hidden_tests=[
                    {
                        "name": "entrenar_regresion: perdida baja y converge a W_true",
                        "code": (
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "X = rng.normal(size=(20, 3))\n"
                            "W_true = np.array([[1.0], [-2.0], [0.5]])\n"
                            "y = X @ W_true + 0.3\n"
                            "W, b, hist = entrenar_regresion(X, y, lr=0.1, epocas=800)\n"
                            "assert len(hist) == 800, len(hist)\n"
                            "assert hist[-1] < hist[0], (hist[0], hist[-1])\n"
                            "assert all(hist[i + 1] <= hist[i] + 1e-9 for i in range(len(hist) - 1)), 'no monotono'\n"
                            "assert hist[-1] < 1e-4, hist[-1]\n"
                            "assert np.allclose(np.asarray(W), W_true, atol=0.05), np.asarray(W).ravel()"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Entrenar regresion logistica",
                description=(
                    "El mismo bucle, pero con sigmoid + BCE para " "clasificar."
                ),
                instructions=(
                    "Implementa `entrenar_logistica(X, y, lr=0.5, "
                    "epocas=500)`: en cada epoca calcula "
                    "`p = sigmoid(X @ W + b)`, guarda la perdida BCE (con "
                    "clip a `[1e-12, 1-1e-12]`), y actualiza con "
                    "`dz = (p - y) / N` (N = numero de muestras), "
                    "`W -= lr*(X.T @ dz)`, `b -= lr*dz.sum(axis=0)`. "
                    "Inicializa `W`, `b` en cero. Devuelve "
                    "`(W, b, historial)`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def entrenar_logistica(X, y, lr=0.5, epocas=500):\n"
                    "    X = np.asarray(X, float)\n"
                    "    y = np.asarray(y, float).reshape(-1, 1)\n"
                    "    W = np.zeros((X.shape[1], 1))\n"
                    "    b = np.zeros((1,))\n"
                    "    historial = []\n"
                    "    # TODO: bucle: p = sigmoid(X@W+b), guardar BCE, dz=(p-y)/N, actualizar\n"
                    "    return W, b, historial\n"
                ),
                hints=[
                    "sigmoid(z) = 1/(1+exp(-z)).",
                    "El gradiente sigmoid+BCE se simplifica a dz = (p - y)/N.",
                    "Con datos separables, la accuracy final debe superar 0.9.",
                ],
                difficulty="advanced",
                points=25,
                hidden_tests=[
                    {
                        "name": "entrenar_logistica: perdida baja y clasifica > 0.9",
                        "code": (
                            "import numpy as np\n"
                            "rng = np.random.default_rng(1)\n"
                            "X = rng.normal(size=(60, 2))\n"
                            "W_true = np.array([[2.0], [-1.0]])\n"
                            "y = ((X @ W_true + 0.5) > 0).astype(float).reshape(-1, 1)\n"
                            "W, b, hist = entrenar_logistica(X, y, lr=0.5, epocas=800)\n"
                            "assert hist[-1] < hist[0], (hist[0], hist[-1])\n"
                            "p = 1.0 / (1.0 + np.exp(-(X @ np.asarray(W) + np.asarray(b))))\n"
                            "acc = float(np.mean((p > 0.5).astype(float) == y))\n"
                            "assert acc > 0.9, acc"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="DL 5 · Tu primer MLP: dos capas resuelven XOR",
        description=(
            "El clima de los fundamentos: una red de 2 capas con "
            "forward y backward encadenados, entrenada para resolver "
            "XOR, el problema no lineal que una sola neurona no puede."
        ),
        content=(
            "# DL 5: el perceptron multicapa (MLP)\n\n"
            "Una sola capa lineal (con o sin sigmoid) solo puede trazar "
            "una **frontera recta**. Hay problemas donde eso no alcanza. "
            "El clasico es **XOR**:\n\n"
            "```\n"
            "  (0,0) -> 0     (0,1) -> 1\n"
            "  (1,0) -> 1     (1,1) -> 0\n"
            "```\n\n"
            "No existe ninguna recta que separe los 1 de los 0. Este "
            "problema **hundio a los perceptrones** en los anos 70... "
            "hasta que se apilaron capas con no-linealidad. Un **MLP "
            "(perceptron multicapa)** de 2 capas lo resuelve sin "
            "problema.\n\n"
            "## Arquitectura de 2 capas\n\n"
            "```\n"
            "X --[W1,b1]--> z1 --relu--> h --[W2,b2]--> z2 --sigmoid--> p\n"
            "   capa oculta                capa de salida\n"
            "```\n\n"
            "```python\n"
            "z1 = X @ W1 + b1     # capa oculta\n"
            "h  = relu(z1)        # no-linealidad (¡clave!)\n"
            "z2 = h @ W2 + b2     # capa de salida\n"
            "p  = sigmoid(z2)     # probabilidad\n"
            "```\n\n"
            "La capa oculta transforma el espacio para que el problema "
            "**si** sea linealmente separable en la salida. Sin el "
            "`relu` de por medio, las dos capas colapsarian en una sola "
            "(recuerda DL 1): la no-linealidad es lo que da el poder.\n\n"
            "## Backward encadenado\n\n"
            "El gradiente fluye hacia atras por **las dos** capas, "
            "aplicando la regla de la cadena de DL 3 dos veces. Con "
            "salida sigmoid + BCE, `dz2 = (p - y)/N`, y de ahi:\n\n"
            "```python\n"
            "dz2 = (p - y) / N\n"
            "dW2 = h.T @ dz2\n"
            "db2 = dz2.sum(axis=0)\n"
            "dh  = dz2 @ W2.T          # gradiente que baja a la capa oculta\n"
            "dz1 = dh * (z1 > 0)       # derivada local del relu\n"
            "dW1 = X.T @ dz1\n"
            "db1 = dz1.sum(axis=0)\n"
            "```\n\n"
            "Nota como el gradiente de la capa 2 (`dh`) se convierte en "
            "el gradiente *upstream* de la capa 1. Eso es "
            "backpropagation encadenado: la salida de un backward "
            "alimenta al siguiente. Con 50 capas seria el mismo patron, "
            "50 veces.\n\n"
            "## Entrenar\n\n"
            "El bucle es identico al de DL 4 (forward -> perdida -> "
            "backward -> actualizar), solo que ahora actualizas "
            "**cuatro** grupos de parametros: `W1, b1, W2, b2`. Con "
            "suficientes neuronas ocultas (p.ej. 8) y epocas, la red "
            "aprende XOR y clasifica los 4 puntos perfecto.\n\n"
            "## Errores comunes\n\n"
            "1. **Olvidar la derivada del relu** — `dz1 = dh * (z1 > 0)`. "
            "Sin ese `(z1 > 0)`, el gradiente de la capa oculta esta "
            "mal.\n"
            "2. **Encadenar mal** — el `dh = dz2 @ W2.T` es lo que "
            "conecta las dos capas; es facil equivocar la transpuesta.\n"
            "3. **Red demasiado pequena** — con 1-2 neuronas ocultas "
            "quiza no aprenda XOR; dale unas 8.\n"
            "4. **Inicializar los pesos en cero** — si `W1` es todo "
            "ceros, todas las neuronas ocultas hacen lo mismo y nunca se "
            "diferencian (*symmetry breaking*). Se inicializan al azar.\n\n"
            "## Resumen\n\n"
            "- Un **MLP** apila capas con no-linealidad entre medias; "
            "resuelve problemas no lineales como XOR.\n"
            "- Forward: `relu(X@W1+b1)` -> `sigmoid(h@W2+b2)`.\n"
            "- Backward: encadena la regla de la cadena; el gradiente de "
            "una capa es el *upstream* de la anterior.\n"
            "- Con esto ya construiste una red neuronal **completa** "
            "desde cero. Lo que sigue (PyTorch) automatiza justo este "
            "backward que ya entiendes.\n"
        ),
        difficulty="advanced",
        category="dl-fundamentos",
        order=37,
        track="track-4",
        estimated_duration=70,
        prerequisites_titles=[
            "DL 4 · Training loop: entrenar con descenso de gradiente",
        ],
        exercises=[
            ExerciseTemplate(
                title="Forward de un MLP de 2 capas",
                description=(
                    "Encadena capa oculta (relu) y capa de salida " "(sigmoid)."
                ),
                instructions=(
                    "Implementa `forward_mlp(X, W1, b1, W2, b2)` que "
                    "calcula `z1 = X @ W1 + b1`, `h = relu(z1)`, "
                    "`z2 = h @ W2 + b2` y devuelve `p = sigmoid(z2)` "
                    "(las probabilidades de salida)."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def forward_mlp(X, W1, b1, W2, b2):\n"
                    "    # TODO: z1 = X @ W1 + b1; h = np.maximum(0.0, z1)\n"
                    "    # TODO: z2 = h @ W2 + b2\n"
                    "    # TODO: return 1.0 / (1.0 + np.exp(-z2))\n"
                    "    ...\n"
                ),
                hints=[
                    "El relu de la capa oculta es np.maximum(0.0, z1).",
                    "La salida pasa por sigmoid, no por relu.",
                    "Shapes: X (n,d_in), W1 (d_in,d_oculta), W2 (d_oculta,1).",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "forward_mlp: shape y valor conocido sigmoid(2)",
                        "code": (
                            "import numpy as np\n"
                            "X = np.array([[1.0, 1.0]])\n"
                            "W1 = np.array([[1.0, 0.0], [0.0, 1.0]])\n"
                            "b1 = np.array([0.0, 0.0])\n"
                            "W2 = np.array([[1.0], [1.0]])\n"
                            "b2 = np.array([0.0])\n"
                            "p = np.asarray(forward_mlp(X, W1, b1, W2, b2))\n"
                            "assert p.shape == (1, 1), p.shape\n"
                            "assert 0 < float(p[0, 0]) < 1\n"
                            "assert abs(float(p[0, 0]) - 0.880797) < 1e-4, p\n"
                            "Xb = np.zeros((5, 2))\n"
                            "assert np.asarray(forward_mlp(Xb, W1, b1, W2, b2)).shape == (5, 1)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Backward encadenado del MLP",
                description=(
                    "Propaga el gradiente por las dos capas y verifica "
                    "con gradient checking."
                ),
                instructions=(
                    "Implementa `backward_mlp(X, W1, b1, W2, b2, y)` que "
                    "hace el forward, y con perdida BCE calcula los "
                    "gradientes de las dos capas: "
                    "`dz2 = (p - y)/N`, `dW2 = h.T @ dz2`, "
                    "`db2 = dz2.sum(0)`, `dh = dz2 @ W2.T`, "
                    "`dz1 = dh * (z1 > 0)`, `dW1 = X.T @ dz1`, "
                    "`db1 = dz1.sum(0)`. Devuelve `(dW1, db1, dW2, db2)`. "
                    "`N` es el numero de muestras."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def backward_mlp(X, W1, b1, W2, b2, y):\n"
                    "    X = np.asarray(X, float)\n"
                    "    y = np.asarray(y, float).reshape(-1, 1)\n"
                    "    N = X.shape[0]\n"
                    "    # forward guardando z1, h, p\n"
                    "    # TODO: z1 = X @ W1 + b1; h = np.maximum(0.0, z1)\n"
                    "    # TODO: p = 1/(1+exp(-(h @ W2 + b2)))\n"
                    "    # backward encadenado\n"
                    "    # TODO: dz2 = (p - y)/N; dW2 = h.T @ dz2; db2 = dz2.sum(0)\n"
                    "    # TODO: dh = dz2 @ W2.T; dz1 = dh * (z1 > 0)\n"
                    "    # TODO: dW1 = X.T @ dz1; db1 = dz1.sum(0)\n"
                    "    # TODO: return dW1, db1, dW2, db2\n"
                    "    ...\n"
                ),
                hints=[
                    "dh = dz2 @ W2.T conecta la salida con la capa oculta.",
                    "La derivada del relu es (z1 > 0): 1 donde z1 positivo, 0 si no.",
                    "El gradiente numerico de DL 2 sirve para verificar esto.",
                ],
                difficulty="advanced",
                points=30,
                hidden_tests=[
                    {
                        "name": "backward_mlp: coincide con gradiente numerico (dW1)",
                        "code": (
                            "import numpy as np\n"
                            "rng = np.random.default_rng(0)\n"
                            "X = rng.normal(size=(6, 3))\n"
                            "y = (rng.normal(size=(6, 1)) > 0).astype(float)\n"
                            "W1 = rng.normal(size=(3, 4)) * 0.5\n"
                            "b1 = rng.normal(size=(4,)) * 0.5\n"
                            "W2 = rng.normal(size=(4, 1)) * 0.5\n"
                            "b2 = np.array([0.1])\n"
                            "dW1, db1, dW2, db2 = backward_mlp(X, W1, b1, W2, b2, y)\n"
                            "dW1 = np.asarray(dW1)\n"
                            "dW2 = np.asarray(dW2)\n"
                            "assert dW1.shape == W1.shape and dW2.shape == W2.shape\n"
                            "def loss(W1_, b1_, W2_, b2_):\n"
                            "    z1 = X @ W1_ + b1_\n"
                            "    h = np.maximum(0.0, z1)\n"
                            "    p = 1.0 / (1.0 + np.exp(-(h @ W2_ + b2_)))\n"
                            "    pc = np.clip(p, 1e-12, 1 - 1e-12)\n"
                            "    return float(-np.mean(y*np.log(pc) + (1-y)*np.log(1-pc)))\n"
                            "h = 1e-5\n"
                            "num = np.zeros_like(W1)\n"
                            "for i in range(W1.shape[0]):\n"
                            "    for j in range(W1.shape[1]):\n"
                            "        Wp = W1.copy(); Wp[i, j] += h\n"
                            "        Wm = W1.copy(); Wm[i, j] -= h\n"
                            "        num[i, j] = (loss(Wp, b1, W2, b2) - loss(Wm, b1, W2, b2)) / (2 * h)\n"
                            "assert np.allclose(dW1, num, atol=1e-4), (dW1.ravel()[:3], num.ravel()[:3])"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Entrenar el MLP para resolver XOR",
                description=(
                    "Bucle de entrenamiento de 2 capas que aprende XOR " "al 100%."
                ),
                instructions=(
                    "Implementa `entrenar_mlp(X, y, W1, b1, W2, b2, "
                    "lr=0.5, epocas=2000)` que en cada epoca hace el "
                    "forward (relu + sigmoid), guarda la perdida BCE, "
                    "computa los gradientes encadenados (como en "
                    "`backward_mlp`) y actualiza los **cuatro** grupos de "
                    "pesos con descenso de gradiente. Recibe los pesos "
                    "iniciales por argumento (no los inicialices tu). "
                    "Devuelve `(W1, b1, W2, b2, historial)`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def entrenar_mlp(X, y, W1, b1, W2, b2, lr=0.5, epocas=2000):\n"
                    "    X = np.asarray(X, float)\n"
                    "    y = np.asarray(y, float).reshape(-1, 1)\n"
                    "    W1 = np.array(W1, float); b1 = np.array(b1, float)\n"
                    "    W2 = np.array(W2, float); b2 = np.array(b2, float)\n"
                    "    N = X.shape[0]\n"
                    "    historial = []\n"
                    "    # TODO: bucle de epocas: forward, guardar BCE, backward encadenado, actualizar\n"
                    "    return W1, b1, W2, b2, historial\n"
                ),
                hints=[
                    "Es el bucle de DL 4 pero actualizando 4 grupos de pesos.",
                    "El backward es el de backward_mlp (dz2 -> dh -> dz1).",
                    "Con 8 neuronas ocultas y varios miles de epocas, XOR llega al 100%.",
                ],
                difficulty="advanced",
                points=30,
                hidden_tests=[
                    {
                        "name": "entrenar_mlp resuelve XOR al 100%",
                        "code": (
                            "import numpy as np\n"
                            "X = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])\n"
                            "y = np.array([[0.0], [1.0], [1.0], [0.0]])\n"
                            "rng = np.random.default_rng(3)\n"
                            "W1 = rng.normal(size=(2, 8)); b1 = np.zeros(8)\n"
                            "W2 = rng.normal(size=(8, 1)); b2 = np.zeros(1)\n"
                            "W1, b1, W2, b2, hist = entrenar_mlp(X, y, W1, b1, W2, b2, lr=0.5, epocas=4000)\n"
                            "assert hist[-1] < hist[0], (hist[0], hist[-1])\n"
                            "z1 = X @ np.asarray(W1) + np.asarray(b1)\n"
                            "h = np.maximum(0.0, z1)\n"
                            "p = 1.0 / (1.0 + np.exp(-(h @ np.asarray(W2) + np.asarray(b2))))\n"
                            "acc = float(np.mean((p > 0.5).astype(float) == y))\n"
                            "assert acc == 1.0, (acc, p.ravel())"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="AI 1 · Embeddings y busqueda semantica desde cero",
        description=(
            "El primer ladrillo de AI Engineering: representar texto como "
            "vectores, medir similitud con coseno y recuperar los mas "
            "parecidos. La 'R' (retrieval) de RAG, en numpy puro."
        ),
        content=(
            "# AI 1: embeddings y busqueda semantica\n\n"
            "Bienvenido al **Track 5 (AI Engineering)**. Aqui dejamos de "
            "entrenar modelos y empezamos a **construir sistemas** sobre "
            "modelos que ya existen (LLMs, embeddings). El primer bloque "
            "es el motor de **RAG** (Retrieval-Augmented Generation): "
            "antes de que un LLM responda, hay que **recuperar** el "
            "contexto relevante. Eso es **busqueda semantica**, y su "
            "mecanica se construye con numpy.\n\n"
            "## De texto a vectores: embeddings\n\n"
            "Un **embedding** es un vector de numeros que representa el "
            "*significado* de un texto. Textos parecidos -> vectores "
            "cercanos. En la practica los produce un modelo de embeddings "
            "(OpenAI, sentence-transformers, etc.); aqui nos centramos en "
            "lo que haces **con** esos vectores, que es lo que define un "
            "sistema RAG.\n\n"
            "```\n"
            '"gato"   -> [0.9, 0.1, ...]\n'
            '"felino" -> [0.88, 0.12, ...]   (cerca de gato)\n'
            '"avion"  -> [0.1, 0.95, ...]    (lejos de gato)\n'
            "```\n\n"
            "## Similitud coseno\n\n"
            "Para medir 'que tan parecidos' son dos vectores se usa la "
            "**similitud coseno**: el coseno del angulo entre ellos. "
            "Ignora la magnitud y se fija solo en la **direccion**, que "
            "es lo que codifica el significado.\n\n"
            "```\n"
            "cos(a, b) = (a . b) / (||a|| * ||b||)\n"
            "  1   -> misma direccion (maxima similitud)\n"
            "  0   -> perpendiculares (sin relacion)\n"
            " -1   -> opuestos\n"
            "```\n\n"
            "```python\n"
            "import numpy as np\n"
            "def cosine_sim(a, b):\n"
            "    a = np.asarray(a, float); b = np.asarray(b, float)\n"
            "    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))\n"
            "```\n\n"
            "Fijate que **la escala no importa**: `[1,2,3]` y `[2,4,6]` "
            "apuntan a lo mismo, similitud 1. Por eso el coseno es el "
            "estandar para comparar embeddings (mejor que la distancia "
            "euclidea, sensible a la magnitud).\n\n"
            "## Recuperar los top-k\n\n"
            "Con una **query** y una coleccion de documentos "
            "vectorizados, calculas la similitud de la query con cada "
            "doc y te quedas con los `k` mas altos. Ese es el corazon de "
            "un buscador semantico (y de un retriever de RAG):\n\n"
            "```python\n"
            "def top_k(query, docs, k):\n"
            "    query = np.asarray(query, float); docs = np.asarray(docs, float)\n"
            "    sims = docs @ query / (np.linalg.norm(docs, axis=1) * np.linalg.norm(query))\n"
            "    return list(np.argsort(sims)[::-1][:k])\n"
            "```\n\n"
            "`np.argsort` ordena ascendente; con `[::-1]` lo inviertes a "
            "descendente y tomas los primeros `k`. Devolver los "
            "**indices** te deja mapear de vuelta a los textos "
            "originales.\n\n"
            "## Esto ya es un mini vector store\n\n"
            "Una matriz de embeddings (una fila por documento) + esta "
            "busqueda top-k es, conceptualmente, lo que hacen Pinecone, "
            "FAISS o pgvector — solo que ellos lo hacen sobre millones de "
            "vectores con indices aproximados (ANN) para ir rapido. La "
            "**mecanica** es la que acabas de escribir.\n\n"
            "## Como encaja en RAG\n\n"
            "```\n"
            "1. Indexar:  documentos -> embeddings -> matriz\n"
            "2. Query:    pregunta   -> embedding\n"
            "3. Retrieve: top_k(query, matriz) -> fragmentos relevantes\n"
            "4. Generate: LLM(pregunta + fragmentos) -> respuesta fundamentada\n"
            "```\n\n"
            "Esta leccion cubre los pasos 1-3 (la parte determinista y "
            "testeable). El paso 4 (llamar al LLM) llega en las "
            "siguientes lecciones del track.\n\n"
            "## Errores comunes\n\n"
            "1. **Usar distancia euclidea en vez de coseno** — sensible a "
            "la longitud del vector; el coseno compara direccion, que es "
            "lo que importa en embeddings.\n"
            "2. **No normalizar** — si implementas el producto punto sin "
            "dividir por las normas, un vector 'largo' gana siempre "
            "aunque no sea el mas parecido.\n"
            "3. **Ordenar ascendente y olvidar invertir** — `argsort` da "
            "menor-a-mayor; los mas similares estan al final.\n"
            "4. **Confundir el indice con el texto** — `top_k` devuelve "
            "posiciones; hay que mapearlas a los documentos.\n\n"
            "## Resumen\n\n"
            "- Un **embedding** convierte texto en un vector de "
            "significado.\n"
            "- La **similitud coseno** `(a.b)/(||a|| ||b||)` mide "
            "cercania por direccion, ignorando la escala.\n"
            "- **Busqueda semantica** = similitud de la query con cada "
            "doc + tomar los top-k.\n"
            "- Esto es el **retriever** de RAG; la generacion con LLM "
            "viene despues.\n"
        ),
        difficulty="intermediate",
        category="ai-fundamentos",
        order=38,
        track="track-5",
        estimated_duration=50,
        prerequisites_titles=[],
        exercises=[
            ExerciseTemplate(
                title="Similitud coseno",
                description=(
                    "Mide que tan parecidos son dos vectores por su " "direccion."
                ),
                instructions=(
                    "Implementa `cosine_sim(a, b)` = "
                    "`(a . b) / (||a|| * ||b||)` usando numpy "
                    "(`a @ b` para el producto punto y `np.linalg.norm` "
                    "para la magnitud). Devuelve un `float`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def cosine_sim(a, b):\n"
                    "    # TODO: a = np.asarray(a, float); b = np.asarray(b, float)\n"
                    "    # TODO: return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))\n"
                    "    ...\n"
                ),
                hints=[
                    "np.linalg.norm(v) da la magnitud (longitud) del vector.",
                    "Vectores paralelos dan 1; perpendiculares, 0.",
                    "La escala no importa: [1,2] y [2,4] dan similitud 1.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "cosine_sim: paralelos=1, ortogonales=0, opuestos=-1",
                        "code": (
                            "import numpy as np\n"
                            "assert abs(cosine_sim([1, 0], [1, 0]) - 1.0) < 1e-12\n"
                            "assert abs(cosine_sim([1, 0], [0, 1]) - 0.0) < 1e-12\n"
                            "assert abs(cosine_sim([1, 0], [-1, 0]) - (-1.0)) < 1e-12\n"
                            "assert abs(cosine_sim([1, 2, 3], [2, 4, 6]) - 1.0) < 1e-9\n"
                            "assert abs(cosine_sim([1, 1], [1, 0]) - 0.70710678) < 1e-6\n"
                            "assert isinstance(cosine_sim([1, 0], [1, 1]), float)"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Recuperar los top-k",
                description=(
                    "Devuelve los indices de los documentos mas similares "
                    "a una query."
                ),
                instructions=(
                    "Implementa `top_k(query, docs, k)` donde `query` es "
                    "un vector `(d,)` y `docs` una matriz `(n_docs, d)`. "
                    "Calcula la similitud coseno de la query con cada "
                    "fila de `docs` y devuelve la lista de los `k` indices "
                    "mas similares, ordenados de mayor a menor. Pista: "
                    "`np.argsort(sims)[::-1][:k]`."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def top_k(query, docs, k):\n"
                    "    query = np.asarray(query, float)\n"
                    "    docs = np.asarray(docs, float)\n"
                    "    # TODO: sims = docs @ query / (np.linalg.norm(docs, axis=1) * np.linalg.norm(query))\n"
                    "    # TODO: return list(np.argsort(sims)[::-1][:k])\n"
                    "    ...\n"
                ),
                hints=[
                    "np.linalg.norm(docs, axis=1) da la norma de cada fila.",
                    "argsort ordena ascendente; [::-1] lo invierte a descendente.",
                    "El resultado son indices (posiciones), no los vectores.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "top_k: indices mas similares, orden desc, invariante a escala",
                        "code": (
                            "import numpy as np\n"
                            "q = [1.0, 0.0]\n"
                            "docs = [[1.0, 0.0], [0.0, 1.0], [0.9, 0.1], [-1.0, 0.0]]\n"
                            "assert list(top_k(q, docs, 2)) == [0, 2], top_k(q, docs, 2)\n"
                            "assert list(top_k(q, docs, 1)) == [0]\n"
                            "docs2 = [[10.0, 0.0], [0.0, 5.0], [0.9, 0.1]]\n"
                            "assert list(top_k(q, docs2, 1)) == [0]"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Busqueda semantica end-to-end",
                description=(
                    "Recupera los textos mas relevantes para una query "
                    "(el retriever de RAG)."
                ),
                instructions=(
                    "Implementa `busqueda_semantica(query, docs, textos, "
                    "k)` que recibe el vector `query`, la matriz `docs` "
                    "de embeddings, la lista `textos` (un string por "
                    "documento, alineado con `docs`), y devuelve la lista "
                    "de los `k` textos mas similares a la query, de mayor "
                    "a menor similitud."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def busqueda_semantica(query, docs, textos, k):\n"
                    "    query = np.asarray(query, float)\n"
                    "    docs = np.asarray(docs, float)\n"
                    "    # TODO: sims = docs @ query / (np.linalg.norm(docs, axis=1) * np.linalg.norm(query))\n"
                    "    # TODO: idx = np.argsort(sims)[::-1][:k]\n"
                    "    # TODO: return [textos[i] for i in idx]\n"
                    "    ...\n"
                ),
                hints=[
                    "Reutiliza la logica de top_k y mapea los indices a textos.",
                    "textos[i] recupera el documento en la posicion i.",
                    "Este es exactamente el retriever de un pipeline RAG.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "busqueda_semantica: devuelve los textos top-k",
                        "code": (
                            "import numpy as np\n"
                            "q = [1.0, 0.0]\n"
                            "docs = [[1.0, 0.0], [0.0, 1.0], [0.9, 0.1], [-1.0, 0.0]]\n"
                            "textos = ['gato', 'avion', 'felino', 'antonimo']\n"
                            "assert busqueda_semantica(q, docs, textos, 2) == ['gato', 'felino']\n"
                            "assert busqueda_semantica(q, docs, textos, 1) == ['gato']"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="AI 2 · Chunking e indexacion de documentos",
        description=(
            "Como preparar un corpus para RAG: partir documentos en "
            "fragmentos (chunks), construir el indice de embeddings y "
            "recuperar el contexto relevante de una pregunta."
        ),
        content=(
            "# AI 2: chunking e indexacion\n\n"
            "En AI 1 recuperaste vectores ya dados. Pero antes de "
            "buscar, hay que **preparar el corpus**: partir los "
            "documentos largos en fragmentos manejables y construir un "
            "**indice** de embeddings. Este es el paso de *indexado* de "
            "RAG, y decisiones aparentemente pequenas aqui determinan si "
            "el sistema recupera bien o mal.\n\n"
            "## Por que partir en chunks\n\n"
            "No puedes (ni quieres) embeder un documento de 50 paginas "
            "como un solo vector: perderias todo el detalle, y no cabe "
            "en la ventana de contexto del LLM. En su lugar lo partes en "
            "**chunks** (fragmentos de unas pocas frases/parrafos), "
            "embedes cada uno, y recuperas solo los chunks relevantes a "
            "la pregunta.\n\n"
            "```\n"
            "documento largo --chunking--> [chunk1, chunk2, ... chunkN]\n"
            "cada chunk --embed--> un vector --> matriz indice (N, dim)\n"
            "```\n\n"
            "## Chunking con solapamiento\n\n"
            "Partir en seco puede cortar una idea justo a la mitad. Por "
            "eso los chunks suelen **solaparse**: cada uno comparte unas "
            "palabras con el anterior, para no perder contexto en los "
            "bordes.\n\n"
            "```python\n"
            "def chunk_texto(texto, tam, solapamiento=0):\n"
            "    palabras = texto.split()\n"
            "    step = tam - solapamiento          # cuanto avanzas cada vez\n"
            "    chunks = []\n"
            "    for i in range(0, len(palabras), step):\n"
            "        chunks.append(' '.join(palabras[i:i + tam]))\n"
            "        if i + tam >= len(palabras):\n"
            "            break                       # ya cubriste el final\n"
            "    return chunks\n"
            "```\n\n"
            "Con `tam=3, solapamiento=1` sobre `a b c d e f g`:\n\n"
            "```\n"
            '  "a b c"  ->  "c d e"  ->  "e f g"\n'
            "   step = 2 (avanzas 2, mantienes 1 de solape)\n"
            "```\n\n"
            "El `tam` y el `solapamiento` son **hiperparametros de "
            "RAG**: chunks muy grandes diluyen la senal; muy chicos "
            "pierden contexto. Solape tipico: 10-20% del tamano.\n\n"
            "## Construir el indice\n\n"
            "El **indice** es simplemente la matriz con el embedding de "
            "cada chunk. En produccion `embed_fn` es una llamada a un "
            "modelo de embeddings; aqui lo recibes como funcion para que "
            "todo sea testeable:\n\n"
            "```python\n"
            "def construir_indice(chunks, embed_fn):\n"
            "    return np.array([embed_fn(c) for c in chunks], float)\n"
            "```\n\n"
            "## Recuperar el contexto\n\n"
            "Juntando todo: embedes la pregunta, la comparas contra el "
            "indice (coseno de AI 1) y devuelves los `k` chunks mas "
            "relevantes. Eso es el **contexto** que despues le pasaras al "
            "LLM.\n\n"
            "```python\n"
            "def recuperar_contexto(pregunta, chunks, embed_fn, k):\n"
            "    indice = np.array([embed_fn(c) for c in chunks], float)\n"
            "    q = np.asarray(embed_fn(pregunta), float)\n"
            "    sims = indice @ q / (np.linalg.norm(indice, axis=1) * np.linalg.norm(q) + 1e-12)\n"
            "    idx = np.argsort(sims)[::-1][:k]\n"
            "    return [chunks[i] for i in idx]\n"
            "```\n\n"
            "El `+ 1e-12` evita dividir por cero si algun chunk quedara "
            "con embedding nulo. Ya tienes el **retriever completo**: "
            "chunk -> index -> retrieve. Solo falta la generacion.\n\n"
            "## Como encaja en RAG\n\n"
            "```\n"
            "1. Indexar:  documento --chunk--> chunks --embed--> indice   <- AI 2\n"
            "2. Retrieve: pregunta --embed--> top-k chunks del indice     <- AI 1 + AI 2\n"
            "3. Generate: LLM(pregunta + chunks recuperados) -> respuesta <- AI 3+\n"
            "```\n\n"
            "## Errores comunes\n\n"
            "1. **Chunks demasiado grandes** — recuperas texto irrelevante "
            "junto al relevante y confundes al LLM.\n"
            "2. **Sin solapamiento** — cortas ideas a la mitad y el chunk "
            "pierde sentido.\n"
            "3. **Solapamiento >= tam** — el `step` seria <= 0 y el bucle "
            "no avanza; valida que `solapamiento < tam`.\n"
            "4. **Reconstruir el indice en cada query** — en produccion "
            "el indice se calcula una vez y se guarda; solo la pregunta "
            "se embede en tiempo real.\n\n"
            "## Resumen\n\n"
            "- **Chunking** parte documentos en fragmentos; el "
            "solapamiento evita cortar ideas.\n"
            "- El **indice** es la matriz de embeddings de los chunks.\n"
            "- **Recuperar contexto** = embeder la pregunta + top-k del "
            "indice.\n"
            "- Con AI 1 + AI 2 tienes el retriever completo de RAG; la "
            "generacion con LLM llega en AI 3.\n"
        ),
        difficulty="intermediate",
        category="ai-fundamentos",
        order=39,
        track="track-5",
        estimated_duration=50,
        prerequisites_titles=[
            "AI 1 · Embeddings y busqueda semantica desde cero",
        ],
        exercises=[
            ExerciseTemplate(
                title="Partir texto en chunks",
                description=(
                    "Divide un texto en fragmentos de N palabras con "
                    "solapamiento opcional."
                ),
                instructions=(
                    "Implementa `chunk_texto(texto, tam, solapamiento=0)` "
                    "que parte `texto` (por palabras, con `.split()`) en "
                    "chunks de `tam` palabras, avanzando "
                    "`step = tam - solapamiento` palabras cada vez. Cada "
                    "chunk se devuelve como string (`' '.join(...)`). "
                    "Para en cuanto un chunk llega al final. Lanza "
                    "`ValueError` si `solapamiento >= tam` (step <= 0)."
                ),
                starter_code=(
                    "def chunk_texto(texto, tam, solapamiento=0):\n"
                    "    palabras = texto.split()\n"
                    "    step = tam - solapamiento\n"
                    "    # TODO: if step <= 0: raise ValueError(...)\n"
                    "    # TODO: recorre range(0, len(palabras), step),\n"
                    "    #   agrega ' '.join(palabras[i:i+tam]) y corta al llegar al final\n"
                    "    ...\n"
                ),
                hints=[
                    "step = tam - solapamiento es cuanto avanzas cada iteracion.",
                    "Corta el bucle cuando i + tam >= len(palabras).",
                    "Un solapamiento >= tam dejaria step <= 0: lanza ValueError.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "chunk_texto: tamano, solapamiento y validacion",
                        "code": (
                            "assert chunk_texto('a b c d e f', 2) == ['a b', 'c d', 'e f']\n"
                            "assert chunk_texto('a b c d e f g', 3, 1) == ['a b c', 'c d e', 'e f g']\n"
                            "assert chunk_texto('hola', 3) == ['hola']\n"
                            "assert chunk_texto('a b c d e', 2) == ['a b', 'c d', 'e']\n"
                            "try:\n"
                            "    chunk_texto('a b c', 2, 2)\n"
                            "    raise AssertionError('debio lanzar ValueError')\n"
                            "except ValueError:\n"
                            "    pass"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Construir el indice de embeddings",
                description=("Embede cada chunk para formar la matriz del indice."),
                instructions=(
                    "Implementa `construir_indice(chunks, embed_fn)` que "
                    "aplica `embed_fn` a cada chunk y devuelve un "
                    "`np.ndarray` de shape `(n_chunks, dim)` "
                    "(`np.array([embed_fn(c) for c in chunks], float)`)."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def construir_indice(chunks, embed_fn):\n"
                    "    # TODO: return np.array([embed_fn(c) for c in chunks], float)\n"
                    "    ...\n"
                ),
                hints=[
                    "Una fila por chunk, una columna por dimension del embedding.",
                    "embed_fn se aplica a cada chunk.",
                    "En produccion embed_fn seria una llamada al modelo de embeddings.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "construir_indice: matriz (n_chunks, dim)",
                        "code": (
                            "import numpy as np\n"
                            "embed = lambda t: [t.count('gato'), t.count('avion')]\n"
                            "chunks = ['el gato duerme', 'un avion vuela', 'gato gato']\n"
                            "M = np.asarray(construir_indice(chunks, embed))\n"
                            "assert M.shape == (3, 2), M.shape\n"
                            "assert np.allclose(M[0], [1, 0])\n"
                            "assert np.allclose(M[2], [2, 0])"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Recuperar el contexto de una pregunta",
                description=(
                    "El retriever completo: indexa, embede la pregunta y "
                    "devuelve los chunks relevantes."
                ),
                instructions=(
                    "Implementa `recuperar_contexto(pregunta, chunks, "
                    "embed_fn, k)` que construye el indice de los chunks, "
                    "embede la `pregunta`, calcula la similitud coseno "
                    "(usa `+ 1e-12` en el denominador para evitar "
                    "division por cero) y devuelve la lista de los `k` "
                    "chunks (strings) mas relevantes, de mayor a menor."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def recuperar_contexto(pregunta, chunks, embed_fn, k):\n"
                    "    indice = np.array([embed_fn(c) for c in chunks], float)\n"
                    "    q = np.asarray(embed_fn(pregunta), float)\n"
                    "    # TODO: sims = indice @ q / (np.linalg.norm(indice, axis=1) * np.linalg.norm(q) + 1e-12)\n"
                    "    # TODO: idx = np.argsort(sims)[::-1][:k]\n"
                    "    # TODO: return [chunks[i] for i in idx]\n"
                    "    ...\n"
                ),
                hints=[
                    "Es AI 1 (top-k) pero embediendo la pregunta y devolviendo chunks.",
                    "El +1e-12 evita NaN si algun chunk tiene embedding nulo.",
                    "Devuelve los textos de los chunks, no sus indices.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "recuperar_contexto: trae los chunks relevantes",
                        "code": (
                            "embed = lambda t: [t.count('gato'), t.count('avion'), t.count('python')]\n"
                            "chunks = ['el gato maulla', 'el avion despega', 'python es un lenguaje', 'gato y python']\n"
                            "res = recuperar_contexto('cuentame del gato', chunks, embed, 2)\n"
                            "assert 'el gato maulla' in res, res\n"
                            "assert 'el avion despega' not in res, res\n"
                            "assert len(res) == 2"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="AI 3 · Llamar a un LLM y armar un prompt RAG",
        description=(
            "La generacion de RAG: llamar a un LLM real desde el editor, "
            "construir un prompt con contexto recuperado, presupuestar la "
            "ventana y parsear salida estructurada (JSON)."
        ),
        content=(
            "# AI 3: llamar a un LLM y armar el prompt de RAG\n\n"
            "En AI 1 y AI 2 construiste el **retriever**. Ahora llega la "
            "**G** de RAG: **generar** la respuesta con un LLM, "
            "pasandole el contexto recuperado. Aqui aprendes a llamar al "
            "modelo y, sobre todo, a **construir bien el prompt** — que "
            "es donde se gana o se pierde la calidad de un sistema de "
            "AI Engineering.\n\n"
            "## Llamar al LLM desde el editor\n\n"
            "PyCode expone un helper que llama a un LLM real **a traves "
            "del backend** (sin exponer API keys). Es asincrono:\n\n"
            "```python\n"
            "import pycode\n"
            "respuesta = await pycode.llm_complete(\n"
            "    'Explica que es un embedding en una frase.',\n"
            "    system='Eres un profesor conciso.',\n"
            "    max_tokens=100,\n"
            ")\n"
            "print(respuesta)\n"
            "```\n\n"
            "El backend aplica **rate limit** y un **tope de tokens** "
            "para controlar el costo. En este entorno, si no hay modelo "
            "configurado, recibiras una respuesta placeholder — la "
            "**logica** que rodea la llamada es lo que importa y lo que "
            "vas a practicar.\n\n"
            "> Nota: la respuesta de un LLM es **no determinista** "
            "(cambia entre llamadas). Por eso los ejercicios evaluados "
            "no comprueban el texto del modelo, sino el codigo que "
            "**prepara** la llamada y **procesa** su salida — que es "
            "justo el trabajo de un AI Engineer.\n\n"
            "## Construir el prompt de RAG\n\n"
            "El truco de RAG esta en el prompt: le das al modelo el "
            "contexto recuperado y le pides que responda **solo** con "
            "eso (para reducir alucinaciones).\n\n"
            "```python\n"
            "def construir_prompt_rag(pregunta, contextos):\n"
            "    bloque = '\\n'.join('- ' + c for c in contextos)\n"
            "    return (\n"
            "        'Usa unicamente el siguiente contexto para responder. '\n"
            "        'Si la respuesta no esta en el contexto, di que no lo sabes.\\n\\n'\n"
            "        'Contexto:\\n' + bloque + '\\n\\nPregunta: ' + pregunta\n"
            "    )\n"
            "```\n\n"
            "El pipeline RAG completo queda:\n\n"
            "```python\n"
            "contextos = recuperar_contexto(pregunta, chunks, embed, k=3)  # AI 2\n"
            "prompt = construir_prompt_rag(pregunta, contextos)            # AI 3\n"
            "respuesta = await pycode.llm_complete(prompt)                 # generacion\n"
            "```\n\n"
            "## Presupuestar la ventana de contexto\n\n"
            "Un LLM tiene una **ventana de contexto** finita (y cada "
            "token cuesta). No puedes meter 500 chunks. Hay que "
            "**presupuestar**: incluir chunks (en orden de relevancia) "
            "hasta agotar un limite.\n\n"
            "```python\n"
            "def truncar_contexto(contextos, max_chars):\n"
            "    incluidos, total = [], 0\n"
            "    for c in contextos:\n"
            "        if total + len(c) > max_chars:\n"
            "            break\n"
            "        incluidos.append(c)\n"
            "        total += len(c)\n"
            "    return incluidos\n"
            "```\n\n"
            "(En produccion se cuenta en **tokens**, no caracteres, con "
            "un tokenizador; la idea es la misma.)\n\n"
            "## Parsear salida estructurada\n\n"
            "Muchas veces le pides al LLM que responda en **JSON** (para "
            "usar la salida en codigo). Pero los modelos a menudo la "
            "envuelven en cercas markdown ```` ```json ... ``` ```` o "
            "agregan texto. Hay que limpiarla antes de `json.loads`:\n\n"
            "```python\n"
            "import json\n"
            "def parsear_json_llm(texto):\n"
            "    t = texto.strip()\n"
            "    if '```' in t:\n"
            "        t = t.split('```')[1]\n"
            "        if t.startswith('json'):\n"
            "            t = t[4:]\n"
            "        t = t.strip()\n"
            "    try:\n"
            "        return json.loads(t)\n"
            "    except json.JSONDecodeError:\n"
            "        ini, fin = t.find('{'), t.rfind('}')\n"
            "        return json.loads(t[ini:fin + 1])\n"
            "```\n\n"
            "## Errores comunes\n\n"
            "1. **No acotar el contexto** — metes texto de mas, gastas "
            "tokens y confundes al modelo.\n"
            "2. **Confiar en que el JSON viene limpio** — casi nunca; "
            "limpia cercas y texto antes de parsear.\n"
            "3. **No instruir contra la alucinacion** — sin el 'usa solo "
            "el contexto', el modelo inventa.\n"
            "4. **Testear el texto exacto del LLM** — es no "
            "determinista; testea la logica que lo rodea.\n\n"
            "## Resumen\n\n"
            "- `pycode.llm_complete(prompt)` llama a un LLM real via el "
            "backend (await, rate-limited).\n"
            "- RAG = recuperar contexto (AI 1-2) + **construir el "
            "prompt** con ese contexto + generar.\n"
            "- **Presupuesta** el contexto para no exceder la ventana.\n"
            "- **Limpia y parsea** la salida estructurada (JSON con "
            "cercas).\n"
            "- Un AI Engineer disena el codigo **alrededor** del LLM; el "
            "modelo es una pieza mas.\n"
        ),
        difficulty="intermediate",
        category="ai-fundamentos",
        order=40,
        track="track-5",
        estimated_duration=55,
        prerequisites_titles=[
            "AI 2 · Chunking e indexacion de documentos",
        ],
        exercises=[
            ExerciseTemplate(
                title="Construir el prompt de RAG",
                description=(
                    "Ensambla el contexto recuperado y la pregunta en un "
                    "prompt anti-alucinacion."
                ),
                instructions=(
                    "Implementa `construir_prompt_rag(pregunta, "
                    "contextos)` que devuelve un prompt que: (1) instruye "
                    "a usar SOLO el contexto y decir 'no lo sabes' si no "
                    "esta; (2) lista cada contexto como vineta "
                    "(`'- ' + c`); (3) termina con `'Pregunta: ' + "
                    "pregunta`."
                ),
                starter_code=(
                    "def construir_prompt_rag(pregunta, contextos):\n"
                    "    # TODO: bloque = '\\n'.join('- ' + c for c in contextos)\n"
                    "    # TODO: return instruccion + 'Contexto:\\n' + bloque + '\\n\\nPregunta: ' + pregunta\n"
                    "    ...\n"
                ),
                hints=[
                    "La instruccion 'usa solo el contexto' reduce alucinaciones.",
                    "Cada contexto va como vineta: '- ' + c.",
                    "El prompt debe contener la pregunta al final.",
                ],
                difficulty="easy",
                points=15,
                hidden_tests=[
                    {
                        "name": "prompt contiene instruccion, contextos y pregunta",
                        "code": (
                            "p = construir_prompt_rag('cual es la capital?', "
                            "['Paris es la capital de Francia', 'Francia esta en Europa'])\n"
                            "assert 'cual es la capital?' in p\n"
                            "assert 'Paris es la capital de Francia' in p\n"
                            "assert 'Francia esta en Europa' in p\n"
                            "assert 'no lo sabes' in p\n"
                            "assert '- Paris es la capital de Francia' in p"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Presupuestar el contexto",
                description=(
                    "Incluye chunks hasta agotar un presupuesto de " "caracteres."
                ),
                instructions=(
                    "Implementa `truncar_contexto(contextos, max_chars)` "
                    "que recorre los chunks en orden y los va incluyendo "
                    "mientras la suma de sus longitudes no supere "
                    "`max_chars`. En cuanto el siguiente chunk no quepa, "
                    "para. Devuelve la lista de chunks incluidos."
                ),
                starter_code=(
                    "def truncar_contexto(contextos, max_chars):\n"
                    "    incluidos = []\n"
                    "    total = 0\n"
                    "    # TODO: for c in contextos: si total+len(c) > max_chars: break;\n"
                    "    #   si no, incluir c y sumar len(c)\n"
                    "    return incluidos\n"
                ),
                hints=[
                    "Acumula la longitud total y corta cuando el siguiente no cabe.",
                    "Si el primer chunk ya excede el presupuesto, devuelves [].",
                    "En produccion se mide en tokens; aqui, en caracteres.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "incluye chunks hasta agotar el presupuesto",
                        "code": (
                            "assert truncar_contexto(['abc', 'defgh', 'ij'], 8) == ['abc', 'defgh']\n"
                            "assert truncar_contexto(['abc'], 2) == []\n"
                            "assert truncar_contexto([], 100) == []\n"
                            "assert truncar_contexto(['ab', 'cd', 'ef'], 100) == ['ab', 'cd', 'ef']"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Parsear la salida JSON del LLM",
                description=(
                    "Limpia cercas markdown y texto para extraer el JSON "
                    "de una respuesta."
                ),
                instructions=(
                    "Implementa `parsear_json_llm(texto)` que devuelve el "
                    "dict parseado. Debe manejar: JSON plano, JSON dentro "
                    "de cercas ```` ```json ... ``` ```` o ```` ``` ... "
                    "``` ````, y JSON con texto alrededor (extrae desde "
                    "el primer `{` hasta el ultimo `}`). Usa `json.loads`."
                ),
                starter_code=(
                    "import json\n"
                    "\n"
                    "\n"
                    "def parsear_json_llm(texto):\n"
                    "    t = texto.strip()\n"
                    "    # TODO: si hay '```', quedate con lo de dentro y quita el prefijo 'json'\n"
                    "    # TODO: intenta json.loads(t); si falla, extrae de '{' a '}' y parsea\n"
                    "    ...\n"
                ),
                hints=[
                    "t.split('```')[1] te da el bloque entre la primera pareja de cercas.",
                    "Si el bloque empieza con 'json', quitalo (t[4:]).",
                    "Como fallback, t[t.find('{'):t.rfind('}')+1] aisla el objeto.",
                ],
                difficulty="medium",
                points=20,
                hidden_tests=[
                    {
                        "name": "parsea JSON plano, con cercas y con texto alrededor",
                        "code": (
                            "assert parsear_json_llm('{\"nombre\": \"ana\", \"edad\": 30}') == {'nombre': 'ana', 'edad': 30}\n"
                            "assert parsear_json_llm('```json\\n{\"ok\": true}\\n```') == {'ok': True}\n"
                            "assert parsear_json_llm('Claro:\\n```\\n{\"n\": [1, 2, 3]}\\n```') == {'n': [1, 2, 3]}\n"
                            "assert parsear_json_llm('bla bla {\"a\": 1} fin') == {'a': 1}"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="AI 4 · RAG de punta a punta",
        description=(
            "El pipeline completo sobre los documentos de una tienda: tokenizar, "
            "indexar una vez, recuperar con umbral de relevancia, citar fuentes "
            "y generar con un LLM inyectable (falso en los tests, real en el editor)."
        ),
        content=(
            "# AI 4: RAG de punta a punta\n"
            "\n"
            "En AI 1, 2 y 3 construiste las piezas por separado: similitud coseno, chunks, indice, prompt y la llamada al LLM. Un sistema real no es la suma de las piezas: es lo que pasa **entre** ellas. Esta leccion las une en un pipeline que responde preguntas sobre los documentos de **Nebula**, una tienda online ficticia, y le anade las tres defensas que separan una demo de algo que se puede poner delante de un usuario.\n"
            "\n"
            "## Por que un RAG de punta a punta\n"
            "\n"
            "Nebula quiere un asistente que conteste sobre sus politicas de envio, pagos y devoluciones. Con las piezas sueltas aparecen tres problemas en cuanto llegan preguntas de verdad:\n"
            "\n"
            "1. **Preguntas que los documentos no responden.** El retriever siempre devuelve *algo*, aunque no tenga que ver. El LLM recibe ruido y **inventa** una respuesta con tono seguro.\n"
            '2. **Respuestas que no se pueden comprobar.** Si el asistente dice "tienes 30 dias", nadie sabe de que documento lo saco, ni si lo saco de alguno.\n'
            "3. **Indexar en cada pregunta.** Recalcular los embeddings de todo el corpus por cada consulta no escala.\n"
            "\n"
            'Al terminar tendras una funcion `responder` que recupera solo lo relevante, dice "no lo se" sin gastar una llamada al LLM cuando no hay nada, y devuelve la respuesta con las **fuentes** que la respaldan.\n'
            "\n"
            "## Tokenizar: el mismo tratamiento para documentos y preguntas\n"
            "\n"
            "Antes de comparar textos hay que partirlos en palabras de la misma forma. Si el documento dice `Envio` y la pregunta `envío`, para el ordenador son palabras distintas.\n"
            "\n"
            "```python\n"
            "import re                                                       # expresiones regulares\n"
            "import unicodedata                                              # para separar las tildes\n"
            "\n"
            "def tokenizar(texto):\n"
            "    minusculas = texto.lower()                                  # 'Envío' -> 'envío'\n"
            "    separado = unicodedata.normalize('NFD', minusculas)         # la tilde queda como caracter aparte\n"
            "    sin_tildes = separado.encode('ascii', 'ignore').decode()    # y se descarta: 'envio'\n"
            "    return re.findall(r'\\w+', sin_tildes)                       # solo palabras, sin signos\n"
            "\n"
            "print(tokenizar('¿Cuánto cuesta el envío?'))   # ['cuanto', 'cuesta', 'el', 'envio']\n"
            "```\n"
            "\n"
            "`re.findall(r'\\w+', texto)` devuelve todos los trozos formados por letras, numeros o `_`: los signos de puntuacion quedan fuera sin tener que listarlos.\n"
            "\n"
            "## Un embedding que puedes construir: bolsa de palabras\n"
            "\n"
            "En AI 1 los embeddings te venian dados. Para que el pipeline funcione de verdad en el editor, construimos uno sencillo: un **vocabulario** (todas las palabras del corpus, ordenadas) y, para cada texto, un vector que cuenta cuantas veces aparece cada palabra.\n"
            "\n"
            "```python\n"
            "import re                                                      # para partir en palabras\n"
            "import numpy as np                                             # para los vectores\n"
            "\n"
            "def tokenizar(texto):                                          # version corta: no quita tildes\n"
            "    return re.findall(r'\\w+', texto.lower())                   # minusculas y solo palabras\n"
            "\n"
            "def vocabulario(textos):                                       # todas las palabras del corpus\n"
            "    palabras = set()                                           # cada palabra, una sola vez\n"
            "    for texto in textos:                                       # recorre cada texto del corpus\n"
            "        palabras.update(tokenizar(texto))                      # anade todas las del texto\n"
            "    return sorted(palabras)                                    # orden fijo: cada palabra, su columna\n"
            "\n"
            "def embed_bow(texto, vocab):                                   # texto -> vector de conteos\n"
            "    columna = {palabra: i for i, palabra in enumerate(vocab)}  # palabra -> posicion en el vector\n"
            "    vector = np.zeros(len(vocab))                              # un hueco por palabra\n"
            "    for palabra in tokenizar(texto):                           # recorre las palabras del texto\n"
            "        if palabra in columna:                                 # las que no estan en el vocabulario no cuentan\n"
            "            vector[columna[palabra]] += 1                      # suma 1 en su columna\n"
            "    return vector                                              # un numero por palabra del vocabulario\n"
            "\n"
            "vocab = vocabulario(['el envio es gratis', 'el pago es seguro'])\n"
            "print(vocab)                                     # ['el', 'envio', 'es', 'gratis', 'pago', 'seguro']\n"
            "print(embed_bow('envio gratis, envio rapido', vocab))   # [0. 2. 0. 1. 0. 0.]  'rapido' no esta\n"
            "```\n"
            "\n"
            "La bolsa de palabras tiene un limite claro: para ella `devolver` y `devoluciones` no se parecen en nada, porque son palabras distintas. Un **modelo de embeddings** captura que significan casi lo mismo. Lo importante es que la interfaz es identica (texto entra, vector sale): cambiar `embed_bow` por un modelo real no toca el resto del pipeline.\n"
            "\n"
            "## Indexar una sola vez\n"
            "\n"
            "El indice se construye **una vez**, cuando cambian los documentos, y se guarda. Por cada pregunta solo se embede la pregunta.\n"
            "\n"
            "```python\n"
            "import re                                                            # para partir en palabras\n"
            "import numpy as np                                                   # para la matriz\n"
            "\n"
            "def tokenizar(texto):                                                # version corta: no quita tildes\n"
            "    return re.findall(r'\\w+', texto.lower())                         # minusculas y solo palabras\n"
            "\n"
            "def construir_indice(textos):                                        # se llama UNA vez, no por pregunta\n"
            "    vocab = sorted({p for t in textos for p in tokenizar(t)})        # vocabulario del corpus\n"
            "    columna = {p: i for i, p in enumerate(vocab)}                    # palabra -> columna\n"
            "    matriz = np.zeros((len(textos), len(vocab)))                     # una fila por texto\n"
            "    for fila, texto in enumerate(textos):                            # cada texto rellena su fila\n"
            "        for palabra in tokenizar(texto):                             # y cada palabra, su columna\n"
            "            matriz[fila, columna[palabra]] += 1                      # cuenta la palabra en su columna\n"
            "    return {'textos': textos, 'vocab': vocab, 'matriz': matriz}      # todo lo que la busqueda necesita\n"
            "\n"
            "indice = construir_indice(['envio gratis desde 50 euros', 'pago con tarjeta'])\n"
            "print(indice['matriz'].shape)                    # (2, 8): 2 textos, 8 palabras distintas\n"
            "```\n"
            "\n"
            "Con documentos largos, primero los partes en chunks (AI 2) y cada chunk es un `texto` del indice. En produccion la matriz se guarda en una base vectorial y no se recalcula al arrancar.\n"
            "\n"
            "## No mandes contexto que no sirve: umbral de relevancia\n"
            "\n"
            "`top_k` devuelve siempre `k` resultados, aunque el mejor tenga similitud 0.05. La defensa es un **umbral**: lo que no llega, no entra. Y si no llega nada, no se llama al LLM.\n"
            "\n"
            "```python\n"
            "import numpy as np                       # para el algebra de vectores\n"
            "\n"
            "matriz = np.array([[1.0, 1.0, 0.0],      # 'envio gratis'\n"
            "                   [0.0, 0.0, 1.0]])     # 'pago tarjeta'\n"
            "consulta = np.array([1.0, 0.0, 0.0])     # la pregunta solo menciona 'envio'\n"
            "\n"
            "normas = np.linalg.norm(matriz, axis=1) * np.linalg.norm(consulta)   # denominador del coseno\n"
            "sims = np.divide(matriz @ consulta, normas, out=np.zeros(len(matriz)), where=normas != 0)\n"
            "print(sims.round(2))                     # [0.71 0.  ]\n"
            "\n"
            "umbral = 0.3\n"
            "orden = np.argsort(sims)[::-1]           # de mas a menos parecido\n"
            "relevantes = [(int(i), float(sims[i])) for i in orden if sims[i] >= umbral]\n"
            "print(relevantes)                        # [(0, 0.7071...)]  el de pagos queda fuera\n"
            "```\n"
            "\n"
            "`np.divide(..., where=normas != 0)` evita dividir por cero cuando la pregunta no comparte ninguna palabra con el vocabulario: esa similitud queda en 0 en vez de `nan`. El valor del umbral se ajusta mirando preguntas reales: muy alto y dejas fuera contexto util, muy bajo y vuelve el ruido.\n"
            "\n"
            "## Fuentes numeradas y citas\n"
            "\n"
            "Para poder comprobar una respuesta, cada fragmento entra al prompt con un **numero**, y se le pide al modelo que cite ese numero junto a cada dato. Despues se leen las citas de la respuesta.\n"
            "\n"
            "```python\n"
            "import re                                                       # para leer las citas\n"
            "\n"
            "def prompt_con_fuentes(pregunta, fragmentos):                   # fragmentos en orden de relevancia\n"
            "    fuentes = '\\n'.join(f'[{i}] {texto}' for i, texto in enumerate(fragmentos, start=1))  # [1] ..., [2] ...\n"
            "    return (\n"
            "        'Responde usando solo las fuentes numeradas. '          # nada de conocimiento propio\n"
            "        'Cita cada dato con su numero entre corchetes, por ejemplo [1]. '   # formato de cita\n"
            "        'Si las fuentes no bastan, di que no lo sabes.\\n\\n'     # permiso para no inventar\n"
            "        f'Fuentes:\\n{fuentes}\\n\\nPregunta: {pregunta}'           # contexto y pregunta al final\n"
            "    )\n"
            "\n"
            "def extraer_citas(respuesta, n_fuentes):                        # respuesta del LLM -> numeros citados\n"
            "    citas = []                                                  # lista: conserva el orden de aparicion\n"
            "    for grupo in re.findall(r'\\[([\\d,\\s]+)\\]', respuesta):      # '[1]', '[1, 3]' -> '1', '1, 3'\n"
            "        for numero in re.findall(r'\\d+', grupo):                # '1, 3' -> '1' y '3'\n"
            "            n = int(numero)                                     # de texto a entero\n"
            "            if 1 <= n <= n_fuentes and n not in citas:          # fuera de rango = inventada\n"
            "                citas.append(n)                                 # la primera vez que aparece\n"
            "    return citas                                                # p. ej. [2, 1]\n"
            "\n"
            "print(extraer_citas('Envio gratis desde 50 euros [2]. Pago seguro [1, 2] [7].', 2))   # [2, 1]\n"
            "```\n"
            "\n"
            "La cita `[7]` no existe (solo hubo 2 fuentes): un modelo que cita fuentes inexistentes esta alucinando, y el codigo tiene que descartarla, no confiar en ella.\n"
            "\n"
            "## El pipeline completo\n"
            "\n"
            "Todo junto. `llm_fn` se **inyecta**: en los tests es una funcion falsa y predecible; en el editor, `pycode.llm_complete`. Como la llamada al LLM es asincrona, `responder` tambien lo es (`async def`) y se usa con `await`.\n"
            "\n"
            "```python\n"
            "import re                                                                    # tokenizar y citas\n"
            "import numpy as np                                                           # vectores y coseno\n"
            "\n"
            "NO_SE = 'No lo se: no encontre informacion sobre eso en los documentos.'     # respuesta sin contexto\n"
            "\n"
            "def tokenizar(texto):                                                        # version corta: no quita tildes\n"
            "    return re.findall(r'\\w+', texto.lower())                                 # minusculas y solo palabras\n"
            "\n"
            "def embed_bow(texto, vocab):                                                 # texto -> vector de conteos\n"
            "    columna = {p: i for i, p in enumerate(vocab)}                            # palabra -> columna\n"
            "    vector = np.zeros(len(vocab))                                            # un hueco por palabra\n"
            "    for p in tokenizar(texto):                                               # recorre las palabras\n"
            "        if p in columna:                                                     # ignora las desconocidas\n"
            "            vector[columna[p]] += 1                                          # y cuenta las demas\n"
            "    return vector                                                            # listo para el coseno\n"
            "\n"
            "async def responder(pregunta, indice, llm_fn, k=3, umbral=0.2):\n"
            "    consulta = embed_bow(pregunta, indice['vocab'])                          # 1. embede la pregunta\n"
            "    normas = np.linalg.norm(indice['matriz'], axis=1) * np.linalg.norm(consulta)   # denominador del coseno\n"
            "    sims = np.divide(indice['matriz'] @ consulta, normas, out=np.zeros(len(normas)), where=normas != 0)   # sin nan\n"
            "    orden = [i for i in np.argsort(sims)[::-1] if sims[i] >= umbral][:k]     # 2. top-k que pasan el umbral\n"
            "    if not orden:\n"
            "        return {'respuesta': NO_SE, 'fuentes': []}                           # 3. sin contexto: ni se llama al LLM\n"
            "    fragmentos = [indice['textos'][i] for i in orden]                        # textos en orden de relevancia\n"
            "    lista = '\\n'.join(f'[{n}] {t}' for n, t in enumerate(fragmentos, start=1))   # [1] ..., [2] ...\n"
            "    prompt = f'Responde citando las fuentes [n].\\n\\nFuentes:\\n{lista}\\n\\nPregunta: {pregunta}'   # prompt RAG\n"
            "    texto = await llm_fn(prompt)                                             # 4. genera\n"
            "    citas = []                                                               # 5. lee y valida las citas\n"
            "    for n in map(int, re.findall(r'\\d+', ' '.join(re.findall(r'\\[([\\d,\\s]+)\\]', texto)))):   # todos los numeros citados\n"
            "        if 1 <= n <= len(fragmentos) and n not in citas:                     # solo los que existen\n"
            "            citas.append(n)                                                  # sin repetir\n"
            "    return {'respuesta': texto, 'fuentes': [fragmentos[n - 1] for n in citas]}  # respuesta + sus fuentes\n"
            "\n"
            "async def llm_falso(prompt):                     # para probar sin gastar llamadas\n"
            "    return 'El envio es gratis desde 50 euros [1].'\n"
            "\n"
            "textos = ['el envio es gratis desde 50 euros', 'el pago se hace con tarjeta']     # el corpus\n"
            "vocab = sorted({p for t in textos for p in tokenizar(t)})                         # su vocabulario\n"
            "indice = {'textos': textos, 'vocab': vocab, 'matriz': np.array([embed_bow(t, vocab) for t in textos])}   # se indexa una vez\n"
            "\n"
            "print(await responder('cuanto cuesta el envio', indice, llm_falso))\n"
            "# {'respuesta': 'El envio es gratis desde 50 euros [1].', 'fuentes': ['el envio es gratis desde 50 euros']}\n"
            "print(await responder('tienen tienda fisica', indice, llm_falso))\n"
            "# {'respuesta': 'No lo se: no encontre informacion sobre eso en los documentos.', 'fuentes': []}\n"
            "```\n"
            "\n"
            "Para usar el LLM real, cambia `llm_falso` por `pycode.llm_complete` (con `import pycode` arriba). La respuesta cambiara en cada ejecucion, pero el pipeline es el mismo: por eso los ejercicios comprueban el codigo **alrededor** del modelo, con un LLM falso.\n"
            "\n"
            "## Errores comunes\n"
            "\n"
            '- **No usar umbral.** El retriever siempre trae algo y el LLM contesta con seguridad a partir de ruido. Filtra por similitud minima y, si no queda nada, responde "no lo se" sin llamar al modelo: es mas barato y mas honesto.\n'
            "- **Tokenizar distinto el corpus y la pregunta.** Si el indice guarda `envio` y la pregunta llega como `Envío`, la similitud es 0 aunque hablen de lo mismo. Usa exactamente la misma funcion `tokenizar` en los dos lados.\n"
            "- **Confiar en las citas del modelo.** Un LLM puede citar `[7]` habiendo recibido 2 fuentes. Valida cada numero contra el rango real antes de mostrarla como fuente.\n"
            "- **Dividir por la norma sin comprobar que no es 0.** Una pregunta sin palabras del vocabulario da un vector de ceros y un `nan` que se propaga por todo el ranking. Usa `np.divide(..., where=normas != 0)`.\n"
            "- **Reconstruir el indice en cada pregunta.** Recalcular todos los embeddings por consulta multiplica el coste por el tamano del corpus. Indexa una vez y guarda el resultado.\n"
            "\n"
            "## Resumen\n"
            "\n"
            "- **Tokenizar**: minusculas, sin tildes y solo palabras, igual para documentos y preguntas.\n"
            "- **Bolsa de palabras**: vocabulario ordenado y un contador por palabra; un modelo de embeddings la sustituye sin tocar el resto.\n"
            "- **Indice**: se construye una vez con textos, vocabulario y matriz.\n"
            '- **Umbral**: solo entra el contexto relevante; sin contexto, "no lo se" sin llamar al LLM.\n'
            "- **Fuentes y citas**: fragmentos numerados en el prompt y citas validadas contra el rango real.\n"
            "- **Pipeline**: `async def responder` con el LLM inyectado, testeable con un LLM falso.\n"
        ),
        difficulty="intermediate",
        category="ai-fundamentos",
        order=41,
        track="track-5",
        estimated_duration=70,
        prerequisites_titles=["AI 3 · Llamar a un LLM y armar un prompt RAG"],
        exercises=[
            ExerciseTemplate(
                title="Tokenizar y construir el vocabulario",
                description="Normaliza textos y reune sus palabras distintas.",
                instructions=(
                    "Implementa `vocabulario(textos)` que devuelva la lista **ordenada** de palabras distintas de todos los textos. Cada texto se tokeniza en minusculas, sin tildes y sin signos de puntuacion.\n"
                    "\n"
                    "Ejemplo: `vocabulario(['El envío es GRATIS.', 'el pago'])` → `['el', 'envio', 'es', 'gratis', 'pago']`"
                ),
                starter_code=(
                    "import re\n"
                    "import unicodedata\n"
                    "\n"
                    "\n"
                    "def vocabulario(textos):\n"
                    "    # TODO: tokeniza cada texto (minusculas, sin tildes, re.findall(r'\\w+', ...))\n"
                    "    # TODO: devuelve las palabras distintas, ordenadas\n"
                    "    pass\n"
                ),
                hints=[
                    "Para quitar tildes: unicodedata.normalize('NFD', t).encode('ascii', 'ignore').decode().",
                    "Un set guarda cada palabra una sola vez; sorted() lo devuelve como lista ordenada.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "palabras distintas y ordenadas",
                        "code": (
                            "assert vocabulario(['b a c', 'a b']) == ['a', 'b', 'c']\n"
                            "assert vocabulario([]) == []\n"
                        ),
                    },
                    {
                        "name": "minusculas, sin tildes y sin signos",
                        "code": (
                            "obtenido = vocabulario(['El envío es GRATIS.', '¿el pago?'])\n"
                            "assert obtenido == ['el', 'envio', 'es', 'gratis', 'pago'], f'devolvio {obtenido}'\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Embedding de bolsa de palabras",
                description="Convierte un texto en un vector de conteos.",
                instructions=(
                    "Implementa `embed_bow(texto, vocab)` que devuelva un `np.ndarray` de `float` con `len(vocab)` posiciones: en cada una, cuantas veces aparece esa palabra del vocabulario en el texto. Las palabras que no esten en `vocab` se ignoran. El texto se tokeniza con la `tokenizar` que ya trae el starter.\n"
                    "\n"
                    "Ejemplo: con `vocab = ['envio', 'gratis', 'pago']`, `embed_bow('Envío gratis, envío rápido', vocab)` → `array([2., 1., 0.])`"
                ),
                starter_code=(
                    "import re\n"
                    "import unicodedata\n"
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def tokenizar(texto):\n"
                    "    sin_tildes = unicodedata.normalize('NFD', texto.lower()).encode('ascii', 'ignore').decode()\n"
                    "    return re.findall(r'\\w+', sin_tildes)\n"
                    "\n"
                    "\n"
                    "def embed_bow(texto, vocab):\n"
                    "    # TODO: un vector de ceros de largo len(vocab)\n"
                    "    # TODO: suma 1 en la columna de cada palabra del texto que este en vocab\n"
                    "    pass\n"
                ),
                hints=[
                    "Un diccionario {palabra: posicion} evita buscar en la lista cada vez.",
                    "np.zeros(len(vocab)) ya es un vector de float.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "cuenta cada palabra en su columna",
                        "code": (
                            "import numpy as np\n"
                            "v = embed_bow('Envío gratis, envío rápido', ['envio', 'gratis', 'pago'])\n"
                            "assert isinstance(v, np.ndarray) and v.dtype.kind == 'f', 'devuelve un array de float'\n"
                            "assert v.tolist() == [2.0, 1.0, 0.0], f'devolvio {v}'\n"
                        ),
                    },
                    {
                        "name": "las palabras fuera del vocabulario no cuentan",
                        "code": (
                            "import numpy as np\n"
                            "v = embed_bow('hola mundo', ['envio', 'pago'])\n"
                            "assert isinstance(v, np.ndarray) and v.shape == (2,)\n"
                            "assert v.tolist() == [0.0, 0.0]\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Construir el indice una vez",
                description="Reune textos, vocabulario y matriz en un indice reutilizable.",
                instructions=(
                    "Implementa `construir_indice(textos)` que devuelva un diccionario con tres claves:\n"
                    "\n"
                    "- `'textos'`: la lista de textos, tal cual;\n"
                    "- `'vocab'`: el vocabulario ordenado de todos los textos;\n"
                    "- `'matriz'`: un `np.ndarray` de forma `(len(textos), len(vocab))` con el embedding de bolsa de palabras de cada texto en su fila.\n"
                    "\n"
                    "El starter trae `tokenizar` y `embed_bow` resueltos: usalos."
                ),
                starter_code=(
                    "import re\n"
                    "import unicodedata\n"
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def tokenizar(texto):\n"
                    "    sin_tildes = unicodedata.normalize('NFD', texto.lower()).encode('ascii', 'ignore').decode()\n"
                    "    return re.findall(r'\\w+', sin_tildes)\n"
                    "\n"
                    "\n"
                    "def embed_bow(texto, vocab):\n"
                    "    columna = {p: i for i, p in enumerate(vocab)}\n"
                    "    vector = np.zeros(len(vocab))\n"
                    "    for p in tokenizar(texto):\n"
                    "        if p in columna:\n"
                    "            vector[columna[p]] += 1\n"
                    "    return vector\n"
                    "\n"
                    "\n"
                    "def construir_indice(textos):\n"
                    "    # TODO: vocabulario ordenado de todos los textos\n"
                    "    # TODO: matriz con embed_bow(texto, vocab) de cada texto\n"
                    "    # TODO: devuelve {'textos': ..., 'vocab': ..., 'matriz': ...}\n"
                    "    pass\n"
                ),
                hints=[
                    "El vocabulario sale de juntar tokenizar(t) de todos los textos en un set.",
                    "np.array([embed_bow(t, vocab) for t in textos]) apila una fila por texto.",
                    "Con una lista vacia de textos, la matriz no tiene filas: cuida ese caso.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "las tres claves con la forma correcta",
                        "code": (
                            "import numpy as np\n"
                            "ind = construir_indice(['envio gratis', 'pago con tarjeta', 'envio rapido'])\n"
                            "assert set(ind) == {'textos', 'vocab', 'matriz'}, f'claves {set(ind)}'\n"
                            "assert ind['textos'] == ['envio gratis', 'pago con tarjeta', 'envio rapido']\n"
                            "assert ind['matriz'].shape == (3, len(ind['vocab'])), ind['matriz'].shape\n"
                        ),
                    },
                    {
                        "name": "vocabulario ordenado y normalizado",
                        "code": (
                            "ind = construir_indice(['Envío GRATIS', 'pago'])\n"
                            "assert ind['vocab'] == ['envio', 'gratis', 'pago'], ind['vocab']\n"
                        ),
                    },
                    {
                        "name": "cada fila es el embedding de su texto",
                        "code": (
                            "import numpy as np\n"
                            "ind = construir_indice(['a b a', 'c'])\n"
                            "assert ind['vocab'] == ['a', 'b', 'c']\n"
                            "assert np.array_equal(ind['matriz'], np.array([[2.0, 1.0, 0.0], [0.0, 0.0, 1.0]])), ind['matriz']\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Recuperar solo lo relevante",
                description="Top-k con umbral de similitud y sin divisiones por cero.",
                instructions=(
                    "Implementa `recuperar(consulta, matriz, k, umbral)`: `consulta` es un vector y `matriz` tiene un embedding por fila. Devuelve una lista de tuplas `(indice, similitud)` con los como mucho `k` indices de mayor similitud coseno, de mayor a menor, **quitando** los que queden por debajo de `umbral`.\n"
                    "\n"
                    "- `indice` es `int` y `similitud` es `float`.\n"
                    "- Si la consulta o una fila son todo ceros, esa similitud vale `0.0` (sin `nan` ni avisos de division por cero)."
                ),
                starter_code=(
                    "import numpy as np\n"
                    "\n"
                    "\n"
                    "def recuperar(consulta, matriz, k, umbral):\n"
                    "    # TODO: similitud coseno de la consulta con cada fila, sin dividir por cero\n"
                    "    # TODO: ordena de mayor a menor, quita las que no llegan al umbral y quedate con k\n"
                    "    pass\n"
                ),
                hints=[
                    "normas = np.linalg.norm(matriz, axis=1) * np.linalg.norm(consulta) es el denominador.",
                    "np.divide(a, b, out=np.zeros(len(b)), where=b != 0) deja 0 donde b es 0.",
                    "Filtra por umbral antes de cortar a k: si no, podrias devolver menos de los que pasan.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "top-k de mayor a menor",
                        "code": (
                            "import numpy as np\n"
                            "m = np.array([[1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])\n"
                            "res = recuperar(np.array([1.0, 0.0]), m, 2, 0.0)\n"
                            "assert [i for i, _ in res] == [0, 1], res\n"
                            "assert abs(res[0][1] - 1.0) < 1e-9 and abs(res[1][1] - 0.70710678) < 1e-6\n"
                            "assert type(res[0][0]) is int and type(res[0][1]) is float\n"
                        ),
                    },
                    {
                        "name": "el umbral deja fuera lo poco relevante",
                        "code": (
                            "import numpy as np\n"
                            "m = np.array([[1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])\n"
                            "res = recuperar(np.array([1.0, 0.0]), m, 3, 0.8)\n"
                            "assert [i for i, _ in res] == [0], res\n"
                        ),
                    },
                    {
                        "name": "consulta sin palabras conocidas: lista vacia y sin avisos",
                        "code": (
                            "import numpy as np, warnings\n"
                            "m = np.array([[1.0, 0.0], [0.0, 0.0]])\n"
                            "with warnings.catch_warnings():\n"
                            "    warnings.simplefilter('error')\n"
                            "    assert recuperar(np.array([0.0, 0.0]), m, 2, 0.1) == []\n"
                            "    res = recuperar(np.array([1.0, 0.0]), m, 2, 0.0)\n"
                            "assert res[0] == (0, 1.0) and res[1] == (1, 0.0), res\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Leer las citas de la respuesta",
                description="Extrae y valida las fuentes que cita el LLM.",
                instructions=(
                    "Implementa `extraer_citas(respuesta, n_fuentes)` que devuelva la lista de numeros de fuente citados en la respuesta, en el orden en que aparecen por primera vez y sin repetir.\n"
                    "\n"
                    "- Una cita es un numero entre corchetes: `[2]`, y tambien `[1, 3]`.\n"
                    "- Descarta los numeros fuera de `1..n_fuentes`: son citas inventadas.\n"
                    "\n"
                    "Ejemplo: `extraer_citas('Gratis desde 50 euros [2]. Pago seguro [1, 2] [7].', 2)` → `[2, 1]`"
                ),
                starter_code=(
                    "import re\n"
                    "\n"
                    "\n"
                    "def extraer_citas(respuesta, n_fuentes):\n"
                    "    # TODO: busca los grupos entre corchetes con re.findall\n"
                    "    # TODO: saca cada numero, valida el rango y no repitas\n"
                    "    pass\n"
                ),
                hints=[
                    "re.findall(r'\\[([\\d,\\s]+)\\]', texto) devuelve lo de dentro de cada corchete con numeros.",
                    "re.findall(r'\\d+', grupo) separa '1, 3' en ['1', '3'].",
                    "Una lista mas un 'if n not in citas' conserva el orden de aparicion.",
                    "Un corchete con texto, como [nota], no es una cita.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "orden de aparicion y sin repetir",
                        "code": (
                            "obtenido = extraer_citas('Dato [2]. Otro [1]. Otra vez [2].', 3)\n"
                            "assert obtenido == [2, 1], f'devolvio {obtenido}'\n"
                        ),
                    },
                    {
                        "name": "descarta citas fuera de rango",
                        "code": (
                            "assert extraer_citas('Seguro [0] y [4] y [1].', 3) == [1]\n"
                        ),
                    },
                    {
                        "name": "citas multiples en un mismo corchete",
                        "code": (
                            "assert extraer_citas('Ambos lo dicen [1, 3].', 3) == [1, 3]\n"
                            "assert extraer_citas('Pegadas [2][1]', 2) == [2, 1]\n"
                        ),
                    },
                    {
                        "name": "sin citas o con corchetes que no son citas",
                        "code": (
                            "assert extraer_citas('No lo se.', 2) == []\n"
                            "assert extraer_citas('Ver [nota] y [2].', 2) == [2]\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="RAG de punta a punta",
                description="Recupera, genera y devuelve la respuesta con sus fuentes.",
                instructions=(
                    "Implementa `async def responder(pregunta, indice, llm_fn, k=3, umbral=0.2)`. El `indice` tiene las claves `'textos'`, `'vocab'` y `'matriz'`, y `llm_fn` es una funcion asincrona que recibe un prompt y devuelve texto. Devuelve un diccionario `{'respuesta': str, 'fuentes': list[str]}`:\n"
                    "\n"
                    "1. Embede la pregunta con `embed_bow` y recupera como mucho `k` textos cuya similitud coseno llegue a `umbral`, de mayor a menor.\n"
                    "2. Si no queda ninguno, devuelve `NO_SE` como respuesta y `[]` como fuentes **sin llamar** a `llm_fn`.\n"
                    "3. Si hay, construye el prompt con `prompt_con_fuentes` y haz `await llm_fn(prompt)`.\n"
                    "4. Lee las citas de la respuesta (validadas contra el numero de fragmentos) y devuelve en `'fuentes'` los textos citados, en el orden de las citas.\n"
                    "\n"
                    "El starter trae `tokenizar`, `embed_bow`, `prompt_con_fuentes` y `NO_SE`."
                ),
                starter_code=(
                    "import re\n"
                    "import unicodedata\n"
                    "import numpy as np\n"
                    "\n"
                    "NO_SE = 'No lo se: no encontre informacion sobre eso en los documentos.'\n"
                    "\n"
                    "\n"
                    "def tokenizar(texto):\n"
                    "    sin_tildes = unicodedata.normalize('NFD', texto.lower()).encode('ascii', 'ignore').decode()\n"
                    "    return re.findall(r'\\w+', sin_tildes)\n"
                    "\n"
                    "\n"
                    "def embed_bow(texto, vocab):\n"
                    "    columna = {p: i for i, p in enumerate(vocab)}\n"
                    "    vector = np.zeros(len(vocab))\n"
                    "    for p in tokenizar(texto):\n"
                    "        if p in columna:\n"
                    "            vector[columna[p]] += 1\n"
                    "    return vector\n"
                    "\n"
                    "\n"
                    "def prompt_con_fuentes(pregunta, fragmentos):\n"
                    "    fuentes = '\\n'.join(f'[{i}] {texto}' for i, texto in enumerate(fragmentos, start=1))\n"
                    "    return (\n"
                    "        'Responde usando solo las fuentes numeradas. '\n"
                    "        'Cita cada dato con su numero entre corchetes, por ejemplo [1]. '\n"
                    "        'Si las fuentes no bastan, di que no lo sabes.\\n\\n'\n"
                    "        f'Fuentes:\\n{fuentes}\\n\\nPregunta: {pregunta}'\n"
                    "    )\n"
                    "\n"
                    "\n"
                    "async def responder(pregunta, indice, llm_fn, k=3, umbral=0.2):\n"
                    "    # TODO: 1. embede la pregunta y recupera los textos relevantes (umbral y k)\n"
                    "    # TODO: 2. sin textos relevantes: {'respuesta': NO_SE, 'fuentes': []} sin llamar al LLM\n"
                    "    # TODO: 3. prompt_con_fuentes + await llm_fn(prompt)\n"
                    "    # TODO: 4. citas validadas -> textos citados como fuentes\n"
                    "    pass\n"
                ),
                hints=[
                    "Es recuperar() del ejercicio anterior aplicado a indice['matriz'].",
                    "Comprueba si hay fragmentos ANTES de llamar a llm_fn: sin contexto no se gasta la llamada.",
                    "Las citas son numeros 1..len(fragmentos); fragmentos[n - 1] es el texto de la cita n.",
                    "Para probarlo en el editor: resultado = await responder(pregunta, indice, llm_falso).",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "llama al LLM con los fragmentos relevantes numerados",
                        "code": (
                            "import numpy as np\n"
                            "llamadas = []\n"
                            "async def llm_falso(prompt):\n"
                            "    llamadas.append(prompt)\n"
                            "    return 'Gratis desde 50 euros [1].'\n"
                            "textos = ['el envio es gratis desde 50 euros', 'el pago se hace con tarjeta']\n"
                            "vocab = sorted({p for t in textos for p in tokenizar(t)})\n"
                            "indice = {'textos': textos, 'vocab': vocab, 'matriz': np.array([embed_bow(t, vocab) for t in textos])}\n"
                            "resultado = await responder('cuanto cuesta el envio', indice, llm_falso, k=1)\n"
                            "assert len(llamadas) == 1, 'tiene que llamar al LLM una vez'\n"
                            "assert '[1] el envio es gratis desde 50 euros' in llamadas[0], llamadas[0]\n"
                            "assert 'cuanto cuesta el envio' in llamadas[0]\n"
                            "assert 'tarjeta' not in llamadas[0], 'con k=1 solo entra el fragmento mas relevante'\n"
                            "assert resultado['respuesta'] == 'Gratis desde 50 euros [1].'\n"
                        ),
                    },
                    {
                        "name": "las fuentes son los textos citados",
                        "code": (
                            "import numpy as np\n"
                            "async def llm_falso(prompt):\n"
                            "    return 'Con tarjeta [2] y envio gratis [1] [9].'\n"
                            "textos = ['envio gratis desde 50 euros', 'pago con tarjeta o envio contra reembolso']\n"
                            "vocab = sorted({p for t in textos for p in tokenizar(t)})\n"
                            "indice = {'textos': textos, 'vocab': vocab, 'matriz': np.array([embed_bow(t, vocab) for t in textos])}\n"
                            "resultado = await responder('envio y pago', indice, llm_falso, k=2, umbral=0.1)\n"
                            "# La numeracion sigue la relevancia, no el orden del corpus: el texto de pagos\n"
                            "# es [1] (menciona envio y pago) y el de envio es [2]. Asi que [2] va primero.\n"
                            "assert resultado['fuentes'] == ['envio gratis desde 50 euros', 'pago con tarjeta o envio contra reembolso'], resultado\n"
                        ),
                    },
                    {
                        "name": "sin contexto relevante: NO_SE y sin llamar al LLM",
                        "code": (
                            "import numpy as np\n"
                            "llamadas = []\n"
                            "async def llm_falso(prompt):\n"
                            "    llamadas.append(prompt)\n"
                            "    return 'inventado'\n"
                            "textos = ['el envio es gratis', 'el pago con tarjeta']\n"
                            "vocab = sorted({p for t in textos for p in tokenizar(t)})\n"
                            "indice = {'textos': textos, 'vocab': vocab, 'matriz': np.array([embed_bow(t, vocab) for t in textos])}\n"
                            "resultado = await responder('tienen tienda fisica', indice, llm_falso)\n"
                            "assert resultado == {'respuesta': NO_SE, 'fuentes': []}, resultado\n"
                            "assert llamadas == [], 'sin contexto no se llama al LLM'\n"
                        ),
                    },
                    {
                        "name": "el umbral filtra antes de generar",
                        "code": (
                            "import numpy as np\n"
                            "llamadas = []\n"
                            "async def llm_falso(prompt):\n"
                            "    llamadas.append(prompt)\n"
                            "    return 'ok [1]'\n"
                            "textos = ['envio envio envio gratis', 'devoluciones en 30 dias con envio']\n"
                            "vocab = sorted({p for t in textos for p in tokenizar(t)})\n"
                            "indice = {'textos': textos, 'vocab': vocab, 'matriz': np.array([embed_bow(t, vocab) for t in textos])}\n"
                            "resultado = await responder('envio', indice, llm_falso, k=3, umbral=0.5)\n"
                            "assert len(llamadas) == 1\n"
                            "assert 'devoluciones' not in llamadas[0], 'el texto poco relevante no deberia entrar al prompt'\n"
                            "assert resultado['fuentes'] == ['envio envio envio gratis']\n"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="AI 5 · Agentes que usan herramientas",
        description=(
            "Un LLM que actua: describir herramientas, leer la accion en JSON, "
            "validar y ejecutar con seguridad, detectar bucles y el ciclo ReAct "
            "con tope de pasos, probado con un LLM falso que sigue un guion."
        ),
        content=(
            "# AI 5: agentes que usan herramientas\n"
            "\n"
            'En AI 4 el asistente de Nebula respondia con lo que habia en los documentos. Pero la pregunta mas repetida en una tienda no esta en ningun documento: **"¿donde esta mi pedido 1042?"**. Esa respuesta vive en una base de datos y hay que **ir a buscarla**. Un **agente** es un LLM que, en vez de contestar directamente, puede pedir que se ejecute una funcion, leer el resultado y decidir el siguiente paso.\n'
            "\n"
            "## Por que un agente y no solo RAG\n"
            "\n"
            "RAG recupera texto que ya existe. Un agente **actua**: consulta el estado de un pedido, calcula un reembolso, busca en el catalogo. Eso abre tres riesgos que no existian en AI 4:\n"
            "\n"
            "1. **El modelo pide herramientas que no existen** o con argumentos que no tienen sentido, y el programa revienta.\n"
            "2. **Una herramienta falla** (el pedido no existe) y el agente se cae en vez de explicarselo al usuario.\n"
            "3. **El agente entra en bucle**: pide lo mismo una y otra vez, gastando llamadas sin avanzar.\n"
            "\n"
            "Al terminar tendras un agente que valida cada accion antes de ejecutarla, convierte los errores en informacion para el modelo, detecta repeticiones y se detiene con un tope de pasos.\n"
            "\n"
            "## Herramientas: funciones con nombre y descripcion\n"
            "\n"
            "Una herramienta es una funcion normal de Python mas lo que el modelo necesita saber para usarla: **como se llama**, **para que sirve** y **que parametros recibe**.\n"
            "\n"
            "```python\n"
            "PEDIDOS = {1042: 'en camino', 1043: 'entregado'}                      # base de datos de juguete\n"
            "\n"
            "def consultar_pedido(id):                                             # la funcion real\n"
            "    if id not in PEDIDOS:                                             # un caso que va a fallar\n"
            "        raise KeyError(f'el pedido {id} no existe')\n"
            "    return PEDIDOS[id]                                                # 'en camino'\n"
            "\n"
            "HERRAMIENTAS = {                                                      # nombre -> ficha de la herramienta\n"
            "    'consultar_pedido': {\n"
            "        'funcion': consultar_pedido,                                  # lo que se ejecuta\n"
            "        'descripcion': 'Devuelve el estado de un pedido',             # lo que lee el modelo\n"
            "        'parametros': ['id'],                                         # argumentos que acepta\n"
            "    },\n"
            "}\n"
            "\n"
            "def describir_herramientas(herramientas):                             # la parte que va al prompt\n"
            "    lineas = []                                                       # una linea por herramienta\n"
            "    for nombre in sorted(herramientas):                               # orden fijo: prompt estable\n"
            "        ficha = herramientas[nombre]                                  # su descripcion y parametros\n"
            "        lineas.append(f\"- {nombre}({', '.join(ficha['parametros'])}): {ficha['descripcion']}\")\n"
            "    return '\\n'.join(lineas)                                          # texto listo para el prompt\n"
            "\n"
            "print(describir_herramientas(HERRAMIENTAS))   # - consultar_pedido(id): Devuelve el estado de un pedido\n"
            "```\n"
            "\n"
            "El modelo **nunca ejecuta nada**: solo lee esa descripcion y pide. Quien ejecuta es tu codigo, y por eso es tu codigo el que decide que se permite.\n"
            "\n"
            "## El modelo pide una accion en JSON\n"
            "\n"
            "Se le pide al modelo que conteste siempre con un JSON de una de dos formas: pedir una herramienta o dar la respuesta final. Como en AI 3, la salida puede venir con cercas o texto alrededor, asi que se limpia y se normaliza.\n"
            "\n"
            "```python\n"
            "import json                                                           # para leer la accion\n"
            "\n"
            "CERCA = '`' * 3                                                       # tres acentos graves, los de markdown\n"
            "\n"
            "def parsear_accion(texto):                                            # texto del LLM -> accion\n"
            "    t = texto.strip()                                                 # quita espacios de los bordes\n"
            "    if CERCA in t:                                                    # viene dentro de cercas\n"
            "        t = t.split(CERCA)[1].removeprefix('json').strip()           # queda solo el JSON\n"
            "    try:\n"
            "        datos = json.loads(t)                                         # intenta leerlo\n"
            "    except json.JSONDecodeError as error:                             # no es JSON valido\n"
            "        return {'tipo': 'error', 'detalle': f'JSON invalido: {error}'}\n"
            "    if isinstance(datos, dict) and 'herramienta' in datos:            # pide una herramienta\n"
            "        return {'tipo': 'herramienta', 'nombre': datos['herramienta'],\n"
            "                'argumentos': datos.get('argumentos', {})}           # sin argumentos = {}\n"
            "    if isinstance(datos, dict) and 'respuesta' in datos:              # da la respuesta final\n"
            "        return {'tipo': 'respuesta', 'texto': datos['respuesta']}\n"
            "    return {'tipo': 'error', 'detalle': 'falta \"herramienta\" o \"respuesta\"'}   # JSON con otra forma\n"
            "\n"
            'con_cercas = CERCA + \'json\\n{"herramienta": "consultar_pedido", "argumentos": {"id": 1042}}\\n\' + CERCA   # como suele llegar\n'
            "print(parsear_accion(con_cercas))\n"
            "# {'tipo': 'herramienta', 'nombre': 'consultar_pedido', 'argumentos': {'id': 1042}}\n"
            "print(parsear_accion('Claro, te ayudo'))      # {'tipo': 'error', 'detalle': 'JSON invalido: ...'}\n"
            "```\n"
            "\n"
            "Un `error` no es un fallo del programa: es una accion mas, que se le devuelve al modelo para que lo intente otra vez con el formato correcto.\n"
            "\n"
            "## Ejecutar con seguridad: validar y convertir errores en observaciones\n"
            "\n"
            "Antes de ejecutar se comprueba que la herramienta existe y que los argumentos son exactamente los que acepta. Y si la funcion lanza una excepcion, el agente no se cae: el error se convierte en una **observacion** que el modelo lee en el siguiente paso.\n"
            "\n"
            "```python\n"
            "def consultar_pedido(id):                                             # herramienta que puede fallar\n"
            "    pedidos = {1042: 'en camino'}                                     # solo existe el 1042\n"
            "    if id not in pedidos:\n"
            "        raise KeyError(f'el pedido {id} no existe')                   # error de negocio\n"
            "    return pedidos[id]\n"
            "\n"
            "HERRAMIENTAS = {'consultar_pedido': {'funcion': consultar_pedido, 'parametros': ['id']}}\n"
            "\n"
            "def validar_argumentos(parametros, argumentos):                       # antes de ejecutar nada\n"
            "    faltan = sorted(set(parametros) - set(argumentos))                # los que no llegaron\n"
            "    sobran = sorted(set(argumentos) - set(parametros))                # los que el modelo invento\n"
            "    problemas = [f'falta el argumento {p}' for p in faltan]           # uno por argumento ausente\n"
            "    problemas += [f'argumento no permitido: {p}' for p in sobran]     # y uno por cada extra\n"
            "    return problemas                                                  # [] si todo esta bien\n"
            "\n"
            "def ejecutar_herramienta(accion, herramientas):                       # accion -> observacion (texto)\n"
            "    ficha = herramientas.get(accion['nombre'])                        # None si no existe\n"
            "    if ficha is None:\n"
            "        return f\"Error: la herramienta {accion['nombre']} no existe\"  # nombre inventado\n"
            "    problemas = validar_argumentos(ficha['parametros'], accion['argumentos'])\n"
            "    if problemas:\n"
            "        return 'Error: ' + '; '.join(problemas)                       # argumentos mal formados\n"
            "    try:\n"
            "        resultado = ficha['funcion'](**accion['argumentos'])          # **dict -> argumentos con nombre\n"
            "    except Exception as error:                                        # la herramienta fallo\n"
            "        return f'Error: {type(error).__name__}: {error}'              # se le cuenta al modelo\n"
            "    return f'Resultado: {resultado}'                                  # todo bien\n"
            "\n"
            "print(ejecutar_herramienta({'nombre': 'consultar_pedido', 'argumentos': {'id': 1042}}, HERRAMIENTAS))\n"
            "# Resultado: en camino\n"
            "print(ejecutar_herramienta({'nombre': 'consultar_pedido', 'argumentos': {'id': 7}}, HERRAMIENTAS))\n"
            "# Error: KeyError: 'el pedido 7 no existe'\n"
            "print(ejecutar_herramienta({'nombre': 'borrar_pedido', 'argumentos': {'id': 7}}, HERRAMIENTAS))\n"
            "# Error: la herramienta borrar_pedido no existe\n"
            "```\n"
            "\n"
            "`ficha['funcion'](**accion['argumentos'])` desempaqueta el diccionario: `{'id': 1042}` se convierte en la llamada `consultar_pedido(id=1042)`. Por eso hay que validar antes: el diccionario lo escribio el modelo.\n"
            "\n"
            "## Detectar un bucle\n"
            "\n"
            "Un agente atascado repite la misma llamada con los mismos argumentos. Para compararlas hay que tratar `{'id': 1, 'x': 2}` y `{'x': 2, 'id': 1}` como la misma cosa: se pasan a un texto con las claves ordenadas.\n"
            "\n"
            "```python\n"
            "import json                                                           # para la forma canonica\n"
            "\n"
            "def clave_accion(accion):                                             # accion -> texto comparable\n"
            "    argumentos = json.dumps(accion['argumentos'], sort_keys=True)     # mismo orden de claves siempre\n"
            "    return f\"{accion['nombre']}:{argumentos}\"                         # 'consultar_pedido:{\"id\": 1042}'\n"
            "\n"
            "def hay_repeticion(acciones, limite):                                 # True si alguna llamada se pasa del limite\n"
            "    vistas = {}                                                       # clave -> veces\n"
            "    for accion in acciones:\n"
            "        clave = clave_accion(accion)                                  # la misma para el mismo pedido\n"
            "        vistas[clave] = vistas.get(clave, 0) + 1                      # cuenta una mas\n"
            "        if vistas[clave] > limite:                                    # se repitio demasiado\n"
            "            return True\n"
            "    return False                                                      # ninguna paso del limite\n"
            "\n"
            "pedir = {'nombre': 'consultar_pedido', 'argumentos': {'id': 1042}}    # la misma accion\n"
            "print(hay_repeticion([pedir, pedir], limite=2))                       # False: 2 veces esta permitido\n"
            "print(hay_repeticion([pedir, pedir, pedir], limite=2))                # True: la tercera ya es un bucle\n"
            "```\n"
            "\n"
            "## El bucle del agente\n"
            "\n"
            "Todo junto es el patron **ReAct** (razonar y actuar): el modelo pide una accion, tu codigo la ejecuta, la observacion vuelve al prompt, y se repite hasta que haya respuesta final o se acaben los pasos. El **tope de pasos** no es opcional: sin el, un modelo confundido gasta llamadas sin fin.\n"
            "\n"
            "```python\n"
            "import json                                                                  # acciones en JSON\n"
            "\n"
            "PEDIDOS = {1042: 'en camino'}                                                # base de datos de juguete\n"
            "\n"
            "def consultar_pedido(id):                                                    # la herramienta\n"
            "    if id not in PEDIDOS:\n"
            "        raise KeyError(f'el pedido {id} no existe')\n"
            "    return PEDIDOS[id]\n"
            "\n"
            "HERRAMIENTAS = {'consultar_pedido': {'funcion': consultar_pedido,            # su ficha\n"
            "                                     'descripcion': 'Estado de un pedido', 'parametros': ['id']}}\n"
            "\n"
            "def ejecutar(accion):                                                        # version corta de ejecutar_herramienta\n"
            "    try:\n"
            "        return f\"Resultado: {HERRAMIENTAS[accion['herramienta']]['funcion'](**accion['argumentos'])}\"\n"
            "    except Exception as error:                                               # nombre, argumentos o fallo interno\n"
            "        return f'Error: {type(error).__name__}: {error}'\n"
            "\n"
            "async def ejecutar_agente(pregunta, llm_fn, max_pasos=4):\n"
            "    pasos = []                                                               # historial: accion + observacion\n"
            "    for _ in range(max_pasos):                                               # nunca mas de max_pasos llamadas\n"
            "        historial = '\\n'.join(f'Accion: {a}\\nObservacion: {o}' for a, o in pasos)   # lo que ya paso\n"
            "        prompt = (f'Herramientas: consultar_pedido(id)\\nResponde solo con JSON: '\n"
            '                  f\'{{"herramienta": ..., "argumentos": ...}} o {{"respuesta": ...}}\\n\'\n'
            "                  f'Pregunta: {pregunta}\\n{historial}')                      # herramientas + pregunta + historial\n"
            "        texto = await llm_fn(prompt)                                         # el modelo decide\n"
            "        accion = json.loads(texto)                                           # (en el ejercicio, con parsear_accion)\n"
            "        if 'respuesta' in accion:                                            # termino\n"
            "            return {'respuesta': accion['respuesta'], 'pasos': len(pasos)}\n"
            "        pasos.append((texto, ejecutar(accion)))                              # actua y guarda lo observado\n"
            "    return {'respuesta': None, 'pasos': len(pasos)}                          # se acabaron los pasos\n"
            "\n"
            'guion = iter([\'{"herramienta": "consultar_pedido", "argumentos": {"id": 1042}}\',   # 1o pide la herramienta\n'
            '              \'{"respuesta": "Tu pedido 1042 esta en camino."}\'])                  # 2o responde con lo observado\n'
            "\n"
            "async def llm_falso(prompt):                                                 # sigue el guion, sin gastar llamadas\n"
            "    return next(guion)\n"
            "\n"
            "print(await ejecutar_agente('donde esta mi pedido 1042', llm_falso))\n"
            "# {'respuesta': 'Tu pedido 1042 esta en camino.', 'pasos': 1}\n"
            "```\n"
            "\n"
            "Con `pycode.llm_complete` en lugar de `llm_falso` tienes un agente real. Los modelos siguen el formato JSON la mayoria de las veces, pero no siempre: por eso el ejercicio final usa `parsear_accion` y trata el JSON invalido como una observacion mas.\n"
            "\n"
            "## Errores comunes\n"
            "\n"
            "- **Ejecutar lo que pide el modelo sin validarlo.** Los argumentos los escribe el LLM: puede inventar una herramienta o un parametro. Comprueba nombre y argumentos antes de llamar a la funcion.\n"
            "- **Dejar que una excepcion tumbe el agente.** Si `consultar_pedido` lanza `KeyError`, el usuario se queda sin respuesta. Captura el error y devuelvelo como observacion: el modelo puede explicar que el pedido no existe.\n"
            "- **Bucle sin tope.** Un modelo confundido pide lo mismo para siempre y cada vuelta cuesta dinero. Pon `max_pasos` y detecta llamadas repetidas.\n"
            '- **Comparar acciones como texto sin normalizar.** `{"id": 1, "x": 2}` y `{"x": 2, "id": 1}` son la misma llamada con otro orden. Usa `json.dumps(..., sort_keys=True)` para compararlas.\n'
            "- **No devolver la observacion al modelo.** Si el resultado de la herramienta no entra en el siguiente prompt, el modelo vuelve a pedirlo. El historial de acciones y observaciones es lo que le permite avanzar.\n"
            "\n"
            "## Resumen\n"
            "\n"
            "- **Herramienta**: funcion + nombre + descripcion + parametros; el modelo solo lee la ficha.\n"
            "- **Accion**: JSON con `herramienta` y `argumentos`, o con `respuesta`; lo invalido se trata como error y se reintenta.\n"
            "- **Ejecucion segura**: validar nombre y argumentos, capturar excepciones y convertirlas en observaciones.\n"
            "- **Repeticiones**: comparar acciones en forma canonica y cortar al pasar el limite.\n"
            "- **ReAct**: pedir accion, ejecutar, observar y repetir, siempre con tope de pasos.\n"
        ),
        difficulty="intermediate",
        category="ai-fundamentos",
        order=42,
        track="track-5",
        estimated_duration=70,
        prerequisites_titles=["AI 4 · RAG de punta a punta"],
        exercises=[
            ExerciseTemplate(
                title="Describir las herramientas al modelo",
                description="Convierte las fichas de herramientas en el texto del prompt.",
                instructions=(
                    "Implementa `describir_herramientas(herramientas)`. `herramientas` es un diccionario nombre → ficha, y cada ficha tiene `'descripcion'` (texto) y `'parametros'` (lista de nombres). Devuelve un texto con una linea por herramienta, **ordenadas por nombre**, con el formato `- nombre(param1, param2): descripcion`. Sin herramientas, texto vacio.\n"
                    "\n"
                    "Ejemplo:\n"
                    "\n"
                    "```\n"
                    "describir_herramientas({\n"
                    "    'consultar_pedido': {'descripcion': 'Estado de un pedido', 'parametros': ['id']},\n"
                    "    'calcular_envio': {'descripcion': 'Coste del envio', 'parametros': ['peso', 'destino']},\n"
                    "})\n"
                    "```\n"
                    "\n"
                    "devuelve `'- calcular_envio(peso, destino): Coste del envio\\n- consultar_pedido(id): Estado de un pedido'`"
                ),
                starter_code=(
                    "def describir_herramientas(herramientas):\n"
                    "    # TODO: una linea por herramienta, ordenadas por nombre\n"
                    "    # TODO: formato '- nombre(param1, param2): descripcion'\n"
                    "    pass\n"
                ),
                hints=[
                    "sorted(herramientas) recorre los nombres en orden alfabetico.",
                    "', '.join(ficha['parametros']) arma 'peso, destino'.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "una linea por herramienta, en orden",
                        "code": (
                            "obtenido = describir_herramientas({\n"
                            "    'consultar_pedido': {'descripcion': 'Estado de un pedido', 'parametros': ['id']},\n"
                            "    'calcular_envio': {'descripcion': 'Coste del envio', 'parametros': ['peso', 'destino']},\n"
                            "})\n"
                            "assert obtenido == '- calcular_envio(peso, destino): Coste del envio\\n- consultar_pedido(id): Estado de un pedido', repr(obtenido)\n"
                        ),
                    },
                    {
                        "name": "sin parametros y sin herramientas",
                        "code": (
                            "assert describir_herramientas({'hora': {'descripcion': 'Hora actual', 'parametros': []}}) == '- hora(): Hora actual'\n"
                            "assert describir_herramientas({}) == ''\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Validar los argumentos",
                description="Detecta argumentos que faltan o que el modelo invento.",
                instructions=(
                    "Implementa `validar_argumentos(parametros, argumentos)`: `parametros` es la lista de nombres que acepta la herramienta y `argumentos` el diccionario que pidio el modelo. Devuelve una lista de problemas, vacia si todo esta bien:\n"
                    "\n"
                    "- primero `'falta el argumento X'` por cada parametro ausente, en orden alfabetico;\n"
                    "- despues `'argumento no permitido: X'` por cada argumento que sobra, en orden alfabetico.\n"
                    "\n"
                    "Ejemplo: `validar_argumentos(['id'], {'pedido': 7, 'urgente': True})` → `['falta el argumento id', 'argumento no permitido: pedido', 'argumento no permitido: urgente']`"
                ),
                starter_code=(
                    "def validar_argumentos(parametros, argumentos):\n"
                    "    # TODO: parametros que no estan en argumentos -> 'falta el argumento X'\n"
                    "    # TODO: argumentos que no estan en parametros -> 'argumento no permitido: X'\n"
                    "    pass\n"
                ),
                hints=[
                    "set(parametros) - set(argumentos) da los que faltan.",
                    "Recorrer un diccionario da sus claves: set(argumentos) son los nombres pedidos.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "argumentos correctos: sin problemas",
                        "code": (
                            "resultado = validar_argumentos(['peso', 'destino'], {'destino': 'Lima', 'peso': 2})\n"
                            "assert resultado == [], f'devolvio {resultado!r}'\n"
                        ),
                    },
                    {
                        "name": "faltan y sobran, en orden",
                        "code": (
                            "obtenido = validar_argumentos(['id'], {'pedido': 7, 'urgente': True})\n"
                            "assert obtenido == ['falta el argumento id', 'argumento no permitido: pedido', 'argumento no permitido: urgente'], obtenido\n"
                            "assert validar_argumentos(['b', 'a'], {}) == ['falta el argumento a', 'falta el argumento b']\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Leer la accion del modelo",
                description="Normaliza el JSON del LLM en una accion que el programa entiende.",
                instructions=(
                    "Implementa `parsear_accion(texto)` que devuelva un diccionario con la clave `'tipo'`:\n"
                    "\n"
                    "- `{'tipo': 'herramienta', 'nombre': ..., 'argumentos': {...}}` si el JSON tiene `\"herramienta\"` (sin `\"argumentos\"`, usa `{}`);\n"
                    "- `{'tipo': 'respuesta', 'texto': ...}` si tiene `\"respuesta\"`;\n"
                    "- `{'tipo': 'error', 'detalle': ...}` si no es JSON valido o no tiene ninguna de las dos claves.\n"
                    "\n"
                    "El JSON puede venir dentro de cercas ```` ```json ```` o ```` ``` ````. Nunca lanza excepciones: un texto invalido es una accion de tipo `'error'`."
                ),
                starter_code=(
                    "import json\n"
                    "\n"
                    "\n"
                    "def parsear_accion(texto):\n"
                    "    # TODO: quita las cercas si las hay\n"
                    "    # TODO: json.loads dentro de try/except json.JSONDecodeError\n"
                    "    # TODO: devuelve la accion normalizada segun las claves\n"
                    "    pass\n"
                ),
                hints=[
                    "t.split('```')[1] da lo de dentro de las cercas; .removeprefix('json') quita la etiqueta.",
                    "json.JSONDecodeError es la excepcion de un JSON mal escrito.",
                    "Comprueba que lo leido sea un dict: '[1, 2]' es JSON valido pero no es una accion.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "pedir una herramienta, con o sin cercas",
                        "code": (
                            'a = parsear_accion(\'{"herramienta": "consultar_pedido", "argumentos": {"id": 1042}}\')\n'
                            "assert a == {'tipo': 'herramienta', 'nombre': 'consultar_pedido', 'argumentos': {'id': 1042}}, a\n"
                            'b = parsear_accion(\'```json\\n{"herramienta": "hora"}\\n```\')\n'
                            "assert b == {'tipo': 'herramienta', 'nombre': 'hora', 'argumentos': {}}, b\n"
                        ),
                    },
                    {
                        "name": "respuesta final",
                        "code": (
                            "assert parsear_accion('```\\n{\"respuesta\": \"Esta en camino\"}\\n```') == {'tipo': 'respuesta', 'texto': 'Esta en camino'}\n"
                        ),
                    },
                    {
                        "name": "texto invalido es un error, no una excepcion",
                        "code": (
                            "for malo in ('Claro, te ayudo', '{\"otra\": 1}', '[1, 2]'):\n"
                            "    accion = parsear_accion(malo)\n"
                            "    assert isinstance(accion, dict) and accion.get('tipo') == 'error', f'{malo!r} -> {accion!r}'\n"
                            "    assert accion.get('detalle'), 'el error explica que paso'\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Ejecutar una herramienta con seguridad",
                description="Valida la accion y convierte cualquier fallo en una observacion.",
                instructions=(
                    "Implementa `ejecutar_herramienta(accion, herramientas)`. `accion` tiene `'nombre'` y `'argumentos'`; cada ficha de `herramientas` tiene `'funcion'` y `'parametros'`. Devuelve **siempre un texto** (nunca lanza):\n"
                    "\n"
                    "- `'Error: la herramienta X no existe'` si el nombre no esta;\n"
                    "- `'Error: '` + los problemas de `validar_argumentos` unidos con `'; '` si los hay;\n"
                    "- `'Error: TipoDeError: mensaje'` si la funcion lanza una excepcion;\n"
                    "- `'Resultado: ...'` con lo que devuelve la funcion si todo va bien.\n"
                    "\n"
                    "El starter trae `validar_argumentos` resuelto."
                ),
                starter_code=(
                    "def validar_argumentos(parametros, argumentos):\n"
                    "    faltan = sorted(set(parametros) - set(argumentos))\n"
                    "    sobran = sorted(set(argumentos) - set(parametros))\n"
                    "    return [f'falta el argumento {p}' for p in faltan] + [f'argumento no permitido: {p}' for p in sobran]\n"
                    "\n"
                    "\n"
                    "def ejecutar_herramienta(accion, herramientas):\n"
                    "    # TODO: herramienta inexistente -> 'Error: la herramienta X no existe'\n"
                    "    # TODO: argumentos invalidos -> 'Error: ' + problemas unidos con '; '\n"
                    "    # TODO: llama a la funcion con **argumentos dentro de try/except\n"
                    "    pass\n"
                ),
                hints=[
                    "herramientas.get(nombre) devuelve None si no existe.",
                    "ficha['funcion'](**accion['argumentos']) pasa el diccionario como argumentos con nombre.",
                    "type(error).__name__ da el nombre de la excepcion, por ejemplo 'KeyError'.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "ejecuta y devuelve el resultado",
                        "code": (
                            "herr = {'sumar': {'funcion': lambda a, b: a + b, 'parametros': ['a', 'b']}}\n"
                            "assert ejecutar_herramienta({'nombre': 'sumar', 'argumentos': {'a': 2, 'b': 3}}, herr) == 'Resultado: 5'\n"
                        ),
                    },
                    {
                        "name": "herramienta inexistente o argumentos invalidos",
                        "code": (
                            "herr = {'sumar': {'funcion': lambda a, b: a + b, 'parametros': ['a', 'b']}}\n"
                            "assert ejecutar_herramienta({'nombre': 'restar', 'argumentos': {}}, herr) == 'Error: la herramienta restar no existe'\n"
                            "obtenido = ejecutar_herramienta({'nombre': 'sumar', 'argumentos': {'a': 1, 'c': 2}}, herr)\n"
                            "assert obtenido == 'Error: falta el argumento b; argumento no permitido: c', obtenido\n"
                        ),
                    },
                    {
                        "name": "una excepcion de la herramienta se vuelve observacion",
                        "code": (
                            "def dividir(a, b):\n"
                            "    return a / b\n"
                            "herr = {'dividir': {'funcion': dividir, 'parametros': ['a', 'b']}}\n"
                            "obtenido = ejecutar_herramienta({'nombre': 'dividir', 'argumentos': {'a': 1, 'b': 0}}, herr)\n"
                            "assert obtenido.startswith('Error: ZeroDivisionError: '), obtenido\n"
                            "llamadas = []\n"
                            "herr2 = {'marca': {'funcion': lambda x: llamadas.append(x), 'parametros': ['x']}}\n"
                            "ejecutar_herramienta({'nombre': 'marca', 'argumentos': {'x': 1, 'y': 2}}, herr2)\n"
                            "assert llamadas == [], 'con argumentos invalidos la funcion no debe ejecutarse'\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Detectar un agente en bucle",
                description="Encuentra llamadas repetidas aunque cambie el orden de los argumentos.",
                instructions=(
                    "Implementa `hay_repeticion(acciones, limite)`: `acciones` es la lista de acciones ejecutadas, cada una con `'nombre'` y `'argumentos'`. Devuelve `True` si alguna misma llamada (mismo nombre y mismos argumentos) aparece **mas de** `limite` veces.\n"
                    "\n"
                    "Dos llamadas son la misma aunque sus argumentos tengan las claves en otro orden: `{'id': 1, 'x': 2}` y `{'x': 2, 'id': 1}` cuentan juntas. No importa si las repeticiones son seguidas o estan intercaladas con otras acciones."
                ),
                starter_code=(
                    "import json\n"
                    "\n"
                    "\n"
                    "def hay_repeticion(acciones, limite):\n"
                    "    # TODO: una clave comparable por accion (nombre + argumentos con claves ordenadas)\n"
                    "    # TODO: cuenta las veces de cada clave y avisa en cuanto una pase del limite\n"
                    "    pass\n"
                ),
                hints=[
                    "json.dumps(argumentos, sort_keys=True) da el mismo texto sea cual sea el orden de las claves.",
                    "Un diccionario clave -> veces lleva la cuenta.",
                    "'Mas de limite' es >, no >=: con limite=2, dos veces esta permitido.",
                    "Los argumentos anidados ({'filtro': {'a': 1, 'b': 2}}) tambien se ordenan con sort_keys.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "cuenta por encima del limite",
                        "code": (
                            "p = {'nombre': 'consultar_pedido', 'argumentos': {'id': 1042}}\n"
                            "assert hay_repeticion([p, p], 2) is False\n"
                            "assert hay_repeticion([p, p, p], 2) is True\n"
                        ),
                    },
                    {
                        "name": "mismo pedido con claves en otro orden",
                        "code": (
                            "a = {'nombre': 'buscar', 'argumentos': {'texto': 'envio', 'k': 3}}\n"
                            "b = {'nombre': 'buscar', 'argumentos': {'k': 3, 'texto': 'envio'}}\n"
                            "assert hay_repeticion([a, b], 1) is True, 'son la misma llamada'\n"
                        ),
                    },
                    {
                        "name": "distinto nombre o argumentos no suman",
                        "code": (
                            "acciones = [\n"
                            "    {'nombre': 'consultar_pedido', 'argumentos': {'id': 1}},\n"
                            "    {'nombre': 'consultar_pedido', 'argumentos': {'id': 2}},\n"
                            "    {'nombre': 'rastrear', 'argumentos': {'id': 1}},\n"
                            "]\n"
                            "assert hay_repeticion(acciones, 1) is False\n"
                            "assert hay_repeticion([], 0) is False\n"
                        ),
                    },
                    {
                        "name": "repeticiones intercaladas y argumentos anidados",
                        "code": (
                            "x = {'nombre': 'filtrar', 'argumentos': {'filtro': {'a': 1, 'b': 2}}}\n"
                            "y = {'nombre': 'filtrar', 'argumentos': {'filtro': {'b': 2, 'a': 1}}}\n"
                            "otra = {'nombre': 'hora', 'argumentos': {}}\n"
                            "assert hay_repeticion([x, otra, y, otra], 1) is True\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="El bucle del agente",
                description="ReAct con tope de pasos, errores recuperables y respuesta final.",
                instructions=(
                    "Implementa `async def ejecutar_agente(pregunta, herramientas, llm_fn, max_pasos=5)`. `llm_fn` es asincrona: recibe un prompt y devuelve el texto del modelo. Devuelve `{'respuesta': texto o None, 'pasos': lista, 'motivo': 'respuesta' o 'max_pasos'}`.\n"
                    "\n"
                    "En cada paso, como mucho `max_pasos` veces:\n"
                    "\n"
                    "1. `prompt = construir_prompt(pregunta, herramientas, pasos)` y `texto = await llm_fn(prompt)`.\n"
                    "2. `accion = parsear_accion(texto)`.\n"
                    "3. Si es una `'respuesta'`, termina con esa respuesta y motivo `'respuesta'`.\n"
                    "4. Si es una `'herramienta'`, la observacion es `ejecutar_herramienta(accion, herramientas)`.\n"
                    "5. Si es un `'error'`, la observacion es `'Error de formato: ' + accion['detalle']`: el modelo lo vera y podra corregirse.\n"
                    "6. Anade a `pasos` un diccionario `{'llm': texto, 'observacion': observacion}`.\n"
                    "\n"
                    "Si se agotan los pasos, devuelve respuesta `None` y motivo `'max_pasos'`. El starter trae `describir_herramientas`, `parsear_accion`, `ejecutar_herramienta` y `construir_prompt`."
                ),
                starter_code=(
                    "import json\n"
                    "\n"
                    "\n"
                    "def describir_herramientas(herramientas):\n"
                    "    return '\\n'.join(\n"
                    "        f\"- {n}({', '.join(herramientas[n]['parametros'])}): {herramientas[n]['descripcion']}\"\n"
                    "        for n in sorted(herramientas)\n"
                    "    )\n"
                    "\n"
                    "\n"
                    "def parsear_accion(texto):\n"
                    "    t = texto.strip()\n"
                    "    if '```' in t:\n"
                    "        t = t.split('```')[1].removeprefix('json').strip()\n"
                    "    try:\n"
                    "        datos = json.loads(t)\n"
                    "    except json.JSONDecodeError as error:\n"
                    "        return {'tipo': 'error', 'detalle': f'JSON invalido: {error}'}\n"
                    "    if isinstance(datos, dict) and 'herramienta' in datos:\n"
                    "        return {'tipo': 'herramienta', 'nombre': datos['herramienta'], 'argumentos': datos.get('argumentos', {})}\n"
                    "    if isinstance(datos, dict) and 'respuesta' in datos:\n"
                    "        return {'tipo': 'respuesta', 'texto': datos['respuesta']}\n"
                    "    return {'tipo': 'error', 'detalle': 'falta \"herramienta\" o \"respuesta\"'}\n"
                    "\n"
                    "\n"
                    "def ejecutar_herramienta(accion, herramientas):\n"
                    "    ficha = herramientas.get(accion['nombre'])\n"
                    "    if ficha is None:\n"
                    "        return f\"Error: la herramienta {accion['nombre']} no existe\"\n"
                    "    faltan = sorted(set(ficha['parametros']) - set(accion['argumentos']))\n"
                    "    sobran = sorted(set(accion['argumentos']) - set(ficha['parametros']))\n"
                    "    if faltan or sobran:\n"
                    "        return 'Error: ' + '; '.join([f'falta el argumento {p}' for p in faltan] + [f'argumento no permitido: {p}' for p in sobran])\n"
                    "    try:\n"
                    "        return f\"Resultado: {ficha['funcion'](**accion['argumentos'])}\"\n"
                    "    except Exception as error:\n"
                    "        return f'Error: {type(error).__name__}: {error}'\n"
                    "\n"
                    "\n"
                    "def construir_prompt(pregunta, herramientas, pasos):\n"
                    "    historial = '\\n'.join(f'Accion: {p[\"llm\"]}\\nObservacion: {p[\"observacion\"]}' for p in pasos)\n"
                    "    return (\n"
                    "        'Eres el asistente de Nebula. Herramientas disponibles:\\n'\n"
                    "        f'{describir_herramientas(herramientas)}\\n\\n'\n"
                    '        \'Responde SOLO con JSON: {"herramienta": nombre, "argumentos": {...}} \'\n'
                    "        'o {\"respuesta\": texto}.\\n\\n'\n"
                    "        f'Pregunta: {pregunta}\\n{historial}'\n"
                    "    )\n"
                    "\n"
                    "\n"
                    "async def ejecutar_agente(pregunta, herramientas, llm_fn, max_pasos=5):\n"
                    "    pasos = []\n"
                    "    # TODO: como mucho max_pasos vueltas:\n"
                    "    #   prompt -> await llm_fn -> parsear_accion\n"
                    "    #   respuesta: termina | herramienta: ejecutar | error: 'Error de formato: ...'\n"
                    "    #   guarda {'llm': texto, 'observacion': ...} en pasos\n"
                    "    # TODO: si se acaban los pasos: respuesta None y motivo 'max_pasos'\n"
                    "    pass\n"
                ),
                hints=[
                    "El historial que ve el modelo sale de pasos: por eso cada paso guarda lo que dijo y lo que observo.",
                    "La respuesta final no se añade a pasos: pasos solo tiene las acciones ejecutadas.",
                    "Un for _ in range(max_pasos) garantiza el tope; el return de la respuesta sale antes.",
                    "Para probarlo: resultado = await ejecutar_agente('...', herramientas, llm_falso).",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "usa la herramienta y responde con lo observado",
                        "code": (
                            "prompts = []\n"
                            'guion = iter([\'{"herramienta": "consultar_pedido", "argumentos": {"id": 1042}}\',\n'
                            '              \'{"respuesta": "Tu pedido 1042 esta en camino."}\'])\n'
                            "async def llm_falso(prompt):\n"
                            "    prompts.append(prompt)\n"
                            "    return next(guion)\n"
                            "herr = {'consultar_pedido': {'funcion': lambda id: {1042: 'en camino'}[id],\n"
                            "                             'descripcion': 'Estado de un pedido', 'parametros': ['id']}}\n"
                            "r = await ejecutar_agente('donde esta mi pedido 1042', herr, llm_falso)\n"
                            "assert r['respuesta'] == 'Tu pedido 1042 esta en camino.' and r['motivo'] == 'respuesta', r\n"
                            "assert len(r['pasos']) == 1 and r['pasos'][0]['observacion'] == 'Resultado: en camino', r['pasos']\n"
                            "assert len(prompts) == 2\n"
                            "assert 'Resultado: en camino' in prompts[1], 'la observacion tiene que llegar al siguiente prompt'\n"
                        ),
                    },
                    {
                        "name": "se detiene al llegar a max_pasos",
                        "code": (
                            "llamadas = []\n"
                            "async def llm_terco(prompt):\n"
                            "    llamadas.append(prompt)\n"
                            '    return \'{"herramienta": "hora", "argumentos": {}}\'\n'
                            "herr = {'hora': {'funcion': lambda: '10:00', 'descripcion': 'Hora actual', 'parametros': []}}\n"
                            "r = await ejecutar_agente('que hora es', herr, llm_terco, max_pasos=3)\n"
                            "assert r['respuesta'] is None and r['motivo'] == 'max_pasos', r\n"
                            "assert len(llamadas) == 3 and len(r['pasos']) == 3, 'nunca mas llamadas que max_pasos'\n"
                        ),
                    },
                    {
                        "name": "se recupera de un JSON mal formado",
                        "code": (
                            "guion = iter(['Claro, ahora lo miro', '{\"respuesta\": \"Son las 10:00\"}'])\n"
                            "prompts = []\n"
                            "async def llm_falso(prompt):\n"
                            "    prompts.append(prompt)\n"
                            "    return next(guion)\n"
                            "herr = {'hora': {'funcion': lambda: '10:00', 'descripcion': 'Hora actual', 'parametros': []}}\n"
                            "r = await ejecutar_agente('que hora es', herr, llm_falso)\n"
                            "assert r['respuesta'] == 'Son las 10:00', r\n"
                            "assert r['pasos'][0]['observacion'].startswith('Error de formato: '), r['pasos']\n"
                            "assert 'Error de formato' in prompts[1], 'el modelo tiene que ver su error de formato'\n"
                        ),
                    },
                    {
                        "name": "un fallo de la herramienta no tumba al agente",
                        "code": (
                            "def consultar_pedido(id):\n"
                            "    raise KeyError(f'el pedido {id} no existe')\n"
                            'guion = iter([\'{"herramienta": "consultar_pedido", "argumentos": {"id": 7}}\',\n'
                            '              \'{"herramienta": "borrar_todo", "argumentos": {}}\',\n'
                            '              \'{"respuesta": "No encuentro el pedido 7."}\'])\n'
                            "async def llm_falso(prompt):\n"
                            "    return next(guion)\n"
                            "herr = {'consultar_pedido': {'funcion': consultar_pedido, 'descripcion': 'Estado', 'parametros': ['id']}}\n"
                            "r = await ejecutar_agente('donde esta el pedido 7', herr, llm_falso)\n"
                            "assert r['respuesta'] == 'No encuentro el pedido 7.', r\n"
                            "assert r['pasos'][0]['observacion'].startswith('Error: KeyError'), r['pasos']\n"
                            "assert r['pasos'][1]['observacion'] == 'Error: la herramienta borrar_todo no existe'\n"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="AI 6 · Evaluar sistemas con LLM",
        description=(
            "Saber si un cambio mejora o empeora: conjunto de casos, metricas "
            "deterministas, un LLM como juez con veredicto validado y comparacion "
            "entre versiones caso por caso para detectar regresiones."
        ),
        content=(
            "# AI 6: evaluar sistemas con LLM\n"
            "\n"
            'El asistente de Nebula ya responde con documentos (AI 4) y consulta pedidos (AI 5). Ahora alguien propone cambiar el prompt, o pasar a un modelo mas barato. ¿Mejora o empeora? Probar tres preguntas a mano y decir "parece que va bien" no es una respuesta: es una opinion. Esta leccion construye una **evaluacion**: un conjunto de casos, metricas automaticas y una comparacion entre versiones que dice que casos se rompieron.\n'
            "\n"
            '## Por que evaluar y no "probar un rato"\n'
            "\n"
            "Un sistema con LLM cambia de comportamiento con cosas que parecen inofensivas: una frase del prompt, la temperatura, la version del modelo. Sin evaluacion pasan tres cosas:\n"
            "\n"
            "1. **Regresiones invisibles.** El cambio arregla la pregunta que estabas mirando y rompe otras cinco que no volviste a probar.\n"
            "2. **Decisiones por intuicion.** Dos personas prueban preguntas distintas y llegan a conclusiones opuestas.\n"
            '3. **Juicios que no se pueden repetir.** "Me gusto mas la respuesta" no se puede automatizar ni poner en CI.\n'
            "\n"
            "Al terminar tendras una funcion `evaluar` que corre todos los casos contra el sistema, combina metricas deterministas con un LLM como juez, y otra que compara dos versiones caso por caso.\n"
            "\n"
            "## El conjunto de evaluacion\n"
            "\n"
            'Cada **caso** es una pregunta con lo que una buena respuesta tiene que cumplir. No se guarda "la respuesta correcta" palabra por palabra, porque un LLM puede decir lo mismo de mil formas: se guardan los **datos clave** y las **fuentes** que debe usar.\n'
            "\n"
            "```python\n"
            "CASOS = [                                                             # el conjunto de evaluacion\n"
            "    {\n"
            "        'id': 'envio-gratis',                                         # identificador estable\n"
            "        'pregunta': '¿Desde cuanto el envio es gratis?',              # lo que pregunta un usuario\n"
            "        'datos_clave': ['50 euros'],                                  # lo que no puede faltar\n"
            "        'fuentes_esperadas': ['envios.md'],                           # de donde tiene que salir\n"
            "    },\n"
            "    {\n"
            "        'id': 'devolucion-plazo',\n"
            "        'pregunta': '¿Cuantos dias tengo para devolver algo?',\n"
            "        'datos_clave': ['30 dias'],\n"
            "        'fuentes_esperadas': ['devoluciones.md'],\n"
            "    },\n"
            "]\n"
            "\n"
            "for caso in CASOS:                                                    # un vistazo al conjunto\n"
            "    print(caso['id'], '->', caso['datos_clave'])                      # envio-gratis -> ['50 euros']\n"
            "```\n"
            "\n"
            "Los casos salen de **preguntas reales** de usuarios y de los errores que ya tuviste: cada fallo que arreglas se convierte en un caso, para que no vuelva.\n"
            "\n"
            "## Metricas deterministas\n"
            "\n"
            "Antes de pedirle nada a otro LLM se mide lo que se puede medir con codigo: si la respuesta contiene los datos clave y si cito las fuentes correctas. Para comparar texto hay que **normalizar**: mayusculas, tildes y espacios no deben cambiar el resultado.\n"
            "\n"
            "```python\n"
            "import re                                                             # para limpiar el texto\n"
            "import unicodedata                                                    # para quitar tildes\n"
            "\n"
            "def normalizar(texto):                                                # texto comparable\n"
            "    sin_tildes = unicodedata.normalize('NFD', texto.lower()).encode('ascii', 'ignore').decode()\n"
            "    solo_palabras = re.sub(r'[^\\w\\s]', ' ', sin_tildes)               # signos fuera\n"
            "    return ' '.join(solo_palabras.split())                            # un solo espacio entre palabras\n"
            "\n"
            "def contiene_datos(respuesta, datos_clave):                           # fraccion de datos presentes\n"
            "    if not datos_clave:                                               # nada que comprobar\n"
            "        return 1.0\n"
            "    texto = normalizar(respuesta)                                     # la respuesta, normalizada\n"
            "    presentes = [d for d in datos_clave if normalizar(d) in texto]    # los que aparecen\n"
            "    return len(presentes) / len(datos_clave)                          # 0.0 a 1.0\n"
            "\n"
            "def puntuar_fuentes(citadas, esperadas):                              # ¿cito lo que debia?\n"
            "    citadas, esperadas = set(citadas), set(esperadas)                 # sin duplicados\n"
            "    aciertos = len(citadas & esperadas)                               # las correctas\n"
            "    precision = aciertos / len(citadas) if citadas else 0.0           # de lo que cito, cuanto sobraba\n"
            "    recall = aciertos / len(esperadas) if esperadas else 1.0          # de lo esperado, cuanto cito\n"
            "    return {'precision': precision, 'recall': recall}\n"
            "\n"
            "print(contiene_datos('El envío es GRATIS desde 50  euros.', ['50 euros', 'gratis']))   # 1.0\n"
            "print(puntuar_fuentes(['envios.md', 'pagos.md'], ['envios.md']))     # {'precision': 0.5, 'recall': 1.0}\n"
            "```\n"
            "\n"
            "**Precision** baja significa que cito fuentes que no venian al caso; **recall** bajo, que le falto alguna. Las dos importan: un sistema que cita todos los documentos tiene recall perfecto y no sirve de nada.\n"
            "\n"
            "## Un LLM como juez\n"
            "\n"
            "Hay cosas que el codigo no mide bien: si la respuesta es clara, si contesta lo que se pregunto, si el tono es correcto. Para eso se usa otro LLM como **juez**, con una **rubrica** explicita y un veredicto en JSON que se valida como cualquier otra salida de un modelo.\n"
            "\n"
            "```python\n"
            "import json                                                           # el veredicto viene en JSON\n"
            "\n"
            "def prompt_juez(pregunta, respuesta):                                 # rubrica cerrada, salida cerrada\n"
            "    return (\n"
            "        'Evalua la respuesta de un asistente de atencion al cliente.\\n'\n"
            "        'Puntua de 1 a 5: 5 = correcta, completa y clara; 1 = incorrecta o no contesta.\\n'\n"
            '        \'Responde SOLO con JSON: {"puntuacion": entero, "motivo": texto breve}.\\n\\n\'\n'
            "        f'Pregunta: {pregunta}\\nRespuesta: {respuesta}'\n"
            "    )\n"
            "\n"
            "def parsear_veredicto(texto):                                         # JSON del juez -> dict o None\n"
            "    try:\n"
            "        datos = json.loads(texto)                                     # (en el ejercicio tambien con cercas)\n"
            "    except json.JSONDecodeError:\n"
            "        return None                                                   # ilegible: sin veredicto\n"
            "    puntos = datos.get('puntuacion') if isinstance(datos, dict) else None\n"
            "    if type(puntos) is not int or not 1 <= puntos <= 5:               # True no es un entero valido\n"
            "        return None                                                   # fuera de la rubrica\n"
            "    return {'puntuacion': puntos, 'motivo': str(datos.get('motivo', ''))}\n"
            "\n"
            'print(parsear_veredicto(\'{"puntuacion": 4, "motivo": "correcta pero escueta"}\'))   # {\'puntuacion\': 4, ...}\n'
            "print(parsear_veredicto('{\"puntuacion\": 9}'))                        # None: la rubrica va de 1 a 5\n"
            "```\n"
            "\n"
            'Un veredicto ilegible **no es un 1**: es "no se pudo juzgar". Si lo cuentas como una mala nota, un fallo del juez parece un fallo del sistema. Y el juez tiene sesgos conocidos (prefiere respuestas largas, se deja convencer por el tono seguro): por eso no decide solo, se combina con las metricas deterministas.\n'
            "\n"
            "## Correr la evaluacion\n"
            "\n"
            "La evaluacion llama al sistema con cada pregunta, calcula las metricas, pide el veredicto y decide si el caso **aprueba**. Tanto el sistema como el juez se inyectan: en los tests son funciones falsas, en el editor serian el `responder` de AI 4 y `pycode.llm_complete`.\n"
            "\n"
            "```python\n"
            "CASOS = [{'id': 'envio', 'pregunta': 'envio gratis?', 'datos_clave': ['50 euros']},    # dos casos minimos\n"
            "         {'id': 'pago', 'pregunta': 'pagar con paypal?', 'datos_clave': ['paypal']}]\n"
            "\n"
            "async def sistema_falso(pregunta):                                    # el sistema que se evalua\n"
            "    if 'envio' in pregunta:\n"
            "        return 'El envio es gratis desde 50 euros.'                   # acierta\n"
            "    return 'Aceptamos tarjeta.'                                       # no menciona paypal\n"
            "\n"
            "async def evaluar_minimo(casos, sistema_fn):                          # version corta: solo datos clave\n"
            "    resultados = []\n"
            "    for caso in casos:                                                # uno a uno, en orden\n"
            "        respuesta = await sistema_fn(caso['pregunta'])                # el sistema contesta\n"
            "        ok = all(d in respuesta for d in caso['datos_clave'])         # ¿estan todos los datos?\n"
            "        resultados.append({'id': caso['id'], 'aprobado': ok})         # se guarda cada caso, no solo la media\n"
            "    tasa = sum(r['aprobado'] for r in resultados) / len(resultados)   # True cuenta 1, False 0\n"
            "    return {'casos': resultados, 'tasa_aprobados': tasa}\n"
            "\n"
            "print(await evaluar_minimo(CASOS, sistema_falso))\n"
            "# {'casos': [{'id': 'envio', 'aprobado': True}, {'id': 'pago', 'aprobado': False}], 'tasa_aprobados': 0.5}\n"
            "```\n"
            "\n"
            "Guarda **el resultado de cada caso**, no solo la media: un 80% no dice que caso fallo, y es lo primero que vas a querer mirar.\n"
            "\n"
            "## Comparar dos versiones\n"
            "\n"
            'La pregunta real no es "¿que nota saca?" sino "¿que se rompio respecto a la version anterior?". Se comparan los resultados caso por caso.\n'
            "\n"
            "```python\n"
            "antes = {'envio': True, 'pago': True, 'horario': False}              # version actual: id -> aprobado\n"
            "despues = {'envio': True, 'pago': False, 'horario': True}            # con el prompt nuevo\n"
            "\n"
            "comunes = sorted(set(antes) & set(despues))                           # solo se comparan los casos de ambas\n"
            "empeoran = [c for c in comunes if antes[c] and not despues[c]]        # aprobaba y ya no\n"
            "mejoran = [c for c in comunes if not antes[c] and despues[c]]         # fallaba y ahora aprueba\n"
            "print(empeoran, mejoran)                                              # ['pago'] ['horario']\n"
            "```\n"
            "\n"
            "Las dos versiones sacan 2 de 3, la misma nota, y sin embargo el cambio **rompio** el caso de pagos. Mirando solo la media lo habrias dado por bueno.\n"
            "\n"
            "## Errores comunes\n"
            "\n"
            '- **Comparar texto sin normalizar.** "50 Euros." y "50 euros" son el mismo dato, pero `\'50 euros\' in respuesta` dice que no. Normaliza mayusculas, tildes, signos y espacios en los dos lados.\n'
            '- **Contar un veredicto ilegible como mala nota.** Si el juez devuelve algo que no es JSON valido y lo tratas como un 1, un fallo del juez aparece como un fallo del sistema. Registralo aparte como "sin veredicto".\n'
            "- **Confiar solo en el LLM juez.** Prefiere respuestas largas y seguras aunque sean incorrectas. Combina su nota con metricas deterministas (datos clave, fuentes) que no se dejan impresionar.\n"
            "- **Mirar solo la media.** Dos versiones con la misma tasa pueden fallar casos distintos. Compara caso por caso y revisa los que empeoran.\n"
            "- **Evaluar con preguntas inventadas en el momento.** Si los casos cambian cada vez, las notas no se pueden comparar. Mantén un conjunto fijo y añade un caso por cada error real que arregles.\n"
            "\n"
            "## Resumen\n"
            "\n"
            "- **Conjunto de evaluacion**: casos fijos con datos clave y fuentes esperadas, no respuestas literales.\n"
            "- **Metricas deterministas**: normalizar y medir cobertura de datos y precision/recall de fuentes.\n"
            '- **LLM como juez**: rubrica explicita, veredicto JSON validado, y lo ilegible es "sin veredicto", no un 1.\n'
            "- **Evaluar**: sistema y juez inyectados, un resultado por caso y una tasa de aprobados.\n"
            "- **Comparar versiones**: que casos empeoran y cuales mejoran, no solo la media.\n"
        ),
        difficulty="intermediate",
        category="ai-fundamentos",
        order=43,
        track="track-5",
        estimated_duration=65,
        prerequisites_titles=["AI 5 · Agentes que usan herramientas"],
        exercises=[
            ExerciseTemplate(
                title="Normalizar texto para comparar",
                description="Minusculas, sin tildes, sin signos y con espacios simples.",
                instructions=(
                    "Implementa `normalizar(texto)` que devuelva el texto preparado para compararlo:\n"
                    "\n"
                    "- en minusculas y sin tildes;\n"
                    "- con los signos de puntuacion cambiados por espacios;\n"
                    "- con un solo espacio entre palabras y sin espacios en los bordes.\n"
                    "\n"
                    "Ejemplo: `normalizar('  El envío es GRATIS: desde 50€!  ')` → `'el envio es gratis desde 50'`"
                ),
                starter_code=(
                    "import re\n"
                    "import unicodedata\n"
                    "\n"
                    "\n"
                    "def normalizar(texto):\n"
                    "    # TODO: minusculas y sin tildes\n"
                    "    # TODO: signos -> espacios y un solo espacio entre palabras\n"
                    "    pass\n"
                ),
                hints=[
                    "unicodedata.normalize('NFD', t).encode('ascii', 'ignore').decode() quita tildes (y simbolos como €).",
                    "re.sub(r'[^\\w\\s]', ' ', t) cambia todo lo que no es letra, numero o espacio; ' '.join(t.split()) deja espacios simples.",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "minusculas, sin tildes ni signos",
                        "code": (
                            "assert normalizar('  El envío es GRATIS: desde 50€!  ') == 'el envio es gratis desde 50', repr(normalizar('  El envío es GRATIS: desde 50€!  '))\n"
                        ),
                    },
                    {
                        "name": "espacios simples y signos entre palabras",
                        "code": (
                            "assert normalizar('30\\tdias,devolucion') == '30 dias devolucion'\n"
                            "assert normalizar('') == ''\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Cobertura de datos clave",
                description="Que fraccion de los datos obligatorios aparece en la respuesta.",
                instructions=(
                    "Implementa `contiene_datos(respuesta, datos_clave)` que devuelva un `float` entre 0 y 1: la fraccion de `datos_clave` que aparecen en la respuesta, comparando ambos lados con `normalizar` (ya viene en el starter). Si `datos_clave` esta vacia, devuelve `1.0`.\n"
                    "\n"
                    "Ejemplo: `contiene_datos('Envío GRATIS desde 50  Euros.', ['50 euros', 'gratis', '24 horas'])` → `0.666...`"
                ),
                starter_code=(
                    "import re\n"
                    "import unicodedata\n"
                    "\n"
                    "\n"
                    "def normalizar(texto):\n"
                    "    sin_tildes = unicodedata.normalize('NFD', texto.lower()).encode('ascii', 'ignore').decode()\n"
                    "    return ' '.join(re.sub(r'[^\\w\\s]', ' ', sin_tildes).split())\n"
                    "\n"
                    "\n"
                    "def contiene_datos(respuesta, datos_clave):\n"
                    "    # TODO: sin datos clave -> 1.0\n"
                    "    # TODO: cuenta los datos (normalizados) que estan en la respuesta (normalizada)\n"
                    "    pass\n"
                ),
                hints=[
                    "Normaliza la respuesta una vez y cada dato antes de buscarlo con 'in'.",
                    "La fraccion es presentes / total: con 2 de 3 da 0.666...",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "fraccion de datos presentes",
                        "code": (
                            "c = contiene_datos('Envío GRATIS desde 50  Euros.', ['50 euros', 'gratis', '24 horas'])\n"
                            "assert abs(c - 2 / 3) < 1e-9, f'devolvio {c}'\n"
                            "assert contiene_datos('nada que ver', ['50 euros']) == 0.0\n"
                        ),
                    },
                    {
                        "name": "sin datos clave es cobertura completa",
                        "code": (
                            "assert contiene_datos('lo que sea', []) == 1.0\n"
                            "assert contiene_datos('Plazo: 30 días.', ['30 dias']) == 1.0\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Precision y recall de fuentes",
                description="Mide si el sistema cito lo que debia y nada mas.",
                instructions=(
                    "Implementa `puntuar_fuentes(citadas, esperadas)` que devuelva `{'precision': float, 'recall': float}` tratando las dos listas como conjuntos (los duplicados no cuentan):\n"
                    "\n"
                    "- `precision` = aciertos / fuentes citadas, o `0.0` si no cito ninguna;\n"
                    "- `recall` = aciertos / fuentes esperadas, o `1.0` si no se esperaba ninguna.\n"
                    "\n"
                    "Ejemplo: `puntuar_fuentes(['envios.md', 'pagos.md', 'envios.md'], ['envios.md', 'horario.md'])` → `{'precision': 0.5, 'recall': 0.5}`"
                ),
                starter_code=(
                    "def puntuar_fuentes(citadas, esperadas):\n"
                    "    # TODO: pasa ambas listas a conjuntos y cuenta los aciertos\n"
                    "    # TODO: precision y recall con sus casos vacios\n"
                    "    pass\n"
                ),
                hints=[
                    "set(a) & set(b) es la interseccion: las fuentes citadas que ademas se esperaban.",
                    "Sin citas no hay precision que medir: 0.0. Sin esperadas no falta nada: recall 1.0.",
                    "Los duplicados desaparecen al pasar a set: citar dos veces la misma no suma.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "precision y recall con duplicados",
                        "code": (
                            "r = puntuar_fuentes(['envios.md', 'pagos.md', 'envios.md'], ['envios.md', 'horario.md'])\n"
                            "assert r == {'precision': 0.5, 'recall': 0.5}, r\n"
                        ),
                    },
                    {
                        "name": "cito de mas o de menos",
                        "code": (
                            "assert puntuar_fuentes(['a', 'b', 'c', 'd'], ['a']) == {'precision': 0.25, 'recall': 1.0}\n"
                            "assert puntuar_fuentes(['a'], ['a', 'b']) == {'precision': 1.0, 'recall': 0.5}\n"
                        ),
                    },
                    {
                        "name": "casos vacios",
                        "code": (
                            "assert puntuar_fuentes([], ['a']) == {'precision': 0.0, 'recall': 0.0}\n"
                            "assert puntuar_fuentes(['a'], []) == {'precision': 0.0, 'recall': 1.0}\n"
                            "assert puntuar_fuentes([], []) == {'precision': 0.0, 'recall': 1.0}\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Leer el veredicto del juez",
                description="Valida el JSON del LLM juez contra la rubrica.",
                instructions=(
                    "Implementa `parsear_veredicto(texto)` que devuelva `{'puntuacion': int, 'motivo': str}` o `None` si el veredicto no es valido:\n"
                    "\n"
                    "- el JSON puede venir dentro de cercas ```` ```json ```` o ```` ``` ````;\n"
                    "- `puntuacion` tiene que ser un **entero** de 1 a 5 (ni `4.5`, ni `'4'`, ni `True`);\n"
                    "- `motivo` es opcional: si falta, `''`;\n"
                    "- JSON invalido, sin `puntuacion` o fuera de rango → `None`. Nunca lanza.\n"
                    "\n"
                    "Ejemplo: `parsear_veredicto('{\"puntuacion\": 4, \"motivo\": \"escueta\"}')` → `{'puntuacion': 4, 'motivo': 'escueta'}`"
                ),
                starter_code=(
                    "import json\n"
                    "\n"
                    "\n"
                    "def parsear_veredicto(texto):\n"
                    "    # TODO: quita las cercas si las hay y json.loads dentro de try/except\n"
                    "    # TODO: puntuacion entera entre 1 y 5 (cuidado: True tambien es int)\n"
                    "    # TODO: devuelve {'puntuacion': ..., 'motivo': ...} o None\n"
                    "    pass\n"
                ),
                hints=[
                    "Para las cercas: CERCA = '`' * 3; si CERCA in t, t = t.split(CERCA)[1].removeprefix('json').",
                    "isinstance(True, int) es True: usa type(p) is int para rechazar booleanos.",
                    "Comprueba que lo leido sea un dict antes de usar .get().",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "veredicto valido, con o sin cercas",
                        "code": (
                            "assert parsear_veredicto('{\"puntuacion\": 4, \"motivo\": \"escueta\"}') == {'puntuacion': 4, 'motivo': 'escueta'}\n"
                            "c = '`' * 3\n"
                            "assert parsear_veredicto(c + 'json\\n{\"puntuacion\": 5}\\n' + c) == {'puntuacion': 5, 'motivo': ''}\n"
                        ),
                    },
                    {
                        "name": "fuera de rango o de tipo equivocado",
                        "code": (
                            "for malo in ('{\"puntuacion\": 0}', '{\"puntuacion\": 6}', '{\"puntuacion\": 4.5}',\n"
                            '             \'{"puntuacion": "4"}\', \'{"puntuacion": true}\', \'{"motivo": "sin nota"}\'):\n'
                            "    assert parsear_veredicto(malo) is None, f'{malo} deberia ser None'\n"
                            "assert parsear_veredicto('{\"puntuacion\": 1}') == {'puntuacion': 1, 'motivo': ''}\n"
                        ),
                    },
                    {
                        "name": "texto que no es JSON: None sin lanzar",
                        "code": (
                            "assert parsear_veredicto('Le daria un 4') is None\n"
                            "assert parsear_veredicto('[4]') is None\n"
                            'assert parsear_veredicto(\'{"puntuacion": 3, "motivo": "ok"}\')[\'puntuacion\'] == 3\n'
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Comparar dos versiones",
                description="Encuentra los casos que se rompen o se arreglan con un cambio.",
                instructions=(
                    "Implementa `comparar_versiones(antes, despues)`: cada argumento es un diccionario `id_caso → aprobado (bool)`. Devuelve un diccionario con:\n"
                    "\n"
                    "- `'empeoran'`: ids que aprobaban antes y no despues, ordenados;\n"
                    "- `'mejoran'`: ids que no aprobaban antes y si despues, ordenados;\n"
                    "- `'solo_en_uno'`: ids que estan en una sola version, ordenados;\n"
                    "- `'tasa_antes'` y `'tasa_despues'`: fraccion de aprobados **sobre los casos comunes** (`0.0` si no hay comunes).\n"
                    "\n"
                    "Solo los casos que estan en las dos versiones se comparan y cuentan para las tasas."
                ),
                starter_code=(
                    "def comparar_versiones(antes, despues):\n"
                    "    # TODO: casos comunes y casos que solo estan en una version\n"
                    "    # TODO: empeoran / mejoran entre los comunes\n"
                    "    # TODO: tasas sobre los comunes\n"
                    "    pass\n"
                ),
                hints=[
                    "set(antes) & set(despues) son los comunes; el operador ^ da los que estan en uno solo.",
                    "Ordena las listas con sorted() para que el resultado sea estable.",
                    "sum(antes[c] for c in comunes) cuenta los True.",
                    "Con dos versiones que suspenden los mismos casos, empeoran y mejoran quedan vacias.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "la misma nota esconde una regresion",
                        "code": (
                            "r = comparar_versiones({'envio': True, 'pago': True, 'horario': False},\n"
                            "                       {'envio': True, 'pago': False, 'horario': True})\n"
                            "assert r['empeoran'] == ['pago'] and r['mejoran'] == ['horario'], r\n"
                            "assert abs(r['tasa_antes'] - 2 / 3) < 1e-9 and abs(r['tasa_despues'] - 2 / 3) < 1e-9, r\n"
                        ),
                    },
                    {
                        "name": "casos que solo estan en una version",
                        "code": (
                            "r = comparar_versiones({'a': True, 'b': False, 'viejo': True}, {'a': False, 'b': False, 'nuevo': True})\n"
                            "assert r['solo_en_uno'] == ['nuevo', 'viejo'], r\n"
                            "assert r['empeoran'] == ['a'] and r['mejoran'] == []\n"
                            "assert r['tasa_antes'] == 0.5 and r['tasa_despues'] == 0.0, 'las tasas solo cuentan los comunes'\n"
                        ),
                    },
                    {
                        "name": "listas ordenadas",
                        "code": (
                            "r = comparar_versiones({'z': True, 'm': True, 'a': True}, {'z': False, 'm': False, 'a': False})\n"
                            "assert r['empeoran'] == ['a', 'm', 'z'], r['empeoran']\n"
                        ),
                    },
                    {
                        "name": "sin casos comunes",
                        "code": (
                            "r = comparar_versiones({'a': True}, {'b': True})\n"
                            "assert r == {'empeoran': [], 'mejoran': [], 'solo_en_uno': ['a', 'b'], 'tasa_antes': 0.0, 'tasa_despues': 0.0}, r\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Correr la evaluacion completa",
                description="Metricas deterministas + LLM juez sobre todo el conjunto de casos.",
                instructions=(
                    "Implementa `async def evaluar(casos, sistema_fn, juez_fn, nota_minima=4)`. Cada caso tiene `'id'`, `'pregunta'`, `'datos_clave'` y `'fuentes_esperadas'`. `sistema_fn(pregunta)` devuelve `{'respuesta': str, 'fuentes': list}` y `juez_fn(prompt)` devuelve el texto del juez; las dos son asincronas.\n"
                    "\n"
                    "Para cada caso, **en orden**:\n"
                    "\n"
                    "1. `resultado = await sistema_fn(caso['pregunta'])`.\n"
                    "2. `cobertura` con `contiene_datos` y `recall` con `puntuar_fuentes` (su clave `'recall'`).\n"
                    "3. `veredicto = parsear_veredicto(await juez_fn(prompt_juez(pregunta, respuesta)))`.\n"
                    "4. Aprueba si `cobertura == 1.0`, `recall == 1.0` y hay veredicto con `puntuacion >= nota_minima`.\n"
                    "\n"
                    "Devuelve:\n"
                    "\n"
                    "```\n"
                    "{\n"
                    "    'casos': [{'id', 'aprobado', 'cobertura', 'recall', 'puntuacion'}, ...],  # puntuacion None si no hubo veredicto\n"
                    "    'tasa_aprobados': float,     # 0.0 si no hay casos\n"
                    "    'sin_veredicto': [ids],      # en el orden de los casos\n"
                    "}\n"
                    "```\n"
                    "\n"
                    "El starter trae `normalizar`, `contiene_datos`, `puntuar_fuentes`, `parsear_veredicto` y `prompt_juez`."
                ),
                starter_code=(
                    "import json\n"
                    "import re\n"
                    "import unicodedata\n"
                    "\n"
                    "CERCA = '`' * 3\n"
                    "\n"
                    "\n"
                    "def normalizar(texto):\n"
                    "    sin_tildes = unicodedata.normalize('NFD', texto.lower()).encode('ascii', 'ignore').decode()\n"
                    "    return ' '.join(re.sub(r'[^\\w\\s]', ' ', sin_tildes).split())\n"
                    "\n"
                    "\n"
                    "def contiene_datos(respuesta, datos_clave):\n"
                    "    if not datos_clave:\n"
                    "        return 1.0\n"
                    "    texto = normalizar(respuesta)\n"
                    "    return sum(normalizar(d) in texto for d in datos_clave) / len(datos_clave)\n"
                    "\n"
                    "\n"
                    "def puntuar_fuentes(citadas, esperadas):\n"
                    "    citadas, esperadas = set(citadas), set(esperadas)\n"
                    "    aciertos = len(citadas & esperadas)\n"
                    "    return {\n"
                    "        'precision': aciertos / len(citadas) if citadas else 0.0,\n"
                    "        'recall': aciertos / len(esperadas) if esperadas else 1.0,\n"
                    "    }\n"
                    "\n"
                    "\n"
                    "def parsear_veredicto(texto):\n"
                    "    t = texto.strip()\n"
                    "    if CERCA in t:\n"
                    "        t = t.split(CERCA)[1].removeprefix('json').strip()\n"
                    "    try:\n"
                    "        datos = json.loads(t)\n"
                    "    except json.JSONDecodeError:\n"
                    "        return None\n"
                    "    if not isinstance(datos, dict):\n"
                    "        return None\n"
                    "    puntos = datos.get('puntuacion')\n"
                    "    if type(puntos) is not int or not 1 <= puntos <= 5:\n"
                    "        return None\n"
                    "    return {'puntuacion': puntos, 'motivo': str(datos.get('motivo', ''))}\n"
                    "\n"
                    "\n"
                    "def prompt_juez(pregunta, respuesta):\n"
                    "    return (\n"
                    "        'Evalua la respuesta de un asistente de atencion al cliente.\\n'\n"
                    "        'Puntua de 1 a 5: 5 = correcta, completa y clara; 1 = incorrecta o no contesta.\\n'\n"
                    '        \'Responde SOLO con JSON: {"puntuacion": entero, "motivo": texto breve}.\\n\\n\'\n'
                    "        f'Pregunta: {pregunta}\\nRespuesta: {respuesta}'\n"
                    "    )\n"
                    "\n"
                    "\n"
                    "async def evaluar(casos, sistema_fn, juez_fn, nota_minima=4):\n"
                    "    # TODO: para cada caso: sistema -> metricas -> juez -> aprobado\n"
                    "    # TODO: guarda un dict por caso y los ids sin veredicto\n"
                    "    # TODO: tasa de aprobados (0.0 si no hay casos)\n"
                    "    pass\n"
                ),
                hints=[
                    "Un veredicto None no aprueba, y su id va a sin_veredicto: no es lo mismo que una nota baja.",
                    "La puntuacion del caso es veredicto['puntuacion'] o None si no hubo veredicto.",
                    "sum(c['aprobado'] for c in resultados) cuenta los aprobados.",
                    "Para probarlo: resumen = await evaluar(casos, sistema_falso, juez_falso).",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "combina metricas y juez por caso",
                        "code": (
                            "casos = [\n"
                            "    {'id': 'envio', 'pregunta': 'envio gratis?', 'datos_clave': ['50 euros'], 'fuentes_esperadas': ['envios.md']},\n"
                            "    {'id': 'pago', 'pregunta': 'paypal?', 'datos_clave': ['paypal'], 'fuentes_esperadas': ['pagos.md']},\n"
                            "]\n"
                            "async def sistema(pregunta):\n"
                            "    if 'envio' in pregunta:\n"
                            "        return {'respuesta': 'Gratis desde 50 Euros.', 'fuentes': ['envios.md']}\n"
                            "    return {'respuesta': 'Aceptamos tarjeta.', 'fuentes': ['pagos.md']}\n"
                            "async def juez(prompt):\n"
                            '    return \'{"puntuacion": 5, "motivo": "ok"}\'\n'
                            "r = await evaluar(casos, sistema, juez)\n"
                            "assert [c['id'] for c in r['casos']] == ['envio', 'pago'], 'en el orden de los casos'\n"
                            "envio, pago = r['casos']\n"
                            "assert envio == {'id': 'envio', 'aprobado': True, 'cobertura': 1.0, 'recall': 1.0, 'puntuacion': 5}, envio\n"
                            "assert pago['aprobado'] is False and pago['cobertura'] == 0.0, 'sin el dato clave no aprueba aunque el juez de un 5'\n"
                            "assert r['tasa_aprobados'] == 0.5 and r['sin_veredicto'] == []\n"
                        ),
                    },
                    {
                        "name": "el juez recibe pregunta y respuesta",
                        "code": (
                            "prompts = []\n"
                            "async def sistema(pregunta):\n"
                            "    return {'respuesta': 'Abrimos de 9 a 18.', 'fuentes': ['horario.md']}\n"
                            "async def juez(prompt):\n"
                            "    prompts.append(prompt)\n"
                            "    return '{\"puntuacion\": 3}'\n"
                            "casos = [{'id': 'h', 'pregunta': 'a que hora abren', 'datos_clave': ['9'], 'fuentes_esperadas': ['horario.md']}]\n"
                            "r = await evaluar(casos, sistema, juez)\n"
                            "assert len(prompts) == 1 and 'a que hora abren' in prompts[0] and 'Abrimos de 9 a 18.' in prompts[0], prompts\n"
                            "assert r['casos'][0]['puntuacion'] == 3 and r['casos'][0]['aprobado'] is False, 'un 3 no llega a la nota minima de 4'\n"
                            "r2 = await evaluar(casos, sistema, juez, nota_minima=3)\n"
                            "assert r2['casos'][0]['aprobado'] is True\n"
                        ),
                    },
                    {
                        "name": "un veredicto ilegible es sin veredicto, no una mala nota",
                        "code": (
                            "async def sistema(pregunta):\n"
                            "    return {'respuesta': 'Gratis desde 50 euros', 'fuentes': ['envios.md']}\n"
                            "async def juez(prompt):\n"
                            "    return 'Le pondria un cinco'\n"
                            "casos = [{'id': 'e', 'pregunta': 'envio?', 'datos_clave': ['50 euros'], 'fuentes_esperadas': ['envios.md']}]\n"
                            "r = await evaluar(casos, sistema, juez)\n"
                            "assert r['sin_veredicto'] == ['e'], r\n"
                            "assert r['casos'][0]['puntuacion'] is None and r['casos'][0]['aprobado'] is False\n"
                            "assert r['casos'][0]['cobertura'] == 1.0, 'las metricas deterministas se calculan igual'\n"
                        ),
                    },
                    {
                        "name": "recall de fuentes y conjunto vacio",
                        "code": (
                            "async def sistema(pregunta):\n"
                            "    return {'respuesta': 'Gratis desde 50 euros', 'fuentes': []}\n"
                            "async def juez(prompt):\n"
                            "    return '{\"puntuacion\": 5}'\n"
                            "casos = [{'id': 'e', 'pregunta': 'envio?', 'datos_clave': ['50 euros'], 'fuentes_esperadas': ['envios.md']}]\n"
                            "r = await evaluar(casos, sistema, juez)\n"
                            "assert r['casos'][0]['recall'] == 0.0 and r['casos'][0]['aprobado'] is False, 'sin citar la fuente no aprueba'\n"
                            "vacio = await evaluar([], sistema, juez)\n"
                            "assert vacio == {'casos': [], 'tasa_aprobados': 0.0, 'sin_veredicto': []}, vacio\n"
                        ),
                    },
                ],
            ),
        ],
    ),
    LessonTemplate(
        title="MLOps 1 · Reproducibilidad: semillas, huellas y manifiestos",
        description=(
            "Repetir un experimento y explicar por que cambio un resultado: semillas, "
            "division train/test reproducible, huellas SHA-256 de datos y configuracion "
            "en formato canonico y un manifiesto con el entorno y las metricas."
        ),
        content=(
            "# MLOps 1: reproducibilidad\n"
            "\n"
            "En los Tracks 3 y 4 entrenaste modelos que funcionaban en tu editor. Llevarlos a produccion empieza por una pregunta incomoda: **¿podrias volver a obtener exactamente el mismo modelo?** Esta leccion construye las piezas que lo hacen posible: semillas, huellas de los datos y de la configuracion, y un manifiesto que acompana a cada experimento.\n"
            "\n"
            "## Por que la reproducibilidad va primero\n"
            "\n"
            'Nebula entrena un modelo que predice que pedidos se van a devolver. El martes daba 0.91 de accuracy; hoy, con "el mismo codigo", da 0.87. ¿Que cambio? Pudo ser:\n'
            "\n"
            "1. **Los datos.** Alguien anadio los pedidos de ayer, o corrigio una columna.\n"
            "2. **La configuracion.** Un `max_depth` de 4 paso a 5 en una rama que ya nadie recuerda.\n"
            "3. **El azar.** La division train/test o la inicializacion salieron distintas.\n"
            "4. **El entorno.** Se actualizo numpy o scikit-learn.\n"
            "\n"
            "Si no guardaste cual de las cuatro era, no hay forma de saberlo: solo queda volver a probar a ciegas. Al terminar tendras una funcion que ejecuta un experimento y devuelve un **manifiesto** con todo lo necesario para repetirlo y para explicar por que dos resultados difieren.\n"
            "\n"
            "## Semillas: el azar bajo control\n"
            "\n"
            "Los ordenadores no generan azar de verdad: generan secuencias que *parecen* aleatorias a partir de un numero inicial, la **semilla**. Misma semilla, misma secuencia.\n"
            "\n"
            "```python\n"
            "import random                                             # azar de la libreria estandar\n"
            "\n"
            "azar = random.Random(42)                                  # un generador propio, con semilla 42\n"
            "print([azar.randint(1, 100) for _ in range(3)])           # [82, 15, 4]\n"
            "\n"
            "otro = random.Random(42)                                  # otro generador con la misma semilla\n"
            "print([otro.randint(1, 100) for _ in range(3)])           # [82, 15, 4]: la secuencia se repite\n"
            "\n"
            "print(random.Random(7).randint(1, 100))                   # 42: otra semilla, otra secuencia\n"
            "```\n"
            "\n"
            "Fijate en que se crea un **generador propio** con `random.Random(semilla)` en vez de llamar a `random.seed(42)`. La version global la comparte todo el programa: si otra funcion saca un numero al azar antes que tu, tu secuencia se desplaza y el resultado cambia sin que hayas tocado nada. numpy sigue la misma idea:\n"
            "\n"
            "```python\n"
            "import numpy as np                                         # numpy trae su propio generador\n"
            "\n"
            "rng = np.random.default_rng(0)                             # generador con semilla 0\n"
            "print(rng.integers(0, 10, size=3))                         # [8 6 5]\n"
            "print(np.random.default_rng(0).integers(0, 10, size=3))    # [8 6 5]: misma semilla, mismos numeros\n"
            "```\n"
            "\n"
            "## Dividir en train y test siempre igual\n"
            "\n"
            "La division train/test es el azar que mas afecta a una metrica: con pocos datos, dos divisiones distintas pueden dar varios puntos de diferencia. Hacerla reproducible es una funcion de cinco lineas.\n"
            "\n"
            "```python\n"
            "import random                                                  # para barajar con semilla\n"
            "\n"
            "def dividir(filas, fraccion_test, semilla):\n"
            "    copia = list(filas)                                        # no desordenar la lista de quien llama\n"
            "    random.Random(semilla).shuffle(copia)                      # barajar siempre igual con la misma semilla\n"
            "    n_test = round(len(copia) * fraccion_test)                 # cuantas filas van a test\n"
            "    return copia[n_test:], copia[:n_test]                      # (train, test)\n"
            "\n"
            "pedidos = list(range(10))                                      # 10 pedidos de ejemplo\n"
            "train, test = dividir(pedidos, 0.3, semilla=1)                 # 7 para entrenar, 3 para evaluar\n"
            "print(test)                                                    # [6, 8, 9]\n"
            "print(dividir(pedidos, 0.3, semilla=1)[1] == test)             # True: la division se repite\n"
            "print(dividir(pedidos, 0.3, semilla=2)[1])                     # [5, 9, 3]: otra semilla, otra division\n"
            "print(pedidos)                                                 # [0, 1, ..., 9]: el original sigue intacto\n"
            "```\n"
            "\n"
            "`shuffle` desordena la lista **en el sitio**. Sin la copia, la funcion alteraria los datos de quien la llama, y la siguiente division partiria de un orden distinto.\n"
            "\n"
            "## Huella de los datos con hashlib\n"
            "\n"
            "Guardar una copia de los datos en cada experimento no escala. Lo que se guarda es su **huella**: un resumen corto que cambia en cuanto cambia un solo byte. `hashlib` calcula huellas criptograficas como SHA-256.\n"
            "\n"
            "```python\n"
            "import hashlib                                                         # huellas criptograficas\n"
            "\n"
            "texto = 'pedido,importe\\n1001,25.5\\n'                                  # un CSV pequeno\n"
            "huella = hashlib.sha256(texto.encode('utf-8')).hexdigest()             # texto -> bytes -> 64 caracteres hex\n"
            "print(huella[:12])                                                     # bb1e500a95ba: con un prefijo basta\n"
            "cambiado = texto.replace('25.5', '25.6')                               # un solo digito distinto\n"
            "print(hashlib.sha256(cambiado.encode('utf-8')).hexdigest()[:12])       # 934d58ae2e70: nada que ver\n"
            "```\n"
            "\n"
            "`sha256` trabaja con **bytes**, no con texto: por eso el `.encode('utf-8')`. Doce caracteres hexadecimales son 48 bits: sobra para distinguir las versiones de un conjunto de datos.\n"
            "\n"
            "## Filas en formato canonico\n"
            "\n"
            "Los datos casi nunca llegan como un texto fijo: son filas (diccionarios) que alguien construyo. El mismo contenido se puede escribir de varias formas, y la huella tiene que ser la misma en todas. Para eso se pasa cada fila a un **formato canonico** con `json.dumps(..., sort_keys=True)`.\n"
            "\n"
            "```python\n"
            "import hashlib                                                          # huellas\n"
            "import json                                                             # serializar de forma estable\n"
            "\n"
            "def huella(texto, n=12):\n"
            "    return hashlib.sha256(texto.encode('utf-8')).hexdigest()[:n]        # prefijo de n caracteres\n"
            "\n"
            "a = {'pedido': 1001, 'importe': 25.5}                                   # una fila...\n"
            "b = {'importe': 25.5, 'pedido': 1001}                                   # ...la misma, con las claves en otro orden\n"
            "print(str(a) == str(b))                                                 # False: str respeta el orden de insercion\n"
            'print(json.dumps(a, sort_keys=True))                                    # {"importe": 25.5, "pedido": 1001}\n'
            "print(huella(json.dumps(a, sort_keys=True)) == huella(json.dumps(b, sort_keys=True)))  # True\n"
            "\n"
            "filas = [{'id': 2}, {'id': 1}]                                          # dos filas en un orden\n"
            "huellas = [huella(json.dumps(f, sort_keys=True)) for f in filas]        # una huella por fila\n"
            "invertidas = list(reversed(huellas))                                    # las mismas filas al reves\n"
            "print(huella(''.join(huellas)) == huella(''.join(invertidas)))          # False: el orden de las filas cuenta\n"
            "print(huella(''.join(sorted(huellas))) == huella(''.join(sorted(invertidas))))  # True: ordenadas, deja de contar\n"
            "```\n"
            "\n"
            "Que el orden de las filas cuente o no es una **decision**: en una serie temporal importa; en una tabla de pedidos que se lee de una base de datos sin `ORDER BY`, no deberia, o cada consulta daria una huella distinta.\n"
            "\n"
            "## Huella de la configuracion\n"
            "\n"
            "Con la configuracion pasa lo mismo que con las filas: un diccionario de hiperparametros tiene que dar la misma huella escriba quien lo escriba. Se anade `separators=(',', ':')` para que ni los espacios de `json.dumps` formen parte de lo que se compara.\n"
            "\n"
            "```python\n"
            "import hashlib                                                               # huellas\n"
            "import json                                                                  # formato canonico\n"
            "\n"
            "def huella_config(config):\n"
            "    canonico = json.dumps(config, sort_keys=True, separators=(',', ':'))     # claves ordenadas, sin espacios\n"
            "    return hashlib.sha256(canonico.encode('utf-8')).hexdigest()[:12]         # 12 caracteres\n"
            "\n"
            "base = {'modelo': 'arbol', 'max_depth': 4, 'fraccion_test': 0.2}             # la configuracion del martes\n"
            "print(huella_config(base))                                                   # ad387d8b5a04\n"
            "reordenada = {'fraccion_test': 0.2, 'max_depth': 4, 'modelo': 'arbol'}       # mismos valores, otro orden\n"
            "print(huella_config(reordenada) == huella_config(base))                      # True\n"
            "print(huella_config(dict(base, max_depth=5)) == huella_config(base))         # False: cambio un hiperparametro\n"
            "print(json.dumps(4), json.dumps(4.0))                                        # 4 4.0: para la huella no son iguales\n"
            "```\n"
            "\n"
            "La ultima linea es un aviso: `4` y `4.0` valen lo mismo en Python, pero se escriben distinto y dan huellas distintas. Decide un tipo por hiperparametro y mantenlo.\n"
            "\n"
            "## El entorno y el manifiesto\n"
            "\n"
            "El ultimo sospechoso es el entorno: la version de Python y de cada libreria. Se anota en un diccionario y, junto con todo lo anterior, forma el **manifiesto** del experimento.\n"
            "\n"
            "```python\n"
            "import json                                                    # el manifiesto se guarda como JSON\n"
            "import sys                                                     # version de Python\n"
            "import numpy as np                                             # una libreria cuya version importa\n"
            "\n"
            "entorno = {\n"
            "    'python': f'{sys.version_info.major}.{sys.version_info.minor}',  # p. ej. '3.12'\n"
            "    'numpy': np.__version__,                                   # la version exacta instalada\n"
            "}\n"
            "manifiesto = {\n"
            "    'datos': {'huella': 'bb1e500a95ba', 'filas': 1200},        # que datos exactamente\n"
            "    'config': {'huella': 'ad387d8b5a04', 'valores': {'max_depth': 4}},  # con que configuracion\n"
            "    'semilla': 42,                                             # con que azar\n"
            "    'entorno': entorno,                                        # con que librerias\n"
            "    'metricas': {'accuracy': 0.91},                            # y que salio\n"
            "}\n"
            "texto = json.dumps(manifiesto, sort_keys=True, indent=2)       # se guarda junto al modelo entrenado\n"
            "print(json.loads(texto) == manifiesto)                         # True: ida y vuelta sin perder nada\n"
            "\n"
            "antes = {'datos': 'bb1e500a95ba', 'config': 'ad387d8b5a04', 'semilla': 42}   # el martes\n"
            "hoy = {'datos': '934d58ae2e70', 'config': 'ad387d8b5a04', 'semilla': 42}     # hoy\n"
            "print([k for k in ('datos', 'config', 'semilla') if antes[k] != hoy[k]])     # ['datos']: cambiaron los datos\n"
            "```\n"
            "\n"
            "Con dos manifiestos, la pregunta del principio tiene respuesta en una linea: la metrica bajo porque **cambiaron los datos**, no el codigo ni el azar. Las metricas van en el manifiesto pero no identifican el experimento: son su resultado, no su receta.\n"
            "\n"
            "## Errores comunes\n"
            "\n"
            '- **Usar `hash()` para las huellas.** El `hash` de un texto cambia en cada ejecucion de Python (se aleatoriza por seguridad), asi que la "huella" de hoy no coincide con la de manana. Usa `hashlib.sha256`, que da siempre lo mismo en cualquier maquina.\n'
            "- **Fijar la semilla global con `random.seed` y creer que basta.** Cualquier otra llamada a `random` en el programa consume numeros de esa misma secuencia y desplaza la tuya. Crea un generador propio, `random.Random(semilla)` o `np.random.default_rng(semilla)`, y pasalo a quien lo necesite.\n"
            "- **Hashear `str(diccionario)` o `json.dumps` sin `sort_keys`.** El mismo contenido con las claves en otro orden da otra huella, y dos experimentos identicos parecen distintos. Pasa siempre por el formato canonico.\n"
            "- **Barajar la lista original.** `random.shuffle(filas)` desordena los datos de quien llamo a la funcion, y la siguiente division ya no parte del mismo orden. Baraja una copia: `copia = list(filas)`.\n"
            '- **Guardar solo la metrica.** "accuracy 0.91" sin datos, configuracion, semilla y entorno no se puede repetir ni comparar. El manifiesto entero se guarda con el modelo.\n'
            "\n"
            "## Resumen\n"
            "\n"
            "- **Semillas**: `random.Random(semilla)` y `np.random.default_rng(semilla)` dan secuencias repetibles sin depender del estado global.\n"
            "- **Division reproducible**: copiar, barajar con semilla y cortar; misma semilla, mismos conjuntos, y el original intacto.\n"
            "- **Huella con hashlib**: `hashlib.sha256(texto.encode('utf-8')).hexdigest()[:12]` resume cualquier contenido y cambia con un solo byte.\n"
            "- **Formato canonico**: `json.dumps(fila, sort_keys=True)` para que el orden de las claves no cambie la huella; ordenar las huellas de las filas si su orden no debe contar.\n"
            "- **Huella de la configuracion**: el mismo formato canonico con `separators=(',', ':')`; cuidado con `4` frente a `4.0`.\n"
            "- **Manifiesto**: datos, configuracion, semilla, entorno y metricas en un JSON junto al modelo; comparando dos se explica por que cambio un resultado.\n"
        ),
        difficulty="intermediate",
        category="mlops",
        order=44,
        track="track-6",
        estimated_duration=60,
        prerequisites_titles=["AI 6 · Evaluar sistemas con LLM"],
        exercises=[
            ExerciseTemplate(
                title="Huella de un texto",
                description="Un prefijo de SHA-256 que identifica un contenido.",
                instructions=(
                    "Implementa `huella(texto, n=12)` que devuelva los primeros `n` caracteres del SHA-256 hexadecimal del texto codificado en UTF-8.\n"
                    "\n"
                    "Ejemplos:\n"
                    "\n"
                    "- `huella('hola')` → `'b221d9dbb083'`\n"
                    "- `huella('hola', n=6)` → `'b221d9'`\n"
                    "- `huella('Hola')` → `'e633f4fc79ba'` (una mayuscula lo cambia todo)"
                ),
                starter_code=(
                    "import hashlib\n"
                    "\n"
                    "\n"
                    "def huella(texto, n=12):\n"
                    "    # TODO: texto -> bytes UTF-8 -> sha256 -> hexdigest -> primeros n caracteres\n"
                    "    pass\n"
                ),
                hints=[
                    "hashlib.sha256 necesita bytes: texto.encode('utf-8').",
                    "hashlib.sha256(datos).hexdigest() devuelve un str de 64 caracteres; corta con [:n].",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "valores conocidos",
                        "code": (
                            "assert huella('hola') == 'b221d9dbb083', huella('hola')\n"
                            "assert huella('Hola') == 'e633f4fc79ba', huella('Hola')\n"
                        ),
                    },
                    {
                        "name": "respeta n y funciona con tildes",
                        "code": (
                            "assert huella('hola', n=6) == 'b221d9', huella('hola', n=6)\n"
                            "h = huella('envío', n=64)\n"
                            "import hashlib\n"
                            "assert h == hashlib.sha256('envío'.encode('utf-8')).hexdigest(), h\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Dividir con semilla",
                description="La misma semilla da siempre los mismos conjuntos de train y test.",
                instructions=(
                    "Implementa `dividir(filas, fraccion_test, semilla)` que devuelva la tupla `(train, test)`:\n"
                    "\n"
                    "1. Haz una **copia** de `filas` (la lista original no se puede modificar).\n"
                    "2. Barajala con `random.Random(semilla).shuffle(...)`.\n"
                    "3. `n_test = round(len(filas) * fraccion_test)`; `test` son las primeras `n_test` filas de la copia barajada y `train` el resto.\n"
                    "\n"
                    "Ejemplo: `dividir(list(range(10)), 0.3, 1)` → `([7, 5, 3, 0, 4, 1, 2], [6, 8, 9])`"
                ),
                starter_code=(
                    "import random\n"
                    "\n"
                    "\n"
                    "def dividir(filas, fraccion_test, semilla):\n"
                    "    # TODO: copiar, barajar con un generador propio y cortar\n"
                    "    pass\n"
                ),
                hints=[
                    "copia = list(filas) crea una lista nueva; random.Random(semilla).shuffle(copia) la baraja en el sitio.",
                    "Con n_test = round(len(copia) * fraccion_test): return copia[n_test:], copia[:n_test].",
                ],
                difficulty="easy",
                points=10,
                hidden_tests=[
                    {
                        "name": "division exacta y repetible",
                        "code": (
                            "r = dividir(list(range(10)), 0.3, 1)\n"
                            "assert tuple(r) == ([7, 5, 3, 0, 4, 1, 2], [6, 8, 9]), r\n"
                            "assert tuple(dividir(list(range(10)), 0.3, 1)) == tuple(r)\n"
                            "assert tuple(dividir(list(range(10)), 0.3, 2)) == ([4, 6, 7, 2, 8, 1, 0], [5, 9, 3])\n"
                        ),
                    },
                    {
                        "name": "no modifica el original y no pierde filas",
                        "code": (
                            "filas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']\n"
                            "train, test = dividir(filas, 0.25, 7)\n"
                            "assert filas == ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'], filas\n"
                            "assert len(test) == 2 and len(train) == 6, (train, test)\n"
                            "assert sorted(train + test) == filas\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Huella de una configuracion",
                description="Mismos hiperparametros, misma huella, en cualquier orden.",
                instructions=(
                    "Implementa `huella_config(config)` que devuelva los primeros 12 caracteres del SHA-256 de la configuracion en formato canonico: `json.dumps(config, sort_keys=True, separators=(',', ':'))`, codificado en UTF-8.\n"
                    "\n"
                    "- El orden de las claves no puede cambiar la huella, tampoco en diccionarios anidados.\n"
                    "- Cualquier cambio de valor si la cambia.\n"
                    "\n"
                    "Ejemplo: `huella_config({'modelo': 'arbol', 'max_depth': 4, 'fraccion_test': 0.2})` → `'ad387d8b5a04'`"
                ),
                starter_code=(
                    "import hashlib\n"
                    "import json\n"
                    "\n"
                    "\n"
                    "def huella_config(config):\n"
                    "    # TODO: formato canonico con json.dumps y huella de 12 caracteres\n"
                    "    pass\n"
                ),
                hints=[
                    "sort_keys=True ordena las claves en todos los niveles, tambien en los diccionarios anidados.",
                    "separators=(',', ':') quita los espacios que json.dumps pone por defecto.",
                    "return hashlib.sha256(canonico.encode('utf-8')).hexdigest()[:12]",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "valor conocido",
                        "code": (
                            "h = huella_config({'modelo': 'arbol', 'max_depth': 4, 'fraccion_test': 0.2})\n"
                            "assert h == 'ad387d8b5a04', h\n"
                        ),
                    },
                    {
                        "name": "el orden de las claves no importa, tampoco anidado",
                        "code": (
                            "a = {'modelo': 'arbol', 'params': {'max_depth': 4, 'min_samples': 2}, 'semilla': 1}\n"
                            "b = {'semilla': 1, 'params': {'min_samples': 2, 'max_depth': 4}, 'modelo': 'arbol'}\n"
                            "assert isinstance(huella_config(a), str) and len(huella_config(a)) == 12, huella_config(a)\n"
                            "assert huella_config(a) == huella_config(b)\n"
                        ),
                    },
                    {
                        "name": "cualquier cambio de valor cambia la huella",
                        "code": (
                            "base = {'modelo': 'arbol', 'params': {'max_depth': 4}}\n"
                            "h = huella_config(base)\n"
                            "assert isinstance(h, str) and len(h) == 12, h\n"
                            "assert huella_config({'modelo': 'arbol', 'params': {'max_depth': 5}}) != h\n"
                            "assert huella_config({'modelo': 'bosque', 'params': {'max_depth': 4}}) != h\n"
                            "assert huella_config({'modelo': 'arbol', 'params': {'max_depth': 4.0}}) != h\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Huella de un conjunto de datos",
                description="Una huella por fila, combinadas, con o sin importar el orden.",
                instructions=(
                    "Implementa `huella_datos(filas, ignorar_orden=False)` para una lista de filas (diccionarios). Devuelve un `str` de 12 caracteres que:\n"
                    "\n"
                    "- no cambia si una fila tiene sus claves en otro orden;\n"
                    "- cambia si cambia cualquier valor, o si se anade o se quita una fila (**tambien una repetida**);\n"
                    "- con `ignorar_orden=False` cambia si las filas cambian de orden; con `ignorar_orden=True`, no.\n"
                    "\n"
                    "Usa `huella` (ya viene en el starter): una huella por fila con `json.dumps(fila, sort_keys=True)`, unelas en un solo texto (ordenadas si `ignorar_orden`) y devuelve la huella de ese texto."
                ),
                starter_code=(
                    "import hashlib\n"
                    "import json\n"
                    "\n"
                    "\n"
                    "def huella(texto, n=12):\n"
                    "    return hashlib.sha256(texto.encode('utf-8')).hexdigest()[:n]\n"
                    "\n"
                    "\n"
                    "def huella_datos(filas, ignorar_orden=False):\n"
                    "    # TODO: una huella por fila en formato canonico\n"
                    "    # TODO: si ignorar_orden, ordenarlas; unirlas y devolver la huella del conjunto\n"
                    "    pass\n"
                ),
                hints=[
                    "huellas = [huella(json.dumps(fila, sort_keys=True)) for fila in filas]",
                    "Un set perderia las filas repetidas: ordena con sorted(huellas), no conviertas en set.",
                    "return huella(''.join(huellas)) despues de ordenar o no segun ignorar_orden.",
                ],
                difficulty="medium",
                points=15,
                hidden_tests=[
                    {
                        "name": "claves en otro orden, misma huella",
                        "code": (
                            "a = [{'pedido': 1, 'importe': 10.0}, {'pedido': 2, 'importe': 5.5}]\n"
                            "b = [{'importe': 10.0, 'pedido': 1}, {'importe': 5.5, 'pedido': 2}]\n"
                            "h = huella_datos(a)\n"
                            "assert isinstance(h, str) and len(h) == 12, h\n"
                            "assert huella_datos(b) == h\n"
                        ),
                    },
                    {
                        "name": "el orden de las filas segun ignorar_orden",
                        "code": (
                            "a = [{'pedido': 1}, {'pedido': 2}, {'pedido': 3}]\n"
                            "b = [{'pedido': 3}, {'pedido': 1}, {'pedido': 2}]\n"
                            "assert isinstance(huella_datos(a), str) and len(huella_datos(a)) == 12\n"
                            "assert huella_datos(a) != huella_datos(b)\n"
                            "assert huella_datos(a, ignorar_orden=True) == huella_datos(b, ignorar_orden=True)\n"
                        ),
                    },
                    {
                        "name": "valores y filas repetidas cuentan",
                        "code": (
                            "a = [{'pedido': 1}, {'pedido': 2}]\n"
                            "h = huella_datos(a, ignorar_orden=True)\n"
                            "assert isinstance(h, str) and len(h) == 12, h\n"
                            "assert huella_datos([{'pedido': 1}, {'pedido': 9}], ignorar_orden=True) != h\n"
                            "assert huella_datos([{'pedido': 1}, {'pedido': 2}, {'pedido': 2}], ignorar_orden=True) != h\n"
                            "assert huella_datos([{'pedido': 1}], ignorar_orden=True) != h\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Explicar por que cambio un resultado",
                description="Comparar dos manifiestos y listar las causas posibles.",
                instructions=(
                    "Un manifiesto tiene esta forma:\n"
                    "\n"
                    "```\n"
                    "{'datos': {'huella': ..., 'filas': ...}, 'config': {'huella': ..., 'valores': {...}},\n"
                    " 'semilla': ..., 'entorno': {'python': '3.12', 'numpy': '2.0.2', ...}, 'metricas': {...}}\n"
                    "```\n"
                    "\n"
                    "Implementa `diferencias(antes, despues)` que devuelva una **lista de textos** con lo que cambio, en este orden:\n"
                    "\n"
                    "1. `'datos'` si cambio la huella de los datos;\n"
                    "2. `'config'` si cambio la huella de la configuracion;\n"
                    "3. `'semilla'` si cambio la semilla;\n"
                    "4. una entrada `'entorno: <paquete> <antes> -> <despues>'` por cada paquete con otra version, en orden alfabetico de paquete. Si un paquete falta en uno de los dos, su version se escribe `ausente`.\n"
                    "\n"
                    "Las `metricas` no son una causa: no aparecen nunca. Si no cambio nada, devuelve `[]`.\n"
                    "\n"
                    "Ejemplo: `['datos', 'entorno: numpy 1.26.4 -> 2.0.2', 'entorno: sklearn ausente -> 1.5.0']`"
                ),
                starter_code=(
                    "def diferencias(antes, despues):\n"
                    "    cambios = []\n"
                    "    # TODO: 'datos', 'config' y 'semilla', en ese orden\n"
                    "    # TODO: paquetes del entorno (union de claves, orden alfabetico, 'ausente' si falta)\n"
                    "    pass\n"
                ),
                hints=[
                    "Compara antes['datos']['huella'] con despues['datos']['huella']; igual con config.",
                    "La union de paquetes: sorted(set(antes['entorno']) | set(despues['entorno'])).",
                    "antes['entorno'].get(paquete, 'ausente') da la version o 'ausente'.",
                    "cambios.append(f'entorno: {paquete} {va} -> {vd}') solo si va != vd; al final return cambios.",
                ],
                difficulty="hard",
                points=20,
                hidden_tests=[
                    {
                        "name": "nada cambia salvo las metricas",
                        "code": (
                            "m = {'datos': {'huella': 'aaa', 'filas': 10}, 'config': {'huella': 'ccc', 'valores': {}},\n"
                            "     'semilla': 1, 'entorno': {'numpy': '2.0.2'}, 'metricas': {'accuracy': 0.9}}\n"
                            "otro = {'datos': {'huella': 'aaa', 'filas': 10}, 'config': {'huella': 'ccc', 'valores': {}},\n"
                            "        'semilla': 1, 'entorno': {'numpy': '2.0.2'}, 'metricas': {'accuracy': 0.7}}\n"
                            "r = diferencias(m, otro)\n"
                            "assert r == [], r\n"
                        ),
                    },
                    {
                        "name": "datos, config y semilla en orden",
                        "code": (
                            "a = {'datos': {'huella': 'aaa', 'filas': 10}, 'config': {'huella': 'ccc', 'valores': {}},\n"
                            "     'semilla': 1, 'entorno': {}, 'metricas': {}}\n"
                            "b = {'datos': {'huella': 'bbb', 'filas': 11}, 'config': {'huella': 'ccc', 'valores': {}},\n"
                            "     'semilla': 2, 'entorno': {}, 'metricas': {}}\n"
                            "assert diferencias(a, b) == ['datos', 'semilla'], diferencias(a, b)\n"
                            "c = dict(b, config={'huella': 'ddd', 'valores': {}})\n"
                            "assert diferencias(a, c) == ['datos', 'config', 'semilla'], diferencias(a, c)\n"
                        ),
                    },
                    {
                        "name": "entorno ordenado y con ausente",
                        "code": (
                            "a = {'datos': {'huella': 'x', 'filas': 1}, 'config': {'huella': 'y', 'valores': {}}, 'semilla': 0,\n"
                            "     'entorno': {'python': '3.12', 'numpy': '1.26.4', 'pandas': '2.2.0'}, 'metricas': {}}\n"
                            "b = {'datos': {'huella': 'x', 'filas': 1}, 'config': {'huella': 'y', 'valores': {}}, 'semilla': 0,\n"
                            "     'entorno': {'python': '3.12', 'numpy': '2.0.2', 'sklearn': '1.5.0'}, 'metricas': {}}\n"
                            "r = diferencias(a, b)\n"
                            "assert r == ['entorno: numpy 1.26.4 -> 2.0.2', 'entorno: pandas 2.2.0 -> ausente', 'entorno: sklearn ausente -> 1.5.0'], r\n"
                        ),
                    },
                    {
                        "name": "todo a la vez",
                        "code": (
                            "a = {'datos': {'huella': 'x', 'filas': 1}, 'config': {'huella': 'y', 'valores': {}}, 'semilla': 0,\n"
                            "     'entorno': {'numpy': '1.26.4'}, 'metricas': {}}\n"
                            "b = {'datos': {'huella': 'z', 'filas': 1}, 'config': {'huella': 'w', 'valores': {}}, 'semilla': 3,\n"
                            "     'entorno': {'numpy': '2.0.2'}, 'metricas': {}}\n"
                            "r = diferencias(a, b)\n"
                            "assert r == ['datos', 'config', 'semilla', 'entorno: numpy 1.26.4 -> 2.0.2'], r\n"
                        ),
                    },
                ],
            ),
            ExerciseTemplate(
                title="Ejecutar un experimento reproducible",
                description="Dividir, entrenar y devolver el manifiesto con su identificador.",
                instructions=(
                    "Implementa `ejecutar_experimento(filas, config, semilla, entrenar_fn, entorno)`. `entrenar_fn(train, test, config)` es una funcion que entrena y devuelve un diccionario de metricas. Las funciones `huella`, `huella_config`, `huella_datos` y `dividir` ya vienen escritas.\n"
                    "\n"
                    "1. Divide con `dividir(filas, config['fraccion_test'], semilla)`.\n"
                    "2. Llama a `entrenar_fn(train, test, config)` y guarda sus metricas.\n"
                    "3. Construye el manifiesto:\n"
                    "\n"
                    "```\n"
                    "{'datos': {'huella': huella_datos(filas), 'filas': len(filas)},\n"
                    " 'config': {'huella': huella_config(config), 'valores': config},\n"
                    " 'semilla': semilla,\n"
                    " 'entorno': una copia de entorno,\n"
                    " 'metricas': metricas}\n"
                    "```\n"
                    "\n"
                    "4. Anadele `'id'`: la `huella_config` de un diccionario con **solo** `datos`, `config`, `semilla` y `entorno` del manifiesto. Las metricas no forman parte del id: dos ejecuciones con la misma receta tienen el mismo id aunque el resultado cambie.\n"
                    "\n"
                    "Devuelve el manifiesto."
                ),
                starter_code=(
                    "import hashlib\n"
                    "import json\n"
                    "import random\n"
                    "\n"
                    "\n"
                    "def huella(texto, n=12):\n"
                    "    return hashlib.sha256(texto.encode('utf-8')).hexdigest()[:n]\n"
                    "\n"
                    "\n"
                    "def huella_config(config):\n"
                    "    return huella(json.dumps(config, sort_keys=True, separators=(',', ':')))\n"
                    "\n"
                    "\n"
                    "def huella_datos(filas, ignorar_orden=False):\n"
                    "    huellas = [huella(json.dumps(fila, sort_keys=True)) for fila in filas]\n"
                    "    if ignorar_orden:\n"
                    "        huellas = sorted(huellas)\n"
                    "    return huella(''.join(huellas))\n"
                    "\n"
                    "\n"
                    "def dividir(filas, fraccion_test, semilla):\n"
                    "    copia = list(filas)\n"
                    "    random.Random(semilla).shuffle(copia)\n"
                    "    n_test = round(len(copia) * fraccion_test)\n"
                    "    return copia[n_test:], copia[:n_test]\n"
                    "\n"
                    "\n"
                    "def ejecutar_experimento(filas, config, semilla, entrenar_fn, entorno):\n"
                    "    # TODO: dividir, entrenar, manifiesto e id\n"
                    "    pass\n"
                ),
                hints=[
                    "train, test = dividir(filas, config['fraccion_test'], semilla); metricas = entrenar_fn(train, test, config)",
                    "dict(entorno) crea una copia: si quien llama cambia su diccionario despues, el manifiesto no se entera.",
                    "receta = {k: manifiesto[k] for k in ('datos', 'config', 'semilla', 'entorno')}",
                    "manifiesto['id'] = huella_config(receta) y return manifiesto.",
                ],
                difficulty="hard",
                points=25,
                hidden_tests=[
                    {
                        "name": "entrena con la division reproducible",
                        "code": (
                            "filas = [{'pedido': i, 'devuelto': i % 3 == 0} for i in range(20)]\n"
                            "config = {'modelo': 'arbol', 'max_depth': 3, 'fraccion_test': 0.25}\n"
                            "llamadas = []\n"
                            "def entrenar_fn(train, test, cfg):\n"
                            "    llamadas.append((train, test, cfg))\n"
                            "    return {'accuracy': 0.8, 'n_test': len(test)}\n"
                            "m = ejecutar_experimento(filas, config, 5, entrenar_fn, {'numpy': '2.0.2'})\n"
                            "assert len(llamadas) == 1, llamadas\n"
                            "esperado = dividir(filas, 0.25, 5)\n"
                            "assert (llamadas[0][0], llamadas[0][1]) == esperado\n"
                            "assert llamadas[0][2] == config\n"
                            "assert m['metricas'] == {'accuracy': 0.8, 'n_test': 5}, m['metricas']\n"
                        ),
                    },
                    {
                        "name": "estructura del manifiesto",
                        "code": (
                            "import json\n"
                            "filas = [{'pedido': 1}, {'pedido': 2}, {'pedido': 3}, {'pedido': 4}]\n"
                            "config = {'max_depth': 2, 'fraccion_test': 0.5}\n"
                            "entorno = {'python': '3.12', 'numpy': '2.0.2'}\n"
                            "m = ejecutar_experimento(filas, config, 1, lambda tr, te, c: {'accuracy': 1.0}, entorno)\n"
                            "assert m['datos'] == {'huella': huella_datos(filas), 'filas': 4}, m['datos']\n"
                            "assert m['config'] == {'huella': huella_config(config), 'valores': config}, m['config']\n"
                            "assert m['semilla'] == 1 and m['entorno'] == entorno\n"
                            "entorno['numpy'] = '9.9'\n"
                            "assert m['entorno']['numpy'] == '2.0.2', 'el manifiesto debe guardar una copia del entorno'\n"
                            "assert json.loads(json.dumps(m)) == m\n"
                        ),
                    },
                    {
                        "name": "el id depende de la receta, no de las metricas",
                        "code": (
                            "filas = [{'pedido': i} for i in range(8)]\n"
                            "config = {'max_depth': 2, 'fraccion_test': 0.25}\n"
                            "resultados = iter([0.9, 0.7, 0.9])\n"
                            "def entrenar_fn(train, test, cfg):\n"
                            "    return {'accuracy': next(resultados)}\n"
                            "a = ejecutar_experimento(filas, config, 1, entrenar_fn, {'numpy': '2.0.2'})\n"
                            "b = ejecutar_experimento(filas, config, 1, entrenar_fn, {'numpy': '2.0.2'})\n"
                            "c = ejecutar_experimento(filas, config, 2, entrenar_fn, {'numpy': '2.0.2'})\n"
                            "assert isinstance(a['id'], str) and len(a['id']) == 12, a.get('id')\n"
                            "assert a['metricas'] != b['metricas']\n"
                            "assert a['id'] == b['id'], 'misma receta, mismo id'\n"
                            "assert c['id'] != a['id'], 'otra semilla, otro id'\n"
                        ),
                    },
                    {
                        "name": "el id es la huella de datos, config, semilla y entorno",
                        "code": (
                            "filas = [{'pedido': 1}, {'pedido': 2}]\n"
                            "config = {'fraccion_test': 0.5}\n"
                            "m = ejecutar_experimento(filas, config, 3, lambda tr, te, c: {'accuracy': 0.5}, {'numpy': '2.0.2'})\n"
                            "receta = {k: m[k] for k in ('datos', 'config', 'semilla', 'entorno')}\n"
                            "assert m['id'] == huella_config(receta), m\n"
                            "otro = ejecutar_experimento(filas, config, 3, lambda tr, te, c: {'accuracy': 0.5}, {'numpy': '2.1.0'})\n"
                            "assert otro['id'] != m['id'], 'otro entorno, otro id'\n"
                        ),
                    },
                ],
            ),
        ],
    ),
]


async def seed_lessons_with_exercises(db: AsyncSession) -> int:
    """Create/update core lessons and their exercises."""
    lessons_by_title: dict[str, Lesson] = {}
    inserted = 0

    for template in LESSON_TEMPLATES:
        existing_result = await db.execute(
            select(Lesson).where(Lesson.title == template.title)
        )
        lesson = existing_result.scalar_one_or_none()

        if not lesson:
            lesson = Lesson(
                title=template.title,
                description=template.description,
                content=template.content,
                difficulty=template.difficulty,
                category=template.category,
                track=template.track,
                order=template.order,
                estimated_duration=template.estimated_duration,
                prerequisites=[],
                is_active=True,
            )
            db.add(lesson)
            await db.flush()
            inserted += 1
        else:
            lesson.description = template.description
            lesson.content = template.content
            lesson.difficulty = template.difficulty
            lesson.category = template.category
            lesson.track = template.track
            lesson.order = template.order
            lesson.estimated_duration = template.estimated_duration
            lesson.is_active = True

        lessons_by_title[template.title] = lesson

        # Upsert de ejercicios por (lesson_id, title) PRESERVANDO el id.
        # Antes se hacia delete+recreate, lo que cambiaba los ids en cada
        # deploy/arranque y dejaba huerfanos los CodeSubmission de los
        # usuarios (el progreso se perdia). Ahora se actualizan in-place.
        existing_ex_result = await db.execute(
            select(Exercise).where(Exercise.lesson_id == lesson.id)
        )
        existing_by_title = {e.title: e for e in existing_ex_result.scalars().all()}
        template_titles = set()
        for index, ex in enumerate(template.exercises, start=1):
            template_titles.add(ex.title)
            row = existing_by_title.get(ex.title)
            if row is None:
                db.add(
                    Exercise(
                        lesson_id=lesson.id,
                        title=ex.title,
                        description=ex.description,
                        instructions=ex.instructions,
                        starter_code=ex.starter_code,
                        solution_code=None,
                        test_cases=[],
                        hidden_tests=list(ex.hidden_tests),
                        hints=ex.hints,
                        points=ex.points,
                        difficulty=ex.difficulty,
                        order=index,
                    )
                )
            else:
                row.description = ex.description
                row.instructions = ex.instructions
                row.starter_code = ex.starter_code
                row.hidden_tests = list(ex.hidden_tests)
                row.hints = ex.hints
                row.points = ex.points
                row.difficulty = ex.difficulty
                row.order = index

        # Limpia ejercicios que ya no estan en el template (renombrados o
        # quitados). Sus submissions se borran en cascada; los ejercicios
        # vigentes conservan su id y su progreso.
        for title, row in existing_by_title.items():
            if title not in template_titles:
                await db.execute(delete(Exercise).where(Exercise.id == row.id))

    await db.flush()
    for template in LESSON_TEMPLATES:
        lesson = lessons_by_title[template.title]
        prerequisites = []
        for prereq_title in template.prerequisites_titles:
            prereq_lesson = lessons_by_title.get(prereq_title)
            if prereq_lesson:
                prerequisites.append(prereq_lesson.id)
        lesson.prerequisites = prerequisites

    await db.commit()
    return inserted
