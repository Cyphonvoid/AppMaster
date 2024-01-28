import queue
import json
import time

class Type:
    ID = "id"
    NAME = "name"  
    CLASS_NAME = "classname"
    RANK = "rank"
    LABEL = "label"
    ROLE = "role"
    RESTRICTED = "restricted"
    ALL = "all"
    
    COMMAND = "command"
    STATUS = "status"
    REFERENCE = "reference"
    ARGS = "arguments"
    TYPES = [ID, NAME, CLASS_NAME, RANK, LABEL, ROLE, RESTRICTED, ALL, STATUS] 

class ComponentManager():
    GLOBAL_ID = 23000
    UNIQUE_INSTANCES = []
    ALL_INSTANCES = []
    SystemManager = None
    IDENTIFIER_DATA = {
        'unique':['id', 'name'],
        'common':['classname','rank', 'label', 'role', 'status', 'restricted']
    }
    
    @staticmethod
    def GetIdentifierData(type):
        if(type == 'unique'):
            return ComponentManager.IDENTIFIER_DATA[type]
        
        elif(type == 'common'):
            return ComponentManager.IDENTIFIER_DATA[type]
        
        return
    

    @staticmethod
    def ConfigureMasterManager(value):
        ComponentManager.SystemManager = value

    
    @staticmethod
    def GetMasterManager():
        return ComponentManager.SystemManager
    

    @staticmethod
    def GenerateID():
        ComponentManager.GLOBAL_ID += 4
        return ComponentManager.GLOBAL_ID
    

    @staticmethod
    def GenerateName(id):
        name = "component" + str(id)
        return name
    

    @staticmethod
    def VerifyInstance(_id_, name, obj):
        for instance in ComponentManager.UNIQUE_INSTANCES:
            if instance.attributes[Type.ID] == _id_ or instance.attributes[Type.NAME] == name:
                obj.attributes[Type.STATUS] = 'Disabled'
                obj.attributes[Type.RESTRICTED] = True
                obj.attributes[Type.NAME] = name
                ComponentManager.ALL_INSTANCES.append(obj)
                return False
    
        obj.attributes[Type.STATUS] = 'Active'
        obj.attributes[Type.RESTRICTED] = False
        obj.attributes[Type.NAME] = name
        ComponentManager.UNIQUE_INSTANCES.append(obj)
        ComponentManager.ALL_INSTANCES.append(obj)
        return True


    @staticmethod
    def CompatibleProfile(ID, Name): 
        for i in range(0, len(ComponentManager.UNIQUE_INSTANCES)):
            if(ComponentManager.UNIQUE_INSTANCES[i].attributes[Type.NAME] == Name):
                return False
        
        return True
    

    @staticmethod
    def Deauthorize(component):
        component.attributes[Type.STATUS] = 'Disabled'
        component.attributes[Type.RESTRICTED] = True
        component.attributes[Type.ROLE] = None
        component.attributes[Type.LABEL] = None
        
    
    @staticmethod
    def Authorize(component):
        component.attributes[Type.STATUS] = 'Active'
        component.attributes[Type.RESTRICTED] = False

        #NOTE We might not need to reset ROLE and LABEL
        component.attributes[Type.ROLE] = None
        component.attributes[Type.LABEL] = None
    

    @staticmethod
    def InstancePresent(component):

        for instance in ComponentManager.UNIQUE_INSTANCES:
            if(instance == component):
                return True
        
        return False


    @staticmethod
    def VerifyUniqueData(AttributeList):
        #Verify any kind of unique keys of component if they're actually unique or not
        DataList = AttributeList
        unique_keys = ComponentManager.GetIdentifierData('unique')
        for instance in ComponentManager.UNIQUE_INSTANCES:
            #instance_keys = list(instance.attributes.keys())
            for key in unique_keys:

                if(isinstance(AttributeList, list)):
                    if(instance.attributes[key] in DataList):
                        return False
                
                else:
                    if(instance.attributes[key] == DataList):
                        return False

            
                  
        return True
    

    @staticmethod
    def AuthorizationProcess(component, block=True):
        #Will output false component if already existing        
        UniqueKeys = ComponentManager.GetIdentifierData('unique')
        process = None
        component_data = []
        for keys in UniqueKeys:
            component_data.append(component.attributes[keys])
        
        if(ComponentManager.InstancePresent(component) == True):
            print("[Authorization process :] Already Authorized:   Location: UNIQUE_INSTANCES = [],  Unique Data:=", component_data)
            return True
        
        data_validity = ComponentManager.VerifyUniqueData(component_data)
        
        if(data_validity == False):
            if(block==True): 
                #NOTE Block parameter would Deauthorize (Restrict) component
                ComponentManager.Deauthorize(component)
                pass
            print("[Authorization process :]  FAILED,  Invalid Data:=", component_data)
            process = False
        

        elif(data_validity == True):
            ComponentManager.Authorize(component)
            ComponentManager.UNIQUE_INSTANCES.append(component)
            print("[Authorization process :]  SUCCESS,  Unique Data:=", component_data)
            process = True
            pass
        
        ComponentManager.ALL_INSTANCES.append(component)
        return process
    

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
                print("ID: ", instance.attributes[Type.ID])
                print("Name: ", instance.attributes[Type.NAME])
                print("Class: ", instance.attributes[Type.CLASS_NAME])
                print("Status: ", instance.attributes[Type.STATUS])
                print("Restricted: ", instance.attributes[Type.RESTRICTED])
                print("Role: ", instance.attributes[Type.ROLE])
                print("Label: ", instance.attributes[Type.LABEL])


    def __init__(self):
        _id = ComponentManager.GenerateID()
        _name = ComponentManager.GenerateName(_id)
        self._SystemManager = ComponentManager.GetMasterManager()
        self.attributes = {
            'id':_id,
            'name':_name,
            'classname':None,
            'rank':None,
            'label':None,
            'role':None,
            'status':'Active',
            'restricted':False,
        }
        
        #NOTE To make changes, configure both attributes and identifier data
        #     Then send this data to System Manager class for it's purposes
        #     To reduce hardcoding and promote automating mechanisms
        self._identifier_data = {
            'unique':['id', 'name'],
            'common':['classname','rank', 'label', 'role', 'status', 'restricted']
        }
        
        #if(ComponentManager.AuthorizationProcess(self)==False):return
        if(ComponentManager.VerifyInstance(_id, _name, self)==False):return
        

        self._my_request_inbox = []
        self._event_connections_outbox = []

        self._command = None
        self._command_name = None
        pass
    

    def __del__(self):
        #NOTE DOESN'T WORK
        self._SystemManager.signal_interrupt('remove', self)
        ComponentManager.RemoveInstance("both", self)
        del self
        pass

    
    def set_default_request(self, command):
        self._my_request_inbox.append(command)
    

    def remove_inbox_request(self, command):
        self._my_request_inbox.remove(command)
    

    def configure_event_connection(self, message, towhom):        
        for i in range(len(self._event_connections_outbox)):
            if self._event_connections_outbox[i][0] == message and self._event_connections_outbox[i][1] == towhom:
                return

        self._event_connections_outbox.append([message, towhom])
    

    def deconfigure_event_connection(self, message, towhom):
        for connection in self._event_connections_outbox:
            if(connection[0] == message and connection[1] == towhom):
                self._event_connections_outbox.remove(connection)
                return
    

    def get_connection_message(self, index):
        if (index < 0 or index > len(self._event_connections_outbox)-1):
            return
            
        return self._event_connections_outbox[index][0] 
    

    def get_message_reciepient(self, index):
        if (index < 0 or index > len(self._event_connections_outbox)-1): 
            return
        
        return self._event_connections_outbox[index][1] 
    

    def get_inbox_requests(self, at_index=None):
        if(len(self._my_request_inbox) == 0): return "Inbox Empty"
        
        if(at_index > len(self._my_request_inbox)-1):
            return "Invalid index"
    
        elif(at_index == None):
            return self._my_request_inbox
        
        else:
            return self._my_request_inbox[at_index]
    

    def __set_name(self, name):
        if(ComponentManager.VerifyUniqueData(name)==False):
            return
        if(len(ComponentManager.UNIQUE_INSTANCES) > 0): ComponentManager.RemoveInstance("both", self)
        self.attributes[Type.NAME] = name
        ComponentManager.AuthorizationProcess(self)
        pass
    

    def get_name(self):
        return self.attributes[Type.NAME]
    
     
    def set_classname(self, classname):
        self.attributes[Type.CLASS_NAME] = classname
        pass


    def native_type(self, type):
        return (type in self.attributes.keys())
       

    def get_attribute(self, type):
        return self.attributes[type]


    def print_inbox(self):

        print("name: ", self.attributes[Type.NAME])
        print("ID: ", self.attributes[Type.ID])

        print("INBOX")
        for messages in self._my_request_inbox:
            print("Command/message: ", messages)
    

    def print_outbox(self):
        print("name: ", self.attributes[Type.NAME])
        print("ID: ", self.attributes[Type.ID])
        
        print("OUTBOX")
        for msg, recipient in self._event_connections_outbox:
            print("request: ", msg, "   recipient:", recipient)
    

    def authorized(self):
        if(self.attributes[Type.RESTRICTED]==True):
            return False
        elif(self.attributes[Type.RESTRICTED]==False):
            return True
        pass
    

    def print(self):
        key_list = self.attributes.keys()
        for key in key_list:
            print(key+": ", self.attributes[key])
        

    def set_attribute(self, type, tothis):
        if(self.native_type(type)==False):
            return
        
        if(type == Type.ID):
            return
        
        elif(type == Type.NAME):
            #BUG NOTE,   Modify this each time the attributes dict is changed to something else
            signal = self._SystemManager.signal_interrupt('myregisteration', self)
            
            if(signal == False):
                self.__set_name(tothis)

            elif(signal == True):
                self._SystemManager.signal_interrupt('update', self, Type.NAME, tothis)

        else:
            signal = self._SystemManager.signal_interrupt('myregisteration', self)
            if(signal == False):
               self.attributes[type] = tothis
               pass

            elif(signal == True):
                self._SystemManager.signal_interrupt('update', self, type, tothis)

        pass


    def get_attribute_bundle(self):
        return self.attributes
    

    def get_identifier_data(self, type):
        if(type == 'unique'):
            return self._identifier_data.get(type)
        
        elif(type == 'common'):
            return self._identifier_data.get(type)
        
        else:
            raise ValueError("Invalid type, can only be unique and common")
        
    
    
    def unregister(self):
        self._SystemManager.signal_interrupt('remove', self)
        self._SystemManager = None
        pass

    def register(self, Manager):
        if(self.authorized() == False):
            return
        self._SystemManager = Manager
        self._SystemManager.register_component(self)
        pass
    

    def delete(self):
        del self
        pass
    
    
    def enable_components(self, reciepient, *args):
        if(self.authorized() == False): return
        self._SystemManager.enable_components(Type.NAME, reciepient, self.get_name())
        return 
        pass

    def disable_components(self, sender, *args):
        if(self.authorized() == False): return
        self._SystemManager.disable_components(Type.NAME, sender, self.get_name())
        return 
        pass

    def broadcast_components(self, *args):
        if(self.authorized() == False): return
        self._SystemManager.broadcast_message(self.get_name(), *args)
        return 
        pass

    def notify_components(self, type, message, reciepient, extra=None):
        if(self.authorized() == False): return
        self._SystemManager.notify_components(type, message, reciepient, self.get_name(), extra)
        return 
        

    def remove_from(self, socket):
        pass

    #Component control mechanism members
    def enable(self, extra=None):
        #Add your component's enable functionality
        pass

    def disable(self, extra=None):
        #Add your component's disable functionality
        pass

    def handle_request(self, request, extra):
        #handle any custom requests recieved for any custom behavior or functionality
        pass






