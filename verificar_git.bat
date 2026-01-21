@echo off
echo Verificando instalacion de Git...
echo.

git --version
if %errorlevel% equ 0 (
    echo.
    echo ✓ Git esta instalado correctamente!
    echo.
    echo Ahora puedes ejecutar: setup_git_and_deploy.bat
) else (
    echo.
    echo ✗ Git NO esta disponible
    echo.
    echo SOLUCION:
    echo 1. Cierra esta ventana de PowerShell/CMD
    echo 2. Abre una NUEVA ventana de PowerShell/CMD
    echo 3. Ejecuta este script de nuevo
    echo.
    echo Si el problema persiste, reinicia tu computadora.
)

echo.
pause
