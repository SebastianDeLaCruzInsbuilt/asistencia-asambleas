#!/usr/bin/env python3
"""
Verifica que las asistencias se registraron correctamente en el sistema
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "https://web-production-299e4.up.railway.app"
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def login_admin():
    """
    Hace login como administrador y obtiene el token
    """
    print("🔐 Autenticando como administrador...")
    
    response = requests.post(
        f"{BASE_URL}/api/admin/login",
        json={
            "username": ADMIN_USER,
            "password": ADMIN_PASS
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Autenticación exitosa")
            return data.get('token')
    
    print("❌ Error al autenticar")
    return None


def obtener_asistencias(token):
    """
    Obtiene la lista de asistencias registradas
    """
    print("\n📋 Obteniendo lista de asistencias...")
    
    response = requests.get(
        f"{BASE_URL}/api/asistencias",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    
    if response.status_code == 200:
        asistencias = response.json()
        print(f"✅ Se obtuvieron {len(asistencias)} asistencias")
        return asistencias
    else:
        print(f"❌ Error al obtener asistencias: {response.status_code}")
        return []


def obtener_usuarios(token):
    """
    Obtiene la lista de usuarios autorizados
    """
    print("\n👥 Obteniendo lista de usuarios...")
    
    response = requests.get(
        f"{BASE_URL}/api/usuarios",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    
    if response.status_code == 200:
        usuarios = response.json()
        print(f"✅ Se obtuvieron {len(usuarios)} usuarios")
        return usuarios
    else:
        print(f"❌ Error al obtener usuarios: {response.status_code}")
        return []


def analizar_asistencias(asistencias, usuarios):
    """
    Analiza las asistencias registradas
    """
    print("\n" + "="*70)
    print("ANÁLISIS DE ASISTENCIAS REGISTRADAS")
    print("="*70)
    
    # Estadísticas generales
    total_asistencias = len(asistencias)
    total_usuarios = len(usuarios)
    
    print(f"\n📊 Estadísticas Generales:")
    print(f"  Total de usuarios autorizados: {total_usuarios}")
    print(f"  Total de asistencias confirmadas: {total_asistencias}")
    print(f"  Porcentaje de asistencia: {total_asistencias/total_usuarios*100:.1f}%")
    
    # Contar usuarios de prueba
    usuarios_prueba = [u for u in usuarios if u['userId'].startswith('TEST')]
    asistencias_prueba = [a for a in asistencias if a['userId'].startswith('TEST')]
    
    print(f"\n🧪 Usuarios de Prueba:")
    print(f"  Usuarios de prueba registrados: {len(usuarios_prueba)}")
    print(f"  Asistencias de prueba confirmadas: {len(asistencias_prueba)}")
    
    if len(usuarios_prueba) > 0:
        porcentaje_prueba = len(asistencias_prueba) / len(usuarios_prueba) * 100
        print(f"  Porcentaje de asistencia (prueba): {porcentaje_prueba:.1f}%")
    
    # Análisis temporal
    if asistencias:
        print(f"\n⏰ Análisis Temporal:")
        
        # Convertir timestamps a datetime
        timestamps = []
        for a in asistencias:
            try:
                # Formato: "2026-01-21 01:34:23"
                dt = datetime.strptime(a['timestamp'], "%Y-%m-%d %H:%M:%S")
                timestamps.append(dt)
            except:
                pass
        
        if timestamps:
            timestamps.sort()
            primera = timestamps[0]
            ultima = timestamps[-1]
            duracion = (ultima - primera).total_seconds()
            
            print(f"  Primera asistencia: {primera.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Última asistencia: {ultima.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Duración total: {duracion:.2f} segundos ({duracion/60:.2f} minutos)")
            
            if duracion > 0:
                tasa = len(timestamps) / duracion
                print(f"  Tasa promedio: {tasa:.2f} asistencias/segundo")
    
    # Verificar usuarios de prueba específicos
    print(f"\n🔍 Verificación de Usuarios de Prueba:")
    
    usuarios_prueba_ids = set(u['userId'] for u in usuarios_prueba)
    asistencias_prueba_ids = set(a['userId'] for a in asistencias_prueba)
    
    usuarios_sin_asistencia = usuarios_prueba_ids - asistencias_prueba_ids
    
    if usuarios_sin_asistencia:
        print(f"  ⚠️  Usuarios sin asistencia: {len(usuarios_sin_asistencia)}")
        if len(usuarios_sin_asistencia) <= 10:
            print(f"     {', '.join(sorted(list(usuarios_sin_asistencia))[:10])}")
    else:
        print(f"  ✅ Todos los usuarios de prueba confirmaron asistencia")
    
    # Evaluación final
    print("\n" + "="*70)
    print("EVALUACIÓN FINAL")
    print("="*70)
    
    if len(asistencias_prueba) >= 500:
        print(f"\n✅ PRUEBA EXITOSA")
        print(f"   Se registraron {len(asistencias_prueba)} asistencias de prueba")
        print(f"   Objetivo: 500 asistencias")
        print(f"   Estado: CUMPLIDO")
    elif len(asistencias_prueba) >= 450:
        print(f"\n⚠️  PRUEBA PARCIALMENTE EXITOSA")
        print(f"   Se registraron {len(asistencias_prueba)} asistencias de prueba")
        print(f"   Objetivo: 500 asistencias")
        print(f"   Estado: {len(asistencias_prueba)/500*100:.1f}% completado")
    else:
        print(f"\n❌ PRUEBA FALLIDA")
        print(f"   Se registraron {len(asistencias_prueba)} asistencias de prueba")
        print(f"   Objetivo: 500 asistencias")
        print(f"   Estado: {len(asistencias_prueba)/500*100:.1f}% completado")
    
    print("\n" + "="*70)
    
    return asistencias_prueba


def exportar_reporte(asistencias, usuarios):
    """
    Exporta un reporte detallado en formato texto
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reporte_asistencias_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("REPORTE DE ASISTENCIAS CONFIRMADAS\n")
        f.write("="*70 + "\n\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total de usuarios: {len(usuarios)}\n")
        f.write(f"Total de asistencias: {len(asistencias)}\n\n")
        
        f.write("LISTA DE ASISTENCIAS:\n")
        f.write("-"*70 + "\n")
        f.write(f"{'Usuario ID':<15} {'Documento':<15} {'Nombre':<30} {'Timestamp'}\n")
        f.write("-"*70 + "\n")
        
        for a in sorted(asistencias, key=lambda x: x['timestamp']):
            f.write(f"{a['userId']:<15} {a['documento']:<15} {a['nombre']:<30} {a['timestamp']}\n")
    
    print(f"\n📄 Reporte detallado guardado en: {filename}")
    return filename


