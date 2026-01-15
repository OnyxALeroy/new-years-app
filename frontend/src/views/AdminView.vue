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
                @click="activeTab = 'events'"
                :class="{ active: activeTab === 'events' }"
                class="tab-btn"
            >
                All Events
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
                                <span :class="['role-badge', user.role]">{{
                                    user.role
                                }}</span>
                            </td>
                            <td>
                                <span
                                    :class="[
                                        'status-badge',
                                        user.is_active ? 'active' : 'inactive',
                                    ]"
                                >
                                    {{ user.is_active ? "Active" : "Inactive" }}
                                </span>
                            </td>
                            <td>{{ formatDate(user.created_at) }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Events Tab -->
        <div v-if="activeTab === 'events'" class="tab-content">
            <h2>All Events</h2>
            <div v-if="eventsLoading" class="loading">Loading events...</div>
            <div v-else-if="eventsError" class="error">{{ eventsError }}</div>
            <div v-else class="events-grid">
                <div
                    v-for="event in allEvents"
                    :key="event.id"
                    class="event-card"
                >
                    <div class="event-header">
                        <h3>{{ event.description }}</h3>
                        <div class="event-meta-inline">
                            <span class="participant-count"
                                >{{
                                    event.participants.length
                                }}
                                participants</span
                            >
                            <span class="location-count"
                                >{{ event.locations.length }} locations</span
                            >
                        </div>
                    </div>

                    <div class="event-summary">
                        <div class="summary-section">
                            <h4>📍 Locations</h4>
                            <div class="tags">
                                <span
                                    v-for="location in event.locations.slice(
                                        0,
                                        3,
                                    )"
                                    :key="location"
                                    class="tag"
                                >
                                    {{ location }}
                                </span>
                                <span
                                    v-if="event.locations.length > 3"
                                    class="tag more"
                                >
                                    +{{ event.locations.length - 3 }} more
                                </span>
                            </div>
                        </div>

                        <div class="summary-section">
                            <h4>👥 Organizers</h4>
                            <div class="tags">
                                <span
                                    v-for="organizer in event.organizers.slice(
                                        0,
                                        3,
                                    )"
                                    :key="organizer"
                                    class="tag"
                                >
                                    {{ organizer }}
                                </span>
                                <span
                                    v-if="event.organizers.length > 3"
                                    class="tag more"
                                >
                                    +{{ event.organizers.length - 3 }} more
                                </span>
                            </div>
                        </div>

                        <div
                            v-if="event.participants.length > 0"
                            class="summary-section"
                        >
                            <h4>💰 Payments</h4>
                            <div class="payment-summary">
                                <span
                                    >Total Due: ${{
                                        totalDue(event).toFixed(2)
                                    }}</span
                                >
                                <span
                                    >Total Paid: ${{
                                        totalPaid(event).toFixed(2)
                                    }}</span
                                >
                            </div>
                        </div>
                    </div>

                    <div class="event-summary">
                        <div class="summary-section">
                            <h4>📅 Event Dates</h4>
                            <div class="dates-list">
                                <div
                                    v-for="date in event.dates.slice(0, 2)"
                                    :key="date"
                                    class="date-item small"
                                >
                                    {{ formatDateTime(date) }}
                                </div>
                                <div
                                    v-if="event.dates.length > 2"
                                    class="date-item small more"
                                >
                                    +{{ event.dates.length - 2 }} more dates
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="event-meta-footer">
                        <span class="date"
                            >Created: {{ formatDate(event.created_at) }}</span
                        >
                        <span v-if="event.updated_at" class="updated">
                            Updated: {{ formatDate(event.updated_at) }}
                        </span>
                    </div>

                    <div class="event-actions">
                        <button @click="startEditEvent(event)" class="edit-btn">
                            Edit
                        </button>
                        <button
                            @click="deleteEventAction(event.id)"
                            class="delete-btn"
                        >
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Edit Event Modal -->
        <div v-if="showEditForm" class="modal-overlay" @click="closeEditModal">
            <div class="modal" @click.stop>
                <h2>Edit Event</h2>
                <form @submit.prevent="updateEvent">
                    <div class="form-group">
                        <label for="edit-description">Description</label>
                        <textarea
                            id="edit-description"
                            v-model="editingEventData.description"
                            rows="3"
                            required
                            placeholder="Describe the event..."
                        ></textarea>
                    </div>

                    <div class="form-group">
                        <label for="edit-organizers"
                            >Organizers (one per line)</label
                        >
                        <textarea
                            id="edit-organizers"
                            v-model="editOrganizersText"
                            rows="3"
                            required
                            placeholder="Enter organizer names (one per line)"
                        ></textarea>
                    </div>

                    <div class="form-group">
                        <label for="edit-locations"
                            >Locations (one per line)</label
                        >
                        <textarea
                            id="edit-locations"
                            v-model="editLocationsText"
                            rows="3"
                            required
                            placeholder="Enter locations (one per line)"
                        ></textarea>
                    </div>

                    <div class="form-group">
                        <label for="edit-dates">Event Dates</label>
                        <div class="dates-input">
                            <div
                                v-for="(date, index) in editEventDates"
                                :key="`edit-${index}`"
                                class="date-input-group"
                            >
                                <input
                                    type="datetime-local"
                                    v-model="editEventDates[index]"
                                    :min="minDateTime"
                                    required
                                />
                                <button
                                    v-if="editEventDates.length > 1"
                                    type="button"
                                    @click="removeEditDate(index)"
                                    class="remove-date-btn"
                                >
                                    ×
                                </button>
                            </div>
                            <button
                                type="button"
                                @click="addEditDate"
                                class="add-date-btn"
                            >
                                + Add Date
                            </button>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="edit-notes"
                            >Notes (one per line, optional)</label
                        >
                        <textarea
                            id="edit-notes"
                            v-model="editNotesText"
                            rows="3"
                            placeholder="Enter any additional notes..."
                        ></textarea>
                    </div>

                    <div class="modal-actions">
                        <button
                            type="button"
                            @click="closeEditModal"
                            class="cancel-btn"
                        >
                            Cancel
                        </button>
                        <button type="submit" class="submit-btn">
                            Update Event
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, reactive, watch } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useEventStore } from "@/stores/events";
import { authAPI, eventsAPI } from "@/utils/api";
import type { Event, EventUpdate } from "@/types";

