# 📍 Sistema de Confirmación de Asistencia a Asambleas

Sistema web para confirmar asistencia a asambleas mediante validación de identidad y ubicación geográfica.

> **Nota:** Este workspace contiene dos proyectos. Ver [WORKSPACE_STRUCTURE.md](WORKSPACE_STRUCTURE.md) para más detalles.

## 🚀 Deploy Rápido en Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## ✨ Características

- ✅ Validación de identidad por documento
- ✅ Verificación de ubicación geográfica (GPS)
- ✅ Panel administrativo con autenticación JWT
- ✅ Carga masiva de usuarios desde CSV
- ✅ Configuración de ubicación de asamblea
- ✅ Gestión de asistencias en tiempo real
- ✅ HTTPS incluido

## 🛠️ Tecnologías

- **Backend:** Python 3.11 + Flask
- **Frontend:** HTML5 + JavaScript vanilla
- **Almacenamiento:** JSON (fácil migración a PostgreSQL)
- **Deploy:** Railway.app

## 📦 Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/TU_USUARIO/asistencia-asamblea.git
cd asistencia-asamblea

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python backend/app.py
```

## 🌐 Deploy en Railway

1. Haz fork de este repositorio
2. Ve a [railway.app](https://railway.app)
3. Conecta tu cuenta de GitHub
4. Selecciona este repositorio
5. ¡Listo! Railway despliega automáticamente

## 🔐 Credenciales por Defecto

- **Usuario:** admin
- **Contraseña:** admin123

⚠️ **IMPORTANTE:** Cambia la contraseña después del primer login

## 📝 Configuración

La aplicación se configura automáticamente. Para personalizar:

1. **Ubicación de la asamblea:** Panel Admin → Configuración de Ubicación
2. **Usuarios autorizados:** Panel Admin → Agregar Usuario o Carga CSV
3. **Radio permitido:** Panel Admin → Configuración de Ubicación

## 🎯 Uso

### Para Usuarios
1. Accede a la URL de tu aplicación
2. Ingresa tu documento de identidad
3. Permite acceso a tu ubicación
4. Confirma tu asistencia

### Para Administradores
1. Accede a `/admin.html`
2. Inicia sesión con tus credenciales
3. Gestiona usuarios y visualiza asistencias

## 📊 Rendimiento

- Soporta hasta 800-1000 usuarios concurrentes
- Escalado automático disponible en Railway
- Optimizado con Gunicorn (4 workers)

## 🔒 Seguridad

- Autenticación JWT para administradores
- Tokens con expiración de 8 horas
- Validación de coordenadas geográficas
- HTTPS obligatorio en producción

## 📄 Licencia

MIT License

---

## 📚 Documentación Adicional

- [Estructura del Workspace](WORKSPACE_STRUCTURE.md) - Organización de ambos proyectos
- [Guía de Inicio Rápido](QUICK_START.md) - Comandos esenciales
- [Resumen de Limpieza](CLEANUP_SUMMARY.md) - Cambios recientes en el workspace
- [Analizador .NET](dotnet-code-analyzer/README.md) - Documentación del segundo proyecto
