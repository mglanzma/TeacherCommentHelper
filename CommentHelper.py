# imports to interact with files
import sys
import os
import csv
# imports for GUI
import PySimpleGUI as sg
from pathlib import Path

'''

HELPER METHODS

'''

def parseFileData(fileName):
    # fields / column headers
    headers = []
    # list of list of student data ordered by headers
    studentData = []

    with open(userFileInput, 'r') as csvfile:

        # csv reader
        csvreader = csv.reader(csvfile)

        # fields
        headers = next(csvreader)

        for line in csvreader:

            # if reading student data from csv file
            studentData.append(line)

    return headers, studentData










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

            headers, studentData = parseFileData(userFileInput)
            print("\n\n")
            print(headers)
            print("\n\n")
            print(studentData)


# closes window if 'X' button is clicked
window.close()


