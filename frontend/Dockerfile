# ---------- Stage 1: Build ----------
FROM node:18-alpine as builder

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy source code
COPY . .

# Build the React app
RUN npm run build


# ---------- Stage 2: Serve ----------
FROM nginx:alpine

# Copy built files from previous stage
COPY --from=builder /app/build /usr/share/nginx/html

# Replace default Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
