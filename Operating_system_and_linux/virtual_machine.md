## What is a Virtual Machine?

A **Virtual Machine (VM)** is a **software-based computer** that runs **inside a physical computer**.

- It allows us to **run multiple operating systems on one device**
- Each VM behaves like a **real computer**
- VM has its own:
    - OS
    - CPU
    - RAM
    - Storage

---

## Why do we use Virtual Machines?

- To run **different OS on the same device**
- To test software safely
- To isolate systems from each other

Examples:

- Windows → Linux
- Linux → Windows
- macOS → Linux
- Even Windows → Windows

👉 Any combination is possible.

---

## How is this achieved?

This is done using a **Hypervisor**.

---

## What is a Hypervisor?

A **Hypervisor** is a **virtualization layer** (software or system) that:

- Allows multiple virtual OS to run on one physical machine
- Manages hardware resources for virtual machines

👉 Virtualization is the **technique**,

👉 Hypervisor is the **tool** that does it.

---

## Example Hypervisor

- **VirtualBox** (widely used)

---

## How Virtual Machine Works (Simple Flow)

1. Hypervisor runs on the host system
2. It takes hardware resources from the **host OS**
3. It creates **virtual hardware**:
    - Virtual CPU
    - Virtual RAM
    - Virtual storage
4. Guest OS is installed on this virtual hardware

---

## Resource Rules (Important)

- You can **only assign resources that you actually have**
- Example:
    - Total RAM: 8 GB
    - Host OS uses: 4 GB
    - VM1 uses: 4 GB
    - ❌ No RAM left for another VM

👉 Hypervisor cannot create extra resources.

---

## Multiple Virtual Machines

- You can run **many VMs on one device**
- Each VM is:
    - Completely **isolated**
    - Independent of others

If one VM crashes:

- Other VMs
- Host OS
    
    👉 are **not affected**
    

---

## VM Isolation (Key Point)

- VMs **do not know they are virtual**
- Each VM thinks it is running on a **real computer**
- Isolation improves:
    - Security
    - Stability
    - Testing safety

---

## Types of Hypervisors

---

## 1️⃣ Type 2 Hypervisor (Hosted)

- Runs **on top of an existing OS**
- Installed like a normal application

### Structure:

```
Hardware
↓
Host OS
↓
Hypervisor
↓
Guest OS (VM)
```

### Example:

- VirtualBox on Windows or Linux

---

## 2️⃣ Type 1 Hypervisor (Bare Metal)

- Runs **directly on hardware**
- No host OS in between
- Full control over hardware

### Structure:

```
Hardware
↓
Hypervisor
↓
Guest OS (VMs)
```

👉 Faster and more efficient than Type 2

👉 Mostly used in servers and data centers:wq

