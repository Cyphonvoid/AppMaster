import customtkinter
from System import *


class Settings(ComponentManager):


    def __init__(self, parent, **arguments):
        ComponentManager.__init__(self)
        self.set_attribute(Type.CLASS_NAME, "Settings")

        self.parent = parent
        self.arguments = {**arguments}

        
        self.FRAME_LAYOUT = {
            "height":900, 
            "width":1130,
            "fg_color":"transparent",
            "bg_color":"transparent"
        }

        self.TITLE_LAYOUT = {
            "bg_color":"transparent",
            "fg_color":"transparent",
            "font":("Arial", 23, "normal"),
            "text_color":"white",
            "text":"Settings"
        }

        self.frame = customtkinter.CTkFrame(master=self.parent, **self.FRAME_LAYOUT)
        self.frame.grid(**self.arguments)
        self.frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=2)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.frame.grid_propagate(False)

        self.page_title = customtkinter.CTkLabel(master=self.frame, **self.TITLE_LAYOUT)
        self.page_title.grid(row=0, column=0, sticky="w", padx=35)
        pass
    

    def enable(self, extra=None):
        self.frame.grid(**self.arguments)
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