import os
import json
import time
import base64
import requests
from glob import glob

apiKey = 'a108cad48026147bbdf3c604f8c38835' # my API key

print("imgBB API Uploader")
print("API Key: " + apiKey)

def ups(fileLocation,apiKey,file_name):
    retry=True
    while retry:
        try:
            with open(fileLocation, "rb") as xfile:
                url = "https://api.imgbb.com/1/upload"
                payload = {
                    "key": apiKey,
                    "image": base64.b64encode(xfile.read()),
                    "name": file_name,
                }
                res = requests.post(url, payload)
            retry=False
            return res
        except:
            print('Retrying...')
            time.sleep(5)
            
def imgBB_upload(fileLocation):
    fileLocaion = fileLocation.replace('\\','/')
    file_name = fileLocaion[fileLocaion.rfind('/')+1:fileLocaion.rfind('.')]
    res=ups(fileLocation,apiKey,file_name)
    if res.status_code == 200:
        print("Server Response: " + str(res.status_code))
        print("Image Successfully Uploaded")
        r = json.loads(res.text)
        url = r['data']['url']
        thumb = r['data']['thumb']['url']
        delete_url = r['data']['delete_url']
    else:
        print("ERROR")
        print("Server Response: " + str(res.status_code))
        if not os.path.exists('wrr.txt'): open('wrr.txt','w')
        with open('wrr.txt','a+') as foc:
            foc.write('%s:%s\n'%(fileLocaion,res.status_code))
            foc.close()
            
    return '%s; %s; %s; %s\n'%(file_name,url,thumb,delete_url)
    


folderLocation = input("Enter Folder location: ")

if os.path.exists(folderLocation+'tmp.txt'):
    fob = open(folderLocation+'tmp.txt','r')
    f=[i[:-1] for i in fob.readlines() if not i=='\n']
    fob.close()
else:
    f=glob(folderLocation+'/*.*')
    tmp = open(folderLocation+'tmp.txt','w')
    [tmp.write(i+'\n') for i in f]
    tmp.close()
if not os.path.exists(folderLocation+'.txt'): open(folderLocation+'.txt','w')

print('Total %i file(s) found'%len(f))
j=1
while (len(f)):
    i=f.pop()
    print(j,':',i)
    with open(folderLocation+'.txt','a+') as fob:
        fob.write(imgBB_upload(i))
        fob.close()
    with open(folderLocation+'tmp.txt','w') as tmp:
        [tmp.write(i+'\n') for i in f]
        tmp.close()
    j=j+1
    
if os.path.exists(folderLocation+'tmp.txt'): os.remove(folderLocation+'tmp.txt')
