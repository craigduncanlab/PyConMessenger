# ftp access for website file management
# Craig Duncan 9.4.24

from pathlib import Path # for reading directory
import re
import os.path as OPath
from ftplib import FTP
from np import login as localinfo
global mysession

# load up html files from local directory
def handleFileTransfers():
    folder = localinfo.getLocalHTMLFolder()
    print(folder)
    htmllist=getLocalHtmlFiles(folder) # these are full POSIX paths
    uploadFiles(htmllist)
       

# the filelist is a list of Path objects
def uploadFiles(filelist):
    session = getSession()
    print("Transferring files...")
    for fc in filelist:
        fname=fc.name
        mycmd = 'STOR '+fname    
        if OPath.isfile(fc):
            fh = open(fc, 'rb') # filehandle and binary read
            session.storbinary(mycmd, fh)
            fh.close()
        else:
            print ("File:",fc.name,' does not exist')

def getLocalHtmlFiles(folder):
    allfilepaths=[]
    p = Path(folder)
    if (p.is_dir()):
        print("Directory exists")
    else:
        print("Problem with specified directory (does not exist)")
        exit()
    mypattern = ['*.html', '*.css']
    for mp in mypattern:
        print(mp)
        for child in p.glob(mp):
            if (len(child.name)>0):
                allfilepaths.append(child)
        #logFiles(allfilepaths)
    
    return allfilepaths

# web related image formats
def getImageFiles(folder):
    allfilepaths=[]
    p = Path(folder)
    if (p.is_dir()):
        print("Directory exists")
    else:
        print("Problem with specified directory (does not exist)")
        exit()
    mypattern = getImageTypes()
    for atype in mypattern:
        mp="*"+atype
        for child in p.glob(mp):
            if (len(child.name)>0):
                allfilepaths.append(child)
    #logFiles(allfilepaths)
    return allfilepaths

def logFiles(mylist):
    print("These are the files I've found in specified directory:")
    for htf in mylist:
        print(htf.name)

# server files login directory
def getServerFileType(myinput):
    print("Server files login directory:")
    if ('.' not in myinput):
        myinput='.'+myinput
    session=getSession()
    files=session.nlst()
    outfiles=[]
    for f in files:
        if (myinput in f):
            outfiles.append(f)
    print(myinput,' files:')
    print(outfiles)
    return outfiles

def getImageTypes():
    output=['.jpg', '.png', '.jpeg']
    return output

def getServerImageFiles():
    session=getSession()
    files=session.nlst()
    print("Server files image directory:")
    imagefiles=[]
    if ('images' in files):
        session.cwd('images')
        print("Changed to image directory")
        imfiles=session.nlst()
        for f in imfiles:
            imtypes = getImageTypes()
            for im in imtypes:
                if (im in f):
                    imagefiles.append(f)
        session.cwd('..')
    print(imagefiles)
    return imagefiles

def downloadServerFiles():
    session=getSession()
    lf=localinfo.getDownloadFolder()
    downloadFileType('.html',lf)
    downloadFileType('.css',lf)
    print("Downloading HTML complete")
    files=session.nlst()
    if ('images' in files):
        session.cwd('images')
        downloadImageTypes()
        session.cwd('..')

def downloadImageTypes():
    lf=localinfo.getDownloadImageFolder()
    glist=getImageTypes()
    for image in glist:
        downloadFileType(image,lf)

# filetype and localfolder
def downloadFileType(ft,lf):
    session=getSession()
    # write binary local
    filelist=getServerFileType(ft)
    for fl in filelist:    
        localpath=lf+'/'+fl    
        fhandle = open(localpath, 'wb')
        print('Downloading: ', fl) 
        session.retrbinary('RETR ' + fl, fhandle.write)

def getServerFileNames():
    getServerFileType('.html')
    getServerFileType('.css')
    getServerImageFiles()

def removeServerFiles():
    removeServerFileType('.html')
    removeServerFileType('.css')
    removeServerImageFiles()
    print("Main Directory after file removal:")
    session=getSession()
    session.dir()

def removeServerFileType(ft):
    session=getSession()
    if '.' not in ft:
        ft='.'+ft
    files=session.nlst()
    delfiles=getServerFileType(ft)
    for f in delfiles:
        session.delete(f)
    
def removeServerImageFiles():
    session=getSession()
    files=session.nlst()
    print(files)
    ifiles=getServerImageFiles()
    print(ifiles)
    if ('images' in files):
        session.cwd('images')
        for f in ifiles:
            session.delete(f)
    print("Images Directory after file removal:")
    session.dir()
    session.cwd('..')

def deleteServerFile(myfile):
    session = getSession()
    session.delete(myfile)

def deleteServerDir(mydir):
    session=getSession()
    session.rmd(mydir)

# myftp is session object
def firstimeMakeDirectory(myftp):
    myftp.mkd("images")

def storeSession(mysess):
    global mysession
    mysession=mysess
    print("My Session:",mysession)
    
def resetSession():
    global mysession
    mysession=None

def getSession():
    global mysession
    return mysession

def startSession():
    #ff.set_debuglevel(self,level=2) # highest, 0= lowest
    myhost=localinfo.getHost()
    ff = FTP(host=myhost)  # connect to host, default port
    storeSession(ff)
    handleLogin()

def handleLogin():
    session=getSession()
    #
    needLogin=False
    print("Preparing for login.")
    usr=localinfo.getUser()
    pw=localinfo.getPassword()
    if needLogin==True:
        usr=input("enter user")
        pw=input("enter pwd")
    session.login(user=usr, passwd=pw)  
    print("Welcome is:")
    session.getwelcome() # optional  
    session.dir()  # or use ff.retrlines('LIST')
    

def upLoad():
    print("Transferring files")
    handleFileTransfers()
    getServerDirectory()

def getServerDirectory():
    session=getSession()
    print("Directory")
    session.dir() # this is relative to server login permissions
    print("PWD")
    a=session.pwd()
    print(a)
    
def endSession():
    session=getSession()
    session.quit()  # this is a polite handshake closure.  ff.close() is unilateral

def start():
    option=input("info(i), server filenames(n), setup(s), upload(u), download(d) or delete(r)?")
    if (option=="i"):
        startSession()
        getServerDirectory()
        endSession()
    if (option=="n"):
        startSession()
        getServerFileNames()
        endSession()
    if (option=="s"):
        startSession()
        firstimeMakeDirectory()
        endSession()
    if (option=="u"):
        startSession()
        upLoad()
        endSession()
    if (option=="d"):
        startSession()
        downloadServerFiles()
        endSession()
    if (option=="r"):
        confirm=input("Are you sure you want to delete all server HTML and image files?")
        if (confirm=="y"):
            startSession()
            removeServerFiles()
            endSession()

start()
