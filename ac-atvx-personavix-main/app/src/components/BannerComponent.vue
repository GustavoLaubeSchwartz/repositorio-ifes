<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import BackIcon from './icons/BackIcon.vue'
import NextIcon from './icons/NextIcon.vue'

const currentSlide = ref(0)
const totalSlides = 3
let slideInterval: NodeJS.Timeout

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % totalSlides
}

const prevSlide = () => {
  currentSlide.value = (currentSlide.value - 1 + totalSlides) % totalSlides
}

const goToSlide = (index: number) => {
  currentSlide.value = index
}

onMounted(() => {
  slideInterval = setInterval(() => {
    nextSlide()
  }, 3000)
})

onBeforeUnmount(() => {
  clearInterval(slideInterval)
})
</script>

<template>
  <header>
    <div class="header-content">
      <div class="header-content-slide">
        <BackIcon
          class="back-icon"
          aria-label="Previous Slide"
          @click="prevSlide"
        />

        <div class="header-content-slide-container">
          <div class="header-content-slide-content" v-show="currentSlide === 0">
            <h1>Teste DISC</h1>
            <h3>Descubra o seu perfil comportamental</h3>
          </div>
          <div class="header-content-slide-content" v-show="currentSlide === 1">
            <h1>Dica</h1>
            <h3>Seja Autêntico em suas respostas</h3>
          </div>
          <div class="header-content-slide-content" v-show="currentSlide === 2">
            <h1>Use o resultado para</h1>
            <h3>Entender seus pontos fortes e áreas de melhoria</h3>
          </div>
        </div>

        <NextIcon
          class="next-icon"
          aria-label="Next Slide"
          @click="nextSlide"
        />
      </div>

      <div class="header-buttons">
        <div
          v-for="(slide, index) in totalSlides"
          :key="index"
          :class="{ active: currentSlide === index }"
          @click="goToSlide(index)"
          :aria-label="'Slide ' + (index + 1)"
        ></div>
      </div>
    </div>
  </header>
</template>

<style scoped>
header {
  background: linear-gradient(
    to right,
    var(--color-base-green),
    var(--color-base-blue)
  );
  height: 366px;
  width: 100%;
  position: relative;
}

h1,
h3,
li {
  color: #ffffff;
}

li {
  font-size: 20px;
  margin-bottom: 8px;
}

ul {
  list-style: none;
}

.header-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.header-content-slide {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.header-content-slide-container {
  width: 70%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.header-content-slide-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  text-align: center;
}

.back-icon,
.next-icon {
  cursor: pointer;
}

.back-icon {
  margin-left: 10%;
}

.next-icon {
  margin-right: 10%;
}

.header-buttons {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 48px;
  & div {
    background: #ffffff;
    border-radius: 50%;
    height: 12px;
    opacity: 0.5;
    width: 12px;
    cursor: pointer;
    transition: opacity 0.3s ease;
  }
  & div.active {
    opacity: 1;
  }
}

@media (max-width: 1024px) {
  h1 {
    font-size: 48px;
  }

  h3 {
    font-size: 28px;
  }

  .back-icon {
    margin-left: 5%;
  }

  .next-icon {
    margin-right: 5%;
  }
}

@media (max-width: 744px) {
  header {
    height: 320px;
  }

  h1 {
    font-size: 42px;
  }

  h3 {
    font-size: 26px;
  }

  .back-icon,
  .next-icon {
    width: 60px;
  }

  .back-icon {
    margin-left: 3.5%;
  }

  .next-icon {
    margin-right: 3.5%;
  }

  .header-buttons div {
    height: 10px;
    width: 10px;
  }
}

@media (max-width: 480px) {
  header {
    height: 220px;
  }

  h1 {
    font-size: 32px;
  }

  h3 {
    font-size: 18px;
  }

  .back-icon,
  .next-icon {
    display: none;
  }

  .header-content-slide-container {
    padding: 0 16px;
    width: 100%;
  }

  .header-buttons {
    gap: 12px;
    margin-top: 32px;
    & div {
      height: 8px;
      width: 8px;
    }
  }
}
</style>
