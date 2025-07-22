// frontend/components/Navbar.js
import { Store } from '../utils/store.js';

export function Navbar() {
    const store = Store.getInstance();
    const user = store.getUser();
    const isLoggedIn = store.isAuthenticated();

    return `
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="/" data-link>
                    <i class="fas fa-graduation-cap me-2"></i>
                    Quiz Master V2
                </a>
                
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="/" data-link>
                                <i class="fas fa-home me-1"></i>Home
                            </a>
                        </li>
                        ${isLoggedIn ? `
                            <li class="nav-item">
                                <a class="nav-link" href="/dashboard" data-link>
                                    <i class="fas fa-tachometer-alt me-1"></i>Dashboard
                                </a>
                            </li>
                            ${user && user.is_admin ? `
                                <li class="nav-item">
                                    <a class="nav-link" href="/admin" data-link>
                                        <i class="fas fa-cog me-1"></i>Admin
                                    </a>
                                </li>
                            ` : ''}
                        ` : ''}
                    </ul>
                    
                    <ul class="navbar-nav">
                        ${!isLoggedIn ? `
                            <li class="nav-item">
                                <a class="nav-link" href="/login" data-link>
                                    <i class="fas fa-sign-in-alt me-1"></i>Login
                                </a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="/register" data-link>
                                    <i class="fas fa-user-plus me-1"></i>Register
                                </a>
                            </li>
                        ` : `
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                                    <i class="fas fa-user me-1"></i>${user ? user.full_name : 'User'}
                                </a>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="/profile" data-link>Profile</a></li>
                                    <li><hr class="dropdown-divider"></li>
                                    <li><a class="dropdown-item" href="#" onclick="logout()">Logout</a></li>
                                </ul>
                            </li>
                        `}
                    </ul>
                </div>
            </div>
        </nav>
    `;
}

// Global logout function
window.logout = function() {
    const store = Store.getInstance();
    store.logout();
    window.location.href = '/';
};
