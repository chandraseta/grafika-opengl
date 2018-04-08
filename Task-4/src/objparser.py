import numpy

def parseModel(filename, isColored, colors):
    vertices = []
    v_parts = []
    indices = []
    f_parts = []

    file = open(filename,"r")
    lines = file.readlines()
    clrID = 0
    v_current = -1
    f_current = -1
    v_set_count = 0
    f_set_count = 0
    v_begin = False
    for line in lines:
        line_split = line.rstrip("\n").split(" ")

        if (len(line_split) > 0):
            if (line_split[0] == 'o' or line_split[0] == 'g'):
                v_set_count += 1
                f_set_count += 1

        if (len(line_split) == 4):
            if (line_split[0] == 'v'):
                if (v_current != v_set_count):
                    v_current += 1
                    if (len(v_parts) > 0):
                        vertices.append(v_parts)
                    v_parts = []
                    v_parts.append(convertColor(colors[clrID]))
                    if isColored:
                        clr += 1
                v_split_temp = []
                for id, val in enumerate(line_split):
                    if (id > 0):
                        v_split_temp.append(float(val)/200)
                v_parts.append(v_split_temp)
            elif (line_split[0] == 'f'):
                if (f_current != f_set_count):
                    f_current += 1
                    if (len(f_parts) > 0):
                        indices.append(f_parts)
                    f_parts = []
                f_split_temp = []
                for id, val in enumerate(line_split):
                    if (id > 0):
                        index = line_split[id].split("/")
                        f_split_temp.append(int(index[0]) - 1)
                f_parts.append(f_split_temp)

    vertices.append(v_parts)
    indices.append(f_parts)

    return vertices, indices

def convertColor(color):
    hexcolor = []
    hexcolor.append(int(color[1:3],16)/255)
    hexcolor.append(int(color[3:5],16)/255)
    hexcolor.append(int(color[5:7],16)/255)
    return hexcolor

if __name__ == '__main__':
    image = parse("../data/models/regalia.obj")