<template>
  <div class="home-container">
    <div class="hero-section">
      <h1 class="hero-title">🎆 New Year's Event Organizer</h1>
      <p class="hero-subtitle">Plan, track, and achieve your New Year's resolutions</p>
      
      <div class="cta-section">
        <template v-if="isAuthenticated">
          <router-link to="/resolutions" class="cta-btn primary">My Resolutions</router-link>
          <router-link v-if="isAdmin" to="/admin" class="cta-btn secondary">Admin Panel</router-link>
        </template>
        <template v-else>
          <router-link to="/register" class="cta-btn primary">Get Started</router-link>
          <router-link to="/login" class="cta-btn secondary">Sign In</router-link>
        </template>
      </div>
    </div>
    
    <div class="features-section">
      <h2 class="features-title">Features</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">📋</div>
          <h3>Resolution Tracking</h3>
          <p>Create and manage your personal New Year's resolutions</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">👥</div>
          <h3>User Roles</h3>
          <p>Secure authentication with role-based access control</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📊</div>
          <h3>Progress Monitoring</h3>
          <p>Track your progress and mark resolutions as complete</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const isAdmin = computed(() => authStore.isAdmin)
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero-section {
  text-align: center;
  padding: 6rem 2rem 4rem;
  color: white;
}

.hero-title {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  font-weight: bold;
  animation: fadeInUp 1s ease-out;
}

.hero-subtitle {
  font-size: 1.25rem;
  margin-bottom: 3rem;
  opacity: 0.9;
  animation: fadeInUp 1s ease-out 0.2s both;
}

.cta-section {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  animation: fadeInUp 1s ease-out 0.4s both;
}

.cta-btn {
  display: inline-block;
  padding: 1rem 2rem;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.cta-btn.primary {
  background-color: #ffd700;
  color: #333;
}

.cta-btn.primary:hover {
  background-color: #ffed4e;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.cta-btn.secondary {
  background-color: transparent;
  color: white;
  border-color: white;
}

.cta-btn.secondary:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.features-section {
  background-color: white;
  padding: 4rem 2rem;
}

.features-title {
  text-align: center;
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 3rem;
}

.features-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  text-align: center;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .cta-section {
    flex-direction: column;
    align-items: center;
  }
  
  .cta-btn {
    width: 200px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>