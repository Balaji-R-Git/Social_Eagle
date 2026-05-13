import random


def display_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")


def available_moves(board):
    return [i for i, spot in enumerate(board) if spot == " "]


def check_winner(board):
    winning_lines = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]
    for a, b, c in winning_lines:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    return None


def is_draw(board):
    return " " not in board and check_winner(board) is None


def human_move(player, board):
    while True:
        move = input(f"Player {player}, enter a move (1-9): ").strip()
        if move.isdigit():
            index = int(move) - 1
            if index in available_moves(board):
                return index
        print("Invalid move. Choose an empty position from 1 to 9.")


def random_ai_move(board):
    return random.choice(available_moves(board))


def play_turn(player, board, ai_enabled):
    if ai_enabled:
        move = random_ai_move(board)
        print(f"Computer ({player}) chooses position {move + 1}.")
    else:
        move = human_move(player, board)
    board[move] = player


def play_game(mode="human"):
    board = [" "] * 9
    current_player = "X"

    print("Tic Tac Toe\nPositions are numbered 1 through 9 as follows:")
    display_board([str(i + 1) for i in range(9)])

    while True:
        display_board(board)
        ai_enabled = mode == "auto" or (mode == "computer" and current_player == "O")
        play_turn(current_player, board, ai_enabled)

        winner = check_winner(board)
        if winner:
            display_board(board)
            print(f"Player {winner} wins!")
            break

        if is_draw(board):
            display_board(board)
            print("The game is a draw.")
            break

        current_player = "O" if current_player == "X" else "X"


def choose_mode():
    print("Choose game mode:")
    print("1 - Human vs Human")
    print("2 - Human vs Computer")
    print("3 - Computer vs Computer")

    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in {"1", "2", "3"}:
            return choice
        print("Invalid selection. Try again.")


def main():
    selection = choose_mode()
    if selection == "1":
        play_game(mode="human")
    elif selection == "2":
        play_game(mode="computer")
    else:
        print("Computer vs Computer simulation starting...")
        play_game(mode="auto")


if __name__ == "__main__":
    main()
