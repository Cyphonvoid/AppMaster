from ApplicationUI import *
from Games import BaseGameBoard as bg
from PIL import Image
import random
import customtkinter
import time

GRID_SIZE = 3
difficulty1 = "Random"
difficulty2 = "Best Move Only"

X_SYMBOL = "X"
O_SYMBOL = "O"

# Mediator class for communication between board and right-panel
class TicTacToe:
    def __init__(self, parent):
        self.game_over = False
        self.winner = None

        self.TicTacToeGameBoard = TicTacToeGameBoard(parent=parent,
                                                     game_control=self,
                                                     padx=10,
                                                     pady=10,
                                                     row=0,
                                                     column=1,
                                                     sticky="nsew",
                                                     rowspan=4,
                                                     columnspan=2)

        self.TicTacToeRightPanel = TTTRightPanel(parent=parent,
                                                 game_control=self,
                                                 padx=10,
                                                 pady=10,
                                                 row=0,
                                                 column=4,
                                                 sticky="nsew",
                                                 rowspan=4)

    def start(self):
        self.TicTacToeGameBoard.enable()
        self.TicTacToeRightPanel.enable()


    def start_game(self, player_starts_first):
        if not player_starts_first: self.TicTacToeGameBoard.computer_move()
        self.TicTacToeGameBoard.game_board.flip_state(True)


    def restart_game(self):
        self.set_winner(None)
        self.TicTacToeGameBoard.reset()


    def update_play_order(self, first_turn, difficulty):
        self.TicTacToeGameBoard.set_variables(difficulty=difficulty, first_turn=first_turn)


    def leave_game(self):
        self.restart_game()
        self.TicTacToeRightPanel.disable()
        self.TicTacToeGameBoard.disable()


    def get_winner(self):
        return self.winner


    def set_winner(self, winner):
        self.winner = winner


    def handle_command(self, command):
        if command == "post_game":
            self.TicTacToeRightPanel.handle_command("post_game")


