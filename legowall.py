#!/usr/bin/python

import os
import sys
import math
import urllib2
import argparse

from BeautifulSoup import BeautifulSoup
from PIL import Image

class BrickColor:
  def __init__(self, id, name, red, green, blue):
    self.id = id
    self.name = name
    self.red = int(red)
    self.green = int(green)
    self.blue = int(blue)

  def __str__(self):
    return '{0}({1}) :: (r:{2},g:{3},b:{4})'.format(self.name, self.id, self.red, self.green, self.blue)

  def get_rgb(self):
    return (self.red, self.green, self.blue)


def find_best_match(sample_color, colors_list):
  # Given a sample colour, find the colour in the colour list
  # that is closest to the sample colour, according to closer_color
  if len(colors_list) is 0:
    print "Error: No colors in color_list!"
    return None
  elif len(colors_list) is 1:
    return colors_list[0]
  else:
    color_a = colors_list[0]
    color_b = find_best_match(sample_color, colors_list[1:])
    return closer_color(sample_color, color_a, color_b)

def closer_color(sample_color, color_a, color_b):
  # For now, just return color with lowest least square difference
  # TODO: There must be a neater way of doing this
  diff_a = pow((sample_color[0] - color_a.red),2)+pow((sample_color[1] - color_a.green),2)+pow((sample_color[2] - color_a.blue),2)
  diff_b = pow((sample_color[0] - color_b.red),2)+pow((sample_color[1] - color_b.green),2)+pow((sample_color[2] - color_b.blue),2)

  if (diff_a < diff_b):
    return color_a 
  else:
    return color_b

def colors_from_peerson():
  soup = BeautifulSoup(urllib2.urlopen('http://www.peeron.com/cgi-bin/invcgis/colorguide.cgi').read())

  # Get all the colors
  bricksList = []
  for row in soup('table')[0]('tr'):
    tds = row('td')
    if tds and tds[0].string.isdigit():
      brick = BrickColor(tds[0].string, tds[1].string, tds[7].string, tds[8].string, tds[9].string)
      bricksList.append(brick)

  return bricksList

def colors_from_lego():
  # Picked from the list of 1x1 and 2x1 colors available from http://shop.lego.com/en-US/Pick-A-Brick-ByTheme,
  # and matching them to the names in the peerson list
  official_colors_ids = [1, 21, 23, 24, 26, 28, 5, 106, 102, 199, 192, 194]

  peerson_colors = colors_from_peerson();
  official_colors = []
  for id in official_colors_ids:
    for brick in peerson_colors:
      if int(brick.id) ==  int(id):
        official_colors.append(brick)
        break

  return official_colors

def get_colors(location):
 if location == 'peerson':
   return colors_from_peerson()
 elif location == 'lego':
  return colors_from_lego()
 else:
   print "Could not find color list for " + location
   return None

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("color_list", help="Where to get the list of colours from. Valid options are: 'lego', 'peerson'", default="peerson")
  args = parser.parse_args()

  bricksList = get_colors(args.color_list)
  if not bricksList:
    print "Color list needed. Aborting"
    return

  # Get the donor image
  path = os.getcwd()
  img_filename = "%s/images/FacebookLondon.png" % path
  im = Image.open(img_filename)
  im.thumbnail((384,384), Image.ANTIALIAS)

  # Go over it pixel by pixel and change the color to the closest match in our bricksList
  imageW = im.size[0]
  imageH = im.size[1]

  pixels = im.load()
  for y in range(0, imageH):
    for x in range(0, imageW):
      rgb = pixels[x,y]

      best_match = find_best_match(rgb, bricksList)
      pixels[x,y] = best_match.get_rgb()

  file_name, ext = os.path.splitext(img_filename)
  im.save(file_name + "_new_colors.png", "PNG")
  

if __name__ == '__main__':
  main()

