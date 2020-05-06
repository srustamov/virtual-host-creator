import os
import click
import modules.message as message

from modules.constants import DEFAULT_PHP_FPM_VERSION

def root_dir():
    while True:
        root = click.prompt(message.info(
            'Input site Root Folder', True), type=str, default='/var/www/html/')

        if root[-1:] == '/':
            root = root[:-1]

        if not os.path.isdir(root):
            print('%s folder not found\n'%root)
            continue
        else:
            return root.strip()


def project_type():
    try:
        print('1 : MVC')
        print('2 : NORMAL')
        project_type = click.prompt(message.info(
            'Input project type', True), type=int, default=2)
    except ValueError:
        project_type = 2

    if project_type == 1:
        return 'try_files $uri $uri/ /index.php?$query_string;'
    return 'try_files $uri $uri/ =404;'


def hostname():
    hostname = ''
    while (hostname == ''):
        hostname = (click.prompt(message.info('Input hostname', True), type=str)).strip(' \t\n\r')

        if hostname == '':
            message.error('Hostname required! try again')
            continue
        else:
            return hostname


def phpfpm_version():
    version = (click.prompt(message.info(
            'Input php-fpm:', True), type=str, default=DEFAULT_PHP_FPM_VERSION)).strip(' \t\n\r')
    return version
