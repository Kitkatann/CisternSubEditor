import imageUtil
from vector2D import Vector2D
from tileType import TileType
import random
import math
from pyglet.window import key
from enum import Enum
from entity import Entity
from entityType import EntityType
import entityTypeData
import saveAndLoad
import screenData
import tileTypeData
import pageData
from pageData import Page



mousePos = Vector2D()

class Layer(Enum):
    BACKGROUND = 1
    FOREGROUND = 2
    WALLS = 3
    ENTITIES = 4

editingEntityAttributes = False

selectedTile = None
selectedEntityType = None

selectedEntityAttribsText = ""

entityPaletteClicked = False

selectedLayer = Layer.WALLS

bgLayerActive = True
fgLayerActive = True
wallsLayerActive = True
entitiesActive = True

entitiesGridSnapSelected = False

gridTileSize = 32
gridOrigin = Vector2D(100, 100)

tilePaletteWidth = 16
tilePaletteHeight = 5
tilePaletteOrigin = Vector2D(1300, 400)

entityPaletteWidth = 16
entityPaletteHeight = 2
entityPaletteOrigin = Vector2D(1300, 700)

toolbarWidth = 11
toolbarHeight = 1
toolbarIconSize = 64
toolbarOrigin = Vector2D(100, 1000)

entityAttribTextBoxPos = Vector2D(1300, 800)
entityAttribTextBoxWidth = 512
entityAttribTextBoxHeight = 30
entityAttribColour = "grey"

tileTypeData.LoadTileTypes()
entityTypeData.LoadEntityTypes()

#tile grid background image
tileGridBackgroundImage = imageUtil.LoadImage("images/screen_edit_bg.png", False)

#tile image from blank spaces - for editor purposes only
blankTile = imageUtil.LoadImage("images/blankTile.png", False)

#toolbar image
toolbarImage = imageUtil.LoadImage("images/toolbar.png", False)
#selected toolbar box image
toolbarSelectionImage = imageUtil.LoadImage("images/toolbarSelection.png", False)

entitySelectionImage = imageUtil.LoadImage("images/entity_selected.png", True)
        
def GetMouseOverGenericGridCell(gridWidth, gridHeight, gridOrigin, tileSize):
    cellX = (mousePos.x - gridOrigin.x) // tileSize
    cellY = (mousePos.y - gridOrigin.y) // tileSize
    if (cellX >= 0) and (cellX < gridWidth) and (cellY >= 0) and (cellY < gridHeight):
        cellIndex = gridWidth * cellY + cellX
        return cellIndex
    else:
        return -1

def GetEntityAtPoint(point):
    for e in screenData.entities:
        if CheckPointOverRectangle(point, Vector2D(e.x - gridTileSize / 2 + gridOrigin.x, e.y - gridTileSize / 2 + gridOrigin.y), gridTileSize, gridTileSize):
            return e
    return None

def CheckPointOverRectangle(point, rectBLPoint, width, height):
    if point.x >= rectBLPoint.x and point.x <= rectBLPoint.x + width and point.y >= rectBLPoint.y and point.y <= rectBLPoint.y + height:
        return True
    return False



def KeyPressed(symbol, modifiers):
    global editingEntityAttributes
    global selectedEntityAttribsText
    global entityAttribColour
    
    if editingEntityAttributes:
        if symbol == key.BACKSPACE:
            selectedEntityAttribsText = selectedEntityAttribsText[:-1]
        elif symbol == key.RETURN:
            editingEntityAttributes = False
            #apply changes to selected entities
            for e in screenData.entities:
                if e.selected:
                    e.attributes = selectedEntityAttribsText
                    e.selected = False
            entityAttribColour = "grey"
            selectedEntityAttribsText = ""
        elif symbol == key.ESCAPE:
            pass
        elif symbol == key.DELETE:
            pass
        else:
            selectedEntityAttribsText += str(chr(symbol))
    else:
        screenData.entities = [e for e in screenData.entities if not e.selected]

def MouseMoved(x, y, dx, dy):
    mousePos.x = x
    mousePos.y = y

def MouseDragged(x, y, dx, dy, buttons, modifiers):
    if selectedLayer != Layer.ENTITIES:
        MousePressed(x, y, buttons, modifiers)

#snaps a point relative to a grid origin to a point on the grid
def SnapPointToGrid(point, cellSize):
    point.x = cellSize * math.floor((point.x / cellSize) + 0.5)
    point.y = cellSize * math.floor((point.y / cellSize) + 0.5)

