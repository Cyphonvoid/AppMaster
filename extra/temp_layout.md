class comp_name(ComponentManager):
    def __init__(self, parent):
        ComponentManager.__init__(self)
        self.set_attribute(Type.CLASS_NAME, "comp_name") 
        
    def enable(self, extra=None):
        pass

    def disable(self, extra=None):
        pass

    def handle_request(self, request, extra):
        if(request == "disable"):
            self.disable()
        elif(request == "enable"):#hi, you need to import System package oh I don;t mean like that, okay sure. 
            self.enable()
        pass