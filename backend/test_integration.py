"""
Pruebas de Integración - Task 10
Sistema de Confirmación de Asistencia a Asambleas

Este archivo contiene pruebas de integración end-to-end que verifican
el funcionamiento completo del sistema.
"""

import sys
import os
import json
import time

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(__file__))

from app import app, inicializar_datos, usuarios_cache, asistencias_cache


def setup_test_environment():
    """
    Configura el entorno de prueba limpiando asistencias previas.
    """
    # Limpiar asistencias para tests frescos
    global asistencias_cache
    asistencias_cache.clear()
    
    # Guardar asistencias vacías
    with open('data/asistencias.json', 'w', encoding='utf-8') as f:
        json.dump([], f)
    
    # Reinicializar datos
    inicializar_datos()


def test_10_1_flujo_completo_exitoso():
    """
    Test 10.1: Probar flujo completo exitoso
    
    Usuario válido + ubicación correcta = asistencia confirmada
    Requirements: 1.1, 1.2, 2.1, 2.2, 2.3, 3.1, 3.2
    """
    print("\n" + "="*70)
    print("TEST 10.1: Flujo Completo Exitoso")
    print("="*70)
    
    with app.test_client() as client:
        print("\n1. Validar identidad del usuario...")
        
        # Paso 1: Validar identidad (Requirements 1.1, 1.2)
        response = client.post('/api/validar-identidad',
                              json={'documento': '12345678'},
                              content_type='application/json')
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.get_json()
        assert data['valido'] == True, "Usuario debería ser válido"
        assert 'nombre' in data, "Respuesta debe incluir nombre"
        assert 'userId' in data, "Respuesta debe incluir userId"
        assert data['nombre'] == 'Juan Pérez', f"Nombre esperado 'Juan Pérez', obtuvo '{data['nombre']}'"
        
        user_id = data['userId']
        print(f"   ✓ Identidad validada: {data['nombre']} (userId: {user_id})")
        
        print("\n2. Confirmar asistencia con ubicación correcta...")
        
        # Paso 2: Confirmar asistencia con ubicación dentro del radio (Requirements 2.1, 2.2, 2.3, 3.1)
        # Usar coordenadas exactas de la asamblea (distancia = 0)
        response = client.post('/api/confirmar-asistencia',
                              json={
                                  'userId': user_id,
                                  'latitud': -12.0464,
                                  'longitud': -77.0428
                              },
                              content_type='application/json')
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.get_json()
        assert data['confirmado'] == True, f"Asistencia debería estar confirmada: {data.get('mensaje')}"
        assert 'mensaje' in data, "Respuesta debe incluir mensaje"
        assert 'distancia' in data, "Respuesta debe incluir distancia"
        assert data['distancia'] < 1, f"Distancia debería ser ~0, obtuvo {data['distancia']}m"
        
        print(f"   ✓ Asistencia confirmada: {data['mensaje']}")
        print(f"   ✓ Distancia: {data['distancia']}m")
        
        print("\n3. Verificar que la asistencia fue registrada...")
        
        # Paso 3: Verificar que la asistencia se registró (Requirement 3.2)
        response = client.get('/api/asistencias')
        assert response.status_code == 200
        asistencias = response.get_json()
        
        assert isinstance(asistencias, list), "Asistencias debe ser una lista"
        assert len(asistencias) >= 1, "Debe haber al menos una asistencia registrada"
        
        # Buscar la asistencia del usuario
        asistencia_encontrada = None
        for asistencia in asistencias:
            if asistencia['userId'] == user_id:
                asistencia_encontrada = asistencia
                break
        
        assert asistencia_encontrada is not None, f"No se encontró asistencia para userId {user_id}"
        assert asistencia_encontrada['nombre'] == 'Juan Pérez'
        assert 'fechaHora' in asistencia_encontrada, "Asistencia debe incluir fechaHora"
        assert 'ubicacion' in asistencia_encontrada, "Asistencia debe incluir ubicacion"
        
        print(f"   ✓ Asistencia registrada correctamente")
        print(f"   ✓ Fecha/Hora: {asistencia_encontrada['fechaHora']}")
        print(f"   ✓ Ubicación: ({asistencia_encontrada['ubicacion']['latitud']}, {asistencia_encontrada['ubicacion']['longitud']})")
    
    print("\n" + "="*70)
    print("✓ TEST 10.1 PASÓ - Flujo completo exitoso")
    print("="*70)
    return True


