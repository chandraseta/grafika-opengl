# Add src to python system path
import sys
sys.path.append('src/')

from svgparser import *
from car import *
from triangle import draw_triangle

if __name__ == '__main__':
    image = parse("data/images/regalia_flat.svg")
    draw(image)