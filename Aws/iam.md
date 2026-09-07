# AWS Account, IAM, Regions & Availability Zones — Structured Notes

## 1. AWS Account Basics

When you create an AWS account, AWS automatically creates a **Root User**.

### Root User

- The root user has **unlimited permissions** in the AWS account.
- It can access and modify everything.
- Root user credentials should be used **rarely** and kept secure.

### Best Practice

After creating the AWS account:

1. Enable MFA (Multi-Factor Authentication) on the root account.
2. Create an **Admin IAM User** with limited day-to-day usage.
3. Use the admin IAM user instead of the root user.

---

## 2. IAM (Identity and Access Management)

AWS Identity and Access Management

IAM is used to:

- Create users
- Manage permissions
- Control access to AWS services

---

# IAM Components

## A. IAM Users

An IAM User represents a person or application that needs access to AWS.

### Types of Users

### 1. Human Users

Examples:

- Developers
- DevOps Engineers
- Security Team

### 2. System Users

Used by applications/tools.

Examples:

- Jenkins
- Terraform
- CI/CD pipelines
- Applications/scripts

---

### Example

A developer may need:

- EC2 access
- S3 read access

A Jenkins server may need:

- Deploy permissions
- Access to artifacts in S3

---

## B. IAM Groups

Groups help manage permissions for multiple users together.

Instead of assigning permissions one-by-one, you:

1. Create a group
2. Attach permissions to the group
3. Add users to the group

---

### Example

### Developers Group

Permissions:

- EC2 access
- CloudWatch logs access

Users:

- Rishabh
- Amit
- Neha

All users inherit the group permissions.

---

## C. IAM Roles

Roles are used when:

- AWS services need to access other AWS services
- Temporary access is needed

### Important

Roles do **NOT** have username/passwords.

They provide temporary permissions.

---

### Example: EC2 accessing S3

Suppose:

- An EC2 instance needs to read files from S3.

Wrong approach:

- Store AWS access keys inside EC2

Correct approach:

- Attach an IAM Role to EC2

The role gives EC2 temporary permissions to access S3 securely.

---

# IAM Users vs IAM Roles

| Feature | IAM User | IAM Role |
| --- | --- | --- |
| Used by | Humans or applications | AWS services or temporary access |
| Has password/access keys | Yes | No |
| Long-term access | Yes | Usually temporary |
| Example | Developer login | EC2 accessing S3 |

---

# AWS Infrastructure Scopes

AWS services operate at different scopes.

There are mainly 3 scopes:

1. Global
2. Regional
3. Availability Zone (AZ)

---

# 1. Global Services

These services are not tied to a single region.

They work globally across AWS.

### Examples

- IAM
- Route 53
- Billing
- CloudFront

### Explanation

If you create:

- an IAM user
- or a Route 53 hosted zone

it is available globally.

---

# 2. Regional Services

These services belong to a specific AWS Region.

### Examples

- VPC
- S3
- RDS
- Lambda

### Example

If you create an S3 bucket in:

- `ap-south-1` (Mumbai)

it exists in that region.

---

# 3. Availability Zone (AZ) Services

Some resources are created inside a specific Availability Zone.

### Examples

- EC2 instances
- EBS volumes

---

## Example

Region:

- `ap-south-1` (Mumbai)

Availability Zones:

- `ap-south-1a`
- `ap-south-1b`
- `ap-south-1c`

An EC2 instance may run specifically in:

- `ap-south-1a`

An EBS volume is also tied to a single AZ.

---

# Region vs Availability Zone

| Region | Availability Zone |
| --- | --- |
| Geographic area | Isolated data center inside a region |
| Example: Mumbai (`ap-south-1`) | Example: `ap-south-1a` |
| Contains multiple AZs | Part of one region |
| Used for disaster isolation across countries/areas | Used for high availability inside a region |

---

## Real-World Analogy

### Region

Think of a **city**.

Example:

- Mumbai
- Singapore
- Frankfurt

### Availability Zone

Think of different **buildings/data centers** inside that city.

If one building fails:

- another AZ can still work.

---

# Important AWS Examples by Scope

| Scope | Services |
| --- | --- |
| Global | IAM, Route53, Billing, CloudFront |
| Regional | S3, VPC, RDS, Lambda |
| AZ-based | EC2, EBS |

---

# Quick Revision Notes

## Root User

- Full access
- Avoid daily usage
- Enable MFA

## IAM User

- For humans/applications
- Has credentials

## IAM Group

- Collection of users
- Easier permission management

## IAM Role

- Temporary permissions
- Mostly for AWS services

## Global Services

- IAM, Route53

## Regional Services

- S3, VPC

## AZ Services

- EC2, EBS

## Region

- Geographic location

## Availability Zone

- Isolated data center inside a region