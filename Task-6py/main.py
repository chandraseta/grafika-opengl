# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import sys, pygame, json, math
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# IMPORT OBJECT LOADER
from objloader import *
from particle import *

class Main:
    rx, ry = (0,0)
    tx, ty = (3,0)
    downX = 0
    downY = 0
    zpos = 5
    rotate = move = False
    leftButton = False
    middleButton = False
    rightButton = False
    sdepth = 10
    
    frame=0
    time=0
    timebase=0

    def __init__(self):
        viewport = (800,600)
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(800,600)
        glutCreateWindow(b"OpenXV")
        glClearColor(0.3,0.3,0.3,1.0)
        hx = viewport[0]/2
        hy = viewport[1]/2

        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

        glutDisplayFunc(self.display)
        glutMouseFunc(self.mouseCallback)
        glutMotionFunc(self.motionCallback)

        # most obj files expect to be smooth-shaded
        # LOAD OBJECT AFTER PYGAME INIT
        self.obj = OBJ('data/models/DB10.obj', swapyz=False)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        width, height = viewport

        gluPerspective(90.0, width/float(height), 1, 100.0)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_MODELVIEW)
        glShadeModel(GL_SMOOTH)
        glCullFace(GL_FRONT)
        
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

        mat_specular = [1.0, 0.0, 0.0, 0.0]
        mat_diffuse = [0.9, 0.0, 0.0, 0.0]
        mat_shininess = [50.0]
        light_position = [5.0, 5.0, 5.0, 1.0]
        white_light = [1.0, 1.0, 1.0, 1.0]
        lmodel_ambient = [0.1, 0.5, 0.1, 1.0]

        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)

        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, white_light)
        glLightfv(GL_LIGHT0, GL_SPECULAR,white_light)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT,lmodel_ambient)


        # Load params from file
        smoke_left = json.load(open('config/smoke_left_config.json'))
        smoke_right = json.load(open('config/smoke_right_config.json'))
        def update_smoke_size(size, age):
            return size + (0.01 * float(age)/400)
        def update_smoke_alpha(init_alpha, age):
            return init_alpha * math.exp(-0.04 * float(age))
        self.smoke_l = ParticleSystem(0, 0, smoke_left, size_updater=update_smoke_size, alpha_updater=update_smoke_alpha)
        self.smoke_r = ParticleSystem(0, 0, smoke_right, size_updater=update_smoke_size, alpha_updater=update_smoke_alpha)
        
        rain_params = json.load(open('config/rain_config.json'))
        self.rain = ParticleSystem(0,0, rain_params)

        glutMainLoop()

    def display(self):
        self.frame += 1
        self.time = glutGet(GLUT_ELAPSED_TIME)
        if (self.time - self.timebase > 1000):
            print("FPS: "+str(self.frame*1000.0/(self.time-self.timebase)))
            self.timebase = self.time
            self.frame = 0
    
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # RENDER OBJECT
        glTranslate(self.tx/20., self.ty/20., - self.zpos)
        glRotate(self.ry, 1, 0, 0)
        glRotate(self.rx, 0, 1, 0)
        glCallList(self.obj.gl_list)
        self.smoke_l.update()
        self.smoke_r.update()
        self.rain.update()

        glutSwapBuffers()
        glutPostRedisplay()

    def mouseCallback(self, button, state, x, y):
        self.downX= x
        self.downY= y
        self.leftButton = ((button == GLUT_LEFT_BUTTON) and (state == GLUT_DOWN))
        self.middleButton = ((button == GLUT_MIDDLE_BUTTON) and (state == GLUT_DOWN))
        self.rightButton = ((button == GLUT_RIGHT_BUTTON) and (state == GLUT_DOWN))
        glutPostRedisplay()

    def motionCallback(self, x, y):
        if (self.leftButton):
            self.rx += float(x - self.downX) / 10.0
            self.ry -= float(self.downY - y) / 10.0
        if (self.middleButton):
            self.zpos -= float(self.downY - y) / 10.0
        if (self.rightButton):
            self.tx += float(x - self.downX) / 6.0
            self.ty += float(self.downY - y) / 6.0
        self.downX = x
        self.downY = y
        glutPostRedisplay()

if __name__ == "__main__":
    main_prog = Main()  