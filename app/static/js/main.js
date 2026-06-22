// PUSAT SEMBAKO - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Update cart count on page load
    updateCartCount();

    // Setup CSRF token for AJAX requests
    const token = document.querySelector('meta[name="csrf-token"]')?.content;
    if (token) {
        setupAjaxToken(token);
    }
});

// Update cart count display
function updateCartCount() {
    fetch('/api/cart/count')
        .then(response => response.json())
        .then(data => {
            const cartCount = document.getElementById('cart-count');
            if (cartCount) {
                cartCount.textContent = data.count;
                if (data.count > 0) {
                    cartCount.style.display = 'inline-block';
                } else {
                    cartCount.style.display = 'none';
                }
            }
        })
        .catch(error => console.log('Error updating cart count:', error));
}

// Add product to cart
function addToCart(variantId, qty = 1) {
    const formData = new FormData();
    formData.append('variant_id', variantId);
    formData.append('qty', qty);

    fetch('/cart/add', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('success', 'Produk berhasil ditambahkan ke keranjang');
            updateCartCount();
        } else {
            showToast('error', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('error', 'Terjadi kesalahan');
    });
}

// Remove product from cart
function removeFromCart(variantId) {
    if (confirm('Yakin ingin menghapus produk ini dari keranjang?')) {
        const formData = new FormData();
        formData.append('variant_id', variantId);

        fetch('/cart/remove', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('success', data.message);
                location.reload();
            } else {
                showToast('error', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('error', 'Terjadi kesalahan');
        });
    }
}

// Update cart item quantity
function updateCartQty(variantId, qty) {
    if (qty < 1) {
        removeFromCart(variantId);
        return;
    }

    const formData = new FormData();
    formData.append('variant_id', variantId);
    formData.append('qty', qty);

    fetch('/cart/update', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            showToast('error', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('error', 'Terjadi kesalahan');
    });
}

// Clear cart
function clearCart() {
    if (confirm('Yakin ingin mengosongkan seluruh keranjang?')) {
        fetch('/cart/clear', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('success', data.message);
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

// Real-time product search
function searchProducts(query) {
    if (query.length < 2) {
        document.getElementById('search-results').innerHTML = '';
        return;
    }

    fetch(`/products/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            let html = '<ul class="list-group">';
            data.forEach(product => {
                html += `
                    <li class="list-group-item">
                        <a href="${product.url}" class="text-decoration-none">
                            <strong>${product.nama}</strong><br>
                            <small class="text-muted">${product.category}</small>
                        </a>
                    </li>
                `;
            });
            html += '</ul>';
            document.getElementById('search-results').innerHTML = html;
        })
        .catch(error => console.error('Error:', error));
}

// Show toast notification
function showToast(type, message) {
    // Create toast element
    const toastHtml = `
        <div class="alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show" role="alert" style="position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    const toastContainer = document.createElement('div');
    toastContainer.innerHTML = toastHtml;
    document.body.appendChild(toastContainer);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        toastContainer.remove();
    }, 5000);
}

// Setup AJAX CSRF token
function setupAjaxToken(token) {
    // For future CSRF token implementation
}

// Logout confirmation
function confirmLogout() {
    if (confirm('Yakin ingin logout?')) {
        window.location.href = location.pathname + '/logout';
    }
}

// Format currency
function formatCurrency(value) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(value);
}

// Validate form
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        return form.checkValidity() === false ? false : true;
    }
    return true;
}

// Load product variants
function loadVariants(productId, selectId) {
    fetch(`/api/products/${productId}/variants`)
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById(selectId);
            select.innerHTML = '<option value="">Pilih Varian...</option>';
            data.forEach(variant => {
                const option = document.createElement('option');
                option.value = variant.id;
                option.textContent = `${variant.nama} (${variant.ukuran}) - ${formatCurrency(variant.harga)}`;
                option.setAttribute('data-stok', variant.stok);
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Check stock availability
function checkStockAvailability(selectId) {
    const select = document.getElementById(selectId);
    const selectedOption = select.options[select.selectedIndex];
    const stok = parseInt(selectedOption.getAttribute('data-stok')) || 0;
    const qtyInput = document.getElementById('qty');
    
    if (qtyInput && stok > 0) {
        qtyInput.max = stok;
        qtyInput.disabled = false;
    } else if (qtyInput) {
        qtyInput.disabled = true;
    }
}

// Filter products
function filterProducts(category, sort) {
    let url = '/products?';
    if (category) url += `category=${category}&`;
    if (sort) url += `sort=${sort}`;
    window.location.href = url;
}
