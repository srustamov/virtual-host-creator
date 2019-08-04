#!/usr/bin/env python
import os


class Inputs:

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

    def project_type():
        Type = input('\033[93m Project type (default Normal)[1:MVC 2:Normal] \033[0m : ')

        if Type==1:
            Type = 'try_files $uri $uri/ /index.php?$query_string;'
        else:
            Type = 'try_files $uri $uri/ =404;'
        
        return Type

    def hostname():

        host = ''

        while (host==''):
            host = input('\033[93m Site hostname(example example.com) \033[0m : ')
            if host=='':
                print('hostname required! try again')
                continue
            else:
                return host

    def phpfpm_version():
        version = input('\n\033[93m php-fpm version|default(php7.2-fpm): [example php7.2-fpm ]\033[0m :')

        if version == '':
            version = 'php7.2-fpm'
        return version






