import numpy
def parse(filename):
    image = []
    part = []
    file = open(filename,"r")
    lines = file.readlines()
    for line in lines:
        coord = line.rstrip("\n").split(",")
        if(len(coord) == 1):
            if(len(part) != 0):
                image.append(part)
            part = []
            part.append(convertColor(coord[0]))
        else:
            coord_temp = []
            j = 0
            for val in coord:
                if(j == 0):
                    coord_temp.append(float(val)/100)
                else:
                    coord_temp.append(float(val)*-1/100)
                j = j+1
            coord_temp.append(0)
            part.append(coord_temp)
    image.append(part)
    return image

def convertColor(color):
    hexcolor = []
    hexcolor.append(int(color[1:3],16)/255)
    hexcolor.append(int(color[3:5],16)/255)
    hexcolor.append(int(color[5:7],16)/255)
    return hexcolor

if __name__ == '__main__':
    image = parse("../data/images/regalia_flat.svg")