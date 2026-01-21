#!/usr/bin/env python3
"""
Muestra la configuración actual del sistema
"""

import requests

BASE_URL = "https://web-production-299e4.up.railway.app"
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

# Login
print("🔐 Autenticando...")
response = requests.post(
    f"{BASE_URL}/api/admin/login",
    json={"username": ADMIN_USER, "password": ADMIN_PASS}
)

if response.status_code != 200:
    print("❌ Error al autenticar")
    exit(1)

token = response.json().get('token')
print("✅ Autenticado\n")

# Obtener configuración
print("📋 Obteniendo configuración...")
response = requests.get(
    f"{BASE_URL}/api/configuracion",
    headers={"Authorization": f"Bearer {token}"}
)

if response.status_code == 200:
    config = response.json()
    print("\n" + "="*60)
    print("CONFIGURACIÓN ACTUAL")
    print("="*60)
    print(f"\nUbicación de la Asamblea:")
    print(f"  Latitud: {config['ubicacionAsamblea']['latitud']}")
    print(f"  Longitud: {config['ubicacionAsamblea']['longitud']}")
    print(f"  Radio permitido: {config['radioPermitido']} metros")
    print("\n" + "="*60)
    
    # Sugerir coordenadas para prueba
    lat = config['ubicacionAsamblea']['latitud']
    lon = config['ubicacionAsamblea']['longitud']
    
    print(f"\n💡 Para la prueba de carga, usa estas coordenadas:")
    print(f"   Latitud: {lat}")
    print(f"   Longitud: {lon}")
    print(f"\n   O actualiza la configuración en el panel admin a:")
    print(f"   Latitud: -12.0464")
    print(f"   Longitud: -77.0428")
else:
    print(f"❌ Error al obtener configuración: {response.status_code}")
