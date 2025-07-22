// frontend/app.js
import { Router } from './utils/router.js';
import { Store } from './utils/store.js';
import { Navbar } from './components/Navbar.js';
import { Footer } from './components/Footer.js';
import { HomePage } from './pages/RegisterPage.js';
import { LoginPage } from './pages/LoginPage.js';
import { RegisterPage } from './pages/RegisterPage.js';

class App {
    constructor() {
        this.store = new Store();
        this.router = new Router();
        this.init();
    }

    init() {
        // Initialize components
        this.initComponents();
        this.initRoutes();
        this.initEventListeners();
        
        // Start router
        this.router.init();
    }

    initComponents() {
        // Render navbar and footer
        document.getElementById('navbar').innerHTML = Navbar();
        document.getElementById('footer').innerHTML = Footer();
    }

    initRoutes() {
        this.router.addRoute('/', HomePage);
        this.router.addRoute('/login', LoginPage);
        this.router.addRoute('/register', RegisterPage);
    }

    initEventListeners() {
        // Listen for navigation events
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-link]')) {
                e.preventDefault();
                this.router.navigateTo(e.target.href);
            }
        });

        // Listen for auth state changes
        document.addEventListener('authStateChanged', (e) => {
            this.handleAuthStateChange(e.detail);
        });
    }

    handleAuthStateChange(authState) {
        // Update navbar based on auth state
        document.getElementById('navbar').innerHTML = Navbar();
        
        if (authState.isLoggedIn) {
            if (authState.user.is_admin) {
                this.router.navigateTo('/admin');
            } else {
                this.router.navigateTo('/dashboard');
            }
        }
    }
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});
