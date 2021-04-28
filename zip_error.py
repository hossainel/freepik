import os
import zipfile
import glob

def testZip(file_name):
    print(file_name,end=": ")
    d = []
    try:
        with zipfile.ZipFile(file_name) as file: # opening the zip file using 'zipfile.ZipFile' class
            print("Ok")
            d = [file_name,'dx/ok'+file_name[2:]]
    except zipfile.BadZipFile: # if the zip file has any errors then it prints the error message which you wrote under the 'except' block
        print('Error: Zip file is corrupted')
        d = [file_name,'dx/xk'+file_name[2:]]
        url = 'https://www.freepik.com/download-file/'+file_name[3:-4]+'\n'
        with open('xlinks.txt','a+') as fob:
            fob.write(url)
            fob.close()
        with open('dx.txt','r') as fob:
            y = fob.readlines()
            fob.close()
        with open('dx.txt','w') as fob:
            if url in y: y.pop(y.index(url))
            for i in y:
                fob.write(i)
            fob.close()
    return d

for i in glob.glob("dx/*.zip"):
    ok, xk = testZip(i)
    os.rename(ok, xk)
