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
  const dropdown = document.querySelector('.language-switch');
  if (!dropdown) return;
  document.addEventListener('click', event => {
    if (!dropdown.contains(event.target)) dropdown.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && dropdown.open) {
      dropdown.open = false;
      dropdown.querySelector('summary').focus();
    }
  });
  dropdown.addEventListener('toggle', () => {
    if (dropdown.open) {
      const menu = document.querySelector('.mobile-nav');
      if (menu) menu.open = false;
    }
  });
  document.querySelector('.mobile-nav')?.addEventListener('toggle', event => {
    if (event.target.open) dropdown.open = false;
  });
})();
