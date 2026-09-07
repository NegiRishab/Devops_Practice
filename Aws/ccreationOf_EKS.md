# Amazon EKS (Elastic Kubernetes Service) - Complete Notes

## EKS Cluster Creation Flow

1. Create IAM Role for EKS Control Plane
2. Create VPC (using CloudFormation)
3. Create EKS Cluster
4. Connect kubectl to the cluster
5. Create IAM Role for Worker Nodes
6. Create Node Group
7. Configure Cluster Autoscaler
8. Deploy Applications
9. Create Fargate IAM Role
10. Create Fargate Profile

---

# 1. Create IAM Role for EKS Cluster

Before creating an EKS cluster, AWS needs permissions to create and manage AWS resources on our behalf.

We create an **IAM Role**.

- Trusted Service → **EKS**
- Attach required AWS managed policies.

### IAM Basics

**Role**

- Represents an identity used by AWS services.
- Contains permissions.

**Policy**

- A collection of permissions.
- Defines what actions are allowed or denied.

Example:

IAM Role

↓

AmazonEKSClusterPolicy

choose aws-service and in eks choose the manage cluster one 

Now EKS can create and manage networking resources required for the control plane.

---

# 2. Create VPC

Instead of using the default VPC, we create a dedicated VPC for EKS.

## Why not use the Default VPC?

Because Kubernetes has networking requirements that work best with a properly configured VPC.

EKS requires:

- Public Subnets
- Private Subnets
- Route Tables
- Internet Gateway
- NAT Gateway
- Security Groups
- Network ACLs

Using a dedicated VPC avoids networking issues and follows AWS best practices.

---

## How Networking Works

There are two different parts of an EKS cluster.

### AWS Managed Control Plane

AWS creates and manages:

- Kubernetes API Server
- Scheduler
- Controller Manager
- etcd

These run inside an AWS-managed VPC (not inside our AWS account).

We never manage these EC2 instances.

---

### Worker Nodes

Worker Nodes are EC2 instances running inside **our AWS account** and **our VPC**.

They execute:

- Pods
- Containers
- kubelet
- kube-proxy

---

The Worker Nodes must communicate securely with the AWS-managed Control Plane.

Therefore AWS automatically creates networking rules and Security Groups that allow communication between both.

---

## VPC Components

```
VPC
│
├── Subnets
│     ├── Public
│     └── Private
│
├── Route Tables
├── Internet Gateway
├── NAT Gateway
├── Network ACLs
└── Security Groups
```

Remember:

- VPC contains Subnets
- Subnets use Route Tables
- Subnets can have Network ACLs
- EC2 instances use Security Groups

---

## Creating the VPC

We do **not** manually create all networking resources.

Instead we use an AWS CloudFormation template.

CloudFormation is AWS Infrastructure as Code (IaC).

It automatically creates:

- VPC
- Subnets
- Route Tables
- NAT Gateway
- Internet Gateway
- Security Groups

Everything needed for EKS.

make sure ehen you run this stack or create  choose region first

https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml

---

# 3. Create the EKS Cluster

After the networking is ready,

Create the EKS Cluster.

The Control Plane is now created by AWS.

At this stage:

- Kubernetes Master Components exist.
- No Worker Nodes exist yet.

The cluster cannot run Pods yet.

---

# 4. Connect kubectl to the Cluster

Run:

```
aws eks update-kubeconfig --name worker-cluster-practice --region us-east-1
```

This command updates the local kubeconfig file.

Now kubectl knows:

- Cluster endpoint
- Authentication method
- Cluster certificate

After this we can run:

```
kubectlget nodes
kubectlget pods
```

---

# 

# 5. Create IAM Role for the Node Group

Worker nodes in Amazon EKS are **EC2 instances**.

Each worker node runs the following Kubernetes components:

- **kubelet** – communicates with the EKS control plane.
- **kube-proxy** – manages network traffic for Kubernetes Services.
- **Container Runtime** – runs the application containers.

The **kubelet** needs permission to communicate with AWS services. For example, it must be able to:

- Join the EKS cluster.
- Pull container images from Amazon ECR.
- Communicate with AWS resources required by Kubernetes networking.

