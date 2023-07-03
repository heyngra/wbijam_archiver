import os
import time
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def load_json():
    import json
    if (os.path.exists('wbijam.json') == False):
        with open('wbijam.json', 'w') as f:
            json.dump([], f, indent=4)
    with open('wbijam.json', 'r') as f:
        return json.load(f)

def save_json(data):
    import json
    with open('wbijam.json', 'w') as f:
        json.dump(data, f, indent=4)


animce = load_json()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
anime = ["https://86.wbijam.pl/","https://accelworld.wbijam.pl/","https://akudama.wbijam.pl/","https://appare.wbijam.pl/","https://arifureta.wbijam.pl/","https://ap.wbijam.pl/","https://blackclover.wbijam.pl/","https://bleach.wbijam.pl/","https://bluelock.wbijam.pl/","https://chainsawman.wbijam.pl/","https://clannad.wbijam.pl/","https://codegeass.wbijam.pl/","https://danmachi.wbijam.pl/","https://dg.wbijam.pl/","https://decadence.wbijam.pl/","https://drstone.wbijam.pl/","https://enen.wbijam.pl/","https://fairytail.wbijam.pl/","https://fulldive.wbijam.pl/","https://fumetsu.wbijam.pl/","https://genkoku.wbijam.pl/","https://gintama.wbijam.pl/","https://gleipnir.wbijam.pl/","https://gs.wbijam.pl/","https://hachinan.wbijam.pl/","https://idaten.wbijam.pl/","https://hunter.wbijam.pl/","https://dendrogram.wbijam.pl/","https://jigokuraku.wbijam.pl/","https://jujutsu.wbijam.pl/","https://knt.wbijam.pl/","https://knm.wbijam.pl/","https://klk.wbijam.pl/","https://kny.wbijam.pl/","https://kimisen.wbijam.pl/","https://kyokousuiri.wbijam.pl/","https://loghorizon.wbijam.pl/","https://mia.wbijam.pl/","https://magi.wbijam.pl/","https://mashle.wbijam.pl/","https://mt.wbijam.pl/","https://naruto.wbijam.pl/","https://ngnl.wbijam.pl/","https://onepiece.wbijam.pl/","https://oshinoko.wbijam.pl/","https://ousamaranking.wbijam.pl/","https://overlord.wbijam.pl/","https://plunderer.wbijam.pl/","https://rezero.wbijam.pl/","https://sentouin.wbijam.pl/","https://shinchou.wbijam.pl/","https://snk.wbijam.pl/","https://sololeveling.wbijam.pl/","https://somali.wbijam.pl/","https://spyxfamily.wbijam.pl/","https://sng.wbijam.pl/","https://swordartonline.wbijam.pl/","https://tate.wbijam.pl/","https://slime.wbijam.pl/","https://goh.wbijam.pl/","https://ynn.wbijam.pl/", "https://inne.wbijam.pl/"]
def get_cda(nazwa, anime, rel, seria, plik):
    driver.get(nazwa + "odtwarzacz-" + rel + ".html")
    time.sleep(0.2)
    link = driver.execute_script(
        "var x = document.evaluate(`//*[text()='TUTAJ']`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;return (x!=null)?x.href:0")
    print(str(plik) + " " + str(link))
    if anime == 'inne':
        animce.append({"nazwa": seria.split("https://inne.wbijam.pl/")[1].split(".html")[0], "seria": seria, "plik": plik, "link": link})
    else:
        animce.append({"nazwa": anime, "seria": seria, "plik": plik, "link": link})
    time.sleep(0.2)

try:
    for nazwa in anime:
        print(nazwa)
        driver.get(nazwa)
        x = driver.execute_script("var x = document.evaluate(`//*[text()='Odcinki anime online' or text()='Akcja' or text()='Lżejsze klimaty']`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;var b=x.nextElementSibling;linki=[];for(const obj of b.children){if(obj.getElementsByTagName(`img`)[0].src.endsWith(`images/tv_info.gif`)){linki.push(obj.getElementsByTagName(`a`)[0].href)}};return linki;")
        for seria in x:
            driver.get(seria)
            print(seria)
            y = driver.execute_script("var lista=[];for(const x of document.querySelector(`#tresc_lewa>table`).children[0].children){for(const odcinek of x.children){var td0=odcinek.children[0];console.log(td0);if(!td0){continue}td1=td0.href;console.log(td1);if(!td1&&td0.hasAttribute(`rel`)&&td0.getAttribute(`rel`).startsWith(`_PLU`)){td1=[td0.getAttribute(`rel`),td0.parentElement.parentElement.children[0].textContent]}if(td1||(typeof td1==Array&&(td1[0]||td[1])&&td1[0].startsWith(`_PLU`))){lista.push(td1);break}}};return lista;")
            for odcinek in y:
                print(odcinek)
                if type(odcinek) == list and not odcinek[0].startswith("https://"):
                    get_cda(nazwa, nazwa.split("https://")[1].split(".wbijam.pl")[0], odcinek[0], seria, odcinek[1])
                    continue
                driver.get(odcinek)
                time.sleep(0.2)
                seria_nr = driver.execute_script("var x = document.evaluate(`//*[text()='Seria:']`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;return x.nextSibling.textContent")
                nr_odcinka = driver.execute_script("var x = document.evaluate(`//*[text()='Numer odcinka:' or text()='Numer porządkowy:']`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;return (x!=null)?x.nextSibling.textContent:0")
                polski_tytul = driver.execute_script("return document.querySelector(`#tresc_lewa > h1`).innerText.slice(0,-1)")
                rel = driver.execute_script("var x = document.evaluate(`//*[text()='cda']//..//span[starts-with(text(),'oglądaj') or starts-with(text(),'zwiastun')]`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;return (x!=null)?x.getAttribute(`rel`):null")
                if not rel or seria_nr+" "+polski_tytul in [x["plik"] for x in animce]:
                    print("Already downloaded!")
                    continue
                get_cda(nazwa, nazwa.split("https://")[1].split(".wbijam.pl")[0], rel, seria, polski_tytul)
            time.sleep(0.5)
        time.sleep(1.0)
    save_json(animce)
    print("Completed! :)")
except Exception:
    print(traceback.format_exc())
    save_json(animce)
