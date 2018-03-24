import ctypes
import numpy
import OpenGL
import pygame
import time

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from pygame.locals import *

width = 1024
height = 768

def getFileContents(filename):
    return open(filename, 'r').read()

def init():
    pygame.init()
    pygame.display.set_mode((width, height), DOUBLEBUF|OPENGL)

    # vertexShader = compileShader(getFileContents("data/shaders/car.vert"), GL_VERTEX_SHADER)
    # fragmentShader = compileShader(getFileContents("data/shaders/car.frag"), GL_FRAGMENT_SHADER)

    # program = glCreateProgram()
    # glAttachShader(program, vertexShader)
    # glAttachShader(program, fragmentShader)
    # glLinkProgram(program)

    # glClearColor(0.0, 0.0, 0.0, 1.0)
    # return program

def wall(image): 
    glBegin(GL_QUADS)
    glTexCoord2f(0,0)
    glVertex3f(-4,-4,-16)
    glTexCoord2f(0,1)
    glVertex3f(-4,4,-16)
    glTexCoord2f(1,1)
    glVertex3f(4,4,-8)
    glTexCoord2f(1,0)
    glVertex3f(4,-4,-8)
    glEnd()

def draw_car():
    # program = init()

    init()

    img = pygame.image.load('data/images/car_sample.png')
    textureData = pygame.image.tostring(img, "RGB", 1)
    img_width = img.get_width()
    img_height = img.get_height()

    img_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, img_texture)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)
    glEnable(GL_TEXTURE_2D)

    aspectRatio = width/height

    running = True
    while running:
        glLoadIdentity()

        # gluPerspective(
        #   fieldOfViewY
        #   aspectRatio
        #   nearField
        #   farField
        # )
        gluPerspective(60, aspectRatio, 0.01, 100.0)
        glTranslatef(0,0,0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        wall(img_texture)

        pygame.display.flip()
        pygame.time.wait(50)

        events = pygame.event.get()

        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    running = False

if __name__ == '__main__':
    draw_car()
