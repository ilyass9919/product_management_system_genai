const BASE_URL = window.BASE_URL || 'http://localhost:8080'


async function fetchProducts() {
  const token = localStorage.getItem('token')
  if (!token) {
    window.location.href = '/login'
    return []
  }

  try {
    const res = await fetch(BASE_URL + '/products/', {
      headers: { 'Authorization': 'Bearer ' + token }
    })
    if (!res.ok) return []
    return await res.json()
  } catch (err) {
    console.error('Fetch error:', err)
    return []
  }
}

async function render() {
  const products = await fetchProducts()
  const tbody = document.getElementById('productsBody')
  
  if (!tbody) return 

  tbody.innerHTML = ''
  if (!products || products.length === 0) {
    tbody.innerHTML = '<tr><td colspan="4" class="text-center">No products found.</td></tr>'
    return
  }
  
  products.forEach(p => {
    const tr = document.createElement('tr')
    tr.innerHTML = `
      <td>${escapeHtml(p.title)}</td>
      <td>$${p.price ? p.price.toFixed(2) : '0.00'}</td>
      <td>${escapeHtml(p.category)}</td>
      <td>${escapeHtml(p.description)}</td>
    `
    tbody.appendChild(tr)
  })
}


function escapeHtml(str) {
  return String(str || '').replace(/[&<>"']/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s]))
}

document.addEventListener('DOMContentLoaded', () => {
  const logoutIds = ['logoutBtn', 'logoutBtn2', 'logoutBtn3']
  logoutIds.forEach(id => {
    const el = document.getElementById(id)
    if (el) { 
      el.addEventListener('click', () => {
        localStorage.removeItem('token')
        window.location.href = '/login'
      })
    }
  })

  // Only run render if we are actually on the products page
  if (document.getElementById('productsBody')) {
    render()
  }
})