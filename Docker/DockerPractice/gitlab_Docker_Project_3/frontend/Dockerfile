FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
ARG VITE_API_BASE_URL=http://13.232.43.163:8080/api
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npm run build
EXPOSE 4173
CMD ["npm", "run", "preview"]
