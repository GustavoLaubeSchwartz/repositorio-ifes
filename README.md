## Sobre o Projeto

Este projeto foi desenvolvido como parte do Projeto Integrador acadêmico.

### Objetivos
- Desenvolver uma solução prática e profissional
- Integrar conhecimentos acadêmicos com necessidades reais do mercado
- Contribuir com a empresa ATVX Code através de uma aplicação funcional e útil

### Código SQL
```sql
CREATE TABLE `caracteristicas_disc` (
  `id_caracteristica` int NOT NULL AUTO_INCREMENT,
  `id_pergunta` int NOT NULL,
  `caracteristica` varchar(45) NOT NULL,
  `fator` enum('Dominância','Influência','Estabilidade','Conformidade') NOT NULL,
  `criado_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `atualizado_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_caracteristica`),
  UNIQUE KEY `id_caracteristica_UNIQUE` (`id_caracteristica`)
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE `links_acesso_unico` (
  `id_sessao` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `link` varchar(255) NOT NULL,
  `senha_hash` varchar(60) NOT NULL,
  `respondido` tinyint NOT NULL DEFAULT '0',
  `id_resposta` int DEFAULT NULL,
  `criado_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `respondido_em` datetime DEFAULT NULL,
  PRIMARY KEY (`id_sessao`),
  UNIQUE KEY `id_sessao_UNIQUE` (`id_sessao`),
  UNIQUE KEY `link_UNIQUE` (`link`),
  KEY `fk_links_acesso_unico_usuariios_idx` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci



CREATE TABLE `perguntas` (
  `id_pergunta` int NOT NULL AUTO_INCREMENT,
  `pergunta` varchar(60) NOT NULL,
  `criado_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `atualizado_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_pergunta`),
  UNIQUE KEY `id_pergunta_UNIQUE` (`id_pergunta`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE `respostas` (
  `id_resposta` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `dominancia` float NOT NULL,
  `influencia` float NOT NULL,
  `estabilidade` float NOT NULL,
  `conformidade` float NOT NULL,
  `motivo` varchar(45) NOT NULL,
  `respondido_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_resposta`),
  UNIQUE KEY `id_resposta_UNIQUE` (`id_resposta`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(80) DEFAULT NULL,
  `email` varchar(80) DEFAULT NULL,
  `telefone` varchar(30) DEFAULT NULL,
  `flag_acesso` tinyint NOT NULL DEFAULT '0',
  `permissao` int NOT NULL DEFAULT '0',
  `setor` varchar(45) DEFAULT NULL,
  `senha_hash` varchar(60) DEFAULT NULL,
  `criado_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `atualizado_em` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `id_usuario_UNIQUE` (`id_usuario`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `telefone_UNIQUE` (`telefone`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```


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
