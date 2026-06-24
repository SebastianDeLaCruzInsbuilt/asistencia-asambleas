/**
 * Sistema de Confirmación de Asistencia a Asambleas
 * Interfaz Administrativa - JavaScript
 * 
 * Requirements: 4.3, 4.4, 4.5
 */

// ============================================================================
// AUTENTICACIÓN
// ============================================================================

/**
 * Obtiene el token de autenticación del localStorage
 */
function obtenerToken() {
    return localStorage.getItem('admin_token');
}

/**
 * Verifica si el usuario está autenticado
 */
async function verificarAutenticacion() {
    const token = obtenerToken();
    
    if (!token) {
        redirigirALogin();
        return false;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/admin/verificar`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            // Token inválido o expirado
            localStorage.removeItem('admin_token');
            redirigirALogin();
            return false;
        }
        
        return true;
    } catch (error) {
        console.error('Error al verificar autenticacion:', error);
        // Error de red - no redirigir, el token puede ser valido
        return true;
    }
}

/**
 * Redirige al usuario a la página de login
 */
function redirigirALogin() {
    window.location.href = 'login.html';
}

/**
 * Cierra la sesión del usuario
 */
async function cerrarSesion() {
    const token = obtenerToken();
    
    if (token) {
        try {
            await fetch(`${API_BASE_URL}/api/admin/logout`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
        } catch (error) {
            console.error('Error al cerrar sesión:', error);
        }
    }
    
    localStorage.removeItem('admin_token');
    redirigirALogin();
}

/**
 * Realiza una petición autenticada a la API
 */
async function fetchAutenticado(url, options = {}) {
    const token = obtenerToken();
    
    if (!token) {
        redirigirALogin();
        throw new Error('No autenticado');
    }
    
    // Agregar token al header
    const headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`
    };
    
    const response = await fetch(url, {
        ...options,
        headers
    });
    
    // Si el token es inválido, redirigir a login
    if (response.status === 401) {
        localStorage.removeItem('admin_token');
        redirigirALogin();
        throw new Error('Sesión expirada');
    }
    
    return response;
}

// ============================================================================
// CONFIGURACIÓN Y CONSTANTES
// ============================================================================

const API_BASE_URL = window.location.origin;

// Estado de la aplicación
const appState = {
    usuarios: [],
    usuarioEditando: null,
    asistencias: []
};

// ============================================================================
// ELEMENTOS DEL DOM
// ============================================================================

// Formulario de agregar
const formAgregar = document.getElementById('form-agregar');
const inputNuevoUserId = document.getElementById('nuevo-userId');
const inputNuevoDocumento = document.getElementById('nuevo-documento');
const inputNuevoNombre = document.getElementById('nuevo-nombre');
const btnAgregar = document.getElementById('btn-agregar');

// Tabla de usuarios
const tbodyUsuarios = document.getElementById('tbody-usuarios');
const loadingIndicator = document.getElementById('loading');

// Tabla de asistencias
const tbodyAsistencias = document.getElementById('tbody-asistencias');
const loadingAsistencias = document.getElementById('loading-asistencias');

// Modal de edición
const modalEditar = document.getElementById('modal-editar');
const formEditar = document.getElementById('form-editar');
const inputEditarUserIdOriginal = document.getElementById('editar-userId-original');
const inputEditarUserId = document.getElementById('editar-userId');
const inputEditarDocumento = document.getElementById('editar-documento');
const inputEditarNombre = document.getElementById('editar-nombre');
const btnCerrarModal = document.getElementById('btn-cerrar-modal');
const btnCancelarEditar = document.getElementById('btn-cancelar-editar');
const btnGuardarEditar = document.getElementById('btn-guardar-editar');

// Botón de exportar
const btnExportar = document.getElementById('btn-exportar');
const btnExportarAsistencias = document.getElementById('btn-exportar-asistencias');

// Botón de eliminar todos los usuarios
const btnEliminarTodosUsuarios = document.getElementById('btn-eliminar-todos-usuarios');

// Importación CSV
const inputCsvFile = document.getElementById('input-csv-file');
const btnImportarCsv = document.getElementById('btn-importar-csv');
const resultadoImportacion = document.getElementById('resultado-importacion');
const resultadoImportacionTexto = document.getElementById('resultado-importacion-texto');

// Reinicio de asistencias
const btnReiniciarAsistencias = document.getElementById('btn-reiniciar-asistencias');
const advertenciaReinicio = document.getElementById('advertencia-reinicio');
const btnConfirmarReinicio = document.getElementById('btn-confirmar-reinicio');
const btnCancelarReinicio = document.getElementById('btn-cancelar-reinicio');

// Mensajes
const areaMensajes = document.getElementById('area-mensajes');

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
    
    // Auto-ocultar después de 5 segundos
    setTimeout(() => {
        divMensaje.remove();
    }, 5000);
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
 * Abre el modal de edición
 */
function abrirModal() {
    modalEditar.classList.add('activo');
}

/**
 * Cierra el modal de edición
 */
function cerrarModal() {
    modalEditar.classList.remove('activo');
    formEditar.reset();
    appState.usuarioEditando = null;
}

// ============================================================================
// FUNCIONES DE API - CRUD DE USUARIOS
// ============================================================================

/**
 * Carga la lista de usuarios desde el backend
 * Requirement: 4.3, 6.2
 * 
 * @returns {Promise<Array>}
 */
