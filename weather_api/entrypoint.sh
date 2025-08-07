#!/bin/sh

echo "Esperando o banco de dados iniciar..."
sleep 5

echo "Rodando migrações..."
python manage.py migrate

echo "Iniciando o servidor..."
exec "$@"