#!/bin/bash

# Salir inmediatamente si un comando falla
set -e

echo "--- Configurando entorno ---"

# Asegurar dependencias
sudo apt update && sudo apt install -y python3-venv python3-pip

# Crea el entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv .venv
fi

# Activar entorno vitual
echo "Activando entorno vitual..."
source .venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "Creando archivo .env de ejemplo..."
    cp .env.example .env 2>/dev/null || echo "# Variables de entorno" > .env
fi

# Ejecutar script SQL
echo "Ejecutando db_scheme.sql..."
mysql -u root -p < db_scheme.sql

echo "Creando el primer administrador"
python -m backend.scripts.creacion_primer_admin

echo "Inicialización completa."
echo "El entorno virtual está listo. Para usarlo, ejecuta:"
echo "  source .venv/bin/activate"
echo "  python -m backend.app"
echo "  python -m frontend.app"
