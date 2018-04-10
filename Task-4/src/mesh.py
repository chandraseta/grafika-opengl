import glm
import shader

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
        self._VAO = glGenVertexArrays(1)
        self._VBO = glGenBuffers(1)
        self._EBO = glGenBuffers(1)

        for idx in range(0, len(buffer), 8):
            position = glm.vec3(buffer[idx], buffer[idx + 1], buffer[idx + 2])

            # TODO: Check if the mesh has empty texture coordinate
            texture = glm.vec2(buffer[idx + 3], buffer[idx + 4])

            normal = glm.vec3(buffer[idx + 5], buffer[idx + 6], buffer[idx + 7])

            v = Vertex(position, texture, normal)
            self._vertices.append(v)
        
        self._indices = index_buffer

        # TODO: Find out how to fill self._textures

        setupMesh(self)

    def __init__(self, vertices, indices, textures):
        self._vertices = vertices
        self._indices = indices
        self._textures = textures
        self._VAO = glGenVertexArrays(1)
        self._VBO = glGenBuffers(1)
        self._EBO = glGenBuffers(1)

        setupMesh(self)  

    def setupMesh():
        vertices = numpy.asarray(self._vertices, numpy.float32)
        indices = numpy.asarray(self._indices)
        textures = numpy.asarray(self._textures, numpy.float32)

        glBindVertexArray(self._VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self._VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)
        
        glEnableVertexAttribArray(0)

        # glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex), (void*)0);
        # // vertex normals
        # glEnableVertexAttribArray(1);	
        # glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex), (void*)offsetof(Vertex, Normal));
        # // vertex texture coords
        # glEnableVertexAttribArray(2);	
        # glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, sizeof(Vertex), (void*)offsetof(Vertex, TexCoords));
        # // vertex tangent
        # glEnableVertexAttribArray(3);
        # glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex), (void*)offsetof(Vertex, Tangent));
        # // vertex bitangent
        # glEnableVertexAttribArray(4);
        # glVertexAttribPointer(4, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex), (void*)offsetof(Vertex, Bitangent));

        # glBindVertexArray(0);

        # TODO: Convert the above lines to python

    def draw(shader):
        diffuseNr = 1
        specularNr = 1
        normalNr = 1
        heightNr = 1

        for idx, texture in enumerate(self._textures):
            glActiveTexture(GL_TEXTURE0 + idx)