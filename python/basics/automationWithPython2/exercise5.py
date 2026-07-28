calcutaion=0

while True:
    if calcutaion>0:
        print(f"{calcutaion +1} calculation is ongoing")
    first = input("First number (or 'exit'): ")

    if first.lower() == "exit":
        print("Calculator closed.")
        break

    second = input("Second number: ")
    operator = input("Operator (+, -, *, /): ")

    first = float(first)
    second = float(second)

    if operator == "+":
        print("Result:", first + second)
    elif operator == "-":
        print("Result:", first - second)
    elif operator == "*":
        print("Result:", first * second)
    elif operator == "/":
        if second == 0:
            print("Cannot divide by zero.")
        else:
            print("Result:", first / second)
    else:
        print("Invalid operator.")

    calcutaion= calcutaion +1

    print()  # blank line