## Creating the IAM Role

1. Go to **IAM → Roles → Create Role**.
2. Choose **AWS Service**.
3. Select **EC2** as the trusted service.
4. Create the role (for example, `node-group-practice`).

## Required IAM Policies

This role **must** have the following three AWS managed policies attached:

### 1. AmazonEKSWorkerNodePolicy

Provides the permissions required for the EC2 worker nodes to communicate with the Amazon EKS control plane and register themselves with the cluster.

### 2. AmazonEC2ContainerRegistryPullOnly

Allows the worker nodes to pull container images from **Amazon Elastic Container Registry (ECR)**.

> In older tutorials, you may see **AmazonEC2ContainerRegistryReadOnly**. AWS now recommends **AmazonEC2ContainerRegistryPullOnly** for EKS worker nodes.
> 

### 3. AmazonEKS_CNI_Policy

Provides the permissions required by the **Amazon VPC CNI plugin** to manage networking resources, such as Elastic Network Interfaces (ENIs) and IP addresses, on EC2 instances.

## Why is this IAM Role required?

Without this IAM role and its required policies:

- The EC2 instances cannot join the EKS cluster.
- They cannot pull container images from ECR.
- Kubernetes networking will not function correctly.
- The node group may remain in the **Creating** state and eventually fail with a **NodeCreationFailure** error.

---

# 6. Create Node Group

A Node Group is a managed collection of EC2 Worker Nodes.

AWS automatically:

- Launches EC2 instances
- Replaces unhealthy nodes
- Handles upgrades
- Integrates with Auto Scaling Groups

---

# 7. Cluster Autoscaler

The Cluster Autoscaler automatically adjusts the number of Worker Nodes based on workload.

If Pods cannot be scheduled because there is not enough CPU or memory:

→ Launch new EC2 instances.

When nodes become empty:

→ Remove unused EC2 instances.

This reduces AWS costs.

---

## How does Cluster Autoscaler create EC2 Instances?

The Cluster Autoscaler runs as a Pod inside Kubernetes.

But a Pod cannot directly call AWS APIs.

It first needs permission.

---

## Authentication

Kubernetes uses:

- Service Accounts

AWS uses:

- IAM Roles

We need a secure bridge between them.

---

## OIDC (OpenID Connect)

EKS provides an OIDC Identity Provider.

This allows Kubernetes Service Accounts to securely assume IAM Roles.

Flow:

```
Cluster Autoscaler Pod
        │
        │
Service Account
        │
OIDC Token
        │
AWS verifies token
        │
Assume IAM Role
        │
Temporary AWS Credentials
        │
AWS Auto Scaling API
        │
Launch/Delete EC2 Instances
```

This mechanism is called **IAM Roles for Service Accounts (IRSA).**

---

## Steps

### 1. Create a Custom IAM Policy

Permissions:

- Describe Auto Scaling Groups
- Set Desired Capacity
- Terminate EC2 Instances
- Describe Launch Templates

{
"Version": "2012-10-17",
"Statement": [
{
"Action": [
"autoscaling:DescribeAutoScalingGroups",
"autoscaling:DescribeAutoScalingInstances",
"autoscaling:DescribeLaunchConfigurations",
"autoscaling:DescribeScalingActivities",
"autoscaling:SetDesiredCapacity",
"autoscaling:TerminateInstanceInAutoScalingGroup",
"ec2:DescribeInstanceTypes",
"ec2:DescribeLaunchTemplateVersions"
],
"Resource": "*",
"Effect": "Allow"
}
]
}

---

### 2. Create an OIDC Provider

Associate your EKS cluster with an OIDC Identity Provider.

---

### 3. Create an IAM Role

Trusted Entity:

- Web Identity

Attach:

- Custom Autoscaler Policy

Configure:

- OIDC Provider
- Audience (`sts.amazonaws.com`)
- Service Account Conditions

---

### 4. Add Tags to the Auto Scaling Group

The Node Group's Auto Scaling Group must contain tags like:

```
k8s.io/cluster-autoscaler/enabled = true

k8s.io/cluster-autoscaler/<cluster-name> = owned
```

