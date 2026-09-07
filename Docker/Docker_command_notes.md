# 

| Command | Purpose | Example | Where Used |
| --- | --- | --- | --- |
| `docker --version` | Check Docker version | `docker --version` | Verify Docker installation |
| `docker info` | Show Docker system info | `docker info` | Debugging Docker environment |
| `docker pull` | Download image from registry | `docker pull nginx` | Before running containers |
| `docker images` | List downloaded images | `docker images` | Check available images |
| `docker run` | Create & start container | `docker run nginx` | Run application |
| `docker run -d` | Run in background | `docker run -d nginx` | Production/background services |
| `docker run -p` | Port mapping | `docker run -p 8080:80 nginx` | Access app from browser |
| `docker run --name` | Assign container name | `docker run --name web nginx` | Easy container management |
| `docker ps` | Show running containers | `docker ps` | Monitor active containers |
| `docker ps -a` | Show all containers | `docker ps -a` | Debug stopped containers |
| `docker stop` | Stop container | `docker stop web` | Graceful shutdown |
| `docker start` | Start stopped container | `docker start web` | Restart old containers |
| `docker restart` | Restart container | `docker restart web` | Apply config changes |
| `docker rm` | Remove container | `docker rm web` | Cleanup unused containers |
| `docker rm -f` | Force remove container | `docker rm -f web` | Remove stuck containers |
| `docker rmi` | Remove image | `docker rmi nginx` | Free disk space |
| `docker logs` | View logs | `docker logs web` | Debug applications |
| `docker logs -f` | Live logs | `docker logs -f web` | Real-time monitoring |
| `docker exec -it` | Enter running container | `docker exec -it web bash` | Troubleshooting |
| `docker inspect` | Detailed container info | `docker inspect web` | Network/IP/debugging |
| `docker build` | Build image from Dockerfile | `docker build -t app:v1 .` | Create custom images |
| `docker push` | Upload image to registry | `docker push user/app:v1` | CI/CD deployment |
| `docker login` | Login to Docker Hub | `docker login` | Push/pull private images |
| `docker cp` | Copy files | `docker cp file.txt web:/tmp` | Transfer files |
| `docker stats` | Resource usage | `docker stats` | Monitor CPU/RAM |
| `docker network ls` | List networks | `docker network ls` | Container networking |
| `docker network create` | Create custom network | `docker network create mynet` | Multi-container communication |
| `docker volume create` | Create volume | `docker volume create data` | Persistent storage |
| `docker system df` | Docker disk usage | `docker system df` | Storage troubleshooting |
| `docker system prune` | Remove unused resources | `docker system prune` | Cleanup Docker |
| `docker system prune -a` | Remove all unused images/resources | `docker system prune -a` | Free heavy disk space |
| `docker compose up` | Start multi-container app | `docker compose up -d` | Run complete stack |
| `docker compose down` | Stop compose services | `docker compose down` | Stop application stack |