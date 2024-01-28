from System import *
from PIL import Image, ImageTk
from .Profilebar import*
from .AppContainer import*
from .SearchBar import*


class HomePage(ComponentManager):

    def __init__(self, parent, **Arguments):
        ComponentManager.__init__(self)
        
        self.set_attribute(Type.CLASS_NAME, "HomePage")


        self.data_hub = None
        self.TITLE_LAYOUT = {
            "text":"Home",
            "text_color":"white",
            "font":customtkinter.CTkFont(family="Arial", size=23, weight="normal")
        }
        

        self.FRAME_LAYOUT = {
            "height":900, 
            "width":1130,
            "fg_color":"transparent",
            "bg_color":"transparent"
        }

        
        self.GRID_ARGUMENTS = {**Arguments}
        self.parent = parent


        self.frame = customtkinter.CTkFrame(master=parent, **self.FRAME_LAYOUT)
        self.frame.grid(**self.GRID_ARGUMENTS)
        self.frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=2)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.frame.grid_propagate(False)


        self.title = customtkinter.CTkLabel(master=self.frame, **self.TITLE_LAYOUT)
        self.title.grid(row=0, column=0, sticky="w", padx=35)
        
        
        self.ProfileBar = ProfileBar(self.frame, row=0, column=7, rowspan=8, sticky="nwes").set_name("Jaedon Spurlock").set_image("ApplicationUI/Assets/profile.jpg")
        self.Search = SearchBar(self.frame, row=1, column=0, rowspan=2, columnspan=7, sticky="wn", padx=35)
        self.GameBoxes = [AppBox(self.frame, row=7, column=0, sticky="e")
                            .set_image("ApplicationUI/Assets/synthwave.png")
                            .set_title("The Drgaon Slayer")
                            .set_description("Strategy game"),
                          AppBox(self.frame, row=7, column=1, sticky="e")
                            .set_image("ApplicationUI/Assets/defaultpic.png")
                            .set_title("Empire worlds"), 
                          AppBox(self.frame, row=7, column=2, sticky="e")
                            .set_image("ApplicationUI/Assets/synthwave.png")
                            .set_title("Tic Tac Toe")
                          ]

    def enable(self, extra=None):
        self.frame.grid(**self.GRID_ARGUMENTS)
        pass

    def disable(self, extra=None):
        self.frame.grid_forget()
        pass

    def handle_request(self, request, extra):

        if(request == "enable"):
            self.enable()

        elif(request == "disable"):
            self.disable()

        pass

    
    pass
