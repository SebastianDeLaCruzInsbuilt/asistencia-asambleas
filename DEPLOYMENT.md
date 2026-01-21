# Guía de Despliegue
Sistema de Confirmación de Asistencia a Asambleas

## 🚀 Despliegue Rápido

### Desarrollo Local (HTTP)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
python backend/app.py
```

Acceder en: http://localhost:5000

---

## 🔒 Despliegue con HTTPS

### Paso 1: Instalar Dependencias

```bash
pip install -r requirements.txt
pip install cryptography
```

### Paso 2: Generar Certificados

**Opción A: Certificados Autofirmados (Desarrollo/Pruebas)**

```bash
python generar_certificados.py
```

O con dominio personalizado:
```bash
python generar_certificados.py --dominio midominio.com
```

**Opción B: Let's Encrypt (Producción)**

```bash
# Instalar certbot
sudo apt-get install certbot  # Ubuntu/Debian
brew install certbot          # macOS

# Obtener certificados
sudo certbot certonly --standalone -d tudominio.com

# Los certificados estarán en:
# /etc/letsencrypt/live/tudominio.com/fullchain.pem
# /etc/letsencrypt/live/tudominio.com/privkey.pem
```

### Paso 3: Configurar Variables de Entorno

**Windows:**
```cmd
set SSL_ENABLED=true
set SSL_CERT_PATH=certs\cert.pem
set SSL_KEY_PATH=certs\key.pem
set PORT=443
```

**Linux/macOS:**
```bash
export SSL_ENABLED=true
export SSL_CERT_PATH=certs/cert.pem
export SSL_KEY_PATH=certs/key.pem
export PORT=443
```

Para Let's Encrypt:
```bash
export SSL_CERT_PATH=/etc/letsencrypt/live/tudominio.com/fullchain.pem
export SSL_KEY_PATH=/etc/letsencrypt/live/tudominio.com/privkey.pem
```

### Paso 4: Iniciar Servidor

**Windows:**
```cmd
start_production.bat
```

**Linux/macOS:**
```bash
chmod +x start_production.sh
sudo ./start_production.sh  # sudo necesario para puerto 443
```

Acceder en: https://localhost (o https://tudominio.com)

---

## ☁️ Despliegue en Cloud

### Heroku

```bash
# 1. Crear Procfile
echo "web: gunicorn backend.app:app" > Procfile

# 2. Crear app
heroku create mi-app-asistencia

# 3. Configurar variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# 4. Desplegar
git push heroku main

# 5. Abrir
heroku open
```

### AWS EC2

```bash
# 1. Conectar a instancia
ssh -i tu-clave.pem ubuntu@tu-ip

# 2. Instalar dependencias del sistema
sudo apt update
sudo apt install python3-pip nginx certbot python3-certbot-nginx

# 3. Clonar proyecto
git clone tu-repositorio
cd tu-repositorio

# 4. Instalar dependencias Python
pip3 install -r requirements.txt

# 5. Obtener certificados SSL
sudo certbot --nginx -d tudominio.com

