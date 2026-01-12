<template>
  <div class="admin-container">
    <h1>Admin Panel</h1>
    <div class="admin-tabs">
      <button
        @click="activeTab = 'users'"
        :class="{ active: activeTab === 'users' }"
        class="tab-btn"
      >
        Users
      </button>
      <button
        @click="activeTab = 'resolutions'"
        :class="{ active: activeTab === 'resolutions' }"
        class="tab-btn"
      >
        All Resolutions
      </button>
    </div>
    
    <!-- Users Tab -->
    <div v-if="activeTab === 'users'" class="tab-content">
      <h2>All Users</h2>
      <div v-if="usersLoading" class="loading">Loading users...</div>
      <div v-else-if="usersError" class="error">{{ usersError }}</div>
      <div v-else class="users-table">
        <table>
          <thead>
            <tr>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th>Active</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>
                <span :class="['role-badge', user.role]">{{ user.role }}</span>
              </td>
              <td>
                <span :class="['status-badge', user.is_active ? 'active' : 'inactive']">
                  {{ user.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td>{{ formatDate(user.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Resolutions Tab -->
    <div v-if="activeTab === 'resolutions'" class="tab-content">
      <h2>All Resolutions</h2>
      <div v-if="resolutionsLoading" class="loading">Loading resolutions...</div>
      <div v-else-if="resolutionsError" class="error">{{ resolutionsError }}</div>
      <div v-else class="resolutions-grid">
        <div
          v-for="resolution in allResolutions"
          :key="resolution.id"
          class="resolution-card"
          :class="{ completed: resolution.completed }"
        >
          <div class="resolution-header">
            <h3>{{ resolution.title }}</h3>
            <span :class="['status-badge', resolution.completed ? 'completed' : 'pending']">
              {{ resolution.completed ? 'Completed' : 'Pending' }}
            </span>
          </div>
          <p v-if="resolution.description">{{ resolution.description }}</p>
          <div class="resolution-meta">
            <span class="user-id">User ID: {{ resolution.user_id }}</span>
            <span class="date">{{ formatDate(resolution.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useResolutionStore } from '@/stores/resolutions'
import { authAPI } from '@/utils/api'

const authStore = useAuthStore()
const resolutionStore = useResolutionStore()

const activeTab = ref('users')
const users = ref([])
const usersLoading = ref(false)
const usersError = ref('')

const allResolutions = computed(() => resolutionStore.resolutions)
const resolutionsLoading = computed(() => resolutionStore.loading)
const resolutionsError = computed(() => resolutionStore.error)

onMounted(async () => {
  await Promise.all([
    fetchUsers(),
    fetchAllResolutions()
  ])
})

const fetchUsers = async () => {
  usersLoading.value = true
  usersError.value = ''
  try {
    users.value = await authAPI.getUsers()
  } catch (err: any) {
    usersError.value = err.response?.data?.detail || 'Failed to fetch users'
  } finally {
    usersLoading.value = false
  }
}

const fetchAllResolutions = async () => {
  try {
    await resolutionStore.fetchAllResolutions()
  } catch (err) {
    console.error('Failed to fetch resolutions:', err)
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}
</script>

<style scoped>
.admin-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.admin-container h1 {
  color: #333;
  margin-bottom: 2rem;
}

.admin-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid #e1e5e9;
}

.tab-btn {
  padding: 1rem 1.5rem;
  border: none;
  background: transparent;
  color: #666;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
  transition: all 0.3s ease;
}

.tab-btn.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.tab-btn:hover {
  color: #667eea;
}

.tab-content {
  animation: fadeIn 0.3s ease;
}

.tab-content h2 {
  color: #333;
  margin-bottom: 1.5rem;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #e74c3c;
  background-color: #fdf2f2;
  border-radius: 8px;
  border: 1px solid #f5c6cb;
}

.users-table {
  overflow-x: auto;
}

.users-table table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.users-table th,
.users-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e1e5e9;
}

.users-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #333;
}

.users-table tr:hover {
  background: #f8f9fa;
}

.role-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: capitalize;
}

.role-badge.user {
  background: #e3f2fd;
  color: #1976d2;
}

.role-badge.admin {
  background: #f3e5f5;
  color: #7b1fa2;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.active {
  background: #e8f5e8;
  color: #27ae60;
}

.status-badge.inactive {
  background: #ffeaea;
  color: #e74c3c;
}

.status-badge.completed {
  background: #e8f5e8;
  color: #27ae60;
}

.status-badge.pending {
  background: #fff3e0;
  color: #f57c00;
}

.resolutions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
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
}

.resolution-card:hover {
  transform: translateY(-2px);
}

.resolution-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.resolution-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.1rem;
  line-height: 1.4;
  flex: 1;
}

.resolution-card p {
  color: #666;
  margin: 0.75rem 0;
  line-height: 1.5;
}

.resolution-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  color: #888;
  margin-top: 1rem;
}

.user-id {
  background: #f0f0f0;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.75rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .admin-container {
    padding: 1rem;
  }
  
  .admin-tabs {
    overflow-x: auto;
  }
  
  .tab-btn {
    white-space: nowrap;
  }
  
  .users-table {
    font-size: 0.875rem;
  }
  
  .resolutions-grid {
    grid-template-columns: 1fr;
  }
  
  .resolution-header {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>