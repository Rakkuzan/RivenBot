from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

def rmkt2semWep(str):
    return {
        "Kuva_Bramma" : "Kuva Bramma",
        "Kuva_Chakkhurr" : "Kuva Chakkhurr",
        "Plague_Kripath" : "Plague Kripath",
        #TODO: wszystkie bronie
    }.get(str,str)

def rmkt2sem(stat, weptype, wepname):
    error = ""
    if stat == "Speed":
        if weptype == "Melee":
            stat += "_m"
        else:
            stat += "_o"
    #BUG: semlar nie ma takiej staty jak dmg w Plague Kripath
    if wepname == "Plague Kripath" and stat == "Damage":
        str = "Error"
        error = "Error: Plague Kripath + Damage"
    return {
        "" : "",
        "Damage" : "% Damage",
        "Multi" : "% Multishot",
        "Speed_m" : "% Attack Speed",
        "Speed_o" : "% Fire Rate",
        "Corpus" : "% Damage to Corpus",
        "Grineer" : "% Damage to Grineer",
        "Infested": "% Damage to Infested",
        "Impact" : "% Impact",
        "Puncture" : "% Puncture",
        "Slash" : "% Slash",
        "Cold" : "% Cold",
        "Electric" : "% Electricity",
        "Heat" : "% Heat",
        "Toxin" : "Toxin",
        "ChannelDmg" : "% Channeling Damage",
        "ChannelEff": "% Channeling Efficiency",
        "Combo" : "Combo Duration",
        "CritChance" : "% Critical Chance",
        "Slide" : "% Critical Chance for Slide Attack",
        "CritDmg" : "% Critical Damage",
        "Finisher" : "% Finisher Damage",
        "Flight" : "% Projectile Speed",
        "Ammo" : "% Ammo Maximum",
        "Punch" : "Punch Through",
        "Reload" : "% Reload Speed",
        "Range" : "Range",
        "StatusC" : "% Status Chance",
        "StatusD" : "% Status Duration",
        "Recoil" : "% Weapon Recoil",
        "Zoom" : "% Zoom",
        "InitC" : "Initial Combo",
        "ComboEfficiency" : "% Melee Combo Efficiency",
        "ComboGainExtra" : "% Additional Combo Count Chance",
        "ComboGainLost": "% Chance to Gain Combo Count",
        "Magazine" : "% Magazine Capacity"
    }.get(stat, "Error"), error

def isStatCorrect(stat, weptype): #TODO: areStatsCorrect
    if weptype == "Melee":
        if stat == "% Ammo Maximum":
            # TODO: wszystkie przypadki
            return False
    return True

def isModCorrect(stat1, stat2, stat3, stat4, weptype, statc):
    if statc >= 3:
        # staty rozne od siebie
        cond = (not ((stat1 == stat2)
                      or (stat1 == stat3)
                      or (stat1 == stat4)
                      or (stat2 == stat3)
                      or (stat2 == stat4)
                      or (stat3 == stat4)))
        # staty rozne od siebie z wyjatkiem ""
    elif statc == 2:
        cond = (not (
                ((stat1 == stat2) and (not stat1 == ""))
                or ((stat1 == stat3) and (not stat1 == ""))
                or ((stat1 == stat4) and (not stat1 == ""))
                or ((stat2 == stat3) and (not stat2 == ""))
                or ((stat2 == stat4) and (not stat2 == ""))
                or (stat3 == stat4) and (not stat3 == "")))
    else:
        cond = False
    return (cond)
