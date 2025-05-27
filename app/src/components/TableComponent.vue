<script setup lang="ts">
import { ref, onMounted, defineEmits, watch } from 'vue'
import PrimaryButtonComponent from '@/components/PrimaryButtonComponent.vue'
import TestResultDialogComponent from './TestResultDialogComponent.vue'
import LoadingAnimation from './LoadingAnimationComponent.vue'
import type { ApiError } from '@/types'
import answerService from '@/services/answerService'

const props = defineProps<{
  filterDatas: {
    name: string
    date: string
  }
}>()

const columns = ref([
  'Nome',
  'Email',
  'Telefone',
  'Motivo',
  'Data',
  'Setor',
  'Resultado',
])
const tableDatas = ref<Array<Answer>>([])
const selectedTestResult = ref<Answer | null>(null)
const isLoading = ref(false)
const errorMessage = ref('')
const showError = ref(false)

interface User {
  atualizado_em: string
  criado_em: string
  email: string
  flag_acesso: number
  id_usuario: number
  nome: string | null
  permissao: number
  setor: string | null
  telefone: string | null
}

interface Answer {
  id_resposta: number
  id_usuario: number
  dominancia: number
  influencia: number
  estabilidade: number
  conformidade: number
  motivo: string
  respondido_em: string
  usuarios_: User
}

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const year = date.getFullYear()
  return `${day}/${month}/${year}`
}

const emit = defineEmits<{
  (e: 'namesLoaded', names: string[]): void
}>()

async function fetchAnswer() {
  try {
    isLoading.value = true
    showError.value = false
    const response = await answerService.getAllAnswers()
    tableDatas.value = response.map(answer => ({
      ...answer,
      respondido_em: formatDate(answer.respondido_em),
    }))
    const names = [
      ...new Set(
        response
          .map(ans => ans.usuarios_.nome)
          .filter((name): name is string => name !== null),
      ),
    ]
    emit('namesLoaded', names)

    filterTableDatas()
  } catch (error) {
    const apiError = error as ApiError
    const statusCode = apiError.response?.status
    errorMessage.value = `Erro ao carregar dados! ${statusCode ? `(Status: ${statusCode})` : ''}`
    showError.value = true
    console.error('Error fetching answers:', error)
  } finally {
    isLoading.value = false
  }
}

function filterTableDatas() {
  if (props.filterDatas.name) {
    tableDatas.value = tableDatas.value.filter(
      data => data.usuarios_.nome === props.filterDatas.name,
    )
  }

  if (props.filterDatas.date) {
    tableDatas.value = tableDatas.value.filter(data => {
      const dataISO = new Date(
        data.respondido_em.split('/').reverse().join('-'),
      )
        .toISOString()
        .split('T')[0]
      return dataISO === props.filterDatas.date
    })
  }

  return tableDatas.value
}

function showResultDialog(data: Answer) {
  selectedTestResult.value = data
}

onMounted(() => {
  fetchAnswer()
})

watch(
  () => props.filterDatas,
  () => {
    fetchAnswer()
  },
  { deep: true },
)
</script>

<template>
  <div class="loading-container-table" v-if="isLoading">
    <LoadingAnimation text="Carregando dados..." />
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

    <div v-else-if="!tableDatas.length" class="no-results-container">
      <div class="no-results-content">
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
        <p>Nenhum resultado encontrado com os filtros aplicados.</p>
        <span>Tente ajustar os filtros para ver mais resultados.</span>
      </div>
    </div>

    <div class="table-container" v-else>
      <table>
        <thead>
          <tr>
            <th v-for="(column, index) in columns" :key="index">
              {{ column }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, index) in tableDatas" :key="index">
            <td>{{ data.usuarios_.nome }}</td>
            <td>{{ data.usuarios_.email }}</td>
            <td>{{ data.usuarios_.telefone }}</td>
            <td>{{ data.motivo }}</td>
            <td>{{ data.respondido_em }}</td>
            <td>{{ data.usuarios_.setor }}</td>
            <td class="last-column">
              <PrimaryButtonComponent
                buttonLabel="Ver Resultado"
                type="button"
                @click="showResultDialog(data)"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <TestResultDialogComponent
        v-if="selectedTestResult"
        :testResult="selectedTestResult"
        @close="selectedTestResult = null"
      />
    </div>
  </div>
</template>

<style scoped>
.table-container {
  overflow-x: auto;
  margin-top: 20px;
  width: 100%;
}

.table-container::-webkit-scrollbar {
  height: 8px;
}

.table-container::-webkit-scrollbar-thumb {
  background-color: var(--color-secondary-gray);
  border-radius: 32px;
}

.table-container::-webkit-scrollbar-track {
  background-color: #cccccc;
  border-radius: 32px;
}

.loading-container-table {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.no-results-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  border-radius: 12px;
  border: 1px solid var(--color-secondary-gray);
  margin-top: 40px;
  padding: 32px;
}

.no-results-content {
  text-align: center;
  color: #666;
}

.no-results-content .icon {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
  color: var(--color-secondary-gray);
}

.no-results-content p {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.no-results-content span {
  font-size: 14px;
  color: #999;
}

table {
  border-collapse: collapse;
  color: var(--color-base-gray);
  min-width: 1312px;
  width: 100%;
}

th,
td {
  border-bottom: 1px solid var(--color-secondary-gray);
  padding: 8px;
  text-align: left;
}

@media screen and (max-width: 480px) {
  table {
    border-collapse: collapse;
    color: var(--color-base-gray);
    min-width: 1240px;
    width: 100%;
  }

  th,
  td {
    font-size: 12px;
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
</style>
