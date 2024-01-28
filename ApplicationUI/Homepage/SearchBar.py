import customtkinter
from PIL import Image, ImageTk


class SearchBar():

    def __init__(self, parent, **arguments):

        self.arguments = {**arguments}
        self.parent = parent  
        self._placement_manager = None


        self.SEARCHBAR_LAYOUT = {
            "width":670,
            "height":50,
            "bg_color":"transparent",
            "fg_color":"black",
            "corner_radius":25,
            "border_width":0.6,
            "border_color":"#333333"
        }


        self.SearchBar = customtkinter.CTkFrame(master=parent, **self.SEARCHBAR_LAYOUT)
        self.dynamic_layout(self.SearchBar, self.arguments)
        pass

    

    def display(self, display):
        pass

    def set_image(self, path):
        new_image  = ImageTk.PhotoImage(Image.open(path).resize((self.SearchBar_LAYOUT["width"], self.SearchBar_LAYOUT["height"])))
        self.SearchBar.configure(image = new_image)
        pass

    def dynamic_layout(self, object, args):

        try:
            object.grid(**args)
            object.grid_propagate(False)
            self._placement_manager = "grid"
            return
        except Exception: pass

        try:
            object.pack(**args)
            object.pack_propagate(False)
            self._placement_manager = "pack"
            return
        except Exception: pass

        try:
            object.place(**args)
            self._placement_manager = "place"
            return
        except Exception: pass
    

    def show(self):
        if(self._placement_manager == "grid"):
            self.SearchBar.grid(**self.arguments)
        elif(self._placement_manager == "pack"):
            self.SearchBar.pack(**self.arguments)
        elif(self._placement_manager == "place"):
            self.SearchBar.place(**self.arguments)
        pass

    def hide(self):
        if(self._placement_manager == "grid"):
            self.SearchBar.grid_forget()
        elif(self._placement_manager == "pack"):
            self.SearchBar.pack_forget()
        elif(self._placement_manager == "place"):
            self.SearchBar.place_forget()
        pass

