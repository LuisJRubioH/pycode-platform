"""
WebSocket de ejecución deprecado: el cliente Pyodide ejecuta localmente.

Mantengo el handler registrado para que clientes antiguos reciban un mensaje
explicativo en vez de un fallo de conexión silencioso. Cuando el frontend
deje de abrir esta ruta (ver Task 24), el handler completo puede borrarse.
"""

from fastapi import WebSocket


async def code_execution_ws(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json(
        {
            "type": "deprecated",
            "content": (
                "Ejecución en backend deshabilitada. El cliente debe usar "
                "Pyodide para ejecutar código localmente."
            ),
        }
    )
    await websocket.close(code=1000)
