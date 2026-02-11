const BASE = (window.BASE_URL = window.BASE_URL || 'http://localhost:8080')

// LOGIN & REGISTER handlers
document.addEventListener('DOMContentLoaded', () => {
  // Login
  const loginForm = document.getElementById('loginForm')
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault()
      const email = document.getElementById('email').value
      const password = document.getElementById('password').value
      try {
        const res = await fetch(BASE + '/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        })
        const data = await res.json()
        const msg = document.getElementById('loginMsg')
        if (res.ok && data.token) {
          localStorage.setItem('token', data.token)
          window.location.href = 'products.html'
        } else {
          msg.innerText = data.message || JSON.stringify(data)
          msg.className = 'text-danger'
        }
      } catch (err) {
        const msg = document.getElementById('loginMsg')
        msg.innerText = 'Network error'
        msg.className = 'text-danger'
      }
    })
  }

  // Register
  const registerForm = document.getElementById('registerForm')
  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault()
      const payload = {
        username: document.getElementById('username').value,
        name: document.getElementById('name').value,
        email: document.getElementById('emailReg').value,
        password: document.getElementById('passwordReg').value
      }
      try {
        const res = await fetch(BASE + '/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
        const data = await res.json()
        const msg = document.getElementById('registerMsg')
        if (res.ok) {
          msg.innerText = 'Account created — please login'
          msg.className = 'text-success'
        } else {
          msg.innerText = data.message || JSON.stringify(data)
          msg.className = 'text-danger'
        }
      } catch (err) {
        const msg = document.getElementById('registerMsg')
        msg.innerText = 'Network error'
        msg.className = 'text-danger'
      }
    })
  }
})
