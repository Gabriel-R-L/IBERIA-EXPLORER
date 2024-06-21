// Extraido de la documentación de Flowbite --> https://flowbite.com/docs/customize/dark-mode/
var themeToggleDarkIcon = document.getElementById("theme-toggle-dark-icon");
var themeToggleLightIcon = document.getElementById("theme-toggle-light-icon");

if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
  document.documentElement.classList.add('dark');
} else {
  document.documentElement.classList.remove('dark')
}

// Change the icons inside the button based on previous settings
if (
  localStorage.getItem("color-theme") === "dark" ||
  (!("color-theme" in localStorage) &&
    window.matchMedia("(prefers-color-scheme: dark)").matches)
) {
  themeToggleLightIcon.classList.remove("hidden");
  labelOscuro();
} else {
  themeToggleDarkIcon.classList.remove("hidden");
  labelClaro();
}

var themeToggleBtn = document.getElementById("theme-toggle");

themeToggleBtn.addEventListener("click", function () {
  // toggle icons inside button
  themeToggleDarkIcon.classList.toggle("hidden");
  themeToggleLightIcon.classList.toggle("hidden");

  // if set via local storage previously
  if (localStorage.getItem("color-theme")) {
    if (localStorage.getItem("color-theme") === "light") {
      document.documentElement.classList.add("dark");
      localStorage.setItem("color-theme", "dark");
      labelOscuro();
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("color-theme", "light");
      labelClaro();
    }

    // if NOT set via local storage previously
  } else {
    if (document.documentElement.classList.contains("dark")) {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("color-theme", "light");
      labelClaro();
    } else {
      document.documentElement.classList.add("dark");
      localStorage.setItem("color-theme", "dark");
      labelOscuro();
    }
  }
});

//? Apaño para los estilos del label
function labelClaro() {
  document.querySelectorAll('label').forEach(label => {
    label.style.color = "black";
  });
}

function labelOscuro() {
  document.querySelectorAll('label').forEach(label => {
    label.style.color = "white"; //////////////////////////////////////
  });
}