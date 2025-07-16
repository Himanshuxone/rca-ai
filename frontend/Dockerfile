# Stage 1: Build the React app
FROM node:18 AS build

WORKDIR /app
COPY package.json ./
COPY package-lock.json ./
RUN npm install

COPY . ./
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy built React files to Nginx's web root
COPY --from=build /app/build /usr/share/nginx/html

# Replace the default Nginx config with custom config (optional)
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
