# Taskboard: simple Ansible + Kubernetes showcase

This example uses the React frontend, Node.js backend, and MongoDB from
`../../completeProject1`. It shows how Ansible can deploy the app to an existing
Kubernetes cluster. Creating the cluster and building images are separate steps.
No cluster is needed to read the project or render the example manifest.

```text
Ansible → render manifest → kubectl apply → wait for deployments

Browser → frontend (Nginx, NodePort 30080)
               └── /api → backend:5000 → mongodb:27017
                                            └── persistent storage (2Gi)
```

## Files

| File | Purpose |
| --- | --- |
| `deploy.yaml` | Kubernetes configuration and tasks to generate, apply, and wait |
| `project-vars.yaml` | Frontend and backend image names |
| `inventory.ini` | Run Ansible locally, where kubectl is configured |
| `ansible.cfg` | Select the inventory |
| `taskboard.yaml` | Generated Kubernetes manifest; do not edit directly |

Edit image names in `project-vars.yaml` and Kubernetes settings in `deploy.yaml`.
Ansible substitutes the variables directly into the playbook's `copy.content`
and writes `taskboard.yaml`. There are no separate `.j2` files. Running the
playbook again recreates this file, so manual edits to it will be overwritten.
The same playbook can be run manually or from Jenkins.

## Showcase without deploying

With Ansible installed, run from this directory:

```bash
cd ansible/k8s_project
ansible-playbook deploy.yaml --syntax-check
ansible-playbook deploy.yaml --tags render
```

The second command creates `taskboard.yaml` for inspection. It does not call
kubectl or contact a cluster. The image names in `project-vars.yaml` are examples.

## How someone would deploy it later

These steps are for a future real deployment. They require Docker to build
images, Ansible and kubectl locally, and an existing Kubernetes cluster with a
default StorageClass. kubectl must already be configured to access that cluster.
The example runs one replica of each component; MongoDB has a persistent volume
and is accessible through an internal service. It uses no database authentication
and is intended for a learning/demo environment.

1. Build and push the Project1 images from the repository root, replacing
   `your-dockerhub-user` with your registry username:

   ```bash
   docker build -t your-dockerhub-user/taskboard-backend:k8s-v1 completeProject1/backend
   docker build --build-arg VITE_API_URL=/api -t your-dockerhub-user/taskboard-frontend:k8s-v1 completeProject1/frontend
   docker push your-dockerhub-user/taskboard-backend:k8s-v1
   docker push your-dockerhub-user/taskboard-frontend:k8s-v1
   ```

   The frontend must be built with `VITE_API_URL=/api`. Project1's current Jenkins
   pipeline builds an absolute server URL into the frontend; that existing image
   needs rebuilding for this example. A container environment variable cannot
   change Vite's already-built JavaScript.

2. Set the two image names in `project-vars.yaml`. This simple example assumes
   public images. Private registries need additional image-pull credentials
   configured in the cluster.

3. Confirm the intended cluster and run the playbook:

   ```bash
   cd ansible/k8s_project
   kubectl config current-context
   ansible-playbook deploy.yaml
   kubectl -n taskboard get pods,services,pvc
   ```

4. Open `http://<your-node-ip>:30080` with TCP port 30080 accessible. Alternatively,
   use `kubectl -n taskboard port-forward service/frontend 8080:80` and open
   `http://localhost:8080`. The browser sends API calls to the same frontend address;
   Nginx forwards them to the internal backend service.

For updates, push images with new tags, update the variables, and run the same
playbook again. MongoDB keeps its data in the PVC across pod replacements. Its
deployment uses `Recreate` so two MongoDB pods do not use the same data directory.

Reference: [Kubernetes workload management](https://kubernetes.io/docs/concepts/workloads/management/)
documents the `kubectl apply` and `kubectl rollout status` flow used here.
