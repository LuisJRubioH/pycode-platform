"""Extraccion de las notas del veredicto del tutor."""

import pytest

from app.services.evaluation_service import _GENERAL_RE, _LOGIC_RE, _extract_score


@pytest.mark.parametrize(
    "texto, logica, general",
    [
        # Lo que escribe openai/gpt-oss-120b: la nota va dentro de negrita.
        # Con el patron viejo (`\s*:?\s*`) esto no casaba y la ficha del modal
        # salia con un guion mientras el texto de al lado decia 95/100.
        (
            "- Logica: **95/100** - correcto\n- Solucion General: **80/100** - legible",
            95,
            80,
        ),
        ("**Logica:** 40/100 | **Solucion General:** 55/100", 40, 55),
        ("- **Logica: 88/100**\n- **Solucion General: 91/100**", 88, 91),
        # El texto de reserva del backend, sin Markdown ni tildes.
        ("CALIFICACION:\n- Logica: 75/100\n- Solucion General: 78/100", 75, 78),
        # Con tildes, que es como lo escribe el modelo en espanol.
        ("- Lógica: 60/100\n- Solución General: 70/100", 60, 70),
        # Sin notas: None, no un cero que pareceria una calificacion real.
        ("El codigo se ve bien, sigue asi.", None, None),
    ],
)
def test_extrae_notas_con_y_sin_markdown(texto, logica, general):
    assert _extract_score(_LOGIC_RE, texto) == logica
    assert _extract_score(_GENERAL_RE, texto) == general


def test_descarta_notas_fuera_de_rango():
    assert _extract_score(_LOGIC_RE, "Logica: 150/100") is None
