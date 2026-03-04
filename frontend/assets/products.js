const BASE_URL = ''  // relative URLs — works on any host/IP

async function fetchProducts() {
    const token = localStorage.getItem('token')
    if (!token) { window.location.href = '/login'; return [] }
    try {
        const res = await fetch(`${BASE_URL}/products/`, {
            headers: { 'Authorization': 'Bearer ' + token }
        })
        if (!res.ok) throw new Error('Failed to fetch')
        return await res.json()
    } catch (err) {
        console.error('Fetch error:', err)
        return []
    }
}

async function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) return
    const token = localStorage.getItem('token')
    try {
        const res = await fetch(`${BASE_URL}/products/${productId}`, {
            method: 'DELETE',
            headers: { 'Authorization': 'Bearer ' + token }
        })
        if (res.ok) {
            render()
        } else {
            const data = await res.json()
            alert(data.error || 'Delete failed')
        }
    } catch (err) {
        console.error('Delete error:', err)
        alert('Network error while deleting')
    }
}

async function render() {
    const products = await fetchProducts()
    const tbody = document.getElementById('productsBody')
    if (!tbody) return

    tbody.innerHTML = ''

    if (!products || products.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="5" style="text-align:center;padding:3rem;color:var(--text-muted);">
              <i class="bi bi-inbox" style="font-size:1.5rem;display:block;margin-bottom:0.5rem;"></i>
              No products found.
            </td>
          </tr>`
        return
    }

    products.forEach(p => {
        const tr = document.createElement('tr')
        tr.innerHTML = `
          <td class="td-title">${escapeHtml(p.title)}</td>
          <td class="td-price">$${p.price ? parseFloat(p.price).toFixed(2) : '0.00'}</td>
          <td><span class="badge-category">${escapeHtml(p.category || 'General')}</span></td>
          <td style="max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
            ${escapeHtml(p.description || '—')}
          </td>
          <td style="text-align:right;padding-right:1.25rem;">
            <button class="btn btn-danger-ghost delete-btn" data-id="${p.id}">
              <i class="bi bi-trash"></i>
            </button>
          </td>`
        tbody.appendChild(tr)
    })
}

document.addEventListener('DOMContentLoaded', () => {
    render()

    const tbody = document.getElementById('productsBody')
    if (tbody) {
        tbody.addEventListener('click', (e) => {
            const btn = e.target.closest('.delete-btn')
            if (btn) deleteProduct(btn.getAttribute('data-id'))
        })
    }

    const logoutBtn = document.getElementById('logoutBtn')
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('token')
            window.location.href = '/login'
        })
    }
})

function escapeHtml(str) {
    return String(str || '').replace(/[&<>"']/g, s => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[s]))
}