# Superset object of base-game-board which has specific functionality
# Note: BaseGameBoard can be inherited or not inherited, the difference both between is minimal
class TicTacToeGameBoard:
    def __init__(self, parent, game_control, **grid_arguments):
        # Setting up main frame to hold all widgets
        self.main_frame = customtkinter.CTkFrame(parent, **TTT_BOARD_BACKGROUND_LAYOUT)
        self.main_frame.grid(**grid_arguments)
        self.original_grid_arguments = {**grid_arguments}

        # Superset class control (For communication purposes)
        self.game_control = game_control

        # Game logic
        self.game_logic = TicTacToeLogic()
        self.difficulty = ""
        self.first_turn = ""
        self.current_turn = ""
        self.game_over = False
        self.symbols = {
            "X": Image.open("Apps/TicTacToe/Assets/X.png"),
            "O": Image.open("Apps/TicTacToe/Assets/O.png")
        }

        # Game board object
        self.game_board = bg.BaseGameBoard(self.main_frame, grid_size_num=GRID_SIZE, background="black", side="left", padx=20, pady=20)

        # Updating allowed symbols of base game board
        for symbol, image_path in self.symbols.items():
            self.game_board.update_symbol(symbol, image_path)

        # Adjust mouse clicking event
        self.game_board.get_game_canvas().bind("<Button-1>", self.on_click)

    # Left-mouse-button click event for board
    def on_click(self, event):
        # If board is not ready
        if not self.game_board.get_state(): return

        # Process event information
        x = event.x
        y = event.y
        grid_x = x // self.game_board.box_width
        grid_y = y // self.game_board.box_height

        # Ready for next turn, symbol will not insert in incorrect location
        if (grid_x, grid_y) not in self.game_board.existing_symbol_locations:
            self.game_board.insert_symbol(grid_x, grid_y, symbol=self.current_turn)

            # Turn off board to not let player put symbols during computer's turn
            self.game_board.flip_state(False)

            # Update game logic backend
            self.game_logic.update_game_board(grid_x, grid_y, self.current_turn)

            # Check state of game
            self.check_game_status(self.current_turn)
            if not self.game_over:
                # Update game information
                self.update_current_turn()
                self.game_board.canvas.after(500, self.computer_move)


    # Check if there is a winner or a tie
    def check_game_status(self, current_player):
        if self.game_logic.check_win():
            self.game_over = True
            self.game_board.flip_state(False)
            self.game_control.set_winner(current_player)
            self.end_game()
            print("[Notification - Game] Winner of Tic-Tac-Toe: ", current_player)

        elif self.game_logic.check_tie():
            self.game_over = True
            self.game_board.flip_state(False)
            self.end_game()
            print("[Notification - Game] Tic-Tac-Toe game tied! ")


    # Set up necessary game information to start game
    def set_variables(self, difficulty, first_turn):
        self.first_turn = first_turn
        self.current_turn = first_turn
        self.difficulty = difficulty


    def update_current_turn(self):
        if self.current_turn == "X":
            self.current_turn = "O"
        else:
            self.current_turn = "X"


    def computer_move(self):
        x = -1
        y = -1

        # COMPUTER'S MOVE HAS 3 DIFFICULTY RATINGS
        if self.difficulty == difficulty1:
            if len(self.game_board.existing_symbols) >= GRID_SIZE * GRID_SIZE:
                return
            while True:
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                if (x, y) not in self.game_board.existing_symbol_locations:
                    break

        elif self.difficulty == difficulty2:
            best_move = self.find_best_move(self.game_logic.get_game_board())
            if best_move is not None:
                x, y = best_move
                print("Best move coordinates: (", x, ",", y, ")")
            else:
                print("No valid move found.")

        self.game_board.insert_symbol(x, y, symbol=self.current_turn)
        self.game_logic.update_game_board(x, y, self.current_turn)
        self.check_game_status(self.current_turn)

        if not self.game_over:
            self.game_board.flip_state(True)
            self.update_current_turn()



    def evaluate_board(self, board):
        # Checking rows, columns, and diagonals for a win or loss
        for i in range(3):
            if board[0][i] == board[1][i] == board[2][i]:
                if board[0][i] == 'X':
                    return 1
                elif board[0][i] == 'O':
                    return -1

            if board[i][0] == board[i][1] == board[i][2]:
                if board[i][0] == 'X':
                    return 1
                elif board[i][0] == 'O':
                    return -1

        if board[0][0] == board[1][1] == board[2][2]:
            if board[0][0] == 'X':
                return 1
            elif board[0][0] == 'O':
                return -1

        if board[2][0] == board[1][1] == board[0][2]:
            if board[2][0] == 'X':
                return 1
            elif board[2][0] == 'O':
                return -1

        # If no winner, the game is a draw
        return 0


    def minimax(self, board, depth, is_maximizing):
        scores = {
            1: 10,
            -1: -10,
            0: 0
        }

        if depth == 0 or self.evaluate_board(board) != 0:
            return scores[self.evaluate_board(board)]

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '.':
                        board[i][j] = 'X'
                        score = self.minimax(board, depth - 1, False)
                        board[i][j] = '.'
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '.':
                        board[i][j] = 'O'
                        score = self.minimax(board, depth - 1, True)
                        board[i][j] = '.'
                        best_score = min(best_score, score)
            return best_score


    def find_best_move(self, board):
        best_move = None
        best_score = float('-inf')

        for i in range(3):
            for j in range(3):
                if board[i][j] == '.':
                    board[i][j] = 'X'
                    score = self.minimax(board, 9, False)
                    board[i][j] = '.'
                    if score > best_score:
                        best_score = score
                        best_move = (j, i)

        return best_move


    def end_game(self):
        self.game_control.handle_command("post_game")


    def enable(self):
        self.main_frame.grid(**self.original_grid_arguments)


    def disable(self):
        self.main_frame.grid_forget()


    def reset(self):
        self.game_board.flip_state(False)
        self.current_turn = ""
        self.first_turn = ""
        self.game_over = False
        self.difficulty = ""
        self.game_board.reset_board()
        self.game_logic.reset_game()


