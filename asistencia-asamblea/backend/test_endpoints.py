"""
Test script para verificar endpoints del backend
Task 4 - Checkpoint
"""

import sys
import os
import json

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(__file__))

from app import app, inicializar_datos


def test_endpoints():
    """
    Prueba básica de los endpoints implementados.
    """
    print("\n" + "="*60)
    print("TEST: Verificación de Endpoints del Backend")
    print("="*60 + "\n")
    
    # Inicializar datos
    inicializar_datos()
    
    # Crear cliente de prueba
    with app.test_client() as client:
        
        # Test 1: GET /api/configuracion
        print("✓ Test 1: GET /api/configuracion")
        response = client.get('/api/configuracion')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.get_json()
        assert 'ubicacionAsamblea' in data
        assert 'radioPermitido' in data
        print(f"  ✓ Configuración obtenida: Radio {data['radioPermitido']}m")
        print()
        
        # Test 2: POST /api/validar-identidad (válido)
        print("✓ Test 2: POST /api/validar-identidad (credenciales válidas)")
        response = client.post('/api/validar-identidad',
                              json={'documento': '12345678'},
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['valido'] == True
        assert 'nombre' in data
        assert 'userId' in data
        print(f"  ✓ Usuario válido: {data['nombre']}")
        print()
        
        # Test 3: POST /api/validar-identidad (inválido)
        print("✓ Test 3: POST /api/validar-identidad (credenciales inválidas)")
        response = client.post('/api/validar-identidad',
                              json={'documento': '99999999'},
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['valido'] == False
        print("  ✓ Usuario inválido correctamente rechazado")
        print()
        
        # Test 4: POST /api/validar-identidad (sin datos)
        print("✓ Test 4: POST /api/validar-identidad (sin documento)")
        response = client.post('/api/validar-identidad',
                              json={},
                              content_type='application/json')
        assert response.status_code == 400
        print("  ✓ Validación de campos requeridos funciona")
        print()
        
        # Test 5: POST /api/confirmar-asistencia (dentro del radio)
        print("✓ Test 5: POST /api/confirmar-asistencia (dentro del radio)")
        # Primero validar identidad para obtener userId
        val_response = client.post('/api/validar-identidad',
                                   json={'documento': '87654321'},
                                   content_type='application/json')
        val_data = val_response.get_json()
        user_id = val_data['userId']
        
        response = client.post('/api/confirmar-asistencia',
                              json={
                                  'userId': user_id,
                                  'latitud': -12.0464,
                                  'longitud': -77.0428
                              },
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['confirmado'] == True
        print(f"  ✓ Asistencia confirmada: {data['mensaje']}")
        print()
        
        # Test 6: POST /api/confirmar-asistencia (duplicado)
        print("✓ Test 6: POST /api/confirmar-asistencia (duplicado)")
        response = client.post('/api/confirmar-asistencia',
                              json={
                                  'userId': user_id,
                                  'latitud': -12.0464,
                                  'longitud': -77.0428
                              },
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['confirmado'] == False
        assert 'duplicado' in data['mensaje'].lower() or 'anteriormente' in data['mensaje'].lower()
        print("  ✓ Duplicado correctamente rechazado")
        print()
        
        # Test 7: POST /api/confirmar-asistencia (fuera del radio)
        print("✓ Test 7: POST /api/confirmar-asistencia (fuera del radio)")
        # Validar otro usuario
        val_response = client.post('/api/validar-identidad',
                                   json={'documento': '11223344'},
                                   content_type='application/json')
        val_data = val_response.get_json()
        user_id_2 = val_data['userId']
        
        response = client.post('/api/confirmar-asistencia',
                              json={
                                  'userId': user_id_2,
                                  'latitud': -12.1,
                                  'longitud': -77.1
                              },
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['confirmado'] == False
        assert data['distancia'] > 100
        print(f"  ✓ Fuera de rango: {data['distancia']}m")
        print()
        
        # Test 8: GET /api/asistencias
        print("✓ Test 8: GET /api/asistencias")
        response = client.get('/api/asistencias')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1  # Al menos la asistencia del test 5
        print(f"  ✓ {len(data)} asistencia(s) registrada(s)")
        print()
        
        # Test 9: GET /api/usuarios
        print("✓ Test 9: GET /api/usuarios")
        response = client.get('/api/usuarios')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"  ✓ {len(data)} usuario(s) en la lista")
        print()
        
        # Test 10: POST /api/usuarios
        print("✓ Test 10: POST /api/usuarios (agregar)")
        response = client.post('/api/usuarios',
                              json={
                                  'userId': 'TEST123',
                                  'documento': 'TEST123',
                                  'nombre': 'Usuario de Prueba'
                              },
                              content_type='application/json')
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] == True
        print("  ✓ Usuario agregado exitosamente")
        print()
        
        # Test 11: PUT /api/usuarios/:userId
        print("✓ Test 11: PUT /api/usuarios/TEST123 (actualizar)")
        response = client.put('/api/usuarios/TEST123',
                             json={
                                 'documento': 'TEST123',
                                 'nombre': 'Usuario Actualizado'
                             },
                             content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        print("  ✓ Usuario actualizado exitosamente")
        print()
        
        # Test 12: DELETE /api/usuarios/:userId
        print("✓ Test 12: DELETE /api/usuarios/TEST123 (eliminar)")
        response = client.delete('/api/usuarios/TEST123')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        print("  ✓ Usuario eliminado exitosamente")
        print()
        
        # Test 13: Validar coordenadas inválidas
        print("✓ Test 13: POST /api/confirmar-asistencia (coordenadas inválidas)")
        # Validar usuario primero
        val_response = client.post('/api/validar-identidad',
                                   json={'documento': '55667788'},
                                   content_type='application/json')
        val_data = val_response.get_json()
        user_id_3 = val_data['userId']
        
        response = client.post('/api/confirmar-asistencia',
                              json={
                                  'userId': user_id_3,
                                  'latitud': 100,  # Fuera de rango
                                  'longitud': -77.0428
                              },
                              content_type='application/json')
        assert response.status_code == 400
        print("  ✓ Coordenadas inválidas correctamente rechazadas")
        print()
    
    print("="*60)
    print("✓ TODOS LOS TESTS PASARON")
    print("="*60 + "\n")
    return True


if __name__ == '__main__':
    try:
        success = test_endpoints()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
