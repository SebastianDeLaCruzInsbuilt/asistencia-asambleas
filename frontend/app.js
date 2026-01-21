/**
 * Sistema de Confirmación de Asistencia a Asambleas
 * Frontend JavaScript Application
 * 
 * Requirements: 1.1, 1.2, 1.3, 2.1, 2.3, 2.4, 2.5, 3.1, 3.2, 6.2, 6.3
 */

// ============================================================================
// CONFIGURACIÓN Y CONSTANTES
// ============================================================================

const API_BASE_URL = window.location.origin;

// Estado de la aplicación
const appState = {
    userId: null,
    nombreUsuario: null,
    ubicacionUsuario: null
};

// ============================================================================
// ELEMENTOS DEL DOM
// ============================================================================

// Pasos
const pasoIdentificacion = document.getElementById('paso-identificacion');
const pasoUbicacion = document.getElementById('paso-ubicacion');

// Formulario de identificación
const formIdentificacion = document.getElementById('form-identificacion');
const inputDocumento = document.getElementById('documento');
const btnValidar = document.getElementById('btn-validar');

// Paso de ubicación
const nombreUsuarioSpan = document.getElementById('nombre-usuario');
const btnConfirmarUbicacion = document.getElementById('btn-confirmar-ubicacion');

// Mensajes y loading
const areaMensajes = document.getElementById('area-mensajes');
const loadingIndicator = document.getElementById('loading');

// ============================================================================
// FUNCIONES DE UI
// ============================================================================

/**
 * Muestra un mensaje al usuario
 * 
 * @param {string} tipo - Tipo de mensaje: 'exito', 'error', 'info', 'warning'
 * @param {string} mensaje - Texto del mensaje a mostrar
 * @param {string} titulo - Título opcional del mensaje
 */
function mostrarMensaje(tipo, mensaje, titulo = null) {
    // Limpiar mensajes anteriores
    areaMensajes.innerHTML = '';
    
    // Crear elemento de mensaje
    const divMensaje = document.createElement('div');
    divMensaje.className = `mensaje mensaje-${tipo}`;
    
    if (titulo) {
        const strong = document.createElement('strong');
        strong.textContent = titulo;
        divMensaje.appendChild(strong);
    }
    
    const p = document.createElement('p');
    p.textContent = mensaje;
    p.style.margin = titulo ? '0' : '0';
    divMensaje.appendChild(p);
    
    areaMensajes.appendChild(divMensaje);
    
    // Scroll al mensaje
    divMensaje.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Limpia todos los mensajes mostrados
 */
function limpiarMensajes() {
    areaMensajes.innerHTML = '';
}

/**
 * Muestra el indicador de carga
 */
function mostrarLoading() {
    loadingIndicator.classList.remove('oculto');
}

/**
 * Oculta el indicador de carga
 */
function ocultarLoading() {
    loadingIndicator.classList.add('oculto');
}

/**
 * Cambia al paso especificado
 * 
 * @param {string} paso - 'identificacion' o 'ubicacion'
 */
function cambiarPaso(paso) {
    if (paso === 'identificacion') {
        pasoIdentificacion.classList.add('activo');
        pasoUbicacion.classList.remove('activo');
    } else if (paso === 'ubicacion') {
        pasoIdentificacion.classList.remove('activo');
        pasoUbicacion.classList.add('activo');
    }
}

/**
 * Deshabilita un botón
 * 
 * @param {HTMLButtonElement} boton - Botón a deshabilitar
 */
function deshabilitarBoton(boton) {
    boton.disabled = true;
}

/**
 * Habilita un botón
 * 
 * @param {HTMLButtonElement} boton - Botón a habilitar
 */
function habilitarBoton(boton) {
    boton.disabled = false;
}

// ============================================================================
// FUNCIONES DE API
// ============================================================================

/**
 * Valida las credenciales del usuario contra el backend
 * Requirements: 1.1, 1.2, 1.3, 6.2
 * 
 * @param {string} documento - Número de documento
 * @returns {Promise<{valido: boolean, nombre?: string, userId?: string}>}
 */
async function validarIdentidad(documento) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/validar-identidad`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                documento: documento
            })
        });
        
        // Manejar errores HTTP (Requirement 6.2)
        if (!response.ok) {
            // Error del servidor (4xx o 5xx)
            let mensajeError = 'Error del servidor';
            
            try {
                const errorData = await response.json();
                mensajeError = errorData.error || errorData.mensaje || mensajeError;
            } catch (e) {
                // Si no se puede parsear el JSON, usar mensaje genérico
                if (response.status >= 500) {
                    mensajeError = 'Error del servidor. Por favor intenta nuevamente más tarde.';
                } else if (response.status >= 400) {
                    mensajeError = 'Solicitud inválida. Por favor verifica los datos ingresados.';
                }
            }
            
            throw new Error(mensajeError);
        }
        
        const data = await response.json();
        return data;
        
    } catch (error) {
        console.error('Error al validar identidad:', error);
        
        // Manejar errores de red (Requirement 6.2)
        if (error instanceof TypeError && error.message.includes('fetch')) {
            throw new Error('Error de conexión. Por favor verifica tu conexión a internet e intenta nuevamente.');
        }
        
        // Re-lanzar el error con el mensaje apropiado
        throw error;
    }
}

/**
 * Confirma la asistencia del usuario enviando su ubicación
 * Requirements: 2.3, 2.4, 3.1, 3.2, 6.2
 * 
 * @param {string} userId - ID del usuario
 * @param {number} latitud - Latitud de la ubicación
 * @param {number} longitud - Longitud de la ubicación
 * @returns {Promise<{confirmado: boolean, mensaje: string, distancia: number}>}
 */
async function confirmarAsistencia(userId, latitud, longitud) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/confirmar-asistencia`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                userId: userId,
                latitud: latitud,
                longitud: longitud
            })
        });
        
        // Manejar errores HTTP (Requirement 6.2)
        if (!response.ok) {
            // Error del servidor (4xx o 5xx)
            let mensajeError = 'Error del servidor';
            
            try {
                const errorData = await response.json();
                mensajeError = errorData.mensaje || errorData.error || mensajeError;
            } catch (e) {
                // Si no se puede parsear el JSON, usar mensaje genérico
                if (response.status >= 500) {
                    mensajeError = 'Error del servidor. Por favor intenta nuevamente más tarde.';
                } else if (response.status >= 400) {
                    mensajeError = 'Solicitud inválida. Por favor verifica los datos ingresados.';
                }
            }
            
            throw new Error(mensajeError);
        }
        
        const data = await response.json();
        return data;
        
    } catch (error) {
        console.error('Error al confirmar asistencia:', error);
        
        // Manejar errores de red (Requirement 6.2)
        if (error instanceof TypeError && error.message.includes('fetch')) {
            throw new Error('Error de conexión. Por favor verifica tu conexión a internet e intenta nuevamente.');
        }
        
        // Re-lanzar el error con el mensaje apropiado
        throw error;
    }
}

