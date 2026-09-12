# Multi-stage Dockerfile for ProofForge AI Platform

# Stage 1: Build the React + Vite application
FROM node:24-alpine AS builder

WORKDIR /app

# Copy package manifests and install dependencies
COPY package*.json ./
RUN npm ci

# Copy codebase
COPY . .

# Build production dist bundle
RUN npm run build

# Stage 2: Serve production bundle with Nginx
FROM nginx:alpine AS runner

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy build artifacts from stage 1
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
