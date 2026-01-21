"""
Sistema de Confirmación de Asistencia a Asambleas
Backend Flask Application
"""

import csv
import json
import math
import os
import threading
import secrets
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from functools import wraps


# ============================================================================
# FUNCIONES DE CARGA Y PARSEO DE CSV (Sub-task 2.1)
# ============================================================================

def cargar_usuarios_csv(ruta_archivo: str = 'data/usuarios.csv') -> List[Dict[str, str]]:
    """
    Carga usuarios desde archivo CSV y retorna lista de diccionarios.
    
    Args:
        ruta_archivo: Ruta al archivo CSV de usuarios
        
    Returns:
        Lista de diccionarios con usuarios cargados
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el formato CSV es inválido
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            return parsear_csv(contenido)
    except Exception as e:
        raise ValueError(f"Error al leer archivo CSV: {str(e)}")


def parsear_csv(contenido_csv: str) -> List[Dict[str, str]]:
    """
    Parsea contenido CSV a lista de diccionarios.
    
    Args:
        contenido_csv: Contenido del archivo CSV como string
        
    Returns:
        Lista de diccionarios con los datos parseados
        
    Raises:
        ValueError: Si el formato CSV es inválido o faltan columnas requeridas
    """
    if not contenido_csv or not contenido_csv.strip():
        raise ValueError("Contenido CSV vacío")
    
    # Parsear CSV
    lineas = contenido_csv.strip().split('\n')
    if len(lineas) < 1:
        raise ValueError("CSV debe contener al menos la fila de encabezados")
    
    lector = csv.DictReader(lineas)
    
    # Validar columnas requeridas
    columnas_requeridas = {'userId', 'documento', 'nombre'}
    if lector.fieldnames is None:
        raise ValueError("No se pudieron leer los encabezados del CSV")
    
    columnas_presentes = set(lector.fieldnames)
    columnas_faltantes = columnas_requeridas - columnas_presentes
    
    if columnas_faltantes:
        raise ValueError(
            f"Columnas requeridas faltantes en CSV: {', '.join(columnas_faltantes)}"
        )
    
    # Parsear filas
    usuarios = []
    for numero_linea, fila in enumerate(lector, start=2):  # start=2 porque línea 1 es header
        # Validar que la fila tenga datos
        if not fila.get('userId') or not fila.get('documento') or not fila.get('nombre'):
            # Ignorar filas vacías o incompletas
            continue
        
        usuarios.append({
            'userId': fila['userId'].strip(),
            'documento': fila['documento'].strip(),
            'nombre': fila['nombre'].strip()
        })
    
    return usuarios



# ============================================================================
# FUNCIÓN DE CÁLCULO DE DISTANCIA HAVERSINE (Sub-task 2.3)
# ============================================================================

def calcular_distancia_haversine(
    lat1: float, 
    lon1: float, 
    lat2: float, 
    lon2: float
) -> float:
    """
    Calcula la distancia entre dos puntos geográficos usando la fórmula de Haversine.
    
    La fórmula de Haversine calcula la distancia entre dos puntos en una esfera
    dados sus coordenadas de latitud y longitud.
    
    Fórmula:
        a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
        c = 2 × atan2(√a, √(1−a))
        d = R × c
    
    Args:
        lat1: Latitud del primer punto en grados decimales
        lon1: Longitud del primer punto en grados decimales
        lat2: Latitud del segundo punto en grados decimales
        lon2: Longitud del segundo punto en grados decimales
        
    Returns:
        Distancia en metros entre los dos puntos
        
    Raises:
        ValueError: Si las coordenadas están fuera de rango válido
    """
    # Validar coordenadas
    if not (-90 <= lat1 <= 90) or not (-90 <= lat2 <= 90):
        raise ValueError("Latitud debe estar entre -90 y 90 grados")
    if not (-180 <= lon1 <= 180) or not (-180 <= lon2 <= 180):
        raise ValueError("Longitud debe estar entre -180 y 180 grados")
    
    # Radio de la Tierra en metros
    R = 6371000  # 6371 km = 6371000 metros
    
    # Convertir grados a radianes
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    # Aplicar fórmula de Haversine
    a = (math.sin(delta_lat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * 
         math.sin(delta_lon / 2) ** 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distancia en metros
    distancia = R * c
    
    return distancia



# ============================================================================
# FUNCIONES DE CARGA DE CONFIGURACIÓN Y ASISTENCIAS (Sub-task 2.5)
# ============================================================================

def cargar_configuracion(ruta_archivo: str = 'data/configuracion.json') -> Dict:
    """
    Carga la configuración de la asamblea desde archivo JSON.
    
    Args:
        ruta_archivo: Ruta al archivo JSON de configuración
        
    Returns:
        Diccionario con la configuración de la asamblea
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el formato JSON es inválido o faltan campos requeridos
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            configuracion = json.load(archivo)
        
        # Validar estructura requerida
        if 'ubicacionAsamblea' not in configuracion:
            raise ValueError("Falta campo 'ubicacionAsamblea' en configuración")
        
        if 'latitud' not in configuracion['ubicacionAsamblea']:
            raise ValueError("Falta campo 'latitud' en ubicacionAsamblea")
        
        if 'longitud' not in configuracion['ubicacionAsamblea']:
            raise ValueError("Falta campo 'longitud' en ubicacionAsamblea")
        
        if 'radioPermitido' not in configuracion:
            raise ValueError("Falta campo 'radioPermitido' en configuración")
        
        # Validar coordenadas usando función de validación (Requirement 4.6)
        lat = configuracion['ubicacionAsamblea']['latitud']
        lon = configuracion['ubicacionAsamblea']['longitud']
        
        es_valido, mensaje_error, _ = validar_coordenadas(lat, lon)
        if not es_valido:
            raise ValueError(f"Coordenadas de asamblea inválidas: {mensaje_error}")
        
        # Validar radio permitido usando función de validación (Requirement 4.6)
        radio = configuracion['radioPermitido']
        es_valido, mensaje_error, _ = validar_radio_positivo(radio)
        if not es_valido:
            raise ValueError(f"Radio permitido inválido: {mensaje_error}")
        
        return configuracion
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Error al parsear JSON: {str(e)}")
    except Exception as e:
        if isinstance(e, (FileNotFoundError, ValueError)):
            raise
        raise ValueError(f"Error al cargar configuración: {str(e)}")


