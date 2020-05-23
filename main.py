from rivenmarket import Rivenmarket
from semlar import Semlar
from weapons import weaponslist1, weaponslist2
from datetime import timedelta
from time import sleep, time
from playsound import playsound

start_time = time()
weapons = weaponslist2()

headless = False
rmkt = Rivenmarket(headless)
semlar = Semlar(headless)

for weapon in weapons:
    rmkt.loadWeapon(weapon)

    for mod in rmkt.list:
        rmkt.loadMod(mod)
        if rmkt.isWeaponBugged():
            continue

        if rmkt.modMeetsCriteria():
            semlar.loadstats(rmkt.wepname, rmkt.stat1, rmkt.stat2, rmkt.stat3, rmkt.stat4,
                             rmkt.wepid, rmkt.modname, rmkt.modprice, rmkt.modage)
            semlar.checkRating()
            semlar.write()
    semlar.writeempty()

rmkt.quit()
semlar.quit()

print("---DONE---")
playsound("sound.wav")
time_elapsed = time() - start_time
print("Time Elapsed " + str(timedelta(seconds=time_elapsed)).split(".")[0])
