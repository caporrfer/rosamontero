// Menú en móvil, sombra de la barra al desplazarse y día de hoy en el horario.
(function () {
  var boton = document.querySelector("[data-menu-boton]");
  var menu = document.getElementById("menu");

  function cerrarMenu() {
    menu.removeAttribute("data-abierto");
    boton.setAttribute("aria-expanded", "false");
  }

  if (boton && menu) {
    boton.addEventListener("click", function () {
      var abierto = boton.getAttribute("aria-expanded") === "true";
      if (abierto) {
        cerrarMenu();
      } else {
        menu.setAttribute("data-abierto", "");
        boton.setAttribute("aria-expanded", "true");
      }
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) cerrarMenu();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && boton.getAttribute("aria-expanded") === "true") {
        cerrarMenu();
        boton.focus();
      }
    });
  }

  var barra = document.querySelector("[data-barra]");
  if (barra) {
    var actualizar = function () {
      if (window.scrollY > 40) barra.setAttribute("data-con-sombra", "");
      else barra.removeAttribute("data-con-sombra");
    };
    window.addEventListener("scroll", actualizar, { passive: true });
    actualizar();
  }

  var hoy = String(new Date().getDay());
  document.querySelectorAll(".horario tr[data-dias]").forEach(function (fila) {
    if (fila.getAttribute("data-dias").split(" ").indexOf(hoy) !== -1) {
      fila.setAttribute("data-hoy", "");
    }
  });
})();
