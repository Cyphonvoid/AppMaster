import customtkinter
from PIL import Image, ImageTk

class AppIcon(customtkinter.CTkFrame):
    
    def __init__(self, parent, **arguments):
        customtkinter.CTkFrame.__init__(self, master=parent)

        self._parent = parent
        self._placement_manager = None
        self.arguments = {
            **arguments
        }
        
        self.ICON_LAYOUT = {
            "width":150,
            "height":115,
            "bg_color":"transparent",
            "fg_color":"black",
            "corner_radius":10,
        }
        
        self.BUTTON_LAYOUT = {
            "width":50,
            "height":30,
            "bg_color":"transparent",
            "fg_color":"#D51989",
            "corner_radius":6,
            "text":"PLAY",
            "text_color":"white",
            "command":None, 
            "hover_color":"#05EAEB"
        }

        self.configure(**self.ICON_LAYOUT)
        self._dynamic_placement()

        self._play_button = customtkinter.CTkButton(master=self, **self.BUTTON_LAYOUT)
        self._play_button.pack(expand=True)
        pass

    
    def _dynamic_placement(self):
        try:
            self.grid(**self.arguments)
            self.grid_propagate(False)
            self._placement_manager = "grid"
            return
        except Exception: pass

        try:
            self.pack(**self.arguments)
            self.pack_propagate(False)
            self._placement_manager = "pack"
            return
        except Exception: pass

        try:
            self.place(**self.arguments)
            self._placement_manager = "place"
            return
        except Exception: pass

    def show(self):
        if(self._placement_manager == "grid"): self.grid(**self.arguments)
        elif(self._placement_manager == "pack"): self.pack(**self.arguments)
        elif(self._placement_manager == "place"): self.place(**self.arguments)
        pass

    def hide(self):
        if(self._placement_manager == "grid"): self.grid_forget()
        elif(self._placement_manager == "pack"): self.pack_forget()
        elif(self._placement_manager == "place"): self.place_forget()
        pass
    
    def onclick(self, action):
        self.BUTTON_LAYOUT["command"] = action
        self._play_button.configure(command=self.BUTTON_LAYOUT["command"])
        pass
    
    def get_height(self):
        return self.ICON_LAYOUT["height"]
    
    def get_width(self):
        return self.ICON_LAYOUT["width"]

    pass