from System import *
import customtkinter
from .DesignStyles import *
from .Utility import *
from PIL import Image, ImageTk



class LoginForm(ComponentManager):

    def __init__(self, parent):
        # Super class
        ComponentManager.__init__(self)
        self.set_attribute(Type.CLASS_NAME, "LoginForm")

        self.parent = parent
        self._username = None
        self._password = None
        self._remember_me = False
        self._width = 350
        self._height = 470

        self.login_socket = Socket()
        self.enable_socket = Socket()
        self.on_register_socket = Socket()
        self.sign_in_event = None
        self.login_object = None
        # Create a login form
        self.frame = customtkinter.CTkFrame(parent, **LOGIN_FRAME_LAYOUT)
        self.frame.configure(width=self._width, height=self._height)

        
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.frame.pack(expand=True)
        self.frame.grid_propagate(False)
        self.frame.pack_propagate(False)

        # Create logo for form
        # self.app_logo = customtkinter.CTkLabel(master=self.frame, text="", image=self.logo)
        # self.app_logo.grid(column = 1, row=2, sticky="w")

        # Create label for text
        self.form_text = customtkinter.CTkLabel(master=self.frame, text="Welcome,\nsign in", **LOGIN_TITLE_TEXT_LAYOUT)
        self.form_text.grid(column=1, row=2)

        # Create username and password text fields
        self.username_field = customtkinter.CTkEntry(master=self.frame, **ENTRY_FIELD_LAYOUT)
        self.username_field.configure(width=260, height=35)
        self.username_field.grid(column=1, row=3)
        self.username_field.grid_propagate(False)
        self.username_field.insert(0, "Username")
        self.username_field.bind("<FocusIn>", self.username_focus)
        self.username_field.bind("<FocusOut>", self.username_focus)

        self.password_field = customtkinter.CTkEntry(master=self.frame, **ENTRY_FIELD_LAYOUT)
        self.password_field.configure(width=260, height=35)
        self.password_field.grid(column=1, row=4)
        self.password_field.grid_propagate(False)
        self.password_field.bind("<FocusIn>", self.password_focus)
        self.password_field.bind("<FocusOut>", self.password_focus)
        self.password_field.insert(0, "Password")

        # Create a check box
        self.save_info = customtkinter.CTkCheckBox(master=self.frame, fg_color=LOGIN_SECONDARY_COLOR, checkmark_color=LOGIN_PRIMARY_COLOR, hover=False, text="Remember my info")
        self.save_info.configure(border_color=LOGIN_SECONDARY_COLOR)
        self.save_info.grid(column=1, row=5)

        # Create a login button
        self.login = customtkinter.CTkButton(master=self.frame, **LOGIN_BUTTON_LAYOUT)
        self.login.configure(width=260, height=40, text="Sign In", command=self.click_login)
        self.login.grid(column=1, row=6)

        # Create a warning message if login are incorrect
        self.warning_text = customtkinter.CTkLabel(master=self.frame, fg_color=LOGIN_PRIMARY_COLOR, bg_color=LOGIN_PRIMARY_COLOR, text="")
        self.warning_text.grid(column=1, row=7)

        # Create a create account option
        self.create_account = customtkinter.CTkButton(master=self.frame, fg_color=LOGIN_PRIMARY_COLOR, bg_color=LOGIN_PRIMARY_COLOR, text="Don't have an account? Register", hover_color=LOGIN_PRIMARY_COLOR, font=("Arial", 14))
        self.create_account.configure(height=2, corner_radius=14)
        self.create_account.grid(column=1, row=8)
        self.create_account.bind("<Enter>", self.register_acc_enter)
        self.create_account.bind("<Leave>", self.register_acc_leave)
        self.create_account.bind("<Button-1>", self.onclick_register)
        self.create_account.bind("<ButtonRelease-1>", self.register_acc_enter)
 
    def onclick_register(self, event):
        self.create_account.configure(text_color="#05EAEB")
        self.on_register_socket.run_commands()
    # self.create_account.configure(text_color=LOGIN_SECONDARY_COLOR)
    

    def set_message(self, msg, clr="White"):
        self.warning_text.configure(text=msg, text_color=clr)
        pass


    def onclick_signin_user(self):
        return self.login_object.SignIn(email=self.get_username(), password=self.get_password())
        pass


    def register_acc_enter(self, event):
        self.create_account.configure(text_color=LOGIN_SECONDARY_COLOR)
        pass


    def register_acc_leave(self, event):
        self.create_account.configure(text_color="white")
        pass


    def username_focus(self, event):

        if (event.widget.focus_get() == event.widget):
            _input = self.username_field.get()

            if (_input == "Username"):
                self.username_field.delete(0, customtkinter.END)

        else:
            _input = self.username_field.get()
            if (_input == ""):
                self.username_field.insert(0, "Username")

        pass

    def password_focus(self, event):

        if (event.widget.focus_get() == event.widget):
            _input = self.password_field.get()
            if (_input == "Password"):
                self.password_field.delete(0, customtkinter.END)
        # print("\x1b[31mFOCUS IN\x1b[0m")

        else:
            _input = self.password_field.get()
            if (_input == ""):
                self.password_field.insert(0, "Password")

        # print("\x1b[36mOUTSIDE\x1b[0m",  "type = ")
        pass


    def check_fields(self):
        approve = True
        if (self.username_field.get() == "" or self.username_field.get() == "Username"):
            self.warning_text.configure(text="Fields must be valid credentials", text_color="red")
            approve = False

        if (self.password_field.get() == "" or self.password_field.get() == "Password"):
            self.warning_text.configure(text="Fields must be valid credentials", text_color="red")
            approve = False


        else:
            self.warning_text.configure(text="")
            approve = True

        return approve

    
    def approve_signin(self):

        if (self.username_field.get() == "yashaswi" and self.password_field.get() == "jaedon"):
            self.warning_text.configure(text="")
            return True

        else:
            self.warning_text.configure(text="Login credentials are incorrect", text_color="red")
            return False
    

    def click_login(self):
        self._username = self.username_field.get()
        self._password = self.password_field.get()
        self._remember_me = self.save_info.get()
        print("Username: ", "["+self._username+"]", "   Password: ", "["+self._password+"] len:", len(self._password), " save: ", self._remember_me)

        # Make some backend call here to verify
        """if(self.check_fields() == True):
            if(self.approve_signin() == True):
                self.login._state = 'disabled'
                self.login.configure(fg_color="#980E87")
                time.sleep(2)
                SystemManager.broadcast_message(self, "disable")
                self.disable()
                SystemManager.notify_components(Type.NAME, self.get_connection_message(0), self.get_message_reciepient(0), self)
                return

        else:
            pass
        """
        
        name = self.get_attribute(Type.NAME)

        component = {
            'name':name
        }
        

        credentials = {
            'email':self._username,
            'password':self._password
        }

        data = {
            'sender':component,
            'credentials':credentials
        }

        SystemManager.notify_components(Type.NAME, "signin", "UserSession", name, data)
        #self.login_socket.run_commands()

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def get_save_info(self):
        return self._remember_me
    
    def get_height(self):
        return self._height
    
    def get_width(self):
        return self._width
    

    def set_width(self, width):
         self._width = width
         self.frame.configure(width=self._width)

    def set_height(self, height):
        self._height = height
        self.frame.configure(height=self._height)

    def enable(self, extra=None):
        self.set_message("Enter your credentials")
        self.login._state = "normal"
        self.login.configure(fg_color=LOGIN_SECONDARY_COLOR, text_color=LOGIN_PRIMARY_COLOR, font=("Roboto", 15, "bold"))
        self.username_field.delete(0, customtkinter.END)
        self.password_field.delete(0, customtkinter.END)
        self.username_field.insert(0, "Username")
        self.password_field.insert(0, "Password")
        self.frame.pack(expand=True)
        self.enable_socket.run_commands()
        pass

    def disable(self, extra=None):
        self.set_message("")
        self.username_field.delete(0, customtkinter.END)
        self.password_field.delete(0, customtkinter.END)
        self.frame.pack_forget()
        pass

    def handle_request(self, request, extra):

        if(request == "disable"):
            self.disable()

        elif(request == "enable"):
            self.enable()

        elif(request == "takethis"):
            self.login_object = extra
            #self.login_object.SignIn("yashaswi.kul@gmail.com", "yash18hema06")
        
        elif(request == "recieve_backend_data"):

            if(extra['responsefor'] == 'signin'):

                if(extra['fullfilled'] == False):
                    self.set_message(extra['message'], "red")
                
                elif(extra['fullfilled'] == True):
                    self.set_message(extra['message'])
                    self.login_socket.run_commands()
        


            pass
        pass







