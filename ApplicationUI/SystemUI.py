import customtkinter
from System import *
from .DesignStyles import *
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("Dark")

class SystemUI(customtkinter.CTk, ComponentManager):
    CLASS_OBJECT_ID = 2000

    @staticmethod
    def assign_classlevel_id():
        SystemUI.CLASS_OBJECT_ID += 1
        return SystemUI.CLASS_OBJECT_ID

    def __init__(self, width_px, height_px):
        customtkinter.CTk.__init__(self)
        ComponentManager.__init__(self)
        

        self._default_width = width_px
        self._default_height = height_px
        
        self.current_height = height_px
        self.current_width = width_px

        self.set_classname("SystemUI")
        self.geometry(str(width_px) + "x" + str(height_px))
        self.title("EnvisionAI") 
        self.configure(fg_color=WINDOW_BACKGROUND_COLOR, corner_radius = 40)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=100)
        self.grid_columnconfigure(2, weight=1)


        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
    
        self.grid_propagate(False)
        self.columnspan = 3

        self.components = []


    def add_component(self, *components):
        for comp in components:
            self.components.append(comp)

    
    def center(self):
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        posX = screen_width/2 - self.winfo_width()/2
        posY = screen_height/2 - self.winfo_height()/2 

        self.geometry(str(self.winfo_width()) + "x" + str(self.winfo_height()) + "+" + str(posY) + "+" + str(posX))
        self.grid(fg_color=WINDOW_BACKGROUND_COLOR, corner_radius = 40)
        pass

    def get_component(self, index=None):
        if index is None:
            last_position = len(self.components) - 1
            return self.components[last_position]

        else:
            return self.components[index]
    
    def remove_component(self, *components):
        if(len(self.components) == 0):
            return
        
        for component in components:
            self.components.remove(component)
        

    def launch(self):
        self.mainloop()
    

    def resize(self, width, height):
        self.geometry(str(width) + "x" + str(height))
        self.current_height = height
        self.current_width = width
        #self.configure(fg_color=WINDOW_BACKGROUND_COLOR, corner_radius = 40)
        pass
    
    def restore(self):
        self.current_height = self._default_height
        self.current_width = self.current_width

        self.current_width -= 1
        self._current_height -=1
        self.geometry(str(self._default_width) + "x" + str(self._default_height))
        print(self._default_height, self._default_width)
        #self.configure(fg_color=WINDOW_BACKGROUND_COLOR, corner_radius = 40)

    def get_reference(self):
        return self

    def enable(self, extra=None):
        pass

    def disable(self, extra=None):
        self.quit()
        pass

    def handle_request(self, message, extra):

        if(message == "turnonbg"):
            self.background_toggle = "ON"
            
        elif(message == "turnoffbg"):
            self.background_toggle = "OFF"
        
        elif(message == "center"):
            self.center()
            pass

        elif(message == "resize"):
            self.resize(extra[0], extra[1])

        elif(message == "restoredefault"):
            self.restore()

