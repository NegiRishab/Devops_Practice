FROM node:20-alpine

WORKDIR /app

COPY package.json .

RUN npm install

COPY ./public ./public
COPY ./server.js ./server.js

CMD ["node", "server.js"]