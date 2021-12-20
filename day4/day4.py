import numpy as np


def create_game(file):
    with open(file, "r") as f:
        content = f.read()

    x = content.split("\n")

    numbers = np.array(x[0].split(","), dtype=int)

    # initialize variables for creating boards
    all_boards = []
    board = np.zeros((5, 5), dtype=int)
    row_idx = 0

    for i in range(2, len(x)):
        if x[i] == "":
            all_boards.append(board)
            board = np.zeros((5, 5), dtype=int)
            row_idx = 0
        else:
            row = np.array(x[i].split(), dtype=int)
            board[row_idx, :] = row
            row_idx += 1

    return numbers, all_boards


def check_number(number, board, results):
    results[board == number] = 1
    return results


def check_win(results):
    row_sum = np.sum(results, axis=1)
    col_sum = np.sum(results, axis=0)
    if np.sum(row_sum == 5) != 0:
        return True
    elif np.sum(col_sum == 5) != 0:
        return True
    else:
        return False


def get_score(number, board, results):
    score = number * np.sum(board[results == 0])
    return score


def run_game(numbers, all_boards):
    all_results = [np.zeros((5, 5)) for i in range(len(all_boards))]
    winning_boards = np.zeros(len(all_boards))
    for j,number in enumerate(numbers):
        for i, board in enumerate(all_boards):
            if winning_boards[i] == 0:
                all_results[i] = check_number(number, board, all_results[i])
                if check_win(all_results[i]):
                    print(f"Winning board at iteration {j}")
                    print(board)
                    print(f"Winning number: {number}")
                    score = get_score(number, board, all_results[i])
                    print(f"Score is: {score}")
                    winning_boards[i] = 1
                    #all_boards.remove(board)


if __name__ == "__main__":
    numbers, all_boards = create_game("day4_input.txt")
    run_game(numbers, all_boards)
