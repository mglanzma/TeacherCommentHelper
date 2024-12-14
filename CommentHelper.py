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

    with open(fileName, 'r') as csvfile:

        # csv reader
        csvreader = csv.reader(csvfile)

        # fields
        headers = next(csvreader)

        for line in csvreader:

            # if reading student data from csv file
            studentData.append(line)

    return headers, studentData


# method called when loading comment template
def loadCommentTemplate(fileName):
    fullComment = ""
    commentList = []
    
    with open(fileName, 'r') as file:
        for line in file:
            fullComment += line

    commentList = fullComment.strip().split("-----")
    commentInput = commentList[0]

    return commentList, commentInput



# method used to generate a comment with supplied data & format
def generateStudentComment(commentInput, studentIndex, headers, studentData):
    workingComment = commentInput
    valIndex = 0
    # checking for each type of header variable in comment
    for val in headers:
        if ("{"+val+"}") in workingComment:
            workingComment = workingComment.replace(("{"+val+"}"), studentData[studentIndex][valIndex])
        
        valIndex += 1

    return workingComment



'''

Setting up Primary GUI

'''

# temp val for myFile
userFileInput = ""

# method to create gui window
def create_window(theme):
    sg.theme(theme)

    menu_layout = [['File',['---','Exit']],
                   ['Open',['Open Student Data','Open Comment Template']],
                   ['Theme',['Light','Gray','Dark','Dark Fancy']],
                   ['Instructions',['View Instructions']]]

    column_L = [[sg.Multiline(default_text='Go to "Instructions" for help or begin loading in your files in the correct format', size=(50,20), key='-COMMENT_INPUT-', enable_events=True)],
                [sg.Multiline(size=(50,20), key='-COMMENT_OUTPUT-')]]

    column_R = [[sg.Text('Current Student: '), sg.Text('Open -> Open Student Data', key='-CurrStudent_Text-')],
                 [sg.Button('Prev', key='-Prev_Student-', visible=False), sg.Button('Next', key='-Next_Student-', visible=False)]]

    layout = [[sg.Menu(menu_layout)],
              [sg.Col(column_L, p=0), sg.Col(column_R, p=0)]]

    return sg.Window('Comment Helper', layout, resizable=True)


'''

Setting up Instructions Window

'''
def create_instructions(currentTheme):
    sg.theme(currentTheme)

    # text for Instructions textbox
    instructions = """
        Instructions:

        NOTES: 
        - While Instructions Window is open, Comment Helper Window will be unable to process inputs
        - Change Theme before loading data to avoid bugs


1. Go to "Open" in menu

2. In "Open" go to "Open Student Data" and open your .csv file containing your column names and rows of student data
\t- To get a .csv file, download your Google Sheets spreadsheet as .csv or Comma Separated Values file

3. Once you have added the data, go back to "Open" and click "Open Comment Template"
\t- Your comment templates should have normal text with "{var}" to use student data. Substitue "var" with the name of the column you want to include data from.
\t- Optional comment lines should be included after your primary comment and a "-----" separator to indicate they are optional lines. You may have up to 5 optional comment lines in addition to the main comment.

4. Begin copying generic comments from the generic output
\t- If the optional line checkbox has not been checked, the optional line will be excluded from the output comment
        
\nEXAMPLE FILES INCLUDED IN OTHER TABS OF THIS WINDOW
    """

    # text for CSV File Example
    csvExample = """First,Last,SingularPronoun,PossesivePronoun,Grade,Year,Extra
Johnny,Smith,he,his,B+,2024,"without a doubt one of my top students."
Annie,Doe,she,her,A,2022,"a super hard worker."
Franklin,McDonald,he,his,A-,2023,"always smiling."
    """

    # text for Comment File Example
    commentsExample = """{First} {Last} got a {Grade} in my class this year. I had a fantastic time teaching {First}, and I love {PossesivePronoun} attitude!

{First} is {Extra}
-----
This is the Optional Comment 1, but still includes {First}'s name!
-----
This is Optional Comment 2. The divider between optional comments is five hyphens.
-----
Remember, you can only have one main comment followed by 5 optional comments
-----
This is optional comment 4. There is no divider after your last optional comment!
    """

    # Creating tabs to use in layout
    instructionsTab = [[sg.Multiline(default_text=instructions, size = (80,40), disabled=True)]]

    csvExampleTab = [[sg.Multiline(default_text=csvExample, size = (80,40), disabled=True)]]

    commentsExampleTab = [[sg.Multiline(default_text=commentsExample, size = (80,40), disabled=True)]]

    # Actual layout incorporating tabs
    layout = [[sg.TabGroup([[sg.Tab("Instructions", instructionsTab), sg.Tab("CSV File", csvExampleTab), sg.Tab("Comment File", commentsExampleTab)]])]]

    instructionsWindow = sg.Window('Comment Helper Instructions', layout)

    while True:
        event, values = instructionsWindow.read()

        if event == sg.WIN_CLOSED:
            break

    instructionsWindow.close()




