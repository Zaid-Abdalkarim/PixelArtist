import pygame as pg
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import sys


class Pixel(object):
    neighbor = []

    def __init__(self, size, location):
        self.size = size
        self.loc = location
        self.color = [255, 255, 255]
        self.pos = (0, 0)

    def change_color(self, color):
        self.color = color

    def getLocationX(self):
        return self.loc[0]

    def getLocationY(self):
        return self.loc[1]

    def setSize(self, _size):
        self.size = _size

    def getSize(self):
        return self.size

    def Draw(self, win, x, y):
        self.pos = (x, y)
        win.blit(self.subsurface, self.pos)

    def getNeighbor(self):
        return neighbor

    def setNeighbor(self, _neighbor):
        self.neighbor.append(_neighbor)

    def getColor(self):
        return self.color

    def setLocation(self, _location):
        self.loc = _location