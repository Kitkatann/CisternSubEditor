import screenData
import tileTypeData
import entityTypeData
from entity import Entity

selectedScreenFilename = ""


#pre-defined level data, muliple layers with the tile IDs for each tile in those layers - read from levelData.txt
def LoadLevelData():
    currentCommand = ""

    keywords = ["bgTiles", "fgTiles", "wallTiles", "entity"]
    screenData.ClearAllLayers()
    f = open(selectedScreenFilename, "r")
    for line in f:
        if line.split()[0] in keywords:
            #if line describes background tiles
            if line.split()[0] == "bgTiles":
                for word in line.split():
                    #line format: bgTiles <width> <height>
                    currentCommand = "bgTiles"
            #if line describes foreground tiles
            if line.split()[0] == "fgTiles":
                for word in line.split():
                    #line format: fgTiles <width> <height>
                    currentCommand = "fgTiles"
            #if line describes wall tiles
            if line.split()[0] == "wallTiles":
                for word in line.split():
                    #line format: wallTiles <width> <height>
                    currentCommand = "wallTiles"
            #if line describes entity
            if line.split()[0] == "entity":
                entityData = []
                for word in line.split():
                    #line format: <entity> <entityTypeID> <x> <y> <attributes>
                    currentCommand = "entity"
                    entityData.append(word)
                attributes = ""
                if len(entityData) > 4:
                    attributes = " ".join(entityData[4:])
                screenData.entities.append(Entity(entityTypeData.GetEntityTypeByID(int(entityData[1])), float(entityData[2]), float(entityData[3]), False, attributes))
        else:
            if currentCommand == "bgTiles":
                for i in range(len(line.split())):
                    word = line.split()[i]
                    #line format: <tileID> <tileID> <tileID> etc.
                    screenData.bgLayer[i] = tileTypeData.GetTileTypeByID(int(word))
                currentCommand = ""
            if currentCommand == "fgTiles":
                for i in range(len(line.split())):
                    word = line.split()[i]
                    #line format: <tileID> <tileID> <tileID> etc.
                    screenData.fgLayer[i] = tileTypeData.GetTileTypeByID(int(word))
                currentCommand = ""
            if currentCommand == "wallTiles":
                for i in range(len(line.split())):
                    word = line.split()[i]
                    #line format: <tileID> <tileID> <tileID> etc.
                    screenData.wallsLayer[i] = tileTypeData.GetTileTypeByID(int(word))
                currentCommand = ""
    f.close()
    
def SaveData():
    f = open(selectedScreenFilename, "w")
    lines = []
    
    #add tile IDs for the background, foreground, and walls layers
    lines.append("bgTiles ")
    lines[0] = lines[0] + str(screenData.gridWidth) + " " + str(screenData.gridHeight) + " "
    
    lines.append("")
    for tile in screenData.bgLayer:
        id = ""
        if tile is not None:
            id = str(tile.id)
        else:
            id = "0"
        lines[1] = lines[1] + id + " "
    
    lines.append("fgTiles ")
    lines[2] = lines[2] + str(screenData.gridWidth) + " " + str(screenData.gridHeight) + " "
    lines.append("")
    for tile in screenData.fgLayer:
        id = ""
        if tile is not None:
            id = str(tile.id)
        else:
            id = "0"
        lines[3] = lines[3] + id + " "
    
    lines.append("wallTiles ")
    lines[4] = lines[4] + str(screenData.gridWidth) + " " + str(screenData.gridHeight) + " "
    lines.append("")
    for tile in screenData.wallsLayer:
        id = ""
        if tile is not None:
            id = str(tile.id)
        else:
            id = "0"
        lines[5] = lines[5] + id + " "   
    
    for entity in screenData.entities:
            lines.append("entity " + str(entity.entityType.id) + " " + str(entity.x) + " " + str(entity.y) + " " + entity.attributes)
    
    for line in lines:
        f.write(line)
        f.write('\n')
    f.close()
