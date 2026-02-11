const BASE_AI = window.BASE_URL || 'http://localhost:8080'

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('aiForm')
  if (!form) return
  form.addEventListener('submit', async (e) => {
    e.preventDefault()
    const token = localStorage.getItem('token')
    if (!token) return window.location.href = 'login.html'
    const q = document.getElementById('aiQuery').value
    const endpoints = ['/ai/query', '/ai']
    let resp = null
    for (const ep of endpoints) {
      try {
        const res = await fetch(BASE_AI + ep, {
          method: 'POST',
          headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: q })
        })
        if (res.ok) { resp = await res.json(); break }
      } catch (err) { /* try next */ }
    }
    const out = document.getElementById('aiResponse')
    if (!resp) out.innerText = 'AI service did not respond or returned an error.'
    else out.innerText = (resp.result || resp.answer || JSON.stringify(resp))
  })
})
