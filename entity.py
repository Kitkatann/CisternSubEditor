from vector2D import Vector2D

class Entity:
    def __init__(self, entityType, x, y, selected, attributes):
        self.entityType = entityType
        self.x = x
        self.y = y
        self.selected = selected
        self.attributes = attributes
        self.dragOffset = Vector2D(0, 0)


