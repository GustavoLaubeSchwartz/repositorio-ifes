<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import LoadingAnimationComponent from './LoadingAnimationComponent.vue'
import { useQuestionaryAnswers } from '@/stores/questionaryAnswers'
import type { ApiError } from '@/types'
import answerService from '@/services/answerService'

const questionaryStore = useQuestionaryAnswers()

const props = defineProps<{
  id_response?: number | null
  testResult?: Answer
}>()

interface Answer {
  id_resposta: number
  id_usuario: number
  dominancia: number
  influencia: number
  estabilidade: number
  conformidade: number
  motivo: string
  respondido_em: string
}

const result = ref<Answer | null>(null)
const isLoading = ref(false)
const errorMessage = ref('')
const showError = ref(false)

async function fetchAnswer() {
  if (props.id_response) {
    try {
      isLoading.value = true
      showError.value = false
      const response = await answerService.getAnswerById(props.id_response)
      result.value = response.data
    } catch (error) {
      const apiError = error as ApiError
      const statusCode = apiError.response?.status
      errorMessage.value = `Erro ao carregar resultado! ${statusCode ? `(Status: ${statusCode})` : ''}`
      showError.value = true
      console.error('Error fetching answer:', error)
    } finally {
      isLoading.value = false
    }
  }
}

onMounted(() => {
  if (props.testResult) {
    result.value = props.testResult
  } else if (!questionaryStore.sessionData) {
    fetchAnswer()
  } else {
    result.value = {
      id_resposta: 0,
      id_usuario: 0,
      dominancia: questionaryStore.sessionData.disc_factors.dominancia,
      influencia: questionaryStore.sessionData.disc_factors.influencia,
      estabilidade: questionaryStore.sessionData.disc_factors.estabilidade,
      conformidade: questionaryStore.sessionData.disc_factors.conformidade,
      motivo: questionaryStore.sessionData.reason ?? '',
      respondido_em: new Date().toISOString(),
    }
  }
})

const dominantTrait = computed(() => {
  if (questionaryStore.sessionData) {
    const traits = {
      Dominância: questionaryStore.sessionData.disc_factors.dominancia,
      Influência: questionaryStore.sessionData.disc_factors.influencia,
      Estabilidade: questionaryStore.sessionData.disc_factors.estabilidade,
      Conformidade: questionaryStore.sessionData.disc_factors.conformidade,
    }

    const sortedTraits = Object.entries(traits).sort(([, a], [, b]) => b - a)
    return sortedTraits[0]
  } else {
    if (!result.value) return null

    const traits = {
      Dominância: result.value.dominancia,
      Influência: result.value.influencia,
      Estabilidade: result.value.estabilidade,
      Conformidade: result.value.conformidade,
    }

    const sortedTraits = Object.entries(traits).sort(([, a], [, b]) => b - a)
    return sortedTraits[0]
  }
})

type FactorKey = keyof FactorsDescriptions

interface FactorDescription {
  description: string
  strengths: string
  weaknesses: string
}

interface FactorsDescriptions {
  Dominância: FactorDescription
  Influência: FactorDescription
  Estabilidade: FactorDescription
  Conformidade: FactorDescription
}

const factorsDescriptions: FactorsDescriptions = {
  Dominância: {
    description:
      'Indivíduos com alta dominância são focados em resultados, desafiadores e diretos. Gostam de tomar decisões rápidas e enfrentam problemas de forma assertiva.',
    strengths: 'Determinação, foco em resultados, liderança.',
    weaknesses:
      'Impaciência, tendência a ser agressivo e a não ouvir os outros.',
  },
  Influência: {
    description:
      'Pessoas influentes são sociáveis, persuasivas e entusiásticas. Elas se destacam na comunicação e na construção de relacionamentos.',
    strengths: 'Habilidade de comunicação, motivação, entusiasmo.',
    weaknesses:
      'Impulsividade, dificuldade em lidar com detalhes e disciplina.',
  },
  Estabilidade: {
    description:
      'Indivíduos estáveis são calmos, pacientes e empáticos. Preferem ambientes previsíveis e colaborativos, focando em apoio e estabilidade.',
    strengths: 'Empatia, paciência, habilidade para trabalhar em equipe.',
    weaknesses:
      'Resistência a mudanças, dificuldade em tomar decisões rápidas.',
  },
  Conformidade: {
    description:
      'Pessoas com alta conformidade são detalhistas, analíticas e orientadas para normas. Valorizam precisão e qualidade em suas tarefas.',
    strengths: 'Atenção aos detalhes, foco em qualidade e organização.',
    weaknesses:
      'Perfeccionismo, dificuldade em lidar com improvisação e mudanças rápidas.',
  },
}
</script>

