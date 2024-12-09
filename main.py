import requests
import pystray
import os
import time
import configparser
import threading
import re
import sys
from PIL import Image as img


def forceupdate(icon):
    print(threading.current_thread())
    icon.notify('Đừng hối anh...','Updating')
    refreshflag.set()

def edit():
     os.system('config.ini')

def iexit(icon):
    icon.stop()
    flag.set()

def setup(icon):
    icon.visible=1
    icon.notify('Anh đang làm việc...','From J97 with love 💖')

def refresh():
    global username,password,domain,icon
    ip = requests.get('https://api.ipify.org').text
    print(ip)
    site=f'https://{username}:{password}@freedns.afraid.org/nic/update?hostname={domain}&myip={ip}'
    result=str(requests.get(site))
    print(result)
    if re.search(r'(?<=\[).*(?=\])',result).group(0) != '200':
        icon.notify(f'Error: {result}','Có gì đó sai sai 🤔')

image=img.open(r'img\j97.jpg').resize((64,64))
refreshflag=threading.Event()
flag=threading.Event()
icon=pystray.Icon('DNS Updater',image,'Vì tinh tú mang tên J97',pystray.Menu(pystray.MenuItem('Update',forceupdate),
                                                                             pystray.MenuItem('Edit',edit),
                                                                             pystray.MenuItem('Exit',iexit)))
icon.run_detached(setup)
config=configparser.ConfigParser()

if not os.path.exists('config.ini'):
    config['Settings']={'Time':300,
                        'username':'', 
                        'password':'',
                        'domain':''}
    with open('config.ini','w') as file:
        config.write(file)

config.read('config.ini')
ftime=config.getint('Settings','time')
username=config.get('Settings','username')
password=config.get('Settings','password')
domain=config.get('Settings','domain')

while 1:
    refresh()
    for current in range(ftime):
        time.sleep(1)
        if refreshflag.is_set():
            refreshflag.clear()
            break
        if flag.is_set():
            sys.exit()

