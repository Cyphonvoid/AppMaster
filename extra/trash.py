

"""class SudokuStats():

    def __init__(self, parent, **arguments):
        

        self.parent = parent, 
        self.arguments = {**arguments}
        
        self.FRAME_LAYOUT = {
            "bg_color":"transparent",
            "fg_color":"transparent",
            "width":400,
            "height":90
        }
        self.MISTAKE_LAYOUT = {
            "width":30, 
            "height":9,
            "bg_color":"transparent",
            "fg_color":"red",
            "font":("Arial", 13)
        }

        self.NO_GAMES = {
            "width":30, 
            "height":9,
            "bg_color":"transparent",
            "fg_color":"red",
            "font":("Arial", 13)
        }

        self.TIMER_LAYOUT = {
            "width":76, 
            "height":70,
            "bg_color":"transparent",
            "fg_color":"red",
            "font":("Arial", 13)
        }
        self._timer_value = 0
        self._timer_trigger = "pause"
        self.pause_image = ImageTk.PhotoImage(Image.open("Games/Sudoku/Assets/pause.png"))
        self.resume_image = ImageTk.PhotoImage(Image.open("Games/Sudoku/Assets/resume.png"))

        self.frame = customtkinter.CTkFrame(master=parent, **self.FRAME_LAYOUT)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        

        #self.mistakes = customtkinter.CTkLabel(master=self.frame, **self.MISTAKE_LAYOUT, text="Mistakes: ")
        #self.mistakes.grid(column=0, row=0, sticky="nsew")

        #self.number_of_games = customtkinter.CTkLabel(master=self.frame, **self.NO_GAMES, text="Games: ")
        #self.number_of_games.grid(column=1, row=0, sticky="nsew")

        #self.timer = customtkinter.CTkLabel(master=self.frame, font=("Arial", 13), text="0:00")
        #self.timer.grid(column=2, row=0, sticky="w")

        self.timer_button = customtkinter.CTkButton(master=self.frame, **self.TIMER_LAYOUT, command=self.TimerTrigger, text="")
        self.timer_button.grid(column=2, row=0)

        pass

    
    def TimerStart(self, num):
        self._timer_value = num
        pass

    def TimerStop(self):
        
        pass

    def TimerTrigger(self):
        if(self._timer_trigger == "pause"):
            self._timer_trigger = "resume"
            print("resume")
            self.timer_button.configure(image=self.resume_image)
        elif(self._timer_trigger == "resume"):
            self._timer_trigger = "pause"
            print("pause")
            self.timer_button.configure(image=self.pause_image)

        pass

    def hide(self):
        self.frame.grid_forget()
        pass

    def show(self):
        self.frame.grid(**self.arguments)
        pass

    pass
"""