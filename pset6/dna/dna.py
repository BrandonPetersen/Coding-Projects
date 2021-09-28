import cs50
from csv import reader, DictReader
import sys

if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py database sequence")
        
with open(sys.argv[1], "r") as csvfile:
    reader = DictReader(csvfile)
    people = list(reader)
    
with open(sys.argv[2], "r") as file:
    dna = file.read()

count = []

for i in range(len(reader.fieldnames)-1):
    sequence = reader.fieldnames[i + 1]
    count.append(0)
    temp = 0
    for k in range(len(dna)):
        if dna[k: k + len(sequence)] == sequence:
            j = k
            while dna[j: j + len(sequence)] == sequence:
                temp += 1 
                j += len(sequence)
            if temp > count[i]:
                count[i] = temp
            temp = 0
            
for i in range(len(people)):
    matches = 0
    for k in range(len(reader.fieldnames) - 1):
        if count[k] == int(people[i][reader.fieldnames[k + 1]]):
            matches += 1
            if matches == len(reader.fieldnames) - 1:
                print(people[i]['name'])
                sys.exit()
print("No match")