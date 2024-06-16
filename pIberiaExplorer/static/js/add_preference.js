// Hecho con JQuery para deshabilitar el botón de guardar si no se ha seleccionado un atributo de plan
$(document).ready(function () {
    function checkSelectedOption() {
        var select = document.getElementById("id_atributo_plan");
        var selectedOption = select.options[select.selectedIndex].value;
        if (selectedOption == "None" || selectedOption == "") {
            $("#saveButton").prop("disabled", true);
        } else {
            $("#saveButton").prop("disabled", false);
        }
    }

    // Check the initial state
    checkSelectedOption();

    // Attach change event listener
    $("#id_atributo_plan").change(function () {
        checkSelectedOption();
    });
});