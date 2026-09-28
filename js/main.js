/* Rosa Montero DepiLáser · interacciones mínimas (menú, cabecera y apariciones) */
(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.add('js');

  document.addEventListener('DOMContentLoaded', function () {
    var header = document.querySelector('[data-header]');
    var toggle = document.querySelector('[data-nav-toggle]');
    var nav = document.getElementById('site-nav');

    // Menú móvil
    function setMenu(open) {
      if (!header || !toggle) return;
      header.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      var label = toggle.querySelector('.visually-hidden');
      if (label) label.textContent = open ? 'Cerrar menú' : 'Abrir menú';
    }

    if (toggle && nav) {
      toggle.addEventListener('click', function () {
        setMenu(toggle.getAttribute('aria-expanded') !== 'true');
      });
      nav.addEventListener('click', function (event) {
        if (event.target.closest('a')) setMenu(false);
      });
      document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') setMenu(false);
      });
      window.matchMedia('(min-width: 1000px)').addEventListener('change', function () {
        setMenu(false);
      });
    }

    // Borde de la cabecera al desplazarse
    if (header) {
      var onScroll = function () {
        header.classList.toggle('is-scrolled', window.scrollY > 8);
      };
      onScroll();
      window.addEventListener('scroll', onScroll, { passive: true });
    }

    // Apariciones suaves al hacer scroll
    var items = document.querySelectorAll('[data-reveal]');
    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (reduceMotion || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-visible'); });
    } else {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var target = entry.target;
            target.classList.add('is-visible');
            observer.unobserve(target);
            // Retira el retardo para que no afecte a los efectos al pasar el ratón
            window.setTimeout(function () { target.style.transitionDelay = ''; }, 1400);
          }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });

      items.forEach(function (el) {
        // Pequeño escalonado entre elementos hermanos
        var siblings = el.parentElement ? el.parentElement.querySelectorAll(':scope > [data-reveal]') : [];
        var index = Array.prototype.indexOf.call(siblings, el);
        if (index > 0) el.style.transitionDelay = Math.min(index, 4) * 90 + 'ms';
        observer.observe(el);
      });
    }

    // Año del pie
    var year = document.querySelector('[data-year]');
    if (year) year.textContent = String(new Date().getFullYear());
  });
})();
