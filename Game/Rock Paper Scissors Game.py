import random
draw = 0
win = 0
lose = 0


print("Welcome to Rock Paper Scissors Game Where you will play 5 rounds with the computer and the one who wins the most rounds wins!")
while True:
    for i in range(1,6):
        user  = int(input("Enter you choice: 1 for Rock and 2 for Paper and 3 For Scissors: "))
        choices = ["Rock", "Paper", "Scissors"]
        computer = random.choice(choices)

        def user_choice(user):
            if user == 1:
                user = "Rock"
            elif user == 2:
                user = "Paper"
            elif user == 3:
                user = "Scissors"
            return user

        if (user == 1 and computer == "Rock") or (user == 2 and computer == "Paper") or (user == 3 and computer == "Scissors"):
            print("Draw")
            print("Computer Chose: ", computer)
            print("You Choose: ", user_choice(user))
            print("Your left Attempts: ", 5-i)
            draw += 1
        elif (user == 1 and computer == "Paper") or (user == 2 and computer == "Scissors") or (user == 3 and computer == "Rock"):
            print("You Lose")
            print("Computer Chose: ", computer)
            print("You Choose: ", user_choice(user))
            print("Your left Attempts: ", 5-i)
            lose += 1
        elif (user == 1 and computer == "Scissors") or (user == 2 and computer == "Rock") or (user == 3 and computer == "Paper"):
            print("You Win")
            print("Computer Chose: ", computer)
            print("You Choose: ", user_choice(user))
            print("Your left Attempts: ", 5-i)
            win += 1
        else:
            print("Invalid Input")
    
    print("Your Score: ", win, "Computer Score: ",lose, "Draws: ", draw)
    break

if win > lose:
    print("You Win The Series")
elif lose > win:
    print("You Lose The Series")
else:
    print("The Series is Draw")
