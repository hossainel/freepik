from torpy import TorClient
from torpy.utils import recv_all
from torpy.http import requests
from torpy.http.adapter import TorHttpAdapter
hostname = 'ifconfig.me'

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
                        
file_download('https://www.freepik.com/download-file/1000440','test.zip')
