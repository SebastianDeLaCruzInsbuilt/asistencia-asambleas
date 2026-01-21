@echo off
REM Script de inicio para producción (Windows)
REM Sistema de Confirmación de Asistencia a Asambleas

echo ========================================
echo Sistema de Confirmacion de Asistencia
echo Modo: PRODUCCION
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    pause
    exit /b 1
)

REM Configurar variables de entorno
set FLASK_ENV=production
if not defined HOST set HOST=0.0.0.0
if not defined PORT set PORT=5000
if not defined SSL_ENABLED set SSL_ENABLED=false

REM Verificar si se debe usar SSL
if /i "%SSL_ENABLED%"=="true" (
    echo [SSL] Modo HTTPS habilitado
    
    REM Verificar que existan los certificados
    if not exist "certs\cert.pem" (
        echo [SSL] Certificados SSL no encontrados
        echo [SSL] Generando certificados autofirmados...
        python generar_certificados.py
        echo.
    )
    
    set PROTOCOL=https
) else (
    echo [HTTP] Modo HTTP sin SSL
    set PROTOCOL=http
)

echo.
echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo.

echo Iniciando servidor de produccion...
echo.
echo Servidor disponible en: %PROTOCOL%://%HOST%:%PORT%
echo.
echo - Confirmacion de asistencia: %PROTOCOL%://%HOST%:%PORT%
echo - Panel administrativo: %PROTOCOL%://%HOST%:%PORT%/admin.html
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
echo ========================================
echo.

REM Usar Waitress en Windows (mejor que el servidor de desarrollo)
if /i "%SSL_ENABLED%"=="true" (
    echo NOTA: Waitress no soporta SSL directamente
    echo Usar un proxy reverso como nginx para SSL en produccion
    echo Iniciando en modo HTTP...
    waitress-serve --host=%HOST% --port=%PORT% --threads=4 backend.app:app
) else (
    waitress-serve --host=%HOST% --port=%PORT% --threads=4 backend.app:app
)

pause
