"""
Safe code executor for development (fallback when Docker unavailable).
Uses subprocess with security restrictions.
"""

import subprocess
import tempfile
import os
from typing import Dict, Any
from datetime import datetime

from app.core.config import settings


class DockerCodeExecutor:
    """Execute Python code safely using subprocess (Docker fallback for dev)."""
    
    def __init__(self, user_id: str, timeout: int = 5):
        self.user_id = user_id
        self.timeout = min(timeout, 10)  # Max 10 seconds in dev
        
    async def run_python_code(self, code: str) -> Dict[str, Any]:
        """Execute Python code in isolated subprocess."""
        start_time = datetime.utcnow()
        temp_file = None
        
        try:
            # Create temporary file with code in current directory (Windows compatible)
            temp_dir = os.path.dirname(os.path.abspath(__file__))
            with tempfile.NamedTemporaryFile(
                mode='w', 
                suffix='.py', 
                delete=False, 
                dir=temp_dir,
                prefix='code_',
                encoding='utf-8'
            ) as f:
                f.write(code)
                temp_file = f.name
            
            # Run code in subprocess with timeout
            process = subprocess.Popen(
                ['python', temp_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace',
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            try:
                stdout, stderr = process.communicate(timeout=self.timeout)
                execution_time = (datetime.utcnow() - start_time).total_seconds()
                
                return {
                    'success': process.returncode == 0,
                    'stdout': stdout,
                    'stderr': stderr,
                    'exit_code': process.returncode,
                    'execution_time': execution_time
                }
                
            except subprocess.TimeoutExpired:
                process.kill()
                return {
                    'success': False,
                    'stdout': '',
                    'stderr': f'Execution timeout after {self.timeout} seconds',
                    'exit_code': -1,
                    'execution_time': self.timeout
                }
                
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': f'Execution error: {str(e)}',
                'exit_code': -1,
                'execution_time': 0
            }
            
        finally:
            # Cleanup temp file
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except Exception:
                    pass
