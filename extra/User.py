import pyrebase
import firebase


class AppCenterUser():

    def __init__(self):
        self.__email = None
        self.__username = None
        self.__password = None
        self.__user_id_token = None
        self.__user_registered = None

        self.__user_logged_in = False
        self.__user_authorization = 'Failed'
        
        self.__criterion = {
            'passwordLength':14,
            'specialChar':['@', '#', '$', '%', '^', '*', '(', ')', '_', '-', '+', '[', ']', ';', ':', '<', '>', '?', '/', '{', '}', '|', '~', '`', '!']
        }

        #Client Identification
        self.AppCenterConfig = {
            "apiKey": "AIzaSyDDXGdcfd7TIVlbmBfdDYSJXKU17puyRGo",
            "authDomain": "envisionai-game-center.firebaseapp.com",
            "databaseURL": "https://envisionai-game-center-default-rtdb.firebaseio.com",
            "projectId": "envisionai-game-center",
            "storageBucket": "envisionai-game-center.appspot.com",
            "messagingSenderId": "923380741942",
            "appId": "1:923380741942:web:7c079818c7ce75bee6a597",
            "measurementId": "G'-L5GYXCXJHK"
        }
        
        self.Database = pyrebase.initialize_app(self.AppCenterConfig)
        self.Authoriser = self.Database.auth()
        self.SignInResponse = None
        self.SignUpResponse = None

        self.Message = None
        pass


    def ResetPassword(self, password):
        if(self.__user_authorized()):
            self.__password = password
        pass

    def ResetUsername(self, username):
        if(self.__user_authorized()):
            self.__username = username
        pass

    def ResetEmail(self, email):
        if(self.__user_authorized() == False): return

        self.__email = email
        pass
    
    def __authorize(self, val):
        if(val == 'yes'):
            self.__user_authorization = 'verified'
            self.__user_logged_in = True

        elif(val == 'no'):
            self.__user_authorization = 'Failed'
            self.__user_logged_in = False

        pass
    
    def __user_authorized(self):
        if (self.__user_authorization == 'Failed'): return False
        elif(self.__user_authorization == 'verified'): return True
        pass

    def SignIn(self, **data):

        try:
            self.__email = data['email']
            self.__password = data['password']

            self.SignInResponse = self.Authoriser.sign_in_with_email_and_password(self.__email, self.__password)
            #self.__user_id_token = self.SignInResponse['idToken']
            #current = self.SignUpResponse['localId']
            #print(current)
            #print(current)
            #print("\x1b[31mUSER TOKEN\x1b[0m", self.__user_id_token)
            self.__username = self.SignInResponse['displayName']
            self.__user_registered = self.SignInResponse['registered']
            self.__authorize('yes')
            print('successfully logged in')
            return True
        
        except:
            self.__authorize('no')
            #self.Message = self.SignInResponse['error']
            print('login failed, try again')
            return False
            pass
        
        pass
    

    def __verify_user_criterion(self, data):
        if(len(data) < self.__criterion['passwordLength']):
            return False
        
        
        #Check special chars
        for char in data:
            if(char not in self.__criterion['specialChar']):
                return False
        
        pass

    def SignOut(self):

        pass
    
    def SignUp(self, **data):
        
        try:
            self.__email = data['email']
            self.__password = data['password']
            
            self.SignUpResponse = self.Authoriser.create_user_with_email_and_password(self.__email, self.__password)
            self.__user_id_token = self.SignUpResponse['idToken']
            self.Authoriser.send_email_verification(self.__user_id_token)
            current = self.SignUpResponse['localId']
            print(current)
       
            print("\x1b[31mUSER TOKEN\x1b[0m", self.__user_id_token)
            #self.__username = self.SignUpResponse['displayName']
            #self.__user_registered = self.SignUpResponse['registered']
            self.__authorize('yes')
            print('successfully registered account')
            return True
        
        except:
            self.__authorize('no')
            self.Message = self.SignUpResponse['error']
            print("couldn't create account")
            return False
            pass
        
        
        pass
    
    
    def GetData(self):
        pass
    

    def DeleteAccount(self):
        pass


    def DisplayInfo(self):
        print(self.Authoriser.get_account_info(self.__user_id_token))
        pass
    pass


#User = AppCenterUser()
##print(User.SignIn(email="yashaswi.kul@gmail.com", password="yash18hema06"))
#print(User.SignUp(email="jaedon@gmail.com", password="jaedon"))
#print(User.SignIn(email="jaedon@gmail.com", password="jaedon"))
