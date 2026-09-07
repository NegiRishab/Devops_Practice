this is backend file , 

- **RUN** → Command executed at **build time** while creating the image.
- **CMD** → **Default command/arguments** executed when the container starts; can be overridden.
- **ENTRYPOINT** → Defines the **main executable** when the container starts; normally not replaced by normal runtime arguments.

### Notes version

```
RUN        → Build-time command
CMD        → Default runtime command/arguments
ENTRYPOINT → Main/fixed runtime executable
```

--omit=dev becuae we dotn want to instal devdependencies ,  npm ci look foer the package.json and install the depedcy form it , 

```docker
FROM node:20-alpine

WORKDIR /app  this will create a new folder in the image

COPY package.json package-lock.json ./        this is to copy the the versions
RUN npm ci --omit=dev                         
 this is okay only when we dont have the build in build we will need devdependecies so make sure on that ,
COPY src ./src  copy the source code 

EXPOSE 5000

CMD ["npm", "run", "start"]   this is to start the server 

```

forntend or build application those need build 

we not use omit dev beuase for build we need the devdepedencies 

```docker
FROM node:20-alpine AS builder   stage 1

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci    here we did not ommit because we need devdependecies 

this will check depedencies in package.json both dependecies and dev depedenies

COPY src ./src
COPY index.html ./index.html
COPY vite.config.js ./vite.config.js

ARG VITE_API_URL=http://localhost:5000/api
ENV VITE_API_URL=$VITE_API_URL

this is set for the image build processs 

RUN npm run build

FROM nginx:alpine
for frotned best practice is to use the nginx work as reverse proxy 

COPY --from=builder /app/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]

```

if we direct run the frontend and backedn we need the network in which tehy communicate, 

but if we use docker compsose file it will create one networedk and use it, for all containers 

```
version: "3.9"
services:
  frontend:
    image: ankit42098/taskboard-frontend:v1
    container_name: taskboard-frontend
    ports:
      - "80:80"
    restart: unless-stopped
    depends_on:
      - backend

  backend:
    image: ankit42098/taskboard-backend:v1
    container_name: taskboard-backend
    ports:
      - "5000:5000"
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/taskboard
      - PORT=5000
      - NODE_ENV=production
      - CORS_ORIGIN=http://localhost
    restart: unless-stopped
    depends_on:
      - mongodb

  mongodb:
    image: mongo:latest
    container_name: mongodb
    ports:
      - "27017:27017"
    restart: unless-stopped
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

check how volumes set, how dependson work, image is puling from remote repo , 

i push there image first and here i am fetching tghem 

docker push  image name 

docker build -t iamge naem 

docker volume ls

docker logs contianername 

docker network  ls

docker netwrok create 

Port mapping connects a port on the Docker host to a port inside the container. If an application is listening on port 4000 inside the container and we want users on the host/network to access it through port 5000, we map `5000:4000`.