const authStore = useAuthStore();
const eventStore = useEventStore();

const activeTab = ref("users");
const users = ref([]);
const usersLoading = ref(false);
const usersError = ref("");

const allEvents = computed(() => eventStore.events);
const eventsLoading = computed(() => eventStore.loading);
const eventsError = computed(() => eventStore.error);

onMounted(async () => {
    await Promise.all([fetchUsers(), fetchAllEvents()]);
});

const fetchUsers = async () => {
    usersLoading.value = true;
    usersError.value = "";
    try {
        users.value = await authAPI.getUsers();
    } catch (err: any) {
        usersError.value =
            err.response?.data?.detail || "Failed to fetch users";
    } finally {
        usersLoading.value = false;
    }
};

const fetchAllEvents = async () => {
    try {
        await eventStore.fetchEvents();
    } catch (err) {
        console.error("Failed to fetch events:", err);
    }
};

const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
};

const formatDateTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
};

const totalDue = (event: any): number => {
    return event.participants.reduce(
        (sum: number, p: any) => sum + p.due_payment,
        0,
    );
};

const totalPaid = (event: any): number => {
    return event.participants.reduce(
        (sum: number, p: any) => sum + p.paid_amount,
        0,
    );
};

// Edit functionality
const showEditForm = ref(false);
const editingEvent = ref<Event | null>(null);
const editingEventData = reactive({
    description: "",
    organizers: [] as string[],
    locations: [] as string[],
    dates: [] as string[],
    notes: [] as string[],
});

const editOrganizersText = ref("");
const editLocationsText = ref("");
const editNotesText = ref("");
const editEventDates = ref([""]);

const minDateTime = computed(() => {
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    return now.toISOString().slice(0, 16);
});

const startEditEvent = (event: Event) => {
    editingEvent.value = event;
    editingEventData.description = event.description;
    editingEventData.organizers = [...event.organizers];
    editingEventData.locations = [...event.locations];
    editingEventData.dates = [...event.dates];
    editingEventData.notes = [...event.notes];

    editOrganizersText.value = event.organizers.join("\n");
    editLocationsText.value = event.locations.join("\n");
    editNotesText.value = event.notes.join("\n");
    editEventDates.value = [...event.dates];

    showEditForm.value = true;
};

const updateEvent = async () => {
    if (!editingEvent.value) return;

    try {
        await eventsAPI.updateEvent(editingEvent.value.id, {
            description: editingEventData.description,
            organizers: editingEventData.organizers,
            locations: editingEventData.locations,
            dates: editEventDates.value.filter((date) => date.trim() !== ""),
            notes:
                editingEventData.notes.length > 0
                    ? editingEventData.notes
                    : undefined,
        });
        closeEditModal();
        await fetchAllEvents();
    } catch (error) {
        console.error("Failed to update event:", error);
    }
};

