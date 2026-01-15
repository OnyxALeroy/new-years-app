<template>
  <div class="events-container">
    <div class="events-header">
      <h1>Events</h1>
      <div class="header-actions">
        <div class="filters">
          <input
            v-model="filterOrganizer"
            placeholder="Filter by organizer..."
            class="filter-input"
          />
          <input
            v-model="filterLocation"
            placeholder="Filter by location..."
            class="filter-input"
          />
        </div>
        <button
          v-if="authStore.isAdmin"
          @click="showCreateForm = true"
          class="create-btn"
        >
          + Create Event
        </button>
      </div>
    </div>
    
    <div v-if="loading" class="loading">Loading events...</div>
    
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else-if="filteredEvents.length === 0" class="empty-state">
      <h3>No events found</h3>
      <p v-if="filterOrganizer || filterLocation">
        Try adjusting your filters or 
        <button @click="clearFilters" class="clear-filters">clear them</button>
      </p>
      <p v-else>Start by creating the first event!</p>
    </div>
    
    <div v-else class="events-grid">
      <div
        v-for="event in filteredEvents"
        :key="event.id"
        class="event-card"
      >
        <div class="event-header">
          <h3>{{ event.description }}</h3>
          <div class="event-badges">
            <span v-if="event.organizers.includes(authStore.user?.username)" class="badge organizer">
              Organizer
            </span>
            <span v-if="isParticipant(event)" class="badge participant">
              Participant
            </span>
          </div>
        </div>
        
        <div class="event-content">
          <div class="event-section">
            <h4>📍 Locations</h4>
            <div class="tags">
              <span v-for="location in event.locations" :key="location" class="tag">
                {{ location }}
              </span>
            </div>
          </div>
          
          <div class="event-section">
            <h4>👥 Organizers</h4>
            <div class="tags">
              <span v-for="organizer in event.organizers" :key="organizer" class="tag">
                {{ organizer }}
              </span>
            </div>
          </div>
          
          <div v-if="event.participants.length > 0" class="event-section">
            <h4>🎫 Participants ({{ event.participants.length }})</h4>
            <div class="participants-summary">
              <span>Total Due: ${{ totalDue(event).toFixed(2) }}</span>
              <span>Total Paid: ${{ totalPaid(event).toFixed(2) }}</span>
            </div>
          </div>
          
          <div v-if="event.notes.length > 0" class="event-section">
            <h4>📝 Notes</h4>
            <ul class="notes-list">
              <li v-for="note in event.notes.slice(0, 2)" :key="note">{{ note }}</li>
              <li v-if="event.notes.length > 2">...and {{ event.notes.length - 2 }} more</li>
            </ul>
          </div>
        </div>
        
        <div class="event-meta">
          <span class="date">Created: {{ formatDate(event.created_at) }}</span>
          <span v-if="event.updated_at" class="updated">
            Updated: {{ formatDate(event.updated_at) }}
          </span>
        </div>
        
        <div class="event-actions">
          <button @click="viewDetails(event)" class="details-btn">
            View Details
          </button>
          <button
            v-if="authStore.isAdmin"
            @click="startEditEvent(event)"
            class="edit-btn"
          >
            Edit
          </button>
          <button
            v-if="authStore.isAdmin || event.organizers.includes(authStore.user?.username)"
            @click="deleteEvent(event.id)"
            class="delete-btn"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
    
    <!-- Create Event Modal -->
    <div v-if="showCreateForm" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <h2>Create New Event</h2>
        <form @submit.prevent="createEvent">
          <div class="form-group">
            <label for="description">Description</label>
            <textarea
              id="description"
              v-model="newEvent.description"
              rows="3"
              required
              placeholder="Describe the event..."
            ></textarea>
          </div>
          
          <div class="form-group">
            <label for="organizers">Organizers (one per line)</label>
            <textarea
              id="organizers"
              v-model="organizersText"
              rows="3"
              required
              placeholder="Enter organizer names (one per line)"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label for="locations">Locations (one per line)</label>
            <textarea
              id="locations"
              v-model="locationsText"
              rows="3"
              required
              placeholder="Enter locations (one per line)"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label for="dates">Event Dates</label>
            <div class="dates-input">
              <div v-for="(date, index) in eventDates" :key="index" class="date-input-group">
                <input
                  type="datetime-local"
                  v-model="eventDates[index]"
                  :min="minDateTime"
                  required
                />
                <button 
                  v-if="eventDates.length > 1"
                  type="button"
                  @click="removeDate(index)"
                  class="remove-date-btn"
                >
                  ×
                </button>
              </div>
              <button type="button" @click="addDate" class="add-date-btn">
                + Add Date
              </button>
            </div>
          </div>
          
          <div class="form-group">
            <label for="notes">Notes (one per line, optional)</label>
            <textarea
              id="notes"
              v-model="notesText"
              rows="3"
              placeholder="Enter any additional notes..."
            ></textarea>
          </div>
          
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="cancel-btn">Cancel</button>
            <button type="submit" :disabled="!isFormValid" class="submit-btn">
              Create Event
            </button>
          </div>
        </form>
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
            <label for="edit-organizers">Organizers (one per line)</label>
            <textarea
              id="edit-organizers"
              v-model="editOrganizersText"
              rows="3"
              required
              placeholder="Enter organizer names (one per line)"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label for="edit-locations">Locations (one per line)</label>
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
              <div v-for="(date, index) in editEventDates" :key="`edit-${index}`" class="date-input-group">
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
              <button type="button" @click="addEditDate" class="add-date-btn">
                + Add Date
              </button>
            </div>
          </div>
          
          <div class="form-group">
            <label for="edit-notes">Notes (one per line, optional)</label>
            <textarea
              id="edit-notes"
              v-model="editNotesText"
              rows="3"
              placeholder="Enter any additional notes..."
            ></textarea>
          </div>
          
          <div class="modal-actions">
            <button type="button" @click="closeEditModal" class="cancel-btn">Cancel</button>
            <button type="submit" class="submit-btn">
              Update Event
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Event Details Modal -->
    <div v-if="selectedEvent" class="modal-overlay" @click="closeDetails">
      <div class="modal details-modal" @click.stop>
        <div class="details-header">
          <h2>{{ selectedEvent.description }}</h2>
          <button @click="closeDetails" class="close-btn">×</button>
        </div>
        
        <div class="details-content">
          <div class="detail-section">
            <h3>📅 Event Dates</h3>
            <div class="dates-list">
              <div v-for="date in selectedEvent.dates" :key="date" class="date-item">
                {{ formatDateTime(date) }}
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h3>📍 Locations</h3>
            <div class="tags">
              <span v-for="location in selectedEvent.locations" :key="location" class="tag">
                {{ location }}
              </span>
            </div>
          </div>
          
          <div class="detail-section">
            <h3>👥 Organizers</h3>
            <div class="tags">
              <span v-for="organizer in selectedEvent.organizers" :key="organizer" class="tag">
                {{ organizer }}
              </span>
            </div>
          </div>
          
          <div class="detail-section">
            <h3>🎫 Participants ({{ selectedEvent.participants.length }})</h3>
            <div v-if="selectedEvent.participants.length === 0" class="empty-participants">
              No participants yet
            </div>
            <div v-else class="participants-list">
              <div
                v-for="participant in selectedEvent.participants"
                :key="participant.user_id"
                class="participant-item"
              >
                <div class="participant-info">
                  <strong>{{ participant.user_id }}</strong>
                  <div v-if="participant.tags.length > 0" class="participant-tags">
                    <span v-for="tag in participant.tags" :key="tag" class="tag small">
                      {{ tag }}
                    </span>
                  </div>
                </div>
                <div class="payment-info">
                  <span class="due">Due: ${{ participant.due_payment.toFixed(2) }}</span>
                  <span class="paid">Paid: ${{ participant.paid_amount.toFixed(2) }}</span>
                  <span 
                    :class="['balance', { 
                      'paid-full': participant.paid_amount >= participant.due_payment,
                      'partial': participant.paid_amount > 0 && participant.paid_amount < participant.due_payment,
                      'unpaid': participant.paid_amount === 0
                    }]"
                  >
                    Balance: ${{ (participant.due_payment - participant.paid_amount).toFixed(2) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="selectedEvent.notes.length > 0" class="detail-section">
            <h3>📝 Notes</h3>
            <ul class="notes-list">
              <li v-for="note in selectedEvent.notes" :key="note">{{ note }}</li>
            </ul>
          </div>
          
          <div v-if="selectedEvent.images.length > 0" class="detail-section">
            <h3>🖼️ Images</h3>
            <div class="images-grid">
              <div v-for="image in selectedEvent.images" :key="image" class="image-item">
                {{ image }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive, computed, watch } from 'vue'
import { useEventStore } from '@/stores/events'
import { useAuthStore } from '@/stores/auth'
import type { Event, EventCreate, Participant } from '@/types'

const eventStore = useEventStore()
const authStore = useAuthStore()

const events = computed(() => eventStore.events)
const loading = computed(() => eventStore.loading)
const error = computed(() => eventStore.error)

const filterOrganizer = ref('')
const filterLocation = ref('')
const showCreateForm = ref(false)
const showEditForm = ref(false)
const selectedEvent = ref<Event | null>(null)
const editingEvent = ref<Event | null>(null)
const editingEventData = reactive({
  description: '',
  organizers: [] as string[],
  locations: [] as string[],
  dates: [] as string[],
  notes: [] as string[]
})

const newEvent = reactive({
  description: '',
  organizers: [] as string[],
  locations: [] as string[],
  dates: [] as string[],
  notes: [] as string[]
})



const organizersText = ref('')
const locationsText = ref('')
const notesText = ref('')
const eventDates = ref([''])

const editOrganizersText = ref('')
const editLocationsText = ref('')
const editNotesText = ref('')
const editEventDates = ref([''])

const filteredEvents = computed(() => {
  let filtered = events.value
  
  if (filterOrganizer.value) {
    filtered = filtered.filter(event =>
      event.organizers.some(org => 
        org.toLowerCase().includes(filterOrganizer.value.toLowerCase())
      )
    )
  }
  
  if (filterLocation.value) {
    filtered = filtered.filter(event =>
      event.locations.some(loc => 
        loc.toLowerCase().includes(filterLocation.value.toLowerCase())
      )
    )
  }
  
  return filtered
})

const isFormValid = computed(() => {
  return newEvent.description.trim() && 
         newEvent.organizers.length > 0 && 
         newEvent.locations.length > 0 &&
         newEvent.dates.length > 0 &&
         eventDates.value.every(date => date.trim() !== '')
})

const minDateTime = computed(() => {
  const now = new Date()
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
  return now.toISOString().slice(0, 16)
})

onMounted(() => {
  eventStore.fetchEvents()
})

const createEvent = async () => {
  try {
    await eventStore.createEvent({
      description: newEvent.description,
      organizers: newEvent.organizers,
      locations: newEvent.locations,
      dates: eventDates.value.filter(date => date.trim() !== ''),
      notes: newEvent.notes.length > 0 ? newEvent.notes : undefined
    })
    closeModal()
  } catch (error) {
    console.error('Failed to create event:', error)
  }
}

const deleteEvent = async (id: string) => {
  if (confirm('Are you sure you want to delete this event?')) {
    try {
      await eventStore.deleteEvent(id)
    } catch (error) {
      console.error('Failed to delete event:', error)
    }
  }
}

const viewDetails = (event: Event) => {
  selectedEvent.value = event
}

const closeModal = () => {
  showCreateForm.value = false
  newEvent.description = ''
  newEvent.organizers = []
  newEvent.locations = []
  newEvent.notes = []
  organizersText.value = ''
  locationsText.value = ''
  notesText.value = ''
  eventDates.value = ['']
}

const addDate = () => {
  eventDates.value.push('')
}

const removeDate = (index: number) => {
  eventDates.value.splice(index, 1)
}

const startEditEvent = (event: Event) => {
  editingEvent.value = event
  editingEventData.description = event.description
  editingEventData.organizers = [...event.organizers]
  editingEventData.locations = [...event.locations]
  editingEventData.dates = [...event.dates]
  editingEventData.notes = [...event.notes]
  
  editOrganizersText.value = event.organizers.join('\n')
  editLocationsText.value = event.locations.join('\n')
  editNotesText.value = event.notes.join('\n')
  editEventDates.value = [...event.dates]
  
  showEditForm.value = true
}

const updateEvent = async () => {
  if (!editingEvent.value) return
  
  try {
    await eventStore.updateEvent(editingEvent.value.id, {
      description: editingEventData.description,
      organizers: editingEventData.organizers,
      locations: editingEventData.locations,
      dates: editEventDates.value.filter(date => date.trim() !== ''),
      notes: editingEventData.notes.length > 0 ? editingEventData.notes : undefined
    })
    closeEditModal()
  } catch (error) {
    console.error('Failed to update event:', error)
  }
}

const closeEditModal = () => {
  showEditForm.value = false
  editingEvent.value = null
  editingEventData.description = ''
  editingEventData.organizers = []
  editingEventData.locations = []
  editingEventData.notes = []
  editOrganizersText.value = ''
  editLocationsText.value = ''
  editNotesText.value = ''
  editEventDates.value = ['']
}

const addEditDate = () => {
  editEventDates.value.push('')
}

const removeEditDate = (index: number) => {
  editEventDates.value.splice(index, 1)
}

const closeDetails = () => {
  selectedEvent.value = null
}

const clearFilters = () => {
  filterOrganizer.value = ''
  filterLocation.value = ''
}

const isParticipant = (event: Event): boolean => {
  return event.participants.some(p => p.user_id === authStore.user?.username)
}

const totalDue = (event: Event): number => {
  return event.participants.reduce((sum, p) => sum + p.due_payment, 0)
}

const totalPaid = (event: Event): number => {
  return event.participants.reduce((sum, p) => sum + p.paid_amount, 0)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

// Watch text areas and update arrays
watch(organizersText, (newText) => {
  newEvent.organizers = newText
    .split('\n')
    .map(line => line.trim())
    .filter(line => line.length > 0)
})

watch(locationsText, (newText) => {
  newEvent.locations = newText
    .split('\n')
    .map(line => line.trim())
    .filter(line => line.length > 0)
})

watch(notesText, (newText) => {
  newEvent.notes = newText
    .split('\n')
    .map(line => line.trim())
    .filter(line => line.length > 0)
})

// Watch edit form text areas and update arrays
watch(editOrganizersText, (newText) => {
  editingEventData.organizers = newText
    .split('\n')
    .map(line => line.trim())
    .filter(line => line.length > 0)
})

watch(editLocationsText, (newText) => {
  editingEventData.locations = newText
    .split('\n')
    .map(line => line.trim())
    .filter(line => line.length > 0)
})

watch(editNotesText, (newText) => {
  editingEventData.notes = newText
    .split('\n')
    .map(line => line.trim())
    .filter(line => line.length > 0)
})
</script>

<style scoped>
.events-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.events-header {
  margin-bottom: 2rem;
}

.events-header h1 {
  color: #333;
  margin: 0 0 1rem 0;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.filters {
  display: flex;
  gap: 0.5rem;
  flex: 1;
}

.filter-input {
  flex: 1;
  min-width: 200px;
  padding: 0.5rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 0.9rem;
}

.filter-input:focus {
  outline: none;
  border-color: #667eea;
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
  white-space: nowrap;
}

.create-btn:hover {
  transform: translateY(-2px);
}

.loading, .error, .empty-state {
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

.clear-filters {
  background: none;
  border: none;
  color: #667eea;
  text-decoration: underline;
  cursor: pointer;
  font: inherit;
}

.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 2rem;
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
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.event-header h3 {
  color: #333;
  margin: 0;
  font-size: 1.25rem;
  flex: 1;
}

.event-badges {
  display: flex;
  gap: 0.5rem;
  margin-left: 1rem;
}

.badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge.organizer {
  background: #e8f5e8;
  color: #27ae60;
}

.badge.participant {
  background: #e3f2fd;
  color: #1976d2;
}

.event-section {
  margin-bottom: 1rem;
}

.event-section h4 {
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

.tag.small {
  font-size: 0.7rem;
}

.participants-summary {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #666;
}

.notes-list {
  margin: 0;
  padding-left: 1.5rem;
  color: #666;
}

.notes-list li {
  margin-bottom: 0.25rem;
}

.event-meta {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-top: 1rem;
  font-size: 0.875rem;
  color: #888;
}

.event-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.details-btn {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #667eea;
  background: white;
  color: #667eea;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.details-btn:hover {
  background: #667eea;
  color: white;
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

.details-modal {
  max-width: 800px;
}

.details-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.details-header h2 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 2rem;
  height: 2rem;
}

.close-btn:hover {
  color: #333;
}

.details-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.detail-section h3 {
  color: #333;
  margin: 0 0 0.75rem 0;
  font-size: 1.1rem;
}

.empty-participants {
  color: #888;
  font-style: italic;
}

.participants-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.participant-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.participant-info {
  flex: 1;
}

.participant-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin-top: 0.5rem;
}

.payment-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.9rem;
  text-align: right;
}

.due {
  color: #e74c3c;
}

.paid {
  color: #27ae60;
}

.balance {
  font-weight: 500;
}

.balance.paid-full {
  color: #27ae60;
}

.balance.partial {
  color: #f39c12;
}

.balance.unpaid {
  color: #e74c3c;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.image-item {
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 6px;
  text-align: center;
  font-size: 0.9rem;
  color: #666;
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

.dates-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.date-item {
  background: #f8f9fa;
  padding: 0.75rem;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  font-weight: 500;
}

@media (max-width: 768px) {
  .events-container {
    padding: 1rem;
  }
  
  .header-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filters {
    flex-direction: column;
  }
  
  .filter-input {
    min-width: auto;
  }
  
  .events-grid {
    grid-template-columns: 1fr;
  }
  
  .modal {
    padding: 1.5rem;
  }
  
  .participant-item {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .payment-info {
    text-align: left;
  }
}
</style>