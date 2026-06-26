FROM node:24-alpine as deps

WORKDIR /app

# Копируем файлы зависимостей и устанавливаем
COPY package*.json ./
RUN npm ci


FROM node:24-alpine as builder

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules

COPY . .

RUN npm run build


FROM nginx:alpine as production

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
