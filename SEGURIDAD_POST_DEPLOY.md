# 🔐 Seguridad Post-Deploy

## ⚠️ IMPORTANTE: Cambiar Credenciales Después del Deploy

Tu aplicación se desplegó con credenciales por defecto:
- **Usuario**: `admin`
- **Password**: `admin123`

**DEBES cambiar estas credenciales inmediatamente** para proteger tu aplicación.

---

## 🔑 Cambiar Contraseña desde el Panel Admin

### Opción 1: Desde la Interfaz Web (RECOMENDADO)

1. Accede a tu aplicación en Railway:
   ```
   https://tu-app.railway.app/login.html
   ```

2. Inicia sesión con las credenciales por defecto:
   - Usuario: `admin`
   - Password: `admin123`

3. En el panel admin, busca el botón **"🔑 Cambiar Contraseña"** en la esquina superior derecha

4. Ingresa:
   - Contraseña actual: `admin123`
   - Nueva contraseña: (tu contraseña segura)
   - Confirmar contraseña: (repite tu contraseña segura)

5. Click en **"Cambiar Contraseña"**

6. Serás desconectado automáticamente

7. Vuelve a iniciar sesión con tu nueva contraseña

---

## 🔒 Recomendaciones de Seguridad

### Contraseña Segura

Tu contraseña debe:
- ✅ Tener al menos 12 caracteres
- ✅ Incluir mayúsculas y minúsculas
- ✅ Incluir números
- ✅ Incluir caracteres especiales (!@#$%^&*)
- ❌ NO usar palabras comunes
- ❌ NO usar información personal

**Ejemplo de contraseña segura**: `Asist3nc!a#2026$Segur@`

### Cambiar Credenciales Localmente (Opcional)

Si quieres cambiar las credenciales en tu código local:

1. Edita `data/admin_credentials.json`:
   ```json
   {
     "username": "admin",
     "password": "tu_nueva_contraseña_super_segura"
   }
   ```

2. Haz commit y push:
   ```powershell
   git add data/admin_credentials.json
   git commit -m "Actualizar credenciales admin"
   git push
   ```

3. Railway redesplegará automáticamente con las nuevas credenciales

---

## 🛡️ Otras Medidas de Seguridad

### 1. Configurar Variables de Entorno en Railway

En lugar de guardar credenciales en archivos, usa variables de entorno:

1. Ve a Railway Dashboard
2. Selecciona tu proyecto
3. Ve a **"Variables"**
4. Agrega:
   ```
   ADMIN_USERNAME=tu_usuario_admin
   ADMIN_PASSWORD=tu_contraseña_super_segura
   ```

5. Modifica `backend/app.py` para leer de variables de entorno:
   ```python
   import os
   
   # En lugar de leer de archivo:
   ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
   ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
   ```

### 2. Habilitar Autenticación de Dos Factores (2FA)

Considera implementar 2FA para mayor seguridad:
- Google Authenticator
- SMS
- Email

### 3. Limitar Intentos de Login

Implementa rate limiting para prevenir ataques de fuerza bruta:
- Máximo 5 intentos por minuto
- Bloqueo temporal después de 10 intentos fallidos

### 4. Logs de Auditoría

Registra todos los accesos administrativos:
- Fecha y hora
- IP del usuario
- Acciones realizadas

### 5. HTTPS Obligatorio

Railway ya proporciona HTTPS automáticamente, pero asegúrate de:
- ✅ Siempre usar `https://` en la URL
- ✅ Nunca compartir la URL sin HTTPS
- ✅ Configurar redirección HTTP → HTTPS si es necesario

---

## 🚨 En Caso de Compromiso

Si sospechas que tus credenciales fueron comprometidas:

1. **Cambia la contraseña inmediatamente** desde el panel admin

2. **Revisa los logs** en Railway para detectar accesos no autorizados

3. **Reinicia las asistencias** si es necesario (botón en panel admin)

4. **Notifica a los usuarios** si hubo acceso no autorizado a datos sensibles

5. **Considera rotar todas las credenciales** y tokens

---

## ✅ Checklist de Seguridad Post-Deploy

- [ ] Cambiar contraseña de admin desde la interfaz web
- [ ] Verificar que la nueva contraseña es segura (12+ caracteres)
- [ ] Probar login con nueva contraseña
- [ ] Configurar variables de entorno en Railway (opcional)
- [ ] Revisar logs de acceso en Railway
- [ ] Documentar credenciales en un gestor de contraseñas seguro
- [ ] Compartir credenciales solo con personal autorizado
- [ ] Configurar backup de datos (opcional)

---

## 📞 Soporte

Si tienes problemas con la seguridad:
- Railway Security: https://docs.railway.app/reference/security
- OWASP Top 10: https://owasp.org/www-project-top-ten/

---

**Recuerda**: La seguridad es un proceso continuo, no un evento único. Revisa y actualiza tus medidas de seguridad regularmente.