class RegistrationForm(ComponentManager):
    def __init__(self, parent):
        # Super class
        ComponentManager.__init__(self)
        self.set_attribute(Type.CLASS_NAME, "RegistrationForm")

        self.parent = parent
        self._username = None
        self._password = None
        self._email = None
        self._width = 350
        self._height = 470
        
        self.register_callback = None
        self.register_socket = Socket()
        self.enable_socket = Socket()
        self.disable_socket = Socket()
        self.go_back_socket = Socket()

        # Create a Registration form
        self.frame = customtkinter.CTkFrame(parent, **LOGIN_FRAME_LAYOUT)
        self.frame.configure(width=self._width, height=self._height)

        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.frame.pack(expand=True)
        self.frame.grid_propagate(False)
        self.frame.pack_propagate(False)


        #TITLE OF REGISTRATION FORM
        self.form_text = customtkinter.CTkLabel(master=self.frame, text="Registration", **LOGIN_TITLE_TEXT_LAYOUT)
        self.form_text.grid(column=1, row=2)
        
        
        #BACK BUTTON
        self.back_button = customtkinter.CTkButton(master=self.frame, text="Back", corner_radius=30, text_color="#D51989", font=("Arial", 15, "bold"))
        self.back_button.configure(width=250, height=40, border_width=2, border_color = "#D51989", bg_color="transparent", fg_color="transparent", hover_color="#05EAEB")
        self.back_button.grid(column=1, row=7)

        #EMAIL TEXT FIELD
        self.email_field = customtkinter.CTkEntry(master=self.frame, **ENTRY_FIELD_LAYOUT)
        self.email_field.configure(width=260, height=35)
        self.email_field.grid(column=1, row=3)
        self.email_field.grid_propagate(False)
        self.email_field.insert(0, "Email")
        self.email_field.bind("<FocusIn>", self.email_focus)
        self.email_field.bind("<FocusOut>", self.email_focus)

        #USERNAME FIELD
        self.username_field = customtkinter.CTkEntry(master=self.frame, **ENTRY_FIELD_LAYOUT)
        self.username_field.configure(width=260, height=35)
        self.username_field.grid(column=1, row=4)
        self.username_field.grid_propagate(False)
        self.username_field.insert(0, "New username")
        self.username_field.bind("<FocusIn>", self.username_focus)
        self.username_field.bind("<FocusOut>", self.username_focus)
        

        #PASSWORD FIELD
        self.password_field = customtkinter.CTkEntry(master=self.frame, **ENTRY_FIELD_LAYOUT)
        self.password_field.configure(width=260, height=35)
        self.password_field.grid(column=1, row=5)
        self.password_field.grid_propagate(False)
        self.password_field.bind("<FocusIn>", self.password_focus)
        self.password_field.bind("<FocusOut>", self.password_focus)
        self.password_field.insert(0, "New password")

        #SIGN UP BUTTON
        self.register_button = customtkinter.CTkButton(master=self.frame, **LOGIN_BUTTON_LAYOUT)
        self.register_button.configure(width=250, height=40, text="Submit", command=self.click_create)
        self.register_button.grid(column=1, row=6)
        
        #WARNING MESSAGE
        self.warning_text = customtkinter.CTkLabel(master=self.frame, fg_color=LOGIN_PRIMARY_COLOR, bg_color=LOGIN_PRIMARY_COLOR, text="")
        self.warning_text.grid(column=1, row=8)

        
    def set_width(self, width):
        self._width = width
        self.frame.configure(width=self._width)

    def set_height(self, height):
        self._height = height
        self.frame.configure(height=self._height)

    def username_focus(self, event):

        if(event.widget.focus_get() == event.widget):
            _input = self.username_field.get()
           
            if (_input == "New username"):
                self.username_field.delete(0, customtkinter.END)

        else:
            _input = self.username_field.get()
            if (_input == ""):
                self.username_field.insert(0, "New username")

        pass

    def password_focus(self, event):

        if(event.widget.focus_get() == event.widget):
            _input = self.password_field.get()
          
            if (_input == "New password"):
                self.password_field.delete(0, customtkinter.END)
                # print("\x1b[31mFOCUS IN\x1b[0m")

        else:
            _input = self.password_field.get()
            if (_input == ""):
                self.password_field.insert(0, "New password")

             # print("\x1b[36mOUTSIDE\x1b[0m",  "type = ")
        pass

    def email_focus(self, event):
        if(event.widget.focus_get() == event.widget):
            _input = self.email_field.get()
           
            if (_input == "Email"):
                self.email_field.delete(0, customtkinter.END)
            # print("\x1b[31mFOCUS IN\x1b[0m")

        else:
            _input = self.email_field.get()
            if (_input == ""):
                self.email_field.insert(0, "Email")

            # print("\x1b[36mOUTSIDE\x1b[0m",  "type = ")
        pass
    

    def get_username(self):
        return self._username
    
    def get_password(self):
        return self._password
    
    def get_email(self):
        return self._email
    
    def set_message(self, msg, clr="White"):
        self.warning_text.configure(text=msg, text_color=clr)
        pass

    def click_create(self):
        self._username = self.username_field.get()
        self._password = self.password_field.get()
        self._email = self.email_field.get()
        print("Username: ", "["+self._username+"]", "   Password: ", "["+self.get_password()+"]", " email: ", "["+self.get_username()+"]")
        
        #if(self.register_callback.SignUp(email=self.get_email(), password=self.get_password()) == True):
        #    self.register_socket.run_commands()
        #    self.set_message("Account successfully registered!", "green")
        #else:
        #    self.set_message("Couldn't register, credentials not valid", "red")
        #    pass
        
        name = self.get_attribute(Type.NAME)

        component = {
            'name':name
        }
        
        credentials = {
            'email':self._email,
            'password':self._password,
            'display_name':self._username
        }

        data = {
            'sender':component,
            'credentials':credentials
        }
        
        SystemManager.notify_components(Type.NAME, "signup", "UserSession", name, data)
   
    def attach_to_back(self, component):
        self.back_button.configure(command=lambda: SystemManager.enable_components(Type.NAME, component.get_attribute(Type.NAME), self))

        pass
    def enable(self, extra=None):
        self.register_button._state = "normal"
        self.register_button.configure(fg_color=LOGIN_SECONDARY_COLOR, text_color=LOGIN_PRIMARY_COLOR, font=("Roboto", 15, "bold"))

        self.email_field.delete(0, customtkinter.END)
        self.username_field.delete(0, customtkinter.END)
        self.password_field.delete(0, customtkinter.END)

        self.email_field.insert(0, "Email")
        self.username_field.insert(0, "New username")
        self.password_field.insert(0, "New password")
        self.frame.pack(expand=True)
        self.enable_socket.run_commands()
        pass

    def disable(self, extra=None):
        self.username_field.delete(0, customtkinter.END)
        self.password_field.delete(0, customtkinter.END)
        self.email_field.delete(0, customtkinter.END)
        self.frame.pack_forget()
        pass


    def handle_request(self, request, extra):

        if (request == "disable"):
            self.disable()


        elif (request == "enable"):
            self.enable()

        elif(request == "takethis"):
            self.register_callback = extra
            pass

        elif(request == "recieve_backend_data"):

            if(extra['responsefor'] == 'signup'):

                if(extra['fullfilled'] == False):
                    self.set_message(extra['message'], "red")
                    print("signup FAILED")
                
                elif(extra['fullfilled'] == True):
                    self.register_socket.run_commands()
                    print("signup WORKED")
                    self.set_message(extra['message'])
                    
                pass
            pass
        pass
    

    pass