"""
author: Eddy Verlinden, Genk Belgium
licence : MIT
"""

import math
import sys
from PySide import QtGui, QtCore
import Part


def horizontal_regular_polygon_vertexes(sidescount,radius,z, startangle = 0):

    vertexes = []
    if radius != 0 :
        for i in range(0,sidescount+1):
            angle = 2 * math.pi * i / sidescount + math.pi + startangle
            vertex = (radius * math.cos(angle), radius * math.sin(angle), z)
            vertexes.append(vertex)
    else:
        vertex = (0,0,z)
        vertexes.append(vertex)

    return vertexes


def build_tetrahedron (radius):
        #R = z / 4 * sqrt(6)
        #ro = z / 12 * sqrt(6)    -->   ro = R / 3
        #z = 4 * R / sqrt(6)
        #h = z / 3 * sqrt(6) = 4 * R / sqrt(6) /3 * sqrt(6) = 4 * R / 3  = ro + R =
        #radius at level = z / 2 / cos(30) = (4 * R / sqrt(6)) / 2 / sqrt(3) * 2 = 4 * R / (sqrt(6) * sqrt(3))= 4 * R / (3 * sqrt(2)


        faces = []
        vertexes_bottom = horizontal_regular_polygon_vertexes(3,4*radius/3/math.sqrt(2),- radius / 3)
        vertexes_top    = horizontal_regular_polygon_vertexes(1,0,radius)

        for i in range(3):
            vertexes_side=[vertexes_bottom[i],vertexes_bottom[i+1],vertexes_top[0],vertexes_bottom[i]]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))

        polygon_bottom=Part.makePolygon(vertexes_bottom)
        faces.append(Part.Face(polygon_bottom))

        shell = Part.makeShell(faces)
        solid = Part.makeSolid(shell)
        obj=App.ActiveDocument.addObject("Part::Feature","tetrahedron")
        obj.Shape = solid


def build_hexahedron(radius):
		side = radius * 2 / math.sqrt(3)
		App.ActiveDocument.addObject("Part::Box","Box")
		App.ActiveDocument.ActiveObject.Label = "Hexahedron"
		App.ActiveDocument.recompute()
		App.ActiveDocument.getObject("Box").Length = side
		App.ActiveDocument.getObject("Box").Width = side
		App.ActiveDocument.getObject("Box").Height = side
		App.ActiveDocument.getObject("Box").Placement = App.Placement(App.Vector(-side/2,-side/2,-side/2),App.Rotation(App.Vector(0,0,1),0))


def build_octahedron (radius):   # Z = R * sqrt(2)
        faces = []
        vertexes_middle = horizontal_regular_polygon_vertexes(4,radius,0)
        vertexes_bottom = horizontal_regular_polygon_vertexes(1,0,-radius)
        vertexes_top    = horizontal_regular_polygon_vertexes(1,0,radius)

        for i in range(4):
            vertexes_side=[vertexes_middle[i],vertexes_middle[i+1],vertexes_top[0],vertexes_middle[i]]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))

        for i in range(4):
            vertexes_side=[vertexes_middle[i],vertexes_middle[i+1],vertexes_bottom[0],vertexes_middle[i]]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))

        shell = Part.makeShell(faces)
        solid = Part.makeSolid(shell)
        obj=App.ActiveDocument.addObject("Part::Feature","Octahedron")
        obj.Shape = solid


def build_dodecahedron (radius):

        angleribs = 121.717474411
        anglefaces = 116.565051177

        faces = []
        z = 4 * radius /  (math.sqrt(3) * ( 1 + math.sqrt(5)))
        r = z/2 * math.sqrt((25 + (11 * math.sqrt(5)))/10)
        # int sphere r is height / 2

        h2 = z * math.sin(angleribs/180 * math.pi)

        #height of the side-tips
        radius1 = z / 2 / math.sin(36 * math.pi / 180)
        h5h = (radius1 + radius1 * math.cos(36 * math.pi / 180))   * math.sin(anglefaces * math.pi / 180) #height of the tops

        radius2 = radius1 - z * math.cos(angleribs * math.pi / 180 )

        r=(h2 + h5h)/2  # XXX to make it fit!




        vertexes_bottom = horizontal_regular_polygon_vertexes(5,radius1,-r)
        vertexes_low = horizontal_regular_polygon_vertexes(5,radius2, -r + h2)
        vertexes_high = horizontal_regular_polygon_vertexes(5,radius2, -r + h5h,  math.pi/5)
        vertexes_top = horizontal_regular_polygon_vertexes(5,radius1, r, math.pi/5)

        polygon_bottom = Part.makePolygon(vertexes_bottom)
        face_bottom = Part.Face(polygon_bottom)
        faces.append(face_bottom)

        polygon_top = Part.makePolygon(vertexes_top)
        face_top = Part.Face(polygon_top)
        faces.append(face_top)

        for i in range(5):
            vertexes_side=[vertexes_bottom[i],vertexes_bottom[i+1],vertexes_low[i+1],vertexes_high[i],vertexes_low[i], vertexes_bottom[i] ]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))

        for i in range(5):
            #vertexes_side=[vertexes_top[i],vertexes_top[i+1],vertexes_high[i+1],vertexes_high2[i], vertexes_high[i],vertexes_top[i] ]
            vertexes_side=[vertexes_top[i],vertexes_top[i+1],vertexes_high[i+1],vertexes_low[i+1],vertexes_high[i],vertexes_top[i] ]
            polygon_side=Part.makePolygon(vertexes_side)
            faces.append(Part.Face(polygon_side))

        shell = Part.makeShell(faces)
        solid = Part.makeSolid(shell)
        obj=App.ActiveDocument.addObject("Part::Feature","Dodecahedron")
        obj.Shape = solid



