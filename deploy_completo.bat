@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  🚀 DEPLOY AUTOMÁTICO A RAILWAY                           ║
echo ║  Sistema de Asistencia a Asambleas                        ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM ============================================
REM PASO 1: Verificar Git
REM ============================================
echo [1/6] Verificando Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Git no está disponible
    echo.
    echo SOLUCIÓN:
    echo 1. Cierra esta ventana
    echo 2. Abre una NUEVA ventana de PowerShell/CMD
    echo 3. Ejecuta este script de nuevo
    echo.
    echo Si el problema persiste, reinicia tu computadora.
    pause
    exit /b 1
)
echo ✓ Git detectado correctamente
echo.

REM ============================================
REM PASO 2: Configurar Git
REM ============================================
echo [2/6] Configurando Git...
echo.
echo Ingresa tu NOMBRE COMPLETO (ejemplo: Juan Perez):
set /p GIT_NAME="> "

echo.
echo Ingresa tu EMAIL (ejemplo: juan.perez@empresa.com):
set /p GIT_EMAIL="> "

git config --global user.name "%GIT_NAME%"
git config --global user.email "%GIT_EMAIL%"

echo.
echo ✓ Git configurado:
echo   Nombre: %GIT_NAME%
echo   Email: %GIT_EMAIL%
echo.
pause

REM ============================================
REM PASO 3: Inicializar Repositorio
REM ============================================
echo.
echo [3/6] Inicializando repositorio Git...

REM Verificar si ya existe un repositorio
if exist .git (
    echo ⚠ Ya existe un repositorio Git
    echo ¿Deseas reinicializarlo? (S/N)
    set /p REINIT="> "
    if /i "%REINIT%"=="S" (
        rmdir /s /q .git
        git init
        echo ✓ Repositorio reinicializado
    ) else (
        echo ✓ Usando repositorio existente
    )
) else (
    git init
    echo ✓ Repositorio inicializado
)

echo.
echo Agregando archivos...
git add .
echo ✓ Archivos agregados

echo.
echo Haciendo commit inicial...
git commit -m "Initial commit - Sistema de Asistencia a Asambleas"
if %errorlevel% equ 0 (
    echo ✓ Commit realizado
) else (
    echo ⚠ No hay cambios para commitear o ya existe un commit
)
echo.
pause

REM ============================================
REM PASO 4: Conectar con GitHub
REM ============================================
echo.
echo [4/6] Conectando con GitHub...
echo.
echo INSTRUCCIONES:
echo 1. Ve a: https://github.com/new
echo 2. Nombre del repo: asistencia-asambleas (o el que prefieras)
echo 3. NO marques: README, .gitignore, o license
echo 4. Click en "Create repository"
echo.
echo Presiona ENTER cuando hayas creado el repositorio...
pause >nul

echo.
echo Ingresa tu USUARIO de GitHub:
set /p GITHUB_USER="> "

echo.
echo Ingresa el NOMBRE del repositorio (ejemplo: asistencia-asambleas):
set /p REPO_NAME="> "

echo.
echo Conectando con GitHub...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git
git branch -M main

echo.
echo Subiendo código a GitHub...
echo (Te pedirá autenticación de GitHub)
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✓ Código subido exitosamente a GitHub!
    echo   URL: https://github.com/%GITHUB_USER%/%REPO_NAME%
) else (
    echo.
    echo ❌ Error al subir a GitHub
    echo Verifica tu usuario, contraseña y nombre del repositorio
    pause
    exit /b 1
)
echo.
pause

REM ============================================
REM PASO 5: Instrucciones para Railway
REM ============================================
echo.
echo [5/6] Deploy en Railway...
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  AHORA SIGUE ESTOS PASOS EN RAILWAY:                      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 1. Ve a: https://railway.app
echo.
echo 2. Click en "Login" y autentícate con GitHub
echo.
echo 3. Click en "New Project"
echo.
echo 4. Selecciona "Deploy from GitHub repo"
echo.
echo 5. Selecciona tu repositorio: %REPO_NAME%
echo.
echo 6. Railway detectará automáticamente la configuración
echo.
echo 7. Espera 2-5 minutos mientras se despliega
echo.
echo 8. Ve a Settings ^> Domains ^> Generate Domain
echo.
echo 9. Railway te dará una URL como:
echo    https://%REPO_NAME%-production.up.railway.app
echo.
echo.
echo Presiona ENTER cuando hayas completado el deploy en Railway...
pause >nul

REM ============================================
REM PASO 6: Finalización
REM ============================================
echo.
echo [6/6] ¡Deploy completado!
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  ✅ TODO LISTO                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Tu aplicación está desplegada en Railway con:
echo.
echo ✓ HTTPS automático
echo ✓ Dominio gratuito .railway.app
echo ✓ Deploy automático con cada push
echo ✓ $5 USD gratis/mes
echo ✓ Logs en tiempo real
echo.
echo ────────────────────────────────────────────────────────────
echo PRÓXIMOS PASOS:
echo ────────────────────────────────────────────────────────────
echo.
echo 1. Abre tu URL de Railway en el navegador
echo.
echo 2. Prueba el login admin:
echo    Usuario: admin
echo    Password: admin123
echo.
echo 3. Para actualizar la app en el futuro:
echo    git add .
echo    git commit -m "Descripción de cambios"
echo    git push
echo.
echo ────────────────────────────────────────────────────────────
echo.
echo Repositorio GitHub:
echo https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
echo Railway Dashboard:
echo https://railway.app/dashboard
echo.
echo ────────────────────────────────────────────────────────────
echo.
pause
