// theme.js: Handles dark mode toggle and system theme detection

const themeToggle = document.getElementById('theme-toggle');
const themeToggleIcon = document.getElementById('theme-toggle-icon');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

const MOON_SVG = `<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15.5 13.5A7 7 0 0 1 6.5 4.5a7 7 0 1 0 9 9z" fill="#222"/></svg>`;
const SUN_SVG = `<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="10" cy="10" r="5" fill="#FFD600" stroke="#222" stroke-width="2"/><g stroke="#222" stroke-width="2"><line x1="10" y1="1" x2="10" y2="4"/><line x1="10" y1="16" x2="10" y2="19"/><line x1="1" y1="10" x2="4" y2="10"/><line x1="16" y1="10" x2="19" y2="10"/><line x1="4.22" y1="4.22" x2="6.34" y2="6.34"/><line x1="15.78" y1="15.78" x2="13.66" y2="13.66"/><line x1="4.22" y1="15.78" x2="6.34" y2="13.66"/><line x1="15.78" y1="4.22" x2="13.66" y2="6.34"/></g></svg>`;

function setTheme(mode) {
  if (mode === 'dark') {
    document.body.classList.add('dark');
    themeToggleIcon.innerHTML = SUN_SVG;
    localStorage.setItem('theme', 'dark');
  } else {
    document.body.classList.remove('dark');
    themeToggleIcon.innerHTML = MOON_SVG;
    localStorage.setItem('theme', 'light');
  }
}

function detectSystemTheme() {
  return prefersDark.matches ? 'dark' : 'light';
}

function loadTheme() {
  const saved = localStorage.getItem('theme');
  if (saved) {
    setTheme(saved);
  } else {
    setTheme(detectSystemTheme());
  }
}

themeToggle.addEventListener('click', () => {
  if (document.body.classList.contains('dark')) {
    setTheme('light');
  } else {
    setTheme('dark');
  }
});

prefersDark.addEventListener('change', e => {
  if (!localStorage.getItem('theme')) {
    setTheme(e.matches ? 'dark' : 'light');
  }
});

window.addEventListener('DOMContentLoaded', loadTheme);
