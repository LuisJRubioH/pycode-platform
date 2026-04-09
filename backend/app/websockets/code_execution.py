"""
WebSocket endpoint for real-time code execution.
"""

import json
from fastapi import WebSocket, WebSocketDisconnect
from app.services.docker_executor import DockerCodeExecutor


async def code_execution_ws(websocket: WebSocket):
    """WebSocket endpoint for code execution."""
    await websocket.accept()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            code = message.get('code', '')
            timeout = message.get('timeout', 30)
            user_id = message.get('user_id', 'anonymous')
            
            if not code:
                await websocket.send_json({
                    'type': 'error',
                    'content': 'No code provided'
                })
                continue
            
            # Send status update
            await websocket.send_json({
                'type': 'status',
                'content': 'Executing...'
            })
            
            try:
                # Execute code in Docker
                executor = DockerCodeExecutor(user_id=user_id, timeout=timeout)
                result = await executor.run_python_code(code)
                
                # Send output
                if result['success']:
                    await websocket.send_json({
                        'type': 'output',
                        'content': result.get('stdout', '')
                    })
                else:
                    await websocket.send_json({
                        'type': 'error',
                        'content': result.get('stderr', 'Execution failed')
                    })
                
                # Send completion
                await websocket.send_json({
                    'type': 'done',
                    'execution_time': result.get('execution_time', 0),
                    'exit_code': result.get('exit_code', 0)
                })
                
            except Exception as e:
                await websocket.send_json({
                    'type': 'error',
                    'content': str(e)
                })
                await websocket.send_json({
                    'type': 'done',
                    'exit_code': -1
                })
    
    except WebSocketDisconnect:
        print("Client disconnected from code execution WebSocket")
    except Exception as e:
        print(f"Error in code execution WebSocket: {e}")
        try:
            await websocket.close()
        except Exception:
            pass
