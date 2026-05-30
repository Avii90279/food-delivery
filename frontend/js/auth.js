/**
 * Authentication JavaScript
 * Handles login and register functionality
 */

// Check if user is already authenticated
if (isAuthenticated()) {
    window.location.href = 'index.html';
}

// Login Form Handler
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const submitBtn = loginForm.querySelector('button[type="submit"]');
        
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading-spinner"></span> Logging in...';
        
        try {
            await authAPI.login(email, password);
            showToast('Login successful!', 'success');
            window.location.href = 'index.html';
        } catch (error) {
            showToast(error.message || 'Login failed', 'error');
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Login';
        }
    });
}

// Register Form Handler
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const username = document.getElementById('username').value;
        const full_name = document.getElementById('full_name').value;
        const phone = document.getElementById('phone').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;
        
        // Validation
        if (password !== confirmPassword) {
            showToast('Passwords do not match', 'error');
            return;
        }
        
        if (password.length < 6) {
            showToast('Password must be at least 6 characters', 'error');
            return;
        }
        
        const submitBtn = registerForm.querySelector('button[type="submit"]');
        
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading-spinner"></span> Creating account...';
        
        try {
            await authAPI.register({
                email,
                username,
                full_name,
                phone,
                password
            });
            showToast('Registration successful!', 'success');
            window.location.href = 'index.html';
        } catch (error) {
            showToast(error.message || 'Registration failed', 'error');
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Create Account';
        }
    });
}

// Password visibility toggle
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = input.nextElementSibling;
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.textContent = '🙈';
    } else {
        input.type = 'password';
        icon.textContent = '👁️';
    }
}
