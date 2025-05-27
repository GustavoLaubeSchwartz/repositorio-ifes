<script setup lang="ts">
import { computed } from 'vue'
import { useUserDatas } from '@/stores/userDatas'
import { useUniqueAccessLinkDatas } from '@/stores/uniqueAccessLinkDatas'
import { useQuestionaryAnswers } from '@/stores/questionaryAnswers'
import NavBar from '@/components/NavBarComponent.vue'
import BannerComponent from '@/components/BannerComponent.vue'
import Footer from '@/components/FooterComponent.vue'
import QuestionaryComponent from '@/components/QuestionaryComponent.vue'
import ReasonFormComponent from '@/components/ReasonFormComponent.vue'
import TestResultComponent from '@/components/TestResultComponent.vue'
import CadastreUserDatasDialogComponent from '@/components/CadastreUserDatasDialogComponent.vue'

const userDatas = useUserDatas()
const uniqueAccessLinkDatas = useUniqueAccessLinkDatas()
const questionaryAnswers = useQuestionaryAnswers()

// Computed properties for controlling what should be rendered
const currentView = computed(() => {
  if (uniqueAccessLinkDatas.sessionData?.respondido) {
    return 'testResult'
  } else if (!questionaryAnswers.sessionData?.reason) {
    return 'reasonForm'
  } else {
    return 'questionary'
  }
})
</script>

<template>
  <NavBar />
  <BannerComponent />
  <section>
    <div class="primary-form">
      <TestResultComponent
        v-if="currentView === 'testResult'"
        :id_response="uniqueAccessLinkDatas.sessionData?.id_resposta ?? null"
      />
      <ReasonFormComponent v-else-if="currentView === 'reasonForm'" />
      <QuestionaryComponent v-else-if="currentView === 'questionary'" />

      <CadastreUserDatasDialogComponent
        :canClose="false"
        v-if="!userDatas.userDatas?.nome"
      />
    </div>
  </section>
  <Footer />
</template>

<style scoped>
section {
  align-items: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: 64px;
}

.primary-form {
  align-items: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
}

@media (max-width: 860px) {
  section {
    margin: 64px 32px;
  }
}

@media (max-width: 480px) {
  section {
    margin: 64px 16px;
  }
}
</style>
