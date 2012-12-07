#!/usr/bin/python

import os
import sys
import math

from PIL import Image
from fysom import Fysom

### Utils
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

def isWhite(pixel):
  # Fairly arbitrary, but our ref image is just whitish and darkish two tone
  return (pixel[0] + pixel[1] + pixel[2])/3 > 200




### FSM Methods

def buildFSM():
  # This is the meat of the application
  # We progress one pixel across on both our two rows
  #
  # The algorithm assumes 2xN bricks are better than 1xN. It tries to build
  # up the largest 2xN brick (up to 2x8). If at any time only one of the rows
  # needs a brick, we'll revert back to the previous 2xN brick and create a
  # single brick on the appropriate row.
  #
  # We then carry on increasing the length of this single brick until we get
  # to a double brick again. At which point we save the bricks and then start over 
  #
  # If neither row needs a brick, we just carry on. Easy.
  # 
  # State needed:
  # Current bricks. There are 6 valid states (any more complex and we'd start 
  # over with a new brick):
  # #noBricks           - No bricks/start
  # #topBrick           - Brick on top row and no brick on bottom row
  # #bottomBrick        - Brick on bottom row and no brick on top row
  # #bothBrick          - Brick on both rows
  # #bothAndTopBrick    - Brick on both rows, and additional brick on top row
  # #bothAndBottomBrick - Brick on both rows, and additional brick on bottom row
  #
  # There are 4 valid states for the current column, which act as events in the state machine
  # #bothWhite   - Both white
  # #bothEmpty   - Both blue (empty)
  # #topWhite    - Top white, bottom blue
  # #bottomWhite - Bottom white, top blue

  global fsm
  fsm = Fysom({
    'initial': 'noBricks',
    'events': [
      {'name': 'bothWhite',   'src': 'noBricks',           'dst': 'bothBrick'},
      {'name': 'bothWhite',   'src': 'topBrick',           'dst': 'noBricks'},
      {'name': 'bothWhite',   'src': 'bottomBrick',        'dst': 'noBricks'},
      {'name': 'bothWhite',   'src': 'bothBrick',          'dst': 'bothBrick'},
      {'name': 'bothWhite',   'src': 'bothAndTopBrick',    'dst': 'noBricks'},
      {'name': 'bothWhite',   'src': 'bothAndBottomBrick', 'dst': 'noBricks'},

      {'name': 'bothEmpty',   'src': 'noBricks',           'dst': 'noBricks'},
      {'name': 'bothEmpty',   'src': 'topBrick',           'dst': 'noBricks'},
      {'name': 'bothEmpty',   'src': 'bottomBrick',        'dst': 'noBricks'},
      {'name': 'bothEmpty',   'src': 'bothBrick',          'dst': 'noBricks'},
      {'name': 'bothEmpty',   'src': 'bothAndTopBrick',    'dst': 'noBricks'},
      {'name': 'bothEmpty',   'src': 'bothAndBottomBrick', 'dst': 'noBricks'},

      {'name': 'topWhite',    'src': 'noBricks',           'dst': 'topBrick'},
      {'name': 'topWhite',    'src': 'topBrick',           'dst': 'topBrick'},
      {'name': 'topWhite',    'src': 'bottomBrick',        'dst': 'noBricks'},
      {'name': 'topWhite',    'src': 'bothBrick',          'dst': 'bothAndTopBrick'},
      {'name': 'topWhite',    'src': 'bothAndTopBrick',    'dst': 'bothAndTopBrick'},
      {'name': 'topWhite',    'src': 'bothAndBottomBrick', 'dst': 'noBricks'},

      {'name': 'bottomWhite', 'src': 'noBricks',           'dst': 'bottomBrick'},
      {'name': 'bottomWhite', 'src': 'topBrick',           'dst': 'noBricks'},
      {'name': 'bottomWhite', 'src': 'bottomBrick',        'dst': 'bottomBrick'},
      {'name': 'bottomWhite', 'src': 'bothBrick',          'dst': 'bothAndBottomBrick'},
      {'name': 'bottomWhite', 'src': 'bothAndTopBrick',    'dst': 'noBricks'},
      {'name': 'bottomWhite', 'src': 'bothAndBottomBrick', 'dst': 'bothAndBottomBrick'}
    ],
    'callbacks': {
#      'onbeforebothWhite'         : onBeforeBothWhite,
#      'onbeforebothEmpty'         : onBeforeBothEmpty,
#      'onbeforetopWhite'          : onBeforeTopWhite,
#      'onbeforebottomWhite'       : onBeforeBottomWhite,

      'onenternoBricks'           : onEnterNoBricks,
      'onentertopBrick'           : onEnterTopBrick,
      'onenterbottomBrick'        : onEnterBottomBrick,
      'onenterbothBrick'          : onEnterBothBrick,
      'onenterbothAndTopBrick'    : onEnterBothAndTopBrick,
      'onenterbothAndBottomBrick' : onEnterBothAndBottomBrick
    }
  })


  return fsm;

