# -*- coding: utf-8 -*-
# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2019 - Suraj <dadralj18@gmail.com>                      *
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

__title__ = "Column Reinforcement"
__author__ = "Suraj"
__url__ = "https://www.freecadweb.org"

from RebarDistribution import runRebarDistribution, removeRebarDistribution
from Rebarfunc import getSelectedFace, check_selected_face
from .SingleTie import makeSingleTieFourRebars
from PySide import QtGui
import FreeCAD
import FreeCADGui
import os


class _ColumnTaskPanel:
    def __init__(self, Rebar=None):
        self.customSpacing = None
        if not Rebar:
            selected_obj = FreeCADGui.Selection.getSelectionEx()[0]
            self.SelectedObj = selected_obj.Object
            self.FaceName = selected_obj.SubElementNames[0]
        else:
            self.FaceName = Rebar.Base.Support[0][1][0]
            self.SelectedObj = Rebar.Base.Support[0][0]
        self.form = FreeCADGui.PySideUic.loadUi(os.path.splitext(__file__)[0] + ".ui")
        self.form.setWindowTitle(
            QtGui.QApplication.translate("RebarAddon", "Column Reinforcement", None)
        )
        self.form.image.setPixmap(
            QtGui.QPixmap(
                os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
                + "/icons/Column_CustomConfiguration.png"
            )
        )
        self.addDropdownMenuItems()
        self.connectSignalSlots()
        self.form.mainRebarOrientationWidget.hide()
        self.form.x_dirRebarOrientationWidget.hide()
        self.form.y_dirRebarOrientationWidget.hide()
        self.Rebar = Rebar

    def addDropdownMenuItems(self):
        """ This function add dropdown items to each Gui::PrefComboBox."""
        self.form.columnConfiguration.addItems(
            ["Custom Configuration", "SingleTieFourRebars"]
        )
        self.form.bentAngle.addItems(["90", "135"])
        self.form.mainRebarType.addItems(["StraightRebar", "LShapeRebar"])
        self.form.x_dirRebarType.addItems(["StraightRebar", "LShapeRebar"])
        self.form.y_dirRebarType.addItems(["StraightRebar", "LShapeRebar"])
        hook_orientation_list = [
            "Top Inside",
            "Top Outside",
            "Top Left",
            "Top Right",
            "Bottom Inside",
            "Bottom Outside",
            "Bottom Left",
            "Bottom Right",
        ]
        self.form.mainRebarHookOrientation.addItems(hook_orientation_list)
        self.form.x_dirRebarHookOrientation.addItems(hook_orientation_list)
        self.form.y_dirRebarHookOrientation.addItems(hook_orientation_list)
        hook_extend_along_list = ["x-axis", "y-axis"]
        self.form.mainRebarHookExtendAlong.addItems(hook_extend_along_list)
        self.form.x_dirRebarHookExtendAlong.addItems(hook_extend_along_list)
        self.form.y_dirRebarHookExtendAlong.addItems(hook_extend_along_list)

    def connectSignalSlots(self):
        """ This function is used to connect different slots in UI to appropriate functions."""
        self.form.columnConfiguration.currentIndexChanged.connect(
            self.changeColumnConfiguration
        )
        self.form.number_radio.clicked.connect(self.number_radio_clicked)
        self.form.spacing_radio.clicked.connect(self.spacing_radio_clicked)
        self.form.mainRebarType.currentIndexChanged.connect(self.getMainRebarType)
        self.form.x_dirRebarType.currentIndexChanged.connect(self.getXDirRebarType)
        self.form.y_dirRebarType.currentIndexChanged.connect(self.getYDirRebarType)
        self.form.mainRebarHookExtendAlong.currentIndexChanged.connect(
            self.getHookExtendAlong
        )
        self.form.x_dirRebarHookExtendAlong.currentIndexChanged.connect(
            self.getHookExtendAlong
        )
        self.form.y_dirRebarHookExtendAlong.currentIndexChanged.connect(
            self.getHookExtendAlong
        )
        self.form.customSpacing.clicked.connect(lambda: runRebarDistribution(self))
        self.form.removeCustomSpacing.clicked.connect(
            lambda: removeRebarDistribution(self)
        )
        self.form.PickSelectedFace.clicked.connect(lambda: getSelectedFace(self))

    def getStandardButtons(self):
        """ This function add standard buttons to tool bar."""
        return (
            int(QtGui.QDialogButtonBox.Ok)
            | int(QtGui.QDialogButtonBox.Apply)
            | int(QtGui.QDialogButtonBox.Cancel)
            | int(QtGui.QDialogButtonBox.Help)
            | int(QtGui.QDialogButtonBox.Reset)
        )

    def clicked(self, button):
        if button == int(QtGui.QDialogButtonBox.Apply):
            self.accept(button)

    def accept(self, signal=None):
        self.column_configuration = self.form.columnConfiguration.currentText()
        if not self.Rebar:
            if self.column_configuration == "Custom Configuration":
                print("Implementation in progress")
            elif self.column_configuration == "SingleTieFourRebars":
                self.getTieData()
                self.getMainRebarData()
                makeSingleTieFourRebars(
                    self.xdir_cover,
                    self.ydir_cover,
                    self.offset_of_tie,
                    self.bentAngle,
                    self.extensionFactor,
                    self.dia_of_tie,
                    self.number_spacing_check,
                    self.number_spacing_value,
                    self.main_rebar_diameter,
                    self.main_rebar_t_offset,
                    self.main_rebar_b_offset,
                    self.main_rebar_type,
                    self.main_rebar_hook_orientation,
                    self.main_rebar_hook_extend_along,
                    self.main_rebar_rounding,
                    self.main_rebar_hook_extension,
                    self.SelectedObj,
                    self.FaceName,
                )
        self.Rebar = True
        if signal == int(QtGui.QDialogButtonBox.Apply):
            pass
        else:
            FreeCADGui.Control.closeDialog(self)

    def getTieData(self):
        self.xdir_cover = self.form.x_dirCover.text()
        self.xdir_cover = FreeCAD.Units.Quantity(self.xdir_cover).Value
        self.ydir_cover = self.form.y_dirCover.text()
        self.ydir_cover = FreeCAD.Units.Quantity(self.ydir_cover).Value
        self.offset_of_tie = self.form.tieOffset.text()
        self.offset_of_tie = FreeCAD.Units.Quantity(self.offset_of_tie).Value
        self.dia_of_tie = self.form.tieDiameter.text()
        self.dia_of_tie = FreeCAD.Units.Quantity(self.dia_of_tie).Value
        self.bentAngle = int(self.form.bentAngle.currentText())
        self.extensionFactor = self.form.extensionFactor.value()
        self.number_check = self.form.number_radio.isChecked()
        self.spacing_check = self.form.spacing_radio.isChecked()
        if self.number_check:
            self.number_spacing_check = True
            self.number_spacing_value = self.form.number.value()
        elif self.spacing_check:
            self.number_spacing_check = False
            self.number_spacing_value = self.form.spacing.value()

    def getMainRebarData(self):
        self.main_rebar_type = self.form.mainRebarType.currentText()
        self.main_rebar_hook_orientation = (
            self.form.mainRebarHookOrientation.currentText()
        )
        self.main_rebar_hook_extend_along = (
            self.form.mainRebarHookExtendAlong.currentText()
        )
        self.main_rebar_hook_extension = self.form.mainRebarHookExtension.text()
        self.main_rebar_hook_extension = FreeCAD.Units.Quantity(
            self.main_rebar_hook_extension
        ).Value
        self.main_rebar_rounding = self.form.mainRebarLRebarRounding.value()
        self.main_rebar_t_offset = self.form.mainRebarTopOffset.text()
        self.main_rebar_t_offset = FreeCAD.Units.Quantity(
            self.main_rebar_t_offset
        ).Value
        self.main_rebar_b_offset = self.form.mainRebarBottomOffset.text()
        self.main_rebar_b_offset = FreeCAD.Units.Quantity(
            self.main_rebar_b_offset
        ).Value
        self.main_rebar_diameter = self.form.mainRebarDiameter.text()
        self.main_rebar_diameter = FreeCAD.Units.Quantity(
            self.main_rebar_diameter
        ).Value

    def getXDirRebarData(self):
        self.xdir_rebar_type = self.form.x_dirRebarType.currentText()
        self.xdir_rebar_hook_orientation = (
            self.form.x_dirRebarHookOrientation.currentText()
        )
        self.xdir_rebar_hook_extend_along = (
            self.form.x_dirRebarHookExtendAlong.currentText()
        )
        self.xdir_rebar_hook_extension = self.form.x_dirRebarHookExtension.text()
        self.xdir_rebar_hook_extension = FreeCAD.Units.Quantity(
            self.xdir_rebar_hook_extension
        ).Value
        self.xdir_rebar_rounding = self.form.x_dirLRebarRounding.value()
        self.xdir_rebar_t_offset = self.form.x_dirRebarTopOffset.text()
        self.xdir_rebar_t_offset = FreeCAD.Units.Quantity(
            self.xdir_rebar_t_offset
        ).Value
        self.xdir_rebar_b_offset = self.form.x_dirRebarBottomOffset.text()
        self.xdir_rebar_b_offset = FreeCAD.Units.Quantity(
            self.xdir_rebar_b_offset
        ).Value
        self.xdir_rebar_dia_str = self.form.x_dirNumberDiameter.text()
        self.xdir_rebar_dia_list = self.gettupleOfNumberDiameter(
            self.xdir_rebar_dia_str
        )

    def getYDirRebarData(self):
        self.ydir_rebar_type = self.form.y_dirRebarType.currentText()
        self.ydir_rebar_hook_orientation = (
            self.form.y_dirRebarHookOrientation.currentText()
        )
        self.ydir_rebar_hook_extend_along = (
            self.form.y_dirRebarHookExtendAlong.currentText()
        )
        self.ydir_rebar_hook_extension = self.form.y_dirRebarHookExtension.text()
        self.ydir_rebar_hook_extension = FreeCAD.Units.Quantity(
            self.ydir_rebar_hook_extension
        ).Value
        self.ydir_rebar_rounding = self.form.y_dirLRebarRounding.value()
        self.ydir_rebar_t_offset = self.form.y_dirRebarTopOffset.text()
        self.ydir_rebar_t_offset = FreeCAD.Units.Quantity(
            self.ydir_rebar_t_offset
        ).Value
        self.ydir_rebar_b_offset = self.form.y_dirRebarBottomOffset.text()
        self.ydir_rebar_b_offset = FreeCAD.Units.Quantity(
            self.ydir_rebar_b_offset
        ).Value
        self.ydir_rebar_dia_str = self.form.y_dirNumberDiameter.text()
        self.ydir_rebar_dia_list = self.gettupleOfNumberDiameter(
            self.ydir_rebar_dia_str
        )

    def changeColumnConfiguration(self):
        """ This function is used to find selected column configuration from UI
        and update UI accordingly."""
        self.column_configuration = self.form.columnConfiguration.currentText()
        if self.column_configuration == "Custom Configuration":
            self.form.image.setPixmap(
                QtGui.QPixmap(
                    os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
                    + "/icons/Column_CustomConfiguration.png"
                )
            )
            self.showXdirRebarsWidget()
            self.showYdirRebarsWidget()
        elif self.column_configuration == "SingleTieFourRebars":
            self.form.image.setPixmap(
                QtGui.QPixmap(
                    os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
                    + "/icons/Column_SingleTieFourRebars.png"
                )
            )
            self.hideXdirRebarsWidget()
            self.hideYdirRebarsWidget()

    def number_radio_clicked(self):
        """ This function enable number field and disable spacing field in UI
        when number radio button is clicked."""
        self.form.spacing.setEnabled(False)
        self.form.number.setEnabled(True)

    def spacing_radio_clicked(self):
        """ This function enable spacing field and disable number field in UI
        when spacing radio button is clicked."""
        self.form.number.setEnabled(False)
        self.form.spacing.setEnabled(True)

    def getMainRebarType(self):
        """ This function is used to find Main Rebars Type and update UI
        accordingly."""
        self.main_rebar_type = self.form.mainRebarType.currentText()
        if self.main_rebar_type == "LShapeRebar":
            self.form.mainRebarOrientationWidget.show()
        else:
            self.form.mainRebarOrientationWidget.hide()

    def getXDirRebarType(self):
        """ This function is used to find Rebar Type of rebars placed along
        X-Direction and update UI accordingly."""
        self.xdir_rebar_type = self.form.x_dirRebarType.currentText()
        if self.xdir_rebar_type == "LShapeRebar":
            self.form.x_dirRebarOrientationWidget.show()
        else:
            self.form.x_dirRebarOrientationWidget.hide()

    def getYDirRebarType(self):
        """ This function is used to find Rebar Type of rebars placed along
        Y-Direction and update UI accordingly."""
        self.ydir_rebar_type = self.form.y_dirRebarType.currentText()
        if self.ydir_rebar_type == "LShapeRebar":
            self.form.y_dirRebarOrientationWidget.show()
        else:
            self.form.y_dirRebarOrientationWidget.hide()

    def getHookExtendAlong(self):
        """ This function is used to find HookExtendAlong value from UI."""
        self.main_hook_extend_along = self.form.mainRebarHookExtendAlong.currentText()
        self.xdir_hook_extend_along = self.form.x_dirRebarHookExtendAlong.currentText()
        self.ydir_hook_extend_along = self.form.y_dirRebarHookExtendAlong.currentText()

    def hideXdirRebarsWidget(self):
        """ This function hide widget related to Rebars placed along
        X-Direction."""
        self.form.x_dirRebarsWidget.hide()

    def hideYdirRebarsWidget(self):
        """ This function hide widget related to Rebars placed along
        Y-Direction."""
        self.form.y_dirRebarsWidget.hide()

    def showXdirRebarsWidget(self):
        """ This function show widget related to Rebars placed along
        X-Direction."""
        self.form.x_dirRebarsWidget.show()

    def showYdirRebarsWidget(self):
        """ This function show widget related to Rebars placed along
        Y-Direction."""
        self.form.y_dirRebarsWidget.show()

    def gettupleOfNumberDiameter(self, diameter_string):
        """ gettupleOfNumberDiameter(diameter_string): This function take input
        in specific syntax and return output in the form of list. For eg.
        Input: "3#100+2#200+3#100"
        Output: [(3, 100), (2, 200), (3, 100)]"""
        diameter_st = diameter_string.strip()
        diameter_sp = diameter_st.split("+")
        index = 0
        number_diameter_list = []
        while index < len(diameter_sp):
            # Find "#" recursively in diameter_sp array.
            in_sp = diameter_sp[index].split("#")
            number_diameter_list.append(
                (int(in_sp[0]), float(in_sp[1].replace("mm", "")))
            )
            index += 1
        return number_diameter_list

def CommandColumnReinforcement():
    selected_obj = check_selected_face()
    if selected_obj:
        FreeCADGui.Control.showDialog(_ColumnTaskPanel())
