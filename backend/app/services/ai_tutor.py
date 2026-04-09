"""
AI Tutor Service with OpenAI integration and Socratic method.
"""

import openai
from app.core.config import settings


class AITutorService:
    """AI Tutor service using OpenAI with Socratic method."""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        
        self.system_prompt = """You are a Python programming tutor who uses the Socratic method. 
Your goal is to guide students to discover answers through questions rather than giving direct solutions.

Guidelines:
1. Never give complete code solutions directly
2. Ask guiding questions to help students think
3. Provide hints and nudges in the right direction
4. Explain concepts through examples and analogies
5. Encourage experimentation and learning from mistakes
6. Adapt your explanations based on the student's level
7. Celebrate small wins and progress

When a student asks about code:
- Ask what they think the code does
- Guide them to trace through it step by step
- Help them identify patterns
- Ask what changes they might try

When a student is stuck on an error:
- Ask them to read the error message carefully
- Guide them to the specific line
- Ask what they think caused it
- Suggest they check specific things (syntax, indentation, variable names)

Always be encouraging, patient, and make learning Python feel achievable and fun!"""

    async def get_response(self, message: str, context: dict = None) -> str:
        """Get response from AI tutor."""
        if not settings.OPENAI_API_KEY:
            return self._get_fallback_response(message)
        
        try:
            # Build context-aware prompt
            user_context = self._build_context(context)
            
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"{user_context}\n\nStudent question: {message}"}
            ]
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return self._get_fallback_response(message)
    
    def _build_context(self, context: dict = None) -> str:
        """Build context string from user context."""
        if not context:
            return ""
        
        context_parts = []
        
        level = context.get('level', 'beginner')
        context_parts.append(f"Student level: {level}")
        
        current_lesson = context.get('currentLesson')
        if current_lesson:
            context_parts.append(f"Current lesson: {current_lesson}")
        
        recent_errors = context.get('recentErrors', [])
        if recent_errors:
            context_parts.append(f"Recent errors: {', '.join(recent_errors)}")
        
        return "\n".join(context_parts) if context_parts else ""
    
    def _get_fallback_response(self, message: str) -> str:
        """Get fallback response when OpenAI is not available."""
        message_lower = message.lower()
        
        if 'variable' in message_lower:
            return """¡Gran pregunta sobre variables! 🎯

Las variables son como cajas etiquetadas donde guardamos información. 

Antes de explicarte más, dime:
- ¿Has intentado crear alguna variable en el editor?
- ¿Qué crees que pasaría si escribimos: `mi_nombre = "Python"`?

¡Inténtalo y cuéntame qué ves!"""
        
        elif 'print' in message_lower or 'imprimir' in message_lower:
            return """¡Excelente! La función `print()` es fundamental. 📢

Pensemos juntos:
- ¿Qué crees que hace `print("Hola")` exactamente?
- ¿Por qué crees que usamos paréntesis `()`?

Prueba esto en el editor:
```python
print("Hola")
print(2 + 3)
print("2 + 3")
```

¿Qué diferencias notas entre las últimas dos líneas? 🤔"""
        
        elif 'error' in message_lower:
            return """¡Los errores son parte del aprendizaje! 💪

Cuando veas un error, pregúntate:
1. ¿Qué línea menciona el error?
2. ¿Qué tipo de error es? (SyntaxError, NameError, etc.)
3. ¿Qué crees que significa ese mensaje?

Copia el mensaje de error aquí y analicémoslo juntos paso a paso."""
        
        elif 'tipo de dato' in message_lower or 'type' in message_lower:
            return """¡Los tipos de datos son super importantes! 🧮

Python tiene varios tipos básicos:
- Números enteros (int): 1, 42, -7
- Números decimales (float): 3.14, 2.5
- Texto (str): "Hola", 'Python'
- Booleanos (bool): True, False

Pregunta clave: ¿Qué crees que obtendrías si sumas `"5" + "3"` vs `5 + 3`?

¡Pruébalo en el editor y sorpréndete! 🎉"""
        
        else:
            return """¡Interesante pregunta! 🤔

Como buen tutor socrático, déjame guiarte:

1. ¿Qué has intentado hasta ahora?
2. ¿Qué esperabas que pasara vs. lo que realmente pasó?
3. ¿Hay algún error específico que estés viendo?

Cuéntame más sobre tu código o el concepto que quieres entender, y juntos lo resolveremos paso a paso. 

Recuerda: ¡no hay preguntas tontas, solo oportunidades de aprender! 🌟"""


# Singleton instance
tutor_service = AITutorService()
