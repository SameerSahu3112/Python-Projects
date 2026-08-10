def print_board(board):
    print("\n")
    print("     |     |     ")
    print(f"  {board[0]}  |  {board[1]}  |  {board[2]}  ")
    print("_____|_____|_____")
    print("     |     |     ")
    print(f"  {board[3]}  |  {board[4]}  |  {board[5]}  ")
    print("_____|_____|_____")
    print("     |     |     ")
    print(f"  {board[6]}  |  {board[7]}  |  {board[8]}  ")
    print("     |     |     ")
    print("\n")


def check_winner(board, player):
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False


def is_draw(board):
    return " " not in board


print("Welcome to Tic Tac Toe!")
print("Player 1: X  |  Player 2: O")
print("Enter a number 1-9 to place your mark:")
print(" 1 | 2 | 3 ")
print("---+---+---")
print(" 4 | 5 | 6 ")
print("---+---+---")
print(" 7 | 8 | 9 ")

while True:
    board = [" "] * 9
    current_player = "X"

    while True:
        print_board(board)
        position = input(f"Player {1 if current_player == 'X' else 2} ({current_player}), enter position (1-9): ")

        if not position.isdigit() or int(position) < 1 or int(position) > 9:
            print("Invalid Input! Enter a number from 1 to 9.")
            continue

        index = int(position) - 1

        if board[index] != " ":
            print("That spot is already taken! Choose another.")
            continue

        board[index] = current_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {1 if current_player == 'X' else 2} ({current_player}) Wins!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a Draw!")
            break

        current_player = "O" if current_player == "X" else "X"

    play_again = input("Play again? (yes/no): ").strip().lower()
    if play_again != "yes":
        print("Thanks for playing!")
        break
