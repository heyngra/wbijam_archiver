from __future__ import unicode_literals

import colorama

colorama.init(autoreset=True)
import json
import os
import re
from tkinter import Tk
from tkinter.filedialog import askopenfile

from colorama import Fore, Style
from yt_dlp import YoutubeDL

Tk().withdraw()
print("Wybierz plik .json z danymi wygenerowanymi przez main.py")
file = askopenfile()
if file is None:
    exit(1)
def load_json(file):
    return json.load(file)

data = load_json(file)

animce = list(dict.fromkeys([x['nazwa'] for x in data if type(x['nazwa']) == str]))

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print(Fore.GREEN+'\nPobieranie zakończone!'+Style.RESET_ALL)
    if d['status'] == 'downloading':
        p = d['_percent_str']
        p = p.replace('%', '')
        tekst = d['filename']+" "+Fore.CYAN+p+Fore.GREEN+"%"+" "+Fore.YELLOW+d['_eta_str']
        print(tekst, end='\r')


to_dl = {}
for anime in animce:
    to_dl[anime] = False
def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
def wypisz_anime():
    clear()
    for i, anime in enumerate(animce):
        print(f"[{i}] [{Fore.GREEN+'✓'+Style.RESET_ALL if to_dl[anime] else Fore.RED+'𐄂'+Style.RESET_ALL}] -  {anime}")
    print("Wybierz z listy podane anime, które chcesz pobrać. Wpisz liczbę i enter by zmienić chęć pobrania. Wpisz rdy i enter by zacząć pobieranie. Wpisz a by włączyć wszystkie, wpisz n by wyłączyć wszystkie.")
    x = input("Wybór: ")
    if x == "a":
        for x in to_dl:
            to_dl[x] = True
        wypisz_anime()
    elif x == "n":
        for x in to_dl:
            to_dl[x] = False
        wypisz_anime()
    elif x == "rdy":
        return
    elif x.isdigit() and int(x) < len(animce):
        to_dl[animce[int(x)]] = not to_dl[animce[int(x)]]
        wypisz_anime()
    else:
        wypisz_anime()
wypisz_anime()
clear()
print("Rozpoczynanie pobierania..")
to_dl2 = []
for anime in data:
    if not type(anime['nazwa']) == str:
        continue #this is so corrupted json won't crash
    if to_dl[anime['nazwa']]:
        to_dl2.append(anime)

for odcinek in to_dl2:
    print("Rozpoczynanie pobierania "+Fore.BLUE+odcinek["plik"]+"\n")
    file_name = re.sub('[^\w_. -]', '_', odcinek['plik'])
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f"anime/{odcinek['nazwa']}/{file_name}.%(ext)s",
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'sleep_interval:': 3,
        'max_sleep_interval': 5,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([odcinek["link"]])
