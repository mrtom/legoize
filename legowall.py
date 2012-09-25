#!/usr/bin/python

import os
import sys
import urllib2

from BeautifulSoup import BeautifulSoup
from PIL import Image

class BrickColor:
  def __init__(self, id, name, red, green, blue):
    self.id = id
    self.name = name
    self.red = red
    self.green = green
    self.blue = blue

  def __str__(self):
    return '{0}({1}) :: (r:{2},g:{3},b:{4})'.format(self.name, self.id, self.red, self.green, self.blue)

def main():
  soup = BeautifulSoup(urllib2.urlopen('http://www.peeron.com/cgi-bin/invcgis/colorguide.cgi').read())

  # Get all the colors
  BricksList = []
  for row in soup('table')[0]('tr'):
    tds = row('td')
    if tds and tds[0].string.isdigit():
      #print tds[0].string, tds[1].string, tds[7].string, tds[8].string, tds[9].string
      brick = BrickColor(tds[0].string, tds[1].string, tds[7].string, tds[8].string, tds[9].string)
      BricksList.append(brick)

  # Get the donor image
  path = os.getcwd()
  img_filename = "%s/FacebookLondon.png" % path
  im = Image.open(img_filename)

  # Go over it pixel by pixel and change the color to the closest match in our BricksList
  imageW = im.size[0]
  imageH = im.size[1]

  pixels = list(im.getdata())
  for y in range(0, imageH):
    for x in range(0, imageW):
      offset = y*imageW + x
      xy = (x, y)
      rgb = im.getpixel(xy)

      print rgb
  

if __name__ == '__main__':
  main()

