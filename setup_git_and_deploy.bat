@echo off
echo ========================================
echo Configurando Git y preparando deploy
echo ========================================
echo.

REM Verificar que Git está instalado
git --version
if %errorlevel% neq 0 (
    echo ERROR: Git no está instalado o no está en el PATH
    echo Por favor reinicia PowerShell/CMD y ejecuta este script de nuevo
    pause
    exit /b 1
)

echo.
echo Git detectado correctamente!
echo.

REM Configurar Git con tu información
echo Configurando Git...
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"

echo.
echo IMPORTANTE: Edita este script y cambia "Tu Nombre" y "tu.email@ejemplo.com"
echo con tu información real antes de continuar.
echo.
pause

REM Inicializar repositorio Git
echo.
echo Inicializando repositorio Git...
git init

REM Agregar todos los archivos
echo.
echo Agregando archivos al repositorio...
git add .

REM Hacer commit inicial
echo.
echo Haciendo commit inicial...
git commit -m "Initial commit - Sistema de Asistencia a Asambleas"

echo.
echo ========================================
echo Git configurado exitosamente!
echo ========================================
echo.
echo PROXIMOS PASOS:
echo.
echo 1. Crea un repositorio en GitHub:
echo    - Ve a https://github.com/new
echo    - Nombre: asistencia-asambleas (o el que prefieras)
echo    - NO inicialices con README, .gitignore o licencia
echo.
echo 2. Conecta tu repositorio local con GitHub:
echo    git remote add origin https://github.com/TU_USUARIO/asistencia-asambleas.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Conecta Railway con GitHub:
echo    - Ve a https://railway.app
echo    - Crea cuenta con GitHub
echo    - New Project ^> Deploy from GitHub repo
echo    - Selecciona tu repositorio
echo    - Railway detectará automáticamente la configuración
echo.
echo 4. Configura variables de entorno en Railway (opcional):
echo    - FLASK_ENV=production
echo    - SECRET_KEY=tu-clave-secreta-aqui
echo.
echo 5. Railway te dará una URL como: https://tu-app.railway.app
echo.
pause
