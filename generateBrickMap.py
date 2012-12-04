#!/usr/bin/python

import os
import sys
import math

from PIL import Image

class Brick:
  def __init__(self, id, cost, mapColor):
    self.id = id
    self.cost = cost
    self.mapColor = mapColor

# Call to store the state of the bricks being calculated
class BrickStore:
  def __init__(self):
    self.empty = True

  def setDoubleBrick(self, brick):
    this.doubleBrick = brick

  def setTopBrick(self, brick):
    this.topBrick = brick

  def setBottomBrick(self, brick):
    this.bottomBrick = brick

def generatePartsList():
  partsList = {}

  partsList["0x0"]  = Brick("0x0" , 0 , "0xFFFFFF")
  partsList["1x1"]  = Brick("1x1" , 10, "0x000000")
  partsList["1x2"]  = Brick("1x2" , 15, "0x0000FF")
  partsList["1x3"]  = Brick("1x3" , 20, "0x00FF00")
  partsList["1x4"]  = Brick("1x4" , 20, "0xFF0000")
  partsList["1x6"]  = Brick("1x6" , 25, "0xFFFF00")
  partsList["1x8"]  = Brick("1x8" , 25, "0xFF00FF")
  partsList["1x10"] = Brick("1x10", 25, "0x00FFFF")
  partsList["1x12"] = Brick("1x12", 30, "0xFF00FF")
  partsList["1x16"] = Brick("1x16", 50, "0xAAAAAA")
  partsList["2x2"]  = Brick("2x2" , 15, "0xFFFFAA")
  partsList["2x3"]  = Brick("2x3" , 25, "0xFFAAFF")
  partsList["2x4"]  = Brick("2x4" , 30, "0xAAFFFF")
  partsList["2x6"]  = Brick("2x6" , 30, "0xAAAAFF")
  partsList["2x8"]  = Brick("2x8" , 30, "0XAAFFAA")

  return partsList

def loadImage():
  path = os.getcwd()
  img_filename = "%s/images/LondonLogo_small_whiteonly.png" % path
  im = Image.open(img_filename)
  im = im.convert('RGB')

  return im

def stepTwoLines(topPixel, bottomPixel):
  # This is the meat of the application
  # We progress one pixel across on both our two rows
  #
  # The algorithm assumes 2x? bricks are better than 1x?. It tries to build
  # up the largest 2x? brick (up to 2x8). If at any time only one of the rows
  # needs a brick, we'll revert back to the previous 2x? brick and create a
  # single brick on the appropriate row.
  #
  # We then carry on increasing the length of this single brick until we get
  # to a double brick again. At which point we save the bricks and then start over 
  #
  # If neither row needs a brick, we just carry on. Easy.
  # 
  # State needed:
  # Current bricks. There are 5 valid states (any more complex and we'd start 
  # over with a new brick):
  # Brick on top row and no brick on bottom row
  # Brick on bottom row and no brick on top row
  # Brick on both rows
  # Brick on both rows, and additional brick on top row
  # Brick on both rows, and additional brick on bottom row

  

  return

def stepSingleLine(topPixel):
  # Similar to the previous function, but simpler. Just traverse along the line
  # making the longest pieces possible

  return

def main():
  parts_list = generatePartsList()

  im = loadImage()

  imageW = im.size[0]
  imageH = im.size[1]

  global curX
  global curY
  global curBricks

  curX = 0
  curY = 0
  curBricks = False

  processLastLine = False
  if (imageH%2 != 0):
    imageH = imageH - 1
    processLastLine = True

  pixels = im.load()  
  for i in range(imageH/2):
    curX = 0
    curY = i*2
    curBricks = False

    while curX < imageW:
      stepTwoLines(pixels[curX, curY], pixels[curX, curY+1])

  shopping_list = {}

if __name__ == '__main__':
  main()