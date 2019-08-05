#!/usr/bin/env python
import os
import re


class Inputs:

    @staticmethod
    def root_dir():
        while True:
            print('Site Root Folder\n')
            print('Default /var/www/html/ \n ')
            root = input('\033[93m Example [/var/www/html/test/public] \033[0m :')

            if root=='':
                root = "/var/www/html"
            elif root[-1:] =='/':
                root = root[:-1]

            if not os.path.isdir(root):
                print(root+' folder not found\n')
                continue
            else:
                return root.strip()
    @staticmethod
    def project_type():
        try:
            Type = int(input('\033[93m Project type (default Normal)[1:MVC 2:Normal] \033[0m : '))
        except ValueError:
	        Type = 2
        if Type==1:
            Type = 'try_files $uri $uri/ /index.php?$query_string;'
        else:
            Type = 'try_files $uri $uri/ =404;'
        
        return Type

    @staticmethod
    def hostname():
        host = ''
        while (host==''):
            host = input('\033[93m Site hostname(example example.com) \033[0m : ')
            if host=='':
                print('hostname required! try again')
                continue
            else:
                return host
    
    @staticmethod
    def phpfpm_version():
        version = input('\n\033[93m php-fpm version|default(php7.2-fpm): [example php7.2-fpm ]\033[0m :')
        if version == '':
            version = 'php7.2-fpm'
        return version





def check_host(hostsfile,hostname):
    with open(hostsfile) as fp:
        line = fp.readline()
        while line:
            if re.match(r'^127.0.0.1([\s\t]+)'+hostname+'$',line,re.M|re.I):
                return line
            line = fp.readline()
    return False

def delete_host(hostsfile,hostname):
    l = check_host(hostsfile,hostname)
    if l:
        with open(hostsfile, "r") as f:
            lines = f.readlines()
        with open(hostsfile, "w") as f:
            for line in lines:                
                if line.strip("\n") != l.strip("\n"):
                    f.write(line)




