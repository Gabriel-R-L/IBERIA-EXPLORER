// Cambio de imagen de perfil
document.addEventListener('DOMContentLoaded', function () {
    const profileImage = document.getElementById('profileImage');
    const fileInput = document.getElementById('fileInput');

    profileImage.onclick = function () {
        fileInput.click();
    };

    fileInput.onchange = function () {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                profileImage.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    };
});
