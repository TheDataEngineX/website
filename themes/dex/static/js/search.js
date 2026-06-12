(function () {
  'use strict';
  var searchIndex = [];
  var overlay = null;
  var input = null;
  var results = null;
  var toggle = null;

  function esc(str) {
    var d = document.createElement('div');
    d.appendChild(document.createTextNode(str));
    return d.innerHTML;
  }

  function init() {
    fetch('/search-index.json')
      .then(function (r) { return r.json(); })
      .then(function (data) { searchIndex = data; })
      .catch(function () {});

    input = document.createElement('input');
    input.type = 'search';
    input.placeholder = 'Search docs...';
    input.className = 'docs-search-input';
    input.setAttribute('aria-label', 'Search documentation');

    results = document.createElement('div');
    results.className = 'docs-search-results';
    results.style.display = 'none';

    overlay = document.createElement('div');
    overlay.className = 'docs-search-overlay';
    overlay.style.display = 'none';
    overlay.appendChild(input);
    overlay.appendChild(results);
    document.body.appendChild(overlay);

    toggle = document.createElement('button');
    toggle.className = 'docs-search-toggle';
    toggle.textContent = '\uD83D\uDD0D';
    toggle.setAttribute('aria-label', 'Open search');
    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      overlay.style.display = 'flex';
      input.focus();
    });

    var navLinks = document.querySelector('.nav-links');
    if (navLinks) {
      var li = document.createElement('li');
      li.appendChild(toggle);
      navLinks.appendChild(li);
    }

    input.addEventListener('input', onInput);
    input.addEventListener('keydown', onKeydown);
    overlay.addEventListener('click', onOverlayClick);
  }

  function onInput() {
    var q = this.value.toLowerCase().trim();
    if (q.length < 2) {
      results.style.display = 'none';
      return;
    }
    var hits = searchIndex.filter(function (p) {
      return p.title.toLowerCase().indexOf(q) !== -1 ||
             p.description.toLowerCase().indexOf(q) !== -1;
    });
    if (hits.length === 0) {
      results.innerHTML = '<div class="docs-search-empty">No results found</div>';
    } else {
      results.innerHTML = hits.slice(0, 20).map(function (h) {
        return '<a href="' + esc(h.url) + '" class="docs-search-result">' +
          '<span class="docs-search-result-title">' + highlight(esc(h.title), q) + '</span>' +
          '<span class="docs-search-result-desc">' + highlight(esc(h.description), q) + '</span>' +
          '<span class="docs-search-result-meta">' + esc(h.repo) + ' ' + esc(h.version) + '</span>' +
          '</a>';
      }).join('');
    }
    results.style.display = 'block';
  }

  function onKeydown(e) {
    if (e.key === 'Escape') {
      close();
    }
  }

  function onOverlayClick(e) {
    if (e.target === overlay) {
      close();
    }
  }

  function close() {
    overlay.style.display = 'none';
    results.style.display = 'none';
    input.value = '';
    if (toggle) toggle.focus();
  }

  function highlight(text, query) {
    var idx = text.toLowerCase().indexOf(query);
    if (idx === -1) return text;
    return text.slice(0, idx) +
      '<mark>' + text.slice(idx, idx + query.length) + '</mark>' +
      text.slice(idx + query.length);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
