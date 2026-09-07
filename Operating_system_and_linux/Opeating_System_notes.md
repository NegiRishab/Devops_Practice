## What is an Operating System?

An **Operating System (OS)** is a **layer between hardware and applications**.

- It **interacts directly with hardware**
- It **acts as a translator** between:
    - **Applications** (Chrome, Safari, etc.)
    - **Hardware** (CPU, RAM, storage, mouse, keyboard)
    

👉 Applications never talk to hardware directly.

👉 They ask the OS, and the OS handles it.

---

## What does the OS do?

### 1. Resource Management

The OS **shares system resources** among applications.

Example:

- Chrome uses 70% CPU
- You switch to Safari
- OS quickly shifts resources to Safari
- User does **not notice** the change

---

### 2. Application Isolation

- Each application has its **own execution environment**
- One app **cannot access another app’s data or memory**
- Prevents crashes and security issues

---

## Main Tasks of an Operating System

---

## 1️⃣ CPU Management (Process Management)

### What is a Process?

A **process** is any active task:

- Opening Chrome
- Closing an app
- Clicking a button

### Key Points

- Each process has **its own isolated space**
- A **single CPU runs one process at a time**
- OS switches between processes **very fast**
- Switching is so fast that users don’t notice it

---

## 2️⃣ Memory Management (RAM)

### What is RAM?

- **RAM (Random Access Memory)** is limited
- Applications need RAM to run

### What OS does:

- Gives RAM to active applications
- Takes RAM from inactive applications

---

### Memory Swapping (Important)

When RAM is full:

1. Inactive process memory is moved from **RAM → storage**
2. Active process memory is moved from **storage → RAM**
3. This operation **takes time**
4. App may feel slow during swap

---

## RAM and Storage – How They Work Together

### Timeline (Easy to Recall)

### 1️⃣ Before opening Chrome

- Chrome exists **only in storage**
- RAM has no Chrome data

---

### 2️⃣ Opening Chrome

OS does this:

- Reads Chrome program from storage
- Copies required parts into RAM
- Creates a process

✅ Chrome is now in RAM

---

### 3️⃣ Chrome running normally

- CPU reads instructions from **RAM**
- Chrome tabs and data are in RAM
- ❌ No storage access needed
- App runs fast

---

### 4️⃣ Chrome becomes inactive

Two cases:

**Case A: Enough RAM**

- Chrome stays in RAM
- Instant resume

**Case B: RAM pressure**

- OS moves Chrome memory to storage (swap)
- Chrome removed from RAM

---

### 5️⃣ Returning to Chrome (swap case)

- OS copies memory from storage → RAM
- Takes time
- App feels slow briefly

👉 Swapping happens **only when needed**

---

### Important Rule

**CPU communicates only with RAM**, not directly with storage.

---

## 3️⃣ Storage Management (File System)

- OS manages how data is stored on disk
- Data is stored in a **structured way**
- In UNIX/Linux:
    - Tree-like file system

---

## 4️⃣ I/O Device Management

OS handles input/output devices:

- Mouse
- Keyboard
- Printer
- Other devices

OS translates actions between:

- Applications
- Hardware devices

---

## 5️⃣ Security and Networking

### Security

- User accounts
- Permissions
- Each user has:
    - Own space
    - Defined access rights

### Networking

- IP addresses
- Ports
- Network resource management

---

## How is an Operating System Constructed?

---

## Kernel (Core of OS)

### What is the Kernel?

- Kernel is the **first part to load**
- It is the **heart of the operating system**
- Kernel is a **program**

### What Kernel Does

- Manages CPU, RAM, and storage
- Handles I/O devices using device drivers
- Starts application processes
- Allocates resources to apps
- Cleans resources when apps close

👉 Kernel is the **only layer that directly talks to hardware**

---

## OS Layers

- **Kernel layer** (core)
- **Application layer** (user programs)

Kernel can be different for different OS.

---

## Linux Kernel

- Many OS use the **same Linux kernel**
- Different application layers create different distributions:
    - Ubuntu
    - Mint
    - CentOS

👉 Same kernel, different OS experience

---

## Android

- Based on **Linux kernel**
- Used in mobile devices

---

## macOS & iOS

- Based on **Darwin kernel**
