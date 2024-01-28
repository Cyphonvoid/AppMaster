import queue

class Type():
    ID = "id"
    NAME = "name"
    STATUS = "status"
    CLASS_NAME = "classname"
    RESTRICTED = True
    REFERENCE = None
    RANK = "rank"
    LABEL = "label"
    ROLE = "role"
    ALL = "all"
    

class ComponentManager():

    GLOBAL_ID = 23000
    UNIQUE_INSTANCES = []
    ALL_INSTANCES = []
    
    @staticmethod
    def create_id():
        ComponentManager.GLOBAL_ID += 4
        return ComponentManager.GLOBAL_ID
    
    
    @staticmethod
    def create_name(id):
        name = "component" + str(id)
        return name
    
    @staticmethod
    def VerifyInstance(_id_, name, obj):
        for instance in ComponentManager.UNIQUE_INSTANCES:
            if instance.global_id == _id_ or instance.name == name:
                obj.restricted = True
                obj.status = 'Disabled'
                obj.name = name
                ComponentManager.ALL_INSTANCES.append(obj)
                return False

        obj.status = 'Active'
        obj.restricted = False
        obj.name = name
        ComponentManager.UNIQUE_INSTANCES.append(obj)
        ComponentManager.ALL_INSTANCES.append(obj)
        return True


    @staticmethod
    def CompatibleProfile(ID, Name):
        for i in range(0, len(ComponentManager.UNIQUE_INSTANCES)):
            if(ComponentManager.UNIQUE_INSTANCES[i].name == Name):
                return False
        
        return True
    
    
    @staticmethod
    def RemoveInstance(type, component):
        if(type=="unique"):
            ComponentManager.UNIQUE_INSTANCES.remove(component)
        
        elif(type=="all"):
            ComponentManager.ALL_INSTANCES.remove(component)
        
        elif(type=="both"):
            ComponentManager.UNIQUE_INSTANCES.remove(component)
            ComponentManager.ALL_INSTANCES.remove(component)
    

    @staticmethod
    def AddInstance(type, component):
        if(type=="unique"):
            ComponentManager.UNIQUE_INSTANCES.append(component)
        
        elif(type=="all"):
            ComponentManager.ALL_INSTANCES.append(component)
        
        elif(type=="both"):
            ComponentManager.UNIQUE_INSTANCES.append(component)
            ComponentManager.ALL_INSTANCES.append(component)
        

    @staticmethod
    def PrintInstances():
        for instance in ComponentManager.ALL_INSTANCES:
            print("\nInstance\n")
            print("ID: ", instance.get_globalid())
            print("Name: ", instance.get_name())
            print("Class: ", instance.get_classname())
            print("Status: ", instance.get_status())
            print("Restricted :", instance.eligible())


    def __init__(self, name=None): 
    
        self.global_id = ComponentManager.create_id()
        self.AppManager = AppManager.GetInstanceReference(0)    
        self.name = name
        self.class_name = None
        self.status = 'Active'
        self.restricted = False
        self.rank = None
        self.label = None
        self.role = None

        if(name==None):self.name = ComponentManager.create_name(self.global_id)
        #Verify profile and disable the object if it doesn't meet the criterion 
        if(ComponentManager.VerifyInstance(self.global_id, self.name, self) == False): return

        #Create a commandbox
        self.last_index = 0
        self.my_command_box = [] 
        self.output_message_and_eventconnection_box = [] 
        
        
        self.add_my_command("enable")
        self.add_my_command("disable")
    

    def configure_event_connection(self, message, towhom):        
        for i in range(len(self.output_message_and_eventconnection_box)):
            if self.output_message_and_eventconnection_box[i][0] == message and self.output_message_and_eventconnection_box[i][1] == towhom:
                return

        self.output_message_and_eventconnection_box.append([message, towhom])


    def deconfigure_event_connection(self, message, towhom):
        for connection in self.output_message_and_eventconnection_box:
            if(connection[0] == message and connection[1] == towhom):
                self.output_message_and_eventconnection_box.remove(connection)
                return
    
    
    def get_connection_message(self, index):
        if (index < 0 or index > len(self.output_message_and_eventconnection_box)-1):
            return
            
        return self.output_message_and_eventconnection_box[index][0] 

      
    def get_message_reciepient(self, index):
        if (index < 0 or index > len(self.output_message_and_eventconnection_box)-1): 
            return
        
        return self.output_message_and_eventconnection_box[index][1] 
        
       
    def add_my_command(self, command):
        #Don't add same command twice
        for i in range(0, len(self.my_command_box)):
            if(self.my_command_box[i] == command):
                return
        
        self.my_command_box.append(command)
        self.last_index=len(self.my_command_box)+1  


    def remove_my_command(self, command):
        #Search for the command and then pop it
        for i in range(0, len(self.my_command_box)):
            if(self.my_command_box[i] == command):
                self.my_command_box.pop(i)
                self.last_index=len(self.my_command_box)-1
    

    def handle_request(self, message, extra_data=None):
        #Override this function in the class inheriting this
        #handles custom requests
        pass
    
    def enable(self):
        #Override this function in the class inheritting this
        #This will enable the component, add your functionality here for enabling for example showing the component on screen
        pass

    def disable(self):
        #Override this function in the class inherriting this
        #This will disable the component, add your functionality here, for example  erasing the component on screen
        pass
    

    def set_name(self, name):
        if(len(ComponentManager.UNIQUE_INSTANCES) > 0): ComponentManager.RemoveInstance("both", self)
        return ComponentManager.VerifyInstance(self.global_id, name, self)
   
    def get_name(self):
        return self.name

    def set_classname(self, name):
        self.class_name = name
    
    def get_classname(self, name):
        return self.class_name
    
    def eligible(self):
        #check if component has any secondary restrictions
        if(self.restricted == False): return True
        elif(self.restricted == True): return False

    def get_my_command(self, at):
        if(len(self.my_command_box) == 0): return "No command"
        return self.my_command_box[at]
    
    def print_connections(self, type):
        
        print("My commonds: Commands that other components use to make this component do stuff")
        print("Ouput event connections: consists of 'message' and 'component name'\n")

        if(type == "mycommands"):
            for mycommand in self.my_command_box: 
                print("My command: ", mycommand)
        
        elif(type == "outputconnections"):
            for connection in self.output_message_and_eventconnection_box:
                print("Output Event Connections: ", connection)
        
        pass
    
    def get_component_attribute(self, type):

        if(type == Type.ID):
            return self.global_id
        
        elif(type == Type.NAME):
            return self.name
        
        elif(type == Type.CLASS_NAME):
            return self.class_name
        
        elif(type == Type.RANK):
            return self.rank
        
        elif(type == Type.ROLE):
            return self.role
        
        elif(type == Type.LABEL):
            return self.label
        
        elif(type == Type.STATUS):
            return self.status
        
        elif(type == Type.RESTRICTED):
            return self.restricted
        
        return None
    
    def set_component_attribute(self, type, tovalue):
         
         if(type == Type.NAME):
             self.name = self.set_name(tovalue)
        
         elif(type == Type.CLASS_NAME):
             self.class_name = tovalue
        
         elif(type == Type.RANK):
             self.rank = tovalue
        
         elif(type == Type.ROLE):
             self.role = tovalue
        
         elif(type == Type.LABEL):
             self.label == tovalue
        
         elif(type == Type.STATUS):
             self.status == tovalue
        
         elif(type == Type.RESTRICTED):
             self.restricted == tovalue
        

