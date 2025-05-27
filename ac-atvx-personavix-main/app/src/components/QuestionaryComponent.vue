<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useQuestionaryAnswers } from '@/stores/questionaryAnswers'
import { useUniqueAccessLinkDatas } from '@/stores/uniqueAccessLinkDatas'
import { useUserDatas } from '@/stores/userDatas'
import TestResultComponent from './TestResultComponent.vue'
import LoadingAnimationComponent from './LoadingAnimationComponent.vue'
import questionaryService from '@/services/questionaryService'
import type { Answers, ApiError, CadasteredAnswer, Questionary } from '@/types'

const uniqueAccessLinkDatas = useUniqueAccessLinkDatas()
const userDatas = useUserDatas()
const questionaryStore = useQuestionaryAnswers()

const showQuestionary = ref(true)
const testResult = ref<CadasteredAnswer | null>(null)
const id_test_response = ref<number | null>(null)
const questionary = ref<Questionary | null>(null)
const currentQuestionIndex = ref(0)
const selectedAnswers = ref<
  Array<{ id_pergunta: number; id_caracteristica: number; fator: string }>
>([])
const isLoading = ref(false)
const errorMessage = ref('')
const showError = ref(false)
const lastOperation = ref<'fetch' | 'submit'>('fetch')

const currentQuestion = computed(
  () => questionary.value?.questions[currentQuestionIndex.value] ?? null,
)

const currentCharacteristics = computed(
  () =>
    questionary.value?.disc_characteristics.filter(
      char => char.id_pergunta === currentQuestion.value?.id_pergunta,
    ) ?? [],
)

async function retryOperation() {
  showError.value = false
  if (lastOperation.value === 'fetch') {
    await fetchQuestionary()
  } else {
    await HandleWithTestResponseCadastrer()
  }
}

async function fetchQuestionary() {
  try {
    lastOperation.value = 'fetch'
    isLoading.value = true
    showError.value = false
    const response = await questionaryService.getQuestionary()
    questionary.value = {
      questions: response.questions,
      disc_characteristics: response.disc_characteristics,
    }
  } catch (error) {
    const apiError = error as ApiError
    errorMessage.value =
      'Erro ao carregar o questionário. Por favor, tente novamente.'
    showError.value = true
    console.error('Erro ao carregar questionário:', apiError)
  } finally {
    isLoading.value = false
  }
}

const progressPercentage = computed(() => {
  const totalQuestions = questionary.value?.questions.length ?? 0
  return totalQuestions > 0
    ? ((currentQuestionIndex.value + 1) / totalQuestions) * 100
    : 0
})

const questionProgress = computed(() => {
  const totalQuestions = questionary.value?.questions.length ?? 0
  return `${currentQuestionIndex.value + 1}/${totalQuestions}`
})

function selectCharacteristic(id_characteristic: number, factor: string) {
  if (currentQuestion.value) {
    selectedAnswers.value.push({
      id_pergunta: currentQuestion.value.id_pergunta,
      id_caracteristica: id_characteristic,
      fator: factor,
    })
    nextQuestion()
  }
}

function nextQuestion() {
  if (
    currentQuestionIndex.value <
    (questionary.value?.questions.length ?? 0) - 1
  ) {
    currentQuestionIndex.value++
  } else {
    submitAnswers()
  }
}

function calculatePercentages(): Answers {
  const totalAnswers = selectedAnswers.value.length
  const factorCounts = selectedAnswers.value.reduce(
    (acc, answer) => {
      acc[answer.fator] = (acc[answer.fator] || 0) + 1
      return acc
    },
    {} as Record<string, number>,
  )

  const percentages = Object.keys(factorCounts).map(fator => ({
    fator,
    percentage: ((factorCounts[fator] / totalAnswers) * 100).toFixed(2),
  }))

  const discFactors: Answers = {
    dominancia: 0,
    influencia: 0,
    estabilidade: 0,
    conformidade: 0,
  }

  percentages.forEach(({ fator, percentage }) => {
    if (fator === 'Dominância') {
      discFactors.dominancia = parseFloat(percentage)
    } else if (fator === 'Influência') {
      discFactors.influencia = parseFloat(percentage)
    } else if (fator === 'Estabilidade') {
      discFactors.estabilidade = parseFloat(percentage)
    } else if (fator === 'Conformidade') {
      discFactors.conformidade = parseFloat(percentage)
    }
  })

  return discFactors
}

