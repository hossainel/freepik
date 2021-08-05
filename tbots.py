import telebot
from glob import glob
from tqdm import tqdm
class vCards:
    TOKEN = '<your bot token>'
    cid = 'channel ID'
    def __init__(self):
        self.tb = telebot.TeleBot(self.TOKEN)

    def pf(self,s):
        print(s)
    def sendDoc(self,fileName):
        with open(fileName,'rb') as Tfile:
            self.tb.send_document(self.cid,Tfile)
    def sendFolder(self,folderName,fileType='.*'):
        for i in tqdm(glob('%s/*%s'%(folderName,fileType))):
            #try:
            self.sendDoc(i)
                #self.pf('[Success] %s'%i)
            #except: self.pf('[Failed] %s'%i)

v = vCards()
folder_name = input('Folder->')
v.sendFolder(folder_name)
