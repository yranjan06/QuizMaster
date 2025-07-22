// frontend/utils/router.js
export class Router {
    constructor() {
        this.routes = {};
        this.currentRoute = null;
    }

    addRoute(path, handler) {
        this.routes[path] = handler;
    }

    navigateTo(url) {
        history.pushState(null, null, url);
        this.handleRoute();
    }

    handleRoute() {
        const path = window.location.pathname;
        const handler = this.routes[path] || this.routes['/'];
        
        if (handler) {
            document.getElementById('app').innerHTML = handler();
            this.currentRoute = path;
            
            // Trigger custom event for route change
            document.dispatchEvent(new CustomEvent('routeChanged', { 
                detail: { path, handler } 
            }));
        }
    }

    init() {
        window.addEventListener('popstate', () => this.handleRoute());
        this.handleRoute();
    }
}
