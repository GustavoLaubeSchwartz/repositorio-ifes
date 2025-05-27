# PersonaVix - ATVX Code

## Sobre o Projeto

Este projeto foi desenvolvido como parte do Projeto Integrador acadêmico e está sendo utilizado ativamente pela empresa ATVX Code. O PersonaVix é uma aplicação moderna construída com Vue 3 e Vite, demonstrando a integração entre o ambiente acadêmico e o mercado de trabalho.

### Objetivos
- Desenvolver uma solução prática e profissional
- Integrar conhecimentos acadêmicos com necessidades reais do mercado
- Contribuir com a empresa ATVX Code através de uma aplicação funcional e útil

## Configuração do Ambiente

### Pré-requisitos
- Docker
- Docker Compose
- Node.js (versão 16 ou superior)
- npm ou yarn

### Configuração com Docker Compose

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd ac-atvx-personavix
```

2. Crie o arquivo `.env` na raiz do projeto:
```bash
cp .env.example .env
```

3. Inicie os containers com Docker Compose:
```bash
docker-compose up -d
```

4. Instale as dependências dentro do container:
```bash
docker-compose exec app npm install
```

5. Execute as migrações do banco de dados (se necessário):
```bash
docker-compose exec app npm run migrate
```

### Comandos Docker Compose Úteis

- Iniciar os containers:
```bash
docker-compose up -d
```

- Parar os containers:
```bash
docker-compose down
```

- Visualizar logs:
```bash
docker-compose logs -f
```

- Acessar o shell do container:
```bash
docker-compose exec app sh
```

### Portas Utilizadas
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Banco de Dados: 5432

## Configuração Técnica

### IDE Recomendada
- [VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (desabilitar Vetur)

### Suporte a TypeScript
Para arquivos `.vue`, o TypeScript requer configuração especial. Utilizamos `vue-tsc` para verificação de tipos e [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) para suporte em editores.

## Configuração do Projeto (Desenvolvimento Local)

### Instalação
```sh
npm install
```

### Desenvolvimento
```sh
npm run dev
```

### Build para Produção
```sh
npm run build
```

### Testes Unitários
```sh
npm run test:unit
```

### Linting
```sh
npm run lint
```

## Tecnologias Utilizadas
- Vue 3
- TypeScript
- Vite
- ESLint
- Vitest
- Docker
- Docker Compose

## Estrutura do Projeto
```
ac-atvx-personavix/
├── app/                 # Frontend Vue.js
├── api/                 # Backend API
├── docker/             # Configurações Docker
├── docker-compose.yml  # Configuração Docker Compose
└── .env               # Variáveis de ambiente
```
