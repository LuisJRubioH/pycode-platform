# Migraciones

Antes de levantar la app:

    cd backend && alembic upgrade head

En CI/Render esto va en el comando de release. Nunca usar `Base.metadata.create_all` en producción.
