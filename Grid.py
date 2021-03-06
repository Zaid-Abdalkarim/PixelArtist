from Pixel import *
import pygame
import pyautogui
import tkinter
import sys
import os
import keyboard as kb
import numpy as np
from PIL import Image

sys.setrecursionlimit(10000)
pygame.init()

sw, sh = 960, 800
screen = pygame.display.set_mode((sw, sh))

width = screen.get_width()
height = screen.get_height()

allColors = [(255, 15, 15), (170, 170, 170), (85, 85, 85), (15, 15, 15),
             (255, 255, 85), (0, 170, 0), (85, 255, 85), (255, 85, 85),
             (170, 0, 0), (170, 85, 0), (170, 0, 170), (255, 85, 255),
             (85, 255, 255), (0, 170, 170), (0, 0, 170), (85, 85, 255)]
selectedColor = allColors[0]


class Grid(object):
    def __init__(self, pixelSize, documentSize, offsetX, offsetY):
        self.documentSize = documentSize
        self.pixelSize = pixelSize
        rows, cols = (pixelSize, pixelSize)
        self.arr = []

        # This initalizes every pixel and places every pixel in the correct position
        for i in range(cols):
            col = []
            for j in range(rows):
                col.append(
                    Pixel(self.documentSize / self.pixelSize,
                          (((((self.documentSize / self.pixelSize) * i) +
                             offsetX)),
                           (((self.documentSize / self.pixelSize) * j) +
                            offsetY))))
            self.arr.append(col)

    #draws all the pixels
    def Draw(self):
        for i in range(self.pixelSize):
            for j in range(self.pixelSize):
                pygame.draw.rect(
                    screen, self.arr[i][j].getColor(),
                    (self.arr[i][j].getLocationX(),
                     self.arr[i][j].getLocationY(), self.arr[i][j].getSize(),
                     self.arr[i][j].getSize()))
                if (pygame.mouse.get_pressed() == (1, 0, 0)):
                    if (self.arr[i][j].getLocationX() <=
                            pygame.mouse.get_pos()[0] <=
                            self.arr[i][j].getLocationX() +
                            self.arr[i][j].getSize()
                            and self.arr[i][j].getLocationY() <=
                            pygame.mouse.get_pos()[1] <=
                            self.arr[i][j].getLocationY() +
                            self.arr[i][j].getSize()):
                        self.arr[i][j].change_color(selectedColor)
                elif (pygame.mouse.get_pressed() == (0, 0, 1)):
                    if (self.arr[i][j].getLocationX() <=
                            pygame.mouse.get_pos()[0] <=
                            self.arr[i][j].getLocationX() +
                            self.arr[i][j].getSize()
                            and self.arr[i][j].getLocationY() <=
                            pygame.mouse.get_pos()[1] <=
                            self.arr[i][j].getLocationY() +
                            self.arr[i][j].getSize()):
                        self.arr[i][j].change_color((255, 255, 255))

    #changes specific pixel color
    def change_color(self, posx, posy, color):
        self.arr[posy][posx].change_color(color)

        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].change_color(self.color)

    #Updates the zoom for the page
    def updateZoomFactor(self, newDocumentSize, newOffsetX, newOffsetY):
        self.documentSize = newDocumentSize
        for i in range(self.pixelSize):
            for j in range(self.pixelSize):
                self.arr[i][j].setLocation(
                    ((((newDocumentSize / self.pixelSize) * i) + newOffsetX),
                     (((newDocumentSize / self.pixelSize) * j) + newOffsetY)))
                self.arr[i][j].setSize(newDocumentSize / self.pixelSize)

    #lets you move around the screen with middle click
    def updateOffset(self, newOffsetX, newOffsetY):
        for i in range(self.pixelSize):
            for j in range(self.pixelSize):
                self.arr[i][j].setLocation(
                    ((((self.documentSize / self.pixelSize) * i) + newOffsetX),
                     (((self.documentSize / self.pixelSize) * j) +
                      newOffsetY)))

    def Save(self, canvas_size):
        array = np.zeros([canvas_size, canvas_size, 3], dtype=np.uint8)
        for x in range(canvas_size):
            for y in range(canvas_size):
                array[y, x] = [
                    self.arr[x][y].getColor()[0], self.arr[x][y].getColor()[1],
                    self.arr[x][y].getColor()[2]
                ]
        rescaled = (255 / array.max() * (array - array.min())).astype(np.uint8)
        img = Image.fromarray(rescaled)
        img.save(
            "C://Users//Lepter//OneDrive//Desktop//Paint Replica//outfile.jpg",
            quality=100,
            subsampling=0)