def cargar_asistencias(ruta_archivo: str = 'data/asistencias.json') -> List[Dict]:
    """
    Carga las asistencias confirmadas desde archivo JSON.
    
    Args:
        ruta_archivo: Ruta al archivo JSON de asistencias
        
    Returns:
        Lista de diccionarios con las asistencias confirmadas
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el formato JSON es inválido
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            asistencias = json.load(archivo)
        
        # Validar que sea una lista
        if not isinstance(asistencias, list):
            raise ValueError("El archivo de asistencias debe contener una lista JSON")
        
        return asistencias
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Error al parsear JSON: {str(e)}")
    except Exception as e:
        if isinstance(e, (FileNotFoundError, ValueError)):
            raise
        raise ValueError(f"Error al cargar asistencias: {str(e)}")


def guardar_asistencias(
    asistencias: List[Dict], 
    ruta_archivo: str = 'data/asistencias.json'
) -> None:
    """
    Guarda las asistencias confirmadas en archivo JSON.
    
    Args:
        asistencias: Lista de diccionarios con las asistencias a guardar
        ruta_archivo: Ruta al archivo JSON de asistencias
        
    Raises:
        ValueError: Si hay error al guardar el archivo
    """
    try:
        # Crear directorio si no existe
        directorio = os.path.dirname(ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(asistencias, archivo, indent=2, ensure_ascii=False)
            
    except Exception as e:
        raise ValueError(f"Error al guardar asistencias: {str(e)}")


def guardar_usuarios_csv(
    usuarios: List[Dict[str, str]], 
    ruta_archivo: str = 'data/usuarios.csv'
) -> None:
    """
    Guarda la lista de usuarios en archivo CSV.
    
    Args:
        usuarios: Lista de diccionarios con los usuarios a guardar
        ruta_archivo: Ruta al archivo CSV de usuarios
        
    Raises:
        ValueError: Si hay error al guardar el archivo
    """
    try:
        # Crear directorio si no existe
        directorio = os.path.dirname(ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        with open(ruta_archivo, 'w', encoding='utf-8', newline='') as archivo:
            if usuarios:
                # Escribir encabezados
                fieldnames = ['userId', 'documento', 'nombre']
                writer = csv.DictWriter(archivo, fieldnames=fieldnames)
                writer.writeheader()
                
                # Escribir usuarios
                for usuario in usuarios:
                    writer.writerow({
                        'userId': usuario['userId'],
                        'documento': usuario['documento'],
                        'nombre': usuario['nombre']
                    })
            else:
                # Si no hay usuarios, escribir solo encabezados
                archivo.write('userId,documento,nombre\n')
            
    except Exception as e:
        raise ValueError(f"Error al guardar usuarios CSV: {str(e)}")



# ============================================================================
# FUNCIONES DE VALIDACIÓN (Sub-task 8.1)
# ============================================================================

def validar_coordenadas(latitud: any, longitud: any) -> Tuple[bool, Optional[str], Optional[Tuple[float, float]]]:
    """
    Valida que las coordenadas sean números válidos dentro de rangos correctos.
    
    Args:
        latitud: Valor de latitud a validar
        longitud: Valor de longitud a validar
        
    Returns:
        Tupla (es_valido, mensaje_error, (lat, lon))
        - es_valido: True si las coordenadas son válidas
        - mensaje_error: Mensaje de error si no son válidas, None si son válidas
        - (lat, lon): Tupla con coordenadas convertidas a float, None si no son válidas
        
    Requirement: 4.6
    """
    # Validar que no sean None
    if latitud is None or longitud is None:
        return False, "latitud y longitud son requeridas", None
    
    # Validar tipos de datos - intentar convertir a float
    try:
        lat = float(latitud)
        lon = float(longitud)
    except (ValueError, TypeError):
        return False, "Coordenadas deben ser números válidos", None
    
    # Validar rangos (latitud: -90 a 90, longitud: -180 a 180)
    if not (-90 <= lat <= 90):
        return False, "Latitud debe estar entre -90 y 90 grados", None
    
    if not (-180 <= lon <= 180):
        return False, "Longitud debe estar entre -180 y 180 grados", None
    
    return True, None, (lat, lon)


def validar_campo_requerido(valor: any, nombre_campo: str) -> Tuple[bool, Optional[str]]:
    """
    Valida que un campo requerido esté presente y no esté vacío.
    
    Args:
        valor: Valor del campo a validar
        nombre_campo: Nombre del campo para el mensaje de error
        
    Returns:
        Tupla (es_valido, mensaje_error)
        
    Requirement: 4.6
    """
    if valor is None:
        return False, f"{nombre_campo} es requerido"
    
    # Si es string, verificar que no esté vacío después de strip
    if isinstance(valor, str):
        if not valor.strip():
            return False, f"{nombre_campo} no puede estar vacío"
    
    return True, None


def validar_radio_positivo(radio: any) -> Tuple[bool, Optional[str], Optional[float]]:
    """
    Valida que el radio permitido sea un número positivo.
    
    Args:
        radio: Valor del radio a validar
        
    Returns:
        Tupla (es_valido, mensaje_error, radio_float)
        
    Requirement: 4.6
    """
    if radio is None:
        return False, "Radio permitido es requerido", None
    
    # Validar tipo de dato
    try:
        radio_float = float(radio)
    except (ValueError, TypeError):
        return False, "Radio permitido debe ser un número válido", None
    
    # Validar que sea positivo
    if radio_float <= 0:
        return False, "Radio permitido debe ser un número positivo", None
    
    return True, None, radio_float


# ============================================================================
# FILE WATCHER PARA USUARIOS.CSV (Sub-task 9.1)
# ============================================================================

class UsuariosCSVHandler(FileSystemEventHandler):
    """
    Handler para detectar cambios en el archivo usuarios.csv.
    
    Cuando el archivo cambia, recarga automáticamente la lista de usuarios.
    
    Requirements: 4.3, 4.6
    """
    
    def __init__(self, ruta_archivo: str):
        """
        Inicializa el handler con la ruta del archivo a observar.
        
        Args:
            ruta_archivo: Ruta completa al archivo usuarios.csv
        """
        super().__init__()
        self.ruta_archivo = os.path.abspath(ruta_archivo)
        self.last_modified = 0
    
    def on_modified(self, event):
        """
        Callback cuando el archivo es modificado.
        
        Args:
            event: Evento del sistema de archivos
        """
        # Verificar que sea el archivo que estamos observando
        if event.is_directory:
            return
        
        event_path = os.path.abspath(event.src_path)
        if event_path != self.ruta_archivo:
            return
        
        # Evitar múltiples recargas por el mismo cambio
        # (algunos editores generan múltiples eventos)
        import time
        current_time = time.time()
        if current_time - self.last_modified < 1:  # Ignorar si fue hace menos de 1 segundo
            return
        
        self.last_modified = current_time
        
        # Recargar usuarios
        print(f"\n📝 Detectado cambio en {os.path.basename(self.ruta_archivo)}")
        recargar_usuarios()


def recargar_usuarios():
    """
    Recarga la lista de usuarios desde el archivo CSV.
    
    Valida el formato al recargar y actualiza el caché global.
    
    Requirements: 4.3, 4.6
    """
    global usuarios_cache
    
    try:
        # Cargar usuarios desde CSV con validación
        nuevos_usuarios = cargar_usuarios_csv()
        
        # Actualizar caché
        usuarios_cache = nuevos_usuarios
        
        print(f"✓ Usuarios recargados exitosamente: {len(usuarios_cache)} usuarios")
        
    except FileNotFoundError as e:
        print(f"⚠ Error: Archivo usuarios.csv no encontrado - {e}")
    except ValueError as e:
        print(f"⚠ Error de formato en CSV: {e}")
    except Exception as e:
        print(f"⚠ Error al recargar usuarios: {e}")


def iniciar_file_watcher():
    """
    Inicia el observador de archivos para usuarios.csv.
    
    El observador corre en un thread separado y detecta cambios automáticamente.
    
    Requirements: 4.3, 4.6
    """
    ruta_csv = 'data/usuarios.csv'
    
    # Verificar que el archivo existe
    if not os.path.exists(ruta_csv):
        print(f"⚠ Advertencia: {ruta_csv} no existe, file watcher no iniciado")
        return None
    
    try:
        # Crear handler y observer
        event_handler = UsuariosCSVHandler(ruta_csv)
        observer = Observer()
        
        # Observar el directorio que contiene el archivo
        directorio = os.path.dirname(os.path.abspath(ruta_csv))
        observer.schedule(event_handler, directorio, recursive=False)
        
        # Iniciar observer en thread separado
        observer.start()
        
        print(f"✓ File watcher iniciado para {ruta_csv}")
        
        return observer
    except Exception as e:
        # Si hay error con watchdog (ej: Python 3.13 threading issues),
        # usar polling como fallback
        print(f"⚠ File watcher no disponible: {e}")
        print("ℹ Usar endpoint POST /api/reload-usuarios para recarga manual")
        print("ℹ O editar usuarios desde la interfaz administrativa")
        return None


# ============================================================================
# FLASK APPLICATION SETUP (Sub-task 4.1)
# ============================================================================

# Crear aplicación Flask
app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Configurar CORS para permitir peticiones desde el frontend
CORS(app)

# Variables globales para caché de datos
usuarios_cache = []
configuracion_cache = {}
asistencias_cache = []
file_observer = None  # Observer para file watcher
admin_tokens = {}  # Tokens de sesión administrativa: {token: expiration_time}


def inicializar_datos():
    """
    Carga inicial de datos al arrancar el servidor.
    """
    global usuarios_cache, configuracion_cache, asistencias_cache, file_observer
    
    try:
        usuarios_cache = cargar_usuarios_csv()
        print(f"✓ Cargados {len(usuarios_cache)} usuarios desde CSV")
    except Exception as e:
        print(f"⚠ Error al cargar usuarios: {e}")
        usuarios_cache = []
    
    try:
        configuracion_cache = cargar_configuracion()
        print(f"✓ Configuración cargada: Radio {configuracion_cache['radioPermitido']}m")
    except Exception as e:
        print(f"⚠ Error al cargar configuración: {e}")
        configuracion_cache = {}
    
    try:
        asistencias_cache = cargar_asistencias()
        print(f"✓ Cargadas {len(asistencias_cache)} asistencias")
    except Exception as e:
        print(f"⚠ Error al cargar asistencias: {e}")
        asistencias_cache = []
    
    # Iniciar file watcher para usuarios.csv (Sub-task 9.1)
    try:
        file_observer = iniciar_file_watcher()
    except Exception as e:
        print(f"⚠ Error al iniciar file watcher: {e}")
        file_observer = None


@app.route('/')
def index():
    """
    Servir página principal del frontend.
    """
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def static_files(path):
    """
    Servir archivos estáticos del frontend.
    """
    return send_from_directory(app.static_folder, path)


# ============================================================================
# FUNCIONES DE AUTENTICACIÓN ADMINISTRATIVA
# ============================================================================

def cargar_credenciales_admin(ruta_archivo: str = 'data/admin_credentials.json') -> Dict:
    """
    Carga las credenciales del administrador desde archivo JSON.
    
    Args:
        ruta_archivo: Ruta al archivo JSON de credenciales
        
    Returns:
        Diccionario con username y password
    """
    if not os.path.exists(ruta_archivo):
        # Credenciales por defecto si no existe el archivo
        return {
            'username': 'admin',
            'password': 'admin123'
        }
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except Exception as e:
        print(f"⚠ Error al cargar credenciales admin: {e}")
        return {
            'username': 'admin',
            'password': 'admin123'
        }


def generar_token() -> str:
    """Genera un token aleatorio seguro."""
    return secrets.token_urlsafe(32)


def validar_token(token: str) -> bool:
    """
    Valida si un token es válido y no ha expirado.
    
    Args:
        token: Token a validar
        
    Returns:
        True si el token es válido, False en caso contrario
    """
    if token not in admin_tokens:
        return False
    
    # Verificar si el token ha expirado
    if datetime.now() > admin_tokens[token]:
        # Token expirado, eliminarlo
        del admin_tokens[token]
        return False
    
    return True


def limpiar_tokens_expirados():
    """Elimina tokens expirados del diccionario."""
    tokens_a_eliminar = []
    ahora = datetime.now()
    
    for token, expiracion in admin_tokens.items():
        if ahora > expiracion:
            tokens_a_eliminar.append(token)
    
    for token in tokens_a_eliminar:
        del admin_tokens[token]


def requiere_autenticacion(f):
    """
    Decorador para proteger endpoints que requieren autenticación administrativa.
    """
    @wraps(f)
    def decorador(*args, **kwargs):
        # Obtener token del header Authorization
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'success': False,
                'mensaje': 'No autorizado. Token requerido.'
            }), 401
        
        # Extraer token (formato: "Bearer TOKEN")
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({
                'success': False,
                'mensaje': 'Formato de token inválido'
            }), 401
        
        # Validar token
        if not validar_token(token):
            return jsonify({
                'success': False,
                'mensaje': 'Token inválido o expirado'
            }), 401
        
        # Token válido, ejecutar función
        return f(*args, **kwargs)
    
    return decorador


# ============================================================================
# ENDPOINTS DE AUTENTICACIÓN ADMINISTRATIVA
# ============================================================================

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """
    Endpoint POST /api/admin/login
    
    Autentica al administrador y genera un token de sesión.
    
    Request Body:
        {
            "username": "string",
            "password": "string"
        }
    
    Response:
        {
            "success": boolean,
            "mensaje": "string",
            "token": "string" (solo si success=true)
        }
    """
    try:
        # Limpiar tokens expirados
        limpiar_tokens_expirados()
        
        # Obtener datos del request
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'success': False,
                'mensaje': 'No se recibieron datos'
            }), 400
        
        username = datos.get('username', '').strip()
        password = datos.get('password', '')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'mensaje': 'Usuario y contraseña son requeridos'
            }), 400
        
        # Cargar credenciales
        credenciales = cargar_credenciales_admin()
        
        # Validar credenciales
        if username == credenciales['username'] and password == credenciales['password']:
            # Generar token
            token = generar_token()
            
            # Token válido por 8 horas
            expiracion = datetime.now() + timedelta(hours=8)
            admin_tokens[token] = expiracion
            
            return jsonify({
                'success': True,
                'mensaje': 'Autenticación exitosa',
                'token': token
            }), 200
        else:
            return jsonify({
                'success': False,
                'mensaje': 'Usuario o contraseña incorrectos'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error del servidor: {str(e)}'
        }), 500


@app.route('/api/admin/logout', methods=['POST'])
@requiere_autenticacion
def admin_logout():
    """
    Endpoint POST /api/admin/logout
    
    Cierra la sesión del administrador eliminando el token.
    
    Response:
        {
            "success": boolean,
            "mensaje": "string"
        }
    """
    try:
        # Obtener token del header
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        
        # Eliminar token
        if token in admin_tokens:
            del admin_tokens[token]
        
        return jsonify({
            'success': True,
            'mensaje': 'Sesión cerrada exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error del servidor: {str(e)}'
        }), 500


@app.route('/api/admin/verificar', methods=['GET'])
@requiere_autenticacion
def verificar_sesion():
    """
    Endpoint GET /api/admin/verificar
    
    Verifica si la sesión del administrador es válida.
    
    Response:
        {
            "success": boolean,
            "mensaje": "string"
        }
    """
    return jsonify({
        'success': True,
        'mensaje': 'Sesión válida'
    }), 200


@app.route('/api/admin/cambiar-password', methods=['POST'])
@requiere_autenticacion
def cambiar_password():
    """
    Endpoint POST /api/admin/cambiar-password
    
    Cambia la contraseña del administrador.
    Requiere autenticación.
    
    Request Body:
        {
            "passwordActual": "string",
            "passwordNueva": "string"
        }
    
    Response:
        {
            "success": boolean,
            "mensaje": "string"
        }
    """
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'success': False,
                'mensaje': 'No se recibieron datos'
            }), 400
        
        password_actual = datos.get('passwordActual', '')
        password_nueva = datos.get('passwordNueva', '')
        
        if not password_actual or not password_nueva:
            return jsonify({
                'success': False,
                'mensaje': 'Se requieren ambas contraseñas'
            }), 400
        
        # Validar longitud mínima
        if len(password_nueva) < 6:
            return jsonify({
                'success': False,
                'mensaje': 'La nueva contraseña debe tener al menos 6 caracteres'
            }), 400
        
        # Cargar credenciales actuales
        credenciales = cargar_credenciales_admin()
        
        # Verificar contraseña actual
        if password_actual != credenciales['password']:
            return jsonify({
                'success': False,
                'mensaje': 'La contraseña actual es incorrecta'
            }), 401
        
        # Actualizar contraseña
        credenciales['password'] = password_nueva
        
        # Guardar en archivo
        with open('data/admin_credentials.json', 'w', encoding='utf-8') as archivo:
            json.dump(credenciales, archivo, indent=2, ensure_ascii=False)
        
        # Invalidar todos los tokens existentes (forzar re-login)
        admin_tokens.clear()
        
        return jsonify({
            'success': True,
            'mensaje': 'Contraseña actualizada exitosamente. Por favor, inicia sesión nuevamente.'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error del servidor: {str(e)}'
        }), 500


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/validar-identidad', methods=['POST'])
def validar_identidad():
    """
    Endpoint POST /api/validar-identidad
    
    Valida las credenciales de un usuario contra la base de datos usando solo el documento.
    
    Request Body:
        {
            "documento": "string"
        }
    
    Response:
        {
            "valido": boolean,
            "nombre": "string" (solo si válido),
            "userId": "string" (solo si válido)
        }
    
    Requirements: 1.1, 1.2, 1.3, 1.4, 4.6
    """
    try:
        # Obtener datos del request
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'valido': False,
                'error': 'No se recibieron datos'
            }), 400
        
        # Validar que documento esté presente (Requirements 1.4, 4.6)
        documento = datos.get('documento')
        es_valido, mensaje_error = validar_campo_requerido(documento, 'documento')
        
        if not es_valido:
            return jsonify({
                'valido': False,
                'error': mensaje_error
            }), 400
        
        documento = documento.strip()
        
        # Buscar usuario en lista cargada desde CSV (Requirement 1.1)
        usuario_encontrado = None
        for usuario in usuarios_cache:
            if usuario['documento'] == documento:
                usuario_encontrado = usuario
                break
        
        # Retornar resultado (Requirements 1.2, 1.3)
        if usuario_encontrado:
            return jsonify({
                'valido': True,
                'nombre': usuario_encontrado['nombre'],
                'userId': usuario_encontrado['userId']
            }), 200
        else:
            return jsonify({
                'valido': False
            }), 200
            
    except Exception as e:
        return jsonify({
            'valido': False,
            'error': f'Error del servidor: {str(e)}'
        }), 500


@app.route('/api/confirmar-asistencia', methods=['POST'])
def confirmar_asistencia():
    """
    Endpoint POST /api/confirmar-asistencia
    
    Confirma la asistencia de un usuario validando su ubicación.
    
    Request Body:
        {
            "userId": "string",
            "latitud": number,
            "longitud": number
        }
    
    Response:
        {
            "confirmado": boolean,
            "mensaje": "string",
            "distancia": number
        }
    
    Requirements: 2.2, 2.3, 2.4, 3.1, 3.3, 3.4, 4.6
    """
    try:
        # Obtener datos del request
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'confirmado': False,
                'mensaje': 'No se recibieron datos',
                'distancia': None
            }), 400
        
        # Validar campo userId requerido (Requirement 4.6)
        user_id = datos.get('userId')
        es_valido, mensaje_error = validar_campo_requerido(user_id, 'userId')
        if not es_valido:
            return jsonify({
                'confirmado': False,
                'mensaje': mensaje_error,
                'distancia': None
            }), 400
        
        user_id = user_id.strip()
        
        # Validar coordenadas (Requirement 4.6)
        latitud = datos.get('latitud')
        longitud = datos.get('longitud')
        
        es_valido, mensaje_error, coordenadas = validar_coordenadas(latitud, longitud)
        if not es_valido:
            return jsonify({
                'confirmado': False,
                'mensaje': mensaje_error,
                'distancia': None
            }), 400
        
        latitud, longitud = coordenadas
        
        # Verificar que no exista registro duplicado (Requirement 3.3)
        for asistencia in asistencias_cache:
            if asistencia['userId'] == user_id:
                return jsonify({
                    'confirmado': False,
                    'mensaje': 'Ya has confirmado tu asistencia anteriormente',
                    'distancia': None
                }), 200
        
        # Obtener configuración de la asamblea
        if not configuracion_cache:
            return jsonify({
                'confirmado': False,
                'mensaje': 'Error: Configuración de asamblea no disponible',
                'distancia': None
            }), 500
        
        ubicacion_asamblea = configuracion_cache['ubicacionAsamblea']
        radio_permitido = configuracion_cache['radioPermitido']
        
        # Calcular distancia a ubicación de asamblea (Requirement 2.2)
        distancia = calcular_distancia_haversine(
            latitud,
            longitud,
            ubicacion_asamblea['latitud'],
            ubicacion_asamblea['longitud']
        )
        
        # Verificar si está dentro del radio permitido (Requirements 2.3, 2.4)
        if distancia <= radio_permitido:
            # Buscar nombre del usuario
            nombre_usuario = None
            for usuario in usuarios_cache:
                if usuario['userId'] == user_id:
                    nombre_usuario = usuario['nombre']
                    break
            
            if not nombre_usuario:
                nombre_usuario = user_id  # Fallback si no se encuentra el nombre
            
            # Guardar asistencia (Requirements 3.1, 3.4)
            nueva_asistencia = {
                'userId': user_id,
                'nombre': nombre_usuario,
                'fechaHora': datetime.utcnow().isoformat() + 'Z',
                'ubicacion': {
                    'latitud': latitud,
                    'longitud': longitud
                }
            }
            
            asistencias_cache.append(nueva_asistencia)
            guardar_asistencias(asistencias_cache)
            
            return jsonify({
                'confirmado': True,
                'mensaje': 'Asistencia confirmada exitosamente',
                'distancia': round(distancia, 2)
            }), 200
        else:
            # Fuera de rango (Requirement 2.4)
            return jsonify({
                'confirmado': False,
                'mensaje': f'No te encuentras en la ubicación de la asamblea. Por favor dirígete al lugar del evento. Distancia actual: {round(distancia, 2)} metros.',
                'distancia': round(distancia, 2)
            }), 200
            
    except Exception as e:
        return jsonify({
            'confirmado': False,
            'mensaje': f'Error del servidor: {str(e)}',
            'distancia': None
        }), 500


@app.route('/api/configuracion', methods=['GET'])
def obtener_configuracion():
    """
    Endpoint GET /api/configuracion
    
    Retorna la configuración actual de la asamblea.
    
    Response:
        {
            "ubicacionAsamblea": {
                "latitud": number,
                "longitud": number
            },
            "radioPermitido": number
        }
    
    Requirements: 4.1, 4.2
    """
    try:
        if not configuracion_cache:
            return jsonify({
                'error': 'Configuración no disponible'
            }), 500
        
        return jsonify(configuracion_cache), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error del servidor: {str(e)}'
        }), 500


@app.route('/api/admin/configuracion', methods=['PUT'])
@requiere_autenticacion
def actualizar_configuracion():
    """
    Endpoint PUT /api/admin/configuracion
    
    Actualiza la configuración de ubicación de la asamblea.
    Requiere autenticación de administrador.
    
    Request Body:
        {
            "latitud": number,
            "longitud": number,
            "radioPermitido": number (opcional)
        }
    
    Response:
        {
            "mensaje": "Configuración actualizada exitosamente",
            "configuracion": {...}
        }
    """
    global configuracion_cache
    
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        # Validar campos requeridos
        if 'latitud' not in datos or 'longitud' not in datos:
            return jsonify({'error': 'Se requieren latitud y longitud'}), 400
        
        latitud = datos['latitud']
        longitud = datos['longitud']
        radio_permitido = datos.get('radioPermitido', configuracion_cache.get('radioPermitido', 100))
        
        # Validar coordenadas
        es_valido, mensaje_error, _ = validar_coordenadas(latitud, longitud)
        if not es_valido:
            return jsonify({'error': mensaje_error}), 400
        
        # Validar radio
        es_valido, mensaje_error, _ = validar_radio_positivo(radio_permitido)
        if not es_valido:
            return jsonify({'error': mensaje_error}), 400
        
        # Actualizar configuración
        nueva_configuracion = {
            'ubicacionAsamblea': {
                'latitud': latitud,
                'longitud': longitud
            },
            'radioPermitido': radio_permitido
        }
        
        # Guardar en archivo
        with open('data/configuracion.json', 'w', encoding='utf-8') as archivo:
            json.dump(nueva_configuracion, archivo, indent=2, ensure_ascii=False)
        
        # Actualizar caché
        configuracion_cache = nueva_configuracion
        
        return jsonify({
            'mensaje': 'Configuración actualizada exitosamente',
            'configuracion': nueva_configuracion
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error al actualizar configuración: {str(e)}'
        }), 500


@app.route('/api/asistencias', methods=['GET'])
def obtener_asistencias():
    """
    Endpoint GET /api/asistencias
    
    Retorna la lista de asistencias confirmadas.
    
    Response:
        [
            {
                "userId": "string",
                "nombre": "string",
                "fechaHora": "ISO8601 string",
                "ubicacion": {
                    "latitud": number,
                    "longitud": number
                }
            }
        ]
    
    Requirements: 4.7
    """
    try:
        return jsonify(asistencias_cache), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error del servidor: {str(e)}'
        }), 500


@app.route('/api/asistencias/reiniciar', methods=['POST'])
@requiere_autenticacion
def reiniciar_asistencias():
    """
    Endpoint POST /api/asistencias/reiniciar
    
    Elimina todas las asistencias confirmadas.
    Útil para reutilizar el sistema en múltiples eventos.
    
    Response:
        {
            "success": boolean,
            "mensaje": "string",
            "asistencias_eliminadas": number
        }
    
    Requirements: 4.7
    """
    try:
        global asistencias_cache
        
        # Contar asistencias antes de eliminar
        total_eliminadas = len(asistencias_cache)
        
        # Limpiar caché
        asistencias_cache = []
        
        # Guardar archivo vacío
        try:
            guardar_asistencias(asistencias_cache)
        except Exception as e:
            return jsonify({
                'success': False,
                'mensaje': f'Error al guardar cambios: {str(e)}',
                'asistencias_eliminadas': 0
            }), 500
        
        return jsonify({
            'success': True,
            'mensaje': f'Se eliminaron {total_eliminadas} asistencia(s) exitosamente',
            'asistencias_eliminadas': total_eliminadas
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error del servidor: {str(e)}',
            'asistencias_eliminadas': 0
        }), 500


@app.route('/api/usuarios', methods=['GET'])
@requiere_autenticacion
def obtener_usuarios():
    """
    Endpoint GET /api/usuarios
    
    Retorna la lista de usuarios autorizados.
    
    Response:
        [
            {
                "userId": "string",
                "documento": "string",
                "nombre": "string"
            }
        ]
    
    Requirements: 4.3
    """
    try:
        return jsonify(usuarios_cache), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error del servidor: {str(e)}'
        }), 500


@app.route('/api/usuarios', methods=['POST'])
@requiere_autenticacion
def agregar_usuario():
    """
    Endpoint POST /api/usuarios
    
    Agrega un nuevo usuario a la lista de autorizados.
    
    Request Body:
        {
            "userId": "string",
            "documento": "string",
            "nombre": "string"
        }
    
    Response:
        {
            "success": boolean,
            "mensaje": "string"
        }
    
    Requirements: 4.3, 4.4, 4.6
    """
    try:
        # Obtener datos del request
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'success': False,
                'mensaje': 'No se recibieron datos'
            }), 400
        
        # Validar campos requeridos (Requirement 4.6)
        user_id = datos.get('userId')
        es_valido, mensaje_error = validar_campo_requerido(user_id, 'userId')
        if not es_valido:
            return jsonify({
                'success': False,
                'mensaje': mensaje_error
            }), 400
        
        documento = datos.get('documento')
        es_valido, mensaje_error = validar_campo_requerido(documento, 'documento')
        if not es_valido:
            return jsonify({
                'success': False,
                'mensaje': mensaje_error
            }), 400
        
        nombre = datos.get('nombre')
        es_valido, mensaje_error = validar_campo_requerido(nombre, 'nombre')
        if not es_valido:
            return jsonify({
                'success': False,
                'mensaje': mensaje_error
            }), 400
        
        user_id = user_id.strip()
        documento = documento.strip()
        nombre = nombre.strip()
        
        # Verificar que no exista un usuario con el mismo userId
        for usuario in usuarios_cache:
            if usuario['userId'] == user_id:
                return jsonify({
                    'success': False,
                    'mensaje': f'Ya existe un usuario con userId: {user_id}'
                }), 400
        
        # Agregar nuevo usuario
        nuevo_usuario = {
            'userId': user_id,
            'documento': documento,
            'nombre': nombre
        }
        
        usuarios_cache.append(nuevo_usuario)
        
        # Guardar en archivo CSV
        guardar_usuarios_csv(usuarios_cache)
        
        return jsonify({
            'success': True,
            'mensaje': 'Usuario agregado exitosamente'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error del servidor: {str(e)}'
        }), 500


@app.route('/api/usuarios/importar-csv', methods=['POST'])
@requiere_autenticacion
def importar_usuarios_csv():
    """
    Endpoint POST /api/usuarios/importar-csv
    
    Importa múltiples usuarios desde contenido CSV.
    
    Request Body:
        {
            "csv_content": "string" (contenido del CSV)
        }
    
    Response:
        {
            "success": boolean,
            "mensaje": "string",
            "agregados": number,
            "omitidos": number,
            "errores": number,
            "detalles": [
                {
                    "linea": number,
                    "userId": "string",
                    "estado": "agregado|omitido|error",
                    "razon": "string"
                }
            ]
        }
    
    Requirements: 4.3, 4.4, 4.6
    """
    try:
        # Obtener datos del request
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'success': False,
                'mensaje': 'No se recibieron datos'
            }), 400
        
        csv_content = datos.get('csv_content', '').strip()
        
        if not csv_content:
            return jsonify({
                'success': False,
                'mensaje': 'El contenido CSV está vacío'
            }), 400
        
        # Parsear CSV
        try:
            usuarios_importar = parsear_csv(csv_content)
        except ValueError as e:
            return jsonify({
                'success': False,
                'mensaje': f'Error al parsear CSV: {str(e)}'
            }), 400
        
        if not usuarios_importar:
            return jsonify({
                'success': False,
                'mensaje': 'No se encontraron usuarios válidos en el CSV'
            }), 400
        
        # Procesar usuarios
        agregados = 0
        omitidos = 0
        errores = 0
        detalles = []
        
        for idx, usuario in enumerate(usuarios_importar, start=2):  # start=2 porque línea 1 es header
            user_id = usuario.get('userId', '').strip()
            documento = usuario.get('documento', '').strip()
            nombre = usuario.get('nombre', '').strip()
            
            # Validar campos
            if not user_id or not documento or not nombre:
                errores += 1
                detalles.append({
                    'linea': idx,
                    'userId': user_id or 'N/A',
                    'estado': 'error',
                    'razon': 'Campos incompletos'
                })
                continue
            
            # Verificar si ya existe
            existe = False
            for u in usuarios_cache:
                if u['userId'] == user_id:
                    existe = True
                    break
            
            if existe:
                omitidos += 1
                detalles.append({
                    'linea': idx,
                    'userId': user_id,
                    'estado': 'omitido',
                    'razon': 'Usuario ya existe'
                })
                continue
            
            # Agregar usuario
            try:
                usuarios_cache.append({
                    'userId': user_id,
                    'documento': documento,
                    'nombre': nombre
                })
                agregados += 1
                detalles.append({
                    'linea': idx,
                    'userId': user_id,
                    'estado': 'agregado',
                    'razon': 'Usuario agregado exitosamente'
                })
            except Exception as e:
                errores += 1
                detalles.append({
                    'linea': idx,
                    'userId': user_id,
                    'estado': 'error',
                    'razon': str(e)
                })
        
        # Guardar en archivo CSV si se agregó al menos uno
        if agregados > 0:
            try:
                guardar_usuarios_csv(usuarios_cache)
            except Exception as e:
                return jsonify({
                    'success': False,
                    'mensaje': f'Error al guardar usuarios: {str(e)}',
                    'agregados': agregados,
                    'omitidos': omitidos,
                    'errores': errores,
                    'detalles': detalles
                }), 500
        
        # Preparar mensaje de respuesta
        mensaje_partes = []
        if agregados > 0:
            mensaje_partes.append(f'{agregados} usuario(s) agregado(s)')
        if omitidos > 0:
            mensaje_partes.append(f'{omitidos} omitido(s)')
        if errores > 0:
            mensaje_partes.append(f'{errores} error(es)')
        
        mensaje = ', '.join(mensaje_partes)
        
        return jsonify({
            'success': True,
            'mensaje': f'Importación completada: {mensaje}',
            'agregados': agregados,
            'omitidos': omitidos,
            'errores': errores,
            'detalles': detalles
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error del servidor: {str(e)}'
        }), 500


@app.route('/api/usuarios/<user_id>', methods=['PUT'])
@requiere_autenticacion
def actualizar_usuario(user_id):
    """
    Endpoint PUT /api/usuarios/:userId
    
    Actualiza la información de un usuario existente.
    
    Request Body:
        {
            "documento": "string",
            "nombre": "string"
        }
    
    Response:
        {
            "success": boolean,
            "mensaje": "string"
        }
    
    Requirements: 4.4, 4.5, 4.6
    """
    try:
        # Obtener datos del request
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'success': False,
                'mensaje': 'No se recibieron datos'
            }), 400
        
        # Validar campos requeridos (Requirement 4.6)
        documento = datos.get('documento')
        es_valido, mensaje_error = validar_campo_requerido(documento, 'documento')
        if not es_valido:
            return jsonify({
                'success': False,
                'mensaje': mensaje_error
            }), 400
        
        nombre = datos.get('nombre')
        es_valido, mensaje_error = validar_campo_requerido(nombre, 'nombre')
        if not es_valido:
            return jsonify({
                'success': False,
                'mensaje': mensaje_error
            }), 400
        
        documento = documento.strip()
        nombre = nombre.strip()
        
        # Buscar usuario
        usuario_encontrado = False
        for i, usuario in enumerate(usuarios_cache):
            if usuario['userId'] == user_id:
                usuarios_cache[i]['documento'] = documento
                usuarios_cache[i]['nombre'] = nombre
                usuario_encontrado = True
                break
        
        if not usuario_encontrado:
            return jsonify({
                'success': False,
                'mensaje': f'Usuario con userId {user_id} no encontrado'
            }), 404
        
        # Guardar en archivo CSV
        guardar_usuarios_csv(usuarios_cache)
        
        return jsonify({
            'success': True,
            'mensaje': 'Usuario actualizado exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error del servidor: {str(e)}'
        }), 500


@app.route('/api/usuarios/<user_id>', methods=['DELETE'])
@requiere_autenticacion
def eliminar_usuario(user_id):
    """
    Endpoint DELETE /api/usuarios/:userId
    
    Elimina un usuario de la lista de autorizados.
    
    Response:
        {
            "success": boolean,
            "mensaje": "string"
        }
    
    Requirements: 4.5
    """
    try:
        # Buscar y eliminar usuario
        usuario_encontrado = False
        for i, usuario in enumerate(usuarios_cache):
            if usuario['userId'] == user_id:
                usuarios_cache.pop(i)
                usuario_encontrado = True
                break
        
        if not usuario_encontrado:
            return jsonify({
                'success': False,
                'mensaje': f'Usuario con userId {user_id} no encontrado'
            }), 404
        
        # Guardar en archivo CSV
        guardar_usuarios_csv(usuarios_cache)
        
        return jsonify({
            'success': True,
            'mensaje': 'Usuario eliminado exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error del servidor: {str(e)}'
        }), 500


@app.route('/api/reload-usuarios', methods=['POST'])
@requiere_autenticacion
def endpoint_reload_usuarios():
    """
    Endpoint POST /api/reload-usuarios
    
    Fuerza la recarga manual de usuarios desde el archivo CSV.
    Útil si el file watcher no funciona o para forzar actualización.
    
    Response:
        {
            "success": boolean,
            "mensaje": "string",
            "totalUsuarios": number
        }
    
    Requirements: 4.3
    Sub-task: 9.2
    """
    try:
        # Recargar usuarios usando la función existente
        recargar_usuarios()
        
        return jsonify({
            'success': True,
            'mensaje': 'Usuarios recargados exitosamente',
            'totalUsuarios': len(usuarios_cache)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error al recargar usuarios: {str(e)}',
            'totalUsuarios': len(usuarios_cache)
        }), 500


@app.route('/api/asistencias/exportar-csv', methods=['GET'])
@requiere_autenticacion
def exportar_asistencias_csv():
    """
    Endpoint GET /api/asistencias/exportar-csv
    
    Genera y descarga un archivo CSV con todas las asistencias confirmadas.
    
    Response:
        Archivo CSV con las columnas:
        - userId: ID del usuario
        - nombre: Nombre completo
        - documento: Número de documento
        - fechaHora: Fecha y hora de confirmación
        - latitud: Latitud donde confirmó
        - longitud: Longitud donde confirmó
        - distancia: Distancia al punto de asamblea (en metros)
    
    Requirements: 4.7
    """
    try:
        from io import StringIO
        from flask import make_response
        
        # Crear StringIO para generar CSV
        output = StringIO()
        writer = csv.writer(output)
        
        # Escribir encabezados
        writer.writerow([
            'userId',
            'nombre',
            'documento',
            'fechaHora',
            'latitud',
            'longitud',
            'distancia_metros'
        ])
        
        # Obtener ubicación de asamblea para calcular distancias
        ubicacion_asamblea = configuracion_cache.get('ubicacionAsamblea', {})
        lat_asamblea = ubicacion_asamblea.get('latitud', 0)
        lon_asamblea = ubicacion_asamblea.get('longitud', 0)
        
        # Escribir datos de asistencias
        for asistencia in asistencias_cache:
            # Buscar documento del usuario
            documento = ''
            for usuario in usuarios_cache:
                if usuario['userId'] == asistencia['userId']:
                    documento = usuario['documento']
                    break
            
            # Calcular distancia
            lat_usuario = asistencia['ubicacion']['latitud']
            lon_usuario = asistencia['ubicacion']['longitud']
            
            try:
                distancia = calcular_distancia_haversine(
                    lat_usuario,
                    lon_usuario,
                    lat_asamblea,
                    lon_asamblea
                )
                distancia_str = f"{distancia:.2f}"
            except:
                distancia_str = "N/A"
            
            # Escribir fila
            writer.writerow([
                asistencia['userId'],
                asistencia['nombre'],
                documento,
                asistencia['fechaHora'],
                asistencia['ubicacion']['latitud'],
                asistencia['ubicacion']['longitud'],
                distancia_str
            ])
        
        # Obtener contenido CSV
        csv_content = output.getvalue()
        output.close()
        
        # Crear respuesta con el CSV
        response = make_response(csv_content)
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename=asistencias_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        return response
        
    except Exception as e:
        return jsonify({
            'error': f'Error al generar CSV: {str(e)}'
        }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Sistema de Confirmación de Asistencia a Asambleas")
    print("="*60 + "\n")
    
    # Inicializar datos
    inicializar_datos()
    
    print("\n" + "="*60)
    
    # Determinar si usar SSL
    ssl_enabled = os.environ.get('SSL_ENABLED', 'false').lower() == 'true'
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    if ssl_enabled:
        ssl_cert = os.environ.get('SSL_CERT_PATH', 'certs/cert.pem')
        ssl_key = os.environ.get('SSL_KEY_PATH', 'certs/key.pem')
        
        # Verificar que existan los certificados
        if os.path.exists(ssl_cert) and os.path.exists(ssl_key):
            print(f"🔒 Servidor HTTPS iniciado en https://{host}:{port}")
            print("="*60 + "\n")
            
            # Iniciar con SSL
            app.run(
                debug=False,
                host=host,
                port=port,
                ssl_context=(ssl_cert, ssl_key),
                use_reloader=False
            )
        else:
            print(f"⚠️  Certificados SSL no encontrados en:")
            print(f"   - {ssl_cert}")
            print(f"   - {ssl_key}")
            print(f"\n💡 Genera certificados con: python generar_certificados.py")
            print(f"\n🔓 Iniciando en modo HTTP en http://{host}:{port}")
            print("="*60 + "\n")
            
            app.run(
                debug=True,
                host=host,
                port=port,
                use_reloader=False
            )
    else:
        print(f"Servidor iniciado en http://{host}:{port}")
        print("="*60 + "\n")
        
        # Iniciar servidor
        # Nota: use_reloader=False para evitar conflictos con nuestro file watcher
        # El file watcher personalizado maneja la recarga de usuarios.csv
        app.run(debug=True, host=host, port=port, use_reloader=False)
