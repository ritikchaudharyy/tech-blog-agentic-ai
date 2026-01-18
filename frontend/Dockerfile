# ============================================
# Stage 1: Build Stage
# ============================================
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# ============================================
# Stage 2: Production Stage with Nginx
# ============================================
FROM nginx:alpine AS production

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:80 || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]