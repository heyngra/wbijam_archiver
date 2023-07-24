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
driver.get("https://wbijam.pl")
anime = driver.execute_script("""anime=[];for (const x of document.evaluate(`//*[text()="Lista anime
      "]`, document, null,XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.nextElementSibling.children){anime.push(x.href)};return anime;""")
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