#draws a typical rectangle with an outline
def draw_rect_border(fill_color, outline_color, outline_size, location, size):
    pygame.draw.rect(screen, outline_color,
                     (location[0], location[1], size[0] + outline_size,
                      size[1] + outline_size))
    pygame.draw.rect(screen, fill_color,
                     (location[0], location[1], size[0], size[1]))


#updates the selected color
def updateSelectedColor(_color):
    selectedColor = _color
    print(selectedColor)


#renders all the GUI on the right side
def renderGUI():
    draw_rect_border((25, 25, 25), (0, 0, 0), 5, (sw - 200, 0), (200, sh))
    global selectedColor
    index = 0
    for j in range(4):
        for y in range(4):
            Size = 30
            locX = (sw - 175) + (y * Size)
            locY = (sh / 2) - (j * Size)
            if (selectedColor == allColors[index]):
                draw_rect_border(allColors[index], (0, 0, 0), 2, (locX, locY),
                                 (Size, Size))
            else:
                pygame.draw.rect(screen, allColors[index],
                                 (locX, locY, Size, Size))

            if (pygame.mouse.get_pressed() == (1, 0, 0)):
                if (locX <= pygame.mouse.get_pos()[0] <= locX + Size
                        and locY <= pygame.mouse.get_pos()[1] <= locY + Size):
                    selectedColor = allColors[index]
            index = index + 1


zoomFactor = 400
offsetX = (sw - zoomFactor) / 2
offsetY = (sh - zoomFactor) / 2
canvas_size = 16
globalGrid = Grid(canvas_size, zoomFactor, offsetX, offsetY)
# screen size subtract what you want then divide by two I think
white = (255, 255, 255)

color_light = (170, 170, 170)
color_dark = (100, 100, 100)

running = True
isReleased = False
lastMousePos = pygame.mouse.get_pos()

choseAspect = False  # This is to check if the person has chosen the Pixel Art canvas Size

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 4:
                zoomFactor = zoomFactor + 100
                globalGrid.updateZoomFactor(zoomFactor, (sw - zoomFactor) / 2,
                                            (sh - zoomFactor) / 2)
            if e.button == 5:
                zoomFactor = zoomFactor + -100
                globalGrid.updateZoomFactor(zoomFactor, (sw - zoomFactor) / 2,
                                            (sh - zoomFactor) / 2)

    if kb.is_pressed("ctrl+s"):
        #save
        globalGrid.Save(canvas_size)

    screen.fill((30, 30, 30))

    screen.fill(allColors[3])  #background color

    if (pygame.mouse.get_pressed() == (0, 1, 0)):
        if (isReleased == False):
            isReleased = True
            lastMousePos = pygame.mouse.get_pos()
    else:
        if (isReleased == True):
            isReleased = False
            globalGrid.updateOffset(
                ((pygame.mouse.get_pos()[0] - lastMousePos[0]) / 3) + offsetX,
                ((pygame.mouse.get_pos()[1] - lastMousePos[1]) / 3) + offsetY)

    mouse = pygame.mouse.get_pos()
    globalGrid.Draw()
    renderGUI()
    pygame.display.flip()

pygame.quit()
