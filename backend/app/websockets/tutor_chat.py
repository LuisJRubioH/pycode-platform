"""
WebSocket endpoint for AI tutor chat.
"""

import json
from fastapi import WebSocket, WebSocketDisconnect
from app.services.ai_tutor import AITutorService


async def tutor_chat_ws(websocket: WebSocket):
    """WebSocket endpoint for AI tutor chat."""
    await websocket.accept()

    tutor_service = AITutorService()

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)

            user_message = message.get("message", "")
            context = message.get("context", {})

            if not user_message:
                await websocket.send_json(
                    {"type": "error", "content": "No message provided"}
                )
                continue

            try:
                # Get response from AI tutor
                response = await tutor_service.get_response(user_message, context)

                await websocket.send_json({"type": "message", "content": response})

            except Exception as e:
                await websocket.send_json(
                    {
                        "type": "error",
                        "content": f"Error getting tutor response: {str(e)}",
                    }
                )

    except WebSocketDisconnect:
        print("Client disconnected from tutor chat WebSocket")
    except Exception as e:
        print(f"Error in tutor chat WebSocket: {e}")
        try:
            await websocket.close()
        except Exception:
            pass
