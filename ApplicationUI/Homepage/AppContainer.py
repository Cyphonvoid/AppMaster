import customtkinter
from PIL import Image, ImageTk
import json

class AppBox():
    
    def __init__(self, parent, **arguments):

        self.arguments = {**arguments}
        self.parent = parent
        self._placement_manager = None
        self.BOX_LAYOUT = {
            "width":170, 
            "height":240,
            "bg_color":"transparent",
            "fg_color":"black",
            "corner_radius":5
        }

        self.IMAGE_LAYOUT = {
            "width":130,
            "height":110,
            "corner_radius":0,
            "bg_color":"transparent",
            "fg_color":"#D51989",
            "text":""
        }
        
        self.BUTTON_LAYOUT = {
            "width":50, "height":30,
            "bg_color":"transparent", "fg_color":"black",
            "corner_radius":6, "text":"PLAY", "text_color":"white",
            "command":None, "hover_color":"#D51989"
        }
        
        self.DESC_BOX_LAYOUT = {
            "font":("Arial", 15, "bold"),
            "bg_color":"transparent",
            "fg_color":"transparent",
            "padx":30

        }

        self.ABOUT_LAYOUT = {
            "fg_color":"transparent",
            "bg_color":"transparent",
            "padx":25,
            "font":("Arial", 13),
            "text_color":"darkgrey",
            "height":34
    
        }

        self.frame = customtkinter.CTkFrame(master=parent, **self.BOX_LAYOUT)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=17)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=18)
        self.dynamic_layout(self.frame, self.arguments)   
       
        self.image = customtkinter.CTkLabel(master=self.frame, **self.IMAGE_LAYOUT)
        self.image.grid(row=0, column=0)
        self.image.grid_columnconfigure(0, weight=1)
        self.image.grid_rowconfigure(0, weight=1) 
        
        self.launch_button = customtkinter.CTkButton(master=self.image, **self.BUTTON_LAYOUT)
        self.launch_button.grid(row=0, column=0)
 
        self.titlebox = customtkinter.CTkLabel(master=self.frame, **self.DESC_BOX_LAYOUT)
        self.titlebox.grid(row=1, column=0, sticky="wn")

        self.aboutbox = customtkinter.CTkTextbox(master=self.frame, **self.ABOUT_LAYOUT)
        self.aboutbox.grid(row=2, column=0, sticky="wn")
        self.aboutbox.insert("1.0", "Game Name")
        self.aboutbox.configure(state="disabled")

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
    
    def set_image(self, path):
        new_image = ImageTk.PhotoImage(Image.open(path).resize((self.IMAGE_LAYOUT["width"]+90, self.IMAGE_LAYOUT["height"]+70)))
        self.image.configure(image=new_image)
        return self
        pass


    def set_title(self, title):
        self.titlebox.configure(text=title)
        return self
        pass
    
    def set_description(self, desc):
        self.aboutbox.configure(state="normal")
        self.aboutbox.delete("1.0", "end")
        self.aboutbox.insert("1.0", desc)
        self.aboutbox.configure(state="disabled")
        return self
        pass
    
    def onclick_play(self, callback):
        self.launch_button.configure(command=callback)
        pass
    
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
    
    pass