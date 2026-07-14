document.addEventListener("DOMContentLoaded", function () {
    var tabla = document.getElementById("tabla-detalles");
    var plantilla = document.getElementById("plantilla-detalle");
    var boton = document.getElementById("btn-agregar-producto");
    if (!tabla || !plantilla || !boton) return;

    var cuerpo = tabla.querySelector("tbody");
    var totalFormsInput = document.querySelector('input[name="detalles-TOTAL_FORMS"]');

    boton.addEventListener("click", function () {
        var indice = parseInt(totalFormsInput.value, 10);
        var html = plantilla.innerHTML.replace(/__prefix__/g, indice);

        var temporal = document.createElement("tbody");
        temporal.innerHTML = html.trim();
        cuerpo.appendChild(temporal.querySelector("tr"));

        totalFormsInput.value = indice + 1;
    });

    cuerpo.addEventListener("click", function (evento) {
        if (!evento.target.classList.contains("btn-quitar-producto")) return;

        var fila = evento.target.closest("tr");
        var checkboxEliminar = fila.querySelector('input[type="checkbox"][name$="-DELETE"]');

        if (checkboxEliminar) {
            checkboxEliminar.checked = true;
            fila.style.display = "none";
        } else {
            fila.remove();
        }
    });
});