def main():
    print("="*70)
    print("VERIFICACIÓN DE ASISTENCIAS REGISTRADAS")
    print("="*70)
    print(f"\nURL: {BASE_URL}")
    print(f"Usuario admin: {ADMIN_USER}")
    print("")
    
    # Login
    token = login_admin()
    if not token:
        print("\n❌ No se pudo autenticar. Verifica las credenciales.")
        return
    
    # Obtener datos
    asistencias = obtener_asistencias(token)
    usuarios = obtener_usuarios(token)
    
    if not asistencias and not usuarios:
        print("\n❌ No se pudieron obtener los datos del sistema.")
        return
    
    # Analizar
    asistencias_prueba = analizar_asistencias(asistencias, usuarios)
    
    # Exportar reporte
    if asistencias:
        exportar_reporte(asistencias, usuarios)
    
    # Preguntar si desea exportar CSV
    print("\n¿Deseas exportar las asistencias a CSV? (S/N): ", end="")
    respuesta = input().strip().upper()
    
    if respuesta == 'S':
        exportar_csv(asistencias)


def exportar_csv(asistencias):
    """
    Exporta asistencias a CSV
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"asistencias_export_{timestamp}.csv"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("userId,documento,nombre,timestamp,latitud,longitud\n")
        for a in asistencias:
            f.write(f"{a['userId']},{a['documento']},{a['nombre']},{a['timestamp']},{a.get('latitud', '')},{a.get('longitud', '')}\n")
    
    print(f"✅ Asistencias exportadas a: {filename}")


if __name__ == "__main__":
    main()
