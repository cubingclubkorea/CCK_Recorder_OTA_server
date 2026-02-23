(function () {
  // ── Mobile menu toggle ──────────────────────────────────
  var menuToggle = document.querySelector('.menu-toggle');
  var siteNav = document.querySelector('.site-nav');

  if (menuToggle && siteNav) {
    menuToggle.addEventListener('click', function () {
      var isOpen = siteNav.getAttribute('data-open') === 'true';
      siteNav.setAttribute('data-open', String(!isOpen));
      menuToggle.setAttribute('aria-expanded', String(!isOpen));
    });
  }

  // ── Firmware list tabs ──────────────────────────────────
  var tabButtons = document.querySelectorAll('[data-tab-target]');
  var tabPanels = document.querySelectorAll('[data-tab-panel]');

  tabButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      var target = button.getAttribute('data-tab-target');
      tabButtons.forEach(function (btn) { btn.classList.remove('active'); });
      button.classList.add('active');
      tabPanels.forEach(function (panel) {
        panel.classList.toggle('active', panel.getAttribute('data-tab-panel') === target);
      });
    });
  });

  // ── Contact inquiry type selector ──────────────────────
  var inquiryBtns = document.querySelectorAll('[data-type]');
  var guidePanels = document.querySelectorAll('[data-guide]');
  var inquiryTypeInput = document.getElementById('inquiry_type');

  if (inquiryBtns.length) {
    inquiryBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var type = btn.getAttribute('data-type');

        inquiryBtns.forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');

        guidePanels.forEach(function (panel) {
          panel.classList.toggle('active', panel.getAttribute('data-guide') === type);
        });

        if (inquiryTypeInput) {
          inquiryTypeInput.value = type;
        }
      });
    });
  }

  // ── Scroll reveal ───────────────────────────────────────
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
      { threshold: 0.12 }
    );

    reveals.forEach(function (el) { observer.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }
})();
