from zipfile import ZipFile
from glob import glob
from PIL import Image
import os

def photo_extractor(xfile):
##    print('Extract all files in ZIP to current directory')
##    # Create a ZipFile Object and load sample.zip in it
##    with ZipFile(xifle, 'r') as zipObj:
##       # Extract all the contents of zip file in current directory
##       zipObj.extractall()
##    print('Extract all files in ZIP to different directory')
##    # Create a ZipFile Object and load sample.zip in it
##    with ZipFile('sampleDir.zip', 'r') as zipObj:
##       # Extract all the contents of zip file in different directory
##       zipObj.extractall('temp')
##    print('Extract single file from ZIP')
    # Create a ZipFile Object and load sample.zip in it
    print(xfile)
    with ZipFile(xfile, 'r') as zipObj:
       # Get a list of all archived file names from the zip
       listOfFileNames = zipObj.namelist()
       # Iterate over the file names
       for fileName in listOfFileNames:
           # Check filename endswith csv
           if fileName.endswith('.jpg'):
               # Extract a single file from zip
               zipObj.extract(fileName, 'imgs/%s'%xfile[:-4])
           if fileName.endswith('.png'):
               # Extract a single file from zip
               zipObj.extract(fileName, 'imgs/%s'%xfile[:-4])

def photo_resizer(xfile):
    baseheight = 775
    basewidth = 775
    img = Image.open(xfile)
    img = img.resize((basewidth, baseheight), Image.ANTIALIAS)
    save_path = 'imgs/ok/'+xfile[xfile.rfind('/')+1:].replace('\\','_')
    print(xfile, '->', save_path)
    img.save(save_path)
                   
def main():
    x=0
    for i in glob('dx/ok/*.zip'):
        print('(%i)'%x,end=' ')
        photo_extractor(i)
        x=x+1
    x=0
    relevant_path = "imgs/dx/ok"
    included_extensions = ['jpg','jpeg', 'bmp', 'png', 'gif']
    file_names = [fn for fn in os.listdir(relevant_path) if any(fn.endswith(ext) for ext in included_extensions)]
    for j in os.listdir('imgs/dx/ok'):
        for i in glob("imgs/dx/ok/%s/*.jpg"%j):
            print('(%i)'%x,end=' ')
            x=x+1
            photo_resizer(i)

if __name__ == '__main__':
   main()
