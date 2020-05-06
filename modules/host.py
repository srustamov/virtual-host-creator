import re
import os


def check(hostsfile, hostname):
    with open(hostsfile) as fp:
        line = fp.readline()
        while line:
            if re.match(r'^127.0.0.1([\s\t]+)'+hostname+'$', line, re.M | re.I):
                return line
            line = fp.readline()
    return False

def delete(hostsfile, hostname):
    l = check(hostsfile, hostname)
    if l:
        with open(hostsfile, "r") as f:
            lines = f.readlines()
        with open(hostsfile, "w") as f:
            for line in lines:
                if line.strip("\n") != l.strip("\n"):
                    f.write(line)

def restart():
    os.system('sudo service nginx restart')
