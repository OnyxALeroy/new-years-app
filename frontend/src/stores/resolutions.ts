import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Resolution, ResolutionCreate, ResolutionUpdate } from '@/types'
import { resolutionsAPI } from '@/utils/api'

export const useResolutionStore = defineStore('resolutions', () => {
  const resolutions = ref<Resolution[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchResolutions = async () => {
    loading.value = true
    error.value = null
    try {
      resolutions.value = await resolutionsAPI.getResolutions()
    } catch (err) {
      error.value = 'Failed to fetch resolutions'
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchAllResolutions = async () => {
    loading.value = true
    error.value = null
    try {
      resolutions.value = await resolutionsAPI.getAllResolutions()
    } catch (err) {
      error.value = 'Failed to fetch all resolutions'
      throw err
    } finally {
      loading.value = false
    }
  }

  const createResolution = async (resolutionData: ResolutionCreate) => {
    loading.value = true
    error.value = null
    try {
      const newResolution = await resolutionsAPI.createResolution(resolutionData)
      resolutions.value.push(newResolution)
      return newResolution
    } catch (err) {
      error.value = 'Failed to create resolution'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateResolution = async (id: string, updateData: ResolutionUpdate) => {
    loading.value = true
    error.value = null
    try {
      const updatedResolution = await resolutionsAPI.updateResolution(id, updateData)
      const index = resolutions.value.findIndex(r => r.id === id)
      if (index !== -1) {
        resolutions.value[index] = updatedResolution
      }
      return updatedResolution
    } catch (err) {
      error.value = 'Failed to update resolution'
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteResolution = async (id: string) => {
    loading.value = true
    error.value = null
    try {
      await resolutionsAPI.deleteResolution(id)
      resolutions.value = resolutions.value.filter(r => r.id !== id)
    } catch (err) {
      error.value = 'Failed to delete resolution'
      throw err
    } finally {
      loading.value = false
    }
  }

  const toggleComplete = async (id: string) => {
    const resolution = resolutions.value.find(r => r.id === id)
    if (resolution) {
      await updateResolution(id, { completed: !resolution.completed })
    }
  }

  return {
    resolutions,
    loading,
    error,
    fetchResolutions,
    fetchAllResolutions,
    createResolution,
    updateResolution,
    deleteResolution,
    toggleComplete,
  }
})