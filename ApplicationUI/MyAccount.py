from System import *
import customtkinter



class Field():

    def __init__(self, parent, **attributes):
        

        self.FRAME_LAYOUT = {
            "width":580,
            "height":140,
            "bg_color":"transparent",
            "fg_color":"black",
            "corner_radius":10,
            "border_width":0.6,
            "border_color":"#333333"
        }

        self.TITLE_LAYOUT = {
            "bg_color":"transparent",
            "fg_color":"transparent",
            "font":("Arial", 14, "normal"),
            "text_color":"white",
            "text":"Title"
        }
        
        self.FIELD_LAYOUT = {
            "width":300, 
            "height":26, 
            "bg_color":"transparent",
            "fg_color":"transparent",
            "border_color":"black",
            "placeholder_text_color":"grey",
            "placeholder_text":"Enter your credential to change"
        }

        self.BUTTON_LAYOUT = {
            "width":70,
            "height":33,
            "bg_color":"transparent",
            "fg_color":"#D51989",
            "text":"Submit",
            "text_color":"White",
            "corner_radius":24,
            "hover_color":"#980E87"
        }
        
        self.FIELD_LINE_LAYOUT = {
            "width":300,
            "height":2.5,
            "bg_color":"transparent",
            "fg_color":"#D51989",
            "text":"",
            "hover":False,
            "corner_radius":2
        }
        
        self.MESSAGE_BOX_LAYOUT = {
            "width":250, 
            "height":20, 
            "bg_color":"transparent",
            "fg_color":"transparent"
        }

        self.parent = parent
        self.attributes = {**attributes}
        self.title = "Title"
        self._placement_manager = None
        self._callback = None
        self._input_data = None
        self._placeholder_text = None
       
       

        self.frame = customtkinter.CTkFrame(master=self.parent, **self.FRAME_LAYOUT)
        self.frame.grid(**self.attributes)
        self.frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame.grid_propagate(False)

        self.page_title = customtkinter.CTkLabel(master=self.frame, **self.TITLE_LAYOUT)
        self.page_title.grid(row=0, column=0, sticky="w", padx=35)

        self.field = customtkinter.CTkEntry(master=self.frame, **self.FIELD_LAYOUT)
        self.field.grid(row=1, column=0, sticky="ws", padx=35)


        self.field_line = customtkinter.CTkButton(master=self.frame, **self.FIELD_LINE_LAYOUT)
        self.field_line.grid(row=2, column=0, sticky="wn", padx=35)

        self.submit_button = customtkinter.CTkButton(master=self.frame, **self.BUTTON_LAYOUT, command=self.onclick_submit)
        self.submit_button.grid(row=1, rowspan=2, column=2, sticky="e", padx=40, pady=7)

        self.message_box = customtkinter.CTkLabel(master=self.frame, **self.MESSAGE_BOX_LAYOUT)
        self.message_box.grid(row=3, column=0, columnspan=3, sticky="w", padx=35)
        pass

    def set_title(self, title):
        self.title = title
        self.page_title.configure(text=self.title)
        return self
    
    def set_placeholder(self, _text):
        self.field.configure(placeholder_text=_text, placeholder_text_color="grey")
        self._placeholder_text = _text
        return self
    
    def set_message(self, _text, clr="White"):
        self.message_box.configure(text=_text, text_color=clr)
        pass
    
    def set_callback(self, call):
        self._callback = call
    
    def get_data(self):
        return self._input_data
    
    def get_title(self):
        return self.title

    def onclick_submit(self):

        if(self._callback == None):
            print("My Account.py line 125 Callback not set")
            return
        
        self._input_data = self.field.get()
        self.submit_button.configure(state="disabled")
       
        data = {
            'data':self._input_data,
            'title':self.get_title()
        }
        
        self._callback(data)
        pass
    

    def show(self):
        self.field.configure(placeholder_text=self._placeholder_text, state="normal")
        self.set_message("")
        #self.frame.configure(**self.FRAME_LAYOUT)
        #self.frame.grid(**self.attributes)
        pass

    def hide(self):
        self.field.delete(0, customtkinter.END)
        self.field.configure(placeholder_text=self._placeholder_text, state="disabled")
        self.set_message("")
        #self.frame.grid_forget()
        pass


    def process_input(self, data):
        self.set_message(data['message'], data['color'])
        self.submit_button.configure(state="normal")
        pass
    pass



