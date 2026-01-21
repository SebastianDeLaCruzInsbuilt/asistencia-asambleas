#!/usr/bin/env python3
"""
Script de prueba de carga para el Sistema de Asistencia a Asambleas
Simula múltiples usuarios confirmando asistencia simultáneamente
"""

import requests
import time
import concurrent.futures
import statistics
from datetime import datetime

# Configuración
BASE_URL = "https://web-production-299e4.up.railway.app"
NUM_USUARIOS = 500  # Número de usuarios a simular
TIEMPO_OBJETIVO = 60  # Segundos (1 minuto)

# Datos de prueba
USUARIOS_PRUEBA = [
    {"userId": f"TEST{i:04d}", "documento": f"1234567{i:04d}", "nombre": f"Usuario Test {i}"}
    for i in range(1, NUM_USUARIOS + 1)
]

# Ubicación de prueba (debe coincidir con la configuración del sistema)
UBICACION_PRUEBA = {
    "latitud": 4.3229422,  # Coordenadas configuradas en el sistema
    "longitud": -74.3693629
}


def confirmar_asistencia(usuario_data):
    """
    Simula un usuario confirmando asistencia
    
    Returns:
        dict: Resultado de la petición con tiempo de respuesta
    """
    inicio = time.time()
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/confirmar-asistencia",
            json={
                "userId": usuario_data["userId"],
                "documento": usuario_data["documento"],
                "latitud": UBICACION_PRUEBA["latitud"],
                "longitud": UBICACION_PRUEBA["longitud"]
            },
            timeout=30
        )
        
        tiempo_respuesta = time.time() - inicio
        
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "tiempo_respuesta": tiempo_respuesta,
            "usuario": usuario_data["userId"],
            "response": response.json() if response.status_code == 200 else None,
            "error": None
        }
    except Exception as e:
        tiempo_respuesta = time.time() - inicio
        return {
            "success": False,
            "status_code": None,
            "tiempo_respuesta": tiempo_respuesta,
            "usuario": usuario_data["userId"],
            "response": None,
            "error": str(e)
        }


