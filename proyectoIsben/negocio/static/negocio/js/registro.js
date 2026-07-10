document.addEventListener("DOMContentLoaded", function () {
    var rolInputs = document.querySelectorAll('input[name="rol"]');
    var rolFieldsets = document.querySelectorAll(".rol-fields");

    function actualizarCamposVisibles() {
        var seleccionado = document.querySelector('input[name="rol"]:checked');
        var rol = seleccionado ? seleccionado.value : null;

        rolFieldsets.forEach(function (fieldset) {
            fieldset.classList.toggle("hidden", fieldset.dataset.rol !== rol);
        });
    }

    rolInputs.forEach(function (input) {
        input.addEventListener("change", actualizarCamposVisibles);
    });

    actualizarCamposVisibles();
});
