from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select


class Rivenmarket:
    def __init__(self, headless):
        self.soup = None
        self.list = None
        self.loading = None
        self.stat1, self.error1 = None, None
        self.stat2, self.error2 = None, None
        self.stat3, self.error3 = None, None
        self.stat4, self.error4 = None, None
        self.moddata = None
        self.modlist = []

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

        self.modlist.clear()
        for mod in self.list:
            # TODO odretardzic
            self.stat1, self.error1 = self.__rmkt2sem(mod["data-stat1"], mod["data-wtype"], mod["data-weapon"])
            self.stat2, self.error2 = self.__rmkt2sem(mod["data-stat2"], mod["data-wtype"], mod["data-weapon"])
            self.stat3, self.error3 = self.__rmkt2sem(mod["data-stat3"], mod["data-wtype"], mod["data-weapon"])
            self.stat4, self.error4 = self.__rmkt2sem(mod["data-stat4"], mod["data-wtype"], mod["data-weapon"])
            self.moddata = {"wepid": mod["id"],
                            "wepname": self.__rmkt2semWep(mod["data-weapon"]),
                            "weptype": mod["data-wtype"],
                            "modname": mod["data-name"],
                            "modprice": mod["data-price"],
                            "modage": mod["data-age"],
                            "stat1": self.stat1,
                            "stat2": self.stat2,
                            "stat3": self.stat3,
                            "stat4": self.stat4,
                            "error1": self.error1,
                            "error2": self.error2,
                            "error3": self.error3,
                            "error4": self.error4}
            self.modlist.append(self.moddata)

    def quit(self):
        self.driver.quit()

    def __waitUntilLoaded(self):
        while True:
            self.soup = BeautifulSoup(self.driver.page_source, "lxml")
            self.loading = self.soup.find_all("center")
            sleep(0.05)
            if not self.loading:  # if there is no "Loading" element
                break

    @staticmethod
    def __rmkt2sem(stat, weptype, wepname):
        error = ""
        if stat == "Speed":
            if weptype == "Melee":
                stat += "_m"
            else:
                stat += "_o"
        # BUG: semlar nie ma takiej staty jak dmg w Plague Kripath
        if "_" in wepname and stat == "Damage":
            stat = "Error"
            error = "Error: weapon name with space + Damage"
        return {
                   "": "",
                   "Damage": "% Damage",
                   "Multi": "% Multishot",
                   "Speed_m": "% Attack Speed",
                   "Speed_o": "% Fire Rate",
                   "Corpus": "% Damage to Corpus",
                   "Grineer": "% Damage to Grineer",
                   "Infested": "% Damage to Infested",
                   "Impact": "% Impact",
                   "Puncture": "% Puncture",
                   "Slash": "% Slash",
                   "Cold": "% Cold",
                   "Electric": "% Electricity",
                   "Heat": "% Heat",
                   "Toxin": "Toxin",
                   "ChannelDmg": "% Channeling Damage",
                   "ChannelEff": "% Channeling Efficiency",
                   "Combo": "Combo Duration",
                   "CritChance": "% Critical Chance",
                   "Slide": "% Critical Chance for Slide Attack",
                   "CritDmg": "% Critical Damage",
                   "Finisher": "% Finisher Damage",
                   "Flight": "% Projectile Speed",
                   "Ammo": "% Ammo Maximum",
                   "Punch": "Punch Through",
                   "Reload": "% Reload Speed",
                   "Range": "Range",
                   "StatusC": "% Status Chance",
                   "StatusD": "% Status Duration",
                   "Recoil": "% Weapon Recoil",
                   "Zoom": "% Zoom",
                   "InitC": "Initial Combo",
                   "ComboEfficiency": "% Melee Combo Efficiency",
                   "ComboGainExtra": "% Additional Combo Count Chance",
                   "ComboGainLost": "% Chance to Gain Combo Count",
                   "Magazine": "% Magazine Capacity"
               }.get(stat, "Error"), error

    @staticmethod
    def __rmkt2semWep(wepname):
        return {
            "Kuva_Bramma": "Kuva Bramma",
            "Kuva_Chakkhurr": "Kuva Chakkhurr",
            "Plague_Kripath": "Plague Kripath",
            "Reaper_Prime": "Reaper Prime",
            # TODO: wszystkie bronie
        }.get(wepname, wepname)