def ejecutar_prueba_carga():
    """
    Ejecuta la prueba de carga con múltiples usuarios simultáneos
    """
    print("="*70)
    print("PRUEBA DE CARGA - SISTEMA DE ASISTENCIA A ASAMBLEAS")
    print("="*70)
    print(f"\nConfiguración:")
    print(f"  URL: {BASE_URL}")
    print(f"  Usuarios a simular: {NUM_USUARIOS}")
    print(f"  Tiempo objetivo: {TIEMPO_OBJETIVO} segundos")
    print(f"  Ubicación: {UBICACION_PRUEBA['latitud']}, {UBICACION_PRUEBA['longitud']}")
    print("\n" + "="*70)
    
    # Primero, agregar usuarios de prueba al sistema
    print("\n[1/3] Preparando usuarios de prueba...")
    print("NOTA: Debes agregar estos usuarios manualmente desde el panel admin")
    print("      o usar la importación CSV con el archivo generado.")
    print("\nPresiona ENTER cuando los usuarios estén listos...")
    input()
    
    # Ejecutar prueba de carga
    print("\n[2/3] Ejecutando prueba de carga...")
    print(f"Iniciando {NUM_USUARIOS} peticiones simultáneas...")
    
    inicio_prueba = time.time()
    resultados = []
    
    # Usar ThreadPoolExecutor para simular usuarios concurrentes
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # Enviar todas las peticiones
        futures = [
            executor.submit(confirmar_asistencia, usuario)
            for usuario in USUARIOS_PRUEBA
        ]
        
        # Recoger resultados
        for future in concurrent.futures.as_completed(futures):
            resultado = future.result()
            resultados.append(resultado)
            
            # Mostrar progreso cada 50 usuarios
            if len(resultados) % 50 == 0:
                print(f"  Progreso: {len(resultados)}/{NUM_USUARIOS} usuarios procesados")
    
    tiempo_total = time.time() - inicio_prueba
    
    # Analizar resultados
    print("\n[3/3] Analizando resultados...")
    print("\n" + "="*70)
    print("RESULTADOS DE LA PRUEBA")
    print("="*70)
    
    exitosos = [r for r in resultados if r["success"]]
    fallidos = [r for r in resultados if not r["success"]]
    
    tiempos_respuesta = [r["tiempo_respuesta"] for r in resultados]
    tiempos_exitosos = [r["tiempo_respuesta"] for r in exitosos]
    
    print(f"\n📊 Estadísticas Generales:")
    print(f"  Total de peticiones: {len(resultados)}")
    print(f"  Exitosas: {len(exitosos)} ({len(exitosos)/len(resultados)*100:.1f}%)")
    print(f"  Fallidas: {len(fallidos)} ({len(fallidos)/len(resultados)*100:.1f}%)")
    print(f"  Tiempo total: {tiempo_total:.2f} segundos")
    print(f"  Throughput: {len(resultados)/tiempo_total:.2f} peticiones/segundo")
    
    if tiempos_respuesta:
        print(f"\n⏱️  Tiempos de Respuesta (todas las peticiones):")
        print(f"  Promedio: {statistics.mean(tiempos_respuesta):.3f}s")
        print(f"  Mediana: {statistics.median(tiempos_respuesta):.3f}s")
        print(f"  Mínimo: {min(tiempos_respuesta):.3f}s")
        print(f"  Máximo: {max(tiempos_respuesta):.3f}s")
        if len(tiempos_respuesta) > 1:
            print(f"  Desv. Estándar: {statistics.stdev(tiempos_respuesta):.3f}s")
    
    if tiempos_exitosos:
        print(f"\n✅ Tiempos de Respuesta (solo exitosas):")
        print(f"  Promedio: {statistics.mean(tiempos_exitosos):.3f}s")
        print(f"  Mediana: {statistics.median(tiempos_exitosos):.3f}s")
        print(f"  Mínimo: {min(tiempos_exitosos):.3f}s")
        print(f"  Máximo: {max(tiempos_exitosos):.3f}s")
    
    # Mostrar errores si los hay
    if fallidos:
        print(f"\n❌ Errores Encontrados:")
        errores_por_tipo = {}
        for r in fallidos:
            error_key = r["error"] or f"HTTP {r['status_code']}"
            errores_por_tipo[error_key] = errores_por_tipo.get(error_key, 0) + 1
        
        for error, count in errores_por_tipo.items():
            print(f"  {error}: {count} ocurrencias")
    
    # Evaluación final
    print("\n" + "="*70)
    print("EVALUACIÓN FINAL")
    print("="*70)
    
    tasa_exito = len(exitosos) / len(resultados) * 100
    tiempo_promedio = statistics.mean(tiempos_exitosos) if tiempos_exitosos else 0
    
    print(f"\n🎯 Objetivo: {NUM_USUARIOS} usuarios en {TIEMPO_OBJETIVO} segundos")
    print(f"📈 Resultado: {len(exitosos)} usuarios en {tiempo_total:.2f} segundos")
    
    if tasa_exito >= 95 and tiempo_total <= TIEMPO_OBJETIVO * 1.5:
        print(f"\n✅ PRUEBA EXITOSA")
        print(f"   El sistema puede manejar {NUM_USUARIOS} usuarios simultáneos")
        print(f"   Tasa de éxito: {tasa_exito:.1f}%")
        print(f"   Tiempo promedio de respuesta: {tiempo_promedio:.3f}s")
    elif tasa_exito >= 90:
        print(f"\n⚠️  PRUEBA PARCIALMENTE EXITOSA")
        print(f"   El sistema maneja la carga pero con algunas fallas")
        print(f"   Tasa de éxito: {tasa_exito:.1f}%")
        print(f"   Considera optimizar o escalar recursos")
    else:
        print(f"\n❌ PRUEBA FALLIDA")
        print(f"   El sistema no puede manejar {NUM_USUARIOS} usuarios simultáneos")
        print(f"   Tasa de éxito: {tasa_exito:.1f}%")
        print(f"   Se requiere optimización o más recursos")
    
    print("\n" + "="*70)
    
    # Guardar resultados detallados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"resultados_prueba_carga_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("RESULTADOS DETALLADOS DE PRUEBA DE CARGA\n")
        f.write("="*70 + "\n\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"URL: {BASE_URL}\n")
        f.write(f"Usuarios: {NUM_USUARIOS}\n")
        f.write(f"Tiempo total: {tiempo_total:.2f}s\n")
        f.write(f"Exitosas: {len(exitosos)}\n")
        f.write(f"Fallidas: {len(fallidos)}\n\n")
        
        f.write("RESULTADOS POR USUARIO:\n")
        f.write("-"*70 + "\n")
        for r in resultados:
            status = "✓" if r["success"] else "✗"
            f.write(f"{status} {r['usuario']}: {r['tiempo_respuesta']:.3f}s")
            if r["error"]:
                f.write(f" - Error: {r['error']}")
            f.write("\n")
    
    print(f"\n📄 Resultados detallados guardados en: {filename}")


def generar_csv_usuarios_prueba():
    """
    Genera un archivo CSV con usuarios de prueba para importar
    """
    filename = "usuarios_prueba_carga.csv"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("userId,documento,nombre\n")
        for usuario in USUARIOS_PRUEBA:
            f.write(f"{usuario['userId']},{usuario['documento']},{usuario['nombre']}\n")
    
    print(f"\n✅ Archivo CSV generado: {filename}")
    print(f"   Importa este archivo desde el panel admin antes de ejecutar la prueba")


if __name__ == "__main__":
    print("\n¿Qué deseas hacer?")
    print("1. Generar CSV de usuarios de prueba")
    print("2. Ejecutar prueba de carga")
    print("3. Ambos")
    
    opcion = input("\nSelecciona una opción (1/2/3): ").strip()
    
    if opcion in ["1", "3"]:
        generar_csv_usuarios_prueba()
    
    if opcion in ["2", "3"]:
        print("\n")
        ejecutar_prueba_carga()
