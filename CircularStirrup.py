# -*- coding: utf-8 -*-
# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2017 - Amritpal Singh <amrit3701@gmail.com>             *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

__title__ = "CircularStirrup"
__author__ = "Amritpal Singh"
__url__ = "https://www.freecadweb.org"

from PySide import QtCore, QtGui
from Rebarfunc import *
from PySide.QtCore import QT_TRANSLATE_NOOP
from RebarDistribution import runRebarDistribution, removeRebarDistribution
import FreeCAD
import FreeCADGui
import ArchCommands
import os
import sys
import math

#def getsubEleCoordinatesCircularStirrup(angel, edges, b_cover, t_cover, size, direction):
#    if direction

def getpointsOfCircularStirrup(FacePRM, s_cover, b_cover, t_cover, pitch, edges, diameter, size, direction):
    """ getpointsOfCircularStirrup(FacePRM, s_cover, b_cover, t_cover):
    Return points of the LShape rebar in the form of array for sketch."""
    #spacing = 150
    #segment = 8*2
    #numCircular = h_col / spacing
    dx = s_cover + diameter / 2
    dz = float(pitch) / edges
    R = diameter / 2 - dx
    R = FacePRM[0][0] / 2 - s_cover
    points = []
    if direction[2] in {-1,1}:
        z = 0
        l = 0
        if direction[2] == 1:
            zz = FacePRM[1][2] - t_cover
        elif direction[2] == -1:
            zz = FacePRM[1][2] + b_cover
        count = 0
        flag = False
        while (round(z) < abs(size - b_cover - t_cover)):
            for i in range(0, int(edges) + 1):
                if not i and flag:
                    continue
                if not flag:
                    z -= dz
                    flag = True
                iAngle = i * 360 / edges
                x =  FacePRM[1][0] + R * math.cos(math.radians(iAngle))
                y =  FacePRM[1][1] + R * math.sin(math.radians(iAngle))
                points.append(FreeCAD.Vector(x, y, zz))
                count += 1
                if direction[2] == 1:
                    zz -= dz
                elif direction[2] == -1:
                    zz += dz
                z += dz
    return points

class _CircularStirrupTaskPanel:
    def __init__(self, Rebar = None):
        self.form = FreeCADGui.PySideUic.loadUi(os.path.splitext(__file__)[0] + ".ui")
        self.form.setWindowTitle(QtGui.QApplication.translate("Arch", "Circular Stirrup Rebar", None))
        self.form.customSpacing.clicked.connect(lambda: runRebarDistribution(Rebar))
        self.form.removeCustomSpacing.clicked.connect(lambda: removeRebarDistribution(Rebar))
        self.form.PickSelectedFace.clicked.connect(lambda: getSelectedFace(self))
        self.form.image.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/icons/CircularStirrupBR.svg"))
        self.Rebar = Rebar
        self.SelectedObj = None
        self.FaceName = None

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok) | int(QtGui.QDialogButtonBox.Cancel)

    def accept(self):
        b_cover = self.form.bottomCover.text()
        b_cover = FreeCAD.Units.Quantity(b_cover).Value
        s_cover = self.form.sideCover.text()
        s_cover = FreeCAD.Units.Quantity(s_cover).Value
        t_cover = self.form.topCover.text()
        t_cover = FreeCAD.Units.Quantity(t_cover).Value
        pitch = self.form.pitch.text()
        pitch = FreeCAD.Units.Quantity(pitch).Value
        edges = self.form.edges.text()
        edges = FreeCAD.Units.Quantity(edges).Value
        diameter = self.form.diameter.text()
        diameter = FreeCAD.Units.Quantity(diameter).Value
        if not self.Rebar:
            makeCircularStirrup(s_cover, b_cover, diameter, t_cover, pitch, edges, self.SelectedObj, self.FaceName)
        else:
            editCircularStirrup(self.Rebar, s_cover, b_cover, diameter, t_cover, pitch, edges, self.SelectedObj, self.FaceName)
        FreeCADGui.Control.closeDialog(self)