These tags allow the Cluster Autoscaler to discover which Auto Scaling Groups it is allowed to manage.

---

## Deploy Cluster Autoscaler

Deploy the official YAML manifest.

https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml

Update:

Cluster Name

```
--cluster-name=eks-cluster-practice
```

Add Service Account Annotation

```
annotations:
  eks.amazonaws.com/role-arn: arn:aws:iam::<ACCOUNT_ID>:role/ClusterAutoscalerRole
```

Prevent Eviction

```
cluster-autoscaler.kubernetes.io/safe-to-evict:"false"
```

This prevents the Cluster Autoscaler Pod from being evicted during node scaling operations.

---

Add Recommended Arguments

```
- --balance-similar-node-groups
- --skip-nodes-with-system-pods=false
```

---

Update Image Version

Always match the Cluster Autoscaler version with your Kubernetes version.

Example:

Kubernetes 1.33

↓

Cluster Autoscaler v1.33.x

---

## 

---

# 8. Deploy Applications

Now deploy your Kubernetes applications.

The applications run on the Worker Nodes.

this we can use to set the tiem 

```yaml
    - --scale-down-unneeded-time=1m
            - --scale-down-delay-after-add=1m
            - --scale-down-delay-after-delete=30s
```

---

# 9. Amazon EKS Fargate

Fargate is a serverless compute engine for Kubernetes.

You don't manage EC2 instances.

AWS provisions compute automatically for each Pod.

---

## Characteristics

- No EC2 management
- One Pod per Fargate VM (microVM)
- Serverless
- AWS manages infrastructure
- Good for stateless workloads
- Not suitable for many stateful applications or DaemonSets

---

# 10. Create IAM Role for Fargate

Pods running on Fargate still run kubelet components managed by AWS.

AWS requires an IAM Role so the Fargate infrastructure can communicate with the EKS cluster.

Create:

**Amazon EKS Fargate Pod Execution Role**

---

# 11. Create a Fargate Profile

A Fargate Profile tells EKS:

**Which Pods should run on Fargate?**

It contains Pod selection rules.

---

## Pod Selection

Selection is based on:

- Namespace (required)
- Labels (optional)

Example:

```
Namespace:
dev

Label:
app=frontend
```

Only Pods matching both conditions will run on Fargate.

---

## Why does Fargate need the VPC?

Even though AWS manages the compute infrastructure, the Pods still receive IP addresses from **your VPC subnets**.

Networking remains part of your AWS account.

Therefore, when creating a Fargate Profile, you must specify the private subnets where the Pods will receive their IP addresses.

---

## Why only Private Subnets?

Fargate Pods are launched only in private subnets.

This improves security because Pods are not directly exposed to the internet.

---

# Mixed Node Group + Fargate

An EKS cluster can use both Worker Nodes and Fargate at the same time.

Example:

```
EKS Cluster
│
├── Node Group
│      ├── Production
│      └── Stateful Applications
│
└── Fargate
       ├── Development
       ├── Testing
       └── Stateless Applications
```

Pods matching a Fargate Profile are launched on Fargate.

All other Pods run on the EC2 Node Group.

---

# Common Use Cases

### Development Environment

```
Namespace: dev
→ Fargate

Namespace: prod
→ Node Group
```

This avoids paying for EC2 instances dedicated to development.

---

### Stateful vs Stateless Applications

Run on **Node Group**:

- Databases
- StatefulSets
- Storage-intensive applications

Run on **Fargate**:

- REST APIs
- Microservices
- Backend services
- Frontend applications
- Jobs and CronJobs

---

# Final Architecture

```
                    AWS Managed
              ┌──────────────────────┐
              │  EKS Control Plane   │
              │ API Server           │
              │ Scheduler            │
              │ Controller Manager   │
              └──────────┬───────────┘
                         │
                Secure Communication
                         │
        ┌────────────────┴────────────────┐
        │                                 │
   EC2 Node Group                  Fargate Profile
   (Your AWS Account)             (AWS Managed Compute)
        │                                 │
     Multiple Pods                  Selected Pods
```