function submitAnswers() {
  showQuestionary.value = false
  const test_result: Answers = calculatePercentages()
  questionaryStore.setDiscFactors(test_result)

  HandleWithTestResponseCadastrer()
}

async function HandleWithTestResponseCadastrer() {
  const questionaryResponseData = {
    motivo: questionaryStore.sessionData?.reason ?? '',
    dominancia: questionaryStore.sessionData?.disc_factors.dominancia ?? 0,
    influencia: questionaryStore.sessionData?.disc_factors.influencia ?? 0,
    estabilidade: questionaryStore.sessionData?.disc_factors.estabilidade ?? 0,
    conformidade: questionaryStore.sessionData?.disc_factors.conformidade ?? 0,
    id_sessao: uniqueAccessLinkDatas.sessionData?.id_sessao ?? null,
  }

  try {
    lastOperation.value = 'submit'
    isLoading.value = true
    showError.value = false
    const response = await questionaryService.submitAnswers(
      userDatas.userDatas?.id_usuario ?? 0,
      questionaryResponseData,
    )
    id_test_response.value = response.id_resposta
    testResult.value = response
  } catch (error) {
    const apiError = error as ApiError
    errorMessage.value =
      'Erro ao enviar as respostas. Por favor, tente novamente.'
    showError.value = true
    console.error('Erro ao enviar respostas:', apiError)
  } finally {
    uniqueAccessLinkDatas.setResponded()
    isLoading.value = false
  }
}

onMounted(() => {
  fetchQuestionary()
})
</script>

<template>
  <div class="loading-container" v-if="isLoading">
    <LoadingAnimationComponent text="Carregando..." />
  </div>
  <div v-if="!testResult">
    <div class="questionary" v-if="currentQuestion && showQuestionary">
      <div class="error-message" v-if="showError">
        <p>{{ errorMessage }}</p>
        <button class="retry-button" @click="retryOperation">
          Tentar Novamente
        </button>
      </div>
      <h4>{{ currentQuestion.pergunta }}</h4>

      <div class="characteristics">
        <button
          v-for="char in currentCharacteristics"
          :key="char.id_caracteristica"
          @click="selectCharacteristic(char.id_caracteristica, char.fator)"
        >
          {{ char.caracteristica }}
        </button>
      </div>
    </div>
  </div>

  <div class="progress-bar-container" v-if="showQuestionary">
    <div class="progress-bar">
      <div
        class="progress-bar-fill"
        :style="{ width: `${progressPercentage}%` }"
      ></div>
    </div>
    <p>{{ questionProgress }}</p>
  </div>

  <TestResultComponent
    v-if="testResult"
    :id_response="id_test_response"
  ></TestResultComponent>
</template>

<style scoped>
.questionary {
  align-items: center;
  display: flex;
  flex-direction: column;
  gap: 32px;
  justify-content: center;
}

.characteristics {
  display: flex;
  gap: 16px;
  & button {
    background: none;
    border: 1px solid var(--color-base-blue);
    border-radius: 8px;
    color: var(--color-base-blue);
    font-size: 18px;
    padding: 10px;
    width: 192px;
  }
}

button {
  transition: background-color 0.3s;
}

button:hover {
  background-color: #e0e0e0;
}

.progress-bar-container {
  width: 100%;
  margin-top: 16px;
  text-align: center;
}

.progress-bar {
  background-color: #f0f0f0;
  border-radius: 8px;
  height: 10px;
  overflow: hidden;
  width: 80%;
  margin: 0 auto;
}

.progress-bar-fill {
  background-color: var(--color-base-blue);
  height: 100%;
  transition: width 0.3s ease-in-out;
}

p {
  margin-top: 8px;
  font-size: 14px;
  color: #555;
}

@media screen and (max-width: 780px) {
  .questionary {
    display: flex;
    flex-direction: column;
  }
}

.error-message {
  background-color: #ffebee;
  border: 1px solid #ffcdd2;
  border-radius: 4px;
  color: #c62828;
  margin-bottom: 16px;
  padding: 12px;
  text-align: center;
  width: 100%;
}

.error-message p {
  margin: 0;
  font-size: 14px;
}

.retry-button {
  background-color: var(--color-base-blue);
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  font-size: 14px;
  margin-top: 8px;
  padding: 8px 16px;
  transition: background-color 0.3s;
}

.retry-button:hover {
  background-color: #1976d2;
}
</style>
