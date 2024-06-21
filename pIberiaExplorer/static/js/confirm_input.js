// Cerrar sesión y borrar cuenta con AJAX para evitar recargar la página
// Espera a que el documento HTML se cargue completamente
document.addEventListener('DOMContentLoaded', function () {
    // Selecciona todos los elementos con la clase 'confirmation-button'
    document.querySelectorAll('.confirmation-button').forEach(button => {
        // Agrega un evento 'click' a cada botón encontrado
        button.addEventListener('click', function (event) {
            event.preventDefault(); // Evita el comportamiento por defecto del enlace

            // Obtiene los datos personalizados de los atributos data-* del botón
            var actionType = this.dataset.action;
            var url = this.dataset.url;
            var confirmButtonId = this.dataset.confirmButtonId;
            var cancelButtonId = this.dataset.cancelButtonId;
            var redirectUrl = this.dataset.redirectUrl;

            // Crea una nueva solicitud XMLHttpRequest
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true); // Abre una solicitud GET asíncrona a la URL especificada
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest'); // Configura la cabecera X-Requested-With

            // Define el evento que se ejecuta cuando cambia el estado de la solicitud
            xhr.onreadystatechange = function () {
                if (xhr.readyState == 4 && xhr.status == 200) { // Comprueba si la solicitud se ha completado correctamente
                    // Parsea la respuesta JSON recibida del servidor
                    var response = JSON.parse(xhr.responseText);

                    // Crea un nuevo elemento div para mostrar el contenido HTML recibido
                    var modalDiv = document.createElement('div');
                    modalDiv.innerHTML = response.html;
                    document.body.appendChild(modalDiv); // Añade el div al cuerpo del documento

                    // Muestra el modal de confirmación según el tipo de acción (cerrar sesión o borrar cuenta)
                    document.getElementById(`${actionType}-confirmation-modal`).style.display = 'block';

                    // Agrega un evento 'click' al botón de confirmación dentro del modal
                    document.getElementById(confirmButtonId).addEventListener('click', function () {
                        window.location.href = redirectUrl; // Redirige a la URL de redirección
                    });

                    // Agrega un evento 'click' al botón de cancelar dentro del modal
                    document.getElementById(cancelButtonId).addEventListener('click', function () {
                        document.getElementById(`${actionType}-confirmation-modal`).style.display = 'none'; // Oculta el modal de confirmación
                    });
                }
            };

            xhr.send(); // Envía la solicitud XMLHttpRequest
        });
    });
});