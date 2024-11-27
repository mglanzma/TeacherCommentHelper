# imports to interact with files
import sys

# checks if program is used correctly with csv file
commandArgs = len(sys.argv)
if(commandArgs != 2):
   print("For usage, please do 'python3 (fileName)'")
   quit()

# "Main" if passed command line argument test

# getting file that user inputted
userFileInput = sys.argv[1]

# counter used to determine if colomn header or actual column values
lineCounter = 0
# list used to store column headers
headers = []

with open(userFileInput, 'r') as file:
    for line in file:

        # if reading the column headers rather than values from csv file
        if(lineCounter == 0):
            headers.append(line.strip().split(','))

        print(line, end=" ")
        lineCounter+=1

print("\n\n")
print(headers)
