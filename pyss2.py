#import socket
import requests
from urllib.request import Request, urlopen
from requests_html import HTMLSession
#import html
import time
import zipfile

def url_scrap():
    with open('links.txt','r') as rr:
        st = int(rr.readlines()[-1])+1
        rr.close()
        
    #url = 'https://all-free-download.com/free-vector/business-card_page_%i.html'%3
    #print(url)
    #req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    #xr = urlopen(req).read().split(b'https://all-free-download.com/free-vector/business-card_page_')[-1]
    #ed = int(xr[:xr.find(b'.')])+1
    ed = 374
    print(st,'->',ed)
    with open('xlinks.txt','rb') as rr:
        rx = rr.readlines()
        rr.close()
    for oa in range(st,ed):
        url = 'https://all-free-download.com/free-vector/business-card_page_%i.html'%oa
        print(oa,":",url)
        r=open('links.txt','ab+')
        #xr = requests.get(url).text.split('id="dtl-')[1:]
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        xr = urlopen(req).read().split(b'https://all-free-download.com/free-vector/download/')[1:]
        n=0
        for i in xr:         
            if b'https://all-free-download.com/free-vector/download/%s_download.html\n'%i[:i.find(b'.html"')] in rx: pass
            else:
                if n%2:
                    n=n+1
                    print(i[:i.find(b'"')])
                    r.write(b'https://all-free-download.com/free-vector/download/%s_download.html\n'%i[:i.find(b'.html"')])
                else: n=n+1
        print(n//2, 'file(s) been found new! out of',len(xr)//2)
        n=0
        r.write(b'%i\n'%oa)
        r.close()
        time.sleep(1)

def url2data():#{
    fob=open('xlinks.txt','r')
    r=fob.readlines()
    fob.close()
    while len(r):#{
        xt = 1
        retry = True
        while retry:#{
            print('Try',xt)
            xt=xt+1
            try:#{
                retry = False
                i=r.pop()
                url = i[:-1]       
                save_path='dx/'+url.split('/')[-1].replace('_download.html','.zip')

                print(url[url.find('/download/'):])
                url2 = 'http://files.all-free-download.com/free_download_graphic_'+save_path[save_path.rfind('_')+1:].replace('zip','html')
                print(url2[url2.find('/free'):])
                session = HTMLSession()
                xr = session.get(url2)
                
                try: xr.html.render()  # this call executes the js in the page
                except Exception as pe: url2=str(pe)[str(pe).find('http://'):] #this to find the redirect file link
                print(url2[url2.rfind('/graphic'):])
                req = Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
                dl_file = urlopen(req)
                exts = dl_file.headers.get('content-length')
                print(exts, 'bytes | %.2f'%(int(exts)/(1024**2)),'MB')
                #exts = dl_file.headers.get('content-type')
                
                with open(save_path, 'wb') as out_file:
                    out_file.write(dl_file.read())
                    out_file.close()
                #}end of with

                session.close()
                with zipfile.ZipFile(save_path): # opening the zip file using 'zipfile.ZipFile' class
                    print("File is Ok")
                #}end of with
                with open('dx.txt','a+') as fob:
                    fob.write(i)
                    fob.close()
                #}end of with
                fob=open('xlinks.txt','w')
                print(len([fob.write(j) for j in r]))
                fob.close()
                print(save_path[3:])
            #}end of try
            except:#{
                retry = True
                print('retrying... in 5sec')
                time.sleep(5)
            #}end of except
        #}end of while retry
    #}end of while len
#}end of url2data

url2data()
