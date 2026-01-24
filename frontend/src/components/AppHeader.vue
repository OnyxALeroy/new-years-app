<template>
    <header class="app-header">
        <nav class="navbar">
            <div class="nav-brand">
                <router-link to="/" class="brand-link">
                    🎆 New Year's Events
                </router-link>
            </div>

            <div class="nav-links">
                <router-link to="/" class="nav-link">Home</router-link>

                <template v-if="isAuthenticated">
                    <router-link to="/events" class="nav-link"
                        >Events</router-link
                    >
                    <router-link to="/profile" class="nav-link"
                        >My Profile</router-link
                    >
                    <router-link v-if="isOrganizer || isAdmin" to="/organizer" class="nav-link"
                        >Organizer</router-link
                    >
                    <router-link v-if="isAdmin" to="/admin" class="nav-link"
                        >Admin</router-link
                    >

                    <div class="user-menu">
                        <span class="user-info"
                            >{{ user?.username }} ({{ user?.role }})</span
                        >
                        <button @click="logout" class="logout-btn">
                            Logout
                        </button>
                    </div>
                </template>

                <template v-else>
                    <router-link to="/login" class="nav-link"
                        >Login</router-link
                    >
                    <router-link to="/register" class="nav-link"
                        >Register</router-link
                    >
                </template>
            </div>
        </nav>
    </header>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

const isAuthenticated = computed(() => authStore.isAuthenticated);
const isAdmin = computed(() => authStore.isAdmin);
const isOrganizer = computed(() => authStore.isOrganizer);
const user = computed(() => authStore.user);

const logout = () => {
    authStore.logout();
    router.push("/");
};
</script>

<style scoped>
.app-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem 0;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.navbar {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-brand .brand-link {
    color: white;
    font-size: 1.5rem;
    font-weight: bold;
    text-decoration: none;
    transition: color 0.3s ease;
}

.nav-brand .brand-link:hover {
    color: #ffd700;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 2rem;
}

.nav-link {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.nav-link:hover {
    background-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}

.nav-link.router-link-active {
    background-color: rgba(255, 255, 255, 0.2);
}

.user-menu {
    display: flex;
    align-items: center;
    gap: 1rem;
    color: white;
}

.user-info {
    font-size: 0.9rem;
    opacity: 0.9;
}

.logout-btn {
    background-color: rgba(255, 255, 255, 0.2);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 0.5rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.logout-btn:hover {
    background-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
}

@media (max-width: 768px) {
    .navbar {
        flex-direction: column;
        gap: 1rem;
    }

    .nav-links {
        flex-wrap: wrap;
        justify-content: center;
        gap: 1rem;
    }

    .user-menu {
        flex-direction: column;
        text-align: center;
    }
}
</style>
