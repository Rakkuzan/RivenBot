import multiprocessing
import copy
from datetime import timedelta
from time import time
from playsound import playsound
from BotFunctions import runSemlar
from rivenmarket import Rivenmarket
from weapons import weaponslist1, weaponslist2

headless = True
max_processes = 6
weapons = weaponslist2()

def main():
    start_time = time()
    pool = multiprocessing.Pool(max_processes)

    rmkt = Rivenmarket(headless)
    argslist = []
    for weapon in weapons:
        print("---Scanning " + weapon + "---")
        rmkt.loadWeapon(weapon)
        filename = weapon + ".csv"
        args = [headless, copy.deepcopy(rmkt.modlist), filename]
        argslist.append(args)
    rmkt.quit()

    pool.map(runSemlar, [*argslist])

    print("---DONE---")
    playsound("sound.wav")
    time_elapsed = time() - start_time
    print("Time Elapsed " + str(timedelta(seconds=time_elapsed)).split(".")[0])


if __name__ == '__main__':
    main()
