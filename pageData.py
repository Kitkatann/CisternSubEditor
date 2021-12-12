from enum import Enum

class Page(Enum):
    EDITOR = 1
    BROWSER = 2
    
currentPage = Page.EDITOR

def SetCurrentPage(page):
    global currentPage
    currentPage = page