from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from time import sleep


class Rivenmarket:
    def __init__(self, headless):
        # zeby mi nie podkreslalo gnoji
        self.soup = None
        self.list = None
        self.loading = None
        self.wepid = None
        self.wepname = None
        self.weptype = None
        self.modname = None
        self.modprice = None
        self.modage = None
        self.stat1, self.error1 = None, None
        self.stat2, self.error2 = None, None
        self.stat3, self.error3 = None, None
        self.stat4, self.error4 = None, None
        self.statcount = None
        self.weaponbugged = None
        self.cond1, self.cond2, self.cond3 = None, None, None

        self.options = Options()
        self.options.headless = headless
        print("Opening riven.market")
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.get("https://riven.market/list/PC")
        print("riven.market opened")

    def loadWeapon(self, weapon):
        print("---Scanning " + weapon + "---")
        Select(self.driver.find_element_by_id("list_limit")).select_by_value("200")  # Show 200 Rivens
        Select(self.driver.find_element_by_id("list_recency")).select_by_value("7")  # <7 days
        Select(self.driver.find_element_by_id("list_weapon")).select_by_visible_text(weapon)  # Weapon
        self.driver.execute_script("loadList(1,'price','ASC')")  # price ascending

        # TODO: Zrobic zeby to gnojstwo dzialalo
        # WebDriverWait(rmkt_driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "center")))
        while True:
            self.soup = BeautifulSoup(self.driver.page_source, "lxml")
            self.loading = self.soup.find_all("center")
            sleep(0.05)
            if not self.loading:  # if there is no "Loading" element
                break

        self.list = self.soup.find_all("div", class_="riven")

    def loadMod(self, mod):
        self.wepid = mod["id"]
        self.wepname = self.__rmkt2semWep(mod["data-weapon"])
        self.weptype = mod["data-wtype"]
        self.modname = mod["data-name"]
        self.modprice = mod["data-price"]
        self.modage = mod["data-age"]
        self.stat1, self.error1 = self.__rmkt2sem(mod["data-stat1"])
        self.stat2, self.error2 = self.__rmkt2sem(mod["data-stat2"])
        self.stat3, self.error3 = self.__rmkt2sem(mod["data-stat3"])
        self.stat4, self.error4 = self.__rmkt2sem(mod["data-stat4"])

    def isWeaponBugged(self):
        #TODO: try catch bo paszyjaja mi placze
        self.weaponbugged = False
        for error in [self.error1, self.error2, self.error3, self.error4]:
            if error != "":
                self.weaponbugged = True
                print(error+"\n"+" \""+self.stat1+"\""
                      + " \""+self.stat2+"\""
                      + " \""+self.stat3+"\""
                      + " \""+self.stat4+"\"")
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

    @staticmethod
    def __rmkt2semWep(wepname):
        return {
            "Kuva_Bramma": "Kuva Bramma",
            "Kuva_Chakkhurr": "Kuva Chakkhurr",
            "Plague_Kripath": "Plague Kripath",
            "Reaper_prime": "Reaper Prime",
            # TODO: wszystkie bronie
        }.get(wepname, wepname)

    def __rmkt2sem(self, stat):
        error = ""
        if stat == "Speed":
            if self.weptype == "Melee":
                stat += "_m"
            else:
                stat += "_o"
        # BUG: semlar nie ma takiej staty jak dmg w Plague Kripath
        if self.wepname == "Plague Kripath" and stat == "Damage":
            stat = "Error"
            error = "Error: Plague Kripath + Damage"
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
