/**
 * API Client for Foodie Application
 * Handles all backend communication using Fetch API
 */

const API_BASE_URL = 'http://localhost:8000';

/**
 * Get JWT token from localStorage
 */
function getToken() {
    return localStorage.getItem('token');
}

/**
 * Set JWT token in localStorage
 */
function setToken(token) {
    localStorage.setItem('token', token);
}

/**
 * Remove JWT token from localStorage
 */
function removeToken() {
    localStorage.removeItem('token');
}

/**
 * Get current user from localStorage
 */
function getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

/**
 * Set current user in localStorage
 */
function setCurrentUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

/**
 * Remove current user from localStorage
 */
function removeCurrentUser() {
    localStorage.removeItem('user');
}

/**
 * Make API request with authentication
 */
async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
        console.log('Sending request with token for:', endpoint);
    } else {
        console.log('Sending request without token for:', endpoint);
    }

    const config = {
        ...options,
        headers,
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('API Error Response:', errorText);
            try {
                const error = JSON.parse(errorText);
                throw new Error(error.detail || 'Something went wrong');
            } catch {
                throw new Error(errorText || 'Something went wrong');
            }
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Authentication API
 */
const authAPI = {
    async register(userData) {
        const response = await apiRequest('/api/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData),
        });
        
        setToken(response.access_token);
        setCurrentUser(response.user);
        
        return response;
    },

    async login(email, password) {
        const response = await apiRequest('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        });
        
        setToken(response.access_token);
        setCurrentUser(response.user);
        
        return response;
    },

    logout() {
        removeToken();
        removeCurrentUser();
    },

    async getCurrentUser() {
        return await apiRequest('/api/auth/me');
    },
};

/**
 * Restaurant API
 */
const restaurantAPI = {
    async getRestaurants(params = {}) {
        // Filter out null and undefined values
        const filteredParams = Object.fromEntries(
            Object.entries(params).filter(([_, value]) => value !== null && value !== undefined && value !== '')
        );
        const queryString = new URLSearchParams(filteredParams).toString();
        return await apiRequest(`/api/restaurants?${queryString}`);
    },

    async getRestaurant(id) {
        return await apiRequest(`/api/restaurants/${id}`);
    },

    async createRestaurant(data) {
        return await apiRequest('/api/restaurants', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    async updateRestaurant(id, data) {
        return await apiRequest(`/api/restaurants/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    async deleteRestaurant(id) {
        return await apiRequest(`/api/restaurants/${id}`, {
            method: 'DELETE',
        });
    },
};

/**
 * Food API
 */
const foodAPI = {
    async getFoods(params = {}) {
        // Filter out null and undefined values
        const filteredParams = Object.fromEntries(
            Object.entries(params).filter(([_, value]) => value !== null && value !== undefined && value !== '')
        );
        const queryString = new URLSearchParams(filteredParams).toString();
        return await apiRequest(`/api/foods?${queryString}`);
    },

    async getFood(id) {
        return await apiRequest(`/api/foods/${id}`);
    },

    async createFood(data) {
        return await apiRequest('/api/foods', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    async updateFood(id, data) {
        return await apiRequest(`/api/foods/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    async deleteFood(id) {
        return await apiRequest(`/api/foods/${id}`, {
            method: 'DELETE',
        });
    },
};

/**
 * Category API
 */
const categoryAPI = {
    async getCategories() {
        return await apiRequest('/api/categories');
    },

    async getCategory(id) {
        return await apiRequest(`/api/categories/${id}`);
    },

    async createCategory(data) {
        return await apiRequest('/api/categories', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    async updateCategory(id, data) {
        return await apiRequest(`/api/categories/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    async deleteCategory(id) {
        return await apiRequest(`/api/categories/${id}`, {
            method: 'DELETE',
        });
    },
};

/**
 * Cart API
 */
const cartAPI = {
    async getCart() {
        return await apiRequest('/api/cart');
    },

    async addToCart(foodId, quantity = 1) {
        return await apiRequest('/api/cart/add', {
            method: 'POST',
            body: JSON.stringify({ food_id: foodId, quantity }),
        });
    },

    async updateCartItem(itemId, quantity) {
        return await apiRequest(`/api/cart/items/${itemId}`, {
            method: 'PUT',
            body: JSON.stringify({ quantity }),
        });
    },

    async removeCartItem(itemId) {
        return await apiRequest(`/api/cart/items/${itemId}`, {
            method: 'DELETE',
        });
    },

    async clearCart() {
        return await apiRequest('/api/cart', {
            method: 'DELETE',
        });
    },
};

/**
 * Order API
 */
const orderAPI = {
    async getOrders() {
        return await apiRequest('/api/orders');
    },

    async getOrder(id) {
        return await apiRequest(`/api/orders/${id}`);
    },

    async createOrder(data) {
        return await apiRequest('/api/orders', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    async updateOrderStatus(id, status) {
        return await apiRequest(`/api/orders/${id}/status?status=${status}`, {
            method: 'PUT',
        });
    },
};

/**
 * Review API
 */
const reviewAPI = {
    async getReviews(params = {}) {
        // Filter out null and undefined values
        const filteredParams = Object.fromEntries(
            Object.entries(params).filter(([_, value]) => value !== null && value !== undefined && value !== '')
        );
        const queryString = new URLSearchParams(filteredParams).toString();
        return await apiRequest(`/api/reviews?${queryString}`);
    },

    async createReview(data) {
        return await apiRequest('/api/reviews', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },
};

/**
 * Coupon API
 */
const couponAPI = {
    async getCoupons() {
        return await apiRequest('/api/coupons');
    },

    async validateCoupon(code, orderAmount) {
        return await apiRequest(`/api/coupons/validate?code=${code}&order_amount=${orderAmount}`, {
            method: 'POST',
        });
    },

    async createCoupon(data) {
        return await apiRequest('/api/coupons', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    async deleteCoupon(id) {
        return await apiRequest(`/api/coupons/${id}`, {
            method: 'DELETE',
        });
    },
};

/**
 * Address API
 */
const addressAPI = {
    async getAddresses() {
        return await apiRequest('/api/addresses');
    },

    async createAddress(data) {
        return await apiRequest('/api/addresses', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    async updateAddress(id, data) {
        return await apiRequest(`/api/addresses/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    async deleteAddress(id) {
        return await apiRequest(`/api/addresses/${id}`, {
            method: 'DELETE',
        });
    },
};

/**
 * User API
 */
const userAPI = {
    async getCurrentUser() {
        return await apiRequest('/api/users/me');
    },

    async updateUser(data) {
        return await apiRequest('/api/users/me', {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    async getAllUsers() {
        return await apiRequest('/api/users');
    },
};

/**
 * Utility Functions
 */

/**
 * Show toast notification
 */
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

/**
 * Check if user is authenticated
 */
function isAuthenticated() {
    return !!getToken();
}

/**
 * Redirect to login if not authenticated
 */
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

/**
 * Redirect to home if authenticated
 */
function requireGuest() {
    if (isAuthenticated()) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

/**
 * Format price
 */
function formatPrice(price) {
    return `₹${price.toFixed(2)}`;
}

/**
 * Format date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

/**
 * Get cart count from localStorage
 */
function getCartCount() {
    return parseInt(localStorage.getItem('cartCount') || '0');
}

/**
 * Set cart count in localStorage
 */
function setCartCount(count) {
    localStorage.setItem('cartCount', count.toString());
    updateCartBadge();
}

/**
 * Update cart badge in navbar
 */
function updateCartBadge() {
    const badge = document.querySelector('.cart-badge');
    if (badge) {
        const count = getCartCount();
        badge.textContent = count;
        badge.style.display = count > 0 ? 'block' : 'none';
    }
}

/**
 * Initialize navbar
 */
function initializeNavbar() {
    const user = getCurrentUser();
    const navbarNav = document.querySelector('.navbar-nav');
    
    if (navbarNav) {
        if (user) {
            // Show authenticated links
            navbarNav.innerHTML = `
                <li><a href="index.html">Home</a></li>
                <li><a href="restaurants.html">Restaurants</a></li>
                <li><a href="orders.html">Orders</a></li>
                <li><a href="profile.html">Profile</a></li>
                <li><a href="#" onclick="logout(); return false;">Logout</a></li>
            `;
        } else {
            // Show guest links
            navbarNav.innerHTML = `
                <li><a href="index.html">Home</a></li>
                <li><a href="restaurants.html">Restaurants</a></li>
                <li><a href="login.html">Login</a></li>
                <li><a href="register.html">Register</a></li>
            `;
        }
    }
    
    updateCartBadge();
}

/**
 * Logout function
 */
function logout() {
    authAPI.logout();
    window.location.href = 'login.html';
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        authAPI,
        restaurantAPI,
        foodAPI,
        categoryAPI,
        cartAPI,
        orderAPI,
        reviewAPI,
        couponAPI,
        addressAPI,
        userAPI,
        getToken,
        setToken,
        getCurrentUser,
        setCurrentUser,
        isAuthenticated,
        requireAuth,
        requireGuest,
        showToast,
        formatPrice,
        formatDate,
        getCartCount,
        setCartCount,
        updateCartBadge,
        initializeNavbar,
        logout,
    };
}
