# Add src to python system path
import sys
sys.path.append('src/')

from svgparser import *
from car import *

if __name__ == '__main__':
    image = parse("data/images/triangle.svg")
    draw(image)