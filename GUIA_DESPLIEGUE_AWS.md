# 🚀 Guía de Despliegue en AWS con CDK

## ✅ Credenciales Configuradas

Las credenciales de AWS ya están configuradas en `cdk-python/credentials.json`.

## 📋 Prerequisitos a Instalar

### 1. Instalar Node.js (Requerido para AWS CDK)

**Descargar e instalar Node.js:**
1. Ir a: https://nodejs.org/
2. Descargar la versión LTS (recomendada)
3. Ejecutar el instalador
4. Seguir las instrucciones (dejar opciones por defecto)
5. Reiniciar la terminal después de instalar

**Verificar instalación:**
```powershell
node --version
npm --version
```

### 2. Instalar AWS CDK

Una vez instalado Node.js, ejecutar:

```powershell
npm install -g aws-cdk
```

**Verificar instalación:**
```powershell
cdk --version
```

### 3. Instalar Dependencias de Python para CDK

```powershell
cd cdk-python
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 🚀 Despliegue

### Opción 1: Despliegue Automático (Recomendado)

Una vez instalados los prerequisitos:

```powershell
cd cdk-python
.venv\Scripts\activate
.\deploy.sh
```

El script te guiará paso a paso.

### Opción 2: Despliegue Manual

```powershell
cd cdk-python
.venv\Scripts\activate

# Bootstrap (solo primera vez)
cdk bootstrap

# Desplegar
cdk deploy
```

## ⏱️ Tiempo Estimado

- **Instalación de prerequisitos**: 5-10 minutos
- **Despliegue en AWS**: 5-10 minutos
- **Total**: 10-20 minutos

## 📊 Después del Despliegue

Al finalizar, verás algo como:

```
Outputs:
AsistenciaAsambleaStack.ApplicationURL = http://xxxxx.us-east-1.elb.amazonaws.com
AsistenciaAsambleaStack.AdminPanelURL = http://xxxxx.us-east-1.elb.amazonaws.com/admin.html
```

**Guarda estas URLs** - son las que usarás para acceder a tu aplicación.

## 🔗 URLs de tu Aplicación

Una vez desplegado:

- **Aplicación Principal**: `http://[tu-load-balancer].elb.amazonaws.com`
- **Panel Administrativo**: `http://[tu-load-balancer].elb.amazonaws.com/admin.html`
- **Login Admin**: `http://[tu-load-balancer].elb.amazonaws.com/login.html`

## 🔐 Credenciales de Admin

- **Usuario**: `admin`
- **Contraseña**: `admin123`

⚠️ **Importante**: Cambiar estas credenciales después del primer acceso.

## 💰 Costos Estimados

- **EC2 t3.micro**: ~$7.50/mes (GRATIS primer año con Free Tier)
- **Application Load Balancer**: ~$16/mes
- **Total**: ~$23.50/mes (~$16/mes con Free Tier)

## 🛑 Eliminar Todo (Cuando ya no lo necesites)

```powershell
cd cdk-python
.venv\Scripts\activate
cdk destroy
```

## 📝 Notas Importantes

1. **Credenciales Temporales**: Las credenciales que proporcionaste son temporales (session token). Si expiran, necesitarás obtener nuevas credenciales.

2. **Región**: El despliegue se hará en `us-east-1` (Virginia del Norte).

3. **Seguridad**: El sistema desplegará con HTTP. Para HTTPS necesitarás un dominio.

## 🆘 Solución de Problemas

### Error: "Unable to locate credentials"

Las credenciales temporales expiraron. Necesitas obtener nuevas credenciales de AWS.

### Error: "cdk command not found"

AWS CDK no está instalado. Ejecutar:
```powershell
npm install -g aws-cdk
```

### Error: "node command not found"

Node.js no está instalado. Descargar de: https://nodejs.org/

## 📞 Próximos Pasos

1. **Instalar Node.js** (si no lo tienes)
2. **Instalar AWS CDK**: `npm install -g aws-cdk`
3. **Ir a cdk-python**: `cd cdk-python`
4. **Crear entorno virtual**: `python -m venv .venv`
5. **Activar entorno**: `.venv\Scripts\activate`
6. **Instalar dependencias**: `pip install -r requirements.txt`
7. **Desplegar**: `cdk deploy`

---

**¿Listo para empezar?** Sigue los pasos en orden y en 20 minutos tendrás tu aplicación en AWS. 🎉
