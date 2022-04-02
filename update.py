import requests
from termcolor import *
import colorama
from datetime import datetime








class UpdateManager:
    def __init__(self,monitor_name,current_version):
        colorama.init()
        self.monitor_name = monitor_name
        self.current_version = current_version

        self.getCurrentVersion()
        

    def LOG(self,text,color):
        print(colored(f'[{datetime.now()}][{self.monitor_name}] {text}',color))

    @staticmethod
    def updateVersionNumber(version):
        with open('version.txt','w') as e:
            e.write(version)

    @staticmethod
    def getCurrentVersion():
        with open('version.txt','r') as e:
            e = e.readlines()
            return e[0].replace('\n','')

    def update(self):
        self.LOG("Updating...",'blue')
        headers = {
            'accept': 'application/vnd.github.VERSION.raw',
            'Authorization': 'token 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'
        }

        try:
            response = requests.get(f'https://api.github.com/repos/bevan654/{self.monitor_name}/contents/{self.new_version}.py',headers=headers)
        except:
            self.LOG('Error while updating','red')
            return False

        if response.status_code == 200:
            with open(str(self.new_version)+'.py','w') as e:
                e.write(response.content.decode('utf-8'))

            self.LOG("Successfully Downloaded New Version!",'green')
            self.updateVersionNumber(self.new_version)


        elif response.status_code == 404:
            self.LOG("Could not locate update file",'red')
            return False
        else:
            self.LOG("Bad Response Status "+str(response.status_code),'red')
            return False

    def checkForUpdates(self):
        self.LOG("Checking for updates..",'blue')
        headers = {
            'accept': 'application/vnd.github.VERSION.raw',
            'Authorization': 'token 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'
        }
        try:
            response = requests.get(f'https://api.github.com/repos/bevan654/{self.monitor_name}/contents/version.txt',headers=headers)
            
        except:
            self.LOG("Error getting version file",'red')
            return False
            

        if response.status_code == 200:
            self.new_version = response.content.decode('utf-8').strip()
            if(str(self.new_version) != str(self.current_version)):
                self.LOG("Update available",'blue')
                if not self.update():
                    return False
            else:
                self.LOG("You are all upto date :)",'yellow')
                return False

        elif response.status_code == 404:
            self.LOG("Monitor Respitory Not Found!",'red')
            return False
        elif response.status_code == 403:
            self.LOG("Unauthorized Access to Github Repo",'red')
            return False
        else:
            self.LOG("Bad Response Status "+str(response.status_code),'red')
            return False

