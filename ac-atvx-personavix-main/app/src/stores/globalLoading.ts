import { defineStore } from 'pinia'

export const useGlobalLoading = defineStore('globalLoading', {
  state: () => ({
    isLoading: false,
  }),
  actions: {
    setLoading(isLoading: boolean) {
      this.isLoading = isLoading
    },
  },
})
