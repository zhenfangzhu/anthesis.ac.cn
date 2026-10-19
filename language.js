(() => {
  // Preserve shared legacy links while keeping each language at a stable URL.
  const url = new URL(location.href);
  const requested = url.searchParams.get('lang');
  if (requested === 'zh' || requested === 'en') {
    const link = document.querySelector(`.language-options a[data-language="${requested}"]`);
    if (link) {
      const target = new URL(link.href);
      url.searchParams.delete('lang');
      target.search = url.search;
      target.hash = url.hash;
      location.replace(target.href);
      return;
    }
  }
  const fallback = document.querySelector('.language-switch');
  if (!fallback) return;
  const drawer = document.createElement('div');
  drawer.className = 'language-switch language-drawer';
  const toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.className = 'language-trigger';
  toggle.setAttribute('aria-label', 'Language / 语言');
  toggle.setAttribute('aria-controls', 'language-options');
  toggle.innerHTML = fallback.querySelector('summary').innerHTML;
  const options = fallback.querySelector('.language-options');
  options.id = 'language-options';
  drawer.append(toggle, options);
  fallback.replaceWith(drawer);

  function setOpen(open) {
    drawer.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    options.inert = !open;
    options.setAttribute('aria-hidden', String(!open));
    if (open) {
      const menu = document.querySelector('.mobile-nav');
      if (menu) menu.open = false;
    }
  }
  setOpen(false);
  toggle.addEventListener('click', () => setOpen(!drawer.classList.contains('is-open')));
  document.addEventListener('click', event => {
    if (!drawer.contains(event.target)) setOpen(false);
  });
  drawer.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      setOpen(false);
      toggle.focus();
    }
  });
  options.addEventListener('click', event => {
    if (event.target.closest('a')) setOpen(false);
  });
  document.querySelector('.mobile-nav')?.addEventListener('toggle', event => {
    if (event.target.open) setOpen(false);
  });
})();