def MouseReleased(x, y, button, modifiers):
    global entityPaletteClicked
    
    if entityPaletteClicked:
        if CheckPointOverRectangle(Vector2D(x, y), gridOrigin, screenData.gridWidth * gridTileSize, screenData.gridHeight * gridTileSize):
            #create new entity at current position
            pos = Vector2D(x, y)
            pos -= gridOrigin
            if entitiesGridSnapSelected:
                SnapPointToGrid(pos, gridTileSize / 2)
            screenData.CreateEntity(selectedEntityType, pos.x, pos.y)

    entityPaletteClicked = False

def MousePressed(x, y, button, modifiers):
    global selectedTile
    global selectedLayer
    global fgLayerActive
    global bgLayerActive
    global wallsLayerActive
    global entitiesActive
    global entityPaletteClicked
    global selectedEntityType
    global editingEntityAttributes
    global entityAttribColour
    global entitiesGridSnapSelected
    
    #mouse pressed over screen grid
    cellIndex = GetMouseOverGenericGridCell(screenData.gridWidth, screenData.gridHeight, gridOrigin, gridTileSize)
    if cellIndex != -1:
        if selectedLayer == Layer.BACKGROUND and bgLayerActive:
            screenData.bgLayer[cellIndex] = selectedTile
        if selectedLayer == Layer.FOREGROUND and fgLayerActive:
            screenData.fgLayer[cellIndex] = selectedTile
        if selectedLayer == Layer.WALLS and wallsLayerActive:
            screenData.wallsLayer[cellIndex] = selectedTile
        if selectedLayer == Layer.ENTITIES and entitiesActive:
            #select entity/entities
            e = GetEntityAtPoint(mousePos)
            if e is not None:
                e.selected = not e.selected
    
    #mouse pressed over tile palette
    cellIndex = GetMouseOverGenericGridCell(tilePaletteWidth, tilePaletteHeight, tilePaletteOrigin, gridTileSize)
    if cellIndex != -1:
        selectedTile = tileTypeData.tileTypes[cellIndex]
        selectedEntityType = None
    
    #mouse pressed over entity type palette
    cellIndex = GetMouseOverGenericGridCell(entityPaletteWidth, entityPaletteHeight, entityPaletteOrigin, gridTileSize)
    if cellIndex != -1:
        if selectedLayer == Layer.ENTITIES and entitiesActive:
            selectedEntityType = entityTypeData.entityTypes[cellIndex]
            selectedTile = None
            entityPaletteClicked = True
    
    #mouse pressed over toolbar
    cellIndex = GetMouseOverGenericGridCell(toolbarWidth, toolbarHeight, toolbarOrigin, toolbarIconSize)
    if cellIndex != -1:
        if cellIndex == 0:
            #foreground layer visible
            fgLayerActive = not fgLayerActive
        if cellIndex == 1:
            #background layer visible
            bgLayerActive = not bgLayerActive
        if cellIndex == 2:
            #walls layer visible
            wallsLayerActive = not wallsLayerActive
        if cellIndex == 3:
            #entities layer visible
            entitiesActive = not entitiesActive
        if cellIndex == 4:
            #foreground layer editable
            selectedLayer = Layer.FOREGROUND
        if cellIndex == 5:
            #background layer editable
            selectedLayer = Layer.BACKGROUND
        if cellIndex == 6:
            #walls layer editable
            selectedLayer = Layer.WALLS
        if cellIndex == 7:
            #entities layer editable
            selectedLayer = Layer.ENTITIES
        if cellIndex == 8:
            #entities grid snap pressed
            entitiesGridSnapSelected = not entitiesGridSnapSelected
        if cellIndex == 9:
            #save screen
            saveAndLoad.SaveData()
        if cellIndex == 10:
            #open other file
            pageData.SetCurrentPage(Page.BROWSER)
    
    #mouse pressed over entity attributes text box
    if selectedLayer == Layer.ENTITIES:
        if CheckPointOverRectangle(mousePos, entityAttribTextBoxPos, entityAttribTextBoxWidth, entityAttribTextBoxHeight):
            editingEntityAttributes = not editingEntityAttributes
            if editingEntityAttributes:
                entityAttribColour = "red"
            else:
                entityAttribColour = "grey"
        
    

