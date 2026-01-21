#!/bin/bash
# Script de inicio para producción (Linux/macOS)
# Sistema de Confirmación de Asistencia a Asambleas

echo "========================================"
echo "Sistema de Confirmación de Asistencia"
echo "Modo: PRODUCCIÓN"
echo "========================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    exit 1
fi

# Configurar variables de entorno
export FLASK_ENV=production
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-5000}
export SSL_ENABLED=${SSL_ENABLED:-false}

# Verificar si se debe usar SSL
if [ "$SSL_ENABLED" = "true" ]; then
    echo "🔒 Modo HTTPS habilitado"
    
    # Verificar que existan los certificados
    if [ ! -f "${SSL_CERT_PATH:-certs/cert.pem}" ] || [ ! -f "${SSL_KEY_PATH:-certs/key.pem}" ]; then
        echo "⚠️  Certificados SSL no encontrados"
        echo "Generando certificados autofirmados..."
        python3 generar_certificados.py
        echo ""
    fi
    
    PROTOCOL="https"
else
    echo "🔓 Modo HTTP (sin SSL)"
    PROTOCOL="http"
fi

echo ""
echo "Instalando dependencias..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi
echo ""

echo "Iniciando servidor de producción..."
echo ""
echo "Servidor disponible en: $PROTOCOL://$HOST:$PORT"
echo ""
echo "- Confirmación de asistencia: $PROTOCOL://$HOST:$PORT"
echo "- Panel administrativo: $PROTOCOL://$HOST:$PORT/admin.html"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""
echo "========================================"
echo ""

# Usar Gunicorn en Linux/macOS
if command -v gunicorn &> /dev/null; then
    if [ "$SSL_ENABLED" = "true" ]; then
        gunicorn \
            --bind $HOST:$PORT \
            --workers 4 \
            --timeout 120 \
            --certfile ${SSL_CERT_PATH:-certs/cert.pem} \
            --keyfile ${SSL_KEY_PATH:-certs/key.pem} \
            --access-logfile - \
            --error-logfile - \
            "backend.app:app"
    else
        gunicorn \
            --bind $HOST:$PORT \
            --workers 4 \
            --timeout 120 \
            --access-logfile - \
            --error-logfile - \
            "backend.app:app"
    fi
else
    echo "⚠️  Gunicorn no está instalado, usando servidor de desarrollo"
    python3 backend/app.py
fi
