# 🚀 Deploy a Railway - Guía Paso a Paso

## ⚠️ PASO 0: Reiniciar PowerShell

**IMPORTANTE**: Git fue instalado pero PowerShell necesita reiniciarse para reconocerlo.

1. **Cierra esta ventana de PowerShell/Terminal**
2. **Abre una NUEVA ventana de PowerShell/Terminal**
3. **Navega a este directorio de nuevo**
4. **Continúa con el Paso 1**

---

## ✅ PASO 1: Verificar Git

Ejecuta en PowerShell:

```powershell
.\verificar_git.bat
```

Si Git está instalado correctamente, verás: `✓ Git esta instalado correctamente!`

Si no, reinicia tu computadora y vuelve a intentar.

---

## 🔧 PASO 2: Configurar Git

Ejecuta estos comandos UNO POR UNO (reemplaza con tu información real):

```powershell
git config --global user.name "Tu Nombre Completo"
git config --global user.email "tu.email@ejemplo.com"
```

**Ejemplo:**
```powershell
git config --global user.name "Juan Perez"
git config --global user.email "juan.perez@empresa.com"
```

Verifica la configuración:
```powershell
git config --global --list
```

---

## 📦 PASO 3: Inicializar Repositorio Git

```powershell
git init
git add .
git commit -m "Initial commit - Sistema de Asistencia"
```

---

## 🌐 PASO 4: Crear Repositorio en GitHub

1. Ve a: https://github.com/new
2. **Nombre del repositorio**: `asistencia-asambleas` (o el que prefieras)
3. **Descripción**: "Sistema de Asistencia a Asambleas"
4. **Visibilidad**: Private (recomendado) o Public
5. ⚠️ **NO marques**: "Add a README file", "Add .gitignore", "Choose a license"
6. Click en **"Create repository"**

---

## 🔗 PASO 5: Conectar con GitHub

GitHub te mostrará comandos. Copia y ejecuta estos (reemplaza TU_USUARIO):

```powershell
git remote add origin https://github.com/TU_USUARIO/asistencia-asambleas.git
git branch -M main
git push -u origin main
```

**Ejemplo:**
```powershell
git remote add origin https://github.com/juanperez/asistencia-asambleas.git
git branch -M main
git push -u origin main
```

Te pedirá autenticación de GitHub. Usa tu usuario y contraseña (o token personal).

---

## 🚂 PASO 6: Deploy en Railway

### 6.1 Crear Cuenta en Railway

1. Ve a: https://railway.app
2. Click en **"Login"** o **"Start a New Project"**
3. **Autentícate con GitHub** (recomendado)

### 6.2 Crear Nuevo Proyecto

1. Click en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Si es la primera vez, Railway pedirá permisos para acceder a tus repositorios
4. Autoriza Railway en GitHub
5. Selecciona el repositorio **`asistencia-asambleas`**

### 6.3 Railway Detectará Automáticamente

Railway detectará:
- ✅ Python
- ✅ `Procfile` (comando de inicio)
- ✅ `requirements.txt` (dependencias)
- ✅ `railway.json` (configuración)

### 6.4 Esperar Deploy

- El deploy toma **2-5 minutos**
- Verás logs en tiempo real
- Cuando termine, verás: **"Success"** o **"Deployed"**

### 6.5 Obtener URL

1. En el dashboard de Railway, click en tu proyecto
2. Ve a la pestaña **"Settings"**
3. Busca **"Domains"**
4. Click en **"Generate Domain"**
5. Railway te dará una URL como: `https://asistencia-asambleas-production.up.railway.app`

---

## 🔐 PASO 7: Configurar Variables de Entorno (Opcional)

En Railway dashboard:

1. Ve a tu proyecto
2. Click en **"Variables"**
3. Agrega estas variables:

```
FLASK_ENV=production
SECRET_KEY=tu-clave-secreta-super-segura-aqui-123456
```

4. Click en **"Add"** para cada variable
5. Railway redesplegará automáticamente

---

## ✅ PASO 8: Probar la Aplicación

1. Abre la URL de Railway en tu navegador
2. Deberías ver la página de inicio del sistema de asistencia
3. Prueba el login admin:
   - Usuario: `admin`
   - Contraseña: `admin123`

---

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real

En Railway dashboard:
1. Click en tu proyecto
2. Ve a la pestaña **"Deployments"**
3. Click en el deployment activo
4. Verás logs en tiempo real

### Métricas

Railway muestra automáticamente:
- CPU usage
- Memory usage
- Network traffic
- Request count

---

## 🔄 Actualizar la Aplicación

Cuando hagas cambios en el código:

```powershell
git add .
git commit -m "Descripción de los cambios"
git push
```

Railway detectará el push y redesplegará automáticamente en **1-2 minutos**.

---

## 💰 Costos

- **$5 USD gratis/mes** (suficiente para desarrollo y pruebas)
- Después de $5: **$0.000463 por GB-hora** (~$10-15/mes para uso moderado)
- **Sin cargos ocultos**
- **Puedes pausar el proyecto** cuando no lo uses

---

## 🆘 Solución de Problemas

### Error: "Git not found"
- Reinicia PowerShell
- Si persiste, reinicia tu computadora

### Error: "Permission denied" en GitHub
- Verifica tu usuario y contraseña
- Considera usar un Personal Access Token: https://github.com/settings/tokens

### Error en Railway: "Build failed"
- Revisa los logs en Railway dashboard
- Verifica que `requirements.txt` esté correcto
- Verifica que `Procfile` esté correcto

### La aplicación no carga
- Verifica que Railway haya generado el dominio
- Espera 2-3 minutos después del deploy
- Revisa los logs en Railway

---

## 📞 Soporte

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Crea un issue en tu repositorio

---

## 🎉 ¡Listo!

Tu aplicación está desplegada en Railway con:
- ✅ HTTPS automático
- ✅ Dominio gratuito `.railway.app`
- ✅ Deploy automático con cada push
- ✅ $5 USD gratis/mes
- ✅ Escalado automático
- ✅ Logs en tiempo real

**URL de ejemplo**: `https://asistencia-asambleas-production.up.railway.app`

---

**Tiempo total estimado**: 15-20 minutos
