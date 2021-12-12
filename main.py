import pyglet
from pyglet.window import key
from pyglet.gl import *
from pyglet import clock
from pyglet.media import StaticSource
import editorPage
import browserPage
import imageUtil
import pageData
from vector2D import Vector2D
from pageData import Page


window = pyglet.window.Window(fullscreen=True)

#enable alpha blending
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

currentPageModule = browserPage


pageData.SetCurrentPage(Page.BROWSER)

@window.event
def on_key_press(symbol, modifiers):
    if currentPageModule is not None:
        currentPageModule.KeyPressed(symbol, modifiers)

@window.event
def on_mouse_press(x, y, button, modifiers):
    if currentPageModule is not None:
        currentPageModule.MousePressed(x, y, button, modifiers)

@window.event
def on_mouse_motion(x, y, dx, dy):
    MouseMoved(x, y, dx, dy)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    MouseMoved(x, y, dx, dy)
    currentPageModule.MouseDragged(x, y, dx, dy, buttons, modifiers)
    
@window.event
def on_mouse_release(x, y, button, modifiers):
    if currentPageModule is not None:
        currentPageModule.MouseReleased(x, y, button, modifiers)

def MouseMoved(x, y, dx, dy):
    if currentPageModule is not None:
        currentPageModule.MouseMoved(x, y, dx, dy)

@window.event
def on_draw():
    window.clear()
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    
    
    if currentPageModule is not None:
        currentPageModule.DrawPage()
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    

def Update(dt):
    global currentPageModule
    
    if pageData.currentPage == Page.EDITOR:
        currentPageModule = editorPage
    if pageData.currentPage == Page.BROWSER:
        currentPageModule = browserPage
    if currentPageModule is not None:
        currentPageModule.Update(dt)
    
    


pyglet.clock.schedule_interval(Update, 1/60.0)
pyglet.app.run()