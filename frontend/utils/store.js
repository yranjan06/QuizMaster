// frontend/utils/store.js
export class Store {
    static instance = null;

    constructor() {
        if (Store.instance) {
            return Store.instance;
        }
        
        this.user = null;
        this.token = null;
        this.loadFromStorage();
        
        Store.instance = this;
    }

    static getInstance() {
        if (!Store.instance) {
            Store.instance = new Store();
        }
        return Store.instance;
    }

    setUser(userData) {
        this.user = userData;
        this.token = userData.token;
        this.saveToStorage();
        
        // Dispatch auth state change event
        document.dispatchEvent(new CustomEvent('authStateChanged', {
            detail: {
                isLoggedIn: true,
                user: userData
            }
        }));
    }

    getUser() {
        return this.user;
    }

    getToken() {
        return this.token;
    }

    isAuthenticated() {
        return !!this.token;
    }

    logout() {
        this.user = null;
        this.token = null;
        this.clearStorage();
        
        document.dispatchEvent(new CustomEvent('authStateChanged', {
            detail: {
                isLoggedIn: false,
                user: null
            }
        }));
    }

    saveToStorage() {
        if (this.user && this.token) {
            localStorage.setItem('quiz_user', JSON.stringify(this.user));
            localStorage.setItem('quiz_token', this.token);
        }
    }

    loadFromStorage() {
        const userData = localStorage.getItem('quiz_user');
        const token = localStorage.getItem('quiz_token');
        
        if (userData && token) {
            this.user = JSON.parse(userData);
            this.token = token;
        }
    }

    clearStorage() {
        localStorage.removeItem('quiz_user');
        localStorage.removeItem('quiz_token');
    }

    // API helper methods
    async apiCall(endpoint, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (this.token) {
            defaultOptions.headers['Authentication-Token'] = this.token;
        }

        const finalOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };

        try {
            const response = await fetch(endpoint, finalOptions);
            
            if (response.status === 401) {
                // Token expired or invalid
                this.logout();
                window.location.href = '/login';
                return;
            }
            
            return response;
        } catch (error) {
            console.error('API call failed:', error);
            throw error;
        }
    }
}
