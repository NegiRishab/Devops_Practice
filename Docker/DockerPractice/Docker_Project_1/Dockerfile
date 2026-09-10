From node:22-alpine

RUN mkdir -p /home/app


WORKDIR /home/app 

COPY package.json /home/app
COPY index.html /home/app
COPY server.js /home/app
RUN npm install


CMD ["node", "server.js"]