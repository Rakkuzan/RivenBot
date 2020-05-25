from semlar import Semlar


def runSemlar(argslist):
    headless, modlist, filename = [argslist[i] for i in range(3)]

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
