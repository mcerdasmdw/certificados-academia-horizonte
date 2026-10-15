document.addEventListener("DOMContentLoaded", () => {
    const programSelect = document.querySelector("#programa");
    const typeSelect = document.querySelector("#tipo");
    const searchInput = document.querySelector("#search");
    const clearButton = document.querySelector("#clearFilters");
    const rows = [...document.querySelectorAll("[data-result-row]")];
    const visibleCount = document.querySelector("#visibleCount");
    const emptyState = document.querySelector("#emptyState");

    // El programa se procesa en Flask para mantener una URL compartible.
    programSelect?.addEventListener("change", () => programSelect.form.submit());

    // Los filtros rápidos trabajan en el navegador sobre los datos ya calculados.
    function filtrarResultados() {
        const texto = searchInput.value.trim().toLocaleLowerCase("es");
        const tipo = typeSelect.value;
        let visibles = 0;

        rows.forEach((fila) => {
            const coincideTexto = !texto
                || fila.dataset.nombre.includes(texto)
                || fila.dataset.identificacion.includes(texto);
            const coincideTipo = tipo === "todos" || fila.dataset.tipo === tipo;
            const mostrar = coincideTexto && coincideTipo;

            fila.hidden = !mostrar;
            if (mostrar) visibles += 1;
        });

        visibleCount.textContent = visibles;
        emptyState.hidden = visibles !== 0;
    }

    typeSelect?.addEventListener("change", filtrarResultados);
    searchInput?.addEventListener("input", filtrarResultados);
    clearButton?.addEventListener("click", () => {
        typeSelect.value = "todos";
        searchInput.value = "";
        filtrarResultados();
        searchInput.focus();
    });
});
