# Shell Scripting Basics (Linux)

## 1. What is a Shell?

A **Shell** is a program that:

- Interprets the commands we type in the terminal
- Executes those commands
- Communicates with the **Linux Kernel**

### Simple Flow

```
User → Shell → Kernel → Hardware
```

Explanation:

1. User types a command in the terminal.
2. The **shell interprets the command**.
3. The shell sends it to the **kernel**.
4. The **kernel executes the command** using system resources.

So the shell acts as a **bridge between the user and the kernel**.

---

# 2. Types of Shells

There are different implementations of shell in Linux.

Common ones include:

| Shell | Description |
| --- | --- |
| **Bourne Shell (sh)** | Original Unix shell |
| **Bash** | Improved version of sh (most common) |
| **Z Shell** | Advanced interactive shell |
| **C Shell** | C-like syntax shell |

### Bash

- **Bash = Bourne Again Shell**
- Most widely used shell in Linux.
- Used for **shell scripting and automation**.

Bash is:

- a **shell program**
- also a **scripting/programming language**

---

# 3. What is Shell Scripting?

A **shell script** is a file that contains multiple Linux commands written together.

Instead of typing commands one by one, we write them in a script and execute them.

### Benefits

- Automates tasks
- Saves time
- Reduces manual work
- Used heavily in **DevOps and System Administration**

---

# 4. Creating a Shell Script

### Step 1: Create a script file

```
vim script.sh
```

### Step 2: Add shebang

```
#!/bin/bash
```

This tells the system to run the script using **Bash**.

Example script:

```
#!/bin/bash

echo"Hello World"
echo"Welcome to Shell Scripting"
```

---

### Step 3: Make it executable

```
chmod+x script.sh
```

### Step 4: Run the script

```
./script.sh
```

---

# 5. Variables in Shell Script

Variables are used to store data.

### Assigning a Variable

```
name="Narshing"
```

⚠️ Important rule:

There should be **no spaces around `=`**

Correct:

```
name="DevOps"
```

Wrong:

```
name="DevOps"
```

---

### Using Variables

Use `$` before the variable name.

Example:

```
#!/bin/bash

name="Narshing"

echo"My name is$name"
```

Output:

```
My name is Narshing
```

---

# 6. User Input in Shell Script

You can take input from the user using `read`.

Example:

```
#!/bin/bash

echo"Enter your name:"
read name

echo"Hello$name"
```

---

# 7. Conditional Statements (if)

Example:

```
#!/bin/bash

num=10

if [$num-gt5 ]
then
echo"Number is greater than 5"
fi
```

Common comparison operators:

| Operator | Meaning |
| --- | --- |
| -eq | equal |
| -ne | not equal |
| -gt | greater than |
| -lt | less than |
| -ge | greater or equal |
| -le | less or equal |

---

# 8. For Loop

A **for loop** is used when we want to repeat a task multiple times.

### Example 1: Print numbers

```
#!/bin/bash

for iin12345
do
echo$i
done
```

Output:

```
1
2
3
4
5
```

---

### Example 2: Loop through files

```
#!/bin/bash

for filein *.txt
do
echo$file
done
```

This will print all `.txt` files in the directory.

---

# 9. While Loop

A **while loop** runs as long as a condition is true.

### Example: Print numbers

```
#!/bin/bash

count=1

while [$count-le5 ]
do
echo$count
count=$((count+1))
done
```

Output:

```
1
2
3
4
5
```

---

# 10. Arithmetic Operations

Example:

```
#!/bin/bash

a=5
b=3

sum=$((a+b))

echo"Sum is$sum"
```

Output:

```
Sum is 8
```

---

# 11. Comments in Shell Script

Comments are ignored by the shell.

Example:

```
# This is a comment
echo"Hello"
```

Used for:

- explaining code
- documentation

---

# 12. Basic Useful Commands in Scripts

Some commonly used commands:

| Command | Purpose |
| --- | --- |
| `echo` | print output |
| `read` | take input |
| `chmod` | change permissions |
| `grep` | search text |
| `sleep` | pause execution |

Example:

```
echo"Starting script..."
sleep2
echo"Script completed"
```

---

# Summary

Shell scripting helps you:

- Automate Linux tasks
- Manage servers
- Write deployment scripts
- Create monitoring scripts

It is **very important for DevOps and system administrators**.