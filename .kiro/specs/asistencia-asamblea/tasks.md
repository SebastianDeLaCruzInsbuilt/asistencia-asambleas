# Plan de Implementación: Sistema de Confirmación de Asistencia a Asambleas

## Visión General

Implementación de una aplicación web simple en Python (Flask) con frontend HTML/CSS/JavaScript vanilla para confirmar asistencia a asambleas mediante verificación de identidad y ubicación geográfica. La base de datos de usuarios usa formato CSV para facilitar edición masiva.

## Tareas

- [x] 1. Configurar estructura del proyecto y dependencias
  - Crear estructura de directorios (backend, frontend, data)
  - Crear requirements.txt con Flask, flask-cors
  - Crear archivos de datos iniciales: usuarios.csv, configuracion.json, asistencias.json
  - Crear README.md con instrucciones de instalación y ejecución
  - _Requirements: 5.1, 5.2, 5.3_

- [x] 2. Implementar capa de datos y utilidades
  - [x] 2.1 Implementar funciones de carga y parseo de CSV
    - Función para cargar usuarios.csv
    - Función para parsear CSV a lista de diccionarios
    - Validación de formato CSV (columnas requeridas)
    - Manejo de errores de formato
    - _Requirements: 4.3, 4.6_

  - [ ]* 2.2 Escribir property test para carga de CSV
    - **Property 9: Round-trip de usuarios**
    - **Validates: Requirements 4.3**

  - [x] 2.3 Implementar función de cálculo de distancia Haversine
    - Implementar fórmula de Haversine en Python
    - Función que recibe dos pares de coordenadas y retorna distancia en metros
    - _Requirements: 2.2_

  - [ ]* 2.4 Escribir property test para cálculo de distancia
    - **Property 4: Cálculo de distancia correcto**
    - **Validates: Requirements 2.2**

  - [x] 2.5 Implementar funciones de carga de configuración y asistencias
    - Cargar configuracion.json
    - Cargar asistencias.json
    - Guardar asistencias.json
    - _Requirements: 4.1, 4.2, 4.7_

  - [ ]* 2.6 Escribir property test para round-trip de configuración
    - **Property 8: Round-trip de configuración**
    - **Validates: Requirements 4.1, 4.2**

- [x] 3. Checkpoint - Verificar funciones de datos
  - Asegurar que todas las pruebas pasen, preguntar al usuario si surgen dudas.

- [x] 4. Implementar endpoints del backend
  - [x] 4.1 Crear servidor Flask básico
    - Configurar Flask app
    - Configurar CORS
    - Servir archivos estáticos del frontend
    - _Requirements: 5.1, 5.4_

  - [x] 4.2 Implementar endpoint POST /api/validar-identidad
    - Validar que userId y documento estén presentes
    - Buscar usuario en lista cargada desde CSV
    - Retornar {valido: true/false, nombre: string}
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [ ]* 4.3 Escribir property test para validación de identidad
    - **Property 1: Validación de credenciales correcta**
    - **Property 3: Identificador único requerido**
    - **Validates: Requirements 1.1, 1.3, 1.4**

  - [x] 4.4 Implementar endpoint POST /api/confirmar-asistencia
    - Recibir userId, latitud, longitud
    - Calcular distancia a ubicación de asamblea
    - Verificar si está dentro del radio permitido
    - Verificar que no exista registro duplicado
    - Guardar asistencia si es válida
    - Retornar {confirmado: boolean, mensaje: string, distancia: number}
    - _Requirements: 2.2, 2.3, 2.4, 3.1, 3.3, 3.4_

  - [ ]* 4.5 Escribir property test para validación de ubicación
    - **Property 5: Validación de ubicación basada en radio**
    - **Validates: Requirements 2.3, 2.4**

  - [ ]* 4.6 Escribir property test para idempotencia de confirmación
    - **Property 7: Idempotencia de confirmación de asistencia**
    - **Validates: Requirements 3.3**

  - [x] 4.7 Implementar endpoint GET /api/configuracion
    - Retornar configuración actual de asamblea
    - _Requirements: 4.1, 4.2_

  - [x] 4.8 Implementar endpoint GET /api/asistencias
    - Retornar lista de asistencias confirmadas
    - _Requirements: 4.7_

  - [x] 4.9 Implementar endpoints CRUD para usuarios
    - GET /api/usuarios - Listar usuarios
    - POST /api/usuarios - Agregar usuario
    - PUT /api/usuarios/:userId - Actualizar usuario
    - DELETE /api/usuarios/:userId - Eliminar usuario
    - Actualizar archivo CSV después de cada operación
    - _Requirements: 4.3, 4.4, 4.5_

- [x] 5. Checkpoint - Verificar API del backend
  - Asegurar que todas las pruebas pasen, preguntar al usuario si surgen dudas.

