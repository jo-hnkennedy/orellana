import os
import re
import ftplib
import subprocess

###########################################################
# orellana_installer - installs orellana and its dependents
# 
# francisco de orellana - first known navigator of entire Amazon river
# orellana.py - navigates amazon web services log files
#
# created and maintained by john kennedy - johngkennedy4@gmail.com

###########################################################
# subroutines

#downloads plink
def install_plink():
        #plink is not installed
        ftp = ftplib.FTP('ftp.chiark.greenend.org.uk', 'anonymous', '@anonymous')
        ftp.cwd('users/sgtatham/putty-latest/x86')
        
        #downloading plink, printing out what ever the output of plink download is
        print (ftp.retrbinary('RETR plink.exe', open('plink.exe', 'wb').write))
        ftp.quit()
        return True

#copies plink from the cwd to orellana dir
def copy_plink():
        plink_dir = os.getcwd()
        print("plink found in ", plink_dir)

        #copying plink to orellana directory
        command = "".join( ("cp ", plink_dir, "\plink.exe ~\orellana\plink.exe") ) 
        print(command)
        os.system(command)
        return True

# returns a bool if error during command or not 
# output('dsjfjds') -> false 
# output('echo hello') -> true

def output(command):
        f = os.popen(command, "r")
        lines = f.readlines()
        f.close()
        if (len(lines) == 0):   
                return False
        else:
                return True 

###########################################################

#installing pLink

#testing to see if plink is installed
plink_test = output("plink --version")

#checking for existing orellana directory, making if not
if (os.path.exists("%USERPROFILE%orellana")):
        #directory exists
        print("found orellana directory")

else:
        os.mkdir("%USERPROFILE%orellana")

os.chdir("%USERPROFILE%orellana")

####################
# installing plink #
####################

print("checking for plink")

if (plink_test):
        print("plink found, copying to orellana directory")
        copy_plink()

else:
        plink_dir = input("plink not found: look in other directory? [dir/N] ")
        if (plink_dir == '' or plink_dir == 'N'):
                #not looking anywhere else, installing plink
                install_plink()

        else:
                print(plink_dir)
                os.chdir(plink_dir)
                print("looking for plink")
                print(os.chdir(plink_dir))
                if (output('\.plink --version')):
                        copy_plink()

                else:
                        print("plink not found here")
                        print("installing plink in orellana directory")
                        os.chdir()
                        os.chdir("orellana")
                        install_plink()


print("plink installed")

#adding orellana to path 
os.system("set PATH=%PATH%;%USERPROFILE\orellana")

################################
# setting up web server on AWS #
################################

print("seting up web server")

WEB_INIT_COMMANDS = 'sudo yum update -y; sudo yum install -y httpd24; sudo service httpd start; sudo ckhconfig httpd on'
FTP_INIT_COMMANDS = 'sudo yum -y install vsftpd; sudo service vsftpd start'

# creating init web server file

web_init = open("web_init.sh", "w")
web_init.write(WEB_INIT_COMMANDS)
web_init.close()

# ditto for FTP
ftp_init = open("ftp_init.sh", "w")
ftp_init.write(FTP_INIT_COMMANDS)
ftp_init.close()

print("close command prompt window to finish")

# running init web server script via newly-installed plink

print("setting up apache on server")
session_name = r'orellana'

webInit_command = "".join( ("plink ", session_name, " -m web_init.sh") )
print(webInit_command)

os.system(webInit_command)

# setting up ftp script
print("setting up ftp on server")
ftp_command = "".join( ("plink ", session_name, " -m ftp_init.sh") )
print(ftp_command)
os.system(ftp_command)

#### apache root is /var/www, creating server at /var/www/logs ####

#### running script to sync logs to /var/www/logs ####
sync_command = "".join( ("plink ", session_name, " -m sync.sh") )
print(sync_command)
os.system(sync_command)

