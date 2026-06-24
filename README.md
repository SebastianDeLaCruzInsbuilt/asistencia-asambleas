# � Workspace de Proyectos

Este workspace contiene dos proyectos independientes listos para desarrollo y deploy.

---

## 📦 Proyectos

### 1️⃣ Sistema de Asistencia a Asambleas
**Carpeta:** `asistencia-asamblea/`  
**Tecnología:** Python + Flask  
**Descripción:** Sistema web para confirmar asistencia mediante validación de identidad y geolocalización

[📖 Ver documentación completa →](asistencia-asamblea/README.md)

```bash
cd asistencia-asamblea
pip install -r requirements.txt
python backend/app.py
```

---

### 2️⃣ Analizador de Código .NET con GenAI
**Carpeta:** `dotnet-code-analyzer/`  
**Tecnología:** Python + AWS Bedrock + Flask  
**Descripción:** Agente GenAI que analiza código C# y genera reportes de negocio en Excel

[📖 Ver documentación completa →](dotnet-code-analyzer/README.md)

```bash
cd dotnet-code-analyzer
pip install -r requirements.txt
python start_server.py
```

---

## 📂 Estructura del Workspace

```
workspace/
│
├── 📁 asistencia-asamblea/      → Proyecto completo de asistencia
│   ├── backend/                 → Backend Flask
│   ├── frontend/                → Frontend web
│   ├── data/                    → Base de datos
│   ├── config.py                → Configuración
│   ├── requirements.txt         → Dependencias
│   ├── start.bat / .sh          → Scripts de inicio
│   └── README.md                → Documentación
│
├── � dotnet-code-analyzer/     → Proyecto completo del analyzer
│   ├── src/                     → Código fuente
│   ├── frontend/                → Interfaz web
│   ├── tests/                   → Pruebas
│   ├── requirements.txt         → Dependencias
│   ├── start_server.py          → Script de inicio
│   └── README.md                → Documentación
│
├── 📁 .kiro/                    → Configuración Kiro
│   └── specs/                   → Especificaciones
│
└── 📚 Documentación/
    ├── README.md                → Este archivo
    ├── QUICK_START.md           → Comandos rápidos
    └── WORKSPACE_STRUCTURE.md   → Estructura detallada
```

---

## 🚀 Inicio Rápido

### Proyecto Asistencia
```bash
cd asistencia-asamblea
pip install -r requirements.txt
python backend/app.py
# Acceder a: http://localhost:5000
```

### Proyecto Analyzer
```bash
cd dotnet-code-analyzer
pip install -r requirements.txt
aws configure  # Configurar AWS si es necesario
python start_server.py
# Acceder a: http://localhost:5000
```

---

## 📊 Comparación de Proyectos

| Aspecto | Asistencia | Analyzer |
|---------|-----------|----------|
| **Lenguaje** | Python 3.11 | Python 3.9+ |
| **Framework** | Flask | Flask + AWS Strands |
| **Frontend** | HTML/CSS/JS | HTML/CSS/JS |
| **Base de Datos** | JSON/CSV | N/A |
| **Cloud** | Railway | AWS Bedrock |
| **Puerto** | 5000 | 5000 |
| **Deploy** | Railway.app | AWS |

---

## 🔧 Requisitos

### Ambos Proyectos
- Python 3.9 o superior
- pip (gestor de paquetes)
- Git

### Proyecto Asistencia
- Ningún requisito adicional

### Proyecto Analyzer
- AWS CLI configurado
- Cuenta AWS con acceso a Bedrock
- Credenciales AWS configuradas

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [asistencia-asamblea/README.md](asistencia-asamblea/README.md) | Documentación completa del sistema de asistencia |
| [dotnet-code-analyzer/README.md](dotnet-code-analyzer/README.md) | Documentación completa del analyzer |
| [QUICK_START.md](QUICK_START.md) | Comandos esenciales para ambos proyectos |
| [WORKSPACE_STRUCTURE.md](WORKSPACE_STRUCTURE.md) | Estructura detallada del workspace |

---

## 🎯 Características

### ✅ Workspace Organizado
- Dos proyectos completamente independientes
- Cada proyecto en su propia carpeta
- Documentación separada y completa
- Fácil de navegar y mantener

### ✅ Listo para Desarrollo
- Configuración mínima requerida
- Scripts de inicio incluidos
- Dependencias claramente definidas
- Pruebas disponibles

### ✅ Listo para Deploy
- Ambos proyectos deployables
- Documentación de deploy incluida
- Configuración de producción lista

---

## 🔄 Flujo de Trabajo

1. **Elegir proyecto:** Navega a la carpeta del proyecto
2. **Instalar dependencias:** `pip install -r requirements.txt`
3. **Configurar (si es necesario):** Ver README del proyecto
4. **Iniciar:** Ejecutar script de inicio
5. **Desarrollar:** Hacer cambios
6. **Probar:** Ejecutar tests
7. **Deploy:** Seguir guía de deploy

---

## 🆘 Soporte

- **Problemas con Asistencia:** Ver [asistencia-asamblea/README.md](asistencia-asamblea/README.md)
- **Problemas con Analyzer:** Ver [dotnet-code-analyzer/README.md](dotnet-code-analyzer/README.md)
- **Problemas generales:** Revisar documentación del workspace

---

## 📝 Notas

- Cada proyecto tiene su propio `requirements.txt`
- Los proyectos son completamente independientes
- Pueden ejecutarse simultáneamente en diferentes puertos
- Las especificaciones Kiro están en `.kiro/specs/`

---

## 📊 Estado

| Proyecto | Estado | Tests | Deploy |
|----------|--------|-------|--------|
| Asistencia | ✅ Activo | ✅ Disponibles | ✅ Railway |
| Analyzer | ✅ Activo | ✅ Disponibles | ✅ AWS |

---

**Última actualización:** 27 de enero de 2026  
**Proyectos activos:** 2  
**Estado del workspace:** ✅ Organizado y listo
