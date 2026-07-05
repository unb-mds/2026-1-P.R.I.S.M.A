#!/bin/sh
set -e

until uv run src/manage.py migrate --noinput; do
  echo "Aguardando o banco de dados ficar pronto..."
  sleep 2
done

exec uv run src/manage.py runserver 0.0.0.0:8000