from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from time import sleep


class Rivenmarket:
    def __init__(self, headless):
        self.soup = None
        self.list = None
        self.loading = None
        self.options = Options()
        self.options.headless = headless
        print("Opening riven.market")
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.get("https://riven.market/list/PC")
        self.__waitUntilLoaded()
        print("riven.market opened")

    def loadWeapon(self, weapon):
        Select(self.driver.find_element_by_id("list_limit")).select_by_value("200")  # Show 200 Rivens
        Select(self.driver.find_element_by_id("list_recency")).select_by_value("7")  # <7 days
        Select(self.driver.find_element_by_id("list_weapon")).select_by_visible_text(weapon)  # Weapon
        self.driver.execute_script("loadList(1,'price','ASC')")  # price ascending
        self.__waitUntilLoaded()

        self.list = self.soup.find_all("div", class_="riven")

    def quit(self):
        self.driver.quit()

    def __waitUntilLoaded(self):
        while True:
            self.soup = BeautifulSoup(self.driver.page_source, "lxml")
            self.loading = self.soup.find_all("center")
            sleep(0.05)
            if not self.loading:  # if there is no "Loading" element
                break
