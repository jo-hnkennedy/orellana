import os
import re
import ftplib
import subprocess
import urllib

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
        print("connecting to plink remote server")
        ftp = ftplib.FTP('ftp.chiark.greenend.org.uk', 'anonymous', '@anonymous')
        ftp.cwd('users/sgtatham/putty-latest/x86')

        print("downloading plink")
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


###########################################################

#installing pLink

#checking for existing orellana directory, making if not
if (os.path.exists(r"C:\Users\orellana")):
        #directory exists
        print("found orellana directory")

else:
        os.mkdir(r"C:\Users\orellana")

os.chdir(r"C:\Users\orellana")

#creating config file
session_name = input("Putty session name: ")
home = input("Cluster IP Address: ")

print(r"These values can be changed in the orellana.conf file in C:\Users\orellana")

conf = open("orellana.conf", mode="w")
conf_write = "".join( (session_name, "\n", home, "\n") )
conf.write(conf_write)
conf.close()

####################
# installing plink #
####################

print("installing plink in orellana")
install_plink()

print("plink installed")

#adding orellana to path 
os.system(r"set PATH=%PATH%;C:\Users\orellana")

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

#### downloading main orellana python file ####
urllib.urlretrieve("https://raw.githubusercontent.com/jo-hnkennedy/orellana/master/orellana.py", "orellana.py")
