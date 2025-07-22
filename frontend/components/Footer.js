// frontend/components/Footer.js
export function Footer() {
    return `
        <footer class="bg-dark text-light py-5 mt-5">
            <div class="container">
                <div class="row">
                    <div class="col-md-4">
                        <h5><i class="fas fa-graduation-cap me-2"></i>Quiz Master V2</h5>
                        <p class="text-muted">आधुनिक exam preparation platform जो आपकी पढ़ाई को बेहतर बनाता है।</p>
                    </div>
                    <div class="col-md-4">
                        <h6>Quick Links</h6>
                        <ul class="list-unstyled">
                            <li><a href="/" data-link class="text-muted text-decoration-none">Home</a></li>
                            <li><a href="/about" data-link class="text-muted text-decoration-none">About</a></li>
                            <li><a href="/contact" data-link class="text-muted text-decoration-none">Contact</a></li>
                        </ul>
                    </div>
                    <div class="col-md-4">
                        <h6>Contact Info</h6>
                        <p class="text-muted mb-1">
                            <i class="fas fa-envelope me-2"></i>
                            admin@quizmaster.com
                        </p>
                        <p class="text-muted">
                            <i class="fas fa-phone me-2"></i>
                            +91 12345 67890
                        </p>
                    </div>
                </div>
                <hr class="my-4">
                <div class="text-center text-muted">
                    <p>&copy; 2024 Quiz Master V2. All rights reserved.</p>
                </div>
            </div>
        </footer>
    `;
}
