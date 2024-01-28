from abc import ABC, abstractmethod
from System.SystemManager import Type

#NOTE  idea: not implemented
#Create a functionality manager to which each functionality can hook to call any function without any order
#Use hooks or connections to let functional objects return other functionalities.


class Command(ABC):
    
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def delete(self):
        pass
    
    @abstractmethod
    def get_attribute(self):
        pass

    @abstractmethod
    def set_attribute(self):
        pass

class FunctionCommand(Command):

    #NOTE: Purpose of this class is create programmable commands of format {Function: (Parameters)}
    def __init__(self, command_name, function, *arguments):
        
        self._command_name = command_name
        self._function = function
        self._arguments = tuple(arguments)
        pass
    
    def __del__(self):
        del self._command_name
        del self._function
        del self._arguments
        
        self.execute = None
        self.configure_arguments = None
        self.configure_command = None

    def __eq__(self, other) -> bool:

        if(isinstance(other, FunctionCommand) == False):
            return False
        
        if(other.get_attribute(Type.NAME) != self.get_attribute(Type.NAME)):
            return False
        
        elif(other.get_attribute(Type.COMMAND) != self.get_attribute(Type.COMMAND)):
            return False
        
        elif(self.get_attribute(Type.ARGS) != self.get_attribute(Type.ARGS)):
            return False
        
        return True
    
    def __ne__(self, other):
        return not (self == other)
    
        pass
    def execute(self):
        try:
            self._function(*self._arguments)

        
        except Exception as e:

            print("\n\n     \x1b[31m FunctionCommand error!\x1b[0m")
            self.print()
            print("\x1b[33m Either function and function args don't match or the function isn't callable\x1b[0m")
            print(e)
            raise


    
    def print(self):
        print("command function: ", self._function)
        print("command name: ", self._command_name)
        print("command arguments: ", self._arguments)
    

    def set_command_name(self, name):
        self._command_name = name

    def set_attribute(self, type, value):

        if(type == Type.NAME):
            self._command_name = value
      
    
    def get_attribute(self, type):
        
        if(type == Type.NAME):
            return self._command_name
        
        elif(type == Type.COMMAND):
            return self._function
        
        elif(type == Type.ARGS):
            return self._arguments
        
    def configure_arguments(self, args):
        self._arguments  = args.copy()
    

    def configure_command(self, function):
        self._function = function


    def delete(self):
        self.__del__()
        pass


    pass

