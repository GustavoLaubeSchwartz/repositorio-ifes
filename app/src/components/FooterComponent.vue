<script setup lang="ts">
import PhoneIcon from './icons/PhoneIcon.vue'
import EmailIcon from './icons/EmailIcon.vue'
import LinkedInIcon from './icons/LinkedInIcon.vue'
import InstagramIcon from './icons/InstagramIcon.vue'
import InternetIcon from './icons/InternetIcon.vue'
import LocalIcon from './icons/LocalIcon.vue'

const actualYear = new Date().getFullYear()
</script>

<template>
  <footer>
    <div class="footer-container">
      <div class="footer-container-informations">
        <div class="footer-contact-info">
          <EmailIcon />
          <p>
            <a
              href="mailto:contato@autvix.com.br"
              target="_blank"
              rel="noopener noreferrer"
              >contato@autvix.com.br</a
            >
          </p>
        </div>
        <div class="footer-contact-info">
          <PhoneIcon />
          <p>
            <a href="" target="_blank" rel="noopener noreferrer"
              >+55 27 3039-6559</a
            >
          </p>
        </div>
        <div class="footer-contact-info">
          <LinkedInIcon />
          <p>
            <a
              href="https://www.linkedin.com/company/autvix/"
              target="_blank"
              rel="noopener noreferrer"
              >Autvix Group</a
            >
          </p>
        </div>
        <div class="footer-contact-info">
          <InstagramIcon />
          <p>
            <a
              href="https://www.instagram.com/autvix/"
              target="_blank"
              rel="noopener noreferrer"
              >@autvix</a
            >
          </p>
        </div>
      </div>

      <hr />

      <div class="footer-container-informations">
        <div class="footer-contact-info">
          <InternetIcon />
          <p>
            <a
              href="https://autvix.com.br/"
              target="_blank"
              rel="noopener noreferrer"
              >www.autvix.com.br</a
            >
          </p>
        </div>
        <div class="footer-contact-info">
          <LocalIcon />
          <p>
            <a
              href="https://www.google.com.br/maps/place/Autvix+Group/@-20.1989675,-40.2314492,21z/data=!4m15!1m8!3m7!1s0xb81e9ef58b5821:0xb0251edc4ab51295!2sR.+dos+Bem-te-vis+-+Carapina,+Serra+-+ES,+29166-767!3b1!8m2!3d-20.1992507!4d-40.2306747!16s%2Fg%2F1pzx8srck!3m5!1s0xb81ee9d519c28d:0x55e674256168f2fb!8m2!3d-20.1990241!4d-40.2312019!16s%2Fg%2F1hhgrz3yz?entry=ttu&g_ep=EgoyMDI0MTAxNi4wIKXMDSoASAFQAw%3D%3D"
              target="_blank"
              rel="noopener noreferrer"
              >Av. Jerônimo Monteiro, 1000, Centro, Vitória - ES, 29010-003</a
            >
          </p>
        </div>
        <div class="footer-contact-info">
          <p>
            A Autvix Group é uma empresa que está sempre em busca de melhoria
            contínua e eficácia, sempre valorizando as ideias e soluções.
          </p>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <p>© {{ actualYear }} Autvix Group.</p>
    </div>
  </footer>
</template>

<style scoped>
footer {
  margin-top: 62px;
}

hr {
  border: solid 1px #000000;
  height: 256px;
  width: 1px;
}

a {
  text-decoration: none;
  color: inherit;
}

a:visited {
  color: inherit;
}

p {
  color: #000000;
  font-size: 16px;
  font-weight: 200;
}

.footer-bottom {
  background: linear-gradient(
    to right,
    var(--color-base-green),
    var(--color-base-blue)
  );
  display: flex;
  height: 48px;
  justify-content: center;
  margin-top: 64px;
  padding: 16px;
  & p {
    color: #ffffff;
    font-size: 16px;
    font-weight: 200;
  }
}

.footer-container {
  align-items: center;
  display: flex;
  flex-direction: row;
  gap: 16px;
  justify-content: center;
}

.footer-container-informations {
  display: flex;
  flex-direction: column;
  gap: 28px;
  height: 100%;
  justify-content: space-evenly;
  padding: 16px;
  width: 100%;
}

.footer-contact-info {
  align-items: center;
  display: flex;
  gap: 8px;
  justify-content: center;
  width: 100%;
}

@media screen and (max-width: 490px) {
  hr {
    height: 1px;
    margin: 32px auto;
    width: 80%;
  }

  p {
    font-size: 14px;
  }

  .footer-container {
    flex-direction: column;
  }

  .footer-container-informations {
    padding: 0 48px;
    width: 100%;
  }
}
</style>
