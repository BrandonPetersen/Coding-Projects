#Brandon Petersen Cowphabet in Python
import sys
cowphabet = input("Cowphabet: ")
string = input("String: ")
counter = 0
cycles = 1

while(True):
    for char in cowphabet:
        if string[counter] == char:
            counter += 1
            if counter == len(string):
                print(cycles)
                sys.exit()
    cycles += 1
