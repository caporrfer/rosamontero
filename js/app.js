(function () {
  'use strict';

  var header = document.getElementById('cabecera');
  var toggle = document.querySelector('.menu-toggle');
  var menu = document.getElementById('menu');
  var toggleLabel = toggle.querySelector('.visually-hidden');

  /* Menú móvil */
  function setMenu(open) {
    toggle.setAttribute('aria-expanded', String(open));
    toggleLabel.textContent = open ? 'Cerrar menú' : 'Abrir menú';
    menu.classList.toggle('is-open', open);
    document.body.classList.toggle('menu-open', open);
  }

  toggle.addEventListener('click', function () {
    setMenu(toggle.getAttribute('aria-expanded') !== 'true');
  });

  menu.addEventListener('click', function (event) {
    if (event.target.closest('a')) setMenu(false);
  });

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && menu.classList.contains('is-open')) {
      setMenu(false);
      toggle.focus();
    }
  });

  window.matchMedia('(min-width: 901px)').addEventListener('change', function (mq) {
    if (mq.matches) setMenu(false);
  });

  /* Cabecera compacta y barra móvil de contacto (aparece al pasar el inicio) */
  var mobileBar = document.getElementById('barra-movil');
  var hero = document.getElementById('inicio');

  function onScroll() {
    header.classList.toggle('is-scrolled', window.scrollY > 12);
    mobileBar.classList.toggle('is-visible', window.scrollY > hero.offsetHeight * 0.6);
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* Animaciones de aparición */
  var items = document.querySelectorAll('[data-reveal]');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (reduceMotion || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    // Escalonar los elementos que comparten contenedor
    items.forEach(function (el) {
      var siblings = Array.prototype.filter.call(el.parentElement.children, function (child) {
        return child.hasAttribute('data-reveal');
      });
      var index = siblings.indexOf(el);
      if (index > 0) el.style.setProperty('--delay', Math.min(index, 6) * 0.08 + 's');
    });

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });

    items.forEach(function (el) { observer.observe(el); });
  }

  /* Año del pie */
  var year = document.getElementById('anio');
  if (year) year.textContent = new Date().getFullYear();
})();
