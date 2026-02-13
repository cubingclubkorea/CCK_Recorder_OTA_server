(function () {
  var menuToggle = document.querySelector('.menu-toggle');
  var siteNav = document.querySelector('.site-nav');

  if (menuToggle && siteNav) {
    menuToggle.addEventListener('click', function () {
      var isOpen = siteNav.getAttribute('data-open') === 'true';
      siteNav.setAttribute('data-open', String(!isOpen));
      menuToggle.setAttribute('aria-expanded', String(!isOpen));
    });
  }

  var tabButtons = document.querySelectorAll('[data-tab-target]');
  var tabPanels = document.querySelectorAll('[data-tab-panel]');

  tabButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      var target = button.getAttribute('data-tab-target');
      tabButtons.forEach(function (btn) {
        btn.classList.remove('active');
      });
      button.classList.add('active');

      tabPanels.forEach(function (panel) {
        panel.classList.toggle('active', panel.getAttribute('data-tab-panel') === target);
      });
    });
  });

  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('in');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.16 }
    );

    reveals.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    reveals.forEach(function (el) {
      el.classList.add('in');
    });
  }
})();