# Game information panel, very buggy and messy at the moment, but is perfectly functional
class TTTRightPanel:
    def __init__(self, parent, game_control, **grid_arguments):
        self.original_grid_arguments = grid_arguments
        self.parent = parent
        self.game_control = game_control

        # Pre-game variables
        self.game_wins = 1000
        self.game_losses = 10000
        self.game_ties = 10230
        self.computer_name = customtkinter.StringVar(value="Computer")
        self.first_turn = X_SYMBOL
        self.second_turn = O_SYMBOL

        # Game variables
        self.current_turn = customtkinter.StringVar()
        self.player_symbol = customtkinter.StringVar()
        self.computer_symbol = customtkinter.StringVar()
        self.game_outcome = customtkinter.StringVar()
        self.selected_difficulty = customtkinter.StringVar()
        self.player_starts_first = customtkinter.StringVar()

        # Right-side panel
        self.right_panel = customtkinter.CTkFrame(parent, **TTT_RIGHT_PANEL_LAYOUT)
        self.right_panel.grid(**grid_arguments)
        self.right_panel.grid_propagate(False)
        self.right_panel.pack_propagate(False)

    def trigger_event(self, state=None):
        if state == "setup":
            self.setup()
        elif state == "game":
            self.game()
        elif state == "post":
            self.post_game()
        else:
            print("Invalid game state, will not trigger", state)


    def setup(self):
        self.clear_panel_widgets()
        # Tic-Tac-Toe
        game_title = customtkinter.CTkLabel(self.right_panel, text="Tic-Tac-Toe", text_color=SECONDARY_TEXT_COLOR, font=("arial", 22))
        game_title.pack(pady=20)

        # Wins:
        wins_frame = customtkinter.CTkFrame(self.right_panel, fg_color="transparent")
        wins_text = customtkinter.CTkLabel(wins_frame, text="WINS", font=("arial", 17))
        wins_number = customtkinter.CTkLabel(wins_frame, text="213", text_color=SECONDARY_TEXT_COLOR, font=("arial bold", 17))

        wins_frame.pack()
        wins_text.pack(**COMMON_PADDING)
        wins_number.pack()

        # Losses:
        losses_frame = customtkinter.CTkFrame(self.right_panel, fg_color="transparent")
        losses_text = customtkinter.CTkLabel(losses_frame, text="LOSSES", font=("arial", 17))
        losses_number = customtkinter.CTkLabel(losses_frame, text="23", text_color=SECONDARY_TEXT_COLOR, font=("arial bold", 17))

        losses_frame.pack()
        losses_text.pack(**COMMON_PADDING)
        losses_number.pack()

        # Ties:
        ties_frame = customtkinter.CTkFrame(self.right_panel, fg_color="transparent")
        ties_text = customtkinter.CTkLabel(ties_frame, text="TIES", font=("arial", 17))
        ties_number = customtkinter.CTkLabel(ties_frame, text="512", text_color=SECONDARY_TEXT_COLOR, font=("arial bold", 17))

        ties_frame.pack()
        ties_text.pack(**COMMON_PADDING)
        ties_number.pack()

        # Difficulty
        game_difficulty = customtkinter.CTkLabel(self.right_panel, text="Choose Difficulty", text_color=SECONDARY_TEXT_COLOR, font=("arial", 22))
        game_difficulty.pack(pady=(30, 10))

        text1 = customtkinter.CTkRadioButton(master=self.right_panel,
                                             variable=self.selected_difficulty,
                                             value=difficulty1,
                                             fg_color=LOGIN_SECONDARY_COLOR,
                                             hover=False,
                                             border_color=LOGIN_SECONDARY_COLOR,
                                             text=f" {difficulty1}",
                                             font=("arial", 16))
        text1.select()
        text2 = customtkinter.CTkRadioButton(master=self.right_panel,
                                             variable=self.selected_difficulty,
                                             value=difficulty2,
                                             fg_color=LOGIN_SECONDARY_COLOR,
                                             hover=False,
                                             border_color=LOGIN_SECONDARY_COLOR,
                                             text=f" {difficulty2}",
                                             font=("arial", 16))


        text1.pack(padx=(40, 10), pady=10, anchor="w")
        text2.pack(padx=(40, 10), pady=10, anchor="w")

        # Play order
        game_difficulty = customtkinter.CTkLabel(self.right_panel,
                                                 text="Play First?",
                                                 text_color=SECONDARY_TEXT_COLOR,
                                                 font=("arial", 22))
        game_difficulty.pack(pady=(30, 10))

        play_order_switch = customtkinter.CTkSwitch(master=self.right_panel,
                                                    progress_color=SECONDARY_TEXT_COLOR,
                                                    variable=self.player_starts_first,
                                                    text="YES",
                                                    font=("arial", 16),
                                                    onvalue="True",
                                                    offvalue="False")
        play_order_switch.pack()

        add_button_via_pack(self.right_panel,
                            text="Leave",
                            font=(BUTTON_FONT, 16),
                            hover_color="grey",
                            fg_color="transparent",
                            side="bottom",
                            **COMMON_PADDING,
                            command=self.exit_game)
        add_button_via_pack(self.right_panel,
                            text="Start Game",
                            **GENERIC_BUTTON_LAYOUT,
                            command=self.game,
                            side="bottom",
                            pady=(5, 15))


    def game(self):
        self.clear_panel_widgets()
        current_turn_label = customtkinter.CTkLabel(self.right_panel, text="TIC-TAC-TOE", font=("arial", 22), text_color=SECONDARY_TEXT_COLOR)
        current_turn_label.pack(pady=20)

        player_symbol_frame = customtkinter.CTkFrame(self.right_panel, fg_color="transparent")
        player_symbol_frame.pack(**COMMON_PADDING, fill="x")
        player_symbol_text = customtkinter.CTkLabel(player_symbol_frame, text="Player", font=(BUTTON_FONT, 16), text_color=SECONDARY_TEXT_COLOR)
        player_symbol_text.pack(side="left", padx=(20, 5), pady=5)
        player_symbol_img = customtkinter.CTkLabel(player_symbol_frame, text="", textvariable=self.player_symbol, font=("arial", 35))
        player_symbol_img.pack(side="right", padx=(5, 20), pady=5)

        computer_symbol_frame = customtkinter.CTkFrame(self.right_panel, fg_color="transparent")
        computer_symbol_frame.pack(**COMMON_PADDING, fill="x")
        computer_symbol_text = customtkinter.CTkLabel(computer_symbol_frame,
                                                      text="Computer",
                                                      font=(BUTTON_FONT, 16),
                                                      text_color=SECONDARY_TEXT_COLOR)

        computer_symbol_text.pack(side="left", padx=(20, 5), pady=5)
        computer_symbol_img = customtkinter.CTkLabel(computer_symbol_frame, text="", textvariable=self.computer_symbol, font=("arial", 35))
        computer_symbol_img.pack(side="right", padx=(5, 20), pady=5)

        # Note: Create bottom box
        bottom_frame = customtkinter.CTkFrame(self.right_panel, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", pady=5, padx=5)

        # Right-side panel buttons
        add_button_via_pack(bottom_frame,
                            text="Leave",
                            font=(BUTTON_FONT, 16),
                            hover_color="grey",
                            fg_color="transparent",
                            side="bottom",
                            **COMMON_PADDING,
                            command=self.exit_game)

        add_button_via_pack(bottom_frame,
                            text="New Game",
                            font=(BUTTON_FONT, 16),
                            hover_color="grey",
                            fg_color="transparent",
                            side="bottom",
                            **COMMON_PADDING,
                            command=self.play_again)

        self.game_control.update_play_order(first_turn=self.first_turn, difficulty=self.selected_difficulty.get())
        self.game_control.start_game(bool(self.player_starts_first.get()))

        # Setting up frontend player symbols (Who plays what)
        if bool(self.player_starts_first.get()):
            self.player_symbol.set(self.first_turn)
            self.computer_symbol.set(self.second_turn)
        else:
            self.player_symbol.set(self.second_turn)
            self.computer_symbol.set(self.first_turn)

    def post_game(self):
        self.clear_panel_widgets()

        # Game-outcome
        if self.player_symbol.get() == self.game_control.get_winner():
            game_outcome_label = customtkinter.CTkLabel(self.right_panel,
                                                        text="You Won!",
                                                        font=("arial", 22),
                                                        text_color=SECONDARY_TEXT_COLOR)
        elif self.game_control.get_winner() is not None:
            game_outcome_label = customtkinter.CTkLabel(self.right_panel,
                                                        text="You Lost!",
                                                        font=("arial", 22),
                                                        text_color=SECONDARY_TEXT_COLOR)
        else:
            game_outcome_label = customtkinter.CTkLabel(self.right_panel,
                                                        text="You Tied!",
                                                        font=("arial", 22),
                                                        text_color=SECONDARY_TEXT_COLOR)

        game_outcome_label.pack(pady=(50, 40))

        difficulty = customtkinter.CTkLabel(self.right_panel, text="Difficulty", font=("arial", 20))
        difficulty_type = customtkinter.CTkLabel(self.right_panel,
                                                 textvariable=self.selected_difficulty,
                                                 text_color=SECONDARY_TEXT_COLOR,
                                                 font=("arial bold", 17))
        difficulty.pack(**COMMON_PADDING)
        difficulty_type.pack(**COMMON_PADDING)

        add_button_via_pack(self.right_panel,
                            text="Play Again",
                            font=(BUTTON_FONT, 16),
                            hover_color="grey",
                            fg_color="transparent",
                            pady=(40, 5),
                            command=self.play_again)

        add_button_via_pack(self.right_panel,
                            text="Leave",
                            font=(BUTTON_FONT, 16),
                            hover_color="grey",
                            fg_color="transparent",
                            **COMMON_PADDING,
                            command=self.exit_game)

    def clear_panel_widgets(self):
        for widget in self.right_panel.winfo_children():
            widget.pack_forget()


    def enable(self):
        self.trigger_event("setup")
        self.right_panel.grid(**self.original_grid_arguments)


    def play_again(self):
        self.player_symbol.set("")
        self.computer_symbol.set("")
        self.player_starts_first.set("")
        self.game_control.restart_game()
        self.trigger_event("setup")


    def exit_game(self):
        self.game_control.restart_game()
        self.game_control.leave_game()
        self.disable()


    def disable(self):
        self.right_panel.grid_forget()


    def handle_command(self, message):
        if message == "post_game":
            self.trigger_event("post")


# Backend logic
# Note: Hardcoded only for 3x3, change to dynamic checking in future
class TicTacToeLogic:
    def __init__(self):
        self.current_game = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.number_of_symbols = 0
        self.allowed_symbols = ["X", "O"]
        self.MAX_NUMBER_SYMBOLS = GRID_SIZE * GRID_SIZE

#



    def reset_game(self):
        self.number_of_symbols = 0
        self.current_game = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


    def check_tie(self) -> bool:
        return self.number_of_symbols >= self.MAX_NUMBER_SYMBOLS


    def check_win(self) -> bool:
        return self.check_diagonal() or self.check_vertical() or self.check_horizontal()


    def check_horizontal(self) -> bool:
        for row in range(GRID_SIZE):
            if self.current_game[row][0] == self.current_game[row][1] and self.current_game[row][1] == self.current_game[row][2]:
                if "." not in self.current_game[row]:
                    return True
        return False


    def check_vertical(self) -> bool:
        for column in range(GRID_SIZE):
            if self.current_game[0][column] == self.current_game[1][column] and self.current_game[1][column] == self.current_game[2][column] and self.current_game[0][column] != ".":
                return True
        return False


    def check_diagonal(self) -> bool:
        if self.current_game[0][0] == self.current_game[1][1] and self.current_game[1][1] == self.current_game[2][2] and self.current_game[0][0] != ".":
            return True
        if self.current_game[2][0] == self.current_game[1][1] and self.current_game[1][1] == self.current_game[0][2] and self.current_game[2][0] != ".":
            return True
        return False


    def print_board_console(self):
        for row in self.current_game:
            print(" ".join(row))


    def get_game_board(self):
        return self.current_game


    def update_game_board(self, x_index, y_index, symbol):
        if self.number_of_symbols >= GRID_SIZE * GRID_SIZE:
            print("You have the maximum number of symbols:", self.number_of_symbols)
            return

        if self.current_game[y_index][x_index] != ".":
            print(f"Symbol already exists! X:{x_index} Y:{y_index}")
            return

        if symbol not in self.allowed_symbols:
            print("Invalid symbol: ", symbol)
            return

        self.current_game[y_index][x_index] = symbol
        self.number_of_symbols += 1


def launch(parent):
    game = TicTacToe(parent)
    game.start()