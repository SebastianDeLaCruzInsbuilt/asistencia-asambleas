#!/usr/bin/env python3
"""
Genera archivo CSV con usuarios de prueba para prueba de carga
"""

NUM_USUARIOS = 500

print(f"Generando {NUM_USUARIOS} usuarios de prueba...")

filename = "usuarios_prueba_carga.csv"

with open(filename, 'w', encoding='utf-8') as f:
    f.write("userId,documento,nombre\n")
    for i in range(1, NUM_USUARIOS + 1):
        user_id = f"TEST{i:04d}"
        documento = f"1234567{i:04d}"
        nombre = f"Usuario Test {i}"
        f.write(f"{user_id},{documento},{nombre}\n")

print(f"✅ Archivo CSV generado: {filename}")
print(f"   Total de usuarios: {NUM_USUARIOS}")
print(f"\nPróximos pasos:")
print(f"1. Importa este archivo desde el panel admin")
print(f"2. Ejecuta: python test_carga.py")
