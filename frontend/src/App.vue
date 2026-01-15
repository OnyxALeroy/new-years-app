<template>
    <div id="app">
        <AppHeader />
        <main class="main-content">
            <router-view />
        </main>
    </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import AppHeader from "@/components/AppHeader.vue";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();

onMounted(() => {
    authStore.initialize();
});
</script>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family:
        "Inter",
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Roboto,
        sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f8f9fa;
}

#app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.main-content {
    flex: 1;
}

/* Global styles */
h1,
h2,
h3,
h4,
h5,
h6 {
    margin-bottom: 0.5rem;
    font-weight: 600;
}

p {
    margin-bottom: 1rem;
}

a {
    color: #667eea;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

button {
    font-family: inherit;
}

/* Scrollbar styles */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
}
</style>
