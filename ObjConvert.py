#workaround installing packages
#import pip
#pip.main(['install','pywavefront'])
#pip.main(['install','pyglet'])
#pip.main(['install','tensorflow'])
#pip.main(['install','tensorflow_io'])
#pip.main(['install','vedo'])

# imports
import pywavefront
#from pywavefront import visualization
#import pyglet
#import tensorflow as tf
from vedo import *
#from tensorflow_io.python.ops import core_ops
import re
import random

coordinates_group = []
coordinates = []

with open('00013739.obj') as f:
    lines = f.readlines()
    vertices = []
    faces = []


for line in lines:
    if line.startswith('v '):
        vertices.append(line)
        coordinates.append(line.replace('v ', ''))
    elif line.startswith('f '):
        faces.append(line)
    else:
        continue





with open("decoded_object.txt", "w") as o:
    for element in vertices:
        o.write(element)
    for element in faces:
        o.write(element)

with open("coordinates.txt", "w") as c:
    for element in coordinates:
        c.write(element)



# .obj as Mesh
test_object = Mesh("00013739.obj")


# .obj as Wavefront
test_object2 = pywavefront.Wavefront('00013739.obj')


def distort_coords(coords):
    help_list = []
    for i in coords:
        help_list.append(i.split(' '))
        for list in help_list:
            for count,number in enumerate(list,start=1):
                if count == 1:
                    coordinates_group.append('v ')
                number = float(number) / random.uniform(1.0,1.00001) #distort the vertices
                if str(number) == '0.0':
                    number = '0.00000000' #zero numbers format correction
                else:
                    number = str(number)[:10] #cut to 10 places
                coordinates_group.append(str(number))
                coordinates_group.append(' ')
                if count % 3 == 0 and count != 0: #break after every three iterations
                    coordinates_group.append("\n")
    with open("distorted coordinates.obj", "w") as dc:
        for element in coordinates_group:
            dc.write(str(element))
        for element in faces:
            dc.write(element)
    #.txt file to check coordinates
    with open("distorted coordinates.txt", "w") as dc:
        for element in coordinates_group:
            dc.write(str(element))
        for element in faces:
            dc.write(element)


distort_coords(coordinates)


distorted = Mesh("distorted coordinates.obj")
distorted.show()


#test_object.show()

#decode_obj(test_obejct)




#OLDER
'''
#window = pyglet.window.Window()

#visualization.draw(test_obejct)


# function idea 1
def decode_obj(contents, name=None):
    """
    Decode a Wavefront (obj) file into a float32 tensor.
    Args:
      contents: A 0-dimensional Tensor of type string, i.e the
        content of the Wavefront (.obj) file.
      name: A name for the operation (optional).
    Returns:
      A `Tensor` of type `float32` and shape of `[n, 3]` for vertices.
    """
    return core_ops.io_decode_obj(contents, name=name)


# function idea 2
def convert_obj(file):
    reComp = re.compile("(?<=^)(v |vn |vt |f )(.*)(?=$)", re.MULTILINE)
    with open(file) as f:
        data = [txt.group() for txt in reComp.finditer(f.read())]

    v_arr, vn_arr, vt_arr, f_arr = [], [], [], []
    for line in data:
        tokens = line.split(' ')
        if tokens[0] == 'v':
            v_arr.append([float(c) for c in tokens[1:]])
        elif tokens[0] == 'vn':
            vn_arr.append([float(c) for c in tokens[1:]])
        elif tokens[0] == 'vt':
            vn_arr.append([float(c) for c in tokens[1:]])
        elif tokens[0] == 'f':
            f_arr.append([[int(i) if len(i) else 0 for i in c.split('/')] for c in tokens[1:]])

    vertices, normals = [], []
    for face in f_arr:
        for tp in face:
            vertices += v_arr[tp[0] - 1]
            normals += vn_arr[tp[2] - 1]
    # just printing results to see if it works
    print(vertices) '''
