import Games.BaseGameBoard as bg
from PIL import Image, ImageTk
import copy
import random

from .SudokuStats import *

WINDOW_BACKGROUND_COLOR = "#1E1F22"
PANEL_COLOR = "#292929"
HOVER_COLOR = "#232323"

SUDOKU_GAMEBOARD_LAYOUT = {
    "fg_color": WINDOW_BACKGROUND_COLOR,
    "border_width": 2,
    "corner_radius": 5,
    "border_color": WINDOW_BACKGROUND_COLOR
}

HIGHLIGHT_COLOR = "#c29dc0"
VISUAL_HIGHLIGHT = "#4a2e48"
HIGHLIGHT_TAG = "h"

SUDOKU_BOARD = "sudoku_board"
RIGHT_PANEL = "right_panel"
TOP_PANEL = "top_panel"
GAME_LOGIC = "game_logic"

MISTAKES_ALLOWED = 10

NEW_GAME_LAYOUT = {
    "width": 350,
    "height": 60,
    "fg_color": "#D51989",
    "bg_color": "transparent",
    "font": ("Arial", 18, "bold"),
    "text": "New Game",
    "text_color": "white",
    "corner_radius": 4
}

FIXED_DIFFICULTY = {
    None: "hard",
    "Easy": "hard",
    "Medium": "very-hard",
    "Hard": "insane"
}