def makeCircularStirrup(s_cover, b_cover, diameter, t_cover, pitch, edges, structure = None, facename = None):
    """ makeCircularStirrup(f_cover, b_cover, s_cover, diameter, t_cover, rounding, rebarAlong, amount_spacing_check, amount_spacing_value):
    Adds the L-Shape reinforcement bar to the selected structural object."""
    if not structure and not facename:
        selected_obj = FreeCADGui.Selection.getSelectionEx()[0]
        structure = selected_obj.Object
        facename = selected_obj.SubElementNames[0]
    face = structure.Shape.Faces[getFaceNumber(facename) - 1]
    StructurePRM = getTrueParametersOfStructure(structure)
    FacePRM = getParametersOfFace(structure, facename, False)
    print FacePRM
    if not FacePRM:
        FreeCAD.Console.PrintError("Cannot identified shape or from which base object sturctural element is derived\n")
        return
    size = (ArchCommands.projectToVector(structure.Shape.copy(), face.normalAt(0, 0))).Length
    normal = face.normalAt(0,0)
    normal = face.Placement.Rotation.inverted().multVec(normal)
    # Get points of L-Shape rebar
    points = getpointsOfCircularStirrup(FacePRM, s_cover, b_cover, t_cover, pitch, edges, diameter, size, normal)
    import Arch
    import Draft
    wire = Draft.makeWire(points,closed=False,face=True,support=None)
    wire.Support = [(structure, facename)]
    rebar = Arch.makeRebar(structure, wire, diameter, 1, 0)
    FreeCAD.ActiveDocument.recompute()
    # Adds properties to the rebar object
    rebar.ViewObject.addProperty("App::PropertyString", "RebarShape", "RebarDialog", QT_TRANSLATE_NOOP("App::Property", "Shape of rebar")).RebarShape = "CircularStirrup"
    rebar.ViewObject.setEditorMode("RebarShape", 2)
    rebar.addProperty("App::PropertyDistance", "SideCover", "RebarDialog", QT_TRANSLATE_NOOP("App::Property", "Front cover of rebar")).SideCover = s_cover
    rebar.setEditorMode("SideCover", 2)
    rebar.addProperty("App::PropertyDistance", "Pitch", "RebarDialog", QT_TRANSLATE_NOOP("App::Property", "Left Side cover of rebar")).Pitch = pitch
    rebar.setEditorMode("Pitch", 2)
    rebar.addProperty("App::PropertyInteger", "Edges", "RebarDialog", QT_TRANSLATE_NOOP("App::Property", "Right Side cover of rebar")).Edges = int(edges)
    rebar.setEditorMode("Edges", 2)
    rebar.addProperty("App::PropertyDistance", "BottomCover", "RebarDialog", QT_TRANSLATE_NOOP("App::Property", "Bottom cover of rebar")).BottomCover = b_cover
    rebar.setEditorMode("BottomCover", 2)
    rebar.addProperty("App::PropertyDistance", "TopCover", "RebarDialog", QT_TRANSLATE_NOOP("App::Property", "Top cover of rebar")).TopCover = t_cover
    rebar.setEditorMode("TopCover", 2)
    rebar.Label = "CircularStirrup"
    FreeCAD.ActiveDocument.recompute()
    return rebar

def editCircularStirrup(Rebar, s_cover, b_cover, diameter, t_cover, pitch, edges, structure = None, facename = None):
    sketch = Rebar.Base
    if structure and facename:
        sketch.Support = [(structure, facename)]
    # Check if sketch support is empty.
    if not sketch.Support:
        showWarning("You have checked remove external geometry of base sketchs when needed.\nTo unchecked Edit->Preferences->Arch.")
        return
    # Assigned values
    facename = sketch.Support[0][1][0]
    structure = sketch.Support[0][0]
    face = structure.Shape.Faces[getFaceNumber(facename) - 1]
    StructurePRM = getTrueParametersOfStructure(structure)
    # Get parameters of the face where sketch of rebar is drawn
    FacePRM = getParametersOfFace(structure, facename, False)
    size = (ArchCommands.projectToVector(structure.Shape.copy(), face.normalAt(0, 0))).Length
    normal = face.normalAt(0,0)
    normal = face.Placement.Rotation.inverted().multVec(normal)
    # Get points of L-Shape rebar
    points = getpointsOfCircularStirrup(FacePRM, s_cover, b_cover, t_cover, pitch, edges, diameter, size, normal)
    Rebar.Base.Points = points
    FreeCAD.ActiveDocument.recompute()
    Rebar.SideCover = s_cover
    Rebar.BottomCover = b_cover
    Rebar.TopCover = t_cover
    Rebar.Pitch = pitch
    Rebar.Edges = int(edges)
    #Rebar.Orientation = orientation
    FreeCAD.ActiveDocument.recompute()

def editDialog(vobj):
    FreeCADGui.Control.closeDialog()
    obj = _CircularStirrupTaskPanel(vobj.Object)
    obj.form.sideCover.setText(str(vobj.Object.SideCover))
    obj.form.bottomCover.setText(str(vobj.Object.BottomCover))
    obj.form.diameter.setText(str(vobj.Object.Diameter))
    obj.form.topCover.setText(str(vobj.Object.TopCover))
    obj.form.edges.setValue(vobj.Object.Edges)
    obj.form.pitch.setText(str(vobj.Object.Pitch))
    #obj.form.orientation.setCurrentIndex(obj.form.orientation.findText(str(vobj.Object.Orientation)))
    FreeCADGui.Control.showDialog(obj)

def CommandCircularStirrup():
    selected_obj = check_selected_face()
    if selected_obj:
        FreeCADGui.Control.showDialog(_CircularStirrupTaskPanel())
