from tileType import TileType
import imageUtil

#pre-defined tile assets with set collision type - read from tileData.txt
tileTypes = []
def LoadTileTypes():
    f = open("data/tileData.txt", "r")
    for line in f:
        tileData = []
        for word in line.split():
            tileData.append(word)
        if len(tileData) == 3:
            tileTypes.append(TileType(int(tileData[0]), imageUtil.LoadImage("images/" + tileData[1], False), tileData[2]))
    f.close()
    tileTypes.append(TileType(0, None, "water"))
    
def GetTileTypeByID(id):
    for t in tileTypes:
        if t.id == id:
            return t