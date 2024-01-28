import pyrebase
import firebase_admin
from firebase_admin import  firestore, credentials, storage, auth
from System import *


class UserCredential():

    def __init__(self):
        #Data interface where Input can vary to whatever however everything inside will adjust to just neccessary properties, 
        #which can also change depending on how we extend our properties. 
        pass
    pass


class ClientSession(ComponentManager):

    def __init__(self):
        ComponentManager.__init__(self)
        self.set_classname("ClientSession")
        self.__user_data = {
             'username':None,
             'password':None,
             'uid':None,
             "email":None,
        }
        
        self.API_CONFIG = {
            "apiKey": "AIzaSyDDXGdcfd7TIVlbmBfdDYSJXKU17puyRGo",
            "authDomain": "envisionai-game-center.firebaseapp.com",
            "databaseURL": "https://envisionai-game-center-default-rtdb.firebaseio.com",
            "projectId": "envisionai-game-center",
            "storageBucket": "envisionai-game-center.appspot.com",
            "messagingSenderId": "923380741942",
            "appId": "1:923380741942:web:7c079818c7ce75bee6a597",
            "measurementId": "G'-L5GYXCXJHK"
        }
        
        self.SERVICE_ACC_KEY = {
            "type": "service_account",
            "project_id": "envisionai-game-center",
            "private_key_id": "d14b15e686f463a763ab517e78380aab33d7359d",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCUJIdlXUorm4qu\nV13aaJksjT2YaG0eXiGQRYAHd7oN2mryM1/QaOKardQ7M58ZDqmqQ64BMTRbmL7k\nFKUx5ZWQrfAuiyAeUU9xrLDTkXxKir68c0ATdFBONLwDkddpFNI0rVkeUF06Qlns\nhUlr0tNLQKvGQaUuQgxk1jpXISL+qehgFpBBbLDE2GoS3IcgmlCACSP3kdhHocDp\n6ZCrYJ2NyBb9bq/UkonnFqt+XZcsXkE5dUWV7084Awdy35qQf3wJ/W3KsMx428v3\nB6GQsW/r+y6ZdCTFre9ewoU2tj//b6eznL+NqtmsSDJU6SBle1wGDegypYByfQuG\ncSmoerrtAgMBAAECggEACtxVY3m1aFZc58SBSEkxgZymjrfegsLFPyh5PGhApvyu\nU9dZsj5zmSzJScB9F38wXR/dGo/wQLmFX9Sg+nQpxOjw74NE9Ylh2PmfdRijaMDx\n6YBMNaDqCkcUyZuK6VScxz6Lhrdpk6MtqIi/sJH3lPrGx8rO61dC8ARB/q/v5YTp\nbAKOnEuqmnPoNnNQQtaPBGx/YZ02Y9IeYtNs/AMBsiAHkF52eU2FPLb60U8kxai3\ns6I5LgukjGSx7HnxCxg/fe3NdYCPM9x2lIBN9YlwKrfUpdQH9RXTJUQS0w84Khbl\nz27uKHamCKduaUENK9TpbU4E355hmFSK8m/2/XohAQKBgQDNEJavgBtlDGKL/jNt\nLnez1Li2AUt9OAN1lPNjCbD3FBEc+WNJvOVTTXUpPZo0h/HPL/S7qUDj/0sOZEia\ntwS61O2UiNfeEoWthmfVsi7PzIM67hz8v1DUNYB3q6Byg1OycgffXwxuCg+HdJfy\nabDbGxJtuNOXYMthHyYykP3y4QKBgQC48HJGnplI1kVYicNZV8CwMF3Co19l1wGZ\nmvvM+SzFWpzrtxGtN9LNICxHYRbkEtmit7yY1DwLhqgT/ZUbW87xnO1tBrQzUtpp\nRFFgf2GtgYrPz62E9ZwAZChv+5Pxk1GiuSQwdNYgXcPsltE10nnErjMqd1+KAzGv\ntwZDNR+VjQKBgHJYja3PAXeXMFxfos1+28CrHVRf5Hgug79ND2pqPQOJbQF7DqJP\ncpDA4FPexd4E8BFX7F+4QTbhZDjiMpoS89A6a0AoDjcGnQPlroC6mt/Eamix3fgR\ntkCelMQmL5GrKUCX1Uv49DVn5sDhgtjplnSW4+/K4DHJB59gfywzLWgBAoGBAJBe\nY1btiAtr+UZchLrB3hGsMAU5M8d0SDN44QfpnCGT0tvPVWU7JrwqWWZ/TDdO38Y+\nWGOViioVPDAezL9GtA24yz9I9HL8QrPaOQxzY/TmI06GeJZKhTVo+ogwhBUZQ6kb\njjyleGJb0A5ozXiOjbATrK2B8nryc18QKTtdxQIhAoGBAK7xwyYTIffnSRWlp2Os\n2kwtA3vHKRfXhx4dqzjCCiGYQz0EjyknBE/apKSyxdfHfR2/ZxEcmdNiGVjuqGTT\nkZW6ZjOoIqBaCHU17lzpCgZV4dlNewTh91Z8i8mFjuI0OjiVUUE9UY2Kg3frt+yq\nGfnhQKxtGSRjsd4Pi+tFwm1Z\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-e8igf@envisionai-game-center.iam.gserviceaccount.com",
            "client_id": "101558038648508484552",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-e8igf%40envisionai-game-center.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }

        self.cred = credentials.Certificate(self.SERVICE_ACC_KEY)
        firebase_admin.initialize_app(self.cred)
        self.app = pyrebase.initialize_app(self.API_CONFIG)

        self.fire_auth = self.app.auth()
        self.storage = self.app.storage()
        self.firedb = firestore.client()
        self.storage_client = storage.bucket("envisionai-game-center.appspot.com")
        
        pass

    def __store_data(self,**arg):

        self.__user_data['email'] = arg['email']
        self.__user_data['password'] = arg['password']
        self.__user_data['uid'] = arg['uid']
        self.__user_data['username'] = arg['username']

        pass
    

    
    def print_session(self):
        print("UID:", self.__user_data['uid'])
        print("email:", self.__user_data['email'])
        print("username:", self.__user_data['username'])
        print("password:", self.__user_data['password'])
        pass
    
    def sign_in(self, **arg):
        try:

            info = self.fire_auth.sign_in_with_email_and_password(arg['email'], arg['password'])
            user=auth.get_user_by_email(arg['email'])
            self.__store_data(email=user.email, uid=user.uid, username=user.display_name, password=arg['password'])
            self.print_session()
           
            return True
            pass
        except:
            
            return False
            pass
        pass
        

    def sign_out(self):
        del self.__user_data
        self.__user_data = None
        
        pass

    def sign_up(self,  **arg):

        try:
            user = auth.create_user(**arg)
            self.__create_storage(user.uid)
            self.__create_profile(user.uid)
            self.__store_data(email=user.email, password=arg['password'], username=user.display_name, uid=user.uid)
            self.print_session()
            return True
            pass
        
        except Exception as e:
            print(e)
            return False
            pass

        pass
        

    def __create_profile(self, UID):
        
        user_profile = {
            'username':'',
            'password':'',
            'email':''
        }

        self.firedb.collection(UID).document('profile').set(user_profile)
        pass

    def __create_storage(self, UID):
        
        
        file_path = r"C:\Users\yasha\Visual Studio Workspaces\Puzzle Mania\Puzzle Mania Application\Backend\FireClient\__deletion__.json"
        self.storage.child(UID + "/" + "images/__file__.json").put(file_path)
        self.storage.child(UID + "/" + "__deletion__.json").put(file_path)
        pass

    def delete_account(self):
      
        UID = self.__user_data['uid']
        
        auth.delete_user(UID)
        
        docs = self.firedb.collection(UID).stream()
        
        for doc in docs:
            doc.reference.delete()
            pass

        #self.storage_client.blob(UID+"/images/__file__.json").delete()
        #self.storage_client.blob(UID+"/__deletion__.json").delete()
        #self.storage_client.delete_blobs(UID+"/images")
        all_files = self.storage_client.list_blobs(prefix=UID)
        
        for file in all_files:
            file.delete()
        return True
        pass

    
    def update_password(self, new_password):
      
        #user = auth.update_user(self.__user_data['uid'], password=new_password)

        #Try relogin to make sure password did get updated
        try:
            user = auth.update_user(self.__user_data['uid'], password=new_password)
            print("TAG LINE 172, session.py")
            self.sign_in(email=self.__user_data['email'], password=new_password)
            self.__user_data['password'] = new_password
            print("Updated password:", self.__user_data['password'])
            return True
        except Exception as e:
            print("TAG LINE 172, session.py", e)
            print("Failed:", self.__user_data['password'])
            return Error(e)
            pass
        pass


    def update_username(self, username):
        try:
            user = auth.update_user(self.__user_data['uid'], display_name=username)
            self.__user_data['username'] = user.display_name
            return True
        except Exception as e:
            print("Failed", e)
            return Error(e)
        pass

    def update_image(self, image):
        pass


    def update_email(self, new_email):
      
        #Try relogin to make sure email did get updated
        try:
            user = auth.update_user(self.__user_data['uid'], email=new_email)
            self.sign_in(email=new_email, password=self.__user_data['password'])
            self.__user_data['email'] = new_email
            print("Updated email:", self.__user_data['email'])
            return True
            pass
        except Exception as e:
            print("Failed:", self.__user_data['email'])
            return Error(e)
            pass
        pass

    
    def get_email(self):
        return self.__user_data['email']
        pass

    def get_username(self):
        return self.__user_data['username']
        pass

    def get_password(self):
        return self.__user_data['password']
        pass

    def get_uid(self):
        return self.__user_data['uid']
        pass

    def enable(self, extra=None):
        return super().enable(extra)
    

    def disable(self, extra=None):
        pass
    
    
    def handle_request(self, request, extra):

        if(request == "enable"):
            pass

        elif(request == "disable"):
            pass
        
        elif(request == "getpassword"):
            SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['component'], self.get_password())
            #return self.get_password()
        
        elif(request == "getusername"):
            SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['component'], self.get_username())
            #return self.get_username()
        
        elif(request == "getemail"):
            SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['component'], self.get_email())
            #return self.get_email()
        
        elif(request == "getuid"):
            SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['component'], self.get_uid())
            #return self.get_uid()
        
        elif(request == "updatepassword"):
            data = {
                'responsefor':request,
                'message':'Empty',
                'fullfilled':None
            }
            
            name = self.get_attribute(Type.NAME)
            Object = self.update_password(extra['credentials']['password'])
            if(isinstance(Object, bool) and Object == True):
                data['message'] = 'Successfully updated password to ' + extra['credentials']['password']
                data['fullfilled'] = True
                SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['sender']['name'], name, data)
        
            
            elif(isinstance(Object, Error)):
                #data['message'] = "Couldn't update your password, we're sorry! "
                data['message'] = Object.get()
                data['fullfilled'] = False
                SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['sender']['name'], name, data)
           
        
        elif(request == "updateusername"):
            data = {
                'responsefor':request,
                'message':'Empty',
                'fullfilled':None
            }
            
            name = self.get_attribute(Type.NAME)
            Object = self.update_username(extra['credentials']['username'])
            if(isinstance(Object, bool) and Object == True):
                data['message'] = 'Successfully updated username to ' + extra['credentials']['username']
                data['fullfilled'] = True
                SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['sender']['name'], name, data)
            
            elif(isinstance(Object, Error)):
                #data['message'] = "Couldn't update your username, we're sorry! "
                data['message'] = Object.get()
                data['fullfilled'] = False
                SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['sender']['name'], name, data)
        
        elif(request == "updateemail"):
            data = {
                'responsefor':request,
                'message':'Empty',
                'fullfilled':None
            }
            
            name = self.get_attribute(Type.NAME)
            Object = self.update_email(extra['credentials']['email'])
            if(isinstance(Object, bool) and Object == True):
                data['message'] = 'Successfully updated email to ' + extra['credentials']['email']
                data['fullfilled'] = True
                SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['sender']['name'], name, data)
            
            elif(isinstance(Object, Error)):
                #data['message'] = "Couldn't update your email, we're sorry! "
                data['message'] = Object.get()
                data['fullfilled'] = False
                SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['sender']['name'], name, data)
        

        elif(request == "updateimage"):

            #NOTE
            print("UPDATE IMAGE Session.py line 331, functionality not implemented yet")
            return
        
            data = {
                'responsefor':request,
                'message':'Empty',
                'fullfilled':None
            }
            
            name = self.get_attribute(Type.NAME)
            if(self.update_image(**extra['credentials']) == True):
                data['message'] = 'Successfully logged in!'
                data['fullfilled'] = True
                SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['sender']['name'], name, data)
               
            else:
                data['message'] = 'Invalid login, try again or contact admin'
                data['fullfilled'] = False
                SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['sender']['name'], name, data)
        
        
        elif(request == "signup"):
            data = {
                'responsefor':request,
                'message':'Empty',
                'fullfilled':None
            }
            
            if(self.sign_up(**extra['credentials']) == True):
                data['message'] = 'Account was successfully created!'
                data['fullfilled'] = True
                SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['sender']['name'], self.get_attribute(Type.NAME), data)
               
            else:
                data['message'] = "Credentials are not valid for registration"
                data['fullfilled'] = False
                SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['sender']['name'], self.get_username(), data)
            
        
        elif(request == "signin"):
            data = {
                'responsefor':request,
                'message':'Empty',
                'fullfilled':None
            }
            
            name = self.get_attribute(Type.NAME)
            if(self.sign_in(**extra['credentials']) == True):
                data['message'] = 'Successfully logged in!'
                data['fullfilled'] = True
                SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['sender']['name'], name, data)
               
            else:
                data['message'] = 'Invalid login, try again or contact admin'
                data['fullfilled'] = False
                SystemManager.notify_components(Type.NAME,"recieve_backend_data", extra['sender']['name'], name, data)
                

        pass
        
    pass



#session = ClientSession()
#session.sign_up(email='newtest@gmail.com', password='verygoodpassword', display_name="tester", email_verified=False, disabled=False)
#session.delete_account("5l26AxMFK7baf99cLNDnzlLPEEv1")
#session.sign_up(email='newtest@gmail.com', password='verygoodpassword', display_name="tester", email_verified=False, disabled=False)
#session.sign_up(email='newtest2@gmail.com', password='verygoodpassword', display_name="tester", email_verified=False, disabled=False)
#session.sign_up(email='newtest2@gmail.com', password='verygoodpassword', display_name="tester", email_verified=False, disabled=False)


#session.sign_in(email="newtest3@gmail.com", password="verygoodpassword")
#session.delete_account()

#session.update_email("newtest3@gmail.com")



