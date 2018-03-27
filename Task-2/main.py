# Add src to python system path
import sys
sys.path.append('src/')

from svgparser import *
from car import *
from triangle import draw_triangle

from pygame import mixer

if __name__ == '__main__':

    pygame.mixer.init()
    pygame.mixer.music.load("data/sounds/stand-by-me.mp3")
    pygame.mixer.music.play(-1, 0.0)

    images = []

    # Back to Front
    images.append(parse("data/images/clouds.svg"))
    images.append(parse("data/images/mountain.svg"))
    images.append(parse("data/images/building_back.svg"))
    images.append(parse("data/images/building_front.svg"))
    images.append(parse("data/images/road.svg"))
    images.append(parse("data/images/regalia_flat.svg"))
    draw(images)