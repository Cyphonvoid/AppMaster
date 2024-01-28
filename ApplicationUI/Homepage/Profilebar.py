import customtkinter 
from PIL import Image, ImageTk



class ProfileBar():

    def __init__(self, parent, **arguments):

        self.arguments = {**arguments}
        self.parent = parent
        self._placement_manager = None
        self.BAR_LAYOUT = {
            "bg_color":"transparent",
            "fg_color":"black",
            "corner_radius":5
        }
        
        self.IMAGE_LAYOUT = {
            "bg_color":"transparent",
            "fg_color":"#111111",
            "corner_radius":0,
            "width":110,
            "height":100,
            #"border_width":2,
            #"border_color":"orange",
            "text":""

        }

        self.NAME_LAYOUT = {
            "width":90,
            "height":4,
            "font":("Arial", 16),
            "text":"Username",
            "bg_color":"transparent",
            "fg_color":"transparent"
        }
        
        self.EDIT_LAYOUT = {
            "width":160,
            "height":30,
            "bg_color":"transparent",
            "fg_color":"#D51989",
            "font":("Arial", 15, "bold"),
            "text_color":"black",
            "text":"Edit Profile",
            "hover_color":"#980E87"
        }

        self.bar = customtkinter.CTkFrame(master=parent, **self.BAR_LAYOUT)
        self.dynamic_layout(self.bar, self.arguments)
        self.bar.grid_columnconfigure(0, weight=1)
        self.bar.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.bar.grid_rowconfigure((7, 8), weight=3)


        self.image = customtkinter.CTkLabel(master=self.bar, **self.IMAGE_LAYOUT)
        self.image.grid(row=0, column=0, sticky="s")

        self.name = customtkinter.CTkLabel(master=self.bar, **self.NAME_LAYOUT)
        self.name.grid(row=1, column=0)
        
        self.edit_profile = customtkinter.CTkButton(master=self.bar, **self.EDIT_LAYOUT)
        self.edit_profile.grid(row=2, column=0, sticky="n")
        
       
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
    
    
    def set_color(self, clr):
        self.bar.configure(fg_color=clr)
        return self
        pass
    
    def set_image(self, path):
        new_image = ImageTk.PhotoImage(Image.open(path).resize( (self.IMAGE_LAYOUT["width"]+44, self.IMAGE_LAYOUT["height"]+40)))
        self.image.configure(image=new_image)
        print("CALLED")
        return self
        pass
    
    def set_name(self, name):
        self.name.configure(text=name)
        return self
        pass

    def onclick_edit(self, callback):
        return self
        pass
    
    def show(self):
        if(self._placement_manager == "grid"):
            self.bar.grid(**self.arguments)
        elif(self._placement_manager == "pack"):
            self.bar.pack(**self.arguments)
        elif(self._placement_manager == "place"):
            self.bar.place(**self.arguments)
        
        pass

    def hide(self):
        if(self._placement_manager == "grid"):
            self.bar.grid_forget()
        elif(self._placement_manager == "pack"):
            self.bar.pack_forget()
        elif(self._placement_manager == "place"):
            self.bar.place_forget()
        pass
    
        pass