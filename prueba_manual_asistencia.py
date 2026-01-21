#!/usr/bin/env python3
"""
Prueba manual de confirmación de asistencia
"""

import requests

BASE_URL = "https://web-production-299e4.up.railway.app"

# Probar con un usuario de prueba
usuario_prueba = {
    "userId": "TEST0001",
    "documento": "12345670001",
    "latitud": -12.0464,
    "longitud": -77.0428
}

print("Probando confirmación de asistencia...")
print(f"Usuario: {usuario_prueba['userId']}")
print(f"Ubicación: {usuario_prueba['latitud']}, {usuario_prueba['longitud']}")

response = requests.post(
    f"{BASE_URL}/api/confirmar-asistencia",
    json=usuario_prueba
)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code == 200:
    data = response.json()
    if data.get('confirmado'):
        print("\n✅ Asistencia confirmada exitosamente!")
    else:
        print(f"\n❌ No se pudo confirmar: {data.get('mensaje')}")
else:
    print(f"\n❌ Error: {response.status_code}")
