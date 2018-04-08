# Add src to python system path
import sys
sys.path.append('src/')

from car3D import startShowcase
from obj import ObjModel
from objparser import parseModel

from pygame import mixer

if __name__ == '__main__':

    # pygame.mixer.init()
    # pygame.mixer.music.load("data/sounds/car-customization.mp3")
    # pygame.mixer.music.play(-1, 0.0)

    car = ObjModel('data/models/regalia.obj')
    startShowcase(car)