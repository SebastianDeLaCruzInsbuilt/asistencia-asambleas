"""
Configuración del Servidor
Sistema de Confirmación de Asistencia a Asambleas
"""

import os

class Config:
    """Configuración base"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Servidor
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # SSL/HTTPS
    SSL_ENABLED = os.environ.get('SSL_ENABLED', 'false').lower() == 'true'
    SSL_CERT_PATH = os.environ.get('SSL_CERT_PATH', 'certs/cert.pem')
    SSL_KEY_PATH = os.environ.get('SSL_KEY_PATH', 'certs/key.pem')
    
    # Archivos de datos
    DATA_DIR = os.environ.get('DATA_DIR', 'data')
    USUARIOS_CSV = os.path.join(DATA_DIR, 'usuarios.csv')
    CONFIGURACION_JSON = os.path.join(DATA_DIR, 'configuracion.json')
    ASISTENCIAS_JSON = os.path.join(DATA_DIR, 'asistencias.json')


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    # En producción, usar variables de entorno para configuración sensible
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY debe estar definida en producción")


# Mapeo de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """
    Obtiene la configuración según el entorno
    
    Args:
        env: Nombre del entorno ('development', 'production')
        
    Returns:
        Clase de configuración correspondiente
    """
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    
    return config.get(env, config['default'])