def build_icosahedron(radius):

    z = 4*radius / math.sqrt(10 + 2 * math.sqrt(5))
    anglefaces = 138.189685104
    r = z/12 * math.sqrt(3) * (3 + math.sqrt(5))


    #radius of a pentagram with the same side
    radius2 = z / math.sin(36 * math.pi/180)/2
    #height of radius2 in the sphere

    angle = math.acos(radius2/radius)
    height = radius * math.sin(angle)

    faces = []

    vertex_bottom = (0,0,-radius)
    vertexes_low = horizontal_regular_polygon_vertexes(5,radius2, -height)
    vertexes_high = horizontal_regular_polygon_vertexes(5,radius2, height, math.pi/5)
    vertex_top = (0,0,radius)


    for i in range(5):
        vertexes_side=[vertex_bottom,vertexes_low[i],vertexes_low[i+1], vertex_bottom]
        polygon_side=Part.makePolygon(vertexes_side)
        faces.append(Part.Face(polygon_side))

    for i in range(5):
        vertexes_side=[vertexes_low[i],vertexes_low[i+1],vertexes_high[i],vertexes_low[i] ]
        polygon_side=Part.makePolygon(vertexes_side)
        faces.append(Part.Face(polygon_side))
        vertexes_side=[vertexes_high[i],vertexes_high[i+1],vertexes_low[i+1],vertexes_high[i] ]
        polygon_side=Part.makePolygon(vertexes_side)
        faces.append(Part.Face(polygon_side))

    for i in range(5):
        vertexes_side=[vertex_top,vertexes_high[i],vertexes_high[i+1],vertex_top ]
        polygon_side=Part.makePolygon(vertexes_side)
        faces.append(Part.Face(polygon_side))

    shell = Part.makeShell(faces)
    solid = Part.makeSolid(shell)
    obj=App.ActiveDocument.addObject("Part::Feature","Icosahedron")
    obj.Shape = solid



