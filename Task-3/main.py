# Add src to python system path
import sys
sys.path.append('src/')

from car import *
from car3D import startShowcase
from objparser import parseModel
from svgparser import parseImage

from pygame import mixer

if __name__ == '__main__':

    # pygame.mixer.init()
    # pygame.mixer.music.load("data/sounds/car-customization.mp3")
    # pygame.mixer.music.play(-1, 0.0)

    colors = ["#333333"]

    models = []
    models.append(parseModel("data/models/regalia.obj", colors))


    startShowcase(models)