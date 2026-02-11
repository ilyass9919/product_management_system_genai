const BASE = window.BASE_URL || 'http://localhost:8080'

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('addProductForm')
  if (!form) return
  form.addEventListener('submit', async (e) => {
    e.preventDefault()
    const token = localStorage.getItem('token')
    if (!token) return window.location.href = 'login.html'

    const payload = {
      title: document.getElementById('title').value,
      price: parseFloat(document.getElementById('price').value),
      category: document.getElementById('category').value,
      description: document.getElementById('description').value
    }

    try {
      const res = await fetch(BASE + '/products/', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      const data = await res.json()
      const msg = document.getElementById('addMsg')
      if (res.ok) {
        msg.innerText = 'Created'
        msg.className = 'text-success'
        setTimeout(() => window.location.href = 'products.html', 800)
      } else {
        msg.innerText = data.message || JSON.stringify(data)
        msg.className = 'text-danger'
      }
    } catch (err) {
      const msg = document.getElementById('addMsg')
      msg.innerText = 'Network error'
      msg.className = 'text-danger'
    }
  })
})
