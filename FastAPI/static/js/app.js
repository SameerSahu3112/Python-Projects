/* ============================================
   Apple Store India — Client-Side JavaScript
   ============================================ */

(function () {
    'use strict';

    // ----- Toast Notification System -----
    const toastContainer = document.getElementById('toastContainer');

    function showToast(message, type = 'success') {
        if (!toastContainer) return;
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toastContainer.appendChild(toast);
        setTimeout(() => {
            if (toast.parentNode) toast.remove();
        }, 3200);
    }

    // ----- Indian Price Formatting -----
    function formatPrice(num) {
        if (typeof num !== 'number') num = parseFloat(num) || 0;
        const parts = num.toFixed(2).split('.');
        let intPart = parts[0];
        const decPart = parts[1];
        // Indian numbering: last 3, then groups of 2
        if (intPart.length > 3) {
            const last3 = intPart.slice(-3);
            let remaining = intPart.slice(0, -3);
            const groups = [];
            while (remaining.length > 2) {
                groups.unshift(remaining.slice(-2));
                remaining = remaining.slice(0, -2);
            }
            if (remaining) groups.unshift(remaining);
            intPart = groups.join(',') + ',' + last3;
        }
        return '₹' + intPart + '.' + decPart;
    }

    // ----- Helper: API Call -----
    async function apiCall(url, method = 'GET', body = null) {
        const options = {
            method,
            credentials: 'same-origin',
            headers: { 'Content-Type': 'application/json' },
        };
        if (body) options.body = JSON.stringify(body);
        const response = await fetch(url, options);
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || errorData.message || `Request failed (${response.status})`);
        }
        return response.json();
    }

    // ----- Update Badge Count -----
    function updateBadge(id, count) {
        const badge = document.getElementById(id);
        if (!badge) return;
        badge.textContent = count;
        if (count > 0) {
            badge.classList.remove('hidden');
        } else {
            badge.classList.add('hidden');
        }
    }

    // ----- Add to Cart -----
    async function addToCart(productId, quantity = 1) {
        try {
            const data = await apiCall('/api/cart/add', 'POST', {
                product_id: productId,
                quantity: quantity,
            });
            updateBadge('cartBadge', data.cart_count || 0);
            showToast('Added to bag!', 'success');
        } catch (err) {
            showToast(err.message || 'Failed to add to bag.', 'error');
        }
    }

    // ----- Update Cart Quantity -----
    async function updateCartQuantity(productId, quantity) {
        try {
            const data = await apiCall('/api/cart/update', 'PUT', {
                product_id: productId,
                quantity: quantity,
            });
            updateBadge('cartBadge', data.cart_count || 0);
            // Update line total and summary on page
            if (data.line_total !== undefined) {
                const lineEl = document.querySelector(`[data-line-total="${productId}"]`);
                if (lineEl) lineEl.textContent = formatPrice(data.line_total);
            }
            updateCartSummary(data);
            showToast('Bag updated.', 'info');
        } catch (err) {
            showToast(err.message || 'Failed to update bag.', 'error');
        }
    }

    // ----- Remove from Cart -----
    async function removeFromCart(productId) {
        try {
            const data = await apiCall(`/api/cart/remove/${productId}`, 'DELETE');
            updateBadge('cartBadge', data.cart_count || 0);
            // Remove row from DOM
            const row = document.querySelector(`[data-cart-item="${productId}"]`);
            if (row) row.remove();
            updateCartSummary(data);
            // If cart is empty, show empty state
            if (data.cart_count === 0) {
                const cartSection = document.querySelector('.cart-items-section');
                if (cartSection) {
                    cartSection.innerHTML = `
                        <div class="empty-state">
                            <div class="empty-state-icon">🛒</div>
                            <h2>Your bag is empty.</h2>
                            <p>Find something you love in our store.</p>
                            <a href="/products" class="btn btn-primary">Start Shopping</a>
                        </div>`;
                }
                const summary = document.querySelector('.cart-summary');
                if (summary) summary.style.display = 'none';
            }
            showToast('Item removed from bag.', 'info');
        } catch (err) {
            showToast(err.message || 'Failed to remove item.', 'error');
        }
    }

    // ----- Update Cart Summary -----
    function updateCartSummary(data) {
        if (data.subtotal !== undefined) {
            const el = document.getElementById('cartSubtotal');
            if (el) el.textContent = formatPrice(data.subtotal);
        }
        if (data.discount !== undefined) {
            const el = document.getElementById('cartDiscount');
            if (el) el.textContent = '−' + formatPrice(data.discount);
        }
        if (data.tax !== undefined) {
            const el = document.getElementById('cartTax');
            if (el) el.textContent = formatPrice(data.tax);
        }
        if (data.shipping !== undefined) {
            const el = document.getElementById('cartShipping');
            if (el) el.textContent = data.shipping === 0 ? 'FREE' : formatPrice(data.shipping);
        }
        if (data.total !== undefined) {
            const el = document.getElementById('cartTotal');
            if (el) el.textContent = formatPrice(data.total);
        }
    }

    // ----- Apply Coupon -----
    async function applyCoupon(code) {
        try {
            const data = await apiCall('/api/coupon/apply', 'POST', { code: code });
            showToast(data.message || 'Coupon applied!', 'success');
            updateCartSummary(data);
            // Show coupon info
            const couponInfo = document.getElementById('couponInfo');
            if (couponInfo && data.coupon_name) {
                couponInfo.classList.remove('hidden');
                couponInfo.innerHTML = `
                    <span>🎉 <strong>${data.coupon_name}</strong> applied — ${data.coupon_description || ''}</span>
                    <button class="btn btn-sm btn-danger" onclick="removeCoupon()">Remove</button>`;
            }
        } catch (err) {
            showToast(err.message || 'Invalid coupon code.', 'error');
        }
    }

    // ----- Remove Coupon (global) -----
    window.removeCoupon = async function () {
        try {
            const data = await apiCall('/api/coupon/remove', 'DELETE');
            showToast('Coupon removed.', 'info');
            updateCartSummary(data);
            const couponInfo = document.getElementById('couponInfo');
            if (couponInfo) couponInfo.classList.add('hidden');
        } catch (err) {
            showToast(err.message || 'Failed to remove coupon.', 'error');
        }
    };

    // ----- Wishlist Toggle -----
    async function toggleWishlist(productId, btn) {
        try {
            const data = await apiCall(`/api/wishlist/toggle/${productId}`, 'POST');
            updateBadge('wishlistBadge', data.wishlist_count || 0);
            if (data.action === 'added') {
                if (btn) {
                    btn.classList.add('wishlisted');
                    btn.innerHTML = '♥ Wishlisted';
                }
                showToast('Added to wishlist!', 'success');
            } else {
                if (btn) {
                    btn.classList.remove('wishlisted');
                    btn.innerHTML = '♡ Add to Wishlist';
                }
                showToast('Removed from wishlist.', 'info');
                // If on wishlist page, remove the card
                const card = btn ? btn.closest('.product-card') : null;
                if (card && document.querySelector('.wishlist-page')) {
                    card.remove();
                    // Check if empty
                    const remaining = document.querySelectorAll('.wishlist-page .product-card');
                    if (remaining.length === 0) {
                        const grid = document.querySelector('.wishlist-page .product-grid');
                        if (grid) {
                            grid.innerHTML = `
                                <div class="empty-state" style="grid-column: 1/-1;">
                                    <div class="empty-state-icon">♡</div>
                                    <h2>Your wishlist is empty.</h2>
                                    <p>Save items you love to your wishlist.</p>
                                    <a href="/products" class="btn btn-primary">Explore Products</a>
                                </div>`;
                        }
                    }
                }
            }
        } catch (err) {
            showToast(err.message || 'Failed to update wishlist.', 'error');
        }
    }

    // ----- Review Submission -----
    async function submitReview(productId, formData) {
        try {
            const data = await apiCall('/api/reviews', 'POST', {
                product_id: productId,
                rating: parseInt(formData.rating),
                title: formData.title,
                text: formData.text,
            });
            showToast('Review submitted!', 'success');
            setTimeout(() => location.reload(), 1000);
        } catch (err) {
            showToast(err.message || 'Failed to submit review.', 'error');
        }
    }

    // ----- Quantity Selector -----
    function setupQuantitySelectors() {
        document.querySelectorAll('.quantity-selector').forEach((selector) => {
            const minusBtn = selector.querySelector('.qty-minus');
            const plusBtn = selector.querySelector('.qty-plus');
            const input = selector.querySelector('.qty-input');

            if (minusBtn) {
                minusBtn.addEventListener('click', () => {
                    let val = parseInt(input.value) || 1;
                    if (val > 1) {
                        input.value = val - 1;
                        input.dispatchEvent(new Event('change'));
                    }
                });
            }

            if (plusBtn) {
                plusBtn.addEventListener('click', () => {
                    let val = parseInt(input.value) || 1;
                    const max = parseInt(input.getAttribute('max')) || 99;
                    if (val < max) {
                        input.value = val + 1;
                        input.dispatchEvent(new Event('change'));
                    }
                });
            }
        });
    }

    // ----- Mobile Menu Toggle -----
    function setupMobileMenu() {
        const hamburger = document.getElementById('hamburger');
        const navLinks = document.getElementById('navLinks');
        if (hamburger && navLinks) {
            hamburger.addEventListener('click', () => {
                hamburger.classList.toggle('active');
                navLinks.classList.toggle('show');
            });
        }
    }

    // ----- Search Bar Toggle -----
    function setupSearchToggle() {
        const searchToggle = document.getElementById('searchToggle');
        const searchBar = document.getElementById('searchBar');
        const searchInput = document.getElementById('searchInput');
        if (searchToggle && searchBar) {
            searchToggle.addEventListener('click', () => {
                searchBar.classList.toggle('show');
                if (searchBar.classList.contains('show') && searchInput) {
                    searchInput.focus();
                }
            });
        }
    }

    // ----- User Dropdown -----
    function setupUserDropdown() {
        const userToggle = document.getElementById('userToggle');
        const dropdownMenu = document.getElementById('dropdownMenu');
        if (userToggle && dropdownMenu) {
            userToggle.addEventListener('click', (e) => {
                e.stopPropagation();
                dropdownMenu.classList.toggle('show');
            });
            document.addEventListener('click', () => {
                dropdownMenu.classList.remove('show');
            });
        }
    }

    // ----- Event Delegation -----
    document.addEventListener('click', function (e) {
        // Add to Cart buttons
        const addToCartBtn = e.target.closest('[data-add-to-cart]');
        if (addToCartBtn) {
            e.preventDefault();
            const productId = addToCartBtn.getAttribute('data-add-to-cart');
            // Try to read quantity from a nearby quantity input
            const qtyInput = document.querySelector(`.qty-input[data-product-id="${productId}"]`);
            const qty = qtyInput ? parseInt(qtyInput.value) || 1 : 1;
            addToCart(productId, qty);
            return;
        }

        // Remove from Cart
        const removeBtn = e.target.closest('[data-remove-from-cart]');
        if (removeBtn) {
            e.preventDefault();
            const productId = removeBtn.getAttribute('data-remove-from-cart');
            removeFromCart(productId);
            return;
        }

        // Wishlist Toggle
        const wishlistBtn = e.target.closest('[data-wishlist-toggle]');
        if (wishlistBtn) {
            e.preventDefault();
            const productId = wishlistBtn.getAttribute('data-wishlist-toggle');
            toggleWishlist(productId, wishlistBtn);
            return;
        }
    });

    // Cart quantity change handler (event delegation)
    document.addEventListener('change', function (e) {
        if (e.target.classList.contains('cart-qty-input')) {
            const productId = e.target.getAttribute('data-product-id');
            const quantity = parseInt(e.target.value) || 1;
            if (quantity < 1) {
                e.target.value = 1;
                return;
            }
            updateCartQuantity(productId, quantity);
        }
    });

    // Coupon form
    const couponForm = document.getElementById('couponForm');
    if (couponForm) {
        couponForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const codeInput = couponForm.querySelector('input[name="coupon_code"]');
            if (codeInput && codeInput.value.trim()) {
                applyCoupon(codeInput.value.trim());
            }
        });
    }

    // Review form
    const reviewForm = document.getElementById('reviewForm');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const productId = reviewForm.getAttribute('data-product-id');
            const formData = {
                rating: reviewForm.querySelector('[name="rating"]').value,
                title: reviewForm.querySelector('[name="title"]').value,
                text: reviewForm.querySelector('[name="text"]').value,
            };
            if (!formData.rating || !formData.title) {
                showToast('Please fill in rating and title.', 'error');
                return;
            }
            submitReview(productId, formData);
        });
    }

    // Address / payment option selection
    document.querySelectorAll('.address-option, .payment-option').forEach((option) => {
        option.addEventListener('click', function () {
            const group = this.closest('.checkout-section');
            if (group) {
                group.querySelectorAll('.address-option, .payment-option').forEach((o) =>
                    o.classList.remove('selected')
                );
            }
            this.classList.add('selected');
            const radio = this.querySelector('input[type="radio"]');
            if (radio) radio.checked = true;
        });
    });

    // ----- Filter sidebar toggle on mobile -----
    const filterToggleBtn = document.getElementById('filterToggle');
    const sidebar = document.querySelector('.products-sidebar');
    if (filterToggleBtn && sidebar) {
        filterToggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('show');
        });
    }

    // ----- Initialisation -----
    setupMobileMenu();
    setupSearchToggle();
    setupUserDropdown();
    setupQuantitySelectors();

    // Expose helpers globally
    window.showToast = showToast;
    window.formatPrice = formatPrice;
    window.addToCart = addToCart;
})();
