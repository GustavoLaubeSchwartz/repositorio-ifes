import { ref } from 'vue'
import { defineStore } from 'pinia'

interface Answers {
  reason: string
  disc_factors: {
    dominancia: number
    influencia: number
    estabilidade: number
    conformidade: number
  }
}

export const useQuestionaryAnswers = defineStore('questionaryAnswers', () => {
  const sessionData = ref<Answers | null>(null)

  function setReason(reason: string) {
    if (!sessionData.value) {
      sessionData.value = {
        reason: '',
        disc_factors: {
          dominancia: 0,
          influencia: 0,
          estabilidade: 0,
          conformidade: 0,
        },
      }
    }

    sessionData.value.reason = reason
  }

  function setDiscFactors(discFactors: Partial<Answers['disc_factors']>) {
    if (!sessionData.value) {
      sessionData.value = {
        reason: '',
        disc_factors: {
          dominancia: 0,
          influencia: 0,
          estabilidade: 0,
          conformidade: 0,
        },
      }
    }

    Object.entries(discFactors).forEach(([key, value]) => {
      if (key in sessionData.value!.disc_factors) {
        sessionData.value!.disc_factors[key as keyof Answers['disc_factors']] =
          value || 0
      }
    })
  }

  function clearSessionData() {
    sessionData.value = null
  }

  return {
    sessionData,
    setReason,
    setDiscFactors,
    clearSessionData,
  }
})
