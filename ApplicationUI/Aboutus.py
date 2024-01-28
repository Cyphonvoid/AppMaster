import customtkinter
from System import *
from PIL import ImageTk, Image



class AboutUs(ComponentManager):

    def __init__(self, parent, **arguments):
        ComponentManager.__init__(self)
        self.set_attribute(Type.CLASS_NAME, "AboutUs")

        self.parent = parent
        self.arguments = {**arguments}


        self.FRAME_LAYOUT = {
            "width":1130,
            "height":900,
             "fg_color":"transparent",
            "bg_color":"transparent"
        }

        self.TITLE_LAYOUT = {
            "text":"AboutUs",
            "font":("Arial", 23, "normal"),
            "text_color":"white"
        }

        self.frame = customtkinter.CTkFrame(master=self.parent, **self.FRAME_LAYOUT)
        self.frame.grid(**self.arguments)
        self.frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=2)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.frame.grid_propagate(False)

        self.title = customtkinter.CTkLabel(master=self.frame, **self.TITLE_LAYOUT)
        self.title.grid(row=0, column=0, sticky="w", padx=35)

    def enable(self, extra = None):
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