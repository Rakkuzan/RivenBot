from BotFunctions import runSemlar
from weapons import weaponslist1, weaponslist2
from datetime import timedelta
from time import time
from playsound import playsound
import asyncio
from rivenmarket import Rivenmarket
from multiprocessing import Process
import sys

sys.setrecursionlimit(50000)
def main():
    print("yes")
    start_time = time()
    weapons = weaponslist2()
    headless = False

    rmkt = Rivenmarket(headless)
    processes = []
    for cnt, weapon in enumerate(weapons):
        rmkt.loadWeapon(weapon)
        filename = weapon + ".csv"
        processes.append(Process(target=runSemlar, args=(headless, rmkt.list, filename,)))
        processes[cnt].start()
    rmkt.quit()

    for process in processes:
        process.join()


    print("---DONE---")
    playsound("sound.wav")
    time_elapsed = time() - start_time
    print("Time Elapsed " + str(timedelta(seconds=time_elapsed)).split(".")[0])


if __name__ == '__main__':
    main()
