
variable "eks_cluster_name" { type = string }
variable "eks_version" { type = string }
variable "eks_node_ami_type" { type = string }
variable "eks_node_desired_capacity" { type = number }
variable "eks_node_max_capacity" { type = number }
variable "eks_node_min_capacity" { type = number }
variable "eks_node_instance_type" { type = string }

variable "eks_public_access_cidrs" {
  description = "Public egress CIDRs of Jenkins and administrators allowed to reach the EKS API."
  type        = list(string)
}

module "my_eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "21.24.0"

  name                                     = var.eks_cluster_name
  kubernetes_version                       = var.eks_version
  subnet_ids                               = module.my_vpc.private_subnets
  vpc_id                                   = module.my_vpc.vpc_id
  endpoint_public_access                   = true
  endpoint_private_access                  = true
  endpoint_public_access_cidrs             = var.eks_public_access_cidrs
  enable_cluster_creator_admin_permissions = true
  eks_managed_node_groups = {
    my_node_group = {
      ami_type     = var.eks_node_ami_type
      desired_size = var.eks_node_desired_capacity
      max_size     = var.eks_node_max_capacity
      min_size     = var.eks_node_min_capacity

      instance_types = [var.eks_node_instance_type]
    }
  }

  addons = {
    aws-ebs-csi-driver = {
      pod_identity_association = [{
        role_arn        = aws_iam_role.ebs_csi.arn
        service_account = "ebs-csi-controller-sa"
      }]
    }
    coredns = {}
    eks-pod-identity-agent = {
      before_compute = true
    }
    kube-proxy = {}
    vpc-cni = {
      before_compute = true
    }
  }

  depends_on = [aws_iam_role_policy_attachment.ebs_csi]
}
