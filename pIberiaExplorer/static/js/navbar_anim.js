// Espera a que el documento HTML se cargue completamente
document.addEventListener('DOMContentLoaded', function () {
  // Variable para almacenar la posición anterior del scroll
  let prevScrollPos = document.documentElement.scrollTop;

  // Obtiene la referencia al elemento de la barra de navegación
  const navbar = document.getElementById("navbar");

  // Función que se ejecuta cada vez que se realiza un scroll en la ventana
  window.onscroll = function () {
      // Obtiene la posición actual del scroll vertical
      const currentScrollPos = document.documentElement.scrollTop;

      // Compara la posición anterior con la posición actual del scroll
      if (prevScrollPos > currentScrollPos) {
          // Si el scroll hacia abajo, muestra la barra de navegación moviéndola hacia arriba
          navbar.style.transform = "translateY(0)";
      } else {
          // Si el scroll es hacia arriba, oculta la barra de navegación moviéndola hacia abajo
          navbar.style.transform = `translateY(-${navbar.offsetHeight}px)`;
      }

      // Actualiza la posición anterior del scroll a la posición actual
      prevScrollPos = currentScrollPos;
  };
});
