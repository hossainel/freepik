#import socket
#import requests
from urllib.request import Request, urlopen
#import html
import time
import zipfile

from torpy import TorClient
from torpy.utils import recv_all
from torpy.http import requests
from torpy.http.adapter import TorHttpAdapter
hostname = 'ifconfig.me'

def testZip(file_name):
    try:
        with zipfile.ZipFile(file_name) as file: # opening the zip file using 'zipfile.ZipFile' class
            return "Ok"
    except zipfile.BadZipFile: # if the zip file has any errors then it prints the error message which you wrote under the 'except' block
        return 'not ok'

def file_download(url,path):#{
    retry = True
    while retry:#{
        try:#{
            with TorClient() as tor:#{
                with tor.get_guard() as guard:#{
                    with tor.create_circuit(3) as circuit:#{
                        with circuit.create_stream((hostname,80)) as stream:#{
                            adapter = TorHttpAdapter(guard, 3)
                            with requests.Session() as sess:#{
                                sess.headers.update({'User-Agent':'Mozilla/5.0'})
                                sess.mount('http://',adapter)
                                sess.mount('https://',adapter)

                                print('Downloading: ',url)                        
                                resp = sess.get(url, timeout=15)
                                exts = resp.headers.get('content-type')
                                if 'application/zip'==exts:#{
                                    print(exts)
                                    with open(path,'wb') as fob:#{
                                        fob.write(resp.content)
                                        fob.close()
                                    with zipfile.ZipFile(path): # opening the zip file using 'zipfile.ZipFile' class
                                        print("File is Ok")
                                    #}end of with open
                                #}end of if
                                else:#{
                                    print(exts,'Wrong File Type!')
                                    raise Exception('Wrong file type!')
                            #}end of with requests
                        #}end of with circuit
                    #}end of tor.create
                #}end of tor.get
            #}end of TorClient                                    
            retry=False
            print('Download Complete!')
            
        #}end of try
        except:#{
            retry = True
            print('Retrying...')
            
        #}end of except            
    #}end of while
#}end of file_download
                        
def url_scrap():
    with open('links.txt','r') as rr:
        st = int(rr.readlines()[-1])+1
        rr.close()
        
    url = 'https://www.freepik.com/search?dates=any&format=search&from_query=business+card+mockup&page=%i&premium=0&query=business+card+mockup&selection=1&sort=popular&type=vector,psd'%1
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    xr = urlopen(req).read().split(b'class="pagination__pages">')[1]
    ed = int(xr[:xr.find(b'</')])+1
    print(st,'->',ed)
    with open('xlinks.txt','rb') as rr:
        rx = rr.readlines()
        rr.close()
    for oa in range(st,ed):
        url = 'https://www.freepik.com/search?dates=any&format=search&from_query=business+card+mockup&page=%i&premium=0&query=business+card+mockup&selection=1&sort=popular&type=vector,psd'%oa
        print(oa,":",url)
        r=open('links.txt','ab+')
        #xr = requests.get(url).text.split('id="dtl-')[1:]
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        xr = urlopen(req).read().split(b'id="dtl-')[1:]
        n=0
        for i in xr:         
            if b'https://www.freepik.com/download-file/%s\n'%i[:i.find(b'"')] in rx: pass
            else:
                n=n+1
                print(i[:i.find(b'"')])
                r.write(b'https://www.freepik.com/download-file/%s\n'%i[:i.find(b'"')])            
        print(n, 'file(s) been found new! out of',len(xr))
        n=0
        r.write(b'%i\n'%oa)
        r.close()
        time.sleep(1)

def url2data():
    fob=open('xlinks.txt','r')
    r=fob.readlines()
    fob.close()
    while len(r):
        i=r.pop()
        url = i[:-1]       
        save_path='dx/'+url.split('/')[-1]+'.zip'
        
        #req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        #dl_file = urlopen(req)
        #with open(save_path, 'wb') as out_file:
        #    out_file.write(dl_file.read())

        file_download(url,save_path)

        with open('dx.txt','a+') as fob:
            fob.write(i)
            fob.close()

        fob=open('xlinks.txt','w')
        for j in r:
            fob.write(j)
        fob.close()  

url2data()
