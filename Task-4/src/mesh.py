import glm

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

        for idx in range(0, len(buffer), 8):
            position = glm.vec3(buffer[idx], buffer[idx + 1], buffer[idx + 2])

            # TODO: Check if the mesh has empty texture coordinate
            texture = glm.vec2(buffer[idx + 3], buffer[idx + 4])

            normal = glm.vec3(buffer[idx + 5], buffer[idx + 6], buffer[idx + 7])

            v = Vertex(position, texture, normal)
            self._vertices.append(v)
        
        self._indices = index_buffer

        