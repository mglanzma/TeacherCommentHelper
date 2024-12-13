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
def create_window(theme):
    sg.theme(theme)

    menu_layout = [['File',['---','Exit']],
                   ['Open',['Open Student Data','Open Comment Template']],
                   ['Theme',['Light','Gray','Dark','Dark Fancy']]]

    column_L = [[sg.Multiline(size=(20,20), key='-COMMENT_INPUT-')],
                [sg.Multiline(size=(20,20), key='-COMMENT_OUTPUT-')]]

    column_R = [[sg.Text('Current Student: '), sg.Text('', key='-CurrStudent_Text-')],
                 [sg.Button('Prev', key='-Prev_Student-'), sg.Button('Next', key='-Next_Student-')]]

    layout = [[sg.Menu(menu_layout)],
              [sg.Col(column_L, p=0), sg.Col(column_R, p=0)]]

    return sg.Window('Comment Helper', layout)



# creating an instance of our gui window
window = create_window('GrayGrayGray')

while True:
    event, values = window.read()

    # Close Window Conditions
    if event == sg.WIN_CLOSED:
        break

    if event == 'Exit':
        break

    # Change Theme Conditions
    if event == 'Light':
        window.close()
        window = create_window('GrayGrayGray')
    if event == 'Gray':
        window.close()
        window = create_window('DarkGrey13')
    if event == 'Dark':
        window.close()
        window = create_window('Black')
    if event == 'Dark Fancy':
        window.close()
        window = create_window('DarkGrey15')

    # Open File Conditions
    if event == 'Open Student Data':
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


