/**
 * Cart JavaScript
 * Handles cart functionality
 */

// Check authentication
if (!isAuthenticated()) {
    window.location.href = 'login.html';
}

// Load cart
async function loadCart() {
    try {
        console.log('Loading cart...');
        console.log('Token exists:', !!getToken());
        const cart = await cartAPI.getCart();
        const container = document.getElementById('cartContent');
        
        if (cart.items.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 4rem;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">🛒</div>
                    <h3 style="color: var(--text-dark); margin-bottom: 1rem;">Your cart is empty</h3>
                    <p style="color: var(--text-light); margin-bottom: 2rem;">Add items from restaurants to get started</p>
                    <a href="restaurants.html" class="btn btn-primary">Browse Restaurants</a>
                </div>
            `;
            setCartCount(0);
            return;
        }
        
        let itemsHtml = cart.items.map(item => `
            <div class="cart-item">
                <img src="${item.food_image || 'https://via.placeholder.com/100'}" alt="${item.food_name}">
                <div class="cart-item-details">
                    <h4>${item.food_name}</h4>
                    <p>${item.restaurant_name}</p>
                    <p style="font-weight: 700; color: var(--text-dark); margin-top: 0.5rem;">${formatPrice(item.food_price)}</p>
                    <div class="cart-item-controls">
                        <button class="quantity-btn" onclick="updateQuantity(${item.id}, ${item.quantity - 1})">-</button>
                        <span style="font-weight: 600; color: var(--text-dark);">${item.quantity}</span>
                        <button class="quantity-btn" onclick="updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                        <button class="btn btn-secondary btn-sm" style="margin-left: auto;" onclick="removeItem(${item.id})">Remove</button>
                    </div>
                </div>
            </div>
        `).join('');
        
        const deliveryFee = 40;
        const gstRate = 0.05;
        const gstAmount = cart.total_amount * gstRate;
        const finalAmount = cart.total_amount + deliveryFee + gstAmount;
        
        itemsHtml += `
            <div class="cart-summary">
                <h3 style="margin-bottom: 1.5rem; color: var(--text-dark);">Order Summary</h3>
                <div class="summary-row">
                    <span>Subtotal</span>
                    <span>${formatPrice(cart.total_amount)}</span>
                </div>
                <div class="summary-row">
                    <span>Delivery Fee</span>
                    <span>${formatPrice(deliveryFee)}</span>
                </div>
                <div class="summary-row">
                    <span>GST (5%)</span>
                    <span>${formatPrice(gstAmount)}</span>
                </div>
                <div class="summary-row">
                    <span>Total</span>
                    <span>${formatPrice(finalAmount)}</span>
                </div>
                <button class="btn btn-primary" style="width: 100%; margin-top: 1.5rem;" onclick="proceedToCheckout()">
                    Proceed to Checkout
                </button>
            </div>
        `;
        
        container.innerHTML = itemsHtml;
        setCartCount(cart.item_count);
    } catch (error) {
        console.error('Error loading cart:', error);
        if (error.message.includes('credentials') || error.message.includes('401')) {
            // Authentication error - clear token and redirect to login
            console.log('Authentication error, clearing token and redirecting to login');
            removeToken();
            removeCurrentUser();
            document.getElementById('cartContent').innerHTML = `
                <div style="text-align: center; padding: 4rem;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">🔐</div>
                    <h3 style="color: var(--text-dark); margin-bottom: 1rem;">Session Expired</h3>
                    <p style="color: var(--text-light); margin-bottom: 2rem;">Please login again to continue</p>
                    <a href="login.html" class="btn btn-primary">Login</a>
                </div>
            `;
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            document.getElementById('cartContent').innerHTML = '<p style="text-align: center; color: var(--text-light);">Failed to load cart</p>';
        }
    }
}

// Update quantity
async function updateQuantity(itemId, quantity) {
    if (quantity <= 0) {
        await removeItem(itemId);
        return;
    }
    
    try {
        await cartAPI.updateCartItem(itemId, quantity);
        showToast('Cart updated', 'success');
        loadCart();
    } catch (error) {
        console.error('Error updating cart:', error);
        showToast('Failed to update cart', 'error');
    }
}

// Remove item
async function removeItem(itemId) {
    try {
        await cartAPI.removeCartItem(itemId);
        showToast('Item removed from cart', 'success');
        loadCart();
    } catch (error) {
        console.error('Error removing item:', error);
        showToast('Failed to remove item', 'error');
    }
}

// Clear cart
async function clearCart() {
    try {
        await cartAPI.clearCart();
        showToast('Cart cleared', 'success');
        loadCart();
    } catch (error) {
        console.error('Error clearing cart:', error);
        showToast('Failed to clear cart', 'error');
    }
}

// Proceed to checkout
function proceedToCheckout() {
    window.location.href = 'checkout.html';
}

// Initialize
loadCart();
