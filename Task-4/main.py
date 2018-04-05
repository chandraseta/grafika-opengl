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
    indices = []

    regalia_vertices, regalia_indices = parseModel("data/models/regalia.obj", False, colors)

    models.append(regalia_vertices)
    indices.append(regalia_indices)
    
    startShowcase(models, indices)