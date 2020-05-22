import re
from datetime import timedelta
from time import sleep, time
from playsound import playsound
from BotFunctions import rmkt2sem, rmkt2semWep, isStatCorrect, isModCorrect
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import csv

start_time = time()
weapons = [
           # "Kuva Bramma",
           # "Lanka",
           # "Rubico",
           # "Vectis",
           # "Corinth",
           # "Redeemer",
           # "Kohm",
           #"Gram",
           #"Opticor",      #uncommon
           #"Kronen",
           #"Catchmoon",
           #"Nukor",
           #"Kuva Chakkhurr",
           #"Amprex",       #uncommon
           #"Shedu",
           #"Acceltra",
           #"Lenz",         #uncommon
           #"Dread",        #uncommon
           "Plague Kripath",
           #"Basmu"]        #uncommon
           ]

# writing to .csv
rmkt_csv = open("rlst.csv", mode='w', newline='')
rmkt_writer = csv.writer(rmkt_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
rmkt_writer.writerow(["id", "weapon", "name", "price", "rating", "age", "sales", "Buff1", "Buff2", "Buff3", "Debuff"])

rmkt_driver = webdriver.Firefox()
semlar_driver = webdriver.Firefox()
rmkt_driver.get("https://riven.market/list/PC")
semlar_driver.get("https://semlar.com/comp")
sleep(1)
semlar_driver.execute_script("window.scrollBy(0,500)")
sleep(1)

# semlar - useful elements
semlar_weapon = semlar_driver.find_element_by_css_selector("#react-select-2-input")
semlar_weapon_but = semlar_driver.find_element_by_xpath(
    "/html/body/div/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div/div/div[2]/div")
semlar_buffs = semlar_driver.find_element_by_css_selector("#react-select-3-input")
semlar_buffs_but = semlar_driver.find_element_by_xpath(
    "/html/body/div/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div")
semlar_debuffs = semlar_driver.find_element_by_css_selector("#react-select-4-input")
semlar_debuffs_but = semlar_driver.find_element_by_xpath(
    "/html/body/div/div[3]/div[2]/div/div[2]/div[1]/div/div[3]/div/div/div[2]/div")
semlar_cmp = semlar_driver.find_element_by_xpath(
    "/html/body/div/div[3]/div[2]/div/div[3]/button")

for weapon in weapons:
    print("---Scanning " + weapon + "---")
    Select(rmkt_driver.find_element_by_id("list_limit")).select_by_value("200")  # Show 200 Rivens
    Select(rmkt_driver.find_element_by_id("list_recency")).select_by_value("7")  # <7 days
    Select(rmkt_driver.find_element_by_id("list_weapon")).select_by_visible_text(weapon)  # Weapon
    rmkt_driver.execute_script("loadList(1,'price','ASC')")  # price ascending
    sleep(2)

    rmkt_soup = BeautifulSoup(rmkt_driver.page_source, "lxml")
    rmkt_list = rmkt_soup.find_all("div", class_="riven")
    for list_el in rmkt_list:
        wepid = list_el["id"]
        wepname = rmkt2semWep(list_el["data-weapon"])
        weptype = list_el["data-wtype"]
        modname = list_el["data-name"]
        modprice = list_el["data-price"]
        modage = list_el["data-age"]
        stat1, error1 = rmkt2sem(list_el["data-stat1"], weptype, wepname)
        stat2, error2 = rmkt2sem(list_el["data-stat2"], weptype, wepname)
        stat3, error3 = rmkt2sem(list_el["data-stat3"], weptype, wepname)
        stat4, error4 = rmkt2sem(list_el["data-stat4"], weptype, wepname)

        cont = False;
        for error in [error1, error2, error3, error4]:
            if error != "":
                cont = True
                print(error+"\n"+" \""+list_el["data-stat1"]+"\""
                      " \""+list_el["data-stat2"]+"\""
                      " \""+list_el["data-stat3"]+"\""
                      " \""+list_el["data-stat4"]+"\"")
        if cont:
            continue

        statc = 0
        cond1 = True
        for stat in [stat1, stat2, stat3, stat4]:
            if not isStatCorrect(stat, weptype):
                cond1 = False
            if stat != "":
                statc = statc + 1
        cond2 = (list_el["data-age"] == "new" or list_el["data-age"] == "> 1 day")
        cond3 = isModCorrect(stat1, stat2, stat3, stat4, weptype, statc)

        if cond1 and cond2 and cond3:
            # Semlar weaponname
            semlar_weapon_but.click()
            semlar_weapon.send_keys(wepname)
            semlar_weapon.send_keys(Keys.ENTER)
            # Semlar buff1
            semlar_buffs_but.click()
            semlar_buffs.clear()
            semlar_buffs.send_keys(stat1)
            semlar_buffs.send_keys(Keys.ENTER)
            # Semlar buff2
            semlar_buffs.send_keys(stat2)
            semlar_buffs.send_keys(Keys.ENTER)
            # Semlar buff3
            semlar_buffs.send_keys(stat3)
            semlar_buffs.send_keys(Keys.ENTER)
            # Semlar debuff
            semlar_debuffs_but.click()
            semlar_debuffs.clear()
            semlar_debuffs.send_keys(stat4)
            semlar_debuffs.send_keys(Keys.ENTER)
            semlar_cmp.click()
            sleep(0.1)
            # write to csv
            semlar_soup = BeautifulSoup(semlar_driver.page_source, "lxml")
            rating = semlar_soup.find_all("h1")
            print("test")
            print(rating)
            sales = "debug"
            #rating = semlar_list[2].text
            #sales = semlar_list[1].text.split(': ')[1]
            rmkt_writer.writerow([wepid, wepname, modname, modprice, rating, modage, sales, stat1, stat2, stat3, stat4])
    rmkt_writer.writerow([])

rmkt_csv.close()
print("---DONE---")
playsound("sound.wav")
time_elapsed = time() - start_time
print("Time Elapsed " + str(timedelta(seconds=time_elapsed)))
