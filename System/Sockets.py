from System.SystemManager import *
from System.Commands import *

class Socket():
    
    @staticmethod
    def Authorize():
        pass

    @staticmethod
    def Deathorize():
        pass

    @staticmethod
    def VerifyCommand():
        pass

    @staticmethod
    def AuthorizationProcess():
        pass


    def __init__(self):
        self._executable_commands = []
        self._temp_command_data = []
        self._total_commands = 0
        self._limit = None
        pass

    def __del__(self):
        del self._executable_commands
        self.run_commands = None    
        self.add_command = None
        self.remove_command = None
    


    def run_commands(self):
        for command_object in self._executable_commands:
            command_object.execute()
        pass
    
    def get_command_object(self, index):
        if(index > len(self._executable_commands)-1):
            return 
        
        return self._executable_commands[index]
    
    def print(self):
        for command_object in self._executable_commands:
            command_object.print()
        

    def add_command(self, command_object):
        if(self._limit == None or len(self._executable_commands) < self._limit):
            self._executable_commands.append(command_object)
    


    def remove_command(self, command_object):
        self._executable_commands.remove(command_object)
    
    def set_limit(self, limit):
        if(isinstance(limit, int)):
            self._limit = limit
        
        return
    
    def remove_limit(self):
        self._limit = None

    def search_command(self, type, value, SINGLE_RETURN=True):

        for command in self._executable_commands:
            command.print()
            if(command.get_attribute(type) == value):

                if(SINGLE_RETURN == False):
                    self._temp_command_data.append(command)
                else:
                    return command
                pass
            pass
            
        return None
    
    def get_command(self, index):
        if(index > len(self._executable_commands)-1):
            return
        
        return self._executable_commands[index]
    
    def command_exists(self, command_object):
        index = 0
        for commands in self._executable_commands:
    
            if(commands == command_object):
                return index
            
            index = index + 1
        
        return None
    
    def delete_searched_commands(self, index=0):
        #This function isn't usuable yet. Not sure if this function is worth it
        if(index == Type.ALL):
            for command in self._temp_command_data:
                command.print()
                self._executable_commands.remove(command)

            return
        
        if(index > len(self._temp_command_data)-1):
            return
        self._executable_commands.remove(self._temp_command_data[index])
        pass
    
    def clear_commands(self):
        self._executable_commands.clear()
        pass
        
    def insert_command(self, command_name, command_function, *args):
        self._executable_commands.append(FunctionCommand(command_name, command_function, *args))

    def delete_self(self):
        self.__del__()
        pass

    pass


class Connection():
    
    def __init__(self):
        #self._command_function = None
        self._auto_clear = False
        self.command = None
        self._command_name = None

        pass
    
    def notify(self, *args):
        name = "notify"
        _command_function = SystemManager.GetInstance(0).notify_components
        self.command = FunctionCommand(name, _command_function, *args)
        self._command_name = name

        return self
    
    def enable(self, *args):
        name = "enable"
        _command_function = SystemManager.GetInstance(0).enable_components
        self.command = FunctionCommand(name, _command_function, *args)
        self._command_name = name
        return self
    
    def disable(self, *args):
        name = "disable"
        _command_function = SystemManager.GetInstance(0).disable_components
        self.command = FunctionCommand(name, _command_function, *args)
        self._command_name = name
        return self
    
    def broadcast(self, *args):
        name = "broadcast"
        _command_function = SystemManager.GetInstance(0).broadcast_message
        self.command = FunctionCommand(name, _command_function, *args)
        self._command_name = name
        return self
    
    
    def function(self, function, *args):
        name = "function"
        self.command = FunctionCommand(name, function, *args)
        self._command_name = name

        return self

    def inject_into(self, socket):
        if(self.command == None):
            return
        
        socket.add_command(self.command)
        if(self._auto_clear == True):self.command = None
        pass
    

    def remove_from(self, socket):
        if(self.command == None):
            return
        
        value = socket.command_exists(self.command) 
        
        if(value != None):
            command = socket.get_command(value)
            socket.remove_command(command)

        if(self._auto_clear == True):self.command = None
        pass
        
    
    
    def clear(self):
        self.command = None
    
    def auto_clear(self, value):
        self._auto_clear = value
    pass


