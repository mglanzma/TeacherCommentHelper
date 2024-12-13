# imports to interact with files
import sys
import os
# imports for GUI
import PySimpleGUI as sg
from pathlib import Path

'''

Setting up GUI

'''

# temp val for myFile
userFileInput = ""

# method to create gui window
def create_window():
    sg.theme('GrayGrayGray')

    menu_layout = [['File',['Open','---','Exit']]]

    layout = [[sg.Menu(menu_layout)]]

    return sg.Window('Comment Helper', layout)



# creating an instance of our gui window
window = create_window()

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'Exit':
        break

    if event == 'Open':
        file_path = sg.popup_get_file('open',no_window=True)

        if file_path:
            myFilePath = Path(file_path)
            userFileInput = file_path


# closes window if 'X' button is clicked
window.close()



# checks if program is used correctly with csv file
'''commandArgs = len(sys.argv)
if(commandArgs != 2):
   print("For usage, please do 'python3 (fileName)'")
   quit()'''



'''

"Main" if passed command line argument test 

'''

'''# getting file that user inputted
userFileInput = sys.argv[1]'''
# if user-inputted file exists, turn into file object
if os.path.isfile(userFileInput):
    myFile = open(userFileInput, 'r')
#else quit program
else:
    print("Unfortunately that file does not seem to exist. Please check your spelling")
    quit()


# counter used to determine if colomn header or actual column values
lineCounter = 0

# 2D list (matrix) used to store student data.
# each row is a different student
studentData = []
numStudents = 0

# quit if no file is opened
if myFile == "":
    quit()

for line in myFile:

    # if reading the column headers from csv file
    if(lineCounter == 0):
        headers = line.strip().split(',')
        numColumns = len(headers)

    # if reading student data from csv file
    else:
        studentData.append(line.strip().split(","))
        numStudents += 1
    

    #print(line, end=" ")
    lineCounter += 1

print("\n\n")
print(headers)
print(studentData)

print("\n\n")
for student in range(numStudents):
    for column in range(numColumns):
        print(studentData[student][column])
    print()
    
