#!/bin/bash
# Script de inicio para Linux/macOS
# Sistema de Confirmación de Asistencia a Asambleas

echo "========================================"
echo "Sistema de Confirmación de Asistencia"
echo "========================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi

echo "[1/3] Verificando Python..."
python3 --version
echo ""

echo "[2/3] Instalando dependencias..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi
echo ""

echo "[3/3] Iniciando servidor..."
echo ""
echo "El servidor se iniciará en: http://localhost:5000"
echo ""
echo "- Confirmación de asistencia: http://localhost:5000"
echo "- Panel administrativo: http://localhost:5000/admin.html"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""
echo "========================================"
echo ""

python3 backend/app.py
