// frontend/pages/LoginPage.js
import { Store } from '../utils/store.js';

export function LoginPage() {
    return `
        <div class="container py-5">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card shadow">
                        <div class="card-body p-5">
                            <div class="text-center mb-4">
                                <i class="fas fa-sign-in-alt text-primary" style="font-size: 3rem;"></i>
                                <h3 class="mt-3">Login करें</h3>
                                <p class="text-muted">अपने account में sign in करें</p>
                            </div>
                            
                            <div id="loginAlert"></div>
                            
                            <form id="loginForm">
                                <div class="mb-3">
                                    <label for="username" class="form-label">Email Address</label>
                                    <input type="email" class="form-control" id="username" required>
                                </div>
                                
                                <div class="mb-3">
                                    <label for="password" class="form-label">Password</label>
                                    <input type="password" class="form-control" id="password" required>
                                </div>
                                
                                <div class="d-grid">
                                    <button type="submit" class="btn btn-primary btn-lg" id="loginBtn">
                                        <i class="fas fa-sign-in-alt me-2"></i>Login
                                    </button>
                                </div>
                            </form>
                            
                            <hr class="my-4">
                            
                            <div class="text-center">
                                <p class="mb-0">Account नहीं है? 
                                    <a href="/register" data-link class="text-primary">Register करें</a>
                                </p>
                            </div>
                            
                            <div class="mt-4">
                                <small class="text-muted">
                                    <strong>Test Accounts:</strong><br>
                                    Admin: admin@quizmaster.com / admin123<br>
                                    Student: student@quizmaster.com / student123
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Initialize login form when page loads
const response = await fetch('/api/login', {  // /api/login instead of /login
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
});

// frontend/pages/RegisterPage.js में भी same change करें
const response = await fetch('/api/register', {  // /api/register instead of /register
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(formData),
});