def build_icosahedron_truncated(radius):

    z = 4*radius / math.sqrt(10 + 2 * math.sqrt(5))
    anglefaces = 138.189685104
    r = z/12 * math.sqrt(3) * (3 + math.sqrt(5))

    #radius of a pentagram with the same side
    radius2 = z / math.sin(36 * math.pi/180)/2

    #height of radius2 in the sphere
    angle = math.acos(radius2/radius)
    height = radius * math.sin(angle)

    faces = []

    vertex_bottom = (0,0,-radius)
    vertexes_low = horizontal_regular_polygon_vertexes(5,radius2, -height)
    vertexes_high = horizontal_regular_polygon_vertexes(5,radius2, height,  -math.pi/5)
    vertex_top = (0,0,radius)

    vertexes_bottom = []
    vertexes_top = []

    for i in range(6):
        new_vertex = ((vertex_bottom[0]+vertexes_low[i][0])/3 , (vertex_bottom[1]+vertexes_low[i][1])/3 , vertex_bottom[2]-(vertex_bottom[2]-vertexes_low[i][2])/3)
        vertexes_bottom.append(new_vertex)
    polygon_side=Part.makePolygon(vertexes_bottom)
    faces.append(Part.Face(polygon_side))

    for i in range(6):
        new_vertex = ((vertex_top[0]+vertexes_high[i][0])/3 , (vertex_top[1]+vertexes_high[i][1])/3 , vertex_top[2]-(vertex_top[2]-vertexes_high[i][2])/3)
        vertexes_top.append(new_vertex)
    polygon_side=Part.makePolygon(vertexes_top)
    faces.append(Part.Face(polygon_side))

    pg6_bottom = []
    for i in range(5):
        vertex1=vertexes_bottom[i]
        vertex2=vertexes_bottom[i+1]
        vertex3=(vertexes_bottom[i+1][0] + (vertexes_low[i+1][0] - vertexes_bottom[i+1][0])/2, vertexes_bottom[i+1][1] + (vertexes_low[i+1][1] - vertexes_bottom[i+1][1])/2, (vertexes_low[i+1][2] + vertexes_bottom[i+1][2])/2)
        vertex4=((vertexes_low[i+1][0]*2 +vertexes_low[i][0])/3, (vertexes_low[i+1][1]*2 +vertexes_low[i][1])/3, -height)
        vertex5=((vertexes_low[i+1][0]+vertexes_low[i][0]*2)/3, (vertexes_low[i+1][1] +vertexes_low[i][1]*2)/3, -height)
        vertex6=(vertexes_bottom[i][0] + (vertexes_low[i][0] - vertexes_bottom[i][0])/2, vertexes_bottom[i][1] + (vertexes_low[i][1] - vertexes_bottom[i][1])/2, (vertexes_low[i][2] + vertexes_bottom[i][2])/2)
        vertexes = [vertex1,vertex2,vertex3,vertex4,vertex5,vertex6,vertex1]
        pg6_bottom.append(vertexes)
        polygon_side=Part.makePolygon(vertexes)
        faces.append(Part.Face(polygon_side))

    pg6_top = []
    for i in range(5):
        vertex1=vertexes_top[i]
        vertex2=vertexes_top[i+1]
        vertex3=(vertexes_top[i+1][0] + (vertexes_high[i+1][0] - vertexes_top[i+1][0])/2, vertexes_top[i+1][1] + (vertexes_high[i+1][1] - vertexes_top[i+1][1])/2, (vertexes_high[i+1][2] + vertexes_top[i+1][2])/2)
        vertex4=((vertexes_high[i+1][0]*2 +vertexes_high[i][0])/3, (vertexes_high[i+1][1]*2 +vertexes_high[i][1])/3, height)
        vertex5=((vertexes_high[i+1][0]+vertexes_high[i][0]*2)/3, (vertexes_high[i+1][1] +vertexes_high[i][1]*2)/3, height)
        vertex6=(vertexes_top[i][0] + (vertexes_high[i][0] - vertexes_top[i][0])/2, vertexes_top[i][1] + (vertexes_high[i][1] - vertexes_top[i][1])/2, (vertexes_high[i][2] + vertexes_top[i][2])/2)
        vertexes = [vertex1,vertex2,vertex3,vertex4, vertex5,vertex6,vertex1]
        pg6_top.append(vertexes)
        polygon_side=Part.makePolygon(vertexes)
        faces.append(Part.Face(polygon_side))

    pg6_low = []
    for i in range(5):
        vertex1 = pg6_bottom[i][3]
        vertex2 = pg6_bottom[i][4]
        vertex3 = ((vertexes_low[i][0]*2 + vertexes_high[i+1][0])/3,(vertexes_low[i][1]*2 + vertexes_high[i+1][1])/3, (vertexes_low[i][2]*2 + vertexes_high[i+1][2])/3)
        vertex4 = ((vertexes_low[i][0] + vertexes_high[i+1][0]*2)/3,(vertexes_low[i][1] + vertexes_high[i+1][1]*2)/3, (vertexes_low[i][2] + vertexes_high[i+1][2]*2)/3)
        vertex5 = ((vertexes_low[i+1][0] + vertexes_high[i+1][0]*2)/3,(vertexes_low[i+1][1] + vertexes_high[i+1][1]*2)/3, (vertexes_low[i+1][2] + vertexes_high[i+1][2]*2)/3)
        vertex6 = ((vertexes_low[i+1][0]*2 + vertexes_high[i+1][0])/3,(vertexes_low[i+1][1]*2 + vertexes_high[i+1][1])/3, (vertexes_low[i+1][2]*2 + vertexes_high[i+1][2])/3)
        vertexes = [vertex1,vertex2,vertex3,vertex4, vertex5,vertex6,vertex1]
        pg6_low.append(vertexes)
        polygon_side=Part.makePolygon(vertexes)
        faces.append(Part.Face(polygon_side))

    pg6_high = []
    for i in range(5):
        vertex1 = pg6_top[i][3]
        vertex2 = pg6_top[i][4]
        vertex3 = pg6_low[i-1][4]
        vertex4 = pg6_low[i-1][5]
        vertex5 = pg6_low[i][2]
        vertex6 = pg6_low[i][3]
        vertexes = [vertex1,vertex2, vertex3, vertex4,vertex5,vertex6 ,vertex1]
        pg6_high.append(vertexes)
        polygon_side=Part.makePolygon(vertexes)
        faces.append(Part.Face(polygon_side))

    for i in range(5):
        vertex1 = pg6_top[i][4]
        vertex2 = pg6_top[i][5]
        vertex3 = pg6_high[i-1][6]
        vertex4 = pg6_high[i-1][5]
        vertex5 = pg6_low[i-1][4]
        vertexes = [vertex1,vertex2, vertex3,vertex4,vertex5,vertex1]
        polygon_side=Part.makePolygon(vertexes)
        faces.append(Part.Face(polygon_side))

    for i in range(5):
        vertex1 = pg6_bottom[i][4]
        vertex2 = pg6_bottom[i][5]
        vertex3 = pg6_low[i-1][6]
        vertex4 = pg6_low[i-1][5]
        vertex5 = pg6_high[i][4]
        vertexes = [vertex1,vertex2, vertex3,vertex4,vertex5, vertex1]
        polygon_side=Part.makePolygon(vertexes)
        faces.append(Part.Face(polygon_side))


    shell = Part.makeShell(faces)
    solid = Part.makeSolid(shell)
    obj=App.ActiveDocument.addObject("Part::Feature","Icosahedron_truncated")
    obj.Shape = solid



