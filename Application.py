from System import *
from ApplicationUI import *
from Games.Sudoku.SudokuGame import *
from Backend import *

class Application:
    CLASS_OBJECT_ID = 1000

    @staticmethod
    def assign_classlevel_id():
        Application.CLASS_OBJECT_ID += 3
        return Application.CLASS_OBJECT_ID

    def __init__(self):
        self.ID = Application.assign_classlevel_id()
        
        self.ApplicationUI = SystemUI(1300, 900)
        self.sidebar = SideBar(self.ApplicationUI, row=0, column=0, sticky="nsw", rowspan=3, ipadx=15) 
        self.loginform = LoginForm(self.ApplicationUI)
        self.registerform = RegistrationForm(self.ApplicationUI)
        self.MainMenu = GameSelector(self.ApplicationUI, padx=10, pady=10, row=0, column=1, sticky="nsew", rowspan=3, columnspan=3)
        self.HomePage = HomePage(self.ApplicationUI, row=0, column=1, sticky="nsew", rowspan=3, columnspan=3)
        self.Settings = Settings(self.ApplicationUI, row=0, column=1, sticky="nsew", rowspan=3, columnspan=3)
        self.AboutUs = AboutUs(self.ApplicationUI, row=0, column=1, sticky="nsew", rowspan=3, columnspan=3)
        self.MyAccountPage = MyAccountPage(self.ApplicationUI, row=0, column=1, sticky="nsew", rowspan=3, columnspan=3)
        self.ClientSession = ClientSession()
        
        
        SystemManager.register_components(self.ApplicationUI, self.loginform, self.Settings, self.MainMenu) 
        SystemManager.register_components(self.sidebar, self.registerform, self.HomePage, self.AboutUs)
        SystemManager.register_components(self.ClientSession, self.MyAccountPage)

        
        self.ApplicationUI.add_component(self.sidebar, self.loginform, self.MainMenu, self.registerform)
        self.ApplicationUI.add_component(self.HomePage, self.Settings, self.AboutUs, self.MyAccountPage)
        self.ApplicationUI.add_component(self.ClientSession)
    

    def CheckFilePaths(self):
        pass
    

    def InitiateCore(self):
        pass


    def CheckDependencies(self):
        pass
    

    def setup(self):
       

        #NOTE APPLICATION UI
        self.ApplicationUI.set_attribute(Type.NAME, "AppUIComponent")
        self.ApplicationUI.set_attribute(Type.LABEL, "master")


        #NOTE SIDEBAR
        self.sidebar.set_attribute(Type.NAME, "sidebar")
        self.sidebar.set_attribute(Type.LABEL, "slave")
        #Connection.function(self.ApplicationUI.quit).inject_into(self.sidebar.button_socket[5])
         


        #NOTE LOGIN FORM          
        self.loginform.set_attribute(Type.NAME, "loginform")
        self.loginform.set_attribute(Type.LABEL, "slave")
        payload = (self.loginform.get_width()+80, self.loginform.get_height()+80)
        Connection.notify(Type.LABEL, "disable", "slave", "loginform").inject_into(self.loginform.enable_socket)
        Connection.notify(Type.NAME, "resize", "AppUIComponent", self.loginform, payload).inject_into(self.loginform.enable_socket)
        #On click register connections
        Connection.enable(Type.NAME, "registerform", "loginform").inject_into(self.loginform.on_register_socket)
        Connection.disable(Type.NAME, "loginform", "loginform").inject_into(self.loginform.on_register_socket)
        #Login connections
        Connection.notify(Type.NAME, "restoredefault", "AppUIComponent", "loginform").inject_into(self.loginform.login_socket)
        #Connection.notify(Type.NAME, "center", "AppUIComponent", "loginform").inject_into(self.loginform.login_socket)
        Connection.enable(Type.NAME, "sidebar", self.loginform).inject_into(self.loginform.login_socket)
        Connection.disable(Type.NAME, self.loginform.get_name(), "loginform").inject_into(self.loginform.login_socket)  
        

        
        #NOTE REGISTER FORM
        self.registerform.set_attribute(Type.NAME, "registerform")
        self.registerform.set_attribute(Type.LABEL, "slave")
        self.registerform.attach_to_back(self.loginform)
        payload = (self.loginform.get_width()+80, self.loginform.get_height()+80)
        #Connection.notify(Type.LABEL, "disable", "slave", "registerform").inject_into(self.registerform.enable_socket)
        #Connection.notify(Type.NAME, "resize", "AppUIComponent", self.loginform, payload).inject_into(self.registerform.enable_socket)
        #Connection.notify(Type.NAME, "restoredefault", "AppUIComponent", "registerform").inject_into(self.registerform.register_socket)
        #Connection.enable(Type.NAME, "sidebar", self.loginform).inject_into(self.registerform.register_socket)
        Connection.disable(Type.NAME, "registerform", "registerform").inject_into(self.registerform.register_socket) 
        Connection.enable(Type.NAME, "loginform", "registerform").inject_into(self.registerform.register_socket)
        
        
        
        #NOTE MAIN MENU 
        self.MainMenu.set_attribute(Type.NAME, "MainMenu")
        self.MainMenu.set_attribute(Type.ROLE, "myapps")
        self.MainMenu.set_attribute(Type.LABEL, "slave")



        #NOTE HOME PAGE
        self.HomePage.set_attribute(Type.NAME, "Home")
        self.HomePage.set_attribute(Type.LABEL, "slave")
        

        #NOTE MY ACCOUNT PAGE
        self.MyAccountPage.set_attribute(Type.NAME, "myaccount")
        self.MyAccountPage.set_attribute(Type.LABEL, "slave")


        #NOTE SETTINGS
        self.Settings.set_attribute(Type.NAME, "AppSettings")
        self.Settings.set_attribute(Type.LABEL, "slave")

    
        #NOTE ABOUT US
        self.AboutUs.set_attribute(Type.NAME, "AboutUs")
        self.AboutUs.set_attribute(Type.LABEL, "slave")

        
        #NOTE FIRE CLIENT
        #NOTE DO NOT CHANGE 'UserSession' to any other name, as it has been harcoded in LoginForm.py
        self.ClientSession.set_attribute(Type.NAME, "UserSession")
        self.ClientSession.set_attribute(Type.LABEL, "slave")




        Connection.disable(Type.NAME, self.MainMenu.get_name()).inject_into(self.MainMenu.socketGS)
        #Connection.notify(Type.ROLE, "enable", self.MainMenu.get_game_selected(), self.MainMenu).inject_into(self.MainMenu.socketGS)

        self.sidebar.attach_component(self.MainMenu, "MyApps")
        self.sidebar.attach_component(self.loginform, "Logout")
        self.sidebar.attach_component(self.HomePage, "Home")
        self.sidebar.attach_component(self.Settings, "Settings")
        self.sidebar.attach_component(self.AboutUs, "AboutUs")
        self.sidebar.attach_component(self.MyAccountPage, "MyAccount")
                                                                           
                                                                        
                                                                  
        SystemManager.broadcast_message("SystemManager", "disable")
        SystemManager.enable_components(Type.NAME, "loginform", "SystemManager")
        #SystemManager.notify_components(Type.NAME, "takethis", "loginform", "SystemManager")
        #SystemManager.notify_components(Type.NAME, "takethis", "registerform", "SystemManager")
        #self.sidebar.notify_components(Type.NAME, "run", "fireclient")
        

    def run(self):
        self.setup()
        self.ApplicationUI.launch()

        
app = Application()
app.run()
