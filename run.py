#!/usr/bin/env python
import os
import itertools
import threading
import time
import sys
from modules import message, host, user

from modules.constants import (
    BASE_PATH,
    NGINX_CONF_FILE,
    NGINX_SITES_CONF_FILE,
    NGINX_SITES_ENABLED,
    HOSTS_FILE
)


# if __name__ == "__main__":
#     if os.getenv("SUDO_USER") == None:
#         message.error('Please start the script as root!', False, True)
# else:
#     message.error('Script exit!', False, True)


if len(sys.argv) == 3:
    args = sys.argv
    if args[1].lower() == '--delete':
        hostname = args[2]
        answer = str(input(message.info('Remove virtual host?', True)+'[y/N]:'))
        if answer.lower() == 'y':
            if os.path.exists(NGINX_SITES_CONF_FILE % (hostname)):
                os.system('sudo rm /etc/nginx/sites-*/'+hostname+'.conf')
            host.delete(HOSTS_FILE, hostname)
            host.restart()
            message.success('Virtual host successfully removed', False, True)
        else:
            message.info('bye',False,True)
    else:
        message.error('Parameters are missing')
        message.info('What do you mean?')
        message.success('\t --delete %s' % (args[2]), False, True)


if os.path.exists(NGINX_CONF_FILE):
    with open(NGINX_CONF_FILE, 'r') as file:
        nginx_conf_content = file.read()
else:
    message.error('%s not found' % (NGINX_CONF_FILE), False, True)


message.title()

try:
    ROOT = user.root_dir()
    PROJECT_TYPE = user.project_type()
    PHPFPM_VERSION = user.phpfpm_version()
    HOSTNAME = user.hostname()
except KeyboardInterrupt:
    message.info('Bye', False, True)
except:
    message.error('\nError! Something went wrong :(', False, True)


nginx_conf_content = nginx_conf_content.replace('__ROOT__', ROOT)\
    .replace('__HOST__', HOSTNAME)\
    .replace('__TYPE__', PROJECT_TYPE)\
    .replace('__PHP__', PHPFPM_VERSION)

CHANGE_CONTENT = input(message.info(
    'Do you want to modify the .conf file?', True)+' [y/N]:')

if CHANGE_CONTENT.lower() == 'y':
    try:
        editable_conf_file = os.path.join(BASE_PATH, HOSTNAME)
        fruntime_conf = open(editable_conf_file, "w")
        fruntime_conf.write(nginx_conf_content)
        fruntime_conf.close()
        os.system('sudo nano %s' % editable_conf_file)
        if os.path.exists(editable_conf_file):
            with open(editable_conf_file, 'r') as file:
                nginx_conf_content = file.read()
        os.system('sudo rm %s' % editable_conf_file)
    except:
        message.error('Error! Something went wrong :(')

fconf = open(NGINX_SITES_CONF_FILE % (HOSTNAME), "w")
symbolic_link = NGINX_SITES_ENABLED % (NGINX_SITES_CONF_FILE % (HOSTNAME))

creating = False


def creating_animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if creating:
            break
        sys.stdout.write('\r Creating virtual host ' + c)
        sys.stdout.flush()
        time.sleep(0.1)


t = threading.Thread(target=creating_animate)

t.start()

if fconf:
    write = fconf.write(nginx_conf_content)
    if write:
        fconf.close()
        try:
            if os.path.exists('/etc/nginx/sites-enabled/'+HOSTNAME+'.conf'):
                os.system('sudo rm /etc/nginx/sites-enabled/'+HOSTNAME+'.conf')
            os.system('sudo ln -s %s' % symbolic_link)
            if not host.check(HOSTS_FILE, HOSTNAME):
                fhosts = open(HOSTS_FILE, "a")
                fhosts.write('127.0.0.1\t %s \n' % HOSTNAME)
                fhosts.close()
            host.restart()
            creating = True
            message.success(
                '\nVirtual host successfully created.Hostname: http://%s\n' % HOSTNAME)
            message.info('Restart nginx before running')
        except:
            message.error('Error! Something went wrong :(', False, True)
    else:
        message.error(
            'The .conf file could not be written. Something went wrong :(', False, True)

else:
    message.error(
        'The .conf file was not openning. Something went wrong :(', False, True)