// ============================================================================
// MANEJADORES DE EVENTOS - VALIDACIÓN DE IDENTIDAD (Sub-task 6.3)
// ============================================================================

/**
 * Maneja el envío del formulario de identificación
 * Requirements: 1.1, 1.2, 1.3, 6.2, 6.3
 */
formIdentificacion.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    // Limpiar mensajes anteriores
    limpiarMensajes();
    
    // Obtener valor del formulario
    const documento = inputDocumento.value.trim();
    
    // Validar que el campo no esté vacío
    if (!documento) {
        mostrarMensaje('error', 'Por favor ingresa tu número de documento', 'Campo requerido');
        return;
    }
    
    // Deshabilitar botón y mostrar loading
    deshabilitarBoton(btnValidar);
    mostrarLoading();
    
    try {
        // Llamar a la API para validar identidad (Requirement 1.1)
        const resultado = await validarIdentidad(documento);
        
        ocultarLoading();
        
        // Verificar si las credenciales son válidas (Requirements 1.2, 1.3)
        if (resultado.valido) {
            // Credenciales válidas - guardar estado y continuar (Requirement 1.2)
            appState.userId = resultado.userId;
            appState.nombreUsuario = resultado.nombre;
            
            // Mostrar mensaje de éxito
            mostrarMensaje('exito', `Bienvenido/a, ${resultado.nombre}`, 'Identidad verificada');
            
            // Esperar un momento antes de cambiar de paso
            setTimeout(() => {
                limpiarMensajes();
                nombreUsuarioSpan.textContent = resultado.nombre;
                cambiarPaso('ubicacion');
            }, 1500);
            
        } else {
            // Credenciales inválidas - mostrar error (Requirement 1.3, 6.2)
            mostrarMensaje('error', 'El número de documento ingresado no es válido. Por favor verifica tu documento.', 'Documento inválido');
            habilitarBoton(btnValidar);
        }
        
    } catch (error) {
        ocultarLoading();
        habilitarBoton(btnValidar);
        
        // Mostrar mensaje de error claro según el tipo (Requirement 6.2)
        const mensajeError = error.message || 'Ocurrió un error al validar tu identidad. Por favor intenta nuevamente.';
        
        // Determinar el tipo de error para mostrar el título apropiado
        let tipoError = 'Error';
        if (mensajeError.includes('conexión') || mensajeError.includes('internet')) {
            tipoError = 'Error de conexión';
        } else if (mensajeError.includes('servidor')) {
            tipoError = 'Error del servidor';
        } else if (mensajeError.includes('inválid')) {
            tipoError = 'Datos inválidos';
        }
        
        mostrarMensaje('error', mensajeError, tipoError);
    }
});

// ============================================================================
// FUNCIONES DE GEOLOCALIZACIÓN (Sub-task 6.4)
// ============================================================================

/**
 * Obtiene la ubicación actual del usuario usando Geolocation API
 * Requirements: 2.1, 2.5, 6.3
 * 
 * @returns {Promise<{latitud: number, longitud: number}>}
 */