def msgbox(s):
    msg = QtGui.QMessageBox()
    msg.setIcon(QtGui.QMessageBox.Information)
    msg.setText(s)
    msg.setWindowTitle("Message")
    msg.setStandardButtons(QtGui.QMessageBox.Ok )
    retval = msg.exec_()






class polyhedron_dialog(QtGui.QWidget):

    def __init__(self):
        super(polyhedron_dialog, self).__init__()

        self.initUI()

    def initUI(self):
        grid = QtGui.QGridLayout()

        button = QtGui.QPushButton('Cancel')
        grid.addWidget(button, 10, 3)
        button.clicked.connect(self.cancel_method)
        button2 = QtGui.QPushButton('OK')
        grid.addWidget(button2, 10, 5)
        button2.clicked.connect(self.slot_method)

        self.comboBox = QtGui.QComboBox(self)
        grid.addWidget(self.comboBox, 0, 3)
        self.comboBox.addItem("tetrahedron")
        self.comboBox.addItem("hexahedron")
        self.comboBox.addItem("octahedron")
        self.comboBox.addItem("dodecahedron")
        self.comboBox.addItem("icosahedron")
        self.comboBox.addItem("icosahedron-truncated")


        grid.addWidget(QtGui.QLabel('radius :'), 3, 2)
        self.radius = QtGui.QLineEdit()
        grid.addWidget(self.radius,3,3)

        grid.addWidget(QtGui.QLabel('or sidelength:'), 3, 4)
        self.side = QtGui.QLineEdit()
        grid.addWidget(self.side, 3,5)



        self.setLayout(grid)
        self.move(500, 350)
        self.setWindowTitle('Polyhedrons as FreeCad-Part')
        self.show()



    def slot_method(self):

        if (str(self.radius.text()))== "":
            radius = 0
        else:
            radius = float(str(self.radius.text()))

        if (str(self.side.text()))== "":
            side = 0
        else:
            side = float(str(self.side.text()))

        if radius == 0 and side == 0 :
            msgbox("INPUT ERROR!")

        else :
            if self.comboBox.currentText() == "tetrahedron":
                if radius==0:
                    radius = side / 4 * math.sqrt(6)
                build_tetrahedron(radius)
            elif self.comboBox.currentText() == "hexahedron":
                if radius == 0:
                    radius = side * 2 / math.sqrt(3)
                build_hexahedron(radius)
            elif self.comboBox.currentText() == "octahedron":
                if radius == 0:
                    radius = side / math.sqrt(2)
                build_octahedron(radius)
            elif self.comboBox.currentText() == "dodecahedron":
                if radius == 0:
                    radius = side / 4 *  math.sqrt(3) * (1 + math.sqrt(5))
                build_dodecahedron(radius)
            elif self.comboBox.currentText() == "icosahedron":
                if radius == 0:
                    radius = side / 4 * math.sqrt(10 + 2 * math.sqrt(5))
                build_icosahedron(radius)
            elif self.comboBox.currentText() == "icosahedron-truncated":
                if radius == 0:
                    radius = side / 4 * math.sqrt(10 + 2 * math.sqrt(5))
                build_icosahedron_truncated(radius)

        self.close()

    def cancel_method(self):
        self.close()


mainaction = polyhedron_dialog()

