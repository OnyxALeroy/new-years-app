<template>
    <div class="register-container">
        <div class="register-card">
            <h1 class="register-title">Create Account</h1>
            <p class="register-subtitle">
                Join us to organize your New Year's resolutions
            </p>

            <form @submit.prevent="handleRegister" class="register-form">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input
                        id="username"
                        v-model="form.username"
                        type="text"
                        required
                        class="form-input"
                        placeholder="Choose a username"
                    />
                </div>

                <div class="form-group">
                    <label for="email">Email</label>
                    <input
                        id="email"
                        v-model="form.email"
                        type="email"
                        required
                        class="form-input"
                        placeholder="Enter your email"
                    />
                </div>

                <div class="form-group">
                    <label for="password">Password</label>
                    <input
                        id="password"
                        v-model="form.password"
                        type="password"
                        required
                        class="form-input"
                        placeholder="Create a password"
                    />
                </div>

                <div v-if="error" class="error-message">
                    {{ error }}
                </div>

                <button type="submit" :disabled="loading" class="register-btn">
                    <span v-if="loading">Creating account...</span>
                    <span v-else>Create Account</span>
                </button>
            </form>

            <div class="register-footer">
                <p>
                    Already have an account?
                    <router-link to="/login" class="link"
                        >Sign in here</router-link
                    >
                </p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const form = reactive({
    username: "",
    email: "",
    password: "",
});

const loading = ref(false);
const error = ref("");

const handleRegister = async () => {
    loading.value = true;
    error.value = "";

    try {
        await authStore.register(form.username, form.email, form.password);
        await authStore.login(form.username, form.password);
        router.push("/resolutions");
    } catch (err: any) {
        error.value =
            err.response?.data?.detail ||
            "Registration failed. Please try again.";
    } finally {
        loading.value = false;
    }
};
</script>

<style scoped>
.register-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

.register-card {
    background: white;
    padding: 3rem;
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
}

.register-title {
    color: #333;
    font-size: 2rem;
    margin-bottom: 0.5rem;
    text-align: center;
}

.register-subtitle {
    color: #666;
    text-align: center;
    margin-bottom: 2rem;
}

.register-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.form-group label {
    color: #333;
    font-weight: 500;
}

.form-input {
    padding: 0.75rem 1rem;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}

.form-input:focus {
    outline: none;
    border-color: #667eea;
}

.error-message {
    color: #e74c3c;
    background-color: #fdf2f2;
    padding: 0.75rem;
    border-radius: 8px;
    text-align: center;
    border: 1px solid #f5c6cb;
}

.register-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 1rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: transform 0.3s ease;
}

.register-btn:hover:not(:disabled) {
    transform: translateY(-2px);
}

.register-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.register-footer {
    text-align: center;
    margin-top: 2rem;
    color: #666;
}

.link {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
}

.link:hover {
    text-decoration: underline;
}
</style>
