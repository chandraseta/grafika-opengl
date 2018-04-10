import glm
import numpy
import shader
from OpenGL.GL import *
from OpenGL.GL.shaders import *
class Vertex(object):
    def __init__(self, position, texture_coordinate, normal):
        self._position = position
        self._texture_coordinate = texture_coordinate
        self._normal = normal

class Texture(object):
    def __init__(self, id, texture_type, path):
        self._id = id
        self._type = texture_type
        self._path = path

class Mesh(object):
    def __init__(self, buffer, index_buffer):
        self._vertices = []
        self._indices = []
        self._textures = []
        self._buffer = buffer
        self._VAO = glGenVertexArrays(1)
        self._VBO = glGenBuffers(1)
        self._EBO = glGenBuffers(1)
        for idx in range(0, len(buffer), 8):
            #position = glm.vec3(buffer[idx], buffer[idx + 1], buffer[idx + 2])

            # TODO: Check if the mesh has empty texture coordinate
            texture = glm.vec2(buffer[idx + 3], buffer[idx + 4])

            normal = glm.vec3(buffer[idx + 5], buffer[idx + 6], buffer[idx + 7])

            #self._vertices.append(v)
        
        self._indices = index_buffer
        self.setupMesh()

        # TODO: Find out how to fill self._textures

    def setupMesh(self):
        vertices = numpy.asarray(self._buffer, numpy.float32)
        indices = numpy.asarray(self._indices)
        textures = numpy.asarray(self._textures, numpy.float32)
        glBindVertexArray(self._VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self._VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)
        
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)


    def draw(self):
        diffuseNr = 1
        specularNr = 1
        normalNr = 1
        heightNr = 1
        glDrawElements(GL_TRIANGLES, len(self._indices), GL_UNSIGNED_INT, 0)