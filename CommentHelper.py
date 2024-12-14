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
def generateStudentComment(commentInput, studentIndex, headers, studentData, checkboxVals, optionalVals):

    workingComment = commentInput

    # filling in any optional sentences
    oValIndex = 0
    for val in checkboxVals:
        if val:
            if("{Optional"+str(oValIndex+1)+"}") in workingComment:
                workingComment = workingComment.replace(("{Optional"+str(oValIndex+1)+"}"), optionalVals[oValIndex].strip())
        else:
            workingComment = workingComment.replace(("{Optional"+str(oValIndex+1)+"}"), "".strip())

        oValIndex += 1



    valIndex = 0
    # checking for each type of header variable in comment
    for val in headers:
        if ("{"+val+"}") in workingComment:
            workingComment = workingComment.replace(("{"+str(val)+"}"), studentData[studentIndex][valIndex])
        
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

    column_R = [[sg.Text('Your Progress:',visible=False,key='-progress_text-')],
                [sg.ProgressBar(1,key='-PROGRESS-',visible=False,size=(20,20))],
                [sg.Text()],
                [sg.Text('Current Student: '), sg.Text('Open -> Open Student Data', key='-CurrStudent_Text-')],
                 [sg.Button('Prev', key='-Prev_Student-', visible=False), sg.Button('Next', key='-Next_Student-', visible=False)],
                [sg.Checkbox('Include Optional Sentence #1',key='-Optional1-',visible=False,default=False,enable_events=True)],
                [sg.Checkbox('Include Optional Sentence #2',key='-Optional2-',visible=False,default=False,enable_events=True)],
                [sg.Checkbox('Include Optional Sentence #3',key='-Optional3-',visible=False,default=False,enable_events=True)],
                [sg.Checkbox('Include Optional Sentence #4',key='-Optional4-',visible=False,default=False,enable_events=True)],
                [sg.Checkbox('Include Optional Sentence #5',key='-Optional5-',visible=False,default=False,enable_events=True)]]

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
        - Using incorrect file formatting will result in errors/crashes


1. Go to "Open" in menu

2. In "Open" go to "Open Student Data" and open your .csv file containing your column names and rows of student data
\t- To get a .csv file, download your Google Sheets spreadsheet as .csv or Comma Separated Values file

3. Once you have added the data, go back to "Open" and click "Open Comment Template"
\t- Your comment templates should have normal text with "{var}" to use student data. Substitue "var" with the name of the column you want to include data from.
\t- To use optional sentences, put "{Optional#}" in your main comment where "#" is replaced with a digit 1-5.
\t- Optional sentence should be included after your primary comment and a "-----" separator to indicate they are optional sentences. You may have up to 5 optional sentences in addition to the main comment.

4. Begin copying generic comments from the generic output
\t- If the optional sentence checkbox has not been checked, the optional sentence will be excluded from the output comment
        
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

I will include the first optional sentence here: {Optional1}

The third will go here: {Optional 3}

{First} is {Extra}
-----
This is the Optional Sentence #1, but still includes {First}'s name!
-----
This is Optional Sentence #2. The divider between optional comments is five hyphens.
-----
Remember, you can only have one main comment followed by 5 optional sentences
-----
This is optional sentence #4. There is no divider after your last optional comment! I could have a fifth optional sentence, but I don't need to!
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

# default optional sentence values
optional = ["","","","",""]

# default values for checkboxVals
myCheckboxes = ['-Optional1-','-Optional2-','-Optional3-','-Optional4-','-Optional5-']
checkboxVals = [False,False,False,False,False]

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
            window['-progress_text-'].update(visible=True)
            window['-PROGRESS-'].update_bar((currentStudentIndex),(len(studentData)-1))
            window['-PROGRESS-'].update(visible=True)

            print("\n\n")
            print(headers)
            print("\n\n")
            print(studentData)

    if event == 'Open Comment Template':
        file_path = sg.popup_get_file('open',no_window=True)
        if file_path:
            myFilePath = Path(file_path)

            # getting main and optional sentences
            fullCommentTemplate, commentInput = loadCommentTemplate(myFilePath)
            # optional sentences
            if len(fullCommentTemplate) >= 2:
                optional[0] = fullCommentTemplate[1]
                window['-Optional1-'].update(visible=True)
            if len(fullCommentTemplate) >= 3:
                optional[1] = fullCommentTemplate[2]
                window['-Optional2-'].update(visible=True)
            if len(fullCommentTemplate) >= 4:
                optional[2] = fullCommentTemplate[3]
                window['-Optional3-'].update(visible=True)
            if len(fullCommentTemplate) >= 5:
                optional[3] = fullCommentTemplate[4]
                window['-Optional4-'].update(visible=True)
            if len(fullCommentTemplate) >= 6:
                optional[4] = fullCommentTemplate[5]
                window['-Optional5-'].update(visible=True)

            
            personalComment = generateStudentComment(commentInput, currentStudentIndex, headers, studentData, checkboxVals, optional)
            window['-COMMENT_INPUT-'].update(commentInput)
            window['-COMMENT_OUTPUT-'].update(personalComment)




    # moving through students (prev/next)
    if event == '-Prev_Student-':
        if currentStudentIndex > 0:
            currentStudentIndex -= 1

        personalComment = generateStudentComment(commentInput, currentStudentIndex, headers, studentData, checkboxVals, optional)
        window['-COMMENT_OUTPUT-'].update(personalComment)
        window['-CurrStudent_Text-'].update(studentData[currentStudentIndex][0])
        window['-PROGRESS-'].update_bar((currentStudentIndex))

    if event == '-Next_Student-':
        if currentStudentIndex < len(studentData) - 1:
            currentStudentIndex += 1
        
        personalComment = generateStudentComment(commentInput, currentStudentIndex, headers, studentData, checkboxVals, optional)
        window['-COMMENT_OUTPUT-'].update(personalComment)
        window['-CurrStudent_Text-'].update(studentData[currentStudentIndex][0])
        window['-PROGRESS-'].update_bar((currentStudentIndex))


    # events for checking/unchecking optional sentence checkbox
    if event in myCheckboxes:
        match event:
            case "-Optional1-":
                if values["-Optional1-"]:
                    checkboxVals[0] = True
                else:
                    checkboxVals[0] = False
            case "-Optional2-":
                if values["-Optional2-"]:
                    checkboxVals[1] = True
                else:
                    checkboxVals[1] = False
            case "-Optional3-":
                if values["-Optional3-"]:
                    checkboxVals[2] = True
                else:
                    checkboxVals[2] = False
            case "-Optional4-":
                if values["-Optional4-"]:
                    checkboxVals[3] = True
                else:
                    checkboxVals[3] = False
            case "-Optional5-":
                if values["-Optional5-"]:
                    checkboxVals[4] = True
                else:
                    checkboxVals[4] = False
        
        personalComment = generateStudentComment(commentInput, currentStudentIndex, headers, studentData, checkboxVals, optional)
        window['-COMMENT_OUTPUT-'].update(personalComment)

    # for input comment box
    if event == '-COMMENT_INPUT-':
        commentInput = values['-COMMENT_INPUT-']
        if headers == None:
            window['-COMMENT_OUTPUT-'].update(values['-COMMENT_INPUT-'])
        else:
            personalComment = generateStudentComment(commentInput, currentStudentIndex, headers, studentData, checkboxVals, optional)
            window['-COMMENT_OUTPUT-'].update(personalComment)

# closes window if 'X' button is clicked
window.close()