class AppManager(ComponentManager):
    
    INSTANCES = []

    @staticmethod
    def GetInstanceReference(at):
        if(len(AppManager.INSTANCES)>0):
            return AppManager.INSTANCES[at]
        return None
    
    
    @staticmethod
    def AddInstances(instance):
        AppManager.INSTANCES.append(instance)
        pass

    def __init__(self, dict=None):
        ComponentManager.__init__(self)
        self.global_id = ComponentManager.create_id()
        self.set_classname("AppManager")


        self.registered_components = []
        self.message_queue = queue.Queue()
        self.hashed_registered_components = {}

        self.ranks = [None]
        
        self.register_component(self)
        AppManager.AddInstances(self)

    def component_exists(self, component):
        #Only the manager and higher authority components should be able to call this
        for comp in self.registered_components:
            if(comp.get_component_attribute(Type.ID) == component.get_component_attribute(Type.ID)):
                return comp
        
        return False
    

    def register_component(self, component):
        #Only the manager and higher authority components should be able to call this
        if(self.component_exists(component)!=False):
            print("register_component():   already exists")
            return
        
        if(component.eligible()==True):
               self.registered_components.append(component)
               return
            
        else:
            print("ERROR (Could not register): Component incompatible with ComponentManager Object")
            print("\n\x1b[31mBLOCKED COMPONENT\x1b[0m")
            print("ID: ", component.get_component_attribute(Type.ID))
            print("Name: ", component.get_component_attribute(Type.NAME))
            print("Class: ", component.get_component_attribute(Type.CLASS_NAME))
            print("Status: ", component.get_component_attribute(Type.STATUS))
            print("Restricted :", component.get_component_attribute(Type.RESTRICTED))
            print("Rank :", component.get_component_attribute(Type.RANK))
            
        
    def unregister_component(self, component):
        comp = self.component_exists(component)

        if(comp == False):
            return
        self.registered_components.remove(comp)

    
    def enable_components(self, type=Type.ALL, value=None):
        for match in self.registered_components:
            
            if(type == Type.ALL or value == Type.ALL):
                match.enable()

            elif(value == match.get_component_attribute(type)):
                match.enable()
                if(type == Type.ID or type == Type.NAME):
                    return
            
            pass


    def disable_components(self, type=Type.ALL, value=Type.ALL):
            for match in self.registered_components:
                if(type == Type.ALL or value == Type.ALL):
                    match.disable()

                elif(value == match.get_component_attribute(type)):
                   match.disable()
                   if(type == Type.ID or type == Type.NAME):
                    return
  
    
    def notify_by_name(self, sender_component, message, target_name):
        for i in range(0, len(self.registered_components)):
            if(self.registered_components[i].get_name() == target_name):
                if(self.registered_components[i] != sender_component):
                    self.registered_components[i].handle_request(message, sender_component)  
                    print("[\x1b[32mSystem direct message - Connected\x1b[0m]  from: '"+sender_component.get_name() + "'    message: '\x1b[33m", message, "\x1b[0m'   To Target component: \x1b[33m", target_name, end="")
                    print(" \x1b[35m  notify_Type_name()\x1b[0m")
                    return True
                
        print("[\x1b[31mSystem direct message - Disconnected\x1b[0m]  from: '"+sender_component.get_name() + "'    message: '\x1b[33m", message, "\x1b[0m'  To Target component: \x1b[33m" + target_name, end="")
        print("\x1b[35m  notify_Type_name()\x1b[0m")
        return False
   
   
    def broadcast_message(self, sender, message, extra_data=None):
        for i in range(0, len(self.registered_components)):
                if(self.registered_components[i] != sender):
                    self.registered_components[i].handle_request(message, extra_data)
                    print("[\x1b[34mSystem broadcast - sent connection\x1b[0m]  from: '"+sender.get_name() + "'    message: '\x1b[33m" + message +"\x1b[0m'",  end="")
                    print("    To reciever component: \x1b[33m"+self.registered_components[i].get_name()+"\x1b[0m", end="")
                    print(" \x1b[36m  broadcast_message()\x1b[0m")
        

    def configure_ranks(self, ranks):
        for i in range(0, len(ranks)):
            self.ranks.append(ranks[i])
    

    def remove_ranks(self, rank):
        self.ranks.remove(rank)


    def PrintComponents(self):
        for instance in self.registered_components:
            print("\nInstance\n")
            print("ID: ", instance.get_globalid())
            print("Name: ", instance.get_name())
            print("Class: ", instance.get_classname())
            print("Status: ", instance.get_status())
            print("Restricted :", instance.get_restriction())
            print("Rank :", instance.get_rank())
   

    def notify_components(self, type, message, target_component, sender):
        Notified = False
        for match in self.registered_components:
            if(type == Type.NAME or type == Type.ID):
                if(match.get_component_attribute(type) == target_component):
                    match.handle_request(message, sender)
                    print("[\x1b[32mSystem direct message - Connected\x1b[0m]  from: '"+sender.get_name() + "'    message: '\x1b[33m", message, "\x1b[0m'   To Target component: \x1b[33m", match.get_component_attribute(type), end="")
                    print(" \x1b[35m  notify_Type_name()\x1b[0m")
                    return True
            
            else:
                if(match.get_component_attribute(type) == target_component):
                    match.handle_request(message, sender)
                    print("[\x1b[32mSystem direct message - Connected\x1b[0m]  from: '"+sender.get_name() + "'    message: '\x1b[33m", message, "\x1b[0m'   To Target component: \x1b[33m", match.get_component_attribute(type), end="")
                    print(" \x1b[35m  notify_Type_name()\x1b[0m")
                    Notified = True

        
        print("[\x1b[31mSystem direct message - Couldn't connect\x1b[0m]  from: '"+sender.get_name() + "'    message: '\x1b[33m", message, "\x1b[0m'   To Target component: \x1b[33m", match.get_component_attribute(type), end="")
        print(" \x1b[35m  notify_Type_name()\x1b[0m")
        return Notified
        

    def find_components(self, type, attribute_value):
        components = []
        for match in self.registered_components:

            if(attribute_value == match.get_component_data(Type)):
                components.append(match)
                if(type == Type.ID or type == Type.NAME):
                    return True
        
        return components
    

    def push_to_message_queue(self, sender_name, message, target_component_attribute):
        self.message_queue.put([sender_name, message, target_component_attribute])
        return [sender_name, message, target_component_attribute]
    
    def get_from_message_queue(self):
        return self.message_queue.get()
        pass


    def Register_component(self, component):

        if(component.eligible() == True):
            id = component.get_component_attribute(Type.ID)
            self.hashed_registered_components[id]
            pass
        pass
        
    def display_message_queue(self):
        print("\x1b[35mSystem Manager Component's Message Queue\x1b[0m")
        for messages in self.message_queue:
            print(messages)
        
    
    def process_message_queue(self):
        pass

    def handle_request(self, message, extra_data=None):
        pass
    
    
#Instance initialized  here
#SystemManager = AppManager()
#SystemManager.set_name("System Manager")