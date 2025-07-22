// frontend/pages/HomePage.js
import { HeroSection } from '../components/HeroSection.js';

export function HomePage() {
    return `
        ${HeroSection()}
        
        <section class="py-5">
            <div class="container">
                <h2 class="text-center mb-5">मुख्य विशेषताएं</h2>
                <div class="row g-4">
                    <div class="col-md-4">
                        <div class="card feature-card h-100 text-center p-4">
                            <div class="mb-3">
                                <i class="fas fa-brain text-primary" style="font-size: 3rem;"></i>
                            </div>
                            <h5 class="card-title">Smart Questions</h5>
                            <p class="card-text text-muted">
                                विभिन्न subjects और chapters के लिए carefully curated MCQ questions।
                            </p>
                        </div>
                    </div>
                    
                    <div class="col-md-4">
                        <div class="card feature-card h-100 text-center p-4">
                            <div class="mb-3">
                                <i class="fas fa-chart-line text-success" style="font-size: 3rem;"></i>
                            </div>
                            <h5 class="card-title">Performance Analytics</h5>
                            <p class="card-text text-muted">
                                Detailed charts और reports के साथ अपनी progress को track करें।
                            </p>
                        </div>
                    </div>
                    
                    <div class="col-md-4">
                        <div class="card feature-card h-100 text-center p-4">
                            <div class="mb-3">
                                <i class="fas fa-stopwatch text-warning" style="font-size: 3rem;"></i>
                            </div>
                            <h5 class="card-title">Timed Quizzes</h5>
                            <p class="card-text text-muted">
                                Real exam जैसा experience पाने के लिए timer-based quizzes।
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="py-5 bg-light">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-lg-6">
                        <h3>Ready to Start Your Journey?</h3>
                        <p class="text-muted">
                            अभी register करें और हजारों questions का access पाएं। 
                            Personalized dashboard के साथ अपनी performance को improve करें।
                        </p>
                        <a href="/register" data-link class="btn btn-primary btn-lg">
                            <i class="fas fa-user-plus me-2"></i>Free Registration
                        </a>
                    </div>
                    <div class="col-lg-6 text-center">
                        <div class="row text-center">
                            <div class="col-4">
                                <h4 class="text-primary">1000+</h4>
                                <small class="text-muted">Questions</small>
                            </div>
                            <div class="col-4">
                                <h4 class="text-success">50+</h4>
                                <small class="text-muted">Subjects</small>
                            </div>
                            <div class="col-4">
                                <h4 class="text-warning">100+</h4>
                                <small class="text-muted">Users</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    `;
}
