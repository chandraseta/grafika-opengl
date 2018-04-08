import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import obj

class Cube(object):
    left_key = False
    right_key = False
    up_key = False
    down_key = False
    angle = 0
    cube_angle = 0
    #-------------------------------------
    def __init__(self):
        self.vertices = []
        self.faces = []
        # self.rubik_id = obj.load_texture("rubik.png")
        # self.surface_id = obj.load_texture("ConcreteTriangles.png")
        #---Coordinates----[x,y,z]-----------------------------
        self.coordinates = [0,0,0]
        # self.ground = obj.ObjLoader("plane.txt")
        # self.pyramid = obj.ObjLoader("scene.txt")
        self.cube = obj.ObjLoader("../data/models/r8.obj")
        #self.monkey = obj.ObjLoader("monkey.txt")

    def render_scene(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #glClearColor(0.7,0.9,1,1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        #Add ambient light:
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT,[0.2,0.2,0.2,1.0])
        
        #Add positioned light:
        glLightfv(GL_LIGHT0,GL_DIFFUSE,[2,2,2,1])
        glLightfv(GL_LIGHT0,GL_POSITION,[4,8,1,1])
        
        glTranslatef(0,-0.5,0)   

        gluLookAt(0,0,0, math.sin(math.radians(self.angle)),0,math.cos(math.radians(self.angle)) *-1, 0,1,0)

        glTranslatef(self.coordinates[0],self.coordinates[1],self.coordinates[2])
        
        # self.ground.render_texture(self.surface_id,((0,0),(2,0),(2,2),(0,2)))
        # self.pyramid.render_scene()
        
        glTranslatef(-7.5,2,0)
        glRotatef(self.cube_angle,0,1,0)
        glRotatef(45,1,0,0)
        # self.cube.render_texture(self.rubik_id,((0,0),(1,0),(1,1),(0,1)))
        
        #self.monkey.render_scene()
            
    def move_forward(self):
        self.coordinates[2] += 0.1 * math.cos(math.radians(self.angle))
        self.coordinates[0] -= 0.1 * math.sin(math.radians(self.angle))
        
    def move_back(self):
        self.coordinates[2] -= 0.1 * math.cos(math.radians(self.angle))
        self.coordinates[0] += 0.1 * math.sin(math.radians(self.angle))
            
    def move_left(self):
        self.coordinates[0] += 0.1 * math.cos(math.radians(self.angle))
        self.coordinates[2] += 0.1 * math.sin(math.radians(self.angle))
        
    def move_right(self):
        self.coordinates[0] -= 0.1 * math.cos(math.radians(self.angle))
        self.coordinates[2] -= 0.1 * math.sin(math.radians(self.angle))
        
    def rotate(self,n):
        if self.angle >= 360 or self.angle <= -360:
            self.angle = 0
        self.angle += n
            
    def update(self):
        if self.left_key:
            self.move_left()
        elif self.right_key:
            self.move_right()
        elif self.up_key:
            self.move_forward()
        elif self.down_key:
            self.move_back()
            
        pos = pygame.mouse.get_pos()
        if pos[0] < 75:
            self.rotate(-1.2)
        elif pos[0] > 565:
            self.rotate(1.2)
        
        if self.cube_angle >= 360:
            self.cube_angle = 0
        else:
            self.cube_angle += 0.5
    
    def keyup(self):
        self.left_key = False
        self.right_key = False
        self.up_key = False
        self.down_key = False
    
    def delete_texture(self):
        glDeleteTextures(self.rubik_id)
        glDeleteTextures(self.surface_id)
    
def main():
    pygame.init()
    pygame.display.set_mode((640,480),pygame.DOUBLEBUF|pygame.OPENGL)
    pygame.display.set_caption("PyOpenGL Tutorial")
    clock = pygame.time.Clock()
    done = False
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45,640.0/480.0,0.1,200.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

    #----------- Main Program Loop -------------------------------------
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
        
        cube.update()
        cube.render_scene()
        
        pygame.display.flip()
        clock.tick(30)
    
    # cube.delete_texture()
    pygame.quit()

if __name__ == '__main__':
	main()