from BotFunctions import runBot
from weapons import weaponslist1, weaponslist2
from datetime import timedelta
from time import time
from playsound import playsound
import multiprocessing




def main():
    start_time = time()
    weapons = weaponslist2()
    headless = False

    processes = []
    for weapon in weapons:
        processes.append(multiprocessing.Process(target=runBot, args=(headless, [weapon],)))

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
