document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");

    // If no token → user must login
    if (!token) {
        window.location.href = "/login.html";
        return;
    }

    // Load products on dashboard load
    fetchProducts();

    // Logout button
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            localStorage.removeItem("token");
            window.location.href = "/login.html";
        });
    }
});

// =======================
// Fetch Products
// =======================
async function fetchProducts() {
    const token = localStorage.getItem("token");

    try {
        const response = await fetch("http://localhost:8080/products", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch products");
        }

        const data = await response.json();
        displayProducts(data);

    } catch (error) {
        console.error("Error:", error);
        alert("Failed to load products. Please login again.");
        localStorage.removeItem("token");
        window.location.href = "/login.html";
    }
}

// =======================
// Display Products in UI
// =======================
function displayProducts(products) {
    const tableBody = document.getElementById("productsTableBody");
    tableBody.innerHTML = "";

    products.forEach((product, index) => {
        const row = `
            <tr>
                <td>${index + 1}</td>
                <td>${product.name}</td>
                <td>${product.reference || "-"}</td>
                <td>${product.category || "-"}</td>
                <td>${product.description || "-"}</td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
}




/*
const BASE_D = window.BASE_URL || 'http://localhost:8080'

async function loadDashboard() {
  const token = localStorage.getItem('token')
  if (!token) return window.location.href = 'login.html'
  try {
    const res = await fetch(BASE_D + '/products/', { headers: { 'Authorization': 'Bearer ' + token } })
    if (!res.ok) return
    const products = await res.json()
    document.getElementById('totalProducts').innerText = products.length

    // categories
    const cats = {}
    products.forEach(p => { const c = p.category || 'Uncategorized'; cats[c] = (cats[c] || 0) + 1 })
    const labels = Object.keys(cats)
    const vals = labels.map(l => cats[l])
    const ctx = document.getElementById('catChart').getContext('2d')
    if (window.catChartInstance) window.catChartInstance.destroy()
    window.catChartInstance = new Chart(ctx, { type: 'bar', data: { labels, datasets: [{ label: 'Products', data: vals }] } })

    // latest
    const latest = products.slice(-5).reverse()
    const ul = document.getElementById('latestList')
    ul.innerHTML = ''
    latest.forEach(p => {
      const li = document.createElement('li')
      li.className = 'list-group-item'
      li.innerText = (p.title || '') + ' — ' + (p.category || '')
      ul.appendChild(li)
    })
  } catch (err) {
    // noop
  }
}

document.addEventListener('DOMContentLoaded', () => { loadDashboard() })
*/