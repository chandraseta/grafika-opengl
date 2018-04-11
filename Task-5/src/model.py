import mesh

class Model(object):
    def __init__(self)
        self._textures_loaded = []
        self._meshes = []
        
    def addMesh(self, new_mesh):
        self._meshes.append(new_mesh)

    def draw(self, shader):
        for mesh in self._meshes:
            mesh.draw(shader)