const closeEditModal = () => {
    showEditForm.value = false;
    editingEvent.value = null;
    editingEventData.description = "";
    editingEventData.organizers = [];
    editingEventData.locations = [];
    editingEventData.notes = [];
    editOrganizersText.value = "";
    editLocationsText.value = "";
    editNotesText.value = "";
    editEventDates.value = [""];
};

const deleteEventAction = async (eventId: string) => {
    if (confirm("Are you sure you want to delete this event?")) {
        try {
            await eventsAPI.deleteEvent(eventId);
            await fetchAllEvents();
        } catch (error) {
            console.error("Failed to delete event:", error);
        }
    }
};

const addEditDate = () => {
    editEventDates.value.push("");
};

const removeEditDate = (index: number) => {
    editEventDates.value.splice(index, 1);
};

// Watch edit form text areas and update arrays
watch(editOrganizersText, (newText) => {
    editingEventData.organizers = newText
        .split("\n")
        .map((line) => line.trim())
        .filter((line) => line.length > 0);
});

watch(editLocationsText, (newText) => {
    editingEventData.locations = newText
        .split("\n")
        .map((line) => line.trim())
        .filter((line) => line.length > 0);
});

watch(editNotesText, (newText) => {
    editingEventData.notes = newText
        .split("\n")
        .map((line) => line.trim())
        .filter((line) => line.length > 0);
});
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

.loading,
.error {
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

.events-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
    gap: 1.5rem;
}

.event-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    border-left: 4px solid #667eea;
}

.event-card:hover {
    transform: translateY(-2px);
}

.event-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
}

.event-header h3 {
    margin: 0;
    color: #333;
    font-size: 1.1rem;
    line-height: 1.4;
    flex: 1;
}

.event-meta-inline {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    font-size: 0.85rem;
    color: #666;
    text-align: right;
}

.participant-count {
    background: #e3f2fd;
    color: #1976d2;
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
}

.location-count {
    background: #f3e5f5;
    color: #7b1fa2;
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
}

.event-summary {
    margin: 1rem 0;
}

.summary-section {
    margin-bottom: 1rem;
}

.summary-section h4 {
    color: #555;
    margin: 0 0 0.5rem 0;
    font-size: 0.9rem;
}

.tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.tag {
    background: #f8f9fa;
    padding: 0.25rem 0.5rem;
    border-radius: 6px;
    font-size: 0.8rem;
    color: #666;
}

.tag.more {
    background: #e1e5e9;
    color: #555;
    font-style: italic;
}

.payment-summary {
    display: flex;
    gap: 1rem;
    font-size: 0.9rem;
    color: #666;
}

.event-meta-footer {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    margin-top: 1rem;
    font-size: 0.875rem;
    color: #888;
    border-top: 1px solid #f0f0f0;
    padding-top: 1rem;
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

    .events-grid {
        grid-template-columns: 1fr;
    }

    .event-header {
        flex-direction: column;
        gap: 0.5rem;
    }

    .event-meta-inline {
        text-align: left;
        flex-direction: row;
        gap: 0.5rem;
    }
}

.event-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #f0f0f0;
}

.edit-btn {
    padding: 0.5rem 1rem;
    border: 1px solid #f39c12;
    background: white;
    color: #f39c12;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.edit-btn:hover {
    background: #f39c12;
    color: white;
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

.dates-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.date-item.small {
    background: #f8f9fa;
    padding: 0.5rem;
    border-radius: 6px;
    border-left: 3px solid #667eea;
    font-size: 0.85rem;
    font-weight: 500;
}

.date-item.small.more {
    background: #e1e5e9;
    border-left-color: #95a5a6;
    font-style: italic;
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
    max-width: 600px;
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

.form-group textarea {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
    resize: vertical;
}

.form-group textarea:focus {
    outline: none;
    border-color: #667eea;
}

.dates-input {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.date-input-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.date-input-group input {
    flex: 1;
    padding: 0.75rem;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}

.date-input-group input:focus {
    outline: none;
    border-color: #667eea;
}

.remove-date-btn {
    background: #e74c3c;
    color: white;
    border: none;
    border-radius: 50%;
    width: 2rem;
    height: 2rem;
    cursor: pointer;
    font-size: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.3s ease;
}

.remove-date-btn:hover {
    background: #c0392b;
}

.add-date-btn {
    background: #27ae60;
    color: white;
    border: none;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background-color 0.3s ease;
    align-self: flex-start;
}

.add-date-btn:hover {
    background: #229954;
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

.submit-btn:hover {
    transform: translateY(-2px);
}
</style>
