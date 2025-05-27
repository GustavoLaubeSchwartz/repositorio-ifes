<script setup lang="ts">
import { ref, computed } from 'vue'
import FilterIcon from '@/components/icons/FilterIcon.vue'
import NavBarComponent from '@/components/NavBarComponent.vue'
import FooterComponent from '@/components/FooterComponent.vue'
import SelectboxComponent from '@/components/SelectboxComponent.vue'
import CadastreInputComponent from '@/components/CadastreInputComponent.vue'
import PrimaryButtonComponent from '@/components/PrimaryButtonComponent.vue'
import TableComponent from '@/components/TableComponent.vue'

const name = ref('')
const date = ref('')

const filterDatas = ref({
  name: '',
  date: '',
})

const nameOptions = ref<{ id: number; option: string }[]>([])

function handleNamesLoaded(names: string[]) {
  nameOptions.value = names.map((n, i) => ({ id: i + 1, option: n }))
}

const selectedName = computed(() => {
  const found = nameOptions.value.find(
    option => option.id === Number(name.value),
  )
  return found ? found.option : ''
})

function getFilterDatas(event: Event) {
  event.preventDefault()
  filterDatas.value = {
    name: selectedName.value,
    date: date.value,
  }
}
</script>

<template>
  <NavBarComponent navBarTitle="Relatórios" />

  <main>
    <h4>Resultados</h4>

    <form @submit.prevent="getFilterDatas">
      <SelectboxComponent label="Nome" :options="nameOptions" v-model="name" />
      <CadastreInputComponent type="date" label="Data" v-model="date" />
      <PrimaryButtonComponent
        buttonLabel="Filtrar"
        :iconComponent="FilterIcon"
        class="filter-button"
        type="submit"
      />
    </form>

    <TableComponent
      @namesLoaded="handleNamesLoaded"
      :filterDatas="filterDatas"
    />
  </main>

  <FooterComponent />
</template>

<style scoped>
main {
  margin: 64px;
}

h4 {
  color: var(--color-base-blue);
  font-weight: 300;
  margin-bottom: 16px;
}

form {
  align-items: end;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 32px;
  justify-content: flex;
}

@media screen and (max-width: 860px) {
  form {
    gap: 16px;
  }
}
</style>
