document.addEventListener("DOMContentLoaded", function () {
    var rolInputs = document.querySelectorAll('input[name="rol"]');
    var rolFieldsets = document.querySelectorAll(".rol-fields");

    function actualizarCamposVisibles() {
        var seleccionado = document.querySelector('input[name="rol"]:checked');
        var rol = seleccionado ? seleccionado.value : null;

        rolFieldsets.forEach(function (fieldset) {
            var visible = fieldset.dataset.rol === rol;
            fieldset.classList.toggle("hidden", !visible);
            if (visible) {
                fieldset.dispatchEvent(new CustomEvent("campo-visible"));
            }
        });
    }

    rolInputs.forEach(function (input) {
        input.addEventListener("change", actualizarCamposVisibles);
    });

    actualizarCamposVisibles();
});
