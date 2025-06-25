// login.js: Handles login and signup logic

// Set to false to disable account creation
const ALLOW_SIGNUP = true;

const loginForm = document.getElementById('login-form');
const signupBtn = document.getElementById('signup-btn');
const loginMessage = document.getElementById('login-message');

let isSignup = false;

function switchToSignup() {
  isSignup = true;
  loginForm.querySelector('button[type="submit"]').textContent = 'Create Account';
  signupBtn.textContent = 'Back to Login';
  document.getElementById('username').value = '';
  document.getElementById('password').value = '';
  // Add email field if not present
  if (!document.getElementById('email')) {
    const emailInput = document.createElement('input');
    emailInput.type = 'email';
    emailInput.id = 'email';
    emailInput.placeholder = 'Email';
    emailInput.required = true;
    emailInput.autocomplete = 'email';
    loginForm.insertBefore(emailInput, loginForm.children[1]);
  }
  // Change title to Sign Up
  const titleSpans = document.querySelectorAll('.login-title span');
  if (titleSpans.length > 1) titleSpans[1].textContent = 'Sign Up';
  loginMessage.textContent = '';
}

function switchToLogin() {
  isSignup = false;
  loginForm.querySelector('button[type="submit"]').textContent = 'Log In';
  signupBtn.textContent = 'Create Account';
  document.getElementById('username').value = '';
  document.getElementById('password').value = '';
  // Remove email field if present
  const emailInput = document.getElementById('email');
  if (emailInput) emailInput.remove();
  // Change title to Login
  const titleSpans = document.querySelectorAll('.login-title span');
  if (titleSpans.length > 1) titleSpans[1].textContent = 'Login';
  loginMessage.textContent = '';
}

if (!ALLOW_SIGNUP) {
  signupBtn.style.display = 'none';
}

loginForm.addEventListener('submit', async function(e) {
  e.preventDefault();
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;
  if (isSignup) {
    const email = document.getElementById('email').value.trim();
    if (username && password && email) {
      // Real signup logic
      const res = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, email })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        loginMessage.style.color = '#2563eb';
        loginMessage.textContent = data.message || 'Account created! You can now log in.';
        switchToLogin();
      } else {
        loginMessage.style.color = '#e17055';
        loginMessage.textContent = data.message || data.error || 'Signup failed.';
      }
    } else {
      loginMessage.style.color = '#e17055';
      loginMessage.textContent = 'Please fill in all fields.';
    }
  } else {
    // Real login logic
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      loginMessage.style.color = '#2563eb';
      loginMessage.textContent = 'Login successful! Redirecting...';
      // Store token in localStorage for API requests
      if (data.token) localStorage.setItem('session_token', data.token);
      setTimeout(() => { window.location.href = '/news'; }, 800);
    } else {
      loginMessage.style.color = '#e17055';
      loginMessage.textContent = data.message || 'Invalid username or password.';
    }
  }
});

signupBtn.addEventListener('click', function() {
  if (!ALLOW_SIGNUP) return;
  if (!isSignup) {
    switchToSignup();
  } else {
    switchToLogin();
  }
});
