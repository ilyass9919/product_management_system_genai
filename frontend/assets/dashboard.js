const BASE_URL = ''  // relative URLs — works on any host/IP

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token")
    if (!token) { window.location.href = "/login"; return }

    fetchProducts()

    const logoutBtn = document.getElementById("logoutBtn")
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            localStorage.removeItem("token")
            window.location.href = "/login"
        })
    }
})

async function fetchProducts() {
    const token = localStorage.getItem("token")
    try {
        const response = await fetch(`${BASE_URL}/products/`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        })
        if (!response.ok) throw new Error("Failed to fetch products")
        const data = await response.json()
        displayProducts(data)
    } catch (error) {
        console.error("Error:", error)
        localStorage.removeItem("token")
        window.location.href = "/login"
    }
}

function displayProducts(products) {
    // dashboard.html overrides this via window.displayProducts
    if (window.displayProducts && window.displayProducts !== displayProducts) {
        window.displayProducts(products)
        return
    }

    const tableBody = document.getElementById("productsTableBody")
    if (!tableBody) return
    tableBody.innerHTML = ""

    products.forEach((product, index) => {
        const row = `
            <tr>
                <td>${index + 1}</td>
                <td>${escapeHtml(product.title)}</td>
                <td>${escapeHtml(product.category || "General")}</td>
                <td>${escapeHtml(product.price ? '$' + product.price : "-")}</td>
                <td>${escapeHtml(product.description || "-")}</td>
            </tr>`
        tableBody.innerHTML += row
    })
}

function escapeHtml(str) {
    if (!str) return ""
    return String(str).replace(/[&<>"']/g, s => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[s]))
}