#SYSTEM MANAGER CLASS IMPLEMENTATION
class SystemManager():
    
    ALL_INSTANCES = []
    CLASS_LEVEL_ID = 67812

    @staticmethod
    def GenerateID():
        SystemManager.CLASS_LEVEL_ID += 4
        return SystemManager.CLASS_LEVEL_ID
    
    
    @staticmethod
    def GenerateName(id):
        return "MediatorComponent" + str(id)


    @staticmethod
    def GetInstance(index):
        if(len(SystemManager.ALL_INSTANCES) == 0):
            print("SYSTEM MANAGER OBJECT ISN'T DECLARED")
            return None
        
        return SystemManager.ALL_INSTANCES[index]
    

    @staticmethod
    def AddInstance(instance):
        SystemManager.ALL_INSTANCES.append(instance)
    

    @staticmethod
    def PrintInstances():
        
        for instance in SystemManager.ALL_INSTANCES:
            print("Mediator Component:\n")
            print("ID: ", instance._id)
            print("Name: ", instance._name)
        pass


   
    def __init__(self):
        self._id = SystemManager.GenerateID()
        self._name = SystemManager.GenerateName(self._id)

        self._attributes = {
            Type.NAME: SystemManager.GenerateName(self._id),
            Type.ID : SystemManager.GenerateID()
        }
        self.priority_queue = queue.Queue()
        self.request_queue = queue.Queue()

        self.unordered_registered_components = {}
        self.system_unique_group_identifiers = ComponentManager.GetIdentifierData('unique')
        self.system_common_group_identifiers = ComponentManager.GetIdentifierData('common')

        self.ordered_regsitered_components = {
            Type.ID:{},
            Type.NAME:{},
            Type.CLASS_NAME:{},
            Type.LABEL:{},
            Type.ROLE:{},
            Type.RANK:{},
            Type.STATUS:{}
        }

        SystemManager.AddInstance(self)
    

    def component_exists(self, component):
        #NOTE need to rewrite this so that, this can adapt dynamically to component
        #     manaager's changing requirement and needs
        id_keys = self.ordered_regsitered_components[Type.ID].keys()
        name_keys = self.ordered_regsitered_components[Type.NAME].keys()
        
        component_id = component.get_attribute(Type.ID)
        component_name = component.get_attribute(Type.NAME)

        for idkey in id_keys:
            if(component_id == idkey ):
                return True
        
        for namekey in name_keys:
            if(component_name == namekey):
                return True
        
        return False

    
    def register_components(self, *components):

        for component in components:
            self.register_component(component)
            
    def register_component(self, component):

        if(component.authorized() == False):
            print("ERROR (Could not register): Component incompatible with ComponentManager Object")
            print("\n\x1b[31mBLOCKED COMPONENT\x1b[0m")
            print("ID: ", component.get_attribute(Type.ID))
            print("Name: ", component.get_attribute(Type.NAME))
            print("Class: ", component.get_attribute(Type.CLASS_NAME))
            print("Status: ", component.get_attribute(Type.STATUS))
            print("Restricted :", component.get_attribute(Type.RESTRICTED))
            print("Rank :", component.get_attribute(Type.RANK))
            return

        if(self.component_exists(component) == True):
            print("Component exists already")
            return 
        

        #Get the identifier information such as unique key
        unique_group_keys = component.get_identifier_data('unique')
        common_group_keys = component.get_identifier_data('common')
        component_data = component.get_attribute_bundle()
        
        #Register the component in the hashmap for the unique identifiers
        
        #NOTE Doesn't currently handle key errors
        #     To setup the key groups without having to hardcode it inside this class
        #     it needs a seperate block of code to parse key groups and define them 
        #     inside the ordered_registered_components, will be set in some run() method

        key_group_value = None
        for key_group in unique_group_keys:
            key_group_value = component_data[key_group]
            self.ordered_regsitered_components[key_group][key_group_value] = component
            
        #Now register all the commong identifiers
        for key_group in common_group_keys:
            key_group_value = component_data[key_group]

            try:
                #Handle key errors on key_group_values 
                if(key_group_value != None):
                    self.ordered_regsitered_components[key_group][key_group_value].append(component)
            
            except KeyError as missing_key:
                #If the key group is missing
                #NOTE,  need to automate this line
                if(key_group == Type.RESTRICTED):
                    continue
                    pass
               
                if(key_group_value != None):
                        self.ordered_regsitered_components[key_group].setdefault(key_group_value, [])
                        self.ordered_regsitered_components[key_group][key_group_value].append(component)

        
        pass
    

    def unregister_component(self, component):
        
        unique_group_keys = component.get_identifier_data('unique')
        common_group_keys = component.get_identifier_data('common')
        component_data = component.get_attribute_bundle()
        component_key_groups = component_data.keys()
        
        if(self.component_exists(component) == False):
            print("Component doesn't exist to remove")
            return
        
        #Unregistering from the unique key group
        key_group_value = None
        for key_group in unique_group_keys:
            key_group_value = component_data[key_group]

            try:
                if(key_group_value != None):
                    del self.ordered_regsitered_components[key_group][key_group_value]
            except Exception as e:
                continue
                pass
        
        #Unregistering from the common key group
        for key_group in common_group_keys:
            key_group_value = component_data[key_group]

            try:
                if(key_group_value != None):
                    self.ordered_regsitered_components[key_group][key_group_value].remove(component)
                pass
            except Exception as e:
                continue
                
    
    def delete_component(self, type, name):
        if(type != Type.NAME and type != Type.ID): 
            return
        
        component = self.find_component(type, name)
        self.unregister_component(component)
        del component
        pass


    def remove_component(self, component):
        self.unregister_component(component)
        pass
    

    def update_system_component_data(self, component, updated_key, update_key_value):
        
        #Update any information of the component itself also update the information in system
        #Updates the information of the component as well as it updates information in the system manager
        if(updated_key == Type.ID):return

        all_keys = list(component.attributes.keys())
        if(updated_key in all_keys == False):
            return 
        
        if(updated_key in self.system_unique_group_identifiers):
            if(ComponentManager.VerifyUniqueData(update_key_value)==True):

                self.unregister_component(component)
                ComponentManager.RemoveInstance("both", component)
                
                component.attributes[updated_key] = update_key_value
                print("Sys man line 699",updated_key, component.attributes[updated_key])
                ComponentManager.AuthorizationProcess(component, True)
                self.register_component(component)
            
            else:
                print("\x1b[31m[ALERT]\x1b[0m Authorization Process: Component ", component.get_attribute(Type.ID), " doesn't contain unique data", end="")
                print(" component data has been corrected to default format. VerifyUniqueData() returns false",)
                component.print()
                return
        
        elif(updated_key in self.system_common_group_identifiers):
            self.unregister_component(component)
            component.attributes[updated_key] = update_key_value
            self.register_component(component)

        pass


    def update_signal(self, signal, component, data1, data2):
        if(self.component_exists(component) == False):
                print("[\x1b[31mSIGNAL INTERCEPTION DETECTTED!:  Internal communication\x1b[0m]  from: '"+component.get_name() + "'    signal: '\x1b[33m", signal, "\x1b[0m'  ignored by : \x1b[33m", "System Manager", end="")
                print("\x1b[35m signal_interrupt() \x1b[0m")
                return
            
        
        self.update_system_component_data(component, data1, data2)

    
    def signal_interrupt(self, signal, component, *data):
        
        print("[\x1b[35mSIGNAL INTERRUPT:  Internal communication\x1b[0m  from: '"+component.get_name() + "'    signal: '\x1b[33m", signal, "\x1b[0m'  sent to : \x1b[33m", "System Manager", end="")
        print("\x1b[35m signal_interrupt() \x1b[0m")

        if(signal == 'update'):
            self.update_signal(signal, component, data[0], data[1])
    
            
        elif(signal == 'myregisteration'):
            return self.component_exists(component)
        
        
        elif(signal == 'remove'):
            self.remove_component(component)

        else:
            print("signal_interrupt() for ", signal ,"signal is not supported.")
        
        return False
        
        
    def enable_components(self, type, reciepient=None, Sender=None):
        unique_group_identifiers = self.system_unique_group_identifiers
        common_group_idenfifiers = self.system_common_group_identifiers
        all_key_groups = self.ordered_regsitered_components.keys()
        
        sender = Sender

        if(isinstance(Sender, ComponentManager)):
            sender = Sender.get_attribute(Type.NAME)

        if(isinstance(reciepient, ComponentManager)):
            reciepient = reciepient.get_attribute(Type.NAME)


        if(type not in all_key_groups):
            return
        
        if(type == Type.ALL):
            all_components_by_key = self.ordered_regsitered_components[Type.ID].keys() 
            for idkey in all_components_by_key:                         
                self.ordered_regsitered_components[Type.ID][idkey].enable()
                print("[\x1b[32mDirect - connected\x1b[0m]  from: '",sender , "'    message: '\x1b[33menable" "\x1b[0m'   To Target component: \x1b[33m", reciepient, "\x1b[0m")
                
            return
        
        elif(type in unique_group_identifiers):
             try:
                reciever = self.ordered_regsitered_components[type][reciepient]
                print("[\x1b[32mDirect - connected\x1b[0m]  from: '", sender, "'    message: '\x1b[33menable" "\x1b[0m'   To Target component: \x1b[33m", reciever.get_attribute(Type.NAME),"\x1b[0m")
                self.ordered_regsitered_components[type][reciepient].enable()
             
             except Exception as e:
                 print("[\x1b[31mEXCEPTION\x1b[0m]", e)
                 print("[\x1b[31mDirect - Disconnected\x1b[0m]  from: '", sender, "'    message: '\x1b[33menable" "\x1b[0m'   To Target component: \x1b[33m", reciepient,"\x1b[0m")
                 return
             return
        
        elif(type in common_group_idenfifiers):
            try:
                sub_group_components = self.ordered_regsitered_components[type][reciepient]
                for component in sub_group_components:
                    print("[\x1b[32mDirect - connected\x1b[0m]  from: '",sender , "'    message: '\x1b[33m", "disable", "\x1b[0m'   To Target component: \x1b[33m", component.get_attribute(Type.NAME), end="\x1b[0m")
                    component.enable()

            except Exception as e:
                 print("[\x1b[31mEXCEPTION\x1b[0m]", e)
                 print("[\x1b[31mDirect - Disconnected\x1b[0m]  from: '", sender, "'    message: '\x1b[33menable" "\x1b[0m'   To Target component: \x1b[33m", reciepient ,"\x1b[0m")
                 return



        pass


    def disable_components(self, type, reciepient=None, Sender=None):
        unique_group_identifiers = self.system_unique_group_identifiers
        common_group_idenfifiers = self.system_common_group_identifiers
        all_key_groups = self.ordered_regsitered_components.keys()

        if(type not in all_key_groups):
            return
        
        sender = Sender

        if(isinstance(Sender, ComponentManager)):
            sender = Sender.get_attribute(Type.NAME)
        
        if(isinstance(reciepient, ComponentManager)):
            reciepient = reciepient.get_attribute(Type.NAME)

        if(type == Type.ALL):
            all_components_by_key = self.ordered_regsitered_components[Type.ID].keys()
            
            for idkey in all_components_by_key:
                print("[\x1b[32mDirect - connected\x1b[0m]  from: '",sender, "'    message: '\x1b[33mdisable" "\x1b[0m'   To Target component: \x1b[33m", reciepient, "\x1b[0m")
                self.ordered_regsitered_components[Type.ID][idkey].disable()
            return


        elif(type in unique_group_identifiers):
             try:
                reciever = self.ordered_regsitered_components[type][reciepient]
                print("[\x1b[32mDirect - connected\x1b[0m]  from: '",sender, "'    message: '\x1b[33mdisable" "\x1b[0m'   To Target component: \x1b[33m", reciepient, "\x1b[0m")
                self.ordered_regsitered_components[type][reciepient].disable()  
                #reciever.disable()
             except Exception as e:
                 print("[\x1b[31mEXCEPTION\x1b[0m]", e)
                 print("[\x1b[31mDirect - Disconnected\x1b[0m]  from: '",sender, "'    message: '\x1b[33mdisable" "\x1b[0m'   To Target component: \x1b[33m", reciepient, "\x1b[0m")
                 print(type, reciepient)

                 return
             return
        
        
        elif(type in common_group_idenfifiers):
            try:
                sub_group_components = self.ordered_regsitered_components[type][reciepient]
                for component in sub_group_components:
                    print("[\x1b[32mDirect - connected\x1b[0m]  from: '",sender, "'    message: '\x1b[33m", "disable", "\x1b[0m'   To Target component: \x1b[33m", component.get_attribute(Type.NAME), "\x1b[0m")
                    component.disable()
            except Exception:
                print("[\x1b[31mDirect - Disconnected\x1b[0m]  from: '",sender, "'    message: '\x1b[33mdisable" "\x1b[0m'   To Target component: \x1b[33m", reciepient, "\x1b[0m")
                return


    def find_component(self, type, value):

        #Determine whether or not the identifier is group key or key value
        unique_keys = self.system_unique_group_identifiers
        common_keys = self.system_common_group_identifiers

        if(type in unique_keys):
        
            try:
                component = self.ordered_regsitered_components[type][value]
                return component
            except Exception:
                return None
            pass


        elif(type in common_keys):
            try:
                components = self.ordered_regsitered_components[type][value]
                return components
            
            except Exception:
                return None
            pass       
 
        return None


    def broadcast_message(self, sender, message, extra=None):
        id_key_group = self.ordered_regsitered_components[Type.ID].keys()
        
        Sender = sender

        if(isinstance(sender, ComponentManager)):
            Sender = sender.get_attribute(Type.NAME)
        
        
        for key in id_key_group:
            if(Sender == self.ordered_regsitered_components[Type.ID][key].get_attribute(Type.NAME)):
                continue
            print("[\x1b[34mBroadcast - message\x1b[0m]  from: '",  Sender ,"'    message: '\x1b[33m" + message +"\x1b[0m'",  end="")
            print("    To reciever component: \x1b[33m"+(self.ordered_regsitered_components[Type.ID][key].get_attribute(Type.NAME))+"\x1b[0m")
            self.ordered_regsitered_components[Type.ID][key].handle_request(message, extra)
        pass


    def notify_components(self, type, message, reciepient, Sender, extra=None):
        all_key_groups = self.ordered_regsitered_components.keys()
        
        sender = Sender
        
        if(isinstance(reciepient, ComponentManager)):
            reciepient = reciepient.get_attribute(Type.NAME)

        if(isinstance(Sender, ComponentManager)):
            sender = Sender.get_attribute(Type.NAME)

            
        if(type not in all_key_groups):
            print("[\x1b[38;2;250;157;0mNotification - couldn't connect\x1b[0m  from: '", sender,"'    message: '\x1b[33m", message, "\x1b[0m'  To Target component: \x1b[33m",  reciepient, "\x1b[0m")
            return
        
        unique_group_identifiers = self.system_unique_group_identifiers
        common_group_idenfifiers = self.system_common_group_identifiers

        if(type in unique_group_identifiers):
             #Add exception handling for incorrect keys in the structure
            try:
                 reciever = self.ordered_regsitered_components[type][reciepient]
                 print("[\x1b[38;2;250;157;0mNotification - Connected\x1b[0m]  from: '",sender, "'    message: '\x1b[33m", message, "\x1b[0m'   To Target component: \x1b[33m", reciepient, "\x1b[0m")
                 self.ordered_regsitered_components[type][reciepient].handle_request(message, extra)

            except Exception as e:
                  print("[\x1b[31mEXCEPTION\x1b[0m]", e)
                  print("[\x1b[31mNotification - Disconnected\x1b[0m]  from: '",sender, "'    message: '\x1b[33m", message, "\x1b[0m'  To Target component: \x1b[33m",  reciepient, "\x1b[0m") 
                  pass
            return
        
        elif(type in common_group_idenfifiers):
            
            try:
                sub_group_components = self.ordered_regsitered_components[type][reciepient]
            
                for component in sub_group_components:
                    if(component.get_attribute(Type.NAME) == sender):
                        continue

                    print("[\x1b[38;2;250;157;0mNotification - Connected\x1b[0m]  from: '",sender, "'    message: '\x1b[33m", message, "\x1b[0m'   To Target component: \x1b[33m", component.get_attribute(Type.NAME), "\x1b[0m")
                    component.handle_request(message, extra)

            except Exception as e:
                print("[\x1b[31mEXCEPTION\x1b[0m]", e)
                print("[\x1b[31mNotification - Disconnected\x1b[0m]  from: '",sender, "'    message: '\x1b[33m", message, "\x1b[0m'  To Target component: \x1b[33m", reciepient, "\x1b[0m") 
                pass 
        else:
            print("[\x1b[31mNotification - Disconnected\x1b[0m]  from: '",sender, "'    message: '\x1b[33m", message, "\x1b[0m'  To Target component: \x1b[33m", reciepient, "\x1b[0m") 
      

    def get_attribute(self, type):
        return self._attributes[type]
    

    def set_attributes(self, type, value):
        if(type == Type.ID):
            return
        
        self._attributes[type] = value
        pass
         

    def print(self):
        
        print(self.ordered_regsitered_components)
        pass

    pass


#BUG 1
#any time it says 'str' does not support, it means that you're not accessing key but the value itself
#which raises error cuz it tries to find the key named that value
#NOTE  Need to handle dynamic unregistration when object is deleted
#NOTE  Need to make sure to remove components who are deauthorized
#NOTE  In future version, Component and system manager classes would be independent and general
       #Component manager will have functionality to process and retrieve any kind of component level data
       #System manager will act as independent general manager/mediator.
       #Component manager class should be compatible with any kind of mediator class, it should store data in some format like json, list 2d etc.
       #There will be two way communication meaning the component and system both will be aware of things around them
