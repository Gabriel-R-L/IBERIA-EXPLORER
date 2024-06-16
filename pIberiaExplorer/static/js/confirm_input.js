// Cerrar sesión y borrar cuenta
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.confirmation-button').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            var actionType = this.dataset.action;
            var url = this.dataset.url;
            var confirmButtonId = this.dataset.confirmButtonId;
            var cancelButtonId = this.dataset.cancelButtonId;
            var redirectUrl = this.dataset.redirectUrl;

            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.onreadystatechange = function () {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var response = JSON.parse(xhr.responseText);
                    var modalDiv = document.createElement('div');
                    modalDiv.innerHTML = response.html;
                    document.body.appendChild(modalDiv);
                    document.getElementById(`${actionType}-confirmation-modal`).style.display = 'block';

                    document.getElementById(confirmButtonId).addEventListener('click', function () {
                        window.location.href = redirectUrl;
                    });

                    document.getElementById(cancelButtonId).addEventListener('click', function () {
                        document.getElementById(`${actionType}-confirmation-modal`).style.display = 'none';
                    });
                }
            };
            xhr.send();
        });
    });
});
