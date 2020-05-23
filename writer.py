import csv


class Writer:
    def __init__(self, filename):
        self.csvfile = open(filename, mode='w', newline='')
        self.csv_writer = csv.writer(self.csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.csv_writer.writerow([
            "id", "weapon", "name", "price", "rating", "age", "sales", "Buff1", "Buff2", "Buff3", "Debuff"])

    def writerow(self, modid, wepname, modname, modprice, rating, modage, sales, buff1, buff2, buff3, debuff4):
        self.csv_writer.writerow([
            modid, wepname, modname, modprice, rating, modage, sales, buff1, buff2, buff3, debuff4])

    def writeempty(self):
        self.csv_writer.writerow([])
        print("writeempty")
