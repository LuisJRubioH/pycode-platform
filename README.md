# PyCode Platform

Plataforma de aprendizaje de Python con tutor IA socrático, ejecución de código en tiempo real y seguimiento de progreso.

## Características

- **Editor de código en vivo**: Ejecuta Python directamente en el navegador
- **Tutor IA Socrático**: Aprende con guía personalizada que te ayuda a pensar
- **Lecciones adaptativas**: Desde básico hasta avanzado con contenido personalizado
- **Ejecución segura**: Código se ejecuta en containers Docker aislados
- **Open Source**: Código libre para la comunidad

## Tecnologías

### Backend
- FastAPI (Python 3.11+)
- PostgreSQL + SQLAlchemy (async)
- Redis para caché
- Docker para ejecución de código
- OpenAI API para tutor IA
- JWT para autenticación

### Frontend
- React + TypeScript
- Vite
- TailwindCSS
- Monaco Editor (VS Code engine)
- React Query + Zustand
- Axios + WebSocket

## Requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 15
- Redis 7
- Docker

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repositorio>
cd plataforma_pycode
```

### 2. Configurar el backend

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

### 3. Configurar la base de datos

```bash
# Iniciar PostgreSQL y Redis (con Docker)
docker-compose up -d db redis

# Ejecutar migraciones (próximamente con Alembic)
```

### 4. Configurar el frontend

```bash
cd frontend
npm install
```

### 5. Iniciar el proyecto

```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

La aplicación estará disponible en:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Documentación: http://localhost:8000/docs

## Estructura del Proyecto

```
plataforma_pycode/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── websockets/
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── store/
│   ├── public/
│   └── package.json
├── requirements.txt
├── docker-compose.yml
└── README.md
```

## Características MVP (Fase 1)

- [x] Autenticación con JWT
- [x] Ejecución de código Python en Docker
- [x] Editor Monaco integrado
- [x] Estructura base de lecciones
- [ ] Integración con OpenAI
- [ ] Sistema de progreso
- [ ] Dashboard de usuario

## Contribuir

1. Fork el repositorio
2. Crea una branch: `git checkout -b feature/nueva-caracteristica`
3. Commit tus cambios: `git commit -am 'Agregar nueva característica'`
4. Push a la branch: `git push origin feature/nueva-caracteristica`
5. Crea un Pull Request

## Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

## Contacto

- Email: contacto@pycode.com
- GitHub Issues: Para reportar bugs y sugerencias

---

**PyCode Platform** - Aprende Python de manera interactiva y divertida!
