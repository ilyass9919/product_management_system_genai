const BASE = (window.BASE_URL = '')  // relative URLs — works on any host/IP

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
          window.location.href = '/products'
        } else {
          msg.innerText = data.message || JSON.stringify(data)
          msg.className = 'text-danger'
          if (document.getElementById('loginLabel')) {
            document.getElementById('loginLabel').style.display = ''
            document.getElementById('loginSpinner').style.display = 'none'
          }
        }
      } catch (err) {
        const msg = document.getElementById('loginMsg')
        msg.innerText = 'Network error'
        msg.className = 'text-danger'
        if (document.getElementById('loginLabel')) {
          document.getElementById('loginLabel').style.display = ''
          document.getElementById('loginSpinner').style.display = 'none'
        }
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
          msg.innerText = '✓ Account created — redirecting to login…'
          msg.className = 'text-success'
          setTimeout(() => { window.location.href = '/login' }, 2000)
        } else {
          msg.innerText = data.message || JSON.stringify(data)
          msg.className = 'text-danger'
          if (document.getElementById('regLabel')) {
            document.getElementById('regLabel').style.display = ''
            document.getElementById('regSpinner').style.display = 'none'
          }
        }
      } catch (err) {
        const msg = document.getElementById('registerMsg')
        msg.innerText = 'Network error'
        msg.className = 'text-danger'
        if (document.getElementById('regLabel')) {
          document.getElementById('regLabel').style.display = ''
          document.getElementById('regSpinner').style.display = 'none'
        }
      }
    })
  }
})