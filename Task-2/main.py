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
    images.append(parse("data/images/clouds.svg"))
    images.append(parse("data/images/mountain.svg"))
    images.append(parse("data/images/building_back.svg"))
    images.append(parse("data/images/building_front.svg"))
    images.append(parse("data/images/road.svg"))
    draw(images)