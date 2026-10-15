// ============================================================
// main.js - Interacciones mínimas del Salón
// Academia Horizonte - Sistema de Certificados
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    
    // Resaltar fila al hacer hover (feedback visual)
    const filas = document.querySelectorAll('.tabla-certificados tbody tr');
    filas.forEach(fila => {
        fila.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.01)';
            this.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
            this.style.zIndex = '10';
        });
        fila.addEventListener('mouseleave', function() {
            this.style.transform = 'none';
            this.style.boxShadow = 'none';
            this.style.zIndex = 'auto';
        });
    });
    
    // Atajo de teclado: Enter en el select para aplicar filtro (ya lo hace onchange)
    const selectPrograma = document.getElementById('programa');
    if (selectPrograma) {
        selectPrograma.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                this.form.submit();
            }
        });
    }
    
    // Tooltip simple para badges fantasma
    const badgesFantasma = document.querySelectorAll('.badge-fantasma');
    badgesFantasma.forEach(badge => {
        badge.title = 'Esta identificación no existe en el Maestro de Estudiantes. No emitir certificado.';
    });
    
    console.log('🎓 Academia Horizonte - Salón cargado correctamente');
    console.log('💡 La Cocina calcula, el Salón muestra');
});

// Función auxiliar para imprimir la tabla (futuro: certificado individual)
function imprimirTabla() {
    window.print();
}