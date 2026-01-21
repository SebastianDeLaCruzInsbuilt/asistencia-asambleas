# Deploy a Railway - Script PowerShell
# Sistema de Asistencia a Asambleas

# Agregar Git al PATH
$env:Path += ";C:\Program Files\Git\cmd"

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🚀 DEPLOY AUTOMÁTICO A RAILWAY                           ║" -ForegroundColor Cyan
Write-Host "║  Sistema de Asistencia a Asambleas                        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ============================================
# PASO 1: Verificar Git
# ============================================
Write-Host "[1/6] Verificando Git..." -ForegroundColor Yellow

try {
    $gitVersion = git --version
    Write-Host "✓ Git detectado correctamente" -ForegroundColor Green
    Write-Host "  $gitVersion" -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "❌ ERROR: Git no está disponible" -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUCIÓN:" -ForegroundColor Yellow
    Write-Host "1. Reinicia tu computadora"
    Write-Host "2. Ejecuta este script de nuevo"
    Write-Host ""
    Read-Host "Presiona ENTER para salir"
    exit 1
}

# ============================================
# PASO 2: Configurar Git
# ============================================
Write-Host "[2/6] Configurando Git..." -ForegroundColor Yellow
Write-Host ""

$gitName = Read-Host "Ingresa tu NOMBRE COMPLETO (ejemplo: Juan Perez)"
$gitEmail = Read-Host "Ingresa tu EMAIL (ejemplo: juan.perez@empresa.com)"

git config --global user.name "$gitName"
git config --global user.email "$gitEmail"

Write-Host ""
Write-Host "✓ Git configurado:" -ForegroundColor Green
Write-Host "  Nombre: $gitName" -ForegroundColor Gray
Write-Host "  Email: $gitEmail" -ForegroundColor Gray
Write-Host ""
Read-Host "Presiona ENTER para continuar"

# ============================================
# PASO 3: Inicializar Repositorio
# ============================================
Write-Host ""
Write-Host "[3/6] Inicializando repositorio Git..." -ForegroundColor Yellow

if (Test-Path ".git") {
    Write-Host "⚠ Ya existe un repositorio Git" -ForegroundColor Yellow
    $reinit = Read-Host "¿Deseas reinicializarlo? (S/N)"
    if ($reinit -eq "S" -or $reinit -eq "s") {
        Remove-Item -Recurse -Force .git
        git init
        Write-Host "✓ Repositorio reinicializado" -ForegroundColor Green
    } else {
        Write-Host "✓ Usando repositorio existente" -ForegroundColor Green
    }
} else {
    git init
    Write-Host "✓ Repositorio inicializado" -ForegroundColor Green
}

Write-Host ""
Write-Host "Agregando archivos..." -ForegroundColor Gray
git add .
Write-Host "✓ Archivos agregados" -ForegroundColor Green

Write-Host ""
Write-Host "Haciendo commit inicial..." -ForegroundColor Gray
try {
    git commit -m "Initial commit - Sistema de Asistencia a Asambleas"
    Write-Host "✓ Commit realizado" -ForegroundColor Green
} catch {
    Write-Host "⚠ No hay cambios para commitear o ya existe un commit" -ForegroundColor Yellow
}
Write-Host ""
Read-Host "Presiona ENTER para continuar"

# ============================================
# PASO 4: Conectar con GitHub
# ============================================
Write-Host ""
Write-Host "[4/6] Conectando con GitHub..." -ForegroundColor Yellow
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  INSTRUCCIONES PARA CREAR REPOSITORIO EN GITHUB           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Ve a: https://github.com/new" -ForegroundColor White
Write-Host "2. Nombre del repo: asistencia-asambleas (o el que prefieras)" -ForegroundColor White
Write-Host "3. Visibilidad: Private (recomendado) o Public" -ForegroundColor White
Write-Host "4. NO marques: README, .gitignore, o license" -ForegroundColor White
Write-Host "5. Click en 'Create repository'" -ForegroundColor White
Write-Host ""
Read-Host "Presiona ENTER cuando hayas creado el repositorio"

Write-Host ""
$githubUser = Read-Host "Ingresa tu USUARIO de GitHub"
$repoName = Read-Host "Ingresa el NOMBRE del repositorio (ejemplo: asistencia-asambleas)"

Write-Host ""
Write-Host "Conectando con GitHub..." -ForegroundColor Gray
git remote remove origin 2>$null
git remote add origin "https://github.com/$githubUser/$repoName.git"
git branch -M main

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  SUBIENDO CÓDIGO A GITHUB                                 ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "GitHub te pedirá autenticación." -ForegroundColor Yellow
Write-Host ""
Write-Host "OPCIONES DE AUTENTICACIÓN:" -ForegroundColor White
Write-Host "  1. Usuario y contraseña (si tienes 2FA, necesitas token)" -ForegroundColor Gray
Write-Host "  2. Personal Access Token (recomendado)" -ForegroundColor Gray
Write-Host ""
Write-Host "Para crear un token:" -ForegroundColor White
Write-Host "  - Ve a: https://github.com/settings/tokens" -ForegroundColor Gray
Write-Host "  - Click en 'Generate new token (classic)'" -ForegroundColor Gray
Write-Host "  - Selecciona 'repo' scope" -ForegroundColor Gray
Write-Host "  - Copia el token y úsalo como contraseña" -ForegroundColor Gray
Write-Host ""
Read-Host "Presiona ENTER para continuar"