async function cargarListaUsuarios() {
    try {
        const response = await fetchAutenticado(`${API_BASE_URL}/api/usuarios`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        // Manejar errores HTTP (Requirement 6.2)
        if (!response.ok) {
            let mensajeError = 'Error al cargar usuarios';
            
            try {
                const errorData = await response.json();
                mensajeError = errorData.error || errorData.mensaje || mensajeError;
            } catch (e) {
                if (response.status >= 500) {
                    mensajeError = 'Error del servidor. Por favor intenta nuevamente más tarde.';
                } else if (response.status >= 400) {
                    mensajeError = 'Error al cargar usuarios. Por favor recarga la página.';
                }
            }
            
            throw new Error(mensajeError);
        }
        
        const usuarios = await response.json();
        return usuarios;
        
    } catch (error) {
        console.error('Error al cargar usuarios:', error);
        
        // Manejar errores de red (Requirement 6.2)
        if (error instanceof TypeError && error.message.includes('fetch')) {
            throw new Error('Error de conexión. Por favor verifica tu conexión a internet.');
        }
        
        throw error;
    }
}

/**
 * Carga la lista de asistencias desde el backend
 * Requirement: 4.7, 6.2
 * 
 * @returns {Promise<Array>}
 */
async function cargarListaAsistencias() {
    try {
        const response = await fetchAutenticado(`${API_BASE_URL}/api/asistencias`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        // Manejar errores HTTP (Requirement 6.2)
        if (!response.ok) {
            let mensajeError = 'Error al cargar asistencias';
            
            try {
                const errorData = await response.json();
                mensajeError = errorData.error || errorData.mensaje || mensajeError;
            } catch (e) {
                if (response.status >= 500) {
                    mensajeError = 'Error del servidor. Por favor intenta nuevamente más tarde.';
                } else if (response.status >= 400) {
                    mensajeError = 'Error al cargar asistencias. Por favor recarga la página.';
                }
            }
            
            throw new Error(mensajeError);
        }
        
        const asistencias = await response.json();
        return asistencias;
        
    } catch (error) {
        console.error('Error al cargar asistencias:', error);
        
        // Manejar errores de red (Requirement 6.2)
        if (error instanceof TypeError && error.message.includes('fetch')) {
            throw new Error('Error de conexión. Por favor verifica tu conexión a internet.');
        }
        
        throw error;
    }
}

/**
 * Agrega un nuevo usuario
 * Requirement: 4.4, 6.2
 * 
 * @param {Object} usuario - Datos del usuario {userId, documento, nombre}
 * @returns {Promise<Object>}
 */
async function agregarNuevoUsuario(usuario) {
    try {
        const response = await fetchAutenticado(`${API_BASE_URL}/api/usuarios`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(usuario)
        });
        
        const data = await response.json();
        
        // Manejar errores HTTP (Requirement 6.2)
        if (!response.ok) {
            const mensajeError = data.mensaje || data.error || 'Error al agregar usuario';
            throw new Error(mensajeError);
        }
        
        return data;
        
    } catch (error) {
        console.error('Error al agregar usuario:', error);
        
        // Manejar errores de red (Requirement 6.2)
        if (error instanceof TypeError && error.message.includes('fetch')) {
            throw new Error('Error de conexión. Por favor verifica tu conexión a internet.');
        }
        
        throw error;
    }
}

/**
 * Edita un usuario existente
 * Requirement: 4.5, 6.2
 * 
 * @param {string} userId - ID del usuario a editar
 * @param {Object} datos - Nuevos datos {documento, nombre}
 * @returns {Promise<Object>}
 */
async function editarUsuario(userId, datos) {
    try {
        const response = await fetchAutenticado(`${API_BASE_URL}/api/usuarios/${userId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datos)
        });
        
        const data = await response.json();
        
        // Manejar errores HTTP (Requirement 6.2)
        if (!response.ok) {
            const mensajeError = data.mensaje || data.error || 'Error al editar usuario';
            throw new Error(mensajeError);
        }
        
        return data;
        
    } catch (error) {
        console.error('Error al editar usuario:', error);
        
        // Manejar errores de red (Requirement 6.2)
        if (error instanceof TypeError && error.message.includes('fetch')) {
            throw new Error('Error de conexión. Por favor verifica tu conexión a internet.');
        }
        
        throw error;
    }
}

/**
 * Elimina un usuario
 * Requirement: 4.5, 6.2
 * 
 * @param {string} userId - ID del usuario a eliminar
 * @returns {Promise<Object>}
 */
async function eliminarUsuario(userId) {
    try {
        const response = await fetchAutenticado(`${API_BASE_URL}/api/usuarios/${userId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        // Manejar errores HTTP (Requirement 6.2)
        if (!response.ok) {
            const mensajeError = data.mensaje || data.error || 'Error al eliminar usuario';
            throw new Error(mensajeError);
        }
        
        return data;
        
    } catch (error) {
        console.error('Error al eliminar usuario:', error);
        
        // Manejar errores de red (Requirement 6.2)
        if (error instanceof TypeError && error.message.includes('fetch')) {
            throw new Error('Error de conexión. Por favor verifica tu conexión a internet.');
        }
        
        throw error;
    }
}

// ============================================================================
// FUNCIONES DE RENDERIZADO
// ============================================================================

/**
 * Renderiza la tabla de usuarios (con filtros aplicados)
 * Requirement: 4.3
 */
function renderizarTablaUsuarios() {
    // Limpiar tabla
    tbodyUsuarios.innerHTML = '';
    
    // Obtener valores de filtros
    const filtroUserId = (document.getElementById('filtro-userId')?.value || '').toLowerCase().trim();
    const filtroDocumento = (document.getElementById('filtro-documento')?.value || '').toLowerCase().trim();
    const filtroNombre = (document.getElementById('filtro-nombre')?.value || '').toLowerCase().trim();
    
    // Filtrar usuarios
    const usuariosFiltrados = appState.usuarios.filter(usuario => {
        if (filtroUserId && !usuario.userId.toLowerCase().includes(filtroUserId)) return false;
        if (filtroDocumento && !usuario.documento.toLowerCase().includes(filtroDocumento)) return false;
        if (filtroNombre && !usuario.nombre.toLowerCase().includes(filtroNombre)) return false;
        return true;
    });
    
    // Si no hay usuarios, mostrar mensaje
    if (usuariosFiltrados.length === 0) {
        const tr = document.createElement('tr');
        const mensaje = appState.usuarios.length === 0 
            ? 'No hay usuarios registrados. Agrega el primer usuario usando el formulario arriba.'
            : 'No se encontraron usuarios con los filtros aplicados.';
        tr.innerHTML = `
            <td colspan="4" class="tabla-vacia">
                ${mensaje}
            </td>
        `;
        tbodyUsuarios.appendChild(tr);
        return;
    }
    
    // Renderizar cada usuario filtrado
    usuariosFiltrados.forEach(usuario => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${escapeHtml(usuario.userId)}</td>
            <td>${escapeHtml(usuario.documento)}</td>
            <td>${escapeHtml(usuario.nombre)}</td>
            <td>
                <button class="btn-accion btn-editar" data-userid="${escapeHtml(usuario.userId)}">
                    Editar
                </button>
                <button class="btn-accion btn-eliminar" data-userid="${escapeHtml(usuario.userId)}">
                    Eliminar
                </button>
            </td>
        `;
        tbodyUsuarios.appendChild(tr);
    });
    
    // Agregar event listeners a los botones
    document.querySelectorAll('.btn-editar').forEach(btn => {
        btn.addEventListener('click', handleEditarClick);
    });
    
    document.querySelectorAll('.btn-eliminar').forEach(btn => {
        btn.addEventListener('click', handleEliminarClick);
    });
}

/**
 * Renderiza la tabla de asistencias (con filtros aplicados)
 * Requirement: 4.7
 */
function renderizarTablaAsistencias() {
    // Limpiar tabla
    tbodyAsistencias.innerHTML = '';
    
    // Obtener valores de filtros
    const filtroNombre = (document.getElementById('filtro-asist-nombre')?.value || '').toLowerCase().trim();
    const filtroUserId = (document.getElementById('filtro-asist-userId')?.value || '').toLowerCase().trim();
    const filtroFecha = (document.getElementById('filtro-asist-fecha')?.value || '').toLowerCase().trim();
    const filtroUbicacion = (document.getElementById('filtro-asist-ubicacion')?.value || '').toLowerCase().trim();
    
    // Filtrar asistencias
    const asistenciasFiltradas = appState.asistencias.filter(asistencia => {
        if (filtroNombre && !asistencia.nombre.toLowerCase().includes(filtroNombre)) return false;
        if (filtroUserId && !asistencia.userId.toLowerCase().includes(filtroUserId)) return false;
        
        if (filtroFecha) {
            const fecha = new Date(asistencia.fechaHora);
            const fechaFormateada = fecha.toLocaleString('es-ES', {
                year: 'numeric', month: '2-digit', day: '2-digit',
                hour: '2-digit', minute: '2-digit', second: '2-digit'
            }).toLowerCase();
            if (!fechaFormateada.includes(filtroFecha)) return false;
        }
        
        if (filtroUbicacion) {
            const lat = asistencia.ubicacion.latitud.toFixed(6);
            const lon = asistencia.ubicacion.longitud.toFixed(6);
            const ubicacionStr = `${lat}, ${lon}`.toLowerCase();
            if (!ubicacionStr.includes(filtroUbicacion)) return false;
        }
        
        return true;
    });
    
    // Si no hay asistencias, mostrar mensaje
    if (asistenciasFiltradas.length === 0) {
        const tr = document.createElement('tr');
        const mensaje = appState.asistencias.length === 0
            ? 'No hay asistencias confirmadas todavía.'
            : 'No se encontraron asistencias con los filtros aplicados.';
        tr.innerHTML = `
            <td colspan="4" class="tabla-vacia">
                ${mensaje}
            </td>
        `;
        tbodyAsistencias.appendChild(tr);
        return;
    }
    
    // Renderizar cada asistencia filtrada
    asistenciasFiltradas.forEach(asistencia => {
        const tr = document.createElement('tr');
        
        // Formatear fecha y hora
        const fecha = new Date(asistencia.fechaHora);
        const fechaFormateada = fecha.toLocaleString('es-ES', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        
        // Formatear ubicación
        const lat = asistencia.ubicacion.latitud.toFixed(6);
        const lon = asistencia.ubicacion.longitud.toFixed(6);
        const ubicacion = `${lat}, ${lon}`;
        
        tr.innerHTML = `
            <td>${escapeHtml(asistencia.nombre)}</td>
            <td>${escapeHtml(asistencia.userId)}</td>
            <td>${fechaFormateada}</td>
            <td style="font-family: monospace; font-size: 12px;">${ubicacion}</td>
        `;
        tbodyAsistencias.appendChild(tr);
    });
}

/**
 * Escapa HTML para prevenir XSS
 * 
 * @param {string} text - Texto a escapar
 * @returns {string}
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ============================================================================
// MANEJADORES DE EVENTOS - CARGAR USUARIOS
// ============================================================================

/**
 * Carga y muestra la lista de usuarios
 * Requirement: 4.3
 */
async function cargarYMostrarUsuarios() {
    mostrarLoading();
    limpiarMensajes();
    
    try {
        const usuarios = await cargarListaUsuarios();
        appState.usuarios = usuarios;
        renderizarTablaUsuarios();
        ocultarLoading();
        
    } catch (error) {
        ocultarLoading();
        mostrarMensaje('error', 'No se pudo cargar la lista de usuarios. Por favor recarga la página.', 'Error');
    }
}

/**
 * Carga y muestra la lista de asistencias
 * Requirement: 4.7
 */
async function cargarYMostrarAsistencias() {
    if (loadingAsistencias) {
        loadingAsistencias.classList.remove('oculto');
    }
    
    try {
        const asistencias = await cargarListaAsistencias();
        appState.asistencias = asistencias;
        renderizarTablaAsistencias();
        
        if (loadingAsistencias) {
            loadingAsistencias.classList.add('oculto');
        }
        
    } catch (error) {
        if (loadingAsistencias) {
            loadingAsistencias.classList.add('oculto');
        }
        console.error('Error al cargar asistencias:', error);
        // No mostrar mensaje de error para asistencias, solo log
    }
}

// ============================================================================
// MANEJADORES DE EVENTOS - AGREGAR USUARIO
// ============================================================================

/**
 * Maneja el envío del formulario de agregar usuario
 * Requirements: 4.4
 */
formAgregar.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    // Obtener valores del formulario
    const userId = inputNuevoUserId.value.trim();
    const documento = inputNuevoDocumento.value.trim();
    const nombre = inputNuevoNombre.value.trim();
    
    // Validación en cliente (Requirement: 4.4)
    if (!userId || !documento || !nombre) {
        mostrarMensaje('error', 'Todos los campos son requeridos', 'Validación');
        return;
    }
    
    // Verificar que el userId no exista ya
    const usuarioExiste = appState.usuarios.some(u => u.userId === userId);
    if (usuarioExiste) {
        mostrarMensaje('error', 'Ya existe un usuario con ese ID', 'Usuario duplicado');
        return;
    }
    
    // Deshabilitar botón
    btnAgregar.disabled = true;
    limpiarMensajes();
    
    try {
        // Agregar usuario
        await agregarNuevoUsuario({
            userId: userId,
            documento: documento,
            nombre: nombre
        });
        
        // Mostrar mensaje de éxito
        mostrarMensaje('exito', `Usuario ${nombre} agregado exitosamente`, 'Usuario agregado');
        
        // Limpiar formulario
        formAgregar.reset();
        inputNuevoUserId.focus();
        
        // Recargar lista de usuarios
        await cargarYMostrarUsuarios();
        
    } catch (error) {
        mostrarMensaje('error', error.message || 'No se pudo agregar el usuario', 'Error');
    } finally {
        btnAgregar.disabled = false;
    }
});

// ============================================================================
// MANEJADORES DE EVENTOS - EDITAR USUARIO
// ============================================================================

/**
 * Maneja el clic en el botón de editar
 * Requirement: 4.5
 */
function handleEditarClick(event) {
    const userId = event.target.dataset.userid;
    const usuario = appState.usuarios.find(u => u.userId === userId);
    
    if (!usuario) {
        mostrarMensaje('error', 'Usuario no encontrado', 'Error');
        return;
    }
    
    // Guardar usuario que se está editando
    appState.usuarioEditando = usuario;
    
    // Llenar formulario de edición
    inputEditarUserIdOriginal.value = usuario.userId;
    inputEditarUserId.value = usuario.userId;
    inputEditarDocumento.value = usuario.documento;
    inputEditarNombre.value = usuario.nombre;
    
    // Abrir modal
    abrirModal();
}

/**
 * Maneja el envío del formulario de editar usuario
 * Requirement: 4.5
 */
formEditar.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const userId = inputEditarUserIdOriginal.value;
    const documento = inputEditarDocumento.value.trim();
    const nombre = inputEditarNombre.value.trim();
    
    // Validación en cliente (Requirement: 4.5)
    if (!documento || !nombre) {
        mostrarMensaje('error', 'Todos los campos son requeridos', 'Validación');
        return;
    }
    
    // Deshabilitar botón
    btnGuardarEditar.disabled = true;
    
    try {
        // Editar usuario
        await editarUsuario(userId, {
            documento: documento,
            nombre: nombre
        });
        
        // Cerrar modal
        cerrarModal();
        
        // Mostrar mensaje de éxito
        mostrarMensaje('exito', `Usuario ${nombre} actualizado exitosamente`, 'Usuario actualizado');
        
        // Recargar lista de usuarios
        await cargarYMostrarUsuarios();
        
    } catch (error) {
        mostrarMensaje('error', error.message || 'No se pudo actualizar el usuario', 'Error');
    } finally {
        btnGuardarEditar.disabled = false;
    }
});

// ============================================================================
// MANEJADORES DE EVENTOS - ELIMINAR USUARIO
// ============================================================================

/**
 * Maneja el clic en el botón de eliminar
 * Requirement: 4.5
 */
function handleEliminarClick(event) {
    const userId = event.target.dataset.userid;
    const usuario = appState.usuarios.find(u => u.userId === userId);
    
    if (!usuario) {
        mostrarMensaje('error', 'Usuario no encontrado', 'Error');
        return;
    }
    
    // Confirmar eliminación
    const confirmar = confirm(`¿Estás seguro de que deseas eliminar al usuario ${usuario.nombre}?\n\nEsta acción no se puede deshacer.`);
    
    if (!confirmar) {
        return;
    }
    
    // Eliminar usuario
    eliminarUsuarioConfirmado(userId, usuario.nombre);
}

/**
 * Elimina un usuario después de confirmación
 * Requirement: 4.5
 */
async function eliminarUsuarioConfirmado(userId, nombre) {
    limpiarMensajes();
    
    try {
        // Eliminar usuario
        await eliminarUsuario(userId);
        
        // Mostrar mensaje de éxito
        mostrarMensaje('exito', `Usuario ${nombre} eliminado exitosamente`, 'Usuario eliminado');
        
        // Recargar lista de usuarios
        await cargarYMostrarUsuarios();
        
    } catch (error) {
        mostrarMensaje('error', error.message || 'No se pudo eliminar el usuario', 'Error');
    }
}

// ============================================================================
// MANEJADORES DE EVENTOS - MODAL
// ============================================================================

// Cerrar modal con botón X
btnCerrarModal.addEventListener('click', cerrarModal);

// Cerrar modal con botón Cancelar
btnCancelarEditar.addEventListener('click', cerrarModal);

// Cerrar modal al hacer clic fuera del contenido
modalEditar.addEventListener('click', (event) => {
    if (event.target === modalEditar) {
        cerrarModal();
    }
});

// ============================================================================
// MANEJADORES DE EVENTOS - EXPORTAR CSV
// ============================================================================

/**
 * Exporta la lista de usuarios a CSV
 * Requirement: 4.3
 */
btnExportar.addEventListener('click', () => {
    if (appState.usuarios.length === 0) {
        mostrarMensaje('warning', 'No hay usuarios para exportar', 'Lista vacía');
        return;
    }
    
    // Generar CSV
    const csv = generarCSV(appState.usuarios);
    
    // Crear blob y descargar
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `usuarios_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
    URL.revokeObjectURL(url);
    
    mostrarMensaje('exito', 'Archivo CSV descargado exitosamente', 'Exportación exitosa');
});

/**
 * Exporta las asistencias confirmadas a CSV
 * Requirement: 4.7
 */
btnExportarAsistencias.addEventListener('click', async () => {
    if (appState.asistencias.length === 0) {
        mostrarMensaje('warning', 'No hay asistencias confirmadas para exportar', 'Lista vacía');
        return;
    }
    
    try {
        const token = obtenerToken();
        if (!token) {
            redirigirALogin();
            return;
        }
        
        // Descargar CSV usando fetch con token
        const response = await fetchAutenticado(`${API_BASE_URL}/api/asistencias/exportar-csv`, {
            method: 'GET'
        });
        
        if (!response.ok) {
            throw new Error('Error al exportar asistencias');
        }
        
        // Obtener el blob del CSV
        const blob = await response.blob();
        
        // Crear URL temporal y descargar
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `asistencias_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
        
        mostrarMensaje('exito', 'Archivo CSV de asistencias descargado exitosamente', 'Exportación exitosa');
        
    } catch (error) {
        console.error('Error al exportar asistencias:', error);
        mostrarMensaje('error', 'Error al exportar asistencias. Por favor intenta nuevamente.', 'Error');
    }
});

/**
 * Genera contenido CSV desde array de usuarios
 * Requirement: 4.3
 * 
 * @param {Array} usuarios - Array de usuarios
 * @returns {string} - Contenido CSV
 */
function generarCSV(usuarios) {
    // Header
    let csv = 'userId,documento,nombre\n';
    
    // Filas
    usuarios.forEach(usuario => {
        // Escapar campos que contengan comas o comillas
        const userId = escaparCampoCSV(usuario.userId);
        const documento = escaparCampoCSV(usuario.documento);
        const nombre = escaparCampoCSV(usuario.nombre);
        
        csv += `${userId},${documento},${nombre}\n`;
    });
    
    return csv;
}

/**
 * Escapa un campo para CSV
 * 
 * @param {string} campo - Campo a escapar
 * @returns {string}
 */
function escaparCampoCSV(campo) {
    // Si contiene coma, comilla o salto de línea, envolver en comillas
    if (campo.includes(',') || campo.includes('"') || campo.includes('\n')) {
        // Duplicar comillas internas
        return `"${campo.replace(/"/g, '""')}"`;
    }
    return campo;
}

// ============================================================================
// IMPORTACIÓN MASIVA DE USUARIOS (CSV)
// ============================================================================

/**
 * Importa usuarios desde un archivo CSV
 * 
 * @param {string} csvContent - Contenido del archivo CSV
 * @returns {Promise<Object>} - Resultado de la importación
 */
async function importarUsuariosCSV(csvContent) {
    try {
        const response = await fetchAutenticado(`${API_BASE_URL}/api/usuarios/importar-csv`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ csv_content: csvContent })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.mensaje || 'Error al importar usuarios');
        }
        
        return data;
        
    } catch (error) {
        console.error('Error al importar usuarios:', error);
        throw error;
    }
}

