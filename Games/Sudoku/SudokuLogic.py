import requests
import copy

class SudokuLogic():
    def __init__(self, game):
        self.unsolved_board = None
        self.untouched_board = None
        self.solved_board = None
        self.spots_left = 0
        self.game = game
        self.EMPTY_SPACE = "."

        """
        Difficulties:
        1 - easy
        2 - medium
        3 - hard
        4 - very-hard
        5 - insane
        6 - inhuman
        """

        self.difficulties = {
            1: "hard",
            2: "very-hard",
            3: "insane"
        }

    def check_if_original_spot(self, grid_x, grid_y):
        symbol_at_location = self.untouched_board[grid_x][grid_y]
        if symbol_at_location == self.EMPTY_SPACE:
            return False
        else: return True

    def receive_api_board(self, difficulty):
        """
                NOTE: 200 REQUESTS PER DAY ONLY
                COST: $0.01 per request after free use
                :return: [[]] UNSOLVED SUDOKU BOARD
                """
        url = "https://sudoku-generator3.p.rapidapi.com/generate"

        if isinstance(difficulty, str):
            selected_difficulty = difficulty
        else:
            selected_difficulty = str(self.difficulties[difficulty])

        # Set up data requirements
        payload = {
            "difficulty": selected_difficulty,
            "spaces": ".",
            "candidates": False,
            "list": False,
            "grid": True
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "98722f7491msh45103732a9a50d6p1e9937jsn4782f73731c2",
            "X-RapidAPI-Host": "sudoku-generator3.p.rapidapi.com"
        }

        # Send request to API
        try:
            response = requests.post(url, json=payload, headers=headers)
        except:
            #back-up board if host is offline, make a json file system for this later
            return [['3', '1', '7', '5', '4', '8', '6', '2', '9'],
                    ['4', '9', '2', '6', '.', '.', '8', '.', '5'],
                    ['.', '.', '8', '2', '.', '9', '.', '.', '.'],
                    ['.', '.', '.', '7', '8', '2', '.', '9', '.'],
                    ['8', '2', '.', '3', '.', '4', '5', '7', '.'],
                    ['.', '.', '.', '1', '.', '5', '.', '8', '.'],
                    ['9', '.', '.', '8', '5', '.', '.', '.', '.'],
                    ['.', '8', '.', '9', '2', '.', '.', '6', '3'],
                    ['2', '.', '.', '4', '.', '.', '9', '5', '8']]

        # Return unsolved board from API response
        # print(response.json()["grid"])
        return response.json()["grid"]

    def get_spots_left(self):
        return self.spots_left

    def increment_spots_left(self):
        self.spots_left += 1

    def decrement_spots_left(self):
        self.spots_left -= 1

    def reset_spots_left(self):
        self.spots_left = 0

    def get_board(self, difficulty=None):
        if difficulty is None:
            self.unsolved_board = self.receive_api_board(difficulty=1)
        else:
            self.unsolved_board = self.receive_api_board(difficulty=difficulty)

        self.untouched_board = copy.deepcopy(self.unsolved_board)
        self.solved_board = self.solve_board(copy.deepcopy(self.unsolved_board))

        return self.unsolved_board

    def is_valid(self, board, row, col, num):
        # Check if 'num' is not in the current row, column, and 3x3 grid
        for i in range(9):
            if board[row][i] == str(num) or board[i][col] == str(num) or board[row // 3 * 3 + i // 3][col // 3 * 3 + i % 3] == str(num):
                return False
        return True

    def solve_sudoku(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == ".":  # Find an empty cell
                    for num in range(1, 10):  # Try placing numbers 1 to 9
                        if self.is_valid(board, row, col, num):
                            board[row][col] = str(num)  # Place the number if valid
                            if self.solve_sudoku(board):  # Recurse with the updated board
                                return True
                            board[row][col] = "."  # Backtrack if the solution is not valid
                    return False  # No valid number found, need to backtrack
        return True  # All cells filled, puzzle solved

    def solve_board(self, board):
        if self.solve_sudoku(board):
            return board
        else:
            print("No solution exists")

    def check_win(self):
        return self.unsolved_board is self.solved_board

    def check_solution(self, grid_x, grid_y):
        if self.unsolved_board[grid_x][grid_y] == self.solved_board[grid_x][grid_y]:
            return True
        return False

    def insert_number(self, grid_x, grid_y, number: str):
        self.unsolved_board[grid_x][grid_y] = number

    def remove_number(self, grid_x, grid_y):
        self.unsolved_board[grid_x][grid_y] = self.EMPTY_SPACE