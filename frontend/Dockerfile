FROM node:18-alpine AS builder

WORKDIR /app

ARG VITE_GRAPHQL_URI
ENV VITE_GRAPHQL_URI=${VITE_GRAPHQL_URI}

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:1.25-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
