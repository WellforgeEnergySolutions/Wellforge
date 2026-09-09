/*!
 * main.js - interface behaviour for the Wellforge Energy Solutions website.
 *
 * No dependencies. Everything degrades: with JavaScript off the pages still
 * read, the navigation still links, and the enquiry forms still submit to the
 * mail client through their own markup.
 */
(function () {
  'use strict';

  /* ---------------------------------------------------------------------
     Set this to POST enquiries to a backend (Formspree, Web3Forms, your own
     handler). Left empty, forms compose a pre-filled email instead, which
     works on static hosting with no server.
     --------------------------------------------------------------------- */
  var FORM_ENDPOINT = '';

  var doc = document;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  function $(sel, ctx) { return (ctx || doc).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }
  function on(el, ev, fn, opts) { if (el) el.addEventListener(ev, fn, opts); }

  /* =====================================================================
     Navigation
     ===================================================================== */
  function initNav() {
    var toggle = $('.nav-toggle');
    var nav = $('#primary-nav');
    var backdrop = $('.nav-backdrop');
    if (!toggle || !nav) return;

    function setOpen(open) {
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      nav.classList.toggle('is-open', open);
      if (backdrop) backdrop.classList.toggle('is-open', open);
      doc.body.style.overflow = open ? 'hidden' : '';
    }

    on(toggle, 'click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    on(backdrop, 'click', function () { setOpen(false); });
    on(doc, 'keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        setOpen(false);
        toggle.focus();
      }
    });

    // On the mobile drawer the caret opens the sub-list instead of navigating.
    $$('.nav__item--has-panel').forEach(function (item) {
      var link = $('.nav__link', item);
      on(link, 'click', function (e) {
        if (window.innerWidth > 1040) return;
        if (!item.classList.contains('is-expanded')) {
          e.preventDefault();
          $$('.nav__item--has-panel').forEach(function (other) {
            if (other !== item) other.classList.remove('is-expanded');
          });
          item.classList.add('is-expanded');
        }
      });
    });

    // Any in-drawer link closes the drawer - unless the tap was consumed above
    // to open a sub-list, in which case the drawer must stay put.
    $$('#primary-nav a').forEach(function (a) {
      on(a, 'click', function (e) {
        if (e.defaultPrevented) return;
        if (window.innerWidth <= 1040) setOpen(false);
      });
    });

    // Reset drawer state when the layout crosses back to desktop.
    var wasNarrow = window.innerWidth <= 1040;
    on(window, 'resize', function () {
      var narrow = window.innerWidth <= 1040;
      if (narrow !== wasNarrow) {
        wasNarrow = narrow;
        setOpen(false);
        $$('.nav__item--has-panel').forEach(function (i) { i.classList.remove('is-expanded'); });
      }
    });
  }

  /* =====================================================================
     Sticky header, scroll progress, back-to-top
     ===================================================================== */
  function initScrollChrome() {
    var header = $('#site-header');
    var bar = $('.page-progress span');
    var toTop = $('.to-top');
    var ticking = false;

    function update() {
      ticking = false;
      var y = window.pageYOffset || doc.documentElement.scrollTop;
      if (header) header.classList.toggle('is-stuck', y > 30);
      if (toTop) toTop.classList.toggle('is-visible', y > 700);
      if (bar) {
        var max = doc.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = (max > 0 ? Math.min(100, (y / max) * 100) : 0) + '%';
      }
    }

    on(window, 'scroll', function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    on(toTop, 'click', function () {
      window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
    });
    update();
  }

  /* =====================================================================
     Reveal on scroll, with a stagger inside each group
     ===================================================================== */
  function initReveal() {
    var items = $$('.reveal');
    if (!items.length) return;

    if (reduced || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }

    // Siblings that share a parent animate one after another.
    var groups = {};
    items.forEach(function (el) {
      var parent = el.parentNode;
      var key = groups.__index === undefined ? 0 : 0;
      if (!parent.__revealSeq) parent.__revealSeq = 0;
      el.style.setProperty('--i', Math.min(parent.__revealSeq++, 7));
      void key;
    });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });

    items.forEach(function (el) { io.observe(el); });
  }

  /* =====================================================================
     Counting statistics
     ===================================================================== */
  function initCounters() {
    var nums = $$('[data-count]');
    if (!nums.length) return;

    // The real figure is already in the markup, so with reduced motion or no
    // IntersectionObserver there is nothing to do - leave it alone.
    if (reduced || !('IntersectionObserver' in window)) return;

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);
        var el = entry.target;
        var target = parseFloat(el.getAttribute('data-count')) || 0;
        var start = null;
        var dur = 1300;
        el.textContent = '0';

        function step(now) {
          if (start === null) start = now;
          var t = Math.min((now - start) / dur, 1);
          var eased = 1 - Math.pow(1 - t, 3);
          el.textContent = Math.round(target * eased).toString();
          if (t < 1) window.requestAnimationFrame(step);
          else el.textContent = target.toString();
        }
        window.requestAnimationFrame(step);
      });
    }, { threshold: 0.4 });

    nums.forEach(function (el) { io.observe(el); });
  }

  /* =====================================================================
     Card tilt - a small parallax that follows the pointer
     ===================================================================== */
  function initTilt() {
    if (reduced || !finePointer) return;
    var MAX = 5.5;                       // degrees

    $$('.tilt').forEach(function (card) {
      var frame = null;

      function move(e) {
        if (frame) return;
        frame = window.requestAnimationFrame(function () {
          frame = null;
          var r = card.getBoundingClientRect();
          var px = (e.clientX - r.left) / r.width - 0.5;
          var py = (e.clientY - r.top) / r.height - 0.5;
          card.style.setProperty('--rx', (px * MAX).toFixed(2) + 'deg');
          card.style.setProperty('--ry', (-py * MAX).toFixed(2) + 'deg');
        });
      }
      function reset() {
        if (frame) { window.cancelAnimationFrame(frame); frame = null; }
        card.style.setProperty('--rx', '0deg');
        card.style.setProperty('--ry', '0deg');
      }

      on(card, 'mousemove', move);
      on(card, 'mouseleave', reset);
    });
  }

  /* =====================================================================
     3D scenes
     ===================================================================== */
  function initScenes() {
    var holders = $$('[data-scene]');
    if (!holders.length) return;
    if (reduced || !window.WFScenes || !window.WF3D || !window.WF3D.supported) return;

    holders.forEach(function (holder) {
      var canvas = $('.scene__canvas', holder);
      var name = holder.getAttribute('data-scene');
      if (!canvas) return;
      try {
        var built = window.WFScenes.mount(canvas, name, {
          // Reveal the canvas only once it has genuinely drawn a frame.
          onFirstFrame: function () { holder.classList.add('is-live'); }
        });
        if (built) {
          // Hide the "drag to rotate" hint once the visitor has done so.
          ['mousedown', 'touchstart'].forEach(function (ev) {
            on(canvas, ev, function () { holder.classList.add('is-touched'); },
               { passive: true, once: true });
          });
        }
      } catch (err) {
        // Leave the still illustration in place; nothing else to do.
        holder.classList.remove('is-live');
      }
    });
  }

  /* =====================================================================
     Enquiry forms
     ===================================================================== */
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function fieldOf(input) {
    var el = input;
    while (el && !(el.classList && el.classList.contains('field'))) el = el.parentNode;
    return el;
  }

  function initForms() {
    $$('form[data-enquiry]').forEach(function (form) {
      var status = $('.form-status', form);
      var emailInput = form.querySelector('input[type="email"]');

      // Clear the error as soon as the visitor starts fixing it.
      on(emailInput, 'input', function () {
        var f = fieldOf(emailInput);
        if (f) f.classList.remove('has-error');
      });

      on(form, 'submit', function (e) {
        e.preventDefault();
        if (status) { status.textContent = ''; status.className = 'form-status'; }

        // Honeypot: a real visitor never sees or fills this.
        var hp = form.querySelector('input[name="company_website"]');
        if (hp && hp.value) return;

        var email = emailInput ? emailInput.value.trim() : '';
        if (!EMAIL_RE.test(email)) {
          var f = fieldOf(emailInput);
          if (f) f.classList.add('has-error');
          if (emailInput) emailInput.focus();
          return;
        }

        var data = {};
        ['name', 'email', 'phone', 'company', 'requirement', 'message'].forEach(function (key) {
          var el = form.querySelector('[name="' + key + '"]');
          if (el) data[key] = el.value.trim();
        });
        var subject = form.getAttribute('data-subject') || 'Website enquiry';

        var btn = form.querySelector('button[type="submit"]');
        if (btn) btn.disabled = true;

        function done(ok, msg) {
          if (btn) btn.disabled = false;
          if (!status) return;
          status.textContent = msg;
          status.className = 'form-status ' + (ok ? 'is-ok' : 'is-error');
        }

        if (FORM_ENDPOINT) {
          data._subject = subject;
          fetch(FORM_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
            body: JSON.stringify(data)
          }).then(function (res) {
            if (!res.ok) throw new Error('bad status');
            form.reset();
            done(true, 'Thank you - your enquiry has been sent. We respond within 24 hours.');
          }).catch(function () {
            done(false, 'Sorry, that did not go through. Please email sales@wellforgeenergysolutions.com.');
          });
          return;
        }

        // Static fallback: hand a fully composed message to the mail client.
        var lines = [
          'Name: ' + (data.name || '-'),
          'Email: ' + data.email,
          'Phone: ' + (data.phone || '-'),
          'Company: ' + (data.company || '-'),
          'Requirement: ' + (data.requirement || '-'),
          '',
          'Message:',
          data.message || '-'
        ];
        window.location.href = 'mailto:sales@wellforgeenergysolutions.com'
          + '?subject=' + encodeURIComponent(subject)
          + '&body=' + encodeURIComponent(lines.join('\n'));
        done(true, 'Opening your email client with the enquiry ready to send.');
      });
    });

    $$('form[data-newsletter]').forEach(function (form) {
      var status = form.parentNode.querySelector('.form-status');
      on(form, 'submit', function (e) {
        e.preventDefault();
        var input = form.querySelector('input[type="email"]');
        var email = input ? input.value.trim() : '';
        if (!status) return;
        if (!EMAIL_RE.test(email)) {
          status.textContent = 'Please enter a valid email address.';
          status.className = 'form-status is-error';
          if (input) input.focus();
          return;
        }
        window.location.href = 'mailto:sales@wellforgeenergysolutions.com'
          + '?subject=' + encodeURIComponent('Subscribe - Wellforge sourcing insights')
          + '&body=' + encodeURIComponent('Please add ' + email + ' to the mailing list.');
        status.textContent = 'Thank you - opening your email client to confirm.';
        status.className = 'form-status is-ok';
        form.reset();
      });
    });
  }

  /* =====================================================================
     Blog category filter
     ===================================================================== */
  function initFilters() {
    var buttons = $$('.filter-btn');
    if (!buttons.length) return;
    var cards = $$('.post-card');

    buttons.forEach(function (btn) {
      on(btn, 'click', function () {
        var key = btn.getAttribute('data-filter');
        buttons.forEach(function (b) {
          var active = b === btn;
          b.classList.toggle('is-active', active);
          b.setAttribute('aria-pressed', active ? 'true' : 'false');
        });
        cards.forEach(function (card) {
          var show = key === 'all' || card.getAttribute('data-category') === key;
          card.hidden = !show;
        });
      });
    });
  }

  /* =====================================================================
     Copyright year
     ===================================================================== */
  function initYear() {
    $$('[data-year]').forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  }

  /* =====================================================================
     Boot
     ===================================================================== */
  function boot() {
    // Confirms to the inline head script that the interface is running, so the
    // scroll-reveal state is allowed to stand.
    doc.documentElement.setAttribute('data-wf-ready', '');
    initNav();
    initScrollChrome();
    initReveal();
    initCounters();
    initTilt();
    initFilters();
    initForms();
    initYear();
    initScenes();
  }

  if (doc.readyState === 'loading') on(doc, 'DOMContentLoaded', boot);
  else boot();
})();
