from .SudokuTimer import *

MISTAKES_ALLOWED = 10

class SudokuStatBar():

    def __init__(self, parent, game, **arguments):
        self.parent = parent
        self.argument = {**arguments}
        self.game = game

        self.right_panel = None
        self.mistake_count = 0

        self.FRAME_LAYOUT = {
            "width": 500,
            "height": 40,
            "bg_color": "transparent",
            "fg_color": "black"
        }

        self.MISTAKE_LAYOUT = {
            "bg_color": "transparent",
            "fg_color": "transparent",
            "font": ("Arial", 15, "bold"),
            "text_color": "grey",
            "padx": 15
        }

        self.TOTAL_GAMES_LAYOUT = {
            "bg_color": "transparent",
            "fg_color": "transparent",
            "font": ("Arial", 15, "bold"),
            "text_color": "grey",
            "text": "Games: 109"
        }

        self.frame = customtkinter.CTkFrame(master=self.parent, **self.FRAME_LAYOUT)
        self.frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_propagate(False)
        self.frame.grid(**self.argument)

        self.timer = SudokuTimer(self.frame, row=0, column=0, columnspan=2, sticky="w", padx=10)
        self.timer.set_time(10)

        self.mistake_counter = customtkinter.CTkLabel(master=self.frame, **self.MISTAKE_LAYOUT)
        self.mistake_counter.grid(row=0, column=2, sticky="w")
        self.change_mistakes()

        self.total_games = customtkinter.CTkLabel(master=self.frame, **self.TOTAL_GAMES_LAYOUT, padx=10)
        self.total_games.grid(row=0, column=3, sticky="e")

    def increment_mistake(self):
        self.mistake_count+=1
        self.change_mistakes()

    def get_mistakes(self):
        return self.mistake_count

    def change_mistakes(self):
        self.mistake_counter.configure(text=f"Mistakes: {self.mistake_count}/{MISTAKES_ALLOWED}")

    def reset_mistakes(self):
        self.mistake_count = 0
        self.change_mistakes()

    def show(self):
        self.frame.grid(**self.argument)
        self.timer.show()

    def hide(self):
        self.frame.grid_forget()
        self.timer.hide()