/**
 * Lee el contenido de un archivo
 * 
 * @param {File} file - Archivo a leer
 * @returns {Promise<string>} - Contenido del archivo
 */
function leerArchivoCSV(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        
        reader.onload = (e) => {
            resolve(e.target.result);
        };
        
        reader.onerror = (e) => {
            reject(new Error('Error al leer el archivo'));
        };
        
        reader.readAsText(file, 'UTF-8');
    });
}

/**
 * Maneja el evento de importación CSV
 */
btnImportarCsv.addEventListener('click', async () => {
    // Verificar que se haya seleccionado un archivo
    if (!inputCsvFile.files || inputCsvFile.files.length === 0) {
        mostrarMensaje('warning', 'Por favor selecciona un archivo CSV', 'Archivo requerido');
        return;
    }
    
    const file = inputCsvFile.files[0];
    
    // Verificar extensión
    if (!file.name.endsWith('.csv')) {
        mostrarMensaje('error', 'El archivo debe tener extensión .csv', 'Formato inválido');
        return;
    }
    
    // Deshabilitar botón
    btnImportarCsv.disabled = true;
    btnImportarCsv.textContent = 'Importando...';
    
    // Ocultar resultado anterior
    resultadoImportacion.style.display = 'none';
    limpiarMensajes();
    
    try {
        // Leer archivo
        const csvContent = await leerArchivoCSV(file);
        
        // Importar usuarios
        const resultado = await importarUsuariosCSV(csvContent);
        
        // Mostrar resultado
        if (resultado.success) {
            // Mostrar resumen
            let mensajeDetalle = `Se procesaron ${resultado.agregados + resultado.omitidos + resultado.errores} usuario(s):\n`;
            mensajeDetalle += `✅ ${resultado.agregados} agregado(s)\n`;
            
            if (resultado.omitidos > 0) {
                mensajeDetalle += `⚠️ ${resultado.omitidos} omitido(s) (ya existían)\n`;
            }
            
            if (resultado.errores > 0) {
                mensajeDetalle += `❌ ${resultado.errores} error(es)`;
            }
            
            resultadoImportacionTexto.textContent = mensajeDetalle;
            resultadoImportacion.style.display = 'block';
            
            // Mostrar mensaje de éxito
            mostrarMensaje('exito', resultado.mensaje, 'Importación completada');
            
            // Limpiar input
            inputCsvFile.value = '';
            
            // Recargar lista de usuarios
            await cargarYMostrarUsuarios();
            
            // Ocultar resultado después de 10 segundos
            setTimeout(() => {
                resultadoImportacion.style.display = 'none';
            }, 10000);
        } else {
            mostrarMensaje('error', resultado.mensaje, 'Error en la importación');
        }
        
    } catch (error) {
        console.error('Error al importar CSV:', error);
        mostrarMensaje('error', error.message || 'Error al importar el archivo CSV', 'Error');
    } finally {
        // Rehabilitar botón
        btnImportarCsv.disabled = false;
        btnImportarCsv.textContent = '📤 Importar CSV';
    }
});

