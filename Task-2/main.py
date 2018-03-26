# Add src to python system path
import sys
sys.path.append('src/')

from svgparser import *
from car import *
from triangle import draw_triangle

if __name__ == '__main__':
    images = []
    images.append(parse("data/images/regalia_flat.svg"))
    images.append(parse("data/images/regalia_flat.svg"))
    draw(images)