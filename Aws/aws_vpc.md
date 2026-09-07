# AWS VPC (Virtual Private Cloud)

AWS Account
│
▼
VPC (Your Private Network)
│
├── Subnet 1 (Public)
│      │
│      ├── NACL
│      └── EC2 Instance
│             └── Security Group
│
└── Subnet 2 (Private)
│
├── NACL
└── EC2 Instance
└── Security Group

1. What is VPC?

**VPC (Virtual Private Cloud)** is your own isolated virtual network inside AWS where you can launch and manage AWS resources securely.

- It is a virtual representation of a traditional network in the cloud.
- A VPC spans **all Availability Zones (AZs)** within a single AWS Region.
- Resources inside a VPC can communicate using private IP addresses.

### Example

Suppose you create a VPC in the Mumbai Region (`ap-south-1`).

The VPC can contain resources across:

- ap-south-1a
- ap-south-1b
- ap-south-1c

All these Availability Zones belong to the same VPC.

---

# Subnets

A **Subnet** is a smaller network created inside a VPC.

- VPC spans the entire Region.
- A Subnet exists within **one Availability Zone only**.
- Each subnet receives a portion of the VPC's IP address range.
- A subnet exists in **only one Availability Zone**.

### Example

VPC CIDR:

```
192.168.0.0/16
```

Subnets:

```
Public Subnet  : 192.168.1.0/24
Private Subnet : 192.168.2.0/24
```

Both subnets belong to the same VPC but are located in specific Availability Zones.

---

# Public vs Private Subnet

There is no checkbox in AWS called "Public Subnet" or "Private Subnet".

The difference is determined by the **Route Table Configuration**.

## Public Subnet

A subnet is considered public when:

- It has a route to an Internet Gateway (IGW).
- Resources inside it can access the internet directly.
- Usually contains:
    - Web Servers
    - Load Balancers
    - Bastion Hosts

### Flow

```
EC2 → Route Table → Internet Gateway → Internet
```

---

## Private Subnet

A subnet is considered private when:

- It does not have a direct route to an Internet Gateway.
- Resources cannot be accessed directly from the internet.
- Usually contains:
    - Databases
    - Internal Applications
    - Backend Services

### Flow

```
Database → Internal Network Only
```

### Real-World Example

```
VPC
│
├── Public Subnet
│     └── Web Application
│
└── Private Subnet
      └── MySQL Database
```

Users access the application through the public subnet.

The application communicates with the database using private IP addresses inside the VPC.

The database is not exposed to the internet.

> **Can an EC2 in a private subnet access the internet?**
> 

Expected answer:

> "Yes. If the private subnet's route table sends `0.0.0.0/0` traffic to a NAT Gateway, the EC2 can access the internet for outbound connections, but it cannot receive inbound internet traffic."
> 

---

# Private IP Addressing in VPC

Each VPC is assigned an internal IP address range called a **CIDR Block**.

These IP addresses are used for communication inside the VPC.

### Example

```
192.168.0.0/16
```

or

```
10.0.0.0/16
```

Resources inside the VPC use these private IPs to communicate with each other.

---

# Internet Gateway (IGW)

An **Internet Gateway** is a VPC component that enables communication between the VPC and the internet.

Without an Internet Gateway:

- Resources cannot access the internet.
- Internet traffic cannot enter the VPC.

### Flow

```
EC2 → Route Table → Internet Gateway → Internet
```

---

# Security Groups

A **Security Group** acts as a virtual firewall at the instance level.

### Characteristics

- Attached to EC2 instances.
- Controls inbound and outbound traffic.
- Stateful firewall.

**Stateful means:**

If inbound traffic is allowed, the return traffic is automatically allowed.

### Example

Allow:

```
Port 22 → SSH
Port 80 → HTTP
Port 443 → HTTPS
```

---

# Network ACL (NACL)

A **Network Access Control List (NACL)** acts as a firewall at the subnet level.

### Characteristics

- Applied to an entire subnet.
- Controls inbound and outbound traffic.
- Stateless firewall.

**Stateless means:**

You must explicitly allow both incoming and outgoing traffic.

---

# Security Group vs NACL

| Feature | Security Group | NACL |
| --- | --- | --- |
| Level | Instance Level | Subnet Level |
| Type | Stateful | Stateless |
| Allow Rules | Yes | Yes |
| Deny Rules | No | Yes |
| Applied To | EC2 Instance | Entire Subnet |

---

# CIDR Block

CIDR stands for:

**Classless Inter-Domain Routing**

It is used to define a range of IP addresses.

### Format

```
Network Address/Prefix
```

Example:

```
192.168.0.0/16
```

The `/16` indicates how many bits are reserved for the network portion.

---

## CIDR Examples

| CIDR | Total IPs |
| --- | --- |
| /32 | 1 IP |
| /24 | 256 IPs |
| /16 | 65,536 IPs |
| /8 | 16.7 Million IPs |

### Important Rule

As the CIDR number increases:

```
/16 → /24 → /28 → /32
```

The available IP range becomes **smaller**.

As the CIDR number decreases:

```
/32 → /24 → /16 → /8
```

The available IP range becomes **larger**.

---

# Quick Interview Answers

### What is VPC?

A VPC is a logically isolated virtual network in AWS where we launch and manage cloud resources securely.

### Does a VPC span multiple Availability Zones?

Yes. A VPC spans all Availability Zones within a Region.

### Does a Subnet span multiple Availability Zones?

No. A subnet exists in only one Availability Zone.

### What makes a subnet public?

A route to an Internet Gateway through its route table.

### What makes a subnet private?

No direct route to an Internet Gateway.

### What is the difference between Security Group and NACL?

Security Groups are stateful and work at the instance level, whereas NACLs are stateless and work at the subnet level.

**Security Groups are stateful because they remember established connections. If inbound traffic is allowed, the response traffic is automatically allowed without needing an explicit outbound rule.**

**Network ACLs are stateless because they do not remember connections. Every inbound and outbound packet is evaluated independently, so you must create rules for both directions.**

### What is CIDR?

CIDR is a notation used to define a range of IP addresses in a network.

A NAT Gateway is an AWS-managed service that performs Network Address Translation. It enables resources in a private subnet to access the internet for outbound connections while blocking unsolicited inbound connections from the internet.

- ✅ **Internet Gateway (IGW)** provides connectivity between a VPC and the internet.
- ✅ **NAT Gateway** provides **outbound internet access for resources in private subnets** by translating their private IP addresses to a public IP.

VPC
│
├── Internet Gateway (attached to VPC)
│
├── Route Table
│      └── Route: 0.0.0.0/0 → Internet Gateway
│
├── Public Subnet
│      └── Associated with Route Table
│
└── Private Subnet
└── Associated with Different Route Table