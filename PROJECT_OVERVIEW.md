# Resumen del Proyecto: PyCode Platform

## 1. ¿Qué es PyCode Platform?

**PyCode Platform** es una aplicación con enfoque educativo y de entrenamiento técnico diseñada específicamente para que los usuarios puedan **aprender y practicar Python en un solo lugar**.  
La visión del proyecto radica en reemplazar las típicas plataformas pasivas (donde el usuario sólo lee o ve vídeos) por un ecosistema donde la interacción mediante la codificación en vivo, un motor estadístico de progreso y un "Tutor Socrático" impulsado por Inteligencia Artificial jueguen un papel central en el aprendizaje diario del usuario.

## 2. Propuesta de Valor y Filosofía de Aprendizaje

A diferencia de otras plataformas, la filosofía central de PyCode es el **"Aprender haciendo, guiado inteligentemente"**. 

- **Resolución Activa (Ejecución Real):** El usuario no responde pautas ficticias ni encuestas interactivas. Cuenta con un editor web `(Monaco Editor)`, capaz de conectarse vía Sockets a ejecutar procesos asíncronos y devolver la misma salida en un pseudo-terminal web de interfaz intuitiva.
- **Tutor Socrático (IA):** En lugar de dar únicamente respuestas explícitas en bloques copiables, el tutor está instruido bajo directrices socráticas. Realiza preguntas al código proporcionado estimulando al usuario a que encuentre él mismo sus propios errores, comprenda lógicas algorítmicas y piense cómo resolver antes que simplemente recibir los resultados, acercándolo más a la realidad de un Ingeniero Senior.
- **Gamificación Sólida:** Retención de estudiantes garantizada con lecciones guiadas en curva de dificultad, sistema dinámico de Puntos por Experiencia (XP), estadísticas de completitud, visualización de progreso asíncrono y control de rachas de aprendizaje para inspirar consistencia diaria.

## 3. Arquitectura del Proyecto

El sistema está construido como una Aplicación Integral moderna separada estrictamente entre **Frontend** y **Backend Api**, bajo el siguiente Stack Tecnológico estandarizado:

### 3.1 Tecnologías del Backend
* **Desarrollo**: Python 3.11+, con el framework **FastAPI** que brinda enrutamiento ultra veloz ASGI.
* **Componentes asíncronos (WebSockets)**: Infraestructura basada en eventos para emitir mensajes y evaluar ejecuciones pesadas en Docker sin congelar a los clientes HTTP en vivo.
* **Persistencia de Base de datos:** 
  - Modelado y Querys mediante **SQLAlchemy 2.0 (Async)**.
  - Bases estructurales Relacionales implementadas con motores estándar (Compatible con *PostgreSQL* y con *SQLite* vía aiosqlite en ambientes locales). 
* **Control de Sesiones e Identidad:** Rutas seguras dependientes de inyección `Depends()` con encriptadores bcrypt validando Tokens JWT estándar en cabeceras Bearer.

### 3.2 Tecnologías del Frontend
* **Core:** Proyecto montado sobre el generador de paquetes modernos **Vite**, impulsando **React y TypeScript**.
* **Gestión de Estados:** Estado global dinámico mantenido con **Zustand** (para controlar sesiones de usuario estables) y herramientas de obtención asíncrona local de promesas (`fetch` api).
* **Navegación e Interfaz:** React Router DOM para evitar recargas constantes asimilando una fluidez tipo *Single Page Application*. 
* **Estilizado de Componentes:** Interfaz puramente estilizada con clases de utilidad impulsadas por **TailwindCSS**, junto con íconos de *Lucide React* dando acabados premium a alertas y botones. Componentes clave como *Monaco-Editor (Tecnología de VSCode)* integrados nativamente.

## 4. Estructura y Flujos Clave

El ecosistema entero gira en torno a estos pilares:
1. **Módulo de Autenticación (`/login`, `/register`)**: Los visitantes nuevos ingresan al flujo de registro (donde un modelo en base de datos `UserProfile` asocia en tiempo cero estadísticas limpias) y loguea recibiendo su Access_Token alojado en Local Storage de manera inmediata sin redirecciones obsoletas. 
2. **Dashboard Dinámico (`/dashboard`)**: Una abstracción gerencial que resume la persistencia del usuario mostrando rachas activas, progreso global de lecciones completadas frente al temario, y puntos XP en UI. Es consultado a la API con consultas optimizadas en PostgreSQL/SQLite asegurando mínima latencia.
3. **Editor de Código en Vivo (`/editor`)**: Donde la destreza es probada. Contiene un gestor que no solo permite correr comandos locales dentro del flujo de la interfaz interactuando por Sockets, sino permite personalización (Ajustes de font-size del editor, temario dark/light, alternar vista de minimapas) o herramientas de externalización (guardar a tu PC un ".py", o enviar el algoritmo directo a un portapapeles).

---

`Elaborado como material complementario de documentación en curso del desarrollo local de PyCode.`
