/**
 * Orders JavaScript
 * Handles orders functionality
 */

// Check authentication
if (!isAuthenticated()) {
    console.log('User not authenticated, redirecting to login');
    window.location.href = 'login.html';
}

// Load orders
async function loadOrders() {
    try {
        console.log('Loading orders...');
        console.log('Token exists:', !!getToken());
        const orders = await orderAPI.getOrders();
        console.log('Orders loaded:', orders);
        const container = document.getElementById('ordersList');
        
        if (orders.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 4rem;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">📦</div>
                    <h3 style="color: var(--text-dark); margin-bottom: 1rem;">No orders yet</h3>
                    <p style="color: var(--text-light); margin-bottom: 2rem;">Start ordering from your favorite restaurants</p>
                    <a href="restaurants.html" class="btn btn-primary">Browse Restaurants</a>
                </div>
            `;
            return;
        }
        
        container.innerHTML = orders.map(order => `
            <div style="background: white; padding: 2rem; border-radius: var(--radius-md); box-shadow: var(--shadow-sm); margin-bottom: 2rem;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;">
                    <div>
                        <h3 style="color: var(--text-dark); margin-bottom: 0.5rem;">Order #${order.id}</h3>
                        <p style="color: var(--text-light);">${formatDate(order.created_at)}</p>
                    </div>
                    <span class="order-status status-${order.status}">${order.status.replace('_', ' ').toUpperCase()}</span>
                </div>
                
                <div style="margin-bottom: 1.5rem;">
                    <h4 style="color: var(--text-dark); margin-bottom: 1rem;">Items</h4>
                    ${order.items.map(item => `
                        <div style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--border-color);">
                            <span style="color: var(--text-light);">${item.food_name} x ${item.quantity}</span>
                            <span style="color: var(--text-dark);">${formatPrice(item.total_price)}</span>
                        </div>
                    `).join('')}
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; padding: 1rem; background: var(--bg-light); border-radius: var(--radius-sm);">
                    <div>
                        <strong style="color: var(--text-dark);">Subtotal:</strong>
                        <span style="color: var(--text-light); margin-left: 0.5rem;">${formatPrice(order.total_amount)}</span>
                    </div>
                    <div>
                        <strong style="color: var(--text-dark);">Delivery:</strong>
                        <span style="color: var(--text-light); margin-left: 0.5rem;">${formatPrice(order.delivery_fee)}</span>
                    </div>
                    <div>
                        <strong style="color: var(--text-dark);">GST:</strong>
                        <span style="color: var(--text-light); margin-left: 0.5rem;">${formatPrice(order.gst_amount)}</span>
                    </div>
                    ${order.discount_amount > 0 ? `
                        <div>
                            <strong style="color: #24963f;">Discount:</strong>
                            <span style="color: #24963f; margin-left: 0.5rem;">-${formatPrice(order.discount_amount)}</span>
                        </div>
                    ` : ''}
                    <div>
                        <strong style="color: var(--text-dark);">Total:</strong>
                        <span style="color: var(--primary-color); margin-left: 0.5rem; font-weight: 700;">${formatPrice(order.final_amount)}</span>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 1rem; border-top: 1px solid var(--border-color);">
                    <div>
                        <strong style="color: var(--text-dark);">Delivery Address:</strong>
                        <span style="color: var(--text-light); margin-left: 0.5rem;">${order.delivery_address}</span>
                    </div>
                    <div>
                        <strong style="color: var(--text-dark);">Payment:</strong>
                        <span style="color: var(--text-light); margin-left: 0.5rem;">${order.payment_method.toUpperCase()}</span>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading orders:', error);
        if (error.message.includes('credentials') || error.message.includes('401')) {
            // Authentication error - clear token and redirect to login
            console.log('Authentication error, clearing token and redirecting to login');
            removeToken();
            removeCurrentUser();
            document.getElementById('ordersList').innerHTML = `
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
            document.getElementById('ordersList').innerHTML = `
                <div style="text-align: center; padding: 4rem;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">❌</div>
                    <h3 style="color: var(--text-dark); margin-bottom: 1rem;">Failed to load orders</h3>
                    <p style="color: var(--text-light); margin-bottom: 2rem;">${error.message}</p>
                    <button class="btn btn-primary" onclick="loadOrders()">Retry</button>
                </div>
            `;
        }
    }
}

// Initialize
loadOrders();
