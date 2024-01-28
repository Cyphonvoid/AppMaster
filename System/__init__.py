from System.SystemManager import *
from System.Sockets import *
from System.Error import*

#System Initialization and configuration
SystemManager = SystemManager()
ComponentManager.ConfigureMasterManager(SystemManager)


print("MULTIPLE TIMES")
Connection = Connection()
Connection.auto_clear(True)
