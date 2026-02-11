const BASE_URL = window.BASE_URL || 'http://localhost:8080'

async function ensureAuth() {
  const t = localStorage.getItem('token')
  if (!t) window.location.href = 'login.html'
  return t
}

async function fetchProducts() {
  const token = await ensureAuth()
  try {
    const res = await fetch(BASE_URL + '/products/', {
      headers: { 'Authorization': 'Bearer ' + token }
    })
    if (!res.ok) {
      document.getElementById('productsMsg').innerText = 'Failed to fetch products'
      return []
    }
    const data = await res.json()
    return data
  } catch (err) {
    document.getElementById('productsMsg').innerText = 'Network error'
    return []
  }
}

async function render() {
  const products = await fetchProducts()
  const tbody = document.getElementById('productsBody')
  tbody.innerHTML = ''
  if (!products || products.length === 0) {
    tbody.innerHTML = '<tr><td colspan="4">No products found.</td></tr>'
    return
  }
  products.forEach(p => {
    const tr = document.createElement('tr')
    const title = p.title || p.name || ''
    tr.innerHTML = `<td>${escapeHtml(title)}</td><td>${p.price ?? ''}</td><td>${escapeHtml(p.category ?? '')}</td><td>${escapeHtml((p.description || '').substring(0,120))}</td>`
    tbody.appendChild(tr)
  })
}

// basic escaping
function escapeHtml(str) {
  return String(str || '').replace(/[&<>"']/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s]))
}

// logout
document.addEventListener('DOMContentLoaded', () => {
  const logoutIds = ['logoutBtn','logoutBtn2','logoutBtn3','logoutBtn4']
  logoutIds.forEach(id => {
    const el = document.getElementById(id)
    if (el) el.addEventListener('click', () => { localStorage.removeItem('token'); window.location.href = 'login.html' })
  })
  if (document.getElementById('productsBody')) render()
})
