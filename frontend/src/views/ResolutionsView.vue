<template>
    <div class="resolutions-container">
        <div class="resolutions-header">
            <h1>My Resolutions</h1>
            <button @click="showCreateForm = true" class="create-btn">
                + Add Resolution
            </button>
        </div>

        <div v-if="loading" class="loading">Loading resolutions...</div>

        <div v-else-if="error" class="error">{{ error }}</div>

        <div v-else-if="resolutions.length === 0" class="empty-state">
            <h3>No resolutions yet</h3>
            <p>Start by adding your first New Year's resolution!</p>
        </div>

        <div v-else class="resolutions-grid">
            <div
                v-for="resolution in resolutions"
                :key="resolution.id"
                class="resolution-card"
                :class="{ completed: resolution.completed }"
            >
                <div class="resolution-content">
                    <h3>{{ resolution.title }}</h3>
                    <p v-if="resolution.description">
                        {{ resolution.description }}
                    </p>
                    <div class="resolution-meta">
                        <span class="date"
                            >Created:
                            {{ formatDate(resolution.created_at) }}</span
                        >
                        <span
                            class="status"
                            :class="{ completed: resolution.completed }"
                        >
                            {{
                                resolution.completed
                                    ? "Completed"
                                    : "In Progress"
                            }}
                        </span>
                    </div>
                </div>
                <div class="resolution-actions">
                    <button
                        @click="toggleComplete(resolution.id)"
                        :class="[
                            'toggle-btn',
                            { completed: resolution.completed },
                        ]"
                    >
                        {{ resolution.completed ? "↩️ Undo" : "✅ Complete" }}
                    </button>
                    <button
                        @click="deleteResolution(resolution.id)"
                        class="delete-btn"
                    >
                        🗑️ Delete
                    </button>
                </div>
            </div>
        </div>

        <!-- Create Resolution Modal -->
        <div v-if="showCreateForm" class="modal-overlay" @click="closeModal">
            <div class="modal" @click.stop>
                <h2>Create New Resolution</h2>
                <form @submit.prevent="createResolution">
                    <div class="form-group">
                        <label for="title">Title</label>
                        <input
                            id="title"
                            v-model="newResolution.title"
                            type="text"
                            required
                            placeholder="Enter resolution title"
                        />
                    </div>
                    <div class="form-group">
                        <label for="description">Description</label>
                        <textarea
                            id="description"
                            v-model="newResolution.description"
                            rows="3"
                            placeholder="Enter description (optional)"
                        ></textarea>
                    </div>
                    <div class="modal-actions">
                        <button
                            type="button"
                            @click="closeModal"
                            class="cancel-btn"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            :disabled="!newResolution.title.trim()"
                            class="submit-btn"
                        >
                            Create Resolution
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from "vue";
import { useResolutionStore } from "@/stores/resolutions";

const resolutionStore = useResolutionStore();

const resolutions = computed(() => resolutionStore.resolutions);
const loading = computed(() => resolutionStore.loading);
const error = computed(() => resolutionStore.error);

const showCreateForm = ref(false);
const newResolution = reactive({
    title: "",
    description: "",
});

onMounted(() => {
    resolutionStore.fetchResolutions();
});

const createResolution = async () => {
    try {
        await resolutionStore.createResolution({
            title: newResolution.title,
            description: newResolution.description || undefined,
        });
        closeModal();
    } catch (error) {
        console.error("Failed to create resolution:", error);
    }
};

const toggleComplete = (id: string) => {
    resolutionStore.toggleComplete(id);
};

const deleteResolution = async (id: string) => {
    if (confirm("Are you sure you want to delete this resolution?")) {
        try {
            await resolutionStore.deleteResolution(id);
        } catch (error) {
            console.error("Failed to delete resolution:", error);
        }
    }
};

const closeModal = () => {
    showCreateForm.value = false;
    newResolution.title = "";
    newResolution.description = "";
};

const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
};
</script>

<style scoped>
.resolutions-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.resolutions-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    flex-wrap: wrap;
    gap: 1rem;
}

.resolutions-header h1 {
    color: #333;
    margin: 0;
}

.create-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
    transition: transform 0.3s ease;
}

.create-btn:hover {
    transform: translateY(-2px);
}

.loading,
.error,
.empty-state {
    text-align: center;
    padding: 3rem;
    color: #666;
}

.error {
    color: #e74c3c;
    background-color: #fdf2f2;
    border-radius: 8px;
    border: 1px solid #f5c6cb;
}

.resolutions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 2rem;
}

.resolution-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    border-left: 4px solid #667eea;
}

.resolution-card.completed {
    border-left-color: #27ae60;
    opacity: 0.8;
}

.resolution-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.resolution-content h3 {
    color: #333;
    margin: 0 0 0.5rem 0;
    font-size: 1.25rem;
}

.resolution-content p {
    color: #666;
    margin: 0.5rem 0;
    line-height: 1.5;
}

.resolution-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    font-size: 0.875rem;
    color: #888;
}

.status.completed {
    color: #27ae60;
    font-weight: 500;
}

.resolution-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
}

.toggle-btn {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid #ddd;
    background: white;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.toggle-btn:hover {
    background: #f8f9fa;
}

.toggle-btn.completed {
    background: #27ae60;
    color: white;
    border-color: #27ae60;
}

.delete-btn {
    padding: 0.5rem 1rem;
    border: 1px solid #e74c3c;
    background: white;
    color: #e74c3c;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.delete-btn:hover {
    background: #e74c3c;
    color: white;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    max-width: 500px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
}

.modal h2 {
    margin-top: 0;
    color: #333;
}

.form-group {
    margin-bottom: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: #333;
    font-weight: 500;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #667eea;
}

.modal-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    margin-top: 2rem;
}

.cancel-btn {
    padding: 0.75rem 1.5rem;
    border: 1px solid #ddd;
    background: white;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.cancel-btn:hover {
    background: #f8f9fa;
}

.submit-btn {
    padding: 0.75rem 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: transform 0.3s ease;
}

.submit-btn:hover:not(:disabled) {
    transform: translateY(-2px);
}

.submit-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

@media (max-width: 768px) {
    .resolutions-container {
        padding: 1rem;
    }

    .resolutions-header {
        flex-direction: column;
        text-align: center;
    }

    .resolutions-grid {
        grid-template-columns: 1fr;
    }

    .modal {
        padding: 1.5rem;
    }
}
</style>