function obtenerUbicacion() {
    return new Promise((resolve, reject) => {
        // Verificar si el navegador soporta geolocalización
        if (!navigator.geolocation) {
            reject(new Error('Tu navegador no soporta geolocalización'));
            return;
        }
        
        // Solicitar ubicación (Requirement 2.1)
        navigator.geolocation.getCurrentPosition(
            // Éxito
            (position) => {
                resolve({
                    latitud: position.coords.latitude,
                    longitud: position.coords.longitude
                });
            },
            // Error (Requirement 2.5)
            (error) => {
                let mensajeError = 'No se pudo obtener tu ubicación';
                
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        mensajeError = 'Permiso de ubicación denegado. Por favor habilita los permisos de ubicación en tu navegador para continuar.';
                        break;
                    case error.POSITION_UNAVAILABLE:
                        mensajeError = 'Información de ubicación no disponible. Por favor verifica tu conexión GPS.';
                        break;
                    case error.TIMEOUT:
                        mensajeError = 'Tiempo de espera agotado al obtener ubicación. Por favor intenta nuevamente.';
                        break;
                }
                
                reject(new Error(mensajeError));
            },
            // Opciones
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    });
}

// ============================================================================
// MANEJADORES DE EVENTOS - CONFIRMACIÓN DE UBICACIÓN (Sub-task 6.4 y 6.5)
// ============================================================================

/**
 * Maneja el clic en el botón de confirmar ubicación
 * Requirements: 2.1, 2.3, 2.4, 2.5, 3.1, 3.2, 6.2, 6.3
 */
btnConfirmarUbicacion.addEventListener('click', async () => {
    // Limpiar mensajes anteriores
    limpiarMensajes();
    
    // Deshabilitar botón y mostrar loading
    deshabilitarBoton(btnConfirmarUbicacion);
    mostrarLoading();
    
    try {
        // Obtener ubicación del usuario (Requirements 2.1, 2.5)
        mostrarMensaje('info', 'Obteniendo tu ubicación GPS...', 'Procesando');
        const ubicacion = await obtenerUbicacion();
        
        appState.ubicacionUsuario = ubicacion;
        
        // Confirmar asistencia con el backend (Requirements 2.3, 2.4, 3.1, 3.2)
        limpiarMensajes();
        mostrarMensaje('info', 'Verificando tu ubicación...', 'Procesando');
        
        const resultado = await confirmarAsistencia(
            appState.userId,
            ubicacion.latitud,
            ubicacion.longitud
        );
        
        ocultarLoading();
        limpiarMensajes();
        
        // Mostrar resultado (Requirements 3.2, 6.2)
        if (resultado.confirmado) {
            // Asistencia confirmada exitosamente (Requirement 3.2)
            mostrarMensaje(
                'exito',
                `Tu asistencia ha sido registrada exitosamente. Distancia: ${resultado.distancia} metros.`,
                '¡Confirmación exitosa!'
            );
            
            // Deshabilitar el botón permanentemente
            btnConfirmarUbicacion.textContent = 'Asistencia Confirmada ✓';
            
        } else {
            // Fuera de rango o error (Requirement 2.4, 6.2)
            mostrarMensaje(
                'warning',
                resultado.mensaje,
                'No se pudo confirmar'
            );
            
            // Habilitar botón para reintentar
            habilitarBoton(btnConfirmarUbicacion);
        }
        
    } catch (error) {
        ocultarLoading();
        habilitarBoton(btnConfirmarUbicacion);
        
        // Mostrar error apropiado según el tipo (Requirement 2.5, 6.2)
        const mensajeError = error.message || 'Ocurrió un error al confirmar tu asistencia. Por favor intenta nuevamente.';
        
        // Determinar el tipo de error para mostrar el título y tipo apropiados
        let tipoMensaje = 'error';
        let tituloError = 'Error';
        
        if (mensajeError.includes('Permiso de ubicación denegado') || mensajeError.includes('permiso')) {
            tipoMensaje = 'error';
            tituloError = 'Permiso requerido';
        } else if (mensajeError.includes('conexión') || mensajeError.includes('internet')) {
            tipoMensaje = 'error';
            tituloError = 'Error de conexión';
        } else if (mensajeError.includes('servidor')) {
            tipoMensaje = 'error';
            tituloError = 'Error del servidor';
        } else if (mensajeError.includes('GPS') || mensajeError.includes('ubicación no disponible')) {
            tipoMensaje = 'warning';
            tituloError = 'Ubicación no disponible';
        } else if (mensajeError.includes('Tiempo de espera')) {
            tipoMensaje = 'warning';
            tituloError = 'Tiempo agotado';
        }
        
        mostrarMensaje(tipoMensaje, mensajeError, tituloError);
    }
});

// ============================================================================
// INICIALIZACIÓN
// ============================================================================

/**
 * Inicializa la aplicación cuando el DOM está listo
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('Sistema de Confirmación de Asistencia iniciado');
    
    // Asegurar que estamos en el paso de identificación
    cambiarPaso('identificacion');
    
    // Focus en el campo de documento
    inputDocumento.focus();
});