# FSM callbacks
def onBeforeBothWhite(e):
  print "on before both white"

def onBeforeBothEmpty(e):
  print "on before both empty"

def onBeforeTopWhite(e):
  print "on before top white"

def onBeforeBottomWhite(e):
  print "on before bottom white"

def onEnterNoBricks(e):
  print "Entering no bricks"

  global bothBrickStart
  global singleBrickStart

  if hasattr(e, 'coords'):
    # Should always be true once we've found a single white brick
    i = e.coords[0]
    j = e.coords[1]

    singleBrickLength = i - singleBrickStart
    bothBrickLength = i - singleBrickLength - bothBrickStart 

    print e.event + " for pixels at " + str(i) + ":" + str(2*j) + " and " + str(i) + ":" + str(2*j+1)
    print "Bricks in current state: " + str(bothBrickLength) + " : " + str(singleBrickLength)

    bothBrickStart = i
    singleBrickStart = i

    # The 'No Brick' state is a kind of dummy state. It allows us to reset our counters,
    # but we still want to move into the correct state
    if e.event == "bothWhite":
      fsm.bothWhite(coords=e.coords)
    elif e.event == "topWhite":
      fsm.topWhite(coords=e.coords)
    elif e.event == "bottomWhite":
      fsm.bottomWhite(coords=e.coords)
    elif e.event == "bothEmpty":
      fsm.bothEmpty(coords=e.coords)
    else:
      if hasattr(e, 'event'):
        print "BROKEN INVESTIGATE for " + e.event
      else:
        print "BROKEN INVESTIGATE - no event!"


def onEnterTopBrick(e):
  global bothBrickStart
  global singleBrickStart

  bothBrickStart = e.coords[0]
  singleBrickStart = e.coords[0]

def onEnterBottomBrick(e):
  global bothBrickStart
  global singleBrickStart

  bothBrickStart = e.coords[0]
  singleBrickStart = e.coords[0]

def onEnterBothBrick(e):
  global bothBrickStart
  bothBrickStart = e.coords[0]

def onEnterBothAndTopBrick(e):
  global singleBrickStart
  singleBrickStart = e.coords[0]

def onEnterBothAndBottomBrick(e):
  global singleBrickStart
  singleBrickStart = e.coords[0]




### Step the state machine
def stepTwoLines(i, j, topPixel, bottomPixel):
  global fsm
  topIsWhite = isWhite(topPixel)
  bottomIsWhite = isWhite(bottomPixel)

  coords=(i,j)
  print str(i) + ":" + str(j) + " - " + fsm.current

  if topIsWhite and bottomIsWhite:
    fsm.bothWhite(coords=coords)
  elif topIsWhite and not bottomIsWhite:
    fsm.topWhite(coords=coords)
  elif bottomIsWhite and not topIsWhite:
    fsm.bottomWhite(coords=coords)
  else:
    fsm.bothEmpty(coords=coords)

  return

def stepSingleLine(i, j, topPixel):
  # Similar to the previous function, but simpler. Just traverse along the line
  # making the longest pieces possible

  # This is equivalent to a bottom line which is empty :)
  return stepTwoLines(i, j, topPixel, (0,0,0))




### Let's GO!
def main():
  # Lazy, use globals
  global fsm
  global bothBrickStart
  global singleBrickStart

  parts_list = generatePartsList()
  shopping_list = {}

  im = loadImage()

  imageW = im.size[0]
  imageH = im.size[1]

  bothBrickStart = 0
  singleBrickStart = 0

  fsm = buildFSM()

  processLastLine = False
  if (imageH%2 != 0):
    imageH = imageH - 1
    processLastLine = True

  pixels = im.load()  
  for j in range(imageH/2):
    bothBrickStart = 0
    singleBrickStart = 0

    for i in range(imageW):
      topPixel = pixels[i, j*2]
      bottomPixel = pixels[i, j*2+1]
      
      stepTwoLines(i, j, topPixel, bottomPixel)      

  if processLastLine:
    for i in range(imageW):
      stepTwoLines(i, imageH, pixels[i, imageH])

if __name__ == '__main__':
  main()