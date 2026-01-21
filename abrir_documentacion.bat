@echo off
echo Abriendo documentación...
echo.

start notepad LEEME_PRIMERO.txt
timeout /t 1 /nobreak >nul

start notepad RESUMEN_DEPLOY.txt
timeout /t 1 /nobreak >nul

start notepad PASOS_DEPLOY_RAILWAY.md
timeout /t 1 /nobreak >nul

echo.
echo ✓ Documentación abierta
echo.
echo Archivos disponibles:
echo   - LEEME_PRIMERO.txt (inicio rápido)
echo   - RESUMEN_DEPLOY.txt (resumen ejecutivo)
echo   - PASOS_DEPLOY_RAILWAY.md (guía detallada)
echo   - SEGURIDAD_POST_DEPLOY.md (seguridad)
echo.
pause
