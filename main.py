from BotFunctions import runSemlar
from weapons import weaponslist1, weaponslist2
from datetime import timedelta
from time import time
from playsound import playsound
from rivenmarket import Rivenmarket
import threading

def main():
    print("yes")
    start_time = time()
    weapons = weaponslist2()
    headless = False

    rmkt = Rivenmarket(headless)
    threads = []
    for cnt, weapon in enumerate(weapons):
        print("---Scanning " + weapon + "---")
        rmkt.loadWeapon(weapon)
        filename = weapon + ".csv"
        threads.append(threading.Thread(target=runSemlar(headless, rmkt.list, filename)))
        threads[cnt].start()
        threads[cnt].run()
    rmkt.quit()

    for thread in threads:
        thread.join()


    print("---DONE---")
    playsound("sound.wav")
    time_elapsed = time() - start_time
    print("Time Elapsed " + str(timedelta(seconds=time_elapsed)).split(".")[0])


if __name__ == '__main__':
    main()
