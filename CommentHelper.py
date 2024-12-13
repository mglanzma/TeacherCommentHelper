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
# method called when loading student data
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


# method used to generate a comment with supplied data & format





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

    column_L = [[sg.Multiline(size=(20,20), key='-COMMENT_INPUT-', enable_events=True)],
                [sg.Multiline(size=(20,20), key='-COMMENT_OUTPUT-')]]

    column_R = [[sg.Text('Current Student: '), sg.Text('', key='-CurrStudent_Text-')],
                 [sg.Button('Prev', key='-Prev_Student-'), sg.Button('Next', key='-Next_Student-')]]

    layout = [[sg.Menu(menu_layout)],
              [sg.Col(column_L, p=0), sg.Col(column_R, p=0)]]

    return sg.Window('Comment Helper', layout, resizable=True)



# creating an instance of our gui window
window = create_window('GrayGrayGray')

# persistent data
headers = []
studentData = []
currentStudentIndex = 0
commentInput = ""

myThemes = ['Light','Gray','Dark','Dark Fancy']

while True:

    # for event tracking
    event, values = window.read()
        
    # Close Window Conditions
    if event == sg.WIN_CLOSED:
        break
    if event == 'Exit':
        break

    # Change Theme Conditions
    if event in myThemes:
        window.close()
        match event:
            case 'Light':
                window = create_window('GrayGrayGray')
            case 'Gray':
                window = create_window('DarkGrey13')
            case 'Dark':
                window = create_window('Black')
            case 'Dark Fancy':
                window = create_window('DarkGrey15')


    # Open File Conditions
    if event == 'Open Student Data':
        file_path = sg.popup_get_file('open',no_window=True)

        if file_path:
            myFilePath = Path(file_path)
            userFileInput = file_path

            headers, studentData = parseFileData(userFileInput)

            window['-CurrStudent_Text-'].update(studentData[currentStudentIndex][0])

            print("\n\n")
            print(headers)
            print("\n\n")
            print(studentData)

    # moving through students (prev/next)
    if event == '-Prev_Student-':
        if currentStudentIndex > 0:
            currentStudentIndex -= 1
        window['-CurrStudent_Text-'].update(studentData[currentStudentIndex][0])

    if event == '-Next_Student-':
        if currentStudentIndex < len(studentData) - 1:
            currentStudentIndex += 1
        window['-CurrStudent_Text-'].update(studentData[currentStudentIndex][0])

    # for input comment box
    if event == '-COMMENT_INPUT-':
        commentInput = values['-COMMENT_INPUT-']
        window['-COMMENT_OUTPUT-'].update(values['-COMMENT_INPUT-'])


# closes window if 'X' button is clicked
window.close()