// ============================================================================
// IMPORTACIÓN DESDE PDF DE NÓMINA
// ============================================================================

/**
 * Importa usuarios desde archivos PDF de nómina
 */
const inputPdfFiles = document.getElementById('input-pdf-files');
const btnImportarPdf = document.getElementById('btn-importar-pdf');
const resultadoImportacionPdf = document.getElementById('resultado-importacion-pdf');
const resultadoImportacionPdfTexto = document.getElementById('resultado-importacion-pdf-texto');
const resultadoImportacionPdfDetalles = document.getElementById('resultado-importacion-pdf-detalles');

btnImportarPdf.addEventListener('click', async () => {
    // Verificar que se hayan seleccionado archivos
    if (!inputPdfFiles.files || inputPdfFiles.files.length === 0) {
        mostrarMensaje('warning', 'Por favor selecciona uno o más archivos PDF', 'Archivo requerido');
        return;
    }
    
    const archivos = inputPdfFiles.files;
    
    // Verificar extensiones
    for (let i = 0; i < archivos.length; i++) {
        if (!archivos[i].name.toLowerCase().endsWith('.pdf')) {
            mostrarMensaje('error', `El archivo "${archivos[i].name}" no es un PDF válido`, 'Formato inválido');
            return;
        }
    }
    
    // Deshabilitar botón
    btnImportarPdf.disabled = true;
    btnImportarPdf.textContent = 'Importando...';
    
    // Ocultar resultado anterior
    resultadoImportacionPdf.style.display = 'none';
    limpiarMensajes();
    
    try {
        // Crear FormData con los archivos
        const formData = new FormData();
        for (let i = 0; i < archivos.length; i++) {
            formData.append('archivos', archivos[i]);
        }
        
        // Enviar al backend
        const token = obtenerToken();
        if (!token) {
            redirigirALogin();
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/api/usuarios/importar-pdf`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });
        
        // Manejar token expirado
        if (response.status === 401) {
            localStorage.removeItem('admin_token');
            redirigirALogin();
            return;
        }
        
        const resultado = await response.json();
        
        if (!response.ok) {
            throw new Error(resultado.mensaje || 'Error al importar PDFs');
        }
        
        if (resultado.success) {
            // Mostrar resumen
            resultadoImportacionPdfTexto.textContent = resultado.mensaje;
            
            // Mostrar detalles por archivo
            let detallesHtml = '';
            if (resultado.detalles_por_archivo && resultado.detalles_por_archivo.length > 0) {
                detallesHtml = '<ul style="margin: 0; padding-left: 20px;">';
                resultado.detalles_por_archivo.forEach(detalle => {
                    const icono = detalle.estado === 'exitoso' ? '✅' : '❌';
                    detallesHtml += `<li>${icono} <strong>${detalle.archivo}</strong>: ${detalle.mensaje}`;
                    if (detalle.empleados_encontrados) {
                        detallesHtml += ` (${detalle.empleados_encontrados} encontrados en PDF)`;
                    }
                    detallesHtml += '</li>';
                });
                detallesHtml += '</ul>';
            }
            resultadoImportacionPdfDetalles.innerHTML = detallesHtml;
            
            resultadoImportacionPdf.style.display = 'block';
            
            // Mostrar mensaje de éxito
            mostrarMensaje('exito', resultado.mensaje, 'Importación PDF completada');
            
            // Limpiar input
            inputPdfFiles.value = '';
            
            // Recargar lista de usuarios
            await cargarYMostrarUsuarios();
            
            // Ocultar resultado después de 15 segundos
            setTimeout(() => {
                resultadoImportacionPdf.style.display = 'none';
            }, 15000);
        } else {
            mostrarMensaje('error', resultado.mensaje, 'Error en la importación');
        }
        
    } catch (error) {
        console.error('Error al importar PDF:', error);
        mostrarMensaje('error', error.message || 'Error al importar los archivos PDF', 'Error');
    } finally {
        // Rehabilitar botón
        btnImportarPdf.disabled = false;
        btnImportarPdf.textContent = '📄 Importar PDF(s)';
    }
});

// ============================================================================
// REINICIO DE ASISTENCIAS
// ============================================================================

/**
 * Reinicia todas las asistencias confirmadas
 * 
 * @returns {Promise<Object>} - Resultado del reinicio
 */
async function reiniciarAsistencias() {
    try {
        const response = await fetchAutenticado(`${API_BASE_URL}/api/asistencias/reiniciar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.mensaje || 'Error al reiniciar asistencias');
        }
        
        return data;
        
    } catch (error) {
        console.error('Error al reiniciar asistencias:', error);
        throw error;
    }
}

