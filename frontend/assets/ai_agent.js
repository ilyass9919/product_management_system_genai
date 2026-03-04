const BASE_AI = ''  // relative URLs — works on any host/IP

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('aiForm')
  if (!form) return

  form.addEventListener('submit', async (e) => {
    e.preventDefault()
    const token = localStorage.getItem('token')
    if (!token) return window.location.href = '/login'

    const q = document.getElementById('aiQuery').value
    const out = document.getElementById('aiResponse')

    try {
      const res = await fetch(BASE_AI + '/ai/chat', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + token,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: q })
      })

      const resp = await res.json()

      if (res.ok) {
        out.textContent = resp.reply || JSON.stringify(resp, null, 2)
      } else {
        out.textContent = 'Error: ' + (resp.error || resp.message || 'Unknown error')
      }
    } catch (err) {
      out.textContent = 'Network error — could not reach AI service.'
      console.error(err)
    }
  })
})