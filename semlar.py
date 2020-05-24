import re
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from writer import Writer


class Semlar:
    def __init__(self, headless, filename):
        # TODO odretardzic
        self.soup = None
        self.sales = None
        self.rating = None
        self.wepname = None
        self.stat1, self.error1 = None, None
        self.stat2, self.error2 = None, None
        self.stat3, self.error3 = None, None
        self.stat4, self.error4 = None, None
        self.wepid = None
        self.modname = None
        self.modprice = None
        self.modage = None
        self.weaponbugged = None
        self.weptype = None
        self.statcount = None
        self.cond1, self.cond2, self.cond3 = None, None, None

        self.writer = Writer(filename)
        self.options = Options()
        self.options.headless = headless
        print("Opening semlar")
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.get("https://semlar.com/comp")
        sleep(1)  # TODO lepsze waity
        self.driver.execute_script("window.scrollBy(0,500)")
        sleep(1)
        print("semlar opened")

        # semlar - useful elements
        self.semlar_weapon = self.driver.find_element_by_css_selector("#react-select-2-input")
        self.semlar_weapon_but = self.driver.find_element_by_xpath(
            "/html/body/div/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div/div/div[2]/div")
        self.semlar_buffs = self.driver.find_element_by_css_selector("#react-select-3-input")
        self.semlar_buffs_but = self.driver.find_element_by_xpath(
            "/html/body/div/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div")
        self.semlar_debuffs = self.driver.find_element_by_css_selector("#react-select-4-input")
        self.semlar_debuffs_but = self.driver.find_element_by_xpath(
            "/html/body/div/div[3]/div[2]/div/div[2]/div[1]/div/div[3]/div/div/div[2]/div")
        self.semlar_cmp = self.driver.find_element_by_xpath(
            "/html/body/div/div[3]/div[2]/div/div[3]/button")

    def loadMod(self, mod):
        self.wepid = mod["wepid"]
        self.wepname = mod["wepname"]
        self.weptype = mod["weptype"]
        self.modname = mod["modname"]
        self.modprice = mod["modprice"]
        self.modage = mod["modage"]
        self.stat1 = mod["stat1"]
        self.stat2 = mod["stat2"]
        self.stat3 = mod["stat3"]
        self.stat4 = mod["stat4"]
        self.error1 = mod["error1"]
        self.error2 = mod["error2"]
        self.error3 = mod["error3"]
        self.error4 = mod["error4"]

    def checkRating(self):
        # Semlar weaponname
        self.semlar_weapon_but.click()
        self.semlar_weapon.send_keys(self.wepname)
        self.semlar_weapon.send_keys(Keys.ENTER)
        # Semlar buff1
        self.semlar_buffs_but.click()
        self.semlar_buffs.clear()
        self.semlar_buffs.send_keys(self.stat1)
        self.semlar_buffs.send_keys(Keys.ENTER)
        # Semlar buff2
        self.semlar_buffs.send_keys(self.stat2)
        self.semlar_buffs.send_keys(Keys.ENTER)
        # Semlar buff3
        self.semlar_buffs.send_keys(self.stat3)
        self.semlar_buffs.send_keys(Keys.ENTER)
        # Semlar debuff
        self.semlar_debuffs_but.click()
        self.semlar_debuffs.clear()
        self.semlar_debuffs.send_keys(self.stat4)
        self.semlar_debuffs.send_keys(Keys.ENTER)
        self.semlar_cmp.click()
        sleep(0.1)  # TODO lepsze czekanie
        self.soup = BeautifulSoup(self.driver.page_source, "lxml")
        self.rating = self.soup.find(
            "h1", attrs={"style": re.compile("color: rgb\([0-9]+, [0-9]+, [0-9]+\)")}).text
        self.sales = (self.soup.find(
            "div", attrs={"style": "margin-top: 50px; text-align: center;"}).text.split(": "))[1]

    def loadstats(self, wepname, stat1, stat2, stat3, stat4, wepid, modname, modprice, modage):
        self.wepname = wepname
        self.stat1 = stat1
        self.stat2 = stat2
        self.stat3 = stat3
        self.stat4 = stat4
        self.wepid = wepid
        self.modname = modname
        self.modprice = modprice
        self.modage = modage

    def isWeaponBugged(self):
        # TODO: try catch bo paszyjaja mi placze
        self.weaponbugged = False
        for error in [self.error1, self.error2, self.error3, self.error4]:
            if error != "":
                self.weaponbugged = True
                print(error + "\n" + " \"" + self.stat1 + "\""
                      + " \"" + self.stat2 + "\""
                      + " \"" + self.stat3 + "\""
                      + " \"" + self.stat4 + "\"")
        return self.weaponbugged

    def modMeetsCriteria(self):
        self.statcount = 0
        self.cond1 = True
        for stat in [self.stat1, self.stat2, self.stat3, self.stat4]:
            if not self.__isStatCorrect(stat):
                self.cond1 = False
            if stat != "":
                self.statcount += 1
        self.cond2 = (self.modage == "new" or self.modage == "> 1 day")
        self.cond3 = self.__isModCorrect()
        return self.cond1 and self.cond2 and self.cond3

    def write(self):
        self.writer.writerow(self.wepid, self.wepname, self.modname, self.modprice, self.rating, self.modage,
                             self.sales, self.stat1, self.stat2, self.stat3, self.stat4)

    def writeempty(self):
        self.writer.writeempty()

    def quit(self):
        self.driver.quit()

    def __isStatCorrect(self, stat):  # TODO: areStatsCorrect
        if self.weptype == "Melee":
            if stat == "% Ammo Maximum":
                # TODO: wszystkie przypadki
                return False
        return True

    def __isModCorrect(self):
        self.stats = [self.stat1, self.stat2, self.stat3, self.stat4]
        if self.statcount >= 3 and len(set(self.stats)) == len(self.stats):
            return True
        elif self.statcount == 2 and len(set(self.stats)) == 3:
            return True
        else:
            return False
