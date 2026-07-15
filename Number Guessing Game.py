import random
x = random.randint(1,100)
attempt = 0
while True:
    y = int(input("How Many Attempts You Want To Make: "))  
    for attempt in range(1,y+1):
        guess = int(input("Guess A Number From 1 to 100 : "))

        if guess < x:
            print("Too Low! Try Again ")
            print("You have", y - attempt, "Attempts Left")

        elif guess > x:
            print("Too High! Try Again ")
            print("You have", y - attempt, "Attempts Left")
        
        elif guess == x:
            print("You Guessed It Right ")
            print("You have done in ", attempt, "attempts")
            break

        else:
            print("Invalid Input ")
    
    if attempt == y:
        print("You Lose The Number Was ", x)
        break

