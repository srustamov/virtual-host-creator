#!/usr/bin/env python
import os
import itertools
import threading
import time
import sys
from client import Inputs,check_host


if __name__ == "__main__":
    if os.getenv("SUDO_USER") == None:
        exit('\033[91m Please start the script as root!\033[0m')
else:
    exit('\033[91m Script exit! \033[0m')

FILES = {
    'user-conf-file':'./nginx-conf.txt',
    'conf-file':"/etc/nginx/sites-available/%s.conf",
    'conf-symbolic-link':'%s /etc/nginx/sites-enabled/',
    'hosts':'/etc/hosts'
}

if os.path.exists(FILES['user-conf-file']):
    with open(FILES['user-conf-file'], 'r') as file:
         content = file.read()
else:
    exit('\033[91m %s not found \033[0m' %(FILES['user-conf-file']))

print('\033[95m'+"""
***************************************************************************************
*                                                                                     *
*                         NGINX SIMPLE VIRTUAL HOST CREATOR                           *
*                              For Ubuntu machines                                    *
*                                                                                     *
***************************************************************************************
"""+'\033[0m')

try:
    ROOT = Inputs.root_dir()
    PROJECT_TYPE = Inputs.project_type()
    PHPFPM_VERSION = Inputs.phpfpm_version()
    HOSTNAME = Inputs.hostname()
except KeyboardInterrupt:
    exit('\nBye!\n')
except:
    exit('\033[91m Error! Something went wrong :( \n \033[0m')


content = content.replace('__ROOT__',ROOT)
content = content.replace('__HOST__',HOSTNAME)
content = content.replace('__TYPE__',PROJECT_TYPE).replace('__PHP__',PHPFPM_VERSION)

CHANGE_CONTENT = input(' \033[92mDo you want to modify the .conf file? \033[0m [y/N]:')

if CHANGE_CONTENT.lower() == 'y':
    try:
        fruntime_conf = open('./'+HOSTNAME+'.conf', "w")
        fruntime_conf.write(content)
        fruntime_conf.close()
        os.system('sudo nano '+'./'+HOSTNAME+'.conf')
        if os.path.exists('./'+HOSTNAME+'.conf'):
            with open('./'+HOSTNAME+'.conf', 'r') as file:
                  content = file.read()
        os.system('sudo rm ./'+HOSTNAME+'.conf')
    except:
       print('\033[91m Error! Something went wrong :( \033[0m \n') 




fconf = open(FILES['conf-file'] %(HOSTNAME), "w")
symbolic_link = FILES['conf-symbolic-link'] %(FILES['conf-file'] %(HOSTNAME))
creating = False


def creating_animate():
    for c in itertools.cycle(['|', '/', '-' ,'\\']):
        if creating:
            break
        sys.stdout.write('\r Creating virtual host ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    

t = threading.Thread(target=creating_animate)
t.start()

if fconf:
    write = fconf.write(content)
    if write:
        fconf.close()
        try:
            if os.path.exists('/etc/nginx/sites-enabled/'+HOSTNAME+'.conf'):
                os.system('sudo rm /etc/nginx/sites-enabled/'+HOSTNAME+'.conf')
            os.system('sudo ln -s '+symbolic_link)
            if not check_host(FILES['hosts'],HOSTNAME):
                fhosts = open(FILES['hosts'], "a")
                fhosts.write('127.0.0.1\t'+HOSTNAME+"\n")
                fhosts.close()
            os.system('sudo service nginx restart')
            creating = True
            print('\n\033[92m Virtual host successfully created.Hostname: http://'+HOSTNAME+'\033[0m')
            print('\n\033[1m\033[104m Restart nginx before running\033[0m\033[0m\n')
        except:
            exit('\033[91m Error! Something went wrong :( \n \033[0m')
    else:
        exit('\033[91m The .conf file could not be written. Something went wrong :( \033[0m')
        
else:
    exit('\033[91m The .conf file was not openning. Something went wrong :( \033[0m')
            