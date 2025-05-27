import { ref } from 'vue'
import { defineStore } from 'pinia'

const showDialog = ref(false)

export const useShowUpdateUserDatasDialog = defineStore(
  'showUpdateUserDatasDialog',
  () => {
    function toggleVisibility() {
      showDialog.value = !showDialog.value
    }

    return { showDialog, toggleVisibility }
  },
)
