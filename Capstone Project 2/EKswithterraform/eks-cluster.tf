
variable "eks_cluster_name" {}
variable "eks_version" {}
variable "eks_node_ami_type" {}
variable "eks_node_desired_capacity" {}
variable "eks_node_max_capacity" {}
variable "eks_node_min_capacity" {}
variable "eks_node_instance_type" {}

module "my_eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "21.24.0"

  name                                     = var.eks_cluster_name
  kubernetes_version                       = var.eks_version
  subnet_ids                               = module.my_vpc.private_subnets
  vpc_id                                   = module.my_vpc.vpc_id
  endpoint_public_access                   = true
  enable_cluster_creator_admin_permissions = true
  eks_managed_node_groups = {
    my_node_group = {
      ami_type         = var.eks_node_ami_type
      desired_size     = var.eks_node_desired_capacity
      max_size         = var.eks_node_max_capacity
      min_size         = var.eks_node_min_capacity

      instance_types = [var.eks_node_instance_type]
    }
  }

  addons = {
    coredns = {}
    eks-pod-identity-agent = {
      before_compute = true
    }
    kube-proxy = {}
    vpc-cni = {
      before_compute = true
    }
  }
}
