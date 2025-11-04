// === ПОИСК ===
document.getElementById('search').addEventListener('input', e => {
  const query = e.target.value.toLowerCase().trim();
  if (!query) {
    document.getElementById('search-results').style.display = 'none';
    return;
  }

  fetch('assets/data/search-index.json')
    .then(res => res.json())
    .then(data => {
      const results = data.filter(item =>
        item.title.toLowerCase().includes(query) ||
        item.content.toLowerCase().includes(query)
      );
      const ul = document.getElementById('search-results');
      ul.innerHTML = results.length
        ? results.map(r => `<li><a href="${r.url}">${r.title}</a></li>`).join('')
        : '<li>Ничего не найдено</li>';
      ul.style.display = 'block';
    })
    .catch(() => {
      const ul = document.getElementById('search-results');
      ul.innerHTML = '<li>Ошибка поиска</li>';
      ul.style.display = 'block';
    });
});

// === ЗАКРЫТИЕ ПОИСКА ПРИ КЛИКЕ ВНЕ ===
document.addEventListener('click', e => {
  const searchBox = document.querySelector('.search-box');
  if (!searchBox.contains(e.target)) {
    document.getElementById('search-results').style.display = 'none';
  }
});

// === ДОГОВОР ===
function previewContract() {
  const form = document.getElementById('contract-form');
  if (!validateForm(form)) return;

  const data = Object.fromEntries(new FormData(form));
  data.preview = true;

  fetch('/generate-contract', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(res => {
    document.getElementById('pdf-preview').src = res.preview;
    document.getElementById('preview-modal').style.display = 'flex';
  })
  .catch(() => alert('Ошибка генерации PDF'));
}

function downloadContract() {
  const form = document.getElementById('contract-form');
  if (!validateForm(form)) return;

  const data = Object.fromEntries(new FormData(form));

  fetch('/generate-contract', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  .then(res => res.blob())
  .then(blob => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'dogovor_group112.pdf';
    a.click();
    URL.revokeObjectURL(url);
  })
  .catch(() => alert('Ошибка скачивания PDF'));
}

function closeModal() {
  document.getElementById('preview-modal').style.display = 'none';
}

// Валидация формы
function validateForm(form) {
  let valid = true;
  form.querySelectorAll('[required]').forEach(input => {
    if (!input.value.trim()) {
      input.style.borderColor = 'red';
      valid = false;
    } else {
      input.style.borderColor = '';
    }
  });
  return valid;
}

// === ФИЛЬТРЫ ПОРТФОЛИО ===
document.querySelectorAll('.filters button').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filters button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const filter = btn.dataset.filter;
    document.querySelectorAll('.gallery .item').forEach(item => {
      const match = filter === 'all' || item.dataset.category === filter;
      item.style.display = match ? 'block' : 'none';
    });
  });
});

// === ПЛАВНАЯ ПРОКРУТКА ===
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', e => {
    const href = anchor.getAttribute('href');
    if (href === '#') return;
    e.preventDefault();
    const target = document.querySelector(href);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});