Write-Host ""
Write-Host "Subiendo código..." -ForegroundColor Gray
try {
    git push -u origin main
    Write-Host ""
    Write-Host "✓ Código subido exitosamente a GitHub!" -ForegroundColor Green
    Write-Host "  URL: https://github.com/$githubUser/$repoName" -ForegroundColor Gray
} catch {
    Write-Host ""
    Write-Host "❌ Error al subir a GitHub" -ForegroundColor Red
    Write-Host ""
    Write-Host "POSIBLES CAUSAS:" -ForegroundColor Yellow
    Write-Host "  - Usuario o contraseña incorrectos" -ForegroundColor Gray
    Write-Host "  - Necesitas usar Personal Access Token" -ForegroundColor Gray
    Write-Host "  - El repositorio ya existe con contenido" -ForegroundColor Gray
    Write-Host ""
    Write-Host "SOLUCIÓN:" -ForegroundColor Yellow
    Write-Host "  1. Verifica tus credenciales" -ForegroundColor Gray
    Write-Host "  2. Usa un Personal Access Token en lugar de contraseña" -ForegroundColor Gray
    Write-Host "  3. Asegúrate de que el repositorio esté vacío" -ForegroundColor Gray
    Write-Host ""
    Read-Host "Presiona ENTER para salir"
    exit 1
}
Write-Host ""
Read-Host "Presiona ENTER para continuar"

# ============================================
# PASO 5: Instrucciones para Railway
# ============================================
Write-Host ""
Write-Host "[5/6] Deploy en Railway..." -ForegroundColor Yellow
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  AHORA SIGUE ESTOS PASOS EN RAILWAY:                      ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Ve a: https://railway.app" -ForegroundColor White
Write-Host ""
Write-Host "2. Click en 'Login' y autentícate con GitHub" -ForegroundColor White
Write-Host ""
Write-Host "3. Click en 'New Project'" -ForegroundColor White
Write-Host ""
Write-Host "4. Selecciona 'Deploy from GitHub repo'" -ForegroundColor White
Write-Host ""
Write-Host "5. Autoriza Railway para acceder a tus repositorios" -ForegroundColor White
Write-Host ""
Write-Host "6. Selecciona tu repositorio: $repoName" -ForegroundColor White
Write-Host ""
Write-Host "7. Railway detectará automáticamente:" -ForegroundColor White
Write-Host "   - Python" -ForegroundColor Gray
Write-Host "   - requirements.txt" -ForegroundColor Gray
Write-Host "   - Procfile" -ForegroundColor Gray
Write-Host "   - railway.json" -ForegroundColor Gray
Write-Host ""
Write-Host "8. Espera 2-5 minutos mientras se despliega" -ForegroundColor White
Write-Host "   (Verás logs en tiempo real)" -ForegroundColor Gray
Write-Host ""
Write-Host "9. Cuando termine, ve a Settings > Domains" -ForegroundColor White
Write-Host ""
Write-Host "10. Click en 'Generate Domain'" -ForegroundColor White
Write-Host ""
Write-Host "11. Railway te dará una URL como:" -ForegroundColor White
Write-Host "    https://$repoName-production.up.railway.app" -ForegroundColor Cyan
Write-Host ""
Write-Host ""
Read-Host "Presiona ENTER cuando hayas completado el deploy en Railway"

# ============================================
# PASO 6: Finalización
# ============================================
Write-Host ""
Write-Host "[6/6] ¡Deploy completado!" -ForegroundColor Yellow
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ TODO LISTO                                            ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Tu aplicación está desplegada en Railway con:" -ForegroundColor White
Write-Host ""
Write-Host "✓ HTTPS automático" -ForegroundColor Green
Write-Host "✓ Dominio gratuito .railway.app" -ForegroundColor Green
Write-Host "✓ Deploy automático con cada push" -ForegroundColor Green
Write-Host "✓ `$5 USD gratis/mes" -ForegroundColor Green
Write-Host "✓ Logs en tiempo real" -ForegroundColor Green
Write-Host "✓ Capacidad para 800-1000 usuarios/minuto" -ForegroundColor Green
Write-Host ""
Write-Host "────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "PRÓXIMOS PASOS:" -ForegroundColor Yellow
Write-Host "────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""
Write-Host "1. Abre tu URL de Railway en el navegador" -ForegroundColor White
Write-Host ""
Write-Host "2. Prueba el login admin:" -ForegroundColor White
Write-Host "   Usuario: admin" -ForegroundColor Gray
Write-Host "   Password: admin123" -ForegroundColor Gray
Write-Host ""
Write-Host "3. ⚠️  IMPORTANTE: Cambia la contraseña inmediatamente" -ForegroundColor Red
Write-Host "   (Usa el botón '🔑 Cambiar Contraseña' en el panel admin)" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Configura la ubicación de la asamblea" -ForegroundColor White
Write-Host ""
Write-Host "5. Importa usuarios desde CSV" -ForegroundColor White
Write-Host ""
Write-Host "6. Para actualizar la app en el futuro:" -ForegroundColor White
Write-Host "   git add ." -ForegroundColor Gray
Write-Host "   git commit -m 'Descripción de cambios'" -ForegroundColor Gray
Write-Host "   git push" -ForegroundColor Gray
Write-Host ""
Write-Host "────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""
Write-Host "Repositorio GitHub:" -ForegroundColor White
Write-Host "https://github.com/$githubUser/$repoName" -ForegroundColor Cyan
Write-Host ""
Write-Host "Railway Dashboard:" -ForegroundColor White
Write-Host "https://railway.app/dashboard" -ForegroundColor Cyan
Write-Host ""
Write-Host "Documentación de seguridad:" -ForegroundColor White
Write-Host "Lee: SEGURIDAD_POST_DEPLOY.md" -ForegroundColor Gray
Write-Host ""
Write-Host "────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""
Write-Host "¡Éxito! 🚀" -ForegroundColor Green
Write-Host ""
Read-Host "Presiona ENTER para salir"
