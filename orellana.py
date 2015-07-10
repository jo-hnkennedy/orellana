import sys
import tarfile
import os
import ftplib
import shutil
import gzip
import re

##############################
# orellana - viewer of amazon log files #
# john kennedy - johngkennedy4@gmail.com
#		 john.kennedy@sas.com until 8/7/2015

# francisco de orellana - spanish explorer
	# first known navigation of the entire Amazon river


######################################################
# methods

#getting local ip address
#ask stackoverflow - i don't know why this works
def get_ip():
	ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	ip.connect( ("google.com", 80) )
	return ip.getsockname()[0]
	ip.close()

#decompresses a file from filename, writes to filename
def decomp(filename):
        print("decompressing file", filename)
        #finding actual filename, not *.gz
        parts = re.split('\.gz', filename)
        name = parts[0]

        #decompressing file, writing to 'name'
        with gzip.open(filename, mode='rb') as gz:
                file_content = gz.read()

        write = open(name, mode='wb')
        write.write(file_content)
        write.close()
        gz.close()

#tests whether a file is .gz or not
def gztest(filename):
        letters = list(filename)
        if (letters[-1] == 'z' and letters[-2] == 'g'):
                return True
        else:
                return False

print (gztest('test1.gz'))
print (gztest('gztest'))

######################################################
# creating files to be executed later
#

#in case the files need to be changed

os.chdir(r"C:\Users\orellana")

# reading from config file
# first line is plink session name
# second is cluster ip

conf = open("orellana.conf", mode='r')
lines = conf.readlines()

session_name = lines[0]
host = lines[1]

if (len(lines) == 2):
        username = 'anonymous'
        password = ''

else:
        username = lines[2]
        password = lines[3]

conf.close()

print("Creating log zip")
INIT_COMMANDS = "sudo tar -zvcf /var/ftp/pub/logs.tar.gz /mnt/var/log"
CLOSE_COMMANDS = "sudo rm logs.tar.gz"


#writing the files

init = open(".init.sh", "w")
init.write(INIT_COMMANDS)
init.close()

close = open(".close_down.sh", "w")
close.write(CLOSE_COMMANDS)
close.close() 

#######################################################

#session_name = sys.argv[1]

#### TESTING VARIABLES ####
session_name = 'orellana'
host = '10.251.75.219'
username = 'anonymous'
password = ''

#initiating ssh, creating a zip file of logs
print( "initiating ssh" )

#using Plink - command line version of putty

#IT IS NECESSARY FOR A PUTTY SAVED SESSION TO EXIST
print( "compressing, encrypting log files on remote" )
command = "".join( ("plink ", session_name, " -m .init.sh") )
print(os.system(command))

#fetching file with FTP
ftp = ftplib.FTP(host, username, password)

print("Starting FTP download")
ftp.cwd('pub')
print(ftp.pwd())

print('files found:')
print(ftp.nlst())

ftp.retrbinary('RETR test', open('test', 'wb').write)
ftp.retrbinary('RETR logs.tar.gz', open('logs.tar.gz', 'wb').write)
ftp.quit()

#opening tarfile
tar = tarfile.open('logs.tar.gz')
tar.extractall()
tar.close()

#should copy the file structure to where ever its downloaded

#deleting big file on remote
command = "".join( ("plink ", session_name, " -m .close_down.sh") )
print( command )
os.system(command)

#moving directories, cleaning up
if (os.path.exists(r'C:\Users\orellana\logs')):
        shutil.rmtree(r'C:\Users\orellana\logs')
        
shutil.copytree(r'C:\Users\orellana\mnt\var\log', r'C:\Users\orellana\logs')
shutil.rmtree(r'C:\Users\orellana\mnt')

#un gz'ing all files, traversing using os.walk
regex = re.compile('gz')
for root, dirs, files in os.walk("logs"):
        print("changing path to ", root)
        for file in files:
                if (gztest(file)):
                        print("decompressing", file)
                        decomp(root + '\\' + file)
                        print('deleting', file)
                        os.remove(root + '\\' + file)
                else:
                        print('not decompressing', file)
                        next
