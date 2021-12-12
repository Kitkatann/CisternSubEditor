import pyglet
from pyglet import image
from pyglet.gl import *
from pyglet import shapes
from vector2D import Vector2D

batch = pyglet.graphics.Batch()

myColors = {"grey":(77, 77, 77), "red":(255,0,0)}

def LoadImage(filename):
    im = image.load(filename)
    texture = im.get_texture()
    glEnable(texture.target)
    glBindTexture(texture.target, texture.id)
    glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    return im

def DrawImage(image, x, y):
    image.blit(x, y)

def DrawRectangle(BLPos, width, height, colour):
    rectangle = shapes.Rectangle(BLPos.x, BLPos.y, width, height, color=myColors[colour], batch=batch)
    batch.draw()

def DisplayText(text, x, y, fontSize):
    label = pyglet.text.Label(text,
                    font_name='Times New Roman',
                    font_size=fontSize,
                    color=(255,255,255,255),
                    x=x, y=y,
                    anchor_x='left', anchor_y='center')
    label.draw()