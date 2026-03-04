const BASE = ''  // relative URLs — works on any host/IP

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('addProductForm')
  if (!form) return

  form.addEventListener('submit', async (e) => {
    e.preventDefault()

    const token = localStorage.getItem('token')
    if (!token) { window.location.href = '/login'; return }

    const payload = {
      title: document.getElementById('title').value,
      price: parseFloat(document.getElementById('price').value),
      category: document.getElementById('category').value,
      description: document.getElementById('description').value
    }

    try {
      const res = await fetch(`${BASE}/products/`, {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      const data = await res.json()
      const msg = document.getElementById('addMsg')

      if (res.ok) {
        msg.innerText = '✓ Product created successfully'
        msg.className = 'text-success'
        setTimeout(() => { window.location.href = '/products' }, 800)
      } else {
        msg.innerText = data.error || data.message || 'Permission Denied'
        msg.className = 'text-danger'
        // Reset button
        document.getElementById('submitLabel').style.display = ''
        document.getElementById('submitSpinner').style.display = 'none'
      }
    } catch (err) {
      console.error('Submission error:', err)
      const msg = document.getElementById('addMsg')
      msg.innerText = 'Network error'
      msg.className = 'text-danger'
      document.getElementById('submitLabel').style.display = ''
      document.getElementById('submitSpinner').style.display = 'none'
    }
  })
})