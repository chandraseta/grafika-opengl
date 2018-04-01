import numpy

def parseModel(filename, colors):
    model = []
    parts = []
    file = open(filename,"r")
    lines = file.readlines()
    clr = 0
    current_model = -1
    model_count = 0
    for line in lines:
        coords = line.rstrip("\n").split(" ")

        if (len(coords) == 4):
            if (coords[0] == 'v'):
                if (current_model != model_count):
                    current_model += 1
                    if (len(parts) > 0):
                        model.append(parts)
                    parts = []
                    parts.append(convertColor(colors[clr]))
                    clr += 1
                coords_temp = []
                for id, val in enumerate(coords):
                    if (id > 0):
                        coords_temp.append(float(val)/200)
                parts.append(coords_temp)
            else:
                model_count += 1
    model.append(parts)
    return model

def convertColor(color):
    hexcolor = []
    hexcolor.append(int(color[1:3],16)/255)
    hexcolor.append(int(color[3:5],16)/255)
    hexcolor.append(int(color[5:7],16)/255)
    return hexcolor

if __name__ == '__main__':
    image = parse("../data/models/regalia.obj")