# 6. Configurar nginx
sudo nano /etc/nginx/sites-available/asistencia
```

**Configuración nginx:**
```nginx
server {
    listen 80;
    server_name tudominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name tudominio.com;

    ssl_certificate /etc/letsencrypt/live/tudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tudominio.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# 7. Habilitar sitio
sudo ln -s /etc/nginx/sites-available/asistencia /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 8. Crear servicio systemd
sudo nano /etc/systemd/system/asistencia.service
```

**Archivo de servicio:**
```ini
[Unit]
Description=Sistema de Asistencia
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/asistencia-asamblea
Environment="FLASK_ENV=production"
Environment="SECRET_KEY=tu-clave-secreta-aqui"
ExecStart=/usr/local/bin/gunicorn --bind 127.0.0.1:5000 --workers 4 backend.app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 9. Iniciar servicio
sudo systemctl daemon-reload
sudo systemctl start asistencia
sudo systemctl enable asistencia
sudo systemctl status asistencia
```

### DigitalOcean

Seguir los mismos pasos que AWS EC2.

### Google Cloud Platform

```bash
# 1. Crear instancia VM
gcloud compute instances create asistencia-vm \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --machine-type=e2-micro \
    --zone=us-central1-a

# 2. Conectar
gcloud compute ssh asistencia-vm --zone=us-central1-a

# 3. Seguir pasos de AWS EC2
```

---

## 🐳 Despliegue con Docker

### Crear Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY . .

# Exponer puerto
EXPOSE 5000

# Variables de entorno por defecto
ENV FLASK_ENV=production
ENV HOST=0.0.0.0
ENV PORT=5000

# Comando de inicio
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "backend.app:app"]
```

### Construir y Ejecutar

```bash
# Construir imagen
docker build -t asistencia-app .

# Ejecutar (HTTP)
docker run -d \
  --name asistencia \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -e FLASK_ENV=production \
  -e SECRET_KEY=tu-clave-secreta \
  asistencia-app

# Ejecutar (HTTPS)
docker run -d \
  --name asistencia \
  -p 443:443 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/certs:/app/certs \
  -e FLASK_ENV=production \
  -e SECRET_KEY=tu-clave-secreta \
  -e SSL_ENABLED=true \
  -e PORT=443 \
  asistencia-app
```

### Docker Compose

Crear `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./certs:/app/certs
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - SSL_ENABLED=${SSL_ENABLED:-false}
      - PORT=5000
    restart: unless-stopped
```

Ejecutar:
```bash
docker-compose up -d
```

---

## 🔐 Seguridad en Producción

### 1. Generar SECRET_KEY Segura

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Configurar CORS

```bash
# Solo permitir tu dominio
export CORS_ORIGINS=https://tudominio.com,https://www.tudominio.com
```

### 3. Configurar Firewall

```bash
# Ubuntu/Debian
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 4. Configurar Rate Limiting (nginx)

```nginx
http {
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    
    server {
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://127.0.0.1:5000;
        }
    }
}
```

### 5. Backups Automáticos

```bash
# Crear script de backup
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/asistencia"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/data_$DATE.tar.gz data/
# Mantener solo últimos 7 días
find $BACKUP_DIR -name "data_*.tar.gz" -mtime +7 -delete
EOF

chmod +x backup.sh

# Agregar a crontab (diario a las 2 AM)
crontab -e
# Agregar: 0 2 * * * /ruta/a/backup.sh
```

---

## 📊 Monitoreo

### Logs

```bash
# Ver logs en tiempo real
tail -f logs/app.log

# Buscar errores
grep ERROR logs/app.log

# Últimas 100 líneas
tail -n 100 logs/app.log
```

### Systemd (Linux)

```bash
# Ver logs del servicio
sudo journalctl -u asistencia -f

# Ver últimas 50 líneas
sudo journalctl -u asistencia -n 50

# Ver logs desde hoy
sudo journalctl -u asistencia --since today
```

### Monitoreo de Recursos

```bash
# CPU y memoria
htop

# Espacio en disco
df -h

# Conexiones activas
netstat -an | grep :5000
```

---

## 🔄 Actualización

### Actualizar Aplicación

```bash
# 1. Detener servidor
sudo systemctl stop asistencia  # Linux con systemd
# O Ctrl+C si está en primer plano

# 2. Actualizar código
git pull origin main

# 3. Actualizar dependencias
pip install -r requirements.txt

# 4. Reiniciar servidor
sudo systemctl start asistencia  # Linux con systemd
# O ejecutar start_production.sh
```

### Renovar Certificados SSL

```bash
# Let's Encrypt (automático)
sudo certbot renew

# Reiniciar nginx
sudo systemctl restart nginx

# Reiniciar aplicación
sudo systemctl restart asistencia
```

---

## 🆘 Solución de Problemas

### Puerto en uso

```bash
# Ver qué proceso usa el puerto
sudo lsof -i :5000  # Linux/macOS
netstat -ano | findstr :5000  # Windows

# Matar proceso
sudo kill -9 <PID>  # Linux/macOS
taskkill /PID <PID> /F  # Windows
```

### Certificados SSL no funcionan

```bash
# Verificar certificados
openssl x509 -in certs/cert.pem -text -noout

# Verificar permisos
ls -la certs/

# Regenerar certificados
python generar_certificados.py
```

### Aplicación no accesible desde internet

1. Verificar firewall del servidor
2. Verificar port forwarding en router
3. Verificar DNS apunta a IP correcta
4. Verificar que aplicación escucha en 0.0.0.0

```bash
# Ver puertos en escucha
sudo netstat -tulpn | grep :5000
```

---

## 📞 Soporte

Para más información, consultar:
- README.md - Documentación completa
- backend/app.py - Código fuente del servidor
- config.py - Configuración del servidor
