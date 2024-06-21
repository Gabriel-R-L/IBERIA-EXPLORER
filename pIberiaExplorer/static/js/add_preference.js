// Hecho con JQuery para deshabilitar el botón de guardar si no se ha seleccionado un atributo de plan
$(document).ready(function () {
    // Función para verificar si se ha seleccionado una opción válida
    function checkSelectedOption() {
        // Obtener el elemento select con el id "id_atributo_plan"
        var select = document.getElementById("id_atributo_plan");
        // Obtener el valor de la opción seleccionada
        var selectedOption = select.options[select.selectedIndex].value;

        // Verificar si la opción seleccionada es "None" o está vacía
        if (selectedOption == "None" || selectedOption == "") {
            // Si es así, deshabilitar el botón de guardar
            $("#saveButton").prop("disabled", true);
        } else {
            // Si se seleccionó una opción válida, habilitar el botón de guardar
            $("#saveButton").prop("disabled", false);
        }
    }

    // Verificar el estado inicial al cargar el documento
    checkSelectedOption();

    // Adjuntar un evento de cambio al elemento select con id "id_atributo_plan"
    $("#id_atributo_plan").change(function () {
        // Llamar a la función checkSelectedOption cuando cambie la selección
        checkSelectedOption();
    });
});