class MyAccountPage(ComponentManager):


    def __init__(self, parent, **arguments):
        ComponentManager.__init__(self)
        self.set_attribute(Type.CLASS_NAME, "MyAccountPage")

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
            "text":"My Account"
        }

        self.frame = customtkinter.CTkFrame(master=self.parent, **self.FRAME_LAYOUT)
        self.frame.grid(**self.arguments)
        self.frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=2)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.frame.grid_propagate(False)

        self.page_title = customtkinter.CTkLabel(master=self.frame, **self.TITLE_LAYOUT)
        self.page_title.grid(row=0, column=0, sticky="w", padx=35)

        self.change_email = Field(self.frame, row=1, column=0,  columnspan=7, sticky="w", padx=35).set_title("Change email").set_placeholder("Enter your email to change")
        self.change_email.set_callback(self.onclick_option)

        self.change_password = Field(self.frame, row=2, column=0,  columnspan=7, sticky="w", padx=35).set_title("Change password").set_placeholder("Enter your password to change")
        self.change_password.set_callback(self.onclick_option)

        self.change_username = Field(self.frame, row=3, column=0, columnspan=7, sticky="w", padx=35).set_title("Change username").set_placeholder("Enter your username to change")
        self.change_username.set_callback(self.onclick_option)
        pass
    
    

    def onclick_option(self, option_data):
        
        name = self.get_attribute(Type.NAME)
        
        
        component = {
            'name':name
        }
        
        credentials = None
        request = None
        if(option_data['title'] == "Change email"):
            credentials = {
                'email':option_data['data']
            }
            request = 'updateemail'
        

        elif(option_data['title'] == "Change password"):
            credentials = {
                'password':option_data['data']
            }
            request = 'updatepassword'
        
        elif(option_data['title'] == "Change username"):
            credentials = {
                'username':option_data['data']
            }
            request = 'updateusername'

        data = {
            'sender':component,
            'credentials':credentials
        }
        

        self_name = self.get_attribute(Type.NAME)
        SystemManager.notify_components(Type.NAME, request, "UserSession", self_name, data)
        pass


    def enable(self, extra=None):
        self.frame.grid(**self.arguments)
        self.change_email.show()
        self.change_password.show()
        self.change_username.show()
        pass

    def disable(self, extra=None):
        self.frame.grid_forget()
        self.change_email.hide()
        self.change_password.hide()
        self.change_username.hide()
        pass
    

    def handle_request(self, request, extra):
        if(request == "enable"):
            self.enable()

        elif(request == "disable"):
            self.disable()
        

        elif(request == "recieve_backend_data"):

            if(extra['responsefor'] == 'updateemail'):

                if(extra['fullfilled'] == False):
                    data = {
                        'message':extra['message'],
                        'color':"red"
                    }
                    #self.change_email.set_message(extra['message'], "red")
                    self.change_email.process_input(data)
                    print("Change email FAILED")
                

                elif(extra['fullfilled'] == True):
                    print("Change email WORKED")
                    data = {
                        'message':extra['message'],
                        'color':"White"
                    }
                    #self.change_email.set_message(extra['message'])
                    self.change_email.process_input(data)
                    
                pass
            
            

            elif(extra['responsefor'] == 'updatepassword'):
                if(extra['fullfilled'] == False):
                    data = {
                        'message':extra['message'],
                        'color':"red"
                    }
                    #self.change_email.set_message(extra['message'], "red")
                    self.change_password.process_input(data)
                    print("Change password FAILED")
                

                elif(extra['fullfilled'] == True):
                    print("Change password WORKED")
                    data = {
                        'message':extra['message'],
                        'color':"White"
                    }
                    #self.change_email.set_message(extra['message'])
                    self.change_password.process_input(data)
                    
                pass


            elif(extra['responsefor'] == 'updateusername'):
                if(extra['fullfilled'] == False):
                    data = {
                        'message':extra['message'],
                        'color':"red"
                    }
                    #self.change_email.set_message(extra['message'], "red")
                    self.change_username.process_input(data)
                    print("Change username FAILED")
                

                elif(extra['fullfilled'] == True):
                    print("Change username WORKED")
                    data = {
                        'message':extra['message'],
                        'color':"White"
                    }
                    #self.change_email.set_message(extra['message'])
                    self.change_username.process_input(data)
                    
                pass
                pass


        pass

    pass