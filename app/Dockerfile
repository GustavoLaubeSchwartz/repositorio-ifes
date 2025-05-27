FROM node:lts-alpine as build-stage

# Expose port for hot-reloading
EXPOSE 5173

COPY package*.json ./
RUN npm install
ENV TZ=America/Sao_Paulo

# Copy app code and set working directory
COPY . /app
WORKDIR /app/

CMD [ "npm", "run", "dev" ]