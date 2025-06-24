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

loginForm.addEventListener('submit', function(e) {
  e.preventDefault();
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;
  if (isSignup) {
    const email = document.getElementById('email').value.trim();
    // Mock signup logic
    if (username && password && email) {
      loginMessage.style.color = '#2563eb';
      loginMessage.textContent = 'Account created! You can now log in.';
      switchToLogin();
    } else {
      loginMessage.style.color = '#e17055';
      loginMessage.textContent = 'Please fill in all fields.';
    }
  } else {
    // Mock login logic
    if (username === 'user' && password === 'pass') {
      loginMessage.style.color = '#2563eb';
      loginMessage.textContent = 'Login successful!';
      // Redirect or further logic here
    } else {
      loginMessage.style.color = '#e17055';
      loginMessage.textContent = 'Invalid username or password.';
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