<template>
  <div class="loading-container" v-if="isLoading">
    <LoadingAnimationComponent text="Carregando resultado..." />
  </div>

  <div v-else>
    <div v-if="showError" class="error-container">
      <div class="error-content">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
        >
          <circle cx="12" cy="12" r="10" stroke-width="2" />
          <line x1="12" y1="8" x2="12" y2="12" stroke-width="2" />
          <line x1="12" y1="16" x2="12.01" y2="16" stroke-width="2" />
        </svg>
        <p>{{ errorMessage }}</p>
        <span>Tente recarregar a página ou contate o suporte.</span>
      </div>
    </div>

    <div class="test-result" v-else-if="result">
      <h1>Resultado do Teste</h1>
      <div class="test-result-container">
        <table>
          <thead>
            <tr>
              <th>Fator</th>
              <th>Porcentagem</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Dominância</td>
              <td>{{ result.dominancia }}%</td>
            </tr>
            <tr>
              <td>Influência</td>
              <td>{{ result.influencia }}%</td>
            </tr>
            <tr>
              <td>Estabilidade</td>
              <td>{{ result.estabilidade }}%</td>
            </tr>
            <tr>
              <td>Conformidade</td>
              <td>{{ result.conformidade }}%</td>
            </tr>
          </tbody>
        </table>

        <div v-if="dominantTrait">
          <h2>Característica Predominante</h2>
          <h3>{{ dominantTrait[0] }}</h3>
          <p>
            {{ factorsDescriptions[dominantTrait[0] as FactorKey].description }}
          </p>
          <p>
            <strong>Pontos fortes:</strong>
            {{ factorsDescriptions[dominantTrait[0] as FactorKey].strengths }}
          </p>
          <p>
            <strong>Pontos fracos:</strong>
            {{ factorsDescriptions[dominantTrait[0] as FactorKey].weaknesses }}
          </p>
        </div>
      </div>
    </div>

    <div v-else class="no-result-container">
      <div class="no-result-content">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
        >
          <path
            d="M21 21l-4.35-4.35"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <circle
            cx="10"
            cy="10"
            r="7"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
        <p>Nenhum resultado encontrado.</p>
        <span>Verifique se o ID da resposta está correto.</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
table {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 20px;
}

th,
td {
  border: 1px solid #ddd;
  text-align: left;
  padding: 8px;
}

th {
  background-color: #f4f4f4;
}

h1 {
  font-size: 48px;
  text-align: center;
}

h3 {
  margin-bottom: 8px;
  margin-top: 16px;
}

p {
  margin-bottom: 16px;
  text-align: justify;
}

strong {
  font-weight: 400;
}

.test-result {
  display: flex;
  flex-direction: column;
  gap: 32px;
  padding: 16px;
  width: 100%;
}

.test-result-container {
  display: flex;
  gap: 32px;
}

@media screen and (max-width: 840px) {
  h1 {
    font-size: 36px;
  }

  .test-result-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
    & h2 {
      text-align: center;
    }
  }
}

@media screen and (max-width: 480px) {
  h1 {
    font-size: 32px;
  }
}

.error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  border-radius: 12px;
  border: 1px solid var(--color-error);
  margin-top: 40px;
  padding: 32px;
  background-color: var(--color-error-light);
}

.error-content {
  text-align: center;
  color: var(--color-error);
}

.error-content .icon {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
}

.error-content p {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.error-content span {
  font-size: 14px;
  color: var(--color-error-dark);
}

.no-result-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  border-radius: 12px;
  border: 1px solid var(--color-secondary-gray);
  margin-top: 40px;
  padding: 32px;
}

.no-result-content {
  text-align: center;
  color: #666;
}

.no-result-content .icon {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
  color: var(--color-secondary-gray);
}

.no-result-content p {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.no-result-content span {
  font-size: 14px;
  color: #999;
}
</style>
