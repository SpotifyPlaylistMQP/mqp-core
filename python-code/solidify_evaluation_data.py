import sys
import csv

rec_systems = [
    "item",
    "user",
    "mf"
]

mongo_collection = sys.argv[1]

filename = "solidified_" + mongo_collection + ".txt"
open('evaluation_data/' + filename, "w").close()
output = open('evaluation_data/' + filename, "a")
header = "N, "

results = {}
for N in range(1, 101):
    results[str(N)] = ""

for rec_system in rec_systems:
    with open('evaluation_data/' + rec_system + '_' + mongo_collection) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                header += rec_system + ', '
                line_count += 1
            else:
                results[row[0]] += str(row[1]) + ", "
                line_count += 1

output.write(header + "\n")
for N in range(1, 101):
    output.write(str(N) + ', ' + results[str(N)] + "\n")