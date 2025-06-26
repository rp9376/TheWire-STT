let lastTimestamp = null;
let loading = false;
let hasMore = true;
const limit = 10;
const container = document.getElementById('news-container');
const loadingDiv = document.getElementById('loading');
const endMessage = document.getElementById('end-message');
const modalBg = document.getElementById('modal-bg');
const modal = document.getElementById('modal');
const closeModalBtn = document.getElementById('close-modal');
const modalTitle = document.getElementById('modal-title');
const modalDate = document.getElementById('modal-date');
const modalContent = document.getElementById('modal-content');
const modalFullStory = document.getElementById('modal-full-story');
const modalPrecedence = document.getElementById('modal-precedence');
const logoutBtn = document.getElementById('logout-btn');

// Remove event delegation, restore per-article click
async function fetchArticles() {
  if (loading || !hasMore) return;
  loading = true;
  loadingDiv.style.display = 'block';
  let url = `/api/news?limit=${limit}`;
  if (lastTimestamp) {
    url += `&before=${encodeURIComponent(lastTimestamp)}`;
  }
  const res = await fetch(url);
  const data = await res.json();
  data.forEach(article => {
    const div = document.createElement('div');
    // Add a class based on precedence
    let precedenceClass = article.precedence ? `precedence-${article.precedence.toLowerCase()}` : '';
    let labelClass = 'precedence-label';
    if (article.precedence && article.precedence.toLowerCase() !== 'routine') {
      labelClass += ' precedence-serious';
    } else if (article.precedence && article.precedence.toLowerCase() === 'routine') {
      labelClass += ' precedence-routine';
    }
    div.className = `news-article ${precedenceClass}`.trim();
    div.innerHTML = `<h2>${article.title}</h2><p>${article.content}</p><small>${article.published_at}</small><br><span class="${labelClass}">${article.precedence ? article.precedence : ''}</span>`;
    div.addEventListener('click', () => {
      console.log('Article clicked:', article);
      showModal(article);
    });
    container.appendChild(div);
  });
  if (data.length < limit) {
    hasMore = false;
    endMessage.style.display = 'block';
  }
  loading = false;
  loadingDiv.style.display = 'none';
  if (data.length > 0) lastTimestamp = data[data.length - 1].published_at;
}

function showModal(article) {
  modalTitle.textContent = article.title;
  // Show the date string as it is in the database
  modalDate.textContent = `${article.broadcast_date || ''} ${article.broadcast_time || ''}`.trim();
  modalContent.textContent = article.content;
  modalFullStory.textContent = article.full_story || article.text || article.content || '';
  if (article.precedence && article.precedence.toLowerCase() !== 'routine') {
    modalPrecedence.className = 'precedence-label precedence-serious';
  } else {
    modalPrecedence.className = 'precedence-label precedence-routine';
  }
  modalPrecedence.textContent = article.precedence ? article.precedence : '';
  modalBg.classList.add('active');
  console.log('modalBg classes:', modalBg.className);
}

function closeModal() {
  modalBg.classList.remove('active');
}

closeModalBtn.addEventListener('click', closeModal);
modalBg.addEventListener('click', function(e) {
  if (e.target === modalBg) closeModal();
});
window.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeModal();
});

function handleScroll() {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
    fetchArticles();
  }
}

window.addEventListener('scroll', handleScroll);
window.addEventListener('DOMContentLoaded', fetchArticles);

if (logoutBtn) {
  logoutBtn.addEventListener('click', async () => {
    try {
      await fetch('/api/logout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
    } catch (e) {}
    document.cookie = 'session_token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    window.location.href = '/login';
  });
}
