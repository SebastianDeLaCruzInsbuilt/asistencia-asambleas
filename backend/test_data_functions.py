"""
Test script para verificar funciones de datos
Checkpoint Task 3
"""

import sys
import os

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(__file__))

from app import (
    cargar_usuarios_csv,
    parsear_csv,
    calcular_distancia_haversine,
    cargar_configuracion,
    cargar_asistencias,
    guardar_asistencias
)


def test_cargar_usuarios_csv():
    """Test: Cargar usuarios desde CSV"""
    print("✓ Test 1: Cargar usuarios desde CSV...")
    try:
        usuarios = cargar_usuarios_csv('data/usuarios.csv')
        assert len(usuarios) == 5, f"Esperaba 5 usuarios, obtuvo {len(usuarios)}"
        assert usuarios[0]['userId'] == '12345678'
        assert usuarios[0]['nombre'] == 'Juan Pérez'
        print("  ✓ Carga de usuarios exitosa")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_parsear_csv():
    """Test: Parsear contenido CSV"""
    print("✓ Test 2: Parsear contenido CSV...")
    try:
        contenido = """userId,documento,nombre
123,123,Test User
456,456,Another User"""
        usuarios = parsear_csv(contenido)
        assert len(usuarios) == 2
        assert usuarios[0]['userId'] == '123'
        print("  ✓ Parseo de CSV exitoso")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_parsear_csv_invalido():
    """Test: Validar que CSV inválido lance error"""
    print("✓ Test 3: Validar CSV inválido...")
    try:
        # CSV sin columnas requeridas
        contenido = """id,name
123,Test"""
        try:
            parsear_csv(contenido)
            print("  ✗ Debería haber lanzado ValueError")
            return False
        except ValueError as e:
            if "faltantes" in str(e).lower():
                print("  ✓ Validación de columnas correcta")
                return True
            else:
                print(f"  ✗ Error inesperado: {e}")
                return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_calcular_distancia_haversine():
    """Test: Calcular distancia entre dos puntos"""
    print("✓ Test 4: Calcular distancia Haversine...")
    try:
        # Distancia entre dos puntos idénticos debe ser 0
        dist = calcular_distancia_haversine(-12.0464, -77.0428, -12.0464, -77.0428)
        assert abs(dist) < 0.1, f"Distancia entre puntos idénticos debe ser ~0, obtuvo {dist}"
        
        # Distancia conocida (aproximadamente 111km por grado de latitud)
        dist2 = calcular_distancia_haversine(0, 0, 1, 0)
        assert 110000 < dist2 < 112000, f"Distancia esperada ~111km, obtuvo {dist2/1000}km"
        
        print("  ✓ Cálculo de distancia correcto")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_validar_coordenadas_invalidas():
    """Test: Validar que coordenadas inválidas lancen error"""
    print("✓ Test 5: Validar coordenadas inválidas...")
    try:
        # Latitud fuera de rango
        try:
            calcular_distancia_haversine(100, 0, 0, 0)
            print("  ✗ Debería haber lanzado ValueError para latitud inválida")
            return False
        except ValueError:
            pass
        
        # Longitud fuera de rango
        try:
            calcular_distancia_haversine(0, 200, 0, 0)
            print("  ✗ Debería haber lanzado ValueError para longitud inválida")
            return False
        except ValueError:
            pass
        
        print("  ✓ Validación de coordenadas correcta")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_cargar_configuracion():
    """Test: Cargar configuración desde JSON"""
    print("✓ Test 6: Cargar configuración...")
    try:
        config = cargar_configuracion('data/configuracion.json')
        assert 'ubicacionAsamblea' in config
        assert config['ubicacionAsamblea']['latitud'] == -12.0464
        assert config['ubicacionAsamblea']['longitud'] == -77.0428
        assert config['radioPermitido'] == 100
        print("  ✓ Carga de configuración exitosa")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_cargar_asistencias():
    """Test: Cargar asistencias desde JSON"""
    print("✓ Test 7: Cargar asistencias...")
    try:
        asistencias = cargar_asistencias('data/asistencias.json')
        assert isinstance(asistencias, list)
        print("  ✓ Carga de asistencias exitosa")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_guardar_asistencias():
    """Test: Guardar asistencias en JSON"""
    print("✓ Test 8: Guardar asistencias...")
    try:
        # Crear archivo temporal
        test_file = 'data/test_asistencias.json'
        test_data = [
            {
                'userId': '12345678',
                'nombre': 'Test User',
                'fechaHora': '2026-01-14T10:00:00Z',
                'ubicacion': {'latitud': -12.0464, 'longitud': -77.0428}
            }
        ]
        
        guardar_asistencias(test_data, test_file)
        
        # Verificar que se guardó correctamente
        asistencias_cargadas = cargar_asistencias(test_file)
        assert len(asistencias_cargadas) == 1
        assert asistencias_cargadas[0]['userId'] == '12345678'
        
        # Limpiar archivo temporal
        os.remove(test_file)
        
        print("  ✓ Guardado de asistencias exitoso")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        # Intentar limpiar archivo temporal si existe
        try:
            if os.path.exists('data/test_asistencias.json'):
                os.remove('data/test_asistencias.json')
        except:
            pass
        return False


def run_all_tests():
    """Ejecutar todos los tests"""
    print("\n" + "="*60)
    print("CHECKPOINT 3: Verificación de Funciones de Datos")
    print("="*60 + "\n")
    
    tests = [
        test_cargar_usuarios_csv,
        test_parsear_csv,
        test_parsear_csv_invalido,
        test_calcular_distancia_haversine,
        test_validar_coordenadas_invalidas,
        test_cargar_configuracion,
        test_cargar_asistencias,
        test_guardar_asistencias
    ]
    
    resultados = []
    for test in tests:
        resultado = test()
        resultados.append(resultado)
        print()
    
    print("="*60)
    exitosos = sum(resultados)
    total = len(resultados)
    print(f"Resultados: {exitosos}/{total} tests pasaron")
    
    if exitosos == total:
        print("✓ TODAS LAS PRUEBAS PASARON")
        print("="*60 + "\n")
        return True
    else:
        print("✗ ALGUNAS PRUEBAS FALLARON")
        print("="*60 + "\n")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
