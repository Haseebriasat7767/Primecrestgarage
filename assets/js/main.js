/* ==========================================================================
   PRIMECREST GARAGE — interactions
   ========================================================================== */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var WhatsAppNumber = '971505708420';

  document.addEventListener('DOMContentLoaded', function () {
    initYear();
    initHeader();
    initMobileNav();
    initActiveNav();
    initReveal();
    initCounters();
    initMarquee();
    initTestimonials();
    initAccordion();
    initBookingForm();
    initToTop();
  });

  function initYear() {
    var y = document.getElementById('year');
    if (y) y.textContent = String(new Date().getFullYear());
  }

  /* ---------- Sticky header + scroll progress ---------- */
  function initHeader() {
    var header = document.getElementById('siteHeader');
    var bar = document.getElementById('scrollProgress');
    var ticking = false;

    function update() {
      var y = window.scrollY || window.pageYOffset;
      if (header) header.classList.toggle('is-scrolled', y > 40);
      if (bar) {
        var h = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = (h > 0 ? Math.min(100, (y / h) * 100) : 0) + '%';
      }
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  /* ---------- Mobile navigation ---------- */
  function initMobileNav() {
    var toggle = document.getElementById('navToggle');
    var nav = document.getElementById('primaryNav');
    if (!toggle || !nav) return;

    function close() {
      document.body.classList.remove('nav-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open menu');
    }
    function open() {
      document.body.classList.add('nav-open');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Close menu');
    }

    toggle.addEventListener('click', function () {
      if (document.body.classList.contains('nav-open')) close(); else open();
    });

    nav.addEventListener('click', function (e) {
      var link = e.target.closest('a');
      if (link) close();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 1080) close();
    });
  }

  /* ---------- Active nav link ---------- */
  function initActiveNav() {
    var sections = Array.prototype.slice.call(document.querySelectorAll('main section[id]'));
    var links = Array.prototype.slice.call(document.querySelectorAll('.primary-nav a[href^="#"]'));
    if (!sections.length || !('IntersectionObserver' in window)) return;

    var map = {};
    links.forEach(function (l) { map[l.getAttribute('href').slice(1)] = l; });

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var id = entry.target.id;
        links.forEach(function (l) { l.classList.remove('is-active'); });
        if (map[id]) map[id].classList.add('is-active');
      });
    }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });

    sections.forEach(function (s) { observer.observe(s); });
  }

  /* ---------- Reveal on scroll ---------- */
  function initReveal() {
    var items = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
    if (!items.length) return;
    if (reduceMotion || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { obs.observe(el); });
  }

  /* ---------- Stat counters ---------- */
  function initCounters() {
    var nums = Array.prototype.slice.call(document.querySelectorAll('[data-count]'));
    if (!nums.length || reduceMotion) return;

    function animate(el) {
      var target = parseInt(el.getAttribute('data-count'), 10) || 0;
      var suffix = el.getAttribute('data-suffix') || '';
      var start = performance.now();
      var dur = 1500;
      function frame(now) {
        var p = Math.min(1, (now - start) / dur);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * eased).toLocaleString('en-US') + suffix;
        if (p < 1) requestAnimationFrame(frame);
      }
      requestAnimationFrame(frame);
    }

    if (!('IntersectionObserver' in window)) return;

    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { animate(entry.target); obs.unobserve(entry.target); }
      });
    }, { threshold: 0.4 });
    nums.forEach(function (n) { obs.observe(n); });
  }

  /* ---------- Brand marquee (duplicate for seamless loop) ---------- */
  function initMarquee() {
    var track = document.querySelector('[data-marquee] .marquee-track');
    if (!track) return;
    var original = Array.prototype.slice.call(track.children);
    original.forEach(function (node) {
      var clone = node.cloneNode(true);
      clone.setAttribute('aria-hidden', 'true');
      if (clone.classList) clone.classList.add('is-clone');
      track.appendChild(clone);
    });
  }

  /* ---------- Testimonials carousel ---------- */
  function initTestimonials() {
    var viewport = document.getElementById('testiViewport');
    var track = document.getElementById('testiTrack');
    var prev = document.getElementById('testiPrev');
    var next = document.getElementById('testiNext');
    var dotsWrap = document.getElementById('testiDots');
    if (!viewport || !track) return;

    var cards = Array.prototype.slice.call(track.children);
    var autoTimer = null;
    var paused = false;

    function step() {
      var first = cards[0];
      if (!first) return viewport.clientWidth;
      var gap = parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap) || 22;
      return first.getBoundingClientRect().width + gap;
    }

    function pages() {
      var s = step();
      var max = viewport.scrollWidth - viewport.clientWidth;
      return Math.max(1, Math.round(max / s) + 1);
    }

    function currentPage() {
      return Math.round(viewport.scrollLeft / step());
    }

    function buildDots() {
      if (!dotsWrap) return;
      var total = pages();
      dotsWrap.innerHTML = '';
      for (var i = 0; i < total; i++) {
        var b = document.createElement('button');
        b.type = 'button';
        b.setAttribute('role', 'tab');
        b.setAttribute('aria-selected', i === 0 ? 'true' : 'false');
        b.setAttribute('aria-label', 'Go to testimonial group ' + (i + 1));
        b.dataset.index = String(i);
        dotsWrap.appendChild(b);
      }
      syncDots();
    }

    function syncDots() {
      if (!dotsWrap) return;
      var active = Math.min(currentPage(), dotsWrap.children.length - 1);
      Array.prototype.forEach.call(dotsWrap.children, function (dot, i) {
        dot.setAttribute('aria-selected', i === active ? 'true' : 'false');
      });
    }

    function goTo(page) {
      var s = step();
      var total = pages();
      var target = Math.max(0, Math.min(total - 1, page));
      viewport.scrollTo({ left: target * s, behavior: reduceMotion ? 'auto' : 'smooth' });
    }

    function nextSlide() {
      var total = pages();
      var p = currentPage() + 1;
      goTo(p >= total ? 0 : p);
    }

    if (next) next.addEventListener('click', function () { goTo(currentPage() + 1); restart(); });
    if (prev) prev.addEventListener('click', function () { goTo(currentPage() - 1); restart(); });

    if (dotsWrap) {
      dotsWrap.addEventListener('click', function (e) {
        var btn = e.target.closest('button');
        if (!btn) return;
        goTo(parseInt(btn.dataset.index, 10) || 0);
        restart();
      });
    }

    var scrollTick = false;
    viewport.addEventListener('scroll', function () {
      if (scrollTick) return;
      scrollTick = true;
      requestAnimationFrame(function () { syncDots(); scrollTick = false; });
    }, { passive: true });

    viewport.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { goTo(currentPage() + 1); e.preventDefault(); }
      if (e.key === 'ArrowLeft') { goTo(currentPage() - 1); e.preventDefault(); }
    });

    /* drag to scroll (desktop) */
    var isDown = false, startX = 0, startScroll = 0, moved = false;
    viewport.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'touch') return;
      isDown = true; moved = false;
      startX = e.clientX; startScroll = viewport.scrollLeft;
      viewport.classList.add('is-dragging');
    });
    window.addEventListener('pointermove', function (e) {
      if (!isDown) return;
      var dx = e.clientX - startX;
      if (Math.abs(dx) > 4) moved = true;
      viewport.scrollLeft = startScroll - dx;
    });
    window.addEventListener('pointerup', function () {
      if (!isDown) return;
      isDown = false;
      viewport.classList.remove('is-dragging');
      if (moved) {
        var s = step();
        goTo(Math.round(viewport.scrollLeft / s));
      }
    });
    viewport.addEventListener('click', function (e) {
      if (moved) e.preventDefault();
    }, true);

    /* autoplay */
    function start() {
      if (reduceMotion) return;
      stop();
      autoTimer = setInterval(function () {
        if (paused || document.hidden) return;
        nextSlide();
      }, 6000);
    }
    function stop() { if (autoTimer) { clearInterval(autoTimer); autoTimer = null; } }
    function restart() { stop(); start(); }

    viewport.addEventListener('mouseenter', function () { paused = true; });
    viewport.addEventListener('mouseleave', function () { paused = false; });
    viewport.addEventListener('focusin', function () { paused = true; });
    viewport.addEventListener('focusout', function () { paused = false; });

    var resizeTick = false;
    window.addEventListener('resize', function () {
      if (resizeTick) return;
      resizeTick = true;
      setTimeout(function () { buildDots(); resizeTick = false; }, 180);
    });

    buildDots();
    start();
  }

  /* ---------- FAQ accordion ---------- */
  function initAccordion() {
    var root = document.getElementById('faqAccordion');
    if (!root) return;
    var triggers = Array.prototype.slice.call(root.querySelectorAll('.acc-trigger'));

    triggers.forEach(function (trigger) {
      var panel = trigger.nextElementSibling;
      if (!panel) return;

      // set initial state
      var open = trigger.getAttribute('aria-expanded') === 'true';
      panel.classList.toggle('open', open);

      trigger.addEventListener('click', function () {
        var isOpen = trigger.getAttribute('aria-expanded') === 'true';
        triggers.forEach(function (t) {
          t.setAttribute('aria-expanded', 'false');
          var p = t.nextElementSibling;
          if (p) p.classList.remove('open');
        });
        if (!isOpen) {
          trigger.setAttribute('aria-expanded', 'true');
          panel.classList.add('open');
        }
      });
    });
  }

  /* ---------- Booking form ---------- */
  function initBookingForm() {
    var form = document.getElementById('bookingForm');
    if (!form) return;
    var status = document.getElementById('formStatus');
    var dateInput = form.querySelector('#date');

    if (dateInput) {
      var today = new Date();
      var iso = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
      dateInput.min = iso;
    }

    function setStatus(msg, isError) {
      if (!status) return;
      status.textContent = msg;
      status.classList.toggle('error', !!isError);
    }

    function validateField(field) {
      var valid = true;
      var value = (field.value || '').trim();
      if (field.hasAttribute('required') && !value) valid = false;
      if (valid && field.type === 'tel') valid = /^[+\d][\d\s().-]{6,}$/.test(value);
      if (valid && field.type === 'date') valid = !isNaN(Date.parse(value));
      field.classList.toggle('is-invalid', !valid);
      return valid;
    }

    var fields = Array.prototype.slice.call(form.querySelectorAll('input, select, textarea'));
    fields.forEach(function (f) {
      f.addEventListener('blur', function () {
        if (f.value || f.classList.contains('is-invalid')) validateField(f);
      });
      f.addEventListener('input', function () {
        if (f.classList.contains('is-invalid')) validateField(f);
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      var firstInvalid = null;
      fields.forEach(function (f) {
        var valid = validateField(f);
        if (!valid && !firstInvalid) firstInvalid = f;
        if (!valid) ok = false;
      });

      if (!ok) {
        setStatus('Please complete the highlighted fields so we can reach you.', true);
        if (firstInvalid) firstInvalid.focus();
        return;
      }

      var data = new FormData(form);
      var lines = [
        'New appointment request — Primecrest Garage',
        '',
        'Name: ' + (data.get('name') || '—'),
        'Phone: ' + (data.get('phone') || '—'),
        'Car model: ' + (data.get('car') || '—'),
        'Service: ' + (data.get('service') || '—'),
        'Preferred date: ' + (data.get('date') || '—'),
        'Preferred time: ' + (data.get('time') || 'Any time'),
        'Message: ' + (data.get('message') || '—')
      ];
      var url = 'https://wa.me/' + WhatsAppNumber + '?text=' + encodeURIComponent(lines.join('\n'));

      setStatus('Thank you — opening WhatsApp so you can send the request directly to our service desk…');
      window.open(url, '_blank', 'noopener');
      form.reset();
      fields.forEach(function (f) { f.classList.remove('is-invalid'); });
    });
  }

  /* ---------- Back to top ---------- */
  function initToTop() {
    var btn = document.getElementById('toTop');
    if (!btn) return;
    window.addEventListener('scroll', function () {
      btn.classList.toggle('show', window.scrollY > 700);
    }, { passive: true });
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  }
})();