/**
 * Muestra la advertencia de confirmación para reiniciar asistencias
 */
btnReiniciarAsistencias.addEventListener('click', () => {
    // Mostrar advertencia
    advertenciaReinicio.style.display = 'block';
    
    // Scroll a la advertencia
    advertenciaReinicio.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
});

/**
 * Cancela el reinicio de asistencias
 */
btnCancelarReinicio.addEventListener('click', () => {
    // Ocultar advertencia
    advertenciaReinicio.style.display = 'none';
});

/**
 * Confirma y ejecuta el reinicio de asistencias
 */
btnConfirmarReinicio.addEventListener('click', async () => {
    // Deshabilitar botones
    btnConfirmarReinicio.disabled = true;
    btnCancelarReinicio.disabled = true;
    btnConfirmarReinicio.textContent = 'Eliminando...';
    
    limpiarMensajes();
    
    try {
        // Reiniciar asistencias
        const resultado = await reiniciarAsistencias();
        
        if (resultado.success) {
            // Mostrar mensaje de éxito
            mostrarMensaje(
                'exito', 
                resultado.mensaje, 
                'Asistencias reiniciadas'
            );
            
            // Ocultar advertencia
            advertenciaReinicio.style.display = 'none';
            
            // Recargar lista de asistencias
            await cargarYMostrarAsistencias();
        } else {
            mostrarMensaje('error', resultado.mensaje, 'Error al reiniciar');
        }
        
    } catch (error) {
        console.error('Error al reiniciar asistencias:', error);
        mostrarMensaje(
            'error', 
            error.message || 'Error al reiniciar las asistencias', 
            'Error'
        );
    } finally {
        // Rehabilitar botones
        btnConfirmarReinicio.disabled = false;
        btnCancelarReinicio.disabled = false;
        btnConfirmarReinicio.textContent = 'Sí, eliminar todas las asistencias';
    }
});

