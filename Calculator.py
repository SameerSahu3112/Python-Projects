while True:
    try:
        a = int(input("Enter A Number: "))
        b = int(input("Enter Another Number: "))
        c = input("Enter The operation you want to perform (+, -, *, /) and 1 for exit:)")

        if c == "+":
            print(a+b)
        elif c == "-":
            print(a-b)
        elif c == "*":
            print(a*b)
        elif c == "/":
            print(a/b)
        elif c == "1":
            break
        else:
            print("Invalid operation")

    except:
        print("Please Enter Number")
