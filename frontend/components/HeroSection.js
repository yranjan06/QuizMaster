// frontend/components/HeroSection.js
export function HeroSection() {
    return `
        <section class="hero-section">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-lg-6">
                        <h1 class="display-4 fw-bold mb-4">
                            Quiz Master V2 में आपका स्वागत है
                        </h1>
                        <p class="lead mb-4">
                            भारत का सबसे advanced exam preparation platform। 
                            हजारों questions, personalized analytics, और real-time progress tracking के साथ।
                        </p>
                        <div class="d-flex gap-3">
                            <a href="/register" data-link class="btn btn-light btn-lg">
                                <i class="fas fa-rocket me-2"></i>अभी शुरू करें
                            </a>
                            <a href="/login" data-link class="btn btn-outline-light btn-lg">
                                <i class="fas fa-sign-in-alt me-2"></i>Login करें
                            </a>
                        </div>
                    </div>
                    <div class="col-lg-6 text-center">
                        <i class="fas fa-graduation-cap" style="font-size: 15rem; opacity: 0.3;"></i>
                    </div>
                </div>
            </div>
        </section>
    `;
}
