# Add src to python system path
import sys
sys.path.append('src/')

from car3D import startShowcase
from objparser import parseModel
import pygame
import time
import ctypes
import sys
import numpy  

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from pygame.locals import *  

from pygame import mixer

def getFileContents(filename):
    return open(filename, 'r').read()

if __name__ == '__main__':

    # pygame.mixer.init()
    # pygame.mixer.music.load("data/sounds/car-customization.mp3")
    # pygame.mixer.music.play(-1, 0.0)
    pygame.init()
    pygame.display.set_mode((640, 480), HWSURFACE|OPENGL|DOUBLEBUF)
    
    vertexShader = compileShader(getFileContents("data/shaders/triangle.vert"), GL_VERTEX_SHADER)
    fragmentShader = compileShader(getFileContents("data/shaders/triangle.frag"), GL_FRAGMENT_SHADER)
    program = glCreateProgram()
    glAttachShader(program, vertexShader)
    glAttachShader(program, fragmentShader)
    glLinkProgram(program)
    glClearColor(0.3, 0.3, 0.3, 1.0)

    models = parseModel("data/models/square.obj")
    startShowcase(program, models)