import matplotlib.pyplot as plt
import numpy as np
import pygame as pg
import math
import json



class ColorStatus(object):
    unchecked = 0
    checked = 1
    complete = 2
    start = 3
    end = 4
    boundary = 5
    best = 6
    _cunchecked = (158, 158, 158)
    _cchecked = (255, 255, 255)
    _ccomplete = (255, 220, 0)
    _cstart = (0, 255, 0)
    _cend = (0, 0, 255)
    _cboundary = (0, 0, 0)
    _cbest = (255, 0, 0)
    background = (0, 0, 0)
    def __init__(self):
        self.getlist = {0: self._cunchecked, 1: self._cchecked, 2:self._ccomplete, 3:self._cstart, 4:self._cend, 5:self._cboundary, 6:self._cbest}
    def Get(self, num):
        return self.getlist[num]
        
COLORPALLET = ColorStatus()

class AStarWeights(object):
    lateral = 10
    diagonal = 14
    heuristic = 10

WEIGHTS = AStarWeights()

class ACell(object):
    def __init__(self, x, y, width, height, id):
        self.parent = (-1, -1)
        self.g = int(100000000)
        self.h = int(100000000)
        self.val = int(1000000)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.status = COLORPALLET.unchecked
        self._id = id
        self.changed = True
    def __iter__(self):
        yield self.val
        yield self.g
        yield self.h
    def __lt__(self, other):
        return self.val < other.val
    def Draw(self, window, font):
        if self.changed:
            window.fill(COLORPALLET.Get(self.status), rect=(self.x+1, self.y+1, self.width-2, self.height-2))
            self.changed = False
        # testfont = font.render("{}, {}".format(self._id[0], self._id[1]), False, (0, 0, 0))
        # window.blit(testfont, (self.x + 1, self.y + 1))
    def SetEnd(self, end):
        self.end = end
        if self._id == self.end:
            self.status = COLORPALLET.end
    def SetStart(self, start):
        self.start = start
        self.parent = start
        if self._id == start:
            self.status = COLORPALLET.start
            self.g = 0
            self.val = 0
    def Update(self, parent, weight):
        if self.status == COLORPALLET.boundary or self.status == COLORPALLET.complete or self.status == COLORPALLET.start:
            return False, self.end == self._id
        if  self.g > weight:
            self.parent = parent
            self.h = round(math.sqrt((self._id[1]-self.end[1])**2+(self._id[0]-self.end[0])**2),0)*WEIGHTS.heuristic
            self.g = weight
            self.val = self.h + self.g
            self.SetStatus(COLORPALLET.checked)
            self.changed = True
            if self.status != COLORPALLET.start and self.status != COLORPALLET.end:
                self.status = COLORPALLET.checked
            return True, self.end == self._id
        return False, self.end == self._id
    def Print(self):
        print("Cell ({}, {}) has value {}".format(self._id[0], self._id[1], self.val))
    def SetStatus(self, status):
        if self.status != COLORPALLET.start and self.status != COLORPALLET.end:
            self.status = status
            self.changed = True

