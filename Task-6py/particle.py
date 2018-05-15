import random
import math
import json

from OpenGL.GL import *
from OpenGL.GLUT import *

# Place holder for all particles in the system
# Made this global, as it needs access across
particleList = []

class Particle(object):
    def __init__(self,x,y,vx,vy,color,size,params):
        #super(Particle, self).__init__()
        self.x = x        #Position
        self.y = y
        self.vx = vx        #velocity components
        self.vy = vy
        self.params = params

        self.age= 0
        self.max_age = self.params['maxAge']

        self.wind = 0.1
        self.size = size
        self.color=color
        self.is_dead = False

    def update(self,dx=0.05,dy=0.05):
        self.vx += dx* self.wind
        self.vy += dy*self.wind - self.params['gravity']/100

        self.vx *= 1- self.params['dragFactor']/1000
        self.vy *= 1- self.params['dragFactor']/1000

        self.x += self.vx
        self.y += self.vy
        self.check_particle_age()

    def draw(self):
        glColor4fv(self.color)
        glPushMatrix()
        glTranslatef(self.x,self.y,0)
        glutSolidSphere(self.size,20,20)
        glPopMatrix()
        glutPostRedisplay()

    def check_particle_age(self):
        self.age +=1
        self.is_dead = self.age >= self.max_age

        #Start ageing
        # Achieve a linear color falloff(ramp) based on age.
        self.color[3]= 1.0 - float(self.age)/float(self.max_age)

class ParticleBurst(Particle):
    def __init__(self,x,y,vx,vy,params):
        self.params = params
        color = self.params['launchColor']
        size = self.params['launchSize']
        Particle.__init__(self,x,y,vx,vy,color,size,params)
        self.wind = 1
        self.age = 0

    # Override parent method for Exploder particle
    def check_particle_age(self):
        if self.vy <0:
            self.age += 1

        # Tweaking explode time
        temp = int ( 100*random.random()) + self.params['explosionVariation']

        if self.age > temp:
            self.is_dead = True

class ParticleSystem():
    def __init__(self, x, y, params):
        self.x = params['initPosX']
        self.y = params['initPosY']
        self.timer = 0
        self.params = params
        self.addExploder()

    def addExploder(self):
        speed = self.params['explosionSpeed']
        speed *= (1 - random.uniform(0,self.params['explosionVariation'])/100)
        angle = 270*3.14/180 + round(random.uniform(-0.5,0.5),2)
        vx = speed * math.cos(angle)
        vy = -speed * math.sin(angle)

        f = ParticleBurst(30,10,vx,vy,self.params)
        particleList.append(f)


    def update(self):
        self.timer += 1
        for i in range(len(particleList)):
            print('asd')
            p = particleList[i]
            x = self.params['windX']
            y = self.params['windY']
            p.update(x,y)
            p.check_particle_age()
            if p.is_dead:
                p.color = [0.0,0.0,0.0,0.0]
                particleList.pop(i)
            else:
                p.draw()