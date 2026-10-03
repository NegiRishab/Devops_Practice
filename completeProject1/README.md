# Taskboard DevOps Project

This is a simple task board application with a React frontend, a Node.js backend, and MongoDB. The project shows how DevOps tools work together to test, package, and deploy an application.

- **Jenkins** connects the whole process. It runs the tests, calls Terraform, builds Docker images, and starts the deployment through Ansible.
- **Terraform** creates the application server on Linode and passes its IP address back to the pipeline.
- **Docker** packages the frontend and backend into separate images so they can run as containers on the server.
- **Docker Hub and AWS ECR** are the two image registry options in the pipeline. ECR is currently active, while the Docker Hub functions are commented out and kept for switching back.
- **Ansible** connects to the server, installs Docker and Docker Compose, and prepares the application configuration.
- **Docker Compose** runs the frontend, backend, and MongoDB together on the server.

The overall flow is:

```text
Jenkins → Run tests → Terraform prepares the server
        → Build Docker images → Push to Docker Hub or ECR
        → Ansible configures the server → Docker Compose runs the app
```

The `Jenkinsfile` defines the stages, and `pipeline.groovy` contains the work each stage performs. The `terraform/` and `ansible/` folders hold the server and deployment configuration.
