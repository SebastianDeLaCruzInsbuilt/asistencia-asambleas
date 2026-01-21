# 🚀 Prueba de Carga - Sistema de Asistencia a Asambleas

## Objetivo

Verificar que el sistema puede manejar **500 usuarios confirmando asistencia en 1 minuto**.

---

## 📋 Requisitos

1. **Python 3.7+** instalado
2. **Librería requests** instalada:
   ```bash
   pip install requests
   ```

---

## 🔧 Preparación

### Paso 1: Generar Usuarios de Prueba

Ejecuta el script para generar el archivo CSV con 500 usuarios de prueba:

```bash
python test_carga.py
```

Selecciona opción **1** para generar el CSV.

Esto creará el archivo: `usuarios_prueba_carga.csv`

### Paso 2: Importar Usuarios al Sistema

1. Accede al panel admin: https://web-production-299e4.up.railway.app/login.html
2. Login con: `admin` / `admin123`
3. Ve a la sección **"Gestión de Usuarios"**
4. Click en **"Importar desde CSV"**
5. Selecciona el archivo `usuarios_prueba_carga.csv`
6. Espera a que se importen los 500 usuarios

### Paso 3: Configurar Ubicación

En el panel admin, configura la ubicación de la asamblea:

- **Latitud**: `-12.0464` (Lima, Perú - ajusta según tu ubicación)
- **Longitud**: `-77.0428`
- **Radio permitido**: `1000` metros (1 km)

**Nota**: El script de prueba usa estas coordenadas. Si cambias la ubicación, actualiza el script.

---

## ▶️ Ejecutar Prueba de Carga

### Opción 1: Prueba Completa (Recomendado)

```bash
python test_carga.py
```

Selecciona opción **3** para generar CSV y ejecutar prueba.

### Opción 2: Solo Prueba (si ya importaste usuarios)

```bash
python test_carga.py
```

Selecciona opción **2** para ejecutar solo la prueba.

---

## 📊 Interpretación de Resultados

El script mostrará:

### Estadísticas Generales
- **Total de peticiones**: Número de usuarios simulados
- **Exitosas**: Confirmaciones exitosas (objetivo: >95%)
- **Fallidas**: Confirmaciones fallidas
- **Tiempo total**: Tiempo que tomó procesar todas las peticiones
- **Throughput**: Peticiones por segundo

### Tiempos de Respuesta
- **Promedio**: Tiempo promedio de respuesta
- **Mediana**: Tiempo medio de respuesta
- **Mínimo/Máximo**: Rango de tiempos
- **Desviación Estándar**: Variabilidad de tiempos

### Evaluación Final

✅ **PRUEBA EXITOSA**
- Tasa de éxito ≥ 95%
- Tiempo total ≤ 90 segundos (1.5x objetivo)
- El sistema puede manejar la carga

⚠️ **PRUEBA PARCIALMENTE EXITOSA**
- Tasa de éxito ≥ 90%
- Algunas fallas pero funcional
- Considera optimizar

❌ **PRUEBA FALLIDA**
- Tasa de éxito < 90%
- El sistema no puede manejar la carga
- Se requiere optimización o más recursos

---

## 🔍 Análisis de Resultados

El script genera un archivo detallado: `resultados_prueba_carga_YYYYMMDD_HHMMSS.txt`

Este archivo contiene:
- Resumen de la prueba
- Resultados por usuario
- Tiempos de respuesta individuales
- Errores específicos

---

## 🛠️ Solución de Problemas

### Error: "Connection timeout"

**Causa**: El servidor no responde a tiempo

**Solución**:
1. Verifica que Railway esté corriendo
2. Aumenta el timeout en el script (línea 35)
3. Reduce el número de usuarios simultáneos

### Error: "Usuario no autorizado"

**Causa**: Los usuarios de prueba no están en el sistema

**Solución**:
1. Verifica que importaste el CSV correctamente
2. Revisa el panel admin para confirmar que los usuarios existen

### Error: "Ubicación fuera de rango"

**Causa**: Las coordenadas de prueba no coinciden con la configuración

**Solución**:
1. Verifica la ubicación configurada en el panel admin
2. Actualiza las coordenadas en el script (líneas 18-21)

### Tasa de éxito baja (<90%)

**Posibles causas**:
1. **Recursos insuficientes**: Railway plan gratuito tiene límites
2. **Timeout muy corto**: Aumenta el timeout
3. **Red lenta**: Ejecuta desde una conexión más rápida

**Soluciones**:
1. **Escalar en Railway**: Aumenta recursos (requiere plan de pago)
2. **Optimizar código**: Revisar endpoints lentos
3. **Usar caché**: Implementar caché para datos frecuentes
4. **Aumentar workers**: Cambiar a 2-4 workers (requiere Redis para tokens)

---

## 📈 Optimizaciones Recomendadas

### Para Mejorar Rendimiento

1. **Aumentar workers** (requiere Redis para tokens compartidos):
   ```
   workers = 4
   ```

2. **Usar caché** para usuarios y configuración

3. **Optimizar queries** a archivos JSON

4. **Implementar rate limiting** para prevenir abuso

### Para Escalar en Railway

1. Ve a Railway Dashboard
2. Selecciona tu proyecto
3. Ve a Settings > Resources
4. Aumenta:
   - **Memory**: 1GB → 2GB
   - **CPU**: Shared → Dedicated

**Costo**: ~$10-20/mes adicional

---

## 🎯 Objetivos de Rendimiento

| Métrica | Objetivo | Aceptable | Crítico |
|---------|----------|-----------|---------|
| Tasa de éxito | ≥95% | ≥90% | <90% |
| Tiempo promedio | <2s | <5s | >5s |
| Tiempo total | ≤60s | ≤90s | >90s |
| Throughput | ≥8 req/s | ≥5 req/s | <5 req/s |

---

## 📞 Soporte

Si tienes problemas con la prueba de carga:

1. Revisa los logs en Railway Dashboard
2. Verifica la sección "Solución de Problemas" arriba
3. Revisa el archivo de resultados detallados

---

## ✅ Checklist Pre-Prueba

- [ ] Python 3.7+ instalado
- [ ] Librería `requests` instalada
- [ ] CSV de usuarios generado
- [ ] 500 usuarios importados en el sistema
- [ ] Ubicación configurada en panel admin
- [ ] Coordenadas del script coinciden con configuración
- [ ] Railway está corriendo sin errores

---

**¡Buena suerte con la prueba!** 🚀