- [x] 6. Implementar frontend de confirmación de asistencia
  - [x] 6.1 Crear index.html con estructura básica
    - Formulario de identificación
    - Área de mensajes de estado
    - Diseño responsive
    - _Requirements: 6.1, 6.4_

  - [x] 6.2 Crear styles.css con estilos simples
    - Estilos para formulario
    - Estilos para mensajes de éxito/error
    - Diseño responsive para móvil y escritorio
    - _Requirements: 6.1, 6.4_

  - [x] 6.3 Implementar app.js - Lógica de validación de identidad
    - Capturar credenciales del formulario
    - Llamar a POST /api/validar-identidad
    - Mostrar mensajes de error si credenciales inválidas
    - Continuar a solicitud de ubicación si válidas
    - _Requirements: 1.1, 1.2, 1.3, 6.2, 6.3_

  - [x] 6.4 Implementar app.js - Lógica de geolocalización
    - Solicitar permiso de ubicación usando Geolocation API
    - Obtener coordenadas del dispositivo
    - Manejar caso de permisos denegados
    - _Requirements: 2.1, 2.5, 6.3_

  - [x] 6.5 Implementar app.js - Lógica de confirmación de asistencia
    - Enviar userId y ubicación a POST /api/confirmar-asistencia
    - Mostrar mensaje de éxito si confirmado
    - Mostrar mensaje con distancia si fuera de rango
    - _Requirements: 2.3, 2.4, 3.1, 3.2, 6.2_

- [x] 7. Implementar interfaz administrativa
  - [x] 7.1 Crear admin.html con tabla de usuarios
    - Tabla para mostrar lista de usuarios
    - Formulario para agregar nuevo usuario
    - Botones para editar/eliminar usuarios
    - _Requirements: 4.3, 4.4, 4.5_

  - [x] 7.2 Crear admin.js con lógica CRUD
    - Cargar y mostrar lista de usuarios (GET /api/usuarios)
    - Agregar nuevo usuario (POST /api/usuarios)
    - Editar usuario existente (PUT /api/usuarios/:userId)
    - Eliminar usuario (DELETE /api/usuarios/:userId)
    - Validación de campos en cliente
    - _Requirements: 4.3, 4.4, 4.5_

  - [x] 7.3 Agregar funcionalidad de exportar usuarios a CSV
    - Botón para descargar usuarios.csv actual
    - Generar CSV desde datos en memoria
    - _Requirements: 4.3_

- [x] 8. Implementar manejo de errores y validaciones
  - [x] 8.1 Agregar validación de entrada en backend
    - Validar formato de coordenadas (latitud: -90 a 90, longitud: -180 a 180)
    - Validar tipos de datos
    - Validar campos requeridos
    - Validar que radio permitido sea positivo
    - _Requirements: 4.6_

  - [ ]* 8.2 Escribir unit tests para validaciones de entrada
    - Test coordenadas inválidas son rechazadas
    - Test campos faltantes son rechazados
    - Test radio negativo es rechazado

  - [x] 8.3 Implementar manejo de errores en frontend
    - Mostrar mensajes claros para cada tipo de error
    - Manejar errores de red
    - Manejar respuestas de error del servidor
    - _Requirements: 6.2_

- [x] 9. Implementar recarga automática de usuarios.csv
  - [x] 9.1 Agregar file watcher para usuarios.csv
    - Detectar cambios en archivo CSV
    - Recargar usuarios automáticamente cuando cambie
    - Validar formato al recargar
    - _Requirements: 4.3, 4.6_

  - [x] 9.2 Agregar endpoint POST /api/reload-usuarios
    - Endpoint manual para forzar recarga
    - Útil si file watcher no funciona
    - _Requirements: 4.3_

- [x] 10. Checkpoint final - Pruebas de integración
  - [x] 10.1 Probar flujo completo exitoso
    - Usuario válido + ubicación correcta = asistencia confirmada
    - _Requirements: 1.1, 1.2, 2.1, 2.2, 2.3, 3.1, 3.2_

  - [x] 10.2 Probar flujo con credenciales inválidas
    - Usuario inválido = mensaje de error
    - _Requirements: 1.3_

  - [x] 10.3 Probar flujo con ubicación fuera de rango
    - Ubicación lejana = mensaje con instrucciones
    - _Requirements: 2.4_

  - [x] 10.4 Probar prevención de duplicados
    - Confirmar dos veces = solo un registro
    - _Requirements: 3.3_

  - [x] 10.5 Probar gestión de usuarios desde admin
    - Agregar, editar, eliminar usuarios desde interfaz
    - Verificar que cambios se reflejen en CSV
    - _Requirements: 4.3, 4.4, 4.5_

  - [x] 10.6 Probar edición manual de CSV
    - Editar usuarios.csv directamente
    - Verificar que servidor recargue automáticamente
    - _Requirements: 4.3, 4.6_

- [x] 11. Documentación y despliegue
  - [x] 11.1 Completar README.md
    - Instrucciones de instalación
    - Instrucciones de configuración (ubicación asamblea, radio)
    - Instrucciones de ejecución
    - Cómo agregar usuarios (CSV y admin)
    - _Requirements: 5.3_

  - [x] 11.2 Crear archivo de ejemplo usuarios.csv
    - Incluir 5-10 usuarios de ejemplo
    - Documentar formato en comentarios
    - _Requirements: 4.3_

  - [x] 11.3 Crear script de inicio simple
    - Script start.sh o start.bat
    - Instalar dependencias y ejecutar servidor
    - _Requirements: 5.1, 5.2_

## Notas

- Las tareas marcadas con `*` son opcionales y pueden omitirse para un MVP más rápido
- Cada tarea referencia requisitos específicos para trazabilidad
- Los checkpoints aseguran validación incremental
- Los property tests validan propiedades de corrección universales
- Los unit tests validan ejemplos específicos y casos edge
- La implementación prioriza simplicidad y facilidad de despliegue
