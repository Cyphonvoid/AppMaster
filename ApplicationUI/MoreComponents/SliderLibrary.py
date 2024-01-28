import customtkinter
from PIL import Image, ImageTk


class SliderLibrary():

    def __init__(self, parent, **Arguments):
    
        self.arguments = {**Arguments}
    
        self._library = []

        self.SCROLL_FRAME = {
            "width":600, 
            "height":120,
            "bg_color":"transparent",
            "fg_color":"red",
            "corner_radius":10,
        }

        self.scroll_frame = customtkinter.CTkScrollableFrame(master=parent, **self.SCROLL_FRAME, orientation="horizontal")
        self.scroll_frame.grid(**self.arguments)

        self.add_icon(6)
        pass

    def add_icon(self, num):
        for i in range(0, num):
            #icon = AppIcon(self.scroll_frame, side="left", padx=20)
            #self._library.append(icon)
            pass
        pass
    
    def show(self):
        self.scroll_frame.grid(**self.arguments)

    def hide(self):
        self.scroll_frame.grid_forget()

    def configure_icon(self):
        pass

    def remove_icon(self, index):
        self._library.pop(index)
    pass
