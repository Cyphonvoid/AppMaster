import pyrebase
import os
import firebase_admin
from firebase_admin import credentials, storage


class FireStorage():

    def __init__(self, UID=None):
        
        if(UID == None):
            self.__deauthorize__()
            return
        
        self._user_id = UID
        self.set_user(UID)
        self.__storage_path = None

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
        
        cred = credentials.Certificate(self.SERVICE_ACC_KEY)
        firebase_admin.initialize_app(cred)
        
        self.firebase = pyrebase.initialize_app(self.API_CONFIG)
        self.storage = self.firebase.storage()
        self.storage_client = storage.bucket("envisionai-game-center.appspot.com")
        
        pass
    
    def __deauthorize__(self):
        self._user_id = None
        pass
    
    def upload_file(self, folder, file_name, local_path=None):
        if(self._user_id == None):return

        if(self.__storage_path == None):
            if(local_path == None):
                return

        if(folder==None):
            local_path = self.__storage_path+file_name
        value = self.storage.child(self._user_id+"/"+folder+"/"+file_name).put(local_path)
        print(value)
        pass

    def download_file(self, folder, download_as, local_path=None):
        if(self._user_id == None):return 

        if(self.__storage_path == None):
            if(local_path == None):
                return

        if(local_path==None):
            local_path = self.__storage_path
        
        #Store the previous path
        prev_path = os.getcwd()
        #Set the path to current to download files in prefered location
        #os.chdir(arg['local_path']) 
        #os.getcwd()
        #self.storage.child(self._user_id + "/"+arg['folder']).download(arg['local_path'], filename=arg['download_as'])
        #os.chdir(prev_path)
        if(local_path == None):
            local_path = self.__storage_path

        os.chdir(local_path) 
        os.getcwd()
        self.storage.child(self._user_id + "/"+folder).download(local_path, filename=download_as)
        os.chdir(prev_path)


    def delete_file(self, path):
        if(self._user_id == None):return 
        self.storage_client.blob(self._user_id+"/"+path).delete()
        pass
    
    def delete_folder(self, path):
        folder_files = self.storage_client.list_blobs(prefix=self._user_id+"/"+path)
        for eachfile in folder_files:
            eachfile.delete()
        
        pass

    def set_user(self, UID):
        self._user_id = UID
        print("UID = '" + self._user_id + "'")
        return self
        pass
    
    def set_local_storage(self, path):
        self.__storage_path = path
        return self
        pass
    pass


#file = r"C:\Users\yasha\Visual Studio Workspaces\Puzzle Mania\Puzzle Mania Application\Backend\FireStorage\test.json"
#file2 = r"C:\Users\yasha\Visual Studio Workspaces\Puzzle Mania\Puzzle Mania Application\Backend\FireStorage"


Fire = FireStorage("Yashaswi")
Fire.set_local_storage(r"C:\Users\yasha\Visual Studio Workspaces\Puzzle Mania\Puzzle Mania Application\Backend")

#Fire.upload_file(folder="profile", file_name='test.txt')
#Fire.upload_file(folder="profile", file_name='ApiConfig.json')
#Fire.download_file(folder="profile/test.json", download_as="new_test.json", local_path=file2)
Fire.delete_folder("profile/images")

