"""
Seed theory-first Python lessons and guided exercises.
"""

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


LESSON_TEMPLATES: list[LessonTemplate] = [
    LessonTemplate(
        title="Python desde Cero",
        description="Que es Python, como ejecutar scripts y estructura minima de un programa.",
        content=(
            "## Objetivo\n"
            "Entender que es Python y como correr tu primer script.\n\n"
            "## Teoria\n"
            "- Python es un lenguaje interpretado y multiparadigma.\n"
            "- `print()` muestra informacion en consola.\n"
            "- Un archivo `.py` se ejecuta de arriba hacia abajo.\n\n"
            "## Buenas practicas\n"
            "- Usa nombres claros.\n"
            "- Comenta solo cuando aporta contexto.\n"
            "- Prueba cambios pequeños y frecuentes.\n"
        ),
        difficulty="beginner",
        category="fundamentos",
        order=1,
        estimated_duration=20,
        exercises=[
            ExerciseTemplate(
                title="Hola Python",
                description="Imprime un saludo y tu nombre.",
                instructions="Crea una variable `nombre` y muestra `Hola, <nombre>` usando f-string.",
                starter_code="nombre = ''\n# TODO\n",
                hints=["Usa print(f'Hola, {nombre}')", "Asigna primero un string a nombre"],
            ),
            ExerciseTemplate(
                title="Mini presentación",
                description="Muestra dos lineas con informacion personal.",
                instructions="Imprime ciudad y lenguaje favorito en lineas separadas.",
                starter_code="ciudad = ''\nlenguaje = 'Python'\n# TODO\n",
            ),
        ],
    ),
    LessonTemplate(
        title="Variables y Tipos",
        description="Numeros, strings, booleanos y conversiones basicas.",
        content=(
            "## Tipos comunes\n"
            "- `int`, `float`, `str`, `bool`\n"
            "- `type(valor)` permite inspeccionar el tipo.\n\n"
            "## Conversion\n"
            "- `int('10')`, `str(25)`, `float(3)`\n"
            "- Convierte antes de operar para evitar errores.\n"
        ),
        difficulty="beginner",
        category="fundamentos",
        order=2,
        estimated_duration=25,
        prerequisites_titles=["Python desde Cero"],
        exercises=[
            ExerciseTemplate(
                title="Conversor simple",
                description="Convierte texto a numero.",
                instructions="Recibe `texto_numero` y calcula su doble como int.",
                starter_code="texto_numero = '12'\n# TODO\n",
            ),
            ExerciseTemplate(
                title="Chequeo de tipos",
                description="Valida tipos de variables.",
                instructions="Imprime el tipo de `edad`, `altura` y `activo`.",
                starter_code="edad = 18\naltura = 1.72\nactivo = True\n# TODO\n",
            ),
        ],
    ),
    LessonTemplate(
        title="Condicionales y Logica",
        description="if/elif/else, comparaciones y operadores logicos.",
        content=(
            "## Estructura\n"
            "```python\n"
            "if condicion:\n"
            "    ...\n"
            "elif otra:\n"
            "    ...\n"
            "else:\n"
            "    ...\n"
            "```\n\n"
            "## Operadores\n"
            "- Comparacion: `==`, `!=`, `<`, `>`, `<=`, `>=`\n"
            "- Logica: `and`, `or`, `not`\n"
        ),
        difficulty="beginner",
        category="control-flujo",
        order=3,
        estimated_duration=30,
        prerequisites_titles=["Variables y Tipos"],
        exercises=[
            ExerciseTemplate(
                title="Clasificador de edad",
                description="Define etapa de vida basica.",
                instructions="Con `edad`, imprime `menor`, `adulto` o `senior`.",
                starter_code="edad = 17\n# TODO\n",
            ),
            ExerciseTemplate(
                title="Acceso permitido",
                description="Combina condiciones.",
                instructions="Permite acceso si `tiene_pase` y `edad >= 18`.",
                starter_code="tiene_pase = True\nedad = 19\n# TODO\n",
            ),
        ],
    ),
    LessonTemplate(
        title="Bucles for y while",
        description="Iteraciones, range y control con break/continue.",
        content=(
            "## for\n"
            "- Recorre elementos o rangos.\n"
            "- `range(inicio, fin, paso)`\n\n"
            "## while\n"
            "- Repite mientras se cumpla una condicion.\n"
            "- Evita bucles infinitos actualizando estado.\n"
        ),
        difficulty="beginner",
        category="control-flujo",
        order=4,
        estimated_duration=35,
        prerequisites_titles=["Condicionales y Logica"],
        exercises=[
            ExerciseTemplate(
                title="Suma acumulada",
                description="Acumula valores 1..n.",
                instructions="Calcula la suma de 1 a `n` usando for.",
                starter_code="n = 10\n# TODO\n",
            ),
            ExerciseTemplate(
                title="Contador while",
                description="Cuenta hacia atras.",
                instructions="Imprime de 5 a 1 usando while.",
                starter_code="# TODO\n",
            ),
        ],
    ),
    LessonTemplate(
        title="Funciones y Parametros",
        description="Definir funciones, retorno y argumentos por defecto.",
        content=(
            "## Funcion\n"
            "Una funcion encapsula una tarea reutilizable.\n\n"
            "## Reglas\n"
            "- Usa `return` para devolver resultados.\n"
            "- Prefiere funciones cortas con una responsabilidad.\n"
            "- Documenta inputs/salidas en comentarios o docstring.\n"
        ),
        difficulty="intermediate",
        category="funciones",
        order=5,
        estimated_duration=35,
        prerequisites_titles=["Bucles for y while"],
        exercises=[
            ExerciseTemplate(
                title="Area de rectangulo",
                description="Funcion con retorno.",
                instructions="Implementa `area_rectangulo(base, altura)`.",
                starter_code="def area_rectangulo(base: float, altura: float) -> float:\n    # TODO\n    pass\n",
            ),
            ExerciseTemplate(
                title="Saludo configurable",
                description="Parametro por defecto.",
                instructions="Implementa `saludar(nombre, prefijo='Hola')`.",
                starter_code="def saludar(nombre: str, prefijo: str = 'Hola') -> str:\n    # TODO\n    pass\n",
            ),
        ],
    ),
    LessonTemplate(
        title="Listas, Tuplas y Diccionarios",
        description="Estructuras de datos base para colecciones.",
        content=(
            "## Listas\n"
            "- Mutables, indexadas y ordenadas.\n\n"
            "## Tuplas\n"
            "- Inmutables, utiles para pares fijos.\n\n"
            "## Diccionarios\n"
            "- Clave-valor para busqueda rapida.\n"
        ),
        difficulty="intermediate",
        category="estructuras-datos",
        order=6,
        estimated_duration=40,
        prerequisites_titles=["Funciones y Parametros"],
        exercises=[
            ExerciseTemplate(
                title="Promedio de notas",
                description="Recorre listas.",
                instructions="Calcula promedio de `notas` con dos decimales.",
                starter_code="notas = [4.5, 3.8, 5.0, 4.2]\n# TODO\n",
            ),
            ExerciseTemplate(
                title="Agenda minima",
                description="Uso de diccionario.",
                instructions="Agrega y consulta un contacto en `agenda`.",
                starter_code="agenda = {}\n# TODO\n",
            ),
        ],
    ),
    LessonTemplate(
        title="Comprensiones y Manejo de Errores",
        description="List comprehensions y try/except para codigo robusto.",
        content=(
            "## Comprensiones\n"
            "- Sintaxis compacta para transformar colecciones.\n"
            "- Ejemplo: `[x * 2 for x in numeros if x % 2 == 0]`\n\n"
            "## Errores\n"
            "- Usa `try/except` para capturar fallos esperables.\n"
            "- No captures excepciones demasiado generales sin contexto.\n"
        ),
        difficulty="intermediate",
        category="python-moderno",
        order=7,
        estimated_duration=35,
        prerequisites_titles=["Listas, Tuplas y Diccionarios"],
        exercises=[
            ExerciseTemplate(
                title="Filtrado par",
                description="Practica comprehension.",
                instructions="Crea lista con cuadrados de numeros pares de 1..20.",
                starter_code="# TODO\n",
            ),
            ExerciseTemplate(
                title="Division segura",
                description="Captura errores comunes.",
                instructions="Implementa `division_segura(a, b)` que retorne None si b es 0.",
                starter_code="def division_segura(a: float, b: float):\n    # TODO\n    pass\n",
            ),
        ],
    ),
    LessonTemplate(
        title="POO en Python",
        description="Clases, objetos, metodos y encapsulacion basica.",
        content=(
            "## Clase y objeto\n"
            "- Clase define estructura/comportamiento.\n"
            "- Objeto es una instancia de clase.\n\n"
            "## Buenas practicas\n"
            "- Usa `__init__` para estado inicial.\n"
            "- Manten metodos pequenos y enfocados.\n"
        ),
        difficulty="advanced",
        category="oop",
        order=8,
        estimated_duration=45,
        prerequisites_titles=["Comprensiones y Manejo de Errores"],
        exercises=[
            ExerciseTemplate(
                title="Clase Producto",
                description="Modela entidad simple.",
                instructions="Crea clase Producto con nombre/precio y metodo aplicar_descuento.",
                starter_code="class Producto:\n    def __init__(self, nombre: str, precio: float):\n        self.nombre = nombre\n        self.precio = precio\n\n    # TODO\n",
                difficulty="medium",
                points=15,
            ),
            ExerciseTemplate(
                title="Cuenta bancaria",
                description="Mutacion de estado.",
                instructions="Implementa depositar y retirar con validaciones.",
                starter_code="class Cuenta:\n    def __init__(self):\n        self.saldo = 0\n\n    # TODO\n",
                difficulty="medium",
                points=15,
            ),
        ],
    ),
    LessonTemplate(
        title="Modulos, Paquetes y Entornos",
        description="Organiza proyectos Python y gestiona dependencias.",
        content=(
            "## Modulos\n"
            "- Un archivo `.py` es un modulo.\n"
            "- Importa con `import` o `from ... import ...`.\n\n"
            "## Entornos virtuales\n"
            "- Aislan dependencias por proyecto.\n"
            "- Usa `python -m venv .venv` y activa antes de instalar paquetes.\n"
        ),
        difficulty="advanced",
        category="tooling",
        order=9,
        estimated_duration=30,
        prerequisites_titles=["POO en Python"],
        exercises=[
            ExerciseTemplate(
                title="Refactor a modulo",
                description="Separacion por archivos.",
                instructions="Divide funciones en un modulo `utils.py` y consumelo desde `main.py`.",
                starter_code="# main.py\n# TODO\n",
                difficulty="medium",
            ),
        ],
    ),
    LessonTemplate(
        title="Testing con pytest",
        description="Pruebas unitarias para validar comportamiento.",
        content=(
            "## Idea central\n"
            "Las pruebas automatizadas permiten refactorizar con confianza.\n\n"
            "## pytest basico\n"
            "- Archivos `test_*.py`\n"
            "- Funciones `test_*`\n"
            "- Usa asserts claros y casos borde.\n"
        ),
        difficulty="advanced",
        category="testing",
        order=10,
        estimated_duration=40,
        prerequisites_titles=["Modulos, Paquetes y Entornos"],
        exercises=[
            ExerciseTemplate(
                title="Prueba de calculadora",
                description="Escribe tus primeros tests.",
                instructions="Crea tests para suma, resta y division por cero.",
                starter_code="# test_calculadora.py\n# TODO\n",
                difficulty="hard",
                points=20,
            ),
        ],
    ),
]


async def seed_lessons_with_exercises(db: AsyncSession) -> int:
    """Create/update core lessons and their exercises."""
    lessons_by_title: dict[str, Lesson] = {}
    inserted = 0

    for template in LESSON_TEMPLATES:
        existing_result = await db.execute(select(Lesson).where(Lesson.title == template.title))
        lesson = existing_result.scalar_one_or_none()

        if not lesson:
            lesson = Lesson(
                title=template.title,
                description=template.description,
                content=template.content,
                difficulty=template.difficulty,
                category=template.category,
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
            lesson.order = template.order
            lesson.estimated_duration = template.estimated_duration
            lesson.is_active = True

        lessons_by_title[template.title] = lesson

        await db.execute(delete(Exercise).where(Exercise.lesson_id == lesson.id))
        for index, ex in enumerate(template.exercises, start=1):
            db.add(
                Exercise(
                    lesson_id=lesson.id,
                    title=ex.title,
                    description=ex.description,
                    instructions=ex.instructions,
                    starter_code=ex.starter_code,
                    solution_code=None,
                    test_cases=[],
                    hints=ex.hints,
                    points=ex.points,
                    difficulty=ex.difficulty,
                    order=index,
                )
            )

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
