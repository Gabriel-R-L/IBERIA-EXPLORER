// Cambio de imagen de perfil
// Espera a que el documento HTML se cargue completamente
document.addEventListener('DOMContentLoaded', function () {
    // Obtiene la referencia al elemento de imagen de perfil y al input de tipo archivo
    const profileImage = document.getElementById('profileImage');
    const fileInput = document.getElementById('fileInput');

    // Cuando se hace clic en la imagen de perfil, activa el input de tipo archivo
    profileImage.onclick = function () {
        fileInput.click(); // Simula un clic en el input de tipo archivo
    };

    // Cuando cambia el contenido del input de tipo archivo (selecciona una nueva imagen)
    fileInput.onchange = function () {
        const file = fileInput.files[0]; // Obtiene el archivo seleccionado

        // Verifica si se seleccionó un archivo
        if (file) {
            const reader = new FileReader(); // Crea un objeto FileReader

            // Cuando se completa la carga del archivo
            reader.onload = function (e) {
                profileImage.src = e.target.result; // Asigna la URL de la imagen cargada al src de la imagen de perfil
            };

            // Lee el contenido del archivo como una URL de datos (data URL)
            reader.readAsDataURL(file);
        }
    };
});