<script setup lang="ts">
import { RouterView } from 'vue-router'
import GlobalLoadingComponent from '@/components/GlobalLoadingComponent.vue'
import { useGlobalLoading } from '@/stores/globalLoading'

const globalLoading = useGlobalLoading()
</script>

<template>
  <GlobalLoadingComponent :is-loading="globalLoading.isLoading" />
  <RouterView />
</template>
