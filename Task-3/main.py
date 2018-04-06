# Add src to python system path
import sys
sys.path.append('src/')

from car3D import startShowcase
from objparser import parseModel

from pygame import mixer

if __name__ == '__main__':

    colors = ["#333333"]

    models = []
    indices = []

    regalia_vertices, regalia_indices = parseModel("data/models/regalia.obj", False, colors)

    models.append(regalia_vertices)
    indices.append(regalia_indices)
    
    startShowcase(models, indices)