'''

Main method (loop that keeps window active until closed)

'''
# creating an instance of our gui window
window = create_window('GrayGrayGray')

# persistent data
headers = []
studentData = []
currentStudentIndex = 0
fullCommentTemplate = []
commentInput = ""

# theme menu labels to cut down on extra cases
myThemes = ['Light','Gray','Dark','Dark Fancy']
currentTheme = "GrayGrayGray"

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
                currentTheme = "GrayGrayGray"
                window = create_window('GrayGrayGray')
            case 'Gray':
                currentTheme = "DarkGrey13"
                window = create_window('DarkGrey13')
            case 'Dark':
                currentTheme = "Black"
                window = create_window('Black')
            case 'Dark Fancy':
                currentTheme = "DarkGrey15"
                window = create_window('DarkGrey15')

    # Viewing Instructions Window
    if event == "View Instructions":
        create_instructions(currentTheme)


    # Open File Conditions
    if event == 'Open Student Data':
        file_path = sg.popup_get_file('open',no_window=True)

        if file_path:
            myFilePath = Path(file_path)
            #userFileInput = file_path

            headers, studentData = parseFileData(myFilePath)

            window['-CurrStudent_Text-'].update(studentData[currentStudentIndex][0])
            window['-Prev_Student-'].update(visible=True)
            window['-Next_Student-'].update(visible=True)

            print("\n\n")
            print(headers)
            print("\n\n")
            print(studentData)

    if event == 'Open Comment Template':
        file_path = sg.popup_get_file('open',no_window=True)
        if file_path:
            myFilePath = Path(file_path)

            fullCommentTemplate, commentInput = loadCommentTemplate(myFilePath)
            personalComment = generateStudentComment(commentInput, currentStudentIndex, headers, studentData)
            window['-COMMENT_INPUT-'].update(commentInput)
            window['-COMMENT_OUTPUT-'].update(personalComment)




    # moving through students (prev/next)
    if event == '-Prev_Student-':
        if currentStudentIndex > 0:
            currentStudentIndex -= 1

        personalComment = generateStudentComment(commentInput, currentStudentIndex, headers, studentData)
        window['-COMMENT_OUTPUT-'].update(personalComment)
        window['-CurrStudent_Text-'].update(studentData[currentStudentIndex][0])

    if event == '-Next_Student-':
        if currentStudentIndex < len(studentData) - 1:
            currentStudentIndex += 1
        
        personalComment = generateStudentComment(commentInput, currentStudentIndex, headers, studentData)
        window['-COMMENT_OUTPUT-'].update(personalComment)
        window['-CurrStudent_Text-'].update(studentData[currentStudentIndex][0])

    # for input comment box
    if event == '-COMMENT_INPUT-':
        commentInput = values['-COMMENT_INPUT-']
        if headers == None:
            window['-COMMENT_OUTPUT-'].update(values['-COMMENT_INPUT-'])
        else:
            personalComment = generateStudentComment(commentInput, currentStudentIndex, headers, studentData)
            window['-COMMENT_OUTPUT-'].update(personalComment)

# closes window if 'X' button is clicked
window.close()


