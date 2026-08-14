// StackScout - Theme Manager & Article Utilities
(function() {
  function getPreferredTheme() {
    const saved = localStorage.getItem('theme');
    if (saved) return saved;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  // Set initial theme attribute before render
  document.documentElement.setAttribute('data-theme', getPreferredTheme());

  // Attach click listener on DOMReady
  document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('theme-toggle');
    if (!toggleBtn) return;

    toggleBtn.addEventListener('click', function() {
      const current = document.documentElement.getAttribute('data-theme') || getPreferredTheme();
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
    });
  });
})();

// One-click Copy Article Link helper for Article Pages
function copyArticleLink(btn) {
  if (!btn) return;
  const url = window.location.href;
  navigator.clipboard.writeText(url).then(function() {
    const originalText = btn.textContent;
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(function() {
      btn.textContent = originalText;
      btn.classList.remove('copied');
    }, 2000);
  }).catch(function() {
    btn.textContent = 'Failed to copy';
  });
}

// Share Card Helper for Index & Archive Pages
function shareCard(event, url, title) {
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }
  const btn = event ? event.currentTarget : null;

  if (navigator.share) {
    navigator.share({
      title: title || 'StackScout Article',
      url: url
    }).catch(function() {});
  } else if (navigator.clipboard) {
    navigator.clipboard.writeText(url).then(function() {
      if (btn) {
        const origHTML = btn.innerHTML;
        btn.innerHTML = 'Copied!';
        btn.classList.add('copied');
        setTimeout(function() {
          btn.innerHTML = origHTML;
          btn.classList.remove('copied');
        }, 2000);
      }
    });
  }
}
