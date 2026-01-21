# 🚀 Instrucciones de Deploy en Railway

## Paso 1: Subir a GitHub (5 minutos)

### Opción A: Desde GitHub Web (SIN GIT LOCAL)

1. **Crear repositorio en GitHub:**
   - Ve a https://github.com/new
   - Nombre: `asistencia-asamblea`
   - Descripción: `Sistema de confirmación de asistencia a asambleas`
   - Visibilidad: Privado (recomendado) o Público
   - ✅ NO inicialices con README (ya lo tienes)
   - Clic en "Create repository"

2. **Subir archivos:**
   - En la página del repositorio, clic en "uploading an existing file"
   - Arrastra TODA la carpeta del proyecto (excepto `lightsail/`, `cdk/`, `*.pem`)
   - O selecciona los archivos manualmente
   - Commit message: "Initial commit - Sistema de asistencia"
   - Clic en "Commit changes"

### Opción B: Desde Git CLI (SI TIENES GIT)

```bash
# Inicializar repositorio
git init

# Agregar archivos
git add .

# Commit inicial
git commit -m "Initial commit - Sistema de asistencia"

# Conectar con GitHub
git remote add origin https://github.com/TU_USUARIO/asistencia-asamblea.git

# Subir código
git branch -M main
git push -u origin main
```

---

## Paso 2: Deploy en Railway (2 minutos)

1. **Crear cuenta en Railway:**
   - Ve a https://railway.app
   - Clic en "Login" → "Login with GitHub"
   - Autoriza Railway a acceder a tus repositorios

2. **Crear nuevo proyecto:**
   - Clic en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Busca y selecciona `asistencia-asamblea`
   - Railway detectará automáticamente que es una app Flask

3. **Configurar variables de entorno (opcional):**
   - En el dashboard del proyecto, ve a "Variables"
   - Agrega si necesitas:
     - `FLASK_ENV=production`
     - `PORT=5000` (Railway lo configura automáticamente)

4. **Esperar el deploy:**
   - Railway construye y despliega automáticamente
   - Toma 2-3 minutos
   - Verás los logs en tiempo real

5. **Obtener tu URL:**
   - En "Settings" → "Domains"
   - Clic en "Generate Domain"
   - Tu app estará en: `https://tu-app.railway.app`

---

## Paso 3: Configuración Inicial

1. **Acceder al panel admin:**
   - Ve a `https://tu-app.railway.app/admin.html`
   - Usuario: `admin`
   - Contraseña: `admin123`

2. **Cambiar contraseña:**
   - Clic en el botón 🔑 "Cambiar Contraseña"
   - Ingresa contraseña actual y nueva
   - Guarda los cambios

3. **Configurar ubicación:**
   - En el panel admin, baja a "Configuración de Ubicación"
   - Ingresa latitud y longitud de tu asamblea
   - Configura el radio permitido (en metros)
   - Guarda

4. **Cargar usuarios:**
   - Opción A: Agregar uno por uno
   - Opción B: Carga masiva desde CSV

---

## 🎯 URLs Importantes

- **App principal:** `https://tu-app.railway.app`
- **Panel admin:** `https://tu-app.railway.app/admin.html`
- **Login admin:** `https://tu-app.railway.app/login.html`

---

## 📊 Monitoreo

En el dashboard de Railway puedes ver:
- Logs en tiempo real
- Uso de CPU y RAM
- Requests por segundo
- Costos estimados

---

## 💰 Costos

- **Primeros $5:** Gratis cada mes
- **Después:** ~$0.000231/GB-hora
- **Estimado para 1000 usuarios/mes:** $10-15/mes

---

## 🔄 Actualizaciones Automáticas

Cada vez que hagas push a GitHub:
1. Railway detecta el cambio
2. Construye la nueva versión
3. Despliega automáticamente
4. Sin downtime (zero-downtime deployment)

---

## 🆘 Troubleshooting

### La app no inicia
- Revisa los logs en Railway dashboard
- Verifica que `requirements.txt` esté completo
- Asegúrate de que `Procfile` esté en la raíz

### Error 502 Bad Gateway
- La app está iniciando, espera 1-2 minutos
- Revisa los logs para ver errores de Python

### No puedo acceder al admin
- Verifica que la URL sea correcta: `/admin.html`
- Limpia caché del navegador
- Prueba en modo incógnito

---

## 📞 Soporte

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Crea un issue en tu repositorio

---

¡Listo! Tu aplicación estará funcionando en menos de 10 minutos 🚀
