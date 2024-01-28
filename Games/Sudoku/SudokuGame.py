from .SudokuGraphics import *
from .SudokuLogic import *
import customtkinter


class Sudoku:
    def __init__(self, parent, **arguments):
        self.parent = parent
        self.arguments = {**arguments}
        self.__PLACE_METHOD = "grid"

        self.GAME_WINDOW_LAYOUT = {
           "bg_color": "transparent",
           "fg_color": "transparent",
           "corner_radius": 0
        }

        self.GameWindow = customtkinter.CTkFrame(master=parent, **self.GAME_WINDOW_LAYOUT)
        self.GameWindow.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=2)
        self.GameWindow.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
        self.GameWindow.parent = parent

        self.objects = {
            "right_panel": SudokuRightPanel(self.GameWindow, game=self, row=5, column=5),
            "sudoku_board": SudokuBoard(self.GameWindow, game=self, row=1, column=0, rowspan=11, columnspan=3, sticky="nsew"),
            "top_panel": SudokuStatBar(self.GameWindow, game=self, row=0, column=0, columnspan=3, sticky="w", padx=20),
            "game_logic": SudokuLogic(game=self)
        }

        self.padding = customtkinter.CTkFrame(self.GameWindow, fg_color="transparent", width=40)
        self.padding.grid(row=0, column=4, rowspan=11)
        self.padding2 = customtkinter.CTkFrame(self.GameWindow, fg_color="transparent", width=40)
        self.padding2.grid(row=0, column=6, rowspan=11)

        # Disabling the board until the game is ready
        self.objects["sudoku_board"].board.flip_state(False)

        # self.right_panel = SudokuRightPanel(parent, row = 1, column=3)
        # self.sudoku_board = sudoku_board(parent, row=1, column=1, rowspan=4)
        # self.top_panel = SudokuStatBar(parent, row=0, column=1, columnspan=8, sticky="w", padx=20)

    def get_object(self, obj_identifier: str):
        return self.objects.get(obj_identifier)

    def leave_game(self):
        self.GameWindow.grid_forget()
        self.parent.unbind("<Keypress>")

    def show(self):
        if self.__PLACE_METHOD == "grid":
            self.GameWindow.grid(**self.arguments)
            self.GameWindow.grid_propagate(False)

        elif self.__PLACE_METHOD == "pack":
            self.GameWindow.pack(**self.arguments)
            self.GameWindow.pack_propagate(False)

        elif self.__PLACE_METHOD == "place":
            self.GameWindow.place(**self.arguments)

        self.objects["right_panel"].show()

    def hide(self):
        if self.__PLACE_METHOD == "grid":
            self.GameWindow.grid_forget()
        elif self.__PLACE_METHOD == "pack":
            self.GameWindow.pack_forget()
        elif self.__PLACE_METHOD == "place":
            self.GameWindow.place_forget()
        pass
        self.objects["right_panel"].hide()

    def setup(self):
        pass

    def start(self):
        self.show()

    def close(self):
        self.hide()