from pyglet.window import key
import imageUtil
import saveAndLoad
import pageData
import screenData
from pageData import Page
from vector2D import Vector2D

mousePos = Vector2D()

screens = []

editScreenButtonPositions = []

editScreenButtonImage = imageUtil.LoadImage("images/editScreenIcon.png")
editScreenButtonSize = 64
editScreenButtonOrigin = Vector2D(200, 800)

screensDataFilename = "data/screens.txt"

editingNewScreenName = False

addNewScreenButtonImage = imageUtil.LoadImage("images/addNewScreenIcon.png")
addNewScreenButtonSize = 64
addNewScreenButtonOrigin = Vector2D(1200, 800)
newScreenName = ""

newScreenNameTextBoxPos = Vector2D(1250, 740)
newScreenNameTextBoxWidth = 512
newScreenNameTextBoxHeight = 30
newScreenNameTextBoxColor = "grey"

def LoadScreens():
    #clear screen list and button positions
    screens.clear()
    editScreenButtonPositions.clear()
    
    yOffset = 0
    f = open(screensDataFilename, "r")
    for line in f:
        screens.append(line.split()[0])
        editScreenButtonPositions.append(Vector2D(editScreenButtonOrigin.x, editScreenButtonOrigin.y - yOffset))
        yOffset += 50
    f.close()

LoadScreens()

def AddNewScreen():
    global newScreenName
    
    #add new empty file to data folder
    f = open("data/" + newScreenName + ".txt", "x")
    f.close()
    #add new file name to screens.txt
    f = open("data/screens.txt", "a")
    f.write(newScreenName + ".txt")
    f.write("\n")
    f.close()
    #reset new screen name text
    newScreenName = ""
    #refresh screens list
    LoadScreens()
    

def CheckPointOverRectangle(point, rectBLPoint, width, height):
    if point.x >= rectBLPoint.x and point.x <= rectBLPoint.x + width and point.y >= rectBLPoint.y and point.y <= rectBLPoint.y + height:
        return True

def KeyPressed(symbol, modifiers):
    global editingNewScreenName
    global newScreenName
    
    if editingNewScreenName:
        if symbol == key.BACKSPACE:
            newScreenName = newScreenName[:-1]
        elif symbol == key.RETURN:
            editingNewScreenName = False
            newScreenNameTextBoxColor = "grey"
        elif symbol == key.ESCAPE:
            pass
        else:
            newScreenName += str(chr(symbol))

def MouseMoved(x, y, dx, dy):
    mousePos.x = x
    mousePos.y = y

def MousePressed(x, y, button, modifiers):
    global editingNewScreenName
    global newScreenNameTextBoxColor
    
    for i in range(len(screens)):
        #if mouse position inside an edit screen button on mouse pressed
        if CheckPointOverRectangle(mousePos, editScreenButtonPositions[i], editScreenButtonSize, editScreenButtonSize):
            #set selected screen to screen name selected
            saveAndLoad.selectedScreenFilename = "data/" + screens[i]
            #change page to editor
            pageData.SetCurrentPage(Page.EDITOR)
            saveAndLoad.LoadLevelData()
    
    #if mouse pressed over new screen name text box
    if CheckPointOverRectangle(mousePos, newScreenNameTextBoxPos, newScreenNameTextBoxWidth, newScreenNameTextBoxHeight):
        if editingNewScreenName:
            newScreenNameTextBoxColor = "grey"
        else:
            newScreenNameTextBoxColor = "red"
        editingNewScreenName = not editingNewScreenName
    
    #if mouse pressed over add new screen button
    if CheckPointOverRectangle(mousePos, addNewScreenButtonOrigin, addNewScreenButtonSize, addNewScreenButtonSize):
        AddNewScreen()
    

def MouseDragged(x, y, dx, dy, buttons, modifiers):
    pass

def MouseReleased(x, y, button, modifiers):
    pass

def DrawPage():
    for i in range(len(screens)):
        imageUtil.DrawImage(editScreenButtonImage, editScreenButtonPositions[i].x, editScreenButtonPositions[i].y)
        imageUtil.DisplayText(screens[i], editScreenButtonPositions[i].x + 100, editScreenButtonPositions[i].y + editScreenButtonSize / 2, 16)
    
    imageUtil.DrawImage(addNewScreenButtonImage, addNewScreenButtonOrigin.x, addNewScreenButtonOrigin.y)
    imageUtil.DisplayText("Add new screen with filename: ", addNewScreenButtonOrigin.x + 100, addNewScreenButtonOrigin.y + addNewScreenButtonSize / 2, 16)
    
    #text box rectangle for new screen name
    imageUtil.DrawRectangle(newScreenNameTextBoxPos, newScreenNameTextBoxWidth, newScreenNameTextBoxHeight, newScreenNameTextBoxColor)
    
    #text for new screen name
    imageUtil.DisplayText(newScreenName, newScreenNameTextBoxPos.x + 10, newScreenNameTextBoxPos.y + newScreenNameTextBoxHeight / 2, 16)
    
    #imageUtil.DisplayText("Mouse position: " + str(mousePos), 100, 50, 16)

def Update(frameTime):
    pass