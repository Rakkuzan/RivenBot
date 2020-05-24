import multiprocessing
from datetime import timedelta
from time import time
from playsound import playsound
from BotFunctions import weaponslist1, weaponslist2, runSemlar
from rivenmarket import Rivenmarket


def main():
    start_time = time()
    weapons = weaponslist2()
    headless = True

    rmkt = Rivenmarket(headless)
    processes = []
    for weapon in weapons:
        print("---Scanning " + weapon + "---")
        rmkt.loadWeapon(weapon)
        filename = weapon + ".csv"
        processes.append(multiprocessing.Process(target=runSemlar, args=(headless, rmkt.modlist, filename,)))
    rmkt.quit()

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print("---DONE---")
    playsound("sound.wav")
    time_elapsed = time() - start_time
    print("Time Elapsed " + str(timedelta(seconds=time_elapsed)).split(".")[0])


if __name__ == '__main__':
    main()
