import asyncio
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
