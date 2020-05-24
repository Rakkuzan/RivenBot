from rivenmarket import Rivenmarket
from semlar import Semlar


def runBot(headless, weapon):
    rmkt = Rivenmarket(headless)
    for cnt, weapon in enumerate(weapon):
        print("---Scanning " + weapon + "---")
        rmkt.loadWeapon(weapon)
        filename = weapon + ".csv"
        runSemlar(headless, rmkt.list, filename)
    rmkt.quit()

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
