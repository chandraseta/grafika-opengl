import numpy
import mesh
import model

def parseModel(filename):
    model = model.Model()
    mesh_cnt = 0

    file = open(filename,"r")
    lines = file.readlines()

    index = []
    vertex = []
    normal = []
    texture = []
    finalizing = False
    for line in lines:
        line_split = line.rstrip("\n").split(" ")
        if (len(line_split) > 0):
            if (line_split[0] == 'o'):       
                # New Mesh
                mesh_cnt += 1
            elif (line_split[0] == 'v'):
                vertex.append([float(line_split[1])/200,float(line_split[2])/200,float(line_split[3])/200])
            elif (line_split[0] == 'vn'):
                normal.append([float(line_split[1]),float(line_split[2]),float(line_split[3])])
            elif (line_split[0] == 'vt'):
                texture.append([float(line_split[1]),float(line_split[2])])
            elif (line_split[0] == 'f'):
                finalizing = True
                index.append([line_split[1],line_split[2],line_split[3]])
            elif(finalizing):
                buffer, index_buffer = processArray(index,vertex,normal,texture)    
                index = []
                vertex = []
                normal = []
                texture = []
                finalizing = False

                new_mesh = mesh.Mesh(buffer, index_buffer)
                model.addMesh(new_mesh)

    return model

def processArray(index, vertex, normal, texture):
    buffer = []
    index_buffer = []
    for faces in index:
        ebo_index = []
        for point in faces:
            indexes = point.split("/")
            buffer += vertex[int(indexes[0])-1]
            buffer += texture[int(indexes[1])-1]
            buffer += normal[int(indexes[2])-1]
            ebo_index.append(float(indexes[0]))
        index_buffer.append(ebo_index)
    return buffer, index_buffer

if __name__ == '__main__':
    parseModel("../data/models/box.obj")