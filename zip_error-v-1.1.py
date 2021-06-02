import os
import zipfile
import glob

def testZip(file_name):
    #print(file_name,end=": ")
    d = []
    try:
        with zipfile.ZipFile(file_name) as file: # opening the zip file using 'zipfile.ZipFile' class
            #print("Ok")
            d = [file_name,'dx/ok'+file_name[file_name.find('dx')+2:]]
            url = 'https://www.freepik.com/download-file/'+file_name[file_name.rfind('\\')+1:-4]+'\n'
            with open('dx - Copy.txt','a+') as fob:
                fob.write(url)
                fob.close()
    except zipfile.BadZipFile: # if the zip file has any errors then it prints the error message which you wrote under the 'except' block
        print('%s: Error: Zip file is corrupted'%file_name)
        d = [file_name,file_name[:file_name.find('/dx')+3]+'/xk'+file_name[file_name.rfind('\\'):]]
        url = 'https://www.freepik.com/download-file/'+file_name[3:-4]+'\n'
        with open('dx.txt','r') as fob:
            y = fob.readlines()
            fob.close()
##        with open('dx.txt','w') as fob:
##            if url in y: y.pop(y.index(url))
##            for i in y:
##                fob.write(i)
##            fob.close()
    return d

if not os.path.exists('dx/ok/'): os.mkdir('dx/ok/')
with open('dx - Copy.txt','w') as fob:
    fob.close()
for j in range(10):
    print('%i - dx'%j)
    for i in glob.glob("%i/dx/*.zip"%j):
        ok, xk = testZip(i)
        os.rename(ok, xk)
print('dx')

for i in glob.glob("dx/*.zip"):
    ok, xk = testZip(i)
    os.rename(ok, xk)
