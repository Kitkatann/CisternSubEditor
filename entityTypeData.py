from entityType import EntityType
import imageUtil

#pre-defined entity assets with set type - read from editorEntitiesData.txt
entityTypes = []
def LoadEntityTypes():
    f = open("data/entitiesData.txt", "r")
    for line in f:
        entityData = []
        for word in line.split():
            entityData.append(word)
        if len(entityData) == 3:
            entityTypes.append(EntityType(int(entityData[0]), imageUtil.LoadImage("images/" + entityData[1]), entityData[2]))
    f.close()
    
def GetEntityTypeByID(id):
    for e in entityTypes:
        if e.id == id:
            return e