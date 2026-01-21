#!/usr/bin/env python3
"""
Script para generar certificados SSL autofirmados
Sistema de Confirmación de Asistencia a Asambleas

NOTA: Los certificados autofirmados son útiles para desarrollo y pruebas.
Para producción, se recomienda usar certificados de una autoridad certificadora
como Let's Encrypt (gratuito) o comprar certificados comerciales.
"""

import os
import sys
from datetime import datetime, timedelta

try:
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
except ImportError:
    print("ERROR: Se requiere la librería 'cryptography'")
    print("Instalar con: pip install cryptography")
    sys.exit(1)


def generar_certificados(
    cert_path='certs/cert.pem',
    key_path='certs/key.pem',
    dias_validez=365,
    nombre_comun='localhost'
):
    """
    Genera certificados SSL autofirmados
    
    Args:
        cert_path: Ruta donde guardar el certificado
        key_path: Ruta donde guardar la clave privada
        dias_validez: Días de validez del certificado
        nombre_comun: Nombre común (CN) del certificado
    """
    print("="*60)
    print("Generador de Certificados SSL Autofirmados")
    print("="*60)
    print()
    
    # Crear directorio si no existe
    cert_dir = os.path.dirname(cert_path)
    if cert_dir and not os.path.exists(cert_dir):
        os.makedirs(cert_dir)
        print(f"✓ Directorio creado: {cert_dir}")
    
    # Generar clave privada
    print("Generando clave privada RSA (2048 bits)...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    print("✓ Clave privada generada")
    
    # Crear certificado
    print(f"Generando certificado para: {nombre_comun}")
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "PE"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Lima"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Lima"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Asamblea"),
        x509.NameAttribute(NameOID.COMMON_NAME, nombre_comun),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=dias_validez)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(nombre_comun),
            x509.DNSName("localhost"),
            x509.DNSName("127.0.0.1"),
            x509.IPAddress(b'\x7f\x00\x00\x01'),  # 127.0.0.1
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256(), default_backend())
    
    print("✓ Certificado generado")
    
    # Guardar clave privada
    print(f"Guardando clave privada en: {key_path}")
    with open(key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    print("✓ Clave privada guardada")
    
    # Guardar certificado
    print(f"Guardando certificado en: {cert_path}")
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    print("✓ Certificado guardado")
    
    print()
    print("="*60)
    print("✓ CERTIFICADOS GENERADOS EXITOSAMENTE")
    print("="*60)
    print()
    print(f"Certificado: {cert_path}")
    print(f"Clave privada: {key_path}")
    print(f"Válido por: {dias_validez} días")
    print(f"Nombre común: {nombre_comun}")
    print()
    print("IMPORTANTE:")
    print("- Estos son certificados AUTOFIRMADOS para desarrollo/pruebas")
    print("- Los navegadores mostrarán advertencia de seguridad")
    print("- Para producción, usar certificados de Let's Encrypt o CA comercial")
    print()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Genera certificados SSL autofirmados'
    )
    parser.add_argument(
        '--cert',
        default='certs/cert.pem',
        help='Ruta del certificado (default: certs/cert.pem)'
    )
    parser.add_argument(
        '--key',
        default='certs/key.pem',
        help='Ruta de la clave privada (default: certs/key.pem)'
    )
    parser.add_argument(
        '--dias',
        type=int,
        default=365,
        help='Días de validez (default: 365)'
    )
    parser.add_argument(
        '--dominio',
        default='localhost',
        help='Nombre de dominio (default: localhost)'
    )
    
    args = parser.parse_args()
    
    try:
        generar_certificados(
            cert_path=args.cert,
            key_path=args.key,
            dias_validez=args.dias,
            nombre_comun=args.dominio
        )
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