// ============================================================================
// ELIMINAR TODOS LOS USUARIOS
// ============================================================================

/**
 * Elimina todos los usuarios autorizados
 */
async function eliminarTodosUsuarios() {
    try {
        const response = await fetchAutenticado(`${API_BASE_URL}/api/usuarios/eliminar-todos`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.mensaje || 'Error al eliminar usuarios');
        }
        
        return data;
        
    } catch (error) {
        console.error('Error al eliminar todos los usuarios:', error);
        throw error;
    }
}

/**
 * Maneja el click en el botón de eliminar todos los usuarios
 */
btnEliminarTodosUsuarios.addEventListener('click', async () => {
    // Confirmar acción
    const confirmacion = confirm(
        `⚠️ ¿Estás seguro que deseas eliminar TODOS los usuarios autorizados?\n\n` +
        `Esta acción eliminará ${appState.usuarios.length} usuarios de forma permanente.\n\n` +
        `Se recomienda exportar el CSV antes de continuar.`
    );
    
    if (!confirmacion) {
        return;
    }
    
    // Segunda confirmación
    const segundaConfirmacion = confirm(
        `⚠️ ÚLTIMA CONFIRMACIÓN\n\n` +
        `Esta acción NO se puede deshacer.\n\n` +
        `¿Realmente deseas eliminar todos los usuarios?`
    );
    
    if (!segundaConfirmacion) {
        return;
    }
    
    // Deshabilitar botón
    btnEliminarTodosUsuarios.disabled = true;
    btnEliminarTodosUsuarios.textContent = 'Eliminando...';
    
    limpiarMensajes();
    
    try {
        // Eliminar todos los usuarios
        const resultado = await eliminarTodosUsuarios();
        
        if (resultado.success) {
            // Mostrar mensaje de éxito
            mostrarMensaje(
                'exito', 
                resultado.mensaje, 
                'Usuarios eliminados'
            );
            
            // Recargar lista de usuarios
            await cargarYMostrarUsuarios();
        } else {
            mostrarMensaje('error', resultado.mensaje, 'Error al eliminar');
        }
        
    } catch (error) {
        console.error('Error al eliminar todos los usuarios:', error);
        mostrarMensaje(
            'error', 
            error.message || 'Error al eliminar los usuarios', 
            'Error'
        );
    } finally {
        // Rehabilitar botón
        btnEliminarTodosUsuarios.disabled = false;
        btnEliminarTodosUsuarios.textContent = '🗑️ Eliminar Todos los Usuarios';
    }
});