class CellGrid(object):
    def __init__(self, nxcell, nycell, dx, dy):
        self.celllist = []
        self._nxcell = nxcell
        self._nycell = nycell
        self._updateList = []
        self._complete = False
        self._failed = False
        for i in range(0, nycell):
            for j in range(0, nxcell):
                self.celllist.append(ACell(j*dx, i*dy, dx, dy, (j, i)))
    def GetList(self):
        return self.celllist
    def Update(self):
        if self._complete:
            self.BuildBestRoute()
            return
        if len(self._updateList) == 0:
            self._failed = True
            return
        mincell = min(self._updateList)
        cellloc = mincell._id
        mincell.SetStatus(COLORPALLET.complete)
        self._updateList.remove(mincell)
        for i in range(-1, 2):
            for j in range(-1, 2):
                weight = mincell.g
                if i == 0 and j == 0:
                    continue
                if i == 0 or j == 0:
                    weight += WEIGHTS.lateral
                else:
                    weight += WEIGHTS.diagonal
                if i+cellloc[0] < self._nxcell and i+cellloc[0] >= 0:
                    if j+cellloc[1] < self._nycell and j+cellloc[1] >= 0:
                        addtolist, isend = self.celllist[i+cellloc[0] + (j+cellloc[1])*self._nxcell].Update(cellloc, weight)
                        if addtolist:
                            self._updateList.append(self.celllist[i+cellloc[0]+self._nxcell*(j+cellloc[1])])
                        if isend:
                            self._complete = True
    def SetEnd(self, end):
        for cell in self.celllist:
            cell.SetEnd(end)
    def SetStart(self, start):
        self._minIndex = start[0]+self._nxcell*start[1]
        for cell in self.celllist:
            cell.SetStart(start)
        cell = self.celllist[start[0]+self._nxcell*start[1]]
        self._updateList.append(cell)
    def GetCell(self, ix, iy):
        return self.celllist[ix+iy*self._nxcell]
    def BuildBestRoute(self):
        end = self.celllist[0].end
        start = self.celllist[0].start
        curr = end
        while (curr != start):
            cell = self.GetCell(curr[0], curr[1])
            cell.SetStatus(COLORPALLET.best)
            curr = cell.parent
    def SetBoundary(self, boundarylist):
        for id in boundarylist:
            self.GetCell(id[0], id[1]).SetStatus(COLORPALLET.boundary)
def getGrid(refinement, windowXMax, windowYMax):
    ncell1d = refinement
    cellWidth = round(windowXMax / ncell1d /10,0)*10
    print(cellWidth)
    assert(cellWidth >=4)
    #cellHeight = round(windowYMax / ncell1d / 10,0)*10
    cellHeight = cellWidth
    ncelly = int( windowYMax / cellHeight)
    print(cellHeight)
    assert(cellHeight >= 4)
    return CellGrid(ncell1d, ncelly, cellWidth, cellHeight)

def run(windowXMax, windowYMax, refinemnetX, cellStart, cellEnd, boundaryFilename = 0):
    # windowXMax = 1500
    # windowYMax = 1000
    # boundaryFilename = "boundary.json"
    # refinemnetX = 150
    # cellStart = (1, 1)
    # cellEnd = (148, 98)
    pg.init()
    pg.font.init()
    sysfont = pg.font.SysFont('arial', 30)
    window = pg.display.set_mode((windowXMax, windowYMax))
    pg.display.set_caption("A Start Search")
    keepRunning = True
    gridlist = getGrid(refinemnetX, windowXMax, windowYMax)
    gridlist.SetStart(cellStart)
    gridlist.SetEnd(cellEnd)
    if boundaryFilename != 0:
        boundaryFile = open(boundaryFilename)
        boundarylist = json.load(boundaryFile)
        gridlist.SetBoundary(boundarylist)
    gridlist.Update()
    window.fill(COLORPALLET.background)
    failmessage = sysfont.render("Failed to find solution", False, (255, 255, 255), (0, 0, 0))
    failbox = failmessage.get_rect()
    while keepRunning:
        #pg.time.delay(1)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                keepRunning = False
            if event.type == pg.MOUSEBUTTONDOWN:
                ps = pg
        keys = pg.key.get_pressed()
        gridlist.Update()
        if gridlist._failed:
            window.blit(failmessage, failbox)
        for cell in gridlist.GetList():
            cell.Draw(window, sysfont)
        pg.display.update()
    pg.quit()

if __name__ ==  "__main__":
    windowXMax = 1500
    windowYMax = 1000
    boundaryFilename = "boundary.json"
    refinemnetX = 150
    cellStart = (1, 1)
    cellEnd = (148, 98)
    run(windowXMax, windowYMax, refinemnetX, cellStart, cellEnd, boundaryFilename)