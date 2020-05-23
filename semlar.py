from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import re

class Semlar:
    def __init__(self, headless):
        self.soup = ""
        self.sales = ""
        self.rating = ""

        self.options = Options()
        self.options.headless = False
        print("Opening semlar")
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.get("https://semlar.com/comp")
        sleep(1)    #TODO lepsze waity
        self.driver.execute_script("window.scrollBy(0,500)")
        sleep(1)

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

    def checkStat(self, wepname, stat1, stat2, stat3, stat4):
        # Semlar weaponname
        self.semlar_weapon_but.click()
        self.semlar_weapon.send_keys(wepname)
        self.semlar_weapon.send_keys(Keys.ENTER)
        # Semlar buff1
        self.semlar_buffs_but.click()
        self.semlar_buffs.clear()
        self.semlar_buffs.send_keys(stat1)
        self.semlar_buffs.send_keys(Keys.ENTER)
        # Semlar buff2
        self.semlar_buffs.send_keys(stat2)
        self.semlar_buffs.send_keys(Keys.ENTER)
        # Semlar buff3
        self.semlar_buffs.send_keys(stat3)
        self.semlar_buffs.send_keys(Keys.ENTER)
        # Semlar debuff
        self.semlar_debuffs_but.click()
        self.semlar_debuffs.clear()
        self.semlar_debuffs.send_keys(stat4)
        self.semlar_debuffs.send_keys(Keys.ENTER)
        self.semlar_cmp.click()
        sleep(0.1)  # TODO lepsze czekanie
        self.soup = BeautifulSoup(self.driver.page_source, "lxml")
        self.rating = self.soup.find(
            "h1", attrs={"style": re.compile("color: rgb\([0-9]+, [0-9]+, [0-9]+\)")}).text
        self.sales = (self.soup.find(
            "div", attrs={"style": "margin-top: 50px; text-align: center;"}).text.split(": "))[1]

    def quit(self):
        self.driver.quit()
