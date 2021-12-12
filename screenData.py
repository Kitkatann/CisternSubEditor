import tileTypeData
from entity import Entity

bgLayer = []
fgLayer = []
wallsLayer = []

entities = []

gridWidth = 33
gridHeight = 24

def SetLayersBlank():
    for i in range(gridWidth * gridHeight):
        bgLayer.append(tileTypeData.GetTileTypeByID(0))
        fgLayer.append(tileTypeData.GetTileTypeByID(0))
        wallsLayer.append(tileTypeData.GetTileTypeByID(0))

SetLayersBlank()

def CreateEntity(entityType, x, y):
    entities.append(Entity(entityType, x, y, True, ""))

#clear all tiles in selected screen (replace with tile ID 0)
def ClearAllLayers():
    entities.clear()
    for i in range(gridWidth * gridHeight):
        bgLayer[i] = tileTypeData.GetTileTypeByID(0)
        fgLayer[i] = tileTypeData.GetTileTypeByID(0)
        wallsLayer[i] = tileTypeData.GetTileTypeByID(0)
    