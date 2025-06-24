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
const MOCK_FULL_STORY = `This is the full story of the news article.\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque euismod, nisi eu consectetur consectetur, nisl nisi consectetur nisi, eu consectetur nisl nisi euismod nisi. Vivamus euismod, nisi eu consectetur consectetur, nisl nisi consectetur nisi, eu consectetur nisl nisi euismod nisi.\n\nSed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam.`;

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
    div.className = 'news-article';
    div.innerHTML = `<h2>${article.title}</h2><p>${article.content}</p><small>${new Date(article.published_at).toLocaleString()}</small>`;
    div.addEventListener('click', () => showModal(article));
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
  modalDate.textContent = new Date(article.published_at).toLocaleString();
  modalContent.textContent = article.content;
  modalFullStory.textContent = MOCK_FULL_STORY;
  modalBg.classList.add('active');
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
