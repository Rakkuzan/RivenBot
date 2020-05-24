from rivenmarket import Rivenmarket
from semlar import Semlar


def runSemlar(headless, modlist, filename):
    semlar = Semlar(headless, filename)
    for mod in modlist:
        semlar.loadMod(mod)
        if semlar.isWeaponBugged():
            continue

        if semlar.modMeetsCriteria():
            semlar.checkRating()
            semlar.write()

    semlar.writeempty()
    semlar.quit()

def weaponslist1():
    return [
           "Kuva Bramma",
           "Lanka",
           "Rubico",
           "Vectis",
           "Corinth",
           "Redeemer",
           "Kohm",
           "Gram",
           # "Opticor",      # uncommon
           "Kronen",
           "Catchmoon",
           "Nukor",
           "Kuva Chakkhurr",
           # "Amprex",       # uncommon
           "Shedu",
           "Acceltra",
           # "Lenz",         # uncommon
           # "Dread",        # uncommon
           #"Plague Kripath", # bugged
           #"Basmu"           # uncommon
           "Tiberon",
           "Fulmin",
           "Ignis",
           "Sepfahn",
           "Daikyu",
           "Tombfinger",
           "Reaper Prime",
           "Vulkar",
           "Baza",
           "Brakk",
           ]

def weaponslist2():
    return [
           "Kuva Bramma",
           "Lanka",
           "Rubico",
           "Vectis",
           "Corinth"]
