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

__title__ = "DialogDistribution"
__author__ = "Amritpal Singh"
__url__ = "https://www.freecadweb.org"

from PySide import QtCore, QtGui
from Rebarfunc import *
from PySide.QtCore import QT_TRANSLATE_NOOP
import FreeCAD
import FreeCADGui
import os
import sys
import math

class _RebarDistributionDialog():
    def __init__(self, Rebar):
        self.form = FreeCADGui.PySideUic.loadUi(os.path.splitext(__file__)[0] + ".ui")
        self.form.setWindowTitle(QtGui.QApplication.translate("Arch", "Rebar Distribution", None))
        self.form.image.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0] + "/icons/RebarDistribution.svg"))
        self.Rebar = Rebar

    def accept(self):
        amount1 = self.form.amount1.value()
        spacing1 = self.form.spacing1.text()
        spacing1 = FreeCAD.Units.Quantity(spacing1).Value
        amount2 = self.form.amount2.value()
        spacing2 = self.form.spacing2.text()
        spacing2 = FreeCAD.Units.Quantity(spacing2).Value
        amount3 = self.form.amount3.value()
        spacing3 = self.form.spacing3.text()
        spacing3 = FreeCAD.Units.Quantity(spacing3).Value
        setRebarDistribution(self.Rebar, amount1, spacing1, amount2, spacing2, amount3, spacing3)

    def setupUi(self):
        # Connect Signals and Slots
        self.form.buttonBox.accepted.connect(self.accept)
        pass

def setRebarDistribution(Rebar, amount1, spacing1, amount2, spacing2, amount3, spacing3):
    import ArchCommands
    structure = Rebar.Host
    # Check if sketch support is empty.
    if not Rebar.Base.Support:
        showWarning("You have checked remove external geometry of base sketchs when needed.\nTo unchecked Edit->Preferences->Arch.")
        return
    facename = Rebar.Base.Support[0][1][0]
    face = structure.Shape.Faces[int(facename[-1]) - 1]
    size = (ArchCommands.projectToVector(structure.Shape.copy(), face.normalAt(0, 0))).Length
    #print size
    #print "amount1: ", amount1
    #print "spacing1: ", spacing1
    #print "amount2: ", amount2
    #print "spacing2: ", spacing2
    #print "amount3: ", amount3
    #print "spacing3: ", spacing3
    seg1_area = amount1 * spacing1 - spacing1 / 2
    seg3_area = amount3 * spacing3 - spacing3 / 2
    seg2_area = size - seg1_area - seg3_area - Rebar.OffsetStart.Value - Rebar.OffsetEnd.Value
    if spacing1 and spacing2 and spacing3 and amount1 and amount2 and amount3:
        pass
    else:
        if spacing1 and spacing2 and spacing3:
            amount2 = math.ceil(seg2_area / spacing2)
            spacing2 = seg2_area / amount2
        elif amount1 and amount2 and amount3:
            spacing2 = math.floor(seg2_area / amount2)
    CustomSpacing = str(amount1)+"@"+str(spacing1)+"+"+str(int(amount2))+"@"+str(spacing2)+"+"+str(amount3)+"@"+str(spacing3)
    Rebar.CustomSpacing = CustomSpacing
    #print CustomSpacing
    FreeCAD.ActiveDocument.recompute()

def getupleOfCustomSpacing(span_string):
    """ gettupleOfCustomSpacing(span_string): This function take input
    in specific syntax and return output in the form of list. For eg.
    Input: "3@100+2@200+3@100"
    Output: [(3, 100), (2, 200), (3, 100)]"""
    import string
    span_st = string.strip(span_string)
    span_sp = string.split(span_st, '+')
    index = 0
    spacinglist = []
    while index < len(span_sp):
        # Find "@" recursively in span_sp array.
        in_sp = string.split(span_sp[index], '@')
        spacinglist.append((int(in_sp[0]),float(in_sp[1])))
        index += 1
    return spacinglist

def runRebarDistribution(Rebar):
    dialog = _RebarDistributionDialog(Rebar)
    dialog.setupUi()
    dialog.form.exec_()

#runRebarDistribution(App.ActiveDocument.Rebar)
