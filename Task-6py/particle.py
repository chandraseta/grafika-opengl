import random
import math
import json

from OpenGL.GL import *
from OpenGL.GLUT import *

# Place holder for all particles in the system
# Made this global, as it needs access across
# particleList = []

class Particle(object):
    def __init__(self,x,y,z,vx,vy,vz,color,size,params, size_updater = None, alpha_updater = None):
        #super(Particle, self).__init__()
        self.x = x        #Position
        self.y = y
        self.z = z
        self.vx = vx        #velocity components
        self.vy = vy
        self.vz = vz
        self.params = params

        self.age = 0
        self.max_age = self.params['maxAge']

        self.wind = 0.1
        self.size = size
        self.color = color
        self.is_dead = False

        self.size_updater = size_updater
        self.alpha_updater = alpha_updater

    def update(self,dx=0.05,dy=0.05, dz=0.05, isDisabled=False):
        if isDisabled:
            self.is_dead = True
            self.size = 0
        else:
            self.vx += dx*self.wind
            self.vy += dy*self.wind - self.params['gravity']/100
            self.vz += dz*self.wind

            self.vx *= 1- self.params['dragFactor']/1000
            self.vy *= 1- self.params['dragFactor']/1000
            self.vz *= 1- self.params['dragFactor']/1000

            self.x += self.vx/100
            self.y += self.vy/100
            self.z += self.vz/100

            if self.size_updater is not None:
                self.size = self.size_updater(self.size, self.age)
            if self.alpha_updater is not None:
                self.color[3] = self.alpha_updater(0.5, self.age)
            # self.size += (0.01 * self.age/400)
            # self.color[3] = 0.5 - 0.5*float(self.age)/float(self.max_age)
            # self.color[3] = 0.5 * math.exp(-0.008 * float(self.age))
        
            self.check_particle_age()

    def draw(self):
        #print ("x: %s Y: %s" %(self.x,self.y))
        glColor4fv(self.color)
        glPushMatrix()
        glTranslatef(self.x,self.y,self.z)
        glutSolidSphere(self.size,10,10)
        glPopMatrix()
        glutPostRedisplay()

    def check_particle_age(self):
        self.age +=1
        self.is_dead = self.age >= self.max_age

        # Start ageing
        # Achieve a linear color falloff(ramp) based on age.
        self.color[3] = 1.0 - float(self.age)/float(self.max_age)

class ParticleBurst(Particle):
    def __init__(self,x,y,z,vx,vy,vz,params, size_updater = None, alpha_updater = None):
        self.params = params
        color = self.params['launchColor']
        size = self.params['launchSize']
        Particle.__init__(self,x,y,z,vx,vy,vz,color,size,params, size_updater, alpha_updater)
        self.wind = 1
        self.age = 0

    # Override parent method for Exploder particle
    def check_particle_age(self):
        self.age += 1
        self.is_dead = self.age >= self.max_age

class ParticleSystem():
    def __init__(self, x, y, params, size_updater = None, alpha_updater = None):
        self.x = params['initPosX']
        self.y = params['initPosY']
        self.maxParticle = params['maxParticle']
        self.count = 0
        self.timer = 0
        self.params = params
        self.particleList = []
        self.size_updater = size_updater
        self.alpha_updater = alpha_updater
        self.addExploder()

    def addExploder(self):
        speed = self.params['explosionSpeed']
        speed *= (1 - random.uniform(0,self.params['explosionVariation'])/100)

        angleVar = self.params['explosionAngleVar']
        baseAngle = self.params['explosionAngle']
        if (angleVar != 0):
            angle = baseAngle * 3.14/180 + round(random.uniform(-angleVar,angleVar)/angleVar * 0.5,2)
            angleZ = baseAngle * 3.14/180 + round(random.uniform(-angleVar,angleVar)/angleVar * 0.5,2)
        else:
            angle = baseAngle * 3.14/180
            angleZ = baseAngle * 3.14/180

        vx = speed * math.cos(angle)
        vy = -speed * math.sin(angle)
        vz = speed * math.cos(angleZ)

        varX = self.params['varX']
        varZ = self.params['varZ']

        startX = self.x + random.uniform(-varX,varX)
        startZ = random.uniform(-varZ,varZ) + self.params['initPosZ']

        f = ParticleBurst(startX,self.y,startZ,vx,vy,vz,self.params, self.size_updater, self.alpha_updater)
        self.particleList.append(f)


    def update(self, isDisabled=False):
        interval = self.params['launchInterval']
        birthRate = self.params['birthRate']
        maxParticle = self.params['maxParticle']

        self.timer += 1
        if self.timer % interval == 0 or self.timer < 2:
            for n in range(birthRate):
                if(len(self.particleList) < maxParticle):
                    self.addExploder()

        for p in self.particleList:
            i = self.particleList.index(p)
            x = self.params['windX']
            y = self.params['windY']
            z = self.params['windZ']
            p.update(x,y,z, isDisabled)
            p.check_particle_age()
            if p.is_dead:
                p.color = [0.0,0.0,0.0,0.0]
                self.particleList.pop(i)
            else:
                p.draw()
                #print('drawing sphere',i,' at ',p.age,' ',p.y)