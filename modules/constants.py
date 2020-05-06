import os

BASE_PATH = os.path.abspath('.')
NGINX_CONF_FILE = os.path.join(BASE_PATH, 'conf/nginx.conf')
NGINX_SITES_CONF_FILE = '/etc/nginx/sites-available/%s.conf'
NGINX_SITES_ENABLED = '%s /etc/nginx/sites-enabled/'
HOSTS_FILE = '/etc/hosts'
DEFAULT_PHP_FPM_VERSION = 'php7.3-fpm'