class SudokuBoard:
    def __init__(self, parent, game, **arguments):

        self.arguments = arguments
        self.game = game
        self.parent = parent

        self.symbols = {
            "1": Image.open("Games/Sudoku/Assets/1.png"),
            "2": Image.open("Games/Sudoku/Assets/2.png"),
            "3": Image.open("Games/Sudoku/Assets/3.png"),
            "4": Image.open("Games/Sudoku/Assets/4.png"),
            "5": Image.open("Games/Sudoku/Assets/5.png"),
            "6": Image.open("Games/Sudoku/Assets/6.png"),
            "7": Image.open("Games/Sudoku/Assets/7.png"),
            "8": Image.open("Games/Sudoku/Assets/8.png"),
            "9": Image.open("Games/Sudoku/Assets/9.png"),
        }

        self.red_symbols = {
            "10": self.get_red_number(Image.open("Games/Sudoku/Assets/1.png")),
            "11": self.get_red_number(Image.open("Games/Sudoku/Assets/2.png")),
            "12": self.get_red_number(Image.open("Games/Sudoku/Assets/3.png")),
            "13": self.get_red_number(Image.open("Games/Sudoku/Assets/4.png")),
            "14": self.get_red_number(Image.open("Games/Sudoku/Assets/5.png")),
            "15": self.get_red_number(Image.open("Games/Sudoku/Assets/6.png")),
            "16": self.get_red_number(Image.open("Games/Sudoku/Assets/7.png")),
            "17": self.get_red_number(Image.open("Games/Sudoku/Assets/8.png")),
            "18": self.get_red_number(Image.open("Games/Sudoku/Assets/9.png")),
        }

        # Keep track of selected position
        self.selected_location = ()

        # Keep track of user-moves
        self.user_move_locations = {}

        # Frame
        self.game_panel = customtkinter.CTkFrame(parent, **SUDOKU_GAMEBOARD_LAYOUT)
        self.game_panel.grid(**arguments)

        # Used for game ending, this just needs to be stored in class __init__
        self.panel = None

        # Frame to hold game + visualization
        self.board = bg.BaseGameBoard(self.game_panel, grid_size_num=9, background="black", line_thickness=4, gap=3, side="left", padx=20, pady=20)

        self.difficulty = None

        # Holds function pointers, typically used for reversing symbol deletion and insertion
        self.undo_stack = []

        # To updated allowed_symbols
        for symbol, image_path in self.symbols.items():
            self.board.update_symbol(symbol, image_path)

        for symbol, image_path in self.red_symbols.items():
            self.board.update_symbol(symbol, image_path)

        # Adjust mouse-clicking event
        self.board.get_game_canvas().bind("<Button-1>", self.on_click)

        # Number-binding
        parent.parent.bind("<KeyPress>", self.key_pressed)

        # Resizing for highlights (Doesn't work...WTF??)
        #self.game_panel.bind("<Configure>", self.resize_highlights)

    def key_pressed(self, event):
        key_pressed = event.char
        if key_pressed in "123456789":
            self.insert_number(key_pressed)
        if key_pressed == "\x08":
            self.remove_number_at_selected_location()

    def resize_highlights(self):
        self.remove_highlights()
        self.draw_highlights(self.selected_location[0], self.selected_location[1])

    # Display sudoku numbers on board from backend API
    def load_board(self, difficulty=None):
        game_logic = self.game.get_object(GAME_LOGIC)
        unsolved_board = game_logic.get_board(difficulty=FIXED_DIFFICULTY[difficulty])

        self.difficulty = "Easy" if self.difficulty is None else difficulty

        # Inserting every number into frontend board from backend board
        for row, row_values in enumerate(unsolved_board):
            for col, sudoku_number in enumerate(row_values):
                if sudoku_number != game_logic.EMPTY_SPACE:
                    # Insert number here
                    self.board.insert_symbol(row, col, sudoku_number)
                else:
                    # Empty spot, so increment spots_left counter
                    game_logic.increment_spots_left()

    def reset(self):
        self.selected_location = ()
        self.user_move_locations.clear()
        self.undo_stack.clear()
        self.board.reset_board()
        self.game.get_object(TOP_PANEL).timer.stop()
        self.game.get_object(TOP_PANEL).timer.reset()
        self.game.get_object(TOP_PANEL).reset_mistakes()
        self.game.get_object(GAME_LOGIC).reset_spots_left()
        self.remove_highlights()

    def on_click(self, event):
        # Board is not ready for simulation
        if not self.board.get_state():
            return

        # Process event information
        x = event.x
        y = event.y
        grid_x = x // self.board.box_width
        grid_y = y // self.board.box_height

        # Change selected location (Used for number-insertion and highlighting)
        self.selected_location = (grid_x, grid_y)

        # Remove any previous highlights
        self.remove_highlights()

        # Draw highlights based on click-position
        self.draw_highlights(grid_x, grid_y)

    def insert_number(self, number, x=None, y=None):
        if not self.board.get_state():
            return

        if self.selected_location == () and x is None and y is None:
            print("No number selected")
            return

        if not 9 >= int(number) >= 1:
            return

        if x is None:
            x = self.selected_location[0]
            y = self.selected_location[1]
        else:
            x = x
            y = y

        game_logic = self.game.get_object(GAME_LOGIC)

        # Check if user entered a number in a locked spot or an empty space
        if not game_logic.check_if_original_spot(x, y):
            if (x, y) in self.user_move_locations:
                if self.user_move_locations[(x, y)] == str(number):
                    # If user presses the same number, a common human habit is to
                    # delete it after pressing it once
                    self.board.remove_symbol(x, y)
                    game_logic.remove_number(x, y)
                    del self.user_move_locations[(x, y)]
                    return
                else:
                    # Remove number if user inserts a previously entered number in same spot
                    self.board.remove_symbol(x, y)

            # Insert number into logic
            game_logic.insert_number(x, y, str(number))

            # Print out either a red number or a white number depending on correctness
            if game_logic.check_solution(x, y):
                #Print white number
                self.board.insert_symbol(grid_x=x, grid_y=y, symbol=str(number))

                # Check win, we don't increment spots left on red numbers
                game_logic.decrement_spots_left()
                if game_logic.get_spots_left() == 0:
                    self.stop_game()
                    self.display_game_win()
            else:
                #the red number which is 9 spots away from white number inside dictionary
                red_number_index = int(number) + 9
                self.board.insert_symbol(grid_x=x, grid_y=y, symbol=str(red_number_index))
                self.game.get_object(TOP_PANEL).increment_mistake()

                if self.game.get_object(TOP_PANEL).get_mistakes() == MISTAKES_ALLOWED:
                    # Put end game here
                    self.stop_game()
                    self.display_game_loss()

            self.user_move_locations[(x, y)] = str(number)

            # Add opposite of insert number to stack
            self.push_to_stack(lambda:self.remove_number_at_location(x, y))
            #print(*self.undo_stack)

    def remove_number_at_selected_location(self):
        x = self.selected_location[0]
        y = self.selected_location[1]
        game_logic = self.game.get_object(GAME_LOGIC)

        #Remove number in unlocked position (user moves only)
        if (x, y) in self.user_move_locations:
            self.push_to_stack(lambda: self.insert_number(self.user_move_locations[(x, y)], x, y))
            print(*self.undo_stack)
            self.board.remove_symbol(x, y)
            game_logic.remove_number(x, y)

    def stop_game(self):
        self.game.get_object(TOP_PANEL).timer.stop()
        self.board.flip_state(False)
        self.remove_highlights()

    def restart_game_from_end(self):
        self.remove_panel()
        self.reset()

    def leave_game(self):
        self.reset()
        self.game.leave_game()

    def display_game_loss(self):
        self.panel = customtkinter.CTkFrame(self.parent, width=400, height=200,
                                            fg_color=PANEL_COLOR, bg_color="transparent",
                                            border_color=HOVER_COLOR, border_width=2)
        game_over = customtkinter.CTkLabel(self.panel, text="Game Over", font=("Arial", 28))
        game_over.pack(pady=40)
        why_you_lost_frame = customtkinter.CTkFrame(self.panel, fg_color=PANEL_COLOR)
        why_you_lost_part_1 = customtkinter.CTkLabel(why_you_lost_frame, text=f"You have made {MISTAKES_ALLOWED} mistakes and lost", font=("Arial", 23), text_color="grey")
        why_you_lost_part_2 = customtkinter.CTkLabel(why_you_lost_frame, text="this game", font=("Arial", 23), text_color="grey")
        why_you_lost_frame.pack(pady=(0, 60))
        why_you_lost_part_1.pack()
        why_you_lost_part_2.pack()
        new_game = customtkinter.CTkButton(self.panel, **NEW_GAME_LAYOUT)
        new_game.configure(command=self.restart_game_from_end)
        new_game.pack()

        leave_game = customtkinter.CTkButton(self.panel, **NEW_GAME_LAYOUT)
        leave_game.configure(text="Leave", fg_color="transparent", hover_color=PANEL_COLOR, command=self.leave_game)
        leave_game.pack(pady=8)

        self.panel.place(relx=0.5, rely=0.5, relheight=0.6, relwidth=0.6, anchor=customtkinter.CENTER)

    def display_game_win(self):
        time_played = self.game.get_object(TOP_PANEL).timer.get_time()
        #:02d is black magic python one-liner code that formats time to 00:00
        time_played = f"{time_played[0]:02d}:{time_played[1]:02d}"

        self.panel = customtkinter.CTkFrame(self.parent, width=400, height=200,
                                            fg_color=PANEL_COLOR, bg_color="transparent",
                                            border_color=HOVER_COLOR, border_width=2)
        game_over = customtkinter.CTkLabel(self.panel, text="Excellent!", font=("Arial", 28))
        game_over.pack(pady=40)
        game_analysis_frame = customtkinter.CTkFrame(self.panel, fg_color=PANEL_COLOR)
        difficulty = customtkinter.CTkLabel(game_analysis_frame, text=f"Difficulty:\t\t{self.difficulty}", font=("Arial", 23), text_color="grey")
        time_completed = customtkinter.CTkLabel(game_analysis_frame, text=f"Time:\t\t{time_played}", font=("Arial", 23), text_color="grey")
        difficulty.pack(anchor="w", pady=(0,10))
        time_completed.pack(anchor="w")
        game_analysis_frame.pack(pady=(0, 60))
        new_game = customtkinter.CTkButton(self.panel, **NEW_GAME_LAYOUT)
        new_game.configure(command=self.restart_game_from_end)
        new_game.pack()

        leave_game = customtkinter.CTkButton(self.panel, **NEW_GAME_LAYOUT)
        leave_game.configure(text="Leave", fg_color="transparent", hover_color=PANEL_COLOR, command=self.leave_game)
        leave_game.pack(pady=8)

        self.panel.place(relx=0.5, rely=0.5, relheight=0.6, relwidth=0.6, anchor=customtkinter.CENTER)

    def draw_highlights(self, grid_x, grid_y):
        # For multiple highlights of same number if a number selected
        if (grid_x, grid_y) in self.board.existing_symbol_locations:
            number_selected_image = self.board.existing_symbol_locations[(grid_x, grid_y)]

            # Get all the same numbers and add highlighting
            for location, symbol_image in self.board.existing_symbol_locations.items():
                if number_selected_image == symbol_image:
                    # Add highlighting box at number
                    self.set_button_highlight(location[0], location[1], HIGHLIGHT_COLOR)
        else:
            self.set_button_highlight(grid_x, grid_y, HIGHLIGHT_COLOR)


        ###Add visual highlights (rows, columns, and 3x3 box)###
        #Column
        for column_index in range(9):
            self.set_button_highlight(grid_x, column_index, VISUAL_HIGHLIGHT)

        # Row
        for row_index in range(9):
            self.set_button_highlight(row_index, grid_y, VISUAL_HIGHLIGHT)

        # Sub-box
        # Calculate the top-left cell coordinates of the sub-box
        sub_box_start_x = (grid_x // 3) * 3
        sub_box_start_y = (grid_y // 3) * 3

        for grid_x in range(sub_box_start_x, sub_box_start_x + 3):
            for grid_y in range(sub_box_start_y, sub_box_start_y + 3):
                self.set_button_highlight(grid_x, grid_y, VISUAL_HIGHLIGHT)

    def remove_highlights(self):
        self.board.get_game_canvas().delete(HIGHLIGHT_TAG)

    def remove_panel(self):
        self.panel.place_forget()

    def remove_number_at_location(self, x, y):
        game_logic = self.game.get_object(GAME_LOGIC)

        # Remove number in unlocked position (user moves only)
        if (x, y) in self.user_move_locations:
            self.push_to_stack(lambda: self.insert_number(self.user_move_locations[(x, y)], x, y))
            print(*self.undo_stack)
            self.board.remove_symbol(x, y)
            game_logic.remove_number(x, y)

    def set_button_highlight(self, grid_x, grid_y, new_color):
        x0 = grid_x * self.board.box_width
        y0 = grid_y * self.board.box_height
        x1 = grid_x * self.board.box_width + self.board.box_width
        y1 = grid_y * self.board.box_height + self.board.box_height
        rect = self.board.get_game_canvas().create_rectangle(x0, y0, x1, y1, fill=new_color, tags=HIGHLIGHT_TAG)
        self.board.get_game_canvas().tag_lower(rect)

    def get_red_number(self, image):
        new_color = (255, 0, 0)
        width, height = image.size

        for x in range(width):
            for y in range(height):
                r, g, b, a = image.getpixel((x, y))
                if r + g + b + a == 0:
                    continue
                image.putpixel((x, y), new_color)
                pass

        return image

    def undo_move(self):
        if self.board.get_state():
            self.undo_stack[-1]()
            self.pop_from_stack()


    def push_to_stack(self, state):
        self.undo_stack.append(state)

    def pop_from_stack(self):
        self.undo_stack.pop()



class SudokuRightPanel:
    def __init__(self, parent, game, **arguments):
        self.arguments = {**arguments}
        self._placement_manager = None

        self.game = game

        self.PANEL_LAYOUT = {
            "width": 200,
            "height": 420,
            "fg_color": "transparent",
            "bg_color": "transparent",
        }

        self.BUTTON_LAYOUT = {
            "width": 65,
            "height": 70,
            "corner_radius": 4,
            "text_color": "#D51989",
            "font": ("Arial", 33),
            "fg_color": "black",
            "bg_color": "transparent",
            "hover_color": "#4F6469"

        }
        # 333635
        self.UNDO_LAYOUT = {
            "width": 15,
            "height": 30,
            "corner_radius": 50,
            "fg_color": "transparent",
            "bg_color": "transparent",
            "text_color": "white",
            "font": ("Arial", 13),
            "text": "Undo",
            "hover_color": "#980E87",
            "text_color": "grey"

        }

        self.ERASE_LAYOUT = {
            "width": 15,
            "height": 30,
            "corner_radius": 50,
            "fg_color": "transparent",
            "bg_color": "transparent",
            "text_color": "white",
            "font": ("Arial", 13),
            "text": "Erase",
            "hover_color": "#980E87",
            "text_color": "grey"

        }

        self.HINT_LAYOUT = {
            "width": 15,
            "height": 30,
            "corner_radius": 50,
            "fg_color": "transparent",
            "bg_color": "transparent",
            "text_color": "white",
            "font": ("Arial", 13),
            "text": "Hint",
            "hover_color": "#980E87",
            "text_color": "grey"
        }

        self.NEW_GAME_LAYOUT = {
            "width": 200,
            "height": 40,
            "fg_color": "#D51989",
            "bg_color": "transparent",
            "font": ("Arial", 15, "bold"),
            "text": "New Game",
            "text_color": "white",
            "corner_radius": 4
        }

        self.LEAVE_GAME_LAYOUT = {
            "width": 200,
            "height": 40,
            "fg_color": "transparent",
            "bg_color": "transparent",
            "hover_color": WINDOW_BACKGROUND_COLOR,
            "font": ("Arial", 15, "bold"),
            "text": "Leave",
            "text_color": "white",
            "corner_radius": 4
        }

        self.DIFFICULTY_BAR = {
            "width": 200,
            "height": 30,
            "fg_color": "black",
            "bg_color": "transparent",
            "selected_hover_color": "#980E87",
            "selected_color": "#D51989",
            "values": ["Easy", "Medium", "Hard"],
            "font": ("Arial", 14),
            "dynamic_resizing": False,
            "unselected_color": "black",
            "unselected_hover_color": "#980E87",
            "corner_radius": 5
        }

        self.frame = customtkinter.CTkFrame(master=parent, **self.PANEL_LAYOUT)
        self.dynamic_layout(self.frame, self.arguments)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.number_pad_keys = []
        self.number_clicked = None

        num = 1
        for i in range(2, 5):
            for j in range(0, 3):
                key = customtkinter.CTkButton(master=self.frame, **self.BUTTON_LAYOUT, text=str(num), command=lambda num=num: self.send_number_to_board(num))
                if i == 2:
                    self.number_pad_keys.append(key)
                    key.grid(row=i, column=j, sticky="s")

                elif i == 4:
                    self.number_pad_keys.append(key)
                    key.grid(row=i, column=j, sticky="n")

                else:
                    self.number_pad_keys.append(key)
                    key.grid(row=i, column=j)

                num += 1

        size = int(self.BUTTON_LAYOUT["height"] * 0.8)
        self.undo = customtkinter.CTkButton(master=self.frame, **self.UNDO_LAYOUT, image=ImageTk.PhotoImage(Image.open("Games/Sudoku/Assets/Undo.png").resize((size, size))), compound="top")
        self.undo.configure(command=self.undo_move)
        self.undo.grid(row=1, column=0, sticky="w")

        self.erase = customtkinter.CTkButton(master=self.frame, **self.ERASE_LAYOUT, image=ImageTk.PhotoImage(Image.open("Games/Sudoku/Assets/eraser.png").resize((size, size))), compound="top")
        self.erase.configure(command=self.erase_move)
        self.erase.grid(row=1, column=1, sticky="w")

        self.hint = customtkinter.CTkButton(master=self.frame, **self.HINT_LAYOUT, image=ImageTk.PhotoImage(Image.open("Games/Sudoku/Assets/hint.png").resize((size, size))), compound="top")
        self.hint.configure(command=self.give_hint)
        self.hint.grid(row=1, column=2, sticky="w")

        self.padding = customtkinter.CTkLabel(master=self.frame, text="")
        self.padding.grid(row=5)

        self.new_game = customtkinter.CTkButton(master=self.frame, **self.NEW_GAME_LAYOUT, command=self.start_new_game)
        self.new_game.grid(row=6, columnspan=3, column=0, sticky="n")

        self.leave_game = customtkinter.CTkButton(master=self.frame, command=self.leave_game, **self.LEAVE_GAME_LAYOUT)
        self.padding2 = customtkinter.CTkLabel(master=self.frame, text="")
        self.padding2.grid(row=8)
        self.leave_game.grid(row=9, columnspan=3, column=0, sticky="n")

        self.difficulty_bar = customtkinter.CTkSegmentedButton(master=self.frame, **self.DIFFICULTY_BAR)
        self.difficulty_bar.grid(row=0, column=0, columnspan=3)
        self.difficulty_bar.configure(command=self.set_selected_button)

        # Set default difficulty
        self.difficulty = "Easy"

    def give_hint(self):
        game_board = self.game.get_object(SUDOKU_BOARD)
        game_logic = self.game.get_object(GAME_LOGIC)
        if game_board.board.get_state():
            x, y = random.randint(0, 8), random.randint(0, 8)
            while game_logic.unsolved_board[x][y] != ".":
                if game_logic.get_spots_left() == 0:
                    return
                x, y = random.randint(0, 8), random.randint(0, 8)
            game_board.insert_number(game_logic.solved_board[x][y], x, y)
            game_board.board.canvas.delete(HIGHLIGHT_TAG)
            game_board.set_button_highlight(x, y, HIGHLIGHT_COLOR)

    def undo_move(self):
        self.game.get_object(SUDOKU_BOARD).undo_move()

    def leave_game(self):
        self.game.get_object(SUDOKU_BOARD).leave_game()

    def erase_move(self):
        game_board = self.game.get_object(SUDOKU_BOARD)
        if game_board.board.get_state():
            self.game.get_object(SUDOKU_BOARD).remove_number_at_selected_location()

    def send_number_to_board(self, number):
        self.game.get_object(SUDOKU_BOARD).insert_number(str(number))

    def set_selected_button(self, value):
        self.difficulty = value

    def start_new_game(self):
        self.game.get_object(SUDOKU_BOARD).reset()
        self.game.get_object(SUDOKU_BOARD).load_board(self.difficulty)
        self.game.get_object(TOP_PANEL).timer.start()

        self.game.get_object(SUDOKU_BOARD).board.flip_state(True)

    def dynamic_layout(self, object, args, prefer=None):

        if prefer == "pack":
            object.pack(**args)
            object.pack_propagate(False)
            self._placement_manager = "pack"

        elif prefer == "grid":
            object.grid(**args)
            object.grid_propagate(False)
            self._placement_manager = "grid"

        elif prefer == "place":
            object.place(**args)
            self._placement_manager = "place"


        else:
            print("Arguments aren't matching up with layout or prefer = None")

        try:
            object.grid(**args)
            object.grid_propagate(False)
            self._placement_manager = "grid"
            return
        except Exception:
            pass

        try:
            object.pack(**args)
            object.pack_propagate(False)
            self._placement_manager = "pack"
            return
        except Exception:
            pass

        try:
            object.place(**args)
            self._placement_manager = "place"
            return
        except Exception:
            pass

    def show(self):
        if self._placement_manager == "grid":
            self.frame.grid(**self.arguments)
            self.frame.grid_propagate(False)

        elif self._placement_manager == "pack":
            self.frame.pack(**self.arguments)
            self.frame.pack_propagate(False)

        elif self._placement_manager == "place":
            self.frame.place(**self.arguments)

    def hide(self):
        if self._placement_manager == "grid":
            self.frame.grid_forget()
        elif self._placement_manager == "pack":
            self.frame.pack_forget()
        elif self._placement_manager == "place":
            self.frame.place_forget()