# 1. Configure AWS CLI

Before using AWS CLI, AWS needs to know:

- Which AWS user you are
- Which AWS region to use
- Output format

```
aws configure

```

Example:

```
AWS Access Key ID: <ACCESS_KEY>
AWS Secret Access Key: <SECRET_KEY>
Default region name: ap-south-1
Default output format: json
```

Verify configuration:

```
aws sts get-caller-identity
```

---

# 2. VPC Commands

## List all VPCs

```
aws ec2 describe-vpcs
```

Purpose:

- Shows all VPCs available in the selected region.

---

# 3. Security Group Commands

## List all Security Groups

```
aws ec2 describe-security-groups
```

---

## View a Specific Security Group

```
aws ec2 describe-security-groups--group-ids sg-xxxxxxxx
```

Example:

```
aws ec2 describe-security-groups--group-ids sg-0123456789abcdef
```

---

## Create a Security Group

```
aws ec2 create-security-group \
--group-name my-security-group \
--description"My security group" \
--vpc-id vpc-xxxxxxxx
```

---

## Add Inbound Rule

Allow HTTP traffic (Port 80):

```
aws ec2 authorize-security-group-ingress \
--group-id sg-xxxxxxxx \
--protocol tcp \
--port80 \
--cidr0.0.0.0/0
```

### Common Ports

| Service | Port |
| --- | --- |
| SSH | 22 |
| HTTP | 80 |
| HTTPS | 443 |
| Jenkins | 8080 |
| MongoDB | 27017 |

Example SSH Rule:

```
aws ec2 authorize-security-group-ingress \
--group-id sg-xxxxxxxx \
--protocol tcp \
--port22 \
--cidr0.0.0.0/0
```

---

# 4. Key Pair Commands

## Create a Key Pair

```
aws ec2 create-key-pair \
--key-name my-key-pair \
--query'KeyMaterial' \
--output text > my-key-pair.pem
```

Give proper permissions:

```
chmod400 my-key-pair.pem
```

Purpose:

- Used to SSH into EC2 instances.

---

# 5. Subnet Commands

## List all Subnets

```
aws ec2 describe-subnets
```

Purpose:

- Get subnet IDs before launching EC2.

---

# 6. EC2 Instance Commands

## Launch an EC2 Instance

```
aws ec2 run-instances \
--image-id ami-xxxxxxxx \
--count1 \
--instance-type t3.micro \
--key-name my-key-pair \
--security-group-ids sg-xxxxxxxx \
--subnet-id subnet-xxxxxxxx
```

### Parameters

| Parameter | Purpose |
| --- | --- |
| image-id | AMI ID |
| count | Number of instances |
| instance-type | Server size |
| key-name | SSH key pair |
| security-group-ids | Firewall rules |
| subnet-id | Network location |

---

## List EC2 Instances

```
aws ec2 describe-instances
```

---

# 7. IAM Group Management

## Create a Group

```
aws iam create-group \
--group-name MyGroup
```

Purpose:

- Groups users together and assigns permissions once.

---

## View Group Details

```
aws iam get-group \
--group-name MyGroup
```

---

# 8. IAM User Management

## Create a User

```
aws iam create-user \
--user-name MyUser
```

---

## View User Details

```
aws iam get-user \
--user-name MyUser
```

---

## Add User to Group

```
aws iam add-user-to-group \
--group-name MyGroup \
--user-name MyUser
```

---

# 9. IAM Policies

## Find Policy ARN

Example:

```
aws iam list-policies \
--query'Policies[?PolicyName==`AmazonEC2FullAccess`].Arn' \
--output text
```

---

## Attach Policy to Group

```
aws iam attach-group-policy \
--group-name MyGroup \
--policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess
```

Purpose:

- Gives EC2 full permissions to every user inside the group.

---

## List Policies Attached to Group

```
aws iam list-attached-group-policies \
--group-name MyGroup
```

---

# 10. IAM Console Login Password

## Create Login Password

```
aws iam create-login-profile \
--user-name MyUser \
--password MyPassword123! \
--password-reset-required
```

Purpose:

- Allows IAM user to log into AWS Console.
- Forces password change at first login.

---

# 11. Custom IAM Policy

Example Policy (Password Change Only)

Create file:

```
{
  "Version":"2012-10-17",
  "Statement": [
    {
      "Effect":"Allow",
      "Action": [
"iam:ChangePassword"
      ],
      "Resource":"arn:aws:iam::<ACCOUNT_ID>:user/MyUser"
    },
    {
      "Effect":"Allow",
      "Action": [
"iam:GetAccountPasswordPolicy"
      ],
      "Resource":"*"
    }
  ]
}
```

Save as:

```
password-policy.json
```

Create Policy:

```
aws iam create-policy \
--policy-name change-password-policy \
--policy-document file://password-policy.json
```

---

## Attach Custom Policy

```
aws iam attach-group-policy \
--group-name MyGroup \
--policy-arn arn:aws:iam::<ACCOUNT_ID>:policy/change-password-policy
```

---

# 12. Access Keys

## Create Access Key for User

```
aws iam create-access-key \
--user-name MyUser
```

Output:

```
AccessKeyId
SecretAccessKey
```

⚠️ AWS shows SecretAccessKey only once.

Store it safely.

---

# 13. Switch AWS CLI User

AWS CLI works using Access Key + Secret Key.

You can temporarily switch users using environment variables.

## Linux/Mac

```
exportAWS_ACCESS_KEY_ID=<ACCESS_KEY>
exportAWS_SECRET_ACCESS_KEY=<SECRET_KEY>
```

Verify:

```
aws sts get-caller-identity
```

---

## Remove Temporary Credentials