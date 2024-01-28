from System import *
from .Utility import *
from PIL import Image, ImageTk


class SideBar(ComponentManager):


    def __init__(self, parent, **grid_layout):
        ComponentManager.__init__(self)
        self.set_attribute(Type.CLASS_NAME, "SideBar")

        #Create a frame
        self.frame = customtkinter.CTkFrame(master=parent, fg_color="black", bg_color="transparent")
        self.frame.grid(**grid_layout)
        self.frame.pack_propagate(False)
        
        self.grid_layout = grid_layout

        self.shrink_layout = {
            **grid_layout.copy(),
            "padx" : 20,
            "pady": 20
        }
        
        self.current_layout = self.grid_layout
        self.parent = parent
        self.rows = 10
        self.columns = 2
        self.previous_button = None

        self.button_socket = [Socket(), Socket(), Socket(), Socket(), Socket(), Socket(), Socket()]
        
        for i in range(1, self.rows+1):
            self.frame.grid_rowconfigure(i, weight=1)

        
        for i in range(1, self.columns+1):
            self.frame.grid_columnconfigure(i, weight=1)

        
        OptionStyle = {
            "bg_color": "transparent",
            "fg_color": "transparent",
            "font": ("Arial", 16),
            "hover_color" : "black"
        }
        
        
        GeneralStyle = {
            "bg_color": "transparent",
            "fg_color": "transparent",
            "font": ("Arial", 17)
        }

        configurations = {
            "height" : OptionStyle["font"][1] * 2,
            "width": 1,
            "corner_radius": 3,
            "anchor" : "w",
            "padx": 25,
            "pady": 10
        }


        self.OptionState = {
           "Home":{ #yeah that makes sense, this dict is so frikken huge tho idk if i coded everything right lol 
               
               "button-ref":None,
               "state":"released",
               "image-pair":[ImageTk.PhotoImage(self.change_icon_color(Image.open("ApplicationUI/Assets/homesmall.png"), (213, 25, 137))),
                             ImageTk.PhotoImage(Image.open("ApplicationUI/Assets/homesmall.png")),
                             ImageTk.PhotoImage(self.change_icon_color(Image.open("ApplicationUI/Assets/homesmall.png"), (0, 253, 251)))
                ],
                "socket":self.button_socket[0],
                "component":None
           },

           "MyApps":{
               "button-ref":None,
               "state":"released",
               "image-pair":[ImageTk.PhotoImage(self.change_icon_color(Image.open("ApplicationUI/Assets/myapps.png"), (213, 25, 137))),
                             ImageTk.PhotoImage(Image.open("ApplicationUI/Assets/myapps.png")),
                             ImageTk.PhotoImage(self.change_icon_color(Image.open("ApplicationUI/Assets/myapps.png"), (0, 253, 251)))   
                ],
                "socket":self.button_socket[1],
                "component":None
           },

           "MyAccount":{
               "button-ref":None,
               "state":"released",
               "image-pair":[ImageTk.PhotoImage(self.change_icon_color(Image.open("ApplicationUI/Assets/settings.png"), (213, 25, 137))),
                             ImageTk.PhotoImage(Image.open("ApplicationUI/Assets/settings.png")),
                             ImageTk.PhotoImage(self.change_icon_color(Image.open("ApplicationUI/Assets/settings.png"), (0, 253, 251)))
                ],
                "socket":self.button_socket[2],
                "component":None
           },

           "Settings":{
               "button-ref":None,
               "state":"released",
               "image-pair":[
                   ImageTk.PhotoImage(self.change_icon_color(Image.open("ApplicationUI/Assets/contact-us.png"), (213, 25, 137))),
                   ImageTk.PhotoImage(Image.open("ApplicationUI/Assets/contact-us.png")),
                   ImageTk.PhotoImage(self.change_icon_color(Image.open("ApplicationUI/Assets/contact-us.png"), (0, 253, 251)))
                ],
                "socket":self.button_socket[3],
                "component":None
           }, 

           "AboutUs":{
              "button-ref":None,
              "state":"released",
              "image-pair":[ImageTk.PhotoImage(self.change_icon_color(Image.open("ApplicationUI/Assets/aboutus.png"), (213, 25, 137))),
                            ImageTk.PhotoImage(Image.open("ApplicationUI/Assets/aboutus.png")),
                            ImageTk.PhotoImage(self.change_icon_color(Image.open("ApplicationUI/Assets/aboutus.png"), (0, 253, 251)))
                ],
               "socket":self.button_socket[4],
               "component":None
               
           },

           "Logout":{
              "button-ref":None,
              "state":"released",
              "image-pair":[ImageTk.PhotoImage(self.change_icon_color(Image.open("ApplicationUI/Assets/logout.png"), (213, 25, 137))),
                            ImageTk.PhotoImage(Image.open("ApplicationUI/Assets/logout.png")),
                            ImageTk.PhotoImage(self.change_icon_color(Image.open("ApplicationUI/Assets/logout.png"), (0, 253, 251)))
                ],
              "socket":self.button_socket[5],
              "component":None
           }
        }

        #Create a profile logo option
        self.logo_label = customtkinter.CTkLabel(master=self.frame, **GeneralStyle, text=" "+"", text_color="#888888")
        self.logo_label.configure(height=150, width=30)
        self.logo_label.pack(anchor="w", padx=27)


        #Create a label
        LabelStyle = GeneralStyle.copy()
        LabelStyle["font"] = ("Arial", 15)
        self.menu_label = customtkinter.CTkLabel(master=self.frame, **LabelStyle, text="MENU", text_color="#D51989", width=1)
        self.menu_label.pack(anchor="w", padx=27, pady=10)
        

        #Create a home option
        self.home_icon = ImageTk.PhotoImage(Image.open("ApplicationUI/Assets/homesmall.png"))
        self.home = add_button_via_pack(self.frame, **configurations, **OptionStyle, image=self.home_icon, text=" Home")
        self.home.bind("<Button-1>", lambda event: self.event_onclick(self.home, "Home")) 
        self.home.bind("<Enter>", lambda event: self.event_hover(self.home, "Home"))
        self.home.bind("<Leave>", lambda event: self.event_leave(self.home, "Home"))
        self.OptionState["Home"]["button-ref"] = self.home
        

        #Create my apps option
        self.my_apps_icon = ImageTk.PhotoImage(Image.open("ApplicationUI/Assets/myapps.png"))
        self.my_apps = add_button_via_pack(self.frame, **configurations, **OptionStyle, text=" My apps",   image=self.my_apps_icon)
        self.my_apps.bind("<Button-1>",  lambda event: self.event_onclick(self.my_apps, "MyApps"))
        self.my_apps.bind("<Enter>", lambda event: self.event_hover(self.my_apps, "MyApps"))
        self.my_apps.bind("<Leave>", lambda event: self.event_leave(self.my_apps, "MyApps"))
        self.OptionState["MyApps"]["button-ref"] = self.my_apps


        #Create my account option
        self.my_account_image = ImageTk.PhotoImage(Image.open("ApplicationUI/Assets/settings.png"))
        self.my_account = add_button_via_pack(self.frame, **configurations, **OptionStyle, text=" My account", image=self.my_account_image)
        self.my_account.bind("<Button-1>", lambda event: self.event_onclick(self.my_account, "MyAccount"))
        self.my_account.bind("<Enter>", lambda event: self.event_hover(self.my_account, "MyAccount"))
        self.my_account.bind("<Leave>", lambda event: self.event_leave(self.my_account, "MyAccount"))
        self.OptionState["MyAccount"]["button-ref"] = self.my_account


        #Create settings option
        self.settings_us_image = ImageTk.PhotoImage(Image.open("ApplicationUI/Assets/contact-us.png"))
        self.settings = add_button_via_pack(self.frame, **configurations, **OptionStyle, text=" Settings", image=self.settings_us_image)
        self.settings.bind("<Button-1>", lambda event : self.event_onclick(self.settings, "Settings"))
        self.settings.bind("<Enter>", lambda event: self.event_hover(self.settings, "Settings"))
        self.settings.bind("<Leave>", lambda event: self.event_leave(self.settings, "Settings"))
        self.OptionState["Settings"]["button-ref"] = self.settings


        #Create About us option
        self.about_us_image = ImageTk.PhotoImage(Image.open("ApplicationUI/Assets/aboutus.png"))
        self.aboutus = add_button_via_pack(self.frame, **configurations, **OptionStyle, text=" About us", image=self.about_us_image)
        self.aboutus.bind("<Button-1>", lambda event: self.event_onclick(self.aboutus, "AboutUs"))
        self.aboutus.bind("<Enter>", lambda event: self.event_hover(self.aboutus, "AboutUs"))
        self.aboutus.bind("<Leave>", lambda event: self.event_leave(self.aboutus, "AboutUs"))
        self.OptionState["AboutUs"]["button-ref"] = self.aboutus


        #Create Logout option
        self.logout_image = ImageTk.PhotoImage(Image.open("ApplicationUI/Assets/logout.png"))
        self.logout = add_button_via_pack(self.frame, **configurations, **OptionStyle, text=" Logout", image=self.logout_image)
        self.logout.configure(height=170)
        self.logout.pack(side="bottom")
        self.logout.bind("<Button-1>", lambda event: self.event_onclick(self.logout, "Logout"))
        self.logout.bind("<Enter>", lambda event: self.event_hover(self.logout, "Logout"))
        self.logout.bind("<Leave>", lambda event: self.event_leave(self.logout, "Logout"))
        self.OptionState["Logout"]["button-ref"] = self.logout

    
    def event_onclick(self, button, button_name):  
        if(button_name == self.previous_button):
            #Only execute if the button is a different from previous one
            #Otherwise it raises risk of reseting the current one. Common sense
            return  
        
        #Configure the button with attributes and render it
        button.configure(text_color="#D51989", font=("Arial", 16), image=self.OptionState[button_name]["image-pair"][0])
        self.OptionState[button_name]["state"] = "clicked"
    
        #Render previous button
        if(self.previous_button != None):
            self.OptionState[self.previous_button]["button-ref"].configure(text_color="white", font=("Arial", 16), image=self.OptionState[self.previous_button]["image-pair"][1])
            self.OptionState[self.previous_button]["state"] = "released"
            
            try:
                #NOTE Direct connection to components    (Valid and works)
                #self.OptionState[self.previous_button]["component"].disable()
                
                #NOTE Indirect connection to components
                component = self.OptionState[self.previous_button]["component"]
                SystemManager.disable_components(Type.NAME, component, self)

            except Exception: pass

        
       
        try:
            #NOTE Direct connection to components    (Valid and works)
            #self.OptionState[button_name]["component"].enable()

            #NOTE Indirect connection to components via mediator
            component = self.OptionState[button_name]["component"]
            SystemManager.enable_components(Type.NAME, component, self)

        except Exception: pass

        self.OptionState[button_name]["socket"].run_commands()
        self.previous_button = button_name
        pass
 

    def event_hover(self, button, buttonname):
        if(self.OptionState[buttonname]["state"] == "released"):
            button.configure(text_color="#00FDFB", font=("Arial", 18), image=self.OptionState[buttonname]["image-pair"][2])
        pass
    

    def event_leave(self, button, buttonname):
        if(self.OptionState[buttonname]["state"] == "released"):
            button.configure(text_color="white", font=("Arial", 16), image=self.OptionState[buttonname]["image-pair"][1])
        pass

    
    def change_icon_color(self, image, new_color):
        
        width, height = image.size
        
        for x in range(width):
            for y in range(height):
                r, g, b, a = image.getpixel((x,y))
                if(r+g+b+a == 0):
            
                    continue
                image.putpixel((x, y), new_color)
                pass

        return image

    def make_transition(self, transition):
        #Shrinks and expands the sidebar.
        if(transition == "shrink"):
            self.frame.configure(corner_radius=5)
            self.frame.grid(**self.shrink_layout)
            self.current_layout = self.shrink_layout
        
        elif(transition == "expand"):
           self.frame.grid(**self.grid_layout)
           self.current_layout = self.grid_layout

    def reset(self):
        if(self.previous_button == None): return
        self.OptionState[self.previous_button]["button-ref"].configure(text_color="white", font=("Arial", 16), image=self.OptionState[self.previous_button]["image-pair"][1])
        self.OptionState[self.previous_button]["state"] = "released"
        self.previous_button = None
        return

    def attach_component(self, component, button):
        self.OptionState[button]["component"] = component
    
    def detach_component(self, button):
        self.OptionState[button]["component"] = None

    #Communication 
    def enable(self, extra=None):
        self.frame.grid(**self.current_layout)
        self.reset()
        pass
    

    def disable(self, extra=None):
        self.frame.grid_forget()
        pass

    def handle_request(self, request, extra):
        
        if(request == "enable"):
            self.enable()

        elif(request == "disable"):
            self.disable()

        elif(request == "expand"):
            self.make_transition("expand")
        
        elif(request == "shrink"):
            self.make_transition("shrink")
        pass