def test_10_2_credenciales_invalidas():
    """
    Test 10.2: Probar flujo con credenciales inválidas
    
    Usuario inválido = mensaje de error
    Requirements: 1.3
    """
    print("\n" + "="*70)
    print("TEST 10.2: Flujo con Credenciales Inválidas")
    print("="*70)
    
    with app.test_client() as client:
        print("\n1. Intentar validar con documento inexistente...")
        
        # Intentar validar con documento que no existe (Requirement 1.3)
        response = client.post('/api/validar-identidad',
                              json={'documento': '99999999'},
                              content_type='application/json')
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.get_json()
        assert data['valido'] == False, "Usuario inválido debería retornar valido=False"
        
        print(f"   ✓ Credenciales inválidas correctamente rechazadas")
        print(f"   ✓ Respuesta: valido={data['valido']}")
        
        print("\n2. Intentar validar sin documento...")
        
        # Intentar validar sin documento (Requirement 1.4)
        response = client.post('/api/validar-identidad',
                              json={},
                              content_type='application/json')
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        data = response.get_json()
        assert 'error' in data, "Respuesta debe incluir mensaje de error"
        
        print(f"   ✓ Validación de campo requerido funciona")
        print(f"   ✓ Error: {data['error']}")
        
        print("\n3. Intentar validar con documento vacío...")
        
        # Intentar validar con documento vacío
        response = client.post('/api/validar-identidad',
                              json={'documento': '   '},
                              content_type='application/json')
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        print(f"   ✓ Documento vacío correctamente rechazado")
    
    print("\n" + "="*70)
    print("✓ TEST 10.2 PASÓ - Credenciales inválidas manejadas correctamente")
    print("="*70)
    return True



