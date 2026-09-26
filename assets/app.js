(() => {
  'use strict';
  const script = document.currentScript;
  const root = new URL('../', script.src);
  const config = window.PFDAV || {};
  const nav = document.getElementById('site-nav');
  const toggle = document.querySelector('.menu-toggle');
  if (nav && toggle) {
    document.documentElement.classList.add('js');
    const setMenu = (open, restoreFocus = false) => {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
      nav.classList.toggle('is-open', open);
      if (restoreFocus) toggle.focus();
    };
    toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
    nav.addEventListener('click', (event) => { if (event.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') setMenu(false, true);
    });
    document.addEventListener('click', (event) => {
      if (!nav.contains(event.target) && !toggle.contains(event.target)) setMenu(false);
    });
    window.matchMedia('(min-width: 801px)').addEventListener('change', () => setMenu(false));
  }
  const publicUrl = (value) => {
    if (typeof value !== 'string' || !value.trim()) return null;
    const raw = value.trim();
    if (raw.startsWith('/') || raw.includes('\\')) return null;
    try {
      const url = new URL(raw, root);
      const isAbsolute = /^[a-z][a-z0-9+.-]*:/i.test(raw);
      if (isAbsolute) return url.protocol === 'https:' && !url.username && !url.password ? url.href : null;
      return url.href.startsWith(root.href) ? url.href : null;
    } catch { return null; }
  };
  const groupName = typeof config.groupName === 'string' ? config.groupName.trim() : '';
  if (groupName) document.querySelectorAll('[data-group-name]').forEach((el) => { el.textContent = groupName; });
  document.querySelectorAll('[data-member]').forEach((el) => {
    const member = config.members?.[el.dataset.member];
    if (!member) return;
    const role = el.querySelector('[data-role]');
    if (role && member.role) role.textContent = member.role;
    const slot = el.querySelector('[data-member-github]');
    const url = publicUrl(member.github);
    if (slot && url) {
      const a = document.createElement('a');
      a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer';
      a.className = 'text-link'; a.textContent = 'GitHub profile ↗';
      slot.replaceChildren(a);
    }
  });
  const assignment = config.assignments?.[document.body.dataset.assignment];
  if (assignment) {
    for (const key of ['dataset', 'description']) {
      if (typeof assignment[key] === 'string' && assignment[key].trim()) {
        document.querySelectorAll(`[data-field="${key}"]`).forEach((el) => { el.textContent = assignment[key]; });
      }
    }
    document.querySelectorAll('[data-resource]').forEach((slot) => {
      const url = publicUrl(assignment[slot.dataset.resource]);
      if (!url) return;
      const a = document.createElement('a');
      a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer';
      a.className = 'text-link'; a.textContent = slot.dataset.label || 'Open resource ↗';
      slot.replaceChildren(a);
    });
  }
  if ('IntersectionObserver' in window) {
    const links = [...document.querySelectorAll('#site-nav a[href^="#"]')];
    const sections = links.map((a) => document.querySelector(a.getAttribute('href'))).filter(Boolean);
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((a) => {
          if (a.hash === '#' + entry.target.id) a.setAttribute('aria-current', 'location');
          else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-15% 0px -60% 0px' });
    sections.forEach((section) => observer.observe(section));
  }
})();
