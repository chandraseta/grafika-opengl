import random
import math
import json

from OpenGL.GL import *
from OpenGL.GLUT import *

# Place holder for all particles in the system
# Made this global, as it needs access across
particleList = []

class Particle(object):
    def __init__(self,x,y,z,vx,vy,vz,color,size,params):
        #super(Particle, self).__init__()
        self.x = x        #Position
        self.y = y
        self.z = z
        self.vx = vx        #velocity components
        self.vy = vy
        self.vz = vz
        self.params = params

        self.age= 0
        self.max_age = self.params['maxAge']

        self.wind = 0.1
        self.size = size
        self.color=color
        self.is_dead = False

    def update(self,dx=0.05,dy=0.05, dz=0.05):
        self.vx += dx*self.wind
        self.vy += dy*self.wind - self.params['gravity']/100
        self.vz += dz*self.wind

        self.vx *= 1- self.params['dragFactor']/1000
        self.vy *= 1- self.params['dragFactor']/1000
        self.vz *= 1- self.params['dragFactor']/1000

        self.x += self.vx/100
        self.y += self.vy/100
        self.z += self.vz/100
        self.check_particle_age()

    def draw(self):
        #print ("x: %s Y: %s" %(self.x,self.y))
        glColor4fv(self.color)
        glPushMatrix()
        glTranslatef(self.x,self.y,self.z)
        glutSolidSphere(self.size,20,20)
        glPopMatrix()
        glutPostRedisplay()

    def check_particle_age(self):
        self.age +=1
        self.is_dead = self.age >= self.max_age

        # Start ageing
        # Achieve a linear color falloff(ramp) based on age.
        self.color[3]= 1.0 - float(self.age)/float(self.max_age)

class ParticleBurst(Particle):
    def __init__(self,x,y,z,vx,vy,vz,params):
        self.params = params
        color = self.params['launchColor']
        size = self.params['launchSize']
        Particle.__init__(self,x,y,z,vx,vy,vz,color,size,params)
        self.wind = 1
        self.age = 0

    # Override parent method for Exploder particle
    def check_particle_age(self):
        self.age += 1
        self.is_dead = self.age >= self.max_age

class ParticleSystem():
    def __init__(self, x, y, params):
        self.x = params['initPosX']
        self.y = params['initPosY']
        self.maxParticle = params['maxParticle']
        self.count = 0
        self.timer = 0
        self.params = params
        self.addExploder()

    def addExploder(self):
        speed = self.params['explosionSpeed']
        speed *= (1 - random.uniform(0,self.params['explosionVariation'])/100)

        angleVar = self.params['explosionAngleVar']
        if(angleVar != 0):
            angle = 270*3.14/180 + round(random.uniform(-angleVar,angleVar)/angleVar * 0.5,2)
            angleZ = 270*3.14/180 + round(random.uniform(-angleVar,angleVar)/angleVar * 0.5,2)
        else:
            angle = -90*3.14/180
            angleZ = -90*3.14/180

        vx = speed * math.cos(angle)
        vy = -speed * math.sin(angle)
        vz = speed * math.cos(angleZ)

        varX = self.params['varX']
        varZ = self.params['varZ']

        startX = self.x + random.uniform(-varX,varX)
        startZ = random.uniform(-varZ,varZ)

        f = ParticleBurst(startX,self.y,startZ,vx,vy,vz,self.params)
        particleList.append(f)


    def update(self):
        interval = self.params['launchInterval']
        birthRate = self.params['birthRate']
        maxParticle = self.params['maxParticle']

        self.timer += 1
        print(interval)
        if self.timer % interval == 0 or self.timer < 2:
            for n in range(birthRate):
                if(len(particleList) < maxParticle):
                    self.addExploder()

        for p in particleList:
            i = particleList.index(p)
            x = self.params['windX']
            y = self.params['windY']
            z = self.params['windZ']
            p.update(x,y,z)
            p.check_particle_age()
            if p.is_dead:
                p.color = [0.0,0.0,0.0,0.0]
                particleList.pop(i)
            else:
                p.draw()
                #print('drawing sphere',i,' at ',p.age,' ',p.y)