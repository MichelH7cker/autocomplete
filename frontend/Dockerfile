# --- STAGE 1: build ---
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

# Copia todo o código-fonte do frontend.
COPY . .

RUN npm run build

# --- STAGE 2: nginx ---
FROM nginx:1.25-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
