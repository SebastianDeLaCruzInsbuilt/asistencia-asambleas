#!/usr/bin/env python3
"""
Ejecuta prueba de carga de 500 usuarios directamente
"""

import requests
import time
import concurrent.futures
import statistics
from datetime import datetime

# Configuración
BASE_URL = "https://web-production-299e4.up.railway.app"
NUM_USUARIOS = 500

# Ubicación (debe coincidir con la configuración del sistema)
UBICACION = {
    "latitud": 4.3229422,
    "longitud": -74.3693629
}

# Usuarios de prueba
USUARIOS = [
    {"userId": f"TEST{i:04d}", "documento": f"1234567{i:04d}"}
    for i in range(1, NUM_USUARIOS + 1)
]


def confirmar_asistencia(usuario):
    """Confirma asistencia de un usuario"""
    inicio = time.time()
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/confirmar-asistencia",
            json={
                "userId": usuario["userId"],
                "documento": usuario["documento"],
                "latitud": UBICACION["latitud"],
                "longitud": UBICACION["longitud"]
            },
            timeout=30
        )
        
        tiempo = time.time() - inicio
        data = response.json() if response.status_code == 200 else None
        
        return {
            "success": response.status_code == 200 and data and data.get('confirmado'),
            "usuario": usuario["userId"],
            "tiempo": tiempo,
            "mensaje": data.get('mensaje') if data else None
        }
    except Exception as e:
        return {
            "success": False,
            "usuario": usuario["userId"],
            "tiempo": time.time() - inicio,
            "mensaje": str(e)
        }


print("="*70)
print("PRUEBA DE CARGA - 500 USUARIOS")
print("="*70)
print(f"\nURL: {BASE_URL}")
print(f"Usuarios: {NUM_USUARIOS}")
print(f"Ubicación: {UBICACION['latitud']}, {UBICACION['longitud']}")
print("\nIniciando prueba...")

inicio_total = time.time()
resultados = []

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    futures = [executor.submit(confirmar_asistencia, u) for u in USUARIOS]
    
    for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
        resultado = future.result()
        resultados.append(resultado)
        
        if i % 50 == 0:
            print(f"  Progreso: {i}/{NUM_USUARIOS}")

tiempo_total = time.time() - inicio_total

# Análisis
exitosos = [r for r in resultados if r["success"]]
fallidos = [r for r in resultados if not r["success"]]

print("\n" + "="*70)
print("RESULTADOS")
print("="*70)
print(f"\nTotal: {len(resultados)}")
print(f"Exitosos: {len(exitosos)} ({len(exitosos)/len(resultados)*100:.1f}%)")
print(f"Fallidos: {len(fallidos)} ({len(fallidos)/len(resultados)*100:.1f}%)")
print(f"Tiempo total: {tiempo_total:.2f}s")
print(f"Throughput: {len(resultados)/tiempo_total:.2f} req/s")

if exitosos:
    tiempos = [r["tiempo"] for r in exitosos]
    print(f"\nTiempos de respuesta:")
    print(f"  Promedio: {statistics.mean(tiempos):.3f}s")
    print(f"  Mediana: {statistics.median(tiempos):.3f}s")
    print(f"  Min/Max: {min(tiempos):.3f}s / {max(tiempos):.3f}s")

if fallidos:
    print(f"\n❌ Errores ({len(fallidos)}):")
    errores = {}
    for r in fallidos:
        msg = r["mensaje"] or "Error desconocido"
        errores[msg] = errores.get(msg, 0) + 1
    for msg, count in list(errores.items())[:5]:
        print(f"  - {msg}: {count}")

print("\n" + "="*70)
if len(exitosos) >= 500:
    print("✅ PRUEBA EXITOSA - 500 asistencias confirmadas")
elif len(exitosos) >= 450:
    print(f"⚠️  PRUEBA PARCIAL - {len(exitosos)} asistencias confirmadas")
else:
    print(f"❌ PRUEBA FALLIDA - Solo {len(exitosos)} asistencias confirmadas")
print("="*70)

# Guardar resultados
filename = f"resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(filename, 'w') as f:
    f.write(f"Exitosos: {len(exitosos)}\n")
    f.write(f"Fallidos: {len(fallidos)}\n")
    f.write(f"Tiempo: {tiempo_total:.2f}s\n\n")
    for r in resultados:
        status = "✓" if r["success"] else "✗"
        f.write(f"{status} {r['usuario']}: {r['tiempo']:.3f}s - {r['mensaje']}\n")

print(f"\n📄 Resultados guardados en: {filename}")