def DrawSelectionBoxOverToolbarButton(cellIndex):
    imageUtil.DrawImage(toolbarSelectionImage, (cellIndex % toolbarWidth) * toolbarIconSize + toolbarOrigin.x, (cellIndex // toolbarWidth) * toolbarIconSize + toolbarOrigin.y)

def DrawTileGrid(layerTiles):
    for i in range(len(layerTiles)):
        if layerTiles[i] is not None:
            if layerTiles[i].image is not None:
                imageUtil.DrawImage(layerTiles[i].image, (i % screenData.gridWidth) * gridTileSize + gridOrigin.x, (i // screenData.gridWidth) * gridTileSize + gridOrigin.y)

def DrawEntities(entities):
    for e in entities:
        x = e.x + gridOrigin.x
        y = e.y + gridOrigin.y
        image = e.entityType.image
        imageUtil.DrawImage(image, x, y)
        if e.selected:
            imageUtil.DrawImage(entitySelectionImage, x, y)

def DrawPage():
    
    #draw tile grid background
    imageUtil.DrawImage(tileGridBackgroundImage, gridOrigin.x - 32, gridOrigin.y - 27)
    
    #draw tile grid
    if bgLayerActive:
        DrawTileGrid(screenData.bgLayer)
    if fgLayerActive:
        DrawTileGrid(screenData.fgLayer)
    if wallsLayerActive:
        DrawTileGrid(screenData.wallsLayer)
    if entitiesActive:
        DrawEntities(screenData.entities)
        
    
    #draw tile palette
    imageUtil.DrawRectangle(tilePaletteOrigin, tilePaletteWidth * gridTileSize, tilePaletteHeight * gridTileSize, "grey")
    for i in range(len(tileTypeData.tileTypes)):
        if tileTypeData.tileTypes[i] is not None:
            image = tileTypeData.tileTypes[i].image if tileTypeData.tileTypes[i].image is not None else blankTile
            imageUtil.DrawImage(image, (i % tilePaletteWidth) * gridTileSize + tilePaletteOrigin.x, (i // tilePaletteWidth) * gridTileSize + tilePaletteOrigin.y)
                
    #draw entity palette
    imageUtil.DrawRectangle(entityPaletteOrigin, entityPaletteWidth * gridTileSize, entityPaletteHeight * gridTileSize, "grey")
    for i in range(len(entityTypeData.entityTypes)):
        if entityTypeData.entityTypes[i] is not None:
            image = entityTypeData.entityTypes[i].image
            imageUtil.DrawImage(image, (i % entityPaletteWidth) * gridTileSize + entityPaletteOrigin.x + gridTileSize / 2, (i // entityPaletteWidth) * gridTileSize + entityPaletteOrigin.y + gridTileSize / 2)
    
    #draw toolbar
    imageUtil.DrawImage(toolbarImage, toolbarOrigin.x, toolbarOrigin.y)
    #draw toolbar selections
    if fgLayerActive:
        DrawSelectionBoxOverToolbarButton(0)
    if bgLayerActive:
        DrawSelectionBoxOverToolbarButton(1)
    if wallsLayerActive:
        DrawSelectionBoxOverToolbarButton(2)
    if entitiesActive:
        DrawSelectionBoxOverToolbarButton(3)
    if selectedLayer == Layer.FOREGROUND:
        DrawSelectionBoxOverToolbarButton(4)
    if selectedLayer == Layer.BACKGROUND:
        DrawSelectionBoxOverToolbarButton(5)
    if selectedLayer == Layer.WALLS:
        DrawSelectionBoxOverToolbarButton(6)
    if selectedLayer == Layer.ENTITIES:
        DrawSelectionBoxOverToolbarButton(7)
    if entitiesGridSnapSelected:
        DrawSelectionBoxOverToolbarButton(8)
    
    #draw selected tile or entity
    if selectedTile is not None:
        if selectedTile.image is not None:
            imageUtil.DrawImage(selectedTile.image, 1400, 180)
        else:
            imageUtil.DrawImage(blankTile, 1400, 180)
    elif selectedEntityType is not None:
        if selectedEntityType.image is not None:
            imageUtil.DrawImage(selectedEntityType.image, 1400, 180)
        else:
            imageUtil.DrawImage(blankTile, 1400, 180)
    else:
        imageUtil.DrawImage(blankTile, 1400, 180)
    
    #draw entity type being dragged
    if entityPaletteClicked:
        pos = mousePos.Clone()
        pos -= gridOrigin
        SnapPointToGrid(pos, gridTileSize / 2)
        pos += gridOrigin
        imageUtil.DrawImage(selectedEntityType.image, pos.x, pos.y)
    
    #display entity/entities being edited attribute text
    imageUtil.DrawRectangle(entityAttribTextBoxPos, entityAttribTextBoxWidth, entityAttribTextBoxHeight, entityAttribColour)
    if selectedLayer == Layer.ENTITIES:
        imageUtil.DisplayText(selectedEntityAttribsText, entityAttribTextBoxPos.x + 10, entityAttribTextBoxPos.y + entityAttribTextBoxHeight / 2, 16)
    
    #imageUtil.DisplayText("Mouse position: " + str(mousePos), 100, 50, 16)

def Update(frameTime):
    pass