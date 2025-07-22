// frontend/pages/RegisterPage.js
export function RegisterPage() {
    return `
        <div class="container py-5">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card shadow">
                        <div class="card-body p-5">
                            <div class="text-center mb-4">
                                <i class="fas fa-user-plus text-success" style="font-size: 3rem;"></i>
                                <h3 class="mt-3">Register करें</h3>
                                <p class="text-muted">नया account बनाएं और शुरू करें</p>
                            </div>
                            
                            <div id="registerAlert"></div>
                            
                            <form id="registerForm">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="fullName" class="form-label">पूरा नाम *</label>
                                            <input type="text" class="form-control" id="fullName" required>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="email" class="form-label">Email Address *</label>
                                            <input type="email" class="form-control" id="email" required>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="password" class="form-label">Password *</label>
                                            <input type="password" class="form-control" id="password" required minlength="6">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="confirmPassword" class="form-label">Confirm Password *</label>
                                            <input type="password" class="form-control" id="confirmPassword" required>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="qualification" class="form-label">शिक्षा</label>
                                            <select class="form-select" id="qualification">
                                                <option value="">Select...</option>
                                                <option value="10th">10th</option>
                                                <option value="12th">12th</option>
                                                <option value="Graduate">Graduate</option>
                                                <option value="Post Graduate">Post Graduate</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="dateOfBirth" class="form-label">जन्म तिथि</label>
                                            <input type="date" class="form-control" id="dateOfBirth">
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="mb-3 form-check">
                                    <input type="checkbox" class="form-check-input" id="termsCheck" required>
                                    <label class="form-check-label" for="termsCheck">
                                        मैं <a href="#" class="text-primary">Terms & Conditions</a> से सहमत हूं
                                    </label>
                                </div>
                                
                                <div class="d-grid">
                                    <button type="submit" class="btn btn-success btn-lg" id="registerBtn">
                                        <i class="fas fa-user-plus me-2"></i>Register करें
                                    </button>
                                </div>
                            </form>
                            
                            <hr class="my-4">
                            
                            <div class="text-center">
                                <p class="mb-0">पहले से account है? 
                                    <a href="/login" data-link class="text-primary">Login करें</a>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Initialize register form
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname === '/register') {
        initRegisterForm();
    }
});

function initRegisterForm() {
    const form = document.getElementById('registerForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            full_name: document.getElementById('fullName').value,
            username: document.getElementById('email').value,
            password: document.getElementById('password').value,
            qualification: document.getElementById('qualification').value,
            date_of_birth: document.getElementById('dateOfBirth').value,
        };
        
        const confirmPassword = document.getElementById('confirmPassword').value;
        const registerBtn = document.getElementById('registerBtn');
        const alertDiv = document.getElementById('registerAlert');
        
        // Validate passwords match
        if (formData.password !== confirmPassword) {
            alertDiv.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>Passwords do not match!
                </div>
            `;
            return;
        }
        
        // Show loading
        registerBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Creating account...';
        registerBtn.disabled = true;
        
        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });
            
            const data = await response.json();
            
            if (response.ok) {
                alertDiv.innerHTML = `
                    <div class="alert alert-success">
                        <i class="fas fa-check me-2"></i>Registration successful! Redirecting to login...
                    </div>
                `;
                
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
                
            } else {
                throw new Error(data.message || 'Registration failed');
            }
            
        } catch (error) {
            alertDiv.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>${error.message}
                </div>
            `;
        } finally {
            registerBtn.innerHTML = '<i class="fas fa-user-plus me-2"></i>Register करें';
            registerBtn.disabled = false;
        }
    });
}