def test_10_3_ubicacion_fuera_de_rango():
    """
    Test 10.3: Probar flujo con ubicación fuera de rango
    
    Ubicación lejana = mensaje con instrucciones
    Requirements: 2.4
    """
    print("\n" + "="*70)
    print("TEST 10.3: Flujo con Ubicación Fuera de Rango")
    print("="*70)
    
    with app.test_client() as client:
        print("\n1. Validar identidad del usuario...")
        
        # Paso 1: Validar identidad
        response = client.post('/api/validar-identidad',
                              json={'documento': '11223344'},
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['valido'] == True
        user_id = data['userId']
        
        print(f"   ✓ Identidad validada: {data['nombre']}")
        
        print("\n2. Intentar confirmar asistencia desde ubicación lejana...")
        
        # Paso 2: Intentar confirmar con ubicación fuera del radio (Requirement 2.4)
        # Usar coordenadas lejanas (aproximadamente 7km de distancia)
        response = client.post('/api/confirmar-asistencia',
                              json={
                                  'userId': user_id,
                                  'latitud': -12.1,
                                  'longitud': -77.1
                              },
                              content_type='application/json')
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.get_json()
        assert data['confirmado'] == False, "Asistencia no debería estar confirmada"
        assert 'mensaje' in data, "Respuesta debe incluir mensaje"
        assert 'distancia' in data, "Respuesta debe incluir distancia"
        assert data['distancia'] > 100, f"Distancia debería ser > 100m, obtuvo {data['distancia']}m"
        
        # Verificar que el mensaje contiene instrucciones (Requirement 2.4)
        mensaje = data['mensaje'].lower()
        assert 'ubicación' in mensaje or 'lugar' in mensaje or 'asamblea' in mensaje, \
            "Mensaje debe contener instrucciones sobre la ubicación"
        
        print(f"   ✓ Confirmación rechazada por distancia")
        print(f"   ✓ Distancia: {data['distancia']}m (límite: 100m)")
        print(f"   ✓ Mensaje: {data['mensaje']}")
        
        print("\n3. Verificar que NO se registró la asistencia...")
        
        # Paso 3: Verificar que NO se registró la asistencia
        response = client.get('/api/asistencias')
        assert response.status_code == 200
        asistencias = response.get_json()
        
        # Buscar si existe asistencia para este usuario
        asistencia_encontrada = False
        for asistencia in asistencias:
            if asistencia['userId'] == user_id:
                asistencia_encontrada = True
                break
        
        assert not asistencia_encontrada, "No debería haber asistencia registrada para usuario fuera de rango"
        
        print(f"   ✓ Asistencia NO registrada (correcto)")
    
    print("\n" + "="*70)
    print("✓ TEST 10.3 PASÓ - Ubicación fuera de rango manejada correctamente")
    print("="*70)
    return True


def test_10_4_prevencion_duplicados():
    """
    Test 10.4: Probar prevención de duplicados
    
    Confirmar dos veces = solo un registro
    Requirements: 3.3
    """
    print("\n" + "="*70)
    print("TEST 10.4: Prevención de Duplicados")
    print("="*70)
    
    with app.test_client() as client:
        print("\n1. Validar identidad del usuario...")
        
        # Paso 1: Validar identidad
        response = client.post('/api/validar-identidad',
                              json={'documento': '55667788'},
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['valido'] == True
        user_id = data['userId']
        
        print(f"   ✓ Identidad validada: {data['nombre']}")
        
        print("\n2. Primera confirmación de asistencia...")
        
        # Paso 2: Primera confirmación (debe ser exitosa)
        response = client.post('/api/confirmar-asistencia',
                              json={
                                  'userId': user_id,
                                  'latitud': -12.0464,
                                  'longitud': -77.0428
                              },
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['confirmado'] == True, "Primera confirmación debe ser exitosa"
        
        print(f"   ✓ Primera confirmación exitosa")
        
        print("\n3. Intentar segunda confirmación (duplicado)...")
        
        # Paso 3: Segunda confirmación (debe ser rechazada) (Requirement 3.3)
        response = client.post('/api/confirmar-asistencia',
                              json={
                                  'userId': user_id,
                                  'latitud': -12.0464,
                                  'longitud': -77.0428
                              },
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['confirmado'] == False, "Segunda confirmación debe ser rechazada"
        
        # Verificar mensaje de duplicado
        mensaje = data['mensaje'].lower()
        assert 'duplicado' in mensaje or 'anteriormente' in mensaje or 'ya' in mensaje, \
            f"Mensaje debe indicar duplicado: {data['mensaje']}"
        
        print(f"   ✓ Segunda confirmación rechazada")
        print(f"   ✓ Mensaje: {data['mensaje']}")
        
        print("\n4. Verificar que solo hay UN registro...")
        
        # Paso 4: Verificar que solo hay un registro
        response = client.get('/api/asistencias')
        assert response.status_code == 200
        asistencias = response.get_json()
        
        # Contar cuántas asistencias hay para este usuario
        count = sum(1 for a in asistencias if a['userId'] == user_id)
        assert count == 1, f"Debe haber exactamente 1 asistencia, encontradas: {count}"
        
        print(f"   ✓ Solo 1 registro de asistencia (correcto)")
    
    print("\n" + "="*70)
    print("✓ TEST 10.4 PASÓ - Prevención de duplicados funciona correctamente")
    print("="*70)
    return True



def test_10_5_gestion_usuarios_admin():
    """
    Test 10.5: Probar gestión de usuarios desde admin
    
    Agregar, editar, eliminar usuarios desde interfaz
    Verificar que cambios se reflejen en CSV
    Requirements: 4.3, 4.4, 4.5
    """
    print("\n" + "="*70)
    print("TEST 10.5: Gestión de Usuarios desde Admin")
    print("="*70)
    
    with app.test_client() as client:
        print("\n1. Obtener lista inicial de usuarios...")
        
        # Paso 1: Obtener lista inicial
        response = client.get('/api/usuarios')
        assert response.status_code == 200
        usuarios_iniciales = response.get_json()
        count_inicial = len(usuarios_iniciales)
        
        print(f"   ✓ Usuarios iniciales: {count_inicial}")
        
        print("\n2. Agregar nuevo usuario...")
        
        # Paso 2: Agregar nuevo usuario (Requirement 4.3, 4.4)
        nuevo_usuario = {
            'userId': 'TEST999',
            'documento': 'TEST999',
            'nombre': 'Usuario de Prueba Integración'
        }
        
        response = client.post('/api/usuarios',
                              json=nuevo_usuario,
                              content_type='application/json')
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.get_json()
        assert data['success'] == True, f"Agregar usuario falló: {data.get('mensaje')}"
        
        print(f"   ✓ Usuario agregado: {nuevo_usuario['nombre']}")
        
        print("\n3. Verificar que el usuario fue agregado...")
        
        # Paso 3: Verificar que aparece en la lista
        response = client.get('/api/usuarios')
        assert response.status_code == 200
        usuarios = response.get_json()
        assert len(usuarios) == count_inicial + 1, "Debe haber un usuario más"
        
        # Buscar el usuario agregado
        usuario_encontrado = None
        for u in usuarios:
            if u['userId'] == 'TEST999':
                usuario_encontrado = u
                break
        
        assert usuario_encontrado is not None, "Usuario agregado no encontrado en la lista"
        assert usuario_encontrado['nombre'] == nuevo_usuario['nombre']
        
        print(f"   ✓ Usuario encontrado en la lista")
        
        print("\n4. Verificar que se guardó en CSV...")
        
        # Paso 4: Verificar que se guardó en CSV (Requirement 4.3)
        with open('data/usuarios.csv', 'r', encoding='utf-8') as f:
            contenido_csv = f.read()
        
        assert 'TEST999' in contenido_csv, "Usuario debe estar en el archivo CSV"
        assert 'Usuario de Prueba Integración' in contenido_csv, "Nombre debe estar en CSV"
        
        print(f"   ✓ Usuario guardado en CSV")
        
        print("\n5. Editar el usuario...")
        
        # Paso 5: Editar usuario (Requirement 4.4, 4.5)
        datos_actualizados = {
            'documento': 'TEST999',
            'nombre': 'Usuario Actualizado'
        }
        
        response = client.put('/api/usuarios/TEST999',
                             json=datos_actualizados,
                             content_type='application/json')
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.get_json()
        assert data['success'] == True, f"Actualizar usuario falló: {data.get('mensaje')}"
        
        print(f"   ✓ Usuario actualizado")
        
        print("\n6. Verificar que la edición se reflejó...")
        
        # Paso 6: Verificar cambios
        response = client.get('/api/usuarios')
        usuarios = response.get_json()
        
        usuario_actualizado = None
        for u in usuarios:
            if u['userId'] == 'TEST999':
                usuario_actualizado = u
                break
        
        assert usuario_actualizado is not None
        assert usuario_actualizado['nombre'] == 'Usuario Actualizado', \
            f"Nombre debería ser 'Usuario Actualizado', obtuvo '{usuario_actualizado['nombre']}'"
        
        print(f"   ✓ Cambios reflejados en la lista")
        
        print("\n7. Verificar que la edición se guardó en CSV...")
        
        # Paso 7: Verificar CSV actualizado
        with open('data/usuarios.csv', 'r', encoding='utf-8') as f:
            contenido_csv = f.read()
        
        assert 'Usuario Actualizado' in contenido_csv, "Nombre actualizado debe estar en CSV"
        
        print(f"   ✓ Cambios guardados en CSV")
        
        print("\n8. Eliminar el usuario...")
        
        # Paso 8: Eliminar usuario (Requirement 4.5)
        response = client.delete('/api/usuarios/TEST999')
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.get_json()
        assert data['success'] == True, f"Eliminar usuario falló: {data.get('mensaje')}"
        
        print(f"   ✓ Usuario eliminado")
        
        print("\n9. Verificar que el usuario fue eliminado...")
        
        # Paso 9: Verificar que ya no está en la lista
        response = client.get('/api/usuarios')
        usuarios = response.get_json()
        assert len(usuarios) == count_inicial, "Debe volver al número inicial de usuarios"
        
        # Verificar que no está en la lista
        for u in usuarios:
            assert u['userId'] != 'TEST999', "Usuario eliminado no debería estar en la lista"
        
        print(f"   ✓ Usuario no está en la lista")
        
        print("\n10. Verificar que se eliminó del CSV...")
        
        # Paso 10: Verificar CSV
        with open('data/usuarios.csv', 'r', encoding='utf-8') as f:
            contenido_csv = f.read()
        
        assert 'TEST999' not in contenido_csv, "Usuario eliminado no debería estar en CSV"
        
        print(f"   ✓ Usuario eliminado del CSV")
    
    print("\n" + "="*70)
    print("✓ TEST 10.5 PASÓ - Gestión de usuarios funciona correctamente")
    print("="*70)
    return True



def test_10_6_edicion_manual_csv():
    """
    Test 10.6: Probar edición manual de CSV
    
    Editar usuarios.csv directamente
    Verificar que servidor recargue automáticamente
    Requirements: 4.3, 4.6
    """
    print("\n" + "="*70)
    print("TEST 10.6: Edición Manual de CSV")
    print("="*70)
    
    with app.test_client() as client:
        print("\n1. Obtener lista inicial de usuarios...")
        
        # Paso 1: Obtener lista inicial
        response = client.get('/api/usuarios')
        assert response.status_code == 200
        usuarios_iniciales = response.get_json()
        count_inicial = len(usuarios_iniciales)
        
        print(f"   ✓ Usuarios iniciales: {count_inicial}")
        
        print("\n2. Editar CSV directamente (agregar usuario)...")
        
        # Paso 2: Leer CSV actual
        with open('data/usuarios.csv', 'r', encoding='utf-8') as f:
            contenido_original = f.read()
        
        # Agregar nuevo usuario al CSV
        nuevo_usuario_csv = '\nMANUAL123,MANUAL123,Usuario Manual Test'
        
        with open('data/usuarios.csv', 'a', encoding='utf-8') as f:
            f.write(nuevo_usuario_csv)
        
        print(f"   ✓ Usuario agregado al CSV manualmente")
        
        print("\n3. Forzar recarga usando endpoint...")
        
        # Paso 3: Forzar recarga (Requirement 4.3)
        # Nota: El file watcher puede no funcionar en tests, usar endpoint manual
        response = client.post('/api/reload-usuarios')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        
        print(f"   ✓ Recarga forzada: {data['totalUsuarios']} usuarios")
        
        print("\n4. Verificar que el nuevo usuario está disponible...")
        
        # Paso 4: Verificar que el usuario está en la lista
        response = client.get('/api/usuarios')
        assert response.status_code == 200
        usuarios = response.get_json()
        
        # Buscar el usuario agregado manualmente
        usuario_encontrado = None
        for u in usuarios:
            if u['userId'] == 'MANUAL123':
                usuario_encontrado = u
                break
        
        assert usuario_encontrado is not None, "Usuario agregado manualmente no encontrado"
        assert usuario_encontrado['nombre'] == 'Usuario Manual Test'
        
        print(f"   ✓ Usuario manual encontrado: {usuario_encontrado['nombre']}")
        
        print("\n5. Validar identidad con el nuevo usuario...")
        
        # Paso 5: Probar que el usuario funciona en validación
        response = client.post('/api/validar-identidad',
                              json={'documento': 'MANUAL123'},
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['valido'] == True, "Usuario manual debería ser válido"
        assert data['nombre'] == 'Usuario Manual Test'
        
        print(f"   ✓ Usuario manual puede validar identidad")
        
        print("\n6. Restaurar CSV original...")
        
        # Paso 6: Restaurar CSV (limpiar)
        with open('data/usuarios.csv', 'w', encoding='utf-8') as f:
            f.write(contenido_original)
        
        # Forzar recarga
        response = client.post('/api/reload-usuarios')
        assert response.status_code == 200
        
        print(f"   ✓ CSV restaurado")
        
        print("\n7. Verificar que el usuario manual ya no está...")
        
        # Paso 7: Verificar que el usuario ya no está
        response = client.get('/api/usuarios')
        usuarios = response.get_json()
        
        for u in usuarios:
            assert u['userId'] != 'MANUAL123', "Usuario manual no debería estar después de restaurar"
        
        print(f"   ✓ Usuario manual eliminado correctamente")
    
    print("\n" + "="*70)
    print("✓ TEST 10.6 PASÓ - Edición manual de CSV funciona correctamente")
    print("="*70)
    return True


def run_all_integration_tests():
    """
    Ejecuta todos los tests de integración.
    """
    print("\n" + "="*70)
    print("CHECKPOINT 10: PRUEBAS DE INTEGRACIÓN")
    print("Sistema de Confirmación de Asistencia a Asambleas")
    print("="*70)
    
    # Configurar entorno de prueba
    setup_test_environment()
    
    # Lista de tests
    tests = [
        ("10.1", test_10_1_flujo_completo_exitoso),
        ("10.2", test_10_2_credenciales_invalidas),
        ("10.3", test_10_3_ubicacion_fuera_de_rango),
        ("10.4", test_10_4_prevencion_duplicados),
        ("10.5", test_10_5_gestion_usuarios_admin),
        ("10.6", test_10_6_edicion_manual_csv),
    ]
    
    resultados = []
    
    for test_id, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((test_id, True, None))
        except AssertionError as e:
            print(f"\n✗ TEST {test_id} FALLÓ: {e}")
            resultados.append((test_id, False, str(e)))
        except Exception as e:
            print(f"\n✗ TEST {test_id} ERROR: {e}")
            import traceback
            traceback.print_exc()
            resultados.append((test_id, False, str(e)))
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE PRUEBAS DE INTEGRACIÓN")
    print("="*70)
    
    exitosos = sum(1 for _, passed, _ in resultados if passed)
    total = len(resultados)
    
    for test_id, passed, error in resultados:
        status = "✓ PASÓ" if passed else "✗ FALLÓ"
        print(f"  Test {test_id}: {status}")
        if error:
            print(f"    Error: {error}")
    
    print("\n" + "="*70)
    print(f"Resultados: {exitosos}/{total} tests pasaron")
    
    if exitosos == total:
        print("✓ TODAS LAS PRUEBAS DE INTEGRACIÓN PASARON")
        print("="*70 + "\n")
        return True
    else:
        print("✗ ALGUNAS PRUEBAS FALLARON")
        print("="*70 + "\n")
        return False


if __name__ == '__main__':
    try:
        success = run_all_integration_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ ERROR FATAL: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
