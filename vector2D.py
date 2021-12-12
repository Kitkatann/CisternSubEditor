import math

class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector2D(x, y)
        
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector2D(x, y)
    
    def __mul__(self, other):
        if isinstance(other, Vector2D):
            x = self.x * other.x
            y = self.y * other.y
        elif isinstance(other, float):
            x = self.x * other
            y = self.y * other
        elif isinstance(other, int):
            x = self.x * other
            y = self.y * other
        return Vector2D(x, y)
        
    def __truediv__(self, other):
        if isinstance(other, Vector2D):
            x = self.x / other.x
            y = self.y / other.y
        elif isinstance(other, float):
            x = self.x / other
            y = self.y / other
        return Vector2D(x, y)
     
    def  __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
            
    def CopyFrom(self, other):
        self.x = other.x
        self.y = other.y
        
    def Clone(self):
        return Vector2D(self.x, self.y)
        
    def DistanceToPoint(self, point):
        ax = (self.x - point.x)
        ay = (self.y - point.y)
        return math.sqrt(ax * ax + ay * ay)