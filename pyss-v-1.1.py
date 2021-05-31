#import socket
#import requests
from urllib.request import Request, urlopen
#import html
import time
import zipfile
from threading import Thread
from tqdm import tqdm

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
    
def file_download(url,path,thrd):#{
    max_retry = 10
    retry = True
    while retry and max_retry>0:#{
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

                                print('%2i: Downloading: '%thrd,url)                        
                                resp = sess.get(url, timeout=15)
                                dexts = resp.headers.get('content-length')
                                print(thrd,':',dexts, 'bytes | %.2f MB'%(int(dexts)/1048576))
                                exts = resp.headers.get('content-type')
                                if 'application/zip'==exts:#{
                                    max_retry = max_retry + 10
                                    print('%2i:'%thrd,exts)
                                    with open(path,'wb') as fob:#{
                                        #[xki for xki in tqdm(range(int(exts)))]
                                        fob.write(resp.content)
                                        
                                        #for i in tqdm(resp.content):#{
                                        #    fob.write(i)
                                        #}end of for
                                            
                                        fob.close()
                                    #}end of with open
##                                    with open(path,'wb') as f:#{
##                                        with tqdm(total=dexts, unit_scale=True, desc=path,initial=0, ascii=True) as pbar:
##                                            for ch in resp.iter_content(chunk_size=1024):
##                                                if ch:#{
##                                                    f.write(ch)
##                                                    pbar.update(len(ch))
##                                                #}end of if
##                                            #}end of for
##                                        #}end of with tqdm
##                                    #}end of with open

                                    with zipfile.ZipFile(path): #{ opening the zip file using 'zipfile.ZipFile' class
                                        with open('dx.txt','a+') as fob: #{ save the file that is being downloaded
                                            fob.write(url+'\n')
                                            fob.close()
                                        #} end of with open
                                        print("%2i: File is Ok"%thrd)  
                                    #}end of with zipfile
                                #}end of if
                                else:#{
                                    print('%2i:'%thrd,exts,'Wrong File Type!')
                                    raise Exception('Wrong file type!')
                                sess.close()
                                print('%2i: Connection Closed.'%thrd)
                            #}end of with requests
                        #}end of with circuit
                    #}end of tor.create
                #}end of tor.get
            #}end of TorClient                                    
            retry=False
            print('%2i: Download Complete!'%thrd)
            
        #}end of try
        except Exception as EXPT:#{
            retry = True
            max_retry = max_retry - 1
            print('%2i: %s :(%i)Retrying...'%(thrd,EXPT,max_retry))
        #}end of except            
    #}end of while
    if max_retry==0: open('wr.txt','a+').write(url+'\n')
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

def url2data(thrd):#{
    with open('xlinks.txt','r') as fob:#{
        r=set(fob.readlines())
        print(len(r), end="->")
        fob.close()
    #}end of with
    with open('dx.txt','r') as fob:#{
        r=r-set(fob.readlines())
        print(len(r))
        fob.close()
    #}end of with
    while len(r):#{
        t=[]

        for k in range(thrd):#{
            lenr = len(r)
            if (lenr==0): break
            i=r.pop()
            url = i[:-1]       
            save_path='dx/'+url.split('/')[-1]+'.zip'
            print(lenr,'remaining |',k,end=':')
            #file_download(url,save_path)
            t.append(Thread(target=file_download, args=(url,save_path,k,)))
            #t[-1].start()
        #}end of for
        #for i in tqdm([t[i].join() for i in range(10)]): pass
        for ti in tqdm(t,desc='Loads'): ti.start()

        for ti in tqdm(t,desc='Ended'): ti.join()

        with open('xlinks.txt','w') as fob:#{
            [fob.write(j) for j in r]
            fob.close()
        #}end of with
    #}end of while
#}end of url2data

url2data(15)
