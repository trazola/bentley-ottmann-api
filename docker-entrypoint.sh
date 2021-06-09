#!/bin/sh

alembic upgrade head
exec uvicorn main:app --reload --app-dir bentley_ottmann_api  --host 0.0.0.0 --port 8000