// ============================================================================
// CAMBIO DE CONTRASEÑA
// ============================================================================

/**
 * Abre el modal de cambiar contraseña
 */
function abrirModalCambiarPassword() {
    const modal = document.getElementById('modal-cambiar-password');
    const form = document.getElementById('form-cambiar-password');
    
    // Limpiar formulario
    form.reset();
    
    // Mostrar modal
    modal.classList.add('activo');
    
    // Focus en primer campo
    document.getElementById('password-actual').focus();
}

/**
 * Cierra el modal de cambiar contraseña
 */
function cerrarModalCambiarPassword() {
    const modal = document.getElementById('modal-cambiar-password');
    modal.classList.remove('activo');
}

/**
 * Maneja el envío del formulario de cambio de contraseña
 */
async function manejarCambioPassword(event) {
    event.preventDefault();
    
    const btnGuardar = document.getElementById('btn-guardar-password');
    btnGuardar.disabled = true;
    btnGuardar.textContent = 'Cambiando...';
    
    try {
        const passwordActual = document.getElementById('password-actual').value;
        const passwordNueva = document.getElementById('password-nueva').value;
        const passwordConfirmar = document.getElementById('password-confirmar').value;
        
        // Validar que las contraseñas coincidan
        if (passwordNueva !== passwordConfirmar) {
            mostrarMensaje('Las contraseñas nuevas no coinciden', 'error');
            return;
        }
        
        // Validar longitud mínima
        if (passwordNueva.length < 6) {
            mostrarMensaje('La contraseña debe tener al menos 6 caracteres', 'error');
            return;
        }
        
        const response = await fetchAutenticado(`${API_BASE_URL}/api/admin/cambiar-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                passwordActual,
                passwordNueva
            })
        });
        
        const resultado = await response.json();
        
        if (!response.ok) {
            throw new Error(resultado.mensaje || 'Error al cambiar contraseña');
        }
        
        mostrarMensaje('✓ ' + resultado.mensaje, 'exito');
        cerrarModalCambiarPassword();
        
        // Esperar 2 segundos y redirigir al login
        setTimeout(() => {
            localStorage.removeItem('admin_token');
            redirigirALogin();
        }, 2000);
        
    } catch (error) {
        console.error('Error al cambiar contraseña:', error);
        mostrarMensaje(`Error: ${error.message}`, 'error');
    } finally {
        btnGuardar.disabled = false;
        btnGuardar.textContent = 'Cambiar Contraseña';
    }
}


// ============================================================================
// CONFIGURACIÓN DE UBICACIÓN
// ============================================================================

/**
 * Carga y muestra la configuración actual de ubicación
 */
async function cargarConfiguracionUbicacion() {
    try {
        const response = await fetchAutenticado(`${API_BASE_URL}/api/configuracion`);
        
        if (!response.ok) {
            throw new Error('Error al cargar configuración');
        }
        
        const config = await response.json();
        
        // Actualizar campos del formulario
        document.getElementById('config-latitud').value = config.ubicacionAsamblea.latitud;
        document.getElementById('config-longitud').value = config.ubicacionAsamblea.longitud;
        document.getElementById('config-radio').value = config.radioPermitido;
        
        // Actualizar información actual
        document.getElementById('ubicacion-actual-lat').textContent = config.ubicacionAsamblea.latitud;
        document.getElementById('ubicacion-actual-lon').textContent = config.ubicacionAsamblea.longitud;
        document.getElementById('ubicacion-actual-radio').textContent = config.radioPermitido;
        
    } catch (error) {
        console.error('Error al cargar configuración:', error);
        mostrarMensaje('Error al cargar configuración de ubicación', 'error');
    }
}

/**
 * Guarda la nueva configuración de ubicación
 */
async function guardarConfiguracionUbicacion(event) {
    event.preventDefault();
    
    const btnGuardar = document.getElementById('btn-guardar-ubicacion');
    btnGuardar.disabled = true;
    btnGuardar.textContent = 'Guardando...';
    
    try {
        const latitud = parseFloat(document.getElementById('config-latitud').value);
        const longitud = parseFloat(document.getElementById('config-longitud').value);
        const radioPermitido = parseInt(document.getElementById('config-radio').value);
        
        // Validar rangos
        if (latitud < -90 || latitud > 90) {
            throw new Error('La latitud debe estar entre -90 y 90');
        }
        
        if (longitud < -180 || longitud > 180) {
            throw new Error('La longitud debe estar entre -180 y 180');
        }
        
        if (radioPermitido < 1) {
            throw new Error('El radio debe ser mayor a 0');
        }
        
        const response = await fetchAutenticado(`${API_BASE_URL}/api/admin/configuracion`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                latitud,
                longitud,
                radioPermitido
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al guardar configuración');
        }
        
        const resultado = await response.json();
        
        // Actualizar información actual
        document.getElementById('ubicacion-actual-lat').textContent = latitud;
        document.getElementById('ubicacion-actual-lon').textContent = longitud;
        document.getElementById('ubicacion-actual-radio').textContent = radioPermitido;
        
        mostrarMensaje('✓ Configuración de ubicación actualizada exitosamente', 'exito');
        
    } catch (error) {
        console.error('Error al guardar configuración:', error);
        mostrarMensaje(`Error: ${error.message}`, 'error');
    } finally {
        btnGuardar.disabled = false;
        btnGuardar.textContent = '💾 Guardar Ubicación';
    }
}


// ============================================================================
// INICIALIZACIÓN
// ============================================================================

/**
 * Inicializa la aplicación cuando el DOM está listo
 */
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Interfaz administrativa iniciada');
    
    // Verificar autenticación primero
    const autenticado = await verificarAutenticacion();
    if (!autenticado) {
        return; // Ya redirigió a login
    }
    
    // Agregar event listener al botón de cerrar sesión
    const btnCerrarSesion = document.getElementById('btn-cerrar-sesion');
    if (btnCerrarSesion) {
        btnCerrarSesion.addEventListener('click', async () => {
            if (confirm('¿Estás seguro que deseas cerrar sesión?')) {
                await cerrarSesion();
            }
        });
    }
    
    // Agregar event listener al botón de cambiar contraseña
    const btnCambiarPassword = document.getElementById('btn-cambiar-password');
    if (btnCambiarPassword) {
        btnCambiarPassword.addEventListener('click', abrirModalCambiarPassword);
    }
    
    // Agregar event listeners al modal de cambiar contraseña
    const btnCerrarModalPassword = document.getElementById('btn-cerrar-modal-password');
    const btnCancelarPassword = document.getElementById('btn-cancelar-password');
    const formCambiarPassword = document.getElementById('form-cambiar-password');
    
    if (btnCerrarModalPassword) {
        btnCerrarModalPassword.addEventListener('click', cerrarModalCambiarPassword);
    }
    
    if (btnCancelarPassword) {
        btnCancelarPassword.addEventListener('click', cerrarModalCambiarPassword);
    }
    
    if (formCambiarPassword) {
        formCambiarPassword.addEventListener('submit', manejarCambioPassword);
    }
    
    // Cerrar modal de cambiar contraseña al hacer clic fuera
    const modalCambiarPassword = document.getElementById('modal-cambiar-password');
    if (modalCambiarPassword) {
        modalCambiarPassword.addEventListener('click', (e) => {
            if (e.target === modalCambiarPassword) {
                cerrarModalCambiarPassword();
            }
        });
    }
    
    // Agregar event listener al formulario de configuración de ubicación
    const formConfiguracion = document.getElementById('form-configuracion-ubicacion');
    if (formConfiguracion) {
        formConfiguracion.addEventListener('submit', guardarConfiguracionUbicacion);
    }
    
    // Cargar usuarios al inicio
    cargarYMostrarUsuarios();
    
    // Cargar asistencias al inicio
    cargarYMostrarAsistencias();
    
    // Cargar configuración de ubicación
    cargarConfiguracionUbicacion();
    
    // Event listeners para filtros de usuarios
    ['filtro-userId', 'filtro-documento', 'filtro-nombre'].forEach(id => {
        const input = document.getElementById(id);
        if (input) {
            input.addEventListener('input', () => renderizarTablaUsuarios());
        }
    });
    
    // Event listeners para filtros de asistencias
    ['filtro-asist-nombre', 'filtro-asist-userId', 'filtro-asist-fecha', 'filtro-asist-ubicacion'].forEach(id => {
        const input = document.getElementById(id);
        if (input) {
            input.addEventListener('input', () => renderizarTablaAsistencias());
        }
    });
    
    // Focus en el primer campo
    inputNuevoUserId.focus();
});
