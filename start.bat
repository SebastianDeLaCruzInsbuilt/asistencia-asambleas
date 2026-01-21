@echo off
REM Script de inicio para Windows
REM Sistema de Confirmación de Asistencia a Asambleas

echo ========================================
echo Sistema de Confirmacion de Asistencia
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8 o superior desde https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Verificando Python...
python --version
echo.

echo [2/3] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo.

echo [3/3] Iniciando servidor...
echo.
echo El servidor se iniciara en: http://localhost:5000
echo.
echo - Confirmacion de asistencia: http://localhost:5000
echo - Panel administrativo: http://localhost:5000/admin.html
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
echo ========================================
echo.

python backend/app.py

pause
