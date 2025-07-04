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

__title__ = "BentShapeRebar"
__author__ = "Amritpal Singh"
__url__ = "https://www.freecadweb.org"

import math
from pathlib import Path
from typing import Tuple, List

import ArchCommands
import FreeCAD
import FreeCADGui
from PySide import QtGui
from PySide.QtCore import QT_TRANSLATE_NOOP

from PopUpImage import showPopUpImageDialog
from RebarData import RebarTypes
from RebarDistribution import runRebarDistribution, removeRebarDistribution
from Rebarfunc import (
    getSelectedFace,
    getFaceNumber,
    getParametersOfFace,
    showWarning,
    check_selected_face,
    facenormalDirection,
    get_rebar_amount_from_spacing,
)


# TODO: Use(Uncomment) typing.Literal for minimum python3.8


def getpointsOfBentShapeRebar(
    FacePRM: Tuple[Tuple[float, float], Tuple[float, float]],
    l_cover: float,
    r_cover: float,
    b_cover: float,
    t_cover: float,
    bentLength: float,
    bentAngle: float,
    # orientation: Literal["Bottom", "Top", "Left", "Right"],
    orientation: str,
    diameter: float,
    face_normal: FreeCAD.Vector,
) -> List[FreeCAD.Vector]:
    """getpointsOfBentShapeRebar(FacePRM, LeftCover, RightCover, BottomCover,
    TopCover, BentLength, BentAngle, Orientation, Diameter, FaceNormal):
    Return points of the LShape rebar in the form of array for sketch.
    It takes four different orientations input i.e. 'Bottom', 'Top', 'Left',
    'Right'.
    """
    center_x = FacePRM[1][0]
    center_y = FacePRM[1][1]
    # When Left/Rear Face of structure is selected
    if round(face_normal[0]) == -1 or round(face_normal[1]) == 1:
        center_x = -center_x
    # When Bottom Face of structure is selected
    elif round(face_normal[2]) == -1:
        center_y = -center_y
    if orientation == "Bottom":
        t_cover += diameter / 2
        b_cover += diameter / 2
        x1 = center_x - FacePRM[0][0] / 2 + l_cover
        y1 = center_y + FacePRM[0][1] / 2 - t_cover
        x2 = x1 + bentLength
        y2 = y1
        dis = (FacePRM[0][1] - t_cover - b_cover) * math.tan(
            math.radians(bentAngle - 90)
        )
        x3 = x2 + dis
        y3 = center_y - FacePRM[0][1] / 2 + b_cover
        x4 = center_x + FacePRM[0][0] / 2 - r_cover - bentLength - dis
        y4 = y3
        x5 = x4 + dis
        y5 = y2
        x6 = x5 + bentLength
        y6 = y5
    elif orientation == "Top":
        t_cover += diameter / 2
        b_cover += diameter / 2
        x1 = center_x - FacePRM[0][0] / 2 + l_cover
        y1 = center_y - FacePRM[0][1] / 2 + b_cover
        x2 = x1 + bentLength
        y2 = y1
        dis = (FacePRM[0][1] - t_cover - b_cover) * math.tan(
            math.radians(bentAngle - 90)
        )
        x3 = x2 + dis
        y3 = center_y + FacePRM[0][1] / 2 - t_cover
        x4 = center_x + FacePRM[0][0] / 2 - r_cover - bentLength - dis
        y4 = y3
        x5 = x4 + dis
        y5 = y2
        x6 = x5 + bentLength
        y6 = y5
    elif orientation == "Left":
        l_cover += diameter / 2
        r_cover += diameter / 2
        x1 = center_x + FacePRM[0][0] / 2 - r_cover
        y1 = center_y + FacePRM[0][1] / 2 - t_cover
        x2 = x1
        y2 = y1 - bentLength
        dis = (FacePRM[0][0] - r_cover - l_cover) * math.tan(
            math.radians(bentAngle - 90)
        )
        x3 = center_x - FacePRM[0][0] / 2 + l_cover
        y3 = y2 - dis
        x4 = x3
        y4 = center_y - FacePRM[0][1] / 2 + b_cover + bentLength + dis
        x5 = x2
        y5 = y4 - dis
        x6 = x5
        y6 = y5 - bentLength
    elif orientation == "Right":
        l_cover += diameter / 2
        r_cover += diameter / 2
        x1 = center_x - FacePRM[0][0] / 2 + l_cover
        y1 = center_y + FacePRM[0][1] / 2 - t_cover
        x2 = x1
        y2 = y1 - bentLength
        dis = (FacePRM[0][0] - r_cover - l_cover) * math.tan(
            math.radians(bentAngle - 90)
        )
        x3 = center_x + FacePRM[0][0] / 2 - r_cover
        y3 = y2 - dis
        x4 = x3
        y4 = center_y - FacePRM[0][1] / 2 + b_cover + bentLength + dis
        x5 = x2
        y5 = y4 - dis
        x6 = x5
        y6 = y5 - bentLength
    else:
        FreeCAD.Console.PrintError(f"Invalid orientation: {orientation}\n")
        return []
    return [
        FreeCAD.Vector(x1, y1, 0),
        FreeCAD.Vector(x2, y2, 0),
        FreeCAD.Vector(x3, y3, 0),
        FreeCAD.Vector(x4, y4, 0),
        FreeCAD.Vector(x5, y5, 0),
        FreeCAD.Vector(x6, y6, 0),
    ]


class _BentShapeRebarTaskPanel:
    def __init__(self, Rebar=None):
        if not Rebar:
            self.CustomSpacing = None
            selected_obj = FreeCADGui.Selection.getSelectionEx()[0]
            self.SelectedObj = selected_obj.Object
            self.FaceName = selected_obj.SubElementNames[0]
        else:
            self.CustomSpacing = Rebar.CustomSpacing
            if hasattr(Rebar.Base, "Support"):
                self.FaceName = Rebar.Base.Support[0][1][0]
                self.SelectedObj = Rebar.Base.Support[0][0]
            else:
                self.FaceName = Rebar.Base.AttachmentSupport[0][1][0]
                self.SelectedObj = Rebar.Base.AttachmentSupport[0][0]
        self.form = FreeCADGui.PySideUic.loadUi(
            str(Path(__file__).with_suffix(".ui"))
        )
        self.form.setWindowTitle(
            QtGui.QApplication.translate("RebarAddon", "Bent Shape Rebar", None)
        )
        self.form.orientationValue.addItems(["Bottom", "Top", "Right", "Left"])
        self.form.amount_radio.clicked.connect(self.amount_radio_clicked)
        self.form.spacing_radio.clicked.connect(self.spacing_radio_clicked)
        self.form.customSpacing.clicked.connect(
            lambda: runRebarDistribution(self)
        )
        self.form.removeCustomSpacing.clicked.connect(
            lambda: removeRebarDistribution(self)
        )
        self.form.PickSelectedFace.clicked.connect(
            lambda: getSelectedFace(self)
        )
        # self.form.orientationValue.currentIndexChanged.connect(
        #     self.getOrientation
        # )
        self.form.image.setPixmap(
            QtGui.QPixmap(
                str(Path(__file__).parent / "icons" / "BentShapeRebar.svg")
            )
        )
        # self.form.toolButton.setIcon(
        #     self.form.toolButton.style().standardIcon(
        #         QtGui.QStyle.SP_DialogHelpButton
        #     )
        # )
        self.form.toolButton.clicked.connect(
            lambda: showPopUpImageDialog(
                str(
                    Path(__file__).parent
                    / "icons"
                    / "BentShapeRebarDetailed.svg"
                )
            )
        )
        self.Rebar = Rebar

    # def getOrientation(self):
    # orientation = self.form.orientationValue.currentText()
    # if orientation == "Bottom":
    #     self.form.image.setPixmap(
    #         QtGui.QPixmap(
    #             os.path.split(os.path.abspath(__file__))[0]
    #             + "/icons/LShapeRebarBR.svg"
    #         )
    #     )
    # elif orientation == "Top":
    #     self.form.image.setPixmap(
    #         QtGui.QPixmap(
    #             os.path.split(os.path.abspath(__file__))[0]
    #             + "/icons/LShapeRebarBL.svg"
    #         )
    #     )
    # elif orientation == "Right":
    #     self.form.image.setPixmap(
    #         QtGui.QPixmap(
    #             os.path.split(os.path.abspath(__file__))[0]
    #             + "/icons/LShapeRebarTR.svg"
    #         )
    #     )
    # else:
    #     self.form.image.setPixmap(
    #         QtGui.QPixmap(
    #             os.path.split(os.path.abspath(__file__))[0]
    #             + "/icons/LShapeRebarTL.svg"
    #         )
    #     )

    @staticmethod
    def getStandardButtons():
        return (
            QtGui.QDialogButtonBox.Ok
            | QtGui.QDialogButtonBox.Apply
            | QtGui.QDialogButtonBox.Cancel
        )

    def clicked(self, button):
        if button == QtGui.QDialogButtonBox.Apply:
            self.accept(button)

    def accept(self, signal=None):
        f_cover = self.form.frontCover.text()
        f_cover = FreeCAD.Units.Quantity(f_cover).Value
        b_cover = self.form.bottomCover.text()
        b_cover = FreeCAD.Units.Quantity(b_cover).Value
        l_cover = self.form.l_sideCover.text()
        l_cover = FreeCAD.Units.Quantity(l_cover).Value
        r_cover = self.form.r_sideCover.text()
        r_cover = FreeCAD.Units.Quantity(r_cover).Value
        t_cover = self.form.topCover.text()
        t_cover = FreeCAD.Units.Quantity(t_cover).Value
        bentLength = self.form.bentLength.text()
        bentLength = FreeCAD.Units.Quantity(bentLength).Value
        bentAngle = self.form.bentAngle.value()
        diameter = self.form.diameter.text()
        diameter = FreeCAD.Units.Quantity(diameter).Value
        rounding = self.form.rounding.value()
        orientation = self.form.orientationValue.currentText()
        amount_check = self.form.amount_radio.isChecked()
        spacing_check = self.form.spacing_radio.isChecked()
        if not self.Rebar:
            if amount_check:
                amount = self.form.amount.value()
                rebar = makeBentShapeRebar(
                    f_cover,
                    b_cover,
                    l_cover,
                    r_cover,
                    diameter,
                    t_cover,
                    bentLength,
                    bentAngle,
                    rounding,
                    True,
                    amount,
                    orientation,
                    self.SelectedObj,
                    self.FaceName,
                )
            elif spacing_check:
                spacing = self.form.spacing.text()
                spacing = FreeCAD.Units.Quantity(spacing).Value
                rebar = makeBentShapeRebar(
                    f_cover,
                    b_cover,
                    l_cover,
                    r_cover,
                    diameter,
                    t_cover,
                    bentLength,
                    bentAngle,
                    rounding,
                    False,
                    spacing,
                    orientation,
                    self.SelectedObj,
                    self.FaceName,
                )
        else:
            if amount_check:
                amount = self.form.amount.value()
                rebar = editBentShapeRebar(
                    self.Rebar,
                    f_cover,
                    b_cover,
                    l_cover,
                    r_cover,
                    diameter,
                    t_cover,
                    bentLength,
                    bentAngle,
                    rounding,
                    True,
                    amount,
                    orientation,
                    self.SelectedObj,
                    self.FaceName,
                )
            elif spacing_check:
                spacing = self.form.spacing.text()
                spacing = FreeCAD.Units.Quantity(spacing).Value
                rebar = editBentShapeRebar(
                    self.Rebar,
                    f_cover,
                    b_cover,
                    l_cover,
                    r_cover,
                    diameter,
                    t_cover,
                    bentLength,
                    bentAngle,
                    rounding,
                    False,
                    spacing,
                    orientation,
                    self.SelectedObj,
                    self.FaceName,
                )
        if self.CustomSpacing:
            rebar.CustomSpacing = self.CustomSpacing
            FreeCAD.ActiveDocument.recompute()
        self.Rebar = rebar
        if signal == QtGui.QDialogButtonBox.Apply:
            pass
        else:
            FreeCADGui.Control.closeDialog()

    def amount_radio_clicked(self):
        self.form.spacing.setEnabled(False)
        self.form.amount.setEnabled(True)

    def spacing_radio_clicked(self):
        self.form.amount.setEnabled(False)
        self.form.spacing.setEnabled(True)


def makeBentShapeRebar(
    f_cover,
    b_cover,
    l_cover,
    r_cover,
    diameter,
    t_cover,
    bentLength,
    bentAngle,
    rounding,
    amount_spacing_check,
    amount_spacing_value,
    orientation="Bottom",
    structure=None,
    facename=None,
):
    """makeBentShapeRebar(FrontCover, BottomCover, LeftCover, RightCover,
    Diameter, TopCover, BentLength, BentAngle, Rounding, AmountSpacingCheck,
    AmountSpacingValue, Orientation, Structure, Facename):
    Adds the Bent-Shape reinforcement bar to the selected structural object.

    It takes four different orientations input i.e. 'Bottom', 'Top', 'Left',
    'Right'.
    """
    if not structure and not facename:
        selected_obj = FreeCADGui.Selection.getSelectionEx()[0]
        structure = selected_obj.Object
        facename = selected_obj.SubElementNames[0]
    face = structure.Shape.Faces[getFaceNumber(facename) - 1]
    # StructurePRM = getTrueParametersOfStructure(structure)
    FacePRM = getParametersOfFace(structure, facename)
    if not FacePRM:
        FreeCAD.Console.PrintError(
            "Cannot identify shape or from which base object structural "
            "element is derived\n"
        )
        return
    # Get points of L-Shape rebar
    points = getpointsOfBentShapeRebar(
        FacePRM,
        l_cover,
        r_cover,
        b_cover,
        t_cover,
        bentLength,
        bentAngle,
        orientation,
        diameter,
        facenormalDirection(structure, facename),
    )
    import Part
    import Arch

    sketch = FreeCAD.activeDocument().addObject(
        "Sketcher::SketchObject", "Sketch"
    )
    sketch.MapMode = "FlatFace"
    if hasattr(sketch, "Support"):
        sketch.Support = [(structure, facename)]
    else:
        sketch.AttachmentSupport = [(structure, facename)]
    FreeCAD.ActiveDocument.recompute()
    sketch.addGeometry(Part.LineSegment(points[0], points[1]), False)
    sketch.addGeometry(Part.LineSegment(points[1], points[2]), False)
    sketch.addGeometry(Part.LineSegment(points[2], points[3]), False)
    sketch.addGeometry(Part.LineSegment(points[3], points[4]), False)
    sketch.addGeometry(Part.LineSegment(points[4], points[5]), False)

    if amount_spacing_check:
        rebar = Arch.makeRebar(
            structure,
            sketch,
            diameter,
            amount_spacing_value,
            f_cover + diameter / 2,
            name="BentShapeRebar",
        )
        FreeCAD.ActiveDocument.recompute()
    else:
        size = (
            ArchCommands.projectToVector(
                structure.Shape.copy(), face.normalAt(0, 0)
            )
        ).Length
        rebar = Arch.makeRebar(
            structure,
            sketch,
            diameter,
            get_rebar_amount_from_spacing(size, diameter, amount_spacing_value),
            f_cover + diameter / 2,
            name="BentShapeRebar",
        )
    rebar.Rounding = rounding
    # Adds properties to the rebar object
    rebar.addProperty(
        "App::PropertyEnumeration",
        "RebarShape",
        "RebarDialog",
        QT_TRANSLATE_NOOP("App::Property", "Shape of rebar"),
    ).RebarShape = RebarTypes.tolist()
    rebar.RebarShape = "BentShapeRebar"
    rebar.setEditorMode("RebarShape", 2)
    rebar.addProperty(
        "App::PropertyDistance",
        "FrontCover",
        "RebarDialog",
        QT_TRANSLATE_NOOP("App::Property", "Front cover of rebar"),
    ).FrontCover = f_cover
    rebar.setEditorMode("FrontCover", 2)
    rebar.addProperty(
        "App::PropertyDistance",
        "LeftCover",
        "RebarDialog",
        QT_TRANSLATE_NOOP("App::Property", "Left Side cover of rebar"),
    ).LeftCover = l_cover
    rebar.setEditorMode("LeftCover", 2)
    rebar.addProperty(
        "App::PropertyDistance",
        "RightCover",
        "RebarDialog",
        QT_TRANSLATE_NOOP("App::Property", "Right Side cover of rebar"),
    ).RightCover = r_cover
    rebar.setEditorMode("RightCover", 2)
    rebar.addProperty(
        "App::PropertyDistance",
        "BottomCover",
        "RebarDialog",
        QT_TRANSLATE_NOOP("App::Property", "Bottom cover of rebar"),
    ).BottomCover = b_cover
    rebar.setEditorMode("BottomCover", 2)
    rebar.addProperty(
        "App::PropertyBool",
        "AmountCheck",
        "RebarDialog",
        QT_TRANSLATE_NOOP("App::Property", "Amount radio button is checked"),
    )
    rebar.setEditorMode("AmountCheck", 2)
    rebar.addProperty(
        "App::PropertyDistance",
        "TopCover",
        "RebarDialog",
        QT_TRANSLATE_NOOP("App::Property", "Top cover of rebar"),
    ).TopCover = t_cover
    rebar.setEditorMode("TopCover", 2)
    rebar.addProperty(
        "App::PropertyDistance",
        "TrueSpacing",
        "RebarDialog",
        QT_TRANSLATE_NOOP("App::Property", "Spacing between of rebars"),
    ).TrueSpacing = amount_spacing_value
    rebar.addProperty(
        "App::PropertyString",
        "Orientation",
        "RebarDialog",
        QT_TRANSLATE_NOOP("App::Property", "Shape of rebar"),
    ).Orientation = orientation
    rebar.setEditorMode("Orientation", 2)
    rebar.setEditorMode("TrueSpacing", 2)
    rebar.addProperty(
        "App::PropertyDistance",
        "BentLength",
        "RebarDialog",
        QT_TRANSLATE_NOOP("App::Property", "BentLength cover of rebar"),
    ).BentLength = bentLength
    rebar.setEditorMode("BentLength", 2)
    rebar.addProperty(
        "App::PropertyFloat",
        "BentAngle",
        "RebarDialog",
        QT_TRANSLATE_NOOP("App::Property", "Bent Angle of rebar"),
    ).BentAngle = bentAngle
    rebar.setEditorMode("BentAngle", 2)

    if amount_spacing_check:
        rebar.AmountCheck = True
    else:
        rebar.AmountCheck = False
        rebar.TrueSpacing = amount_spacing_value
    FreeCAD.ActiveDocument.recompute()
    return rebar


def editBentShapeRebar(
    Rebar,
    f_cover,
    b_cover,
    l_cover,
    r_cover,
    diameter,
    t_cover,
    bentLength,
    bentAngle,
    rounding,
    amount_spacing_check,
    amount_spacing_value,
    orientation,
    structure=None,
    facename=None,
):
    sketch = Rebar.Base
    if structure and facename:
        if hasattr(sketch, "Support"):
            sketch.Support = [(structure, facename)]
        else:
            sketch.AttachmentSupport = [(structure, facename)]
    # Check if sketch support is empty.
    if hasattr(sketch, "Support"):
        if not sketch.Support:
            showWarning(
                "You have checked: 'Remove external geometry of base sketches when "
                "needed.'\nTo uncheck: Edit->Preferences->Arch."
            )
            return
    else:
        if not sketch.AttachmentSupport:
            showWarning(
                "You have checked: 'Remove external geometry of base sketches when "
                "needed.'\nTo uncheck: Edit->Preferences->BIM."
            )
            return
    # Assigned values
    if hasattr(sketch, "Support"):
        facename = sketch.Support[0][1][0]
        structure = sketch.Support[0][0]
    else:
        facename = sketch.AttachmentSupport[0][1][0]
        structure = sketch.AttachmentSupport[0][0]
    face = structure.Shape.Faces[getFaceNumber(facename) - 1]
    # StructurePRM = getTrueParametersOfStructure(structure)
    # Get parameters of the face where sketch of rebar is drawn
    FacePRM = getParametersOfFace(structure, facename)
    # Get points of L-Shape rebar
    points = getpointsOfBentShapeRebar(
        FacePRM,
        l_cover,
        r_cover,
        b_cover,
        t_cover,
        bentLength,
        bentAngle,
        orientation,
        diameter,
        facenormalDirection(structure, facename),
    )
    sketch.movePoint(0, 1, points[0], 0)
    FreeCAD.ActiveDocument.recompute()
    sketch.movePoint(0, 2, points[1], 0)
    FreeCAD.ActiveDocument.recompute()
    sketch.movePoint(1, 1, points[1], 0)
    FreeCAD.ActiveDocument.recompute()
    sketch.movePoint(1, 2, points[2], 0)
    FreeCAD.ActiveDocument.recompute()

    sketch.movePoint(2, 1, points[2], 0)
    FreeCAD.ActiveDocument.recompute()
    sketch.movePoint(2, 2, points[3], 0)
    FreeCAD.ActiveDocument.recompute()
    sketch.movePoint(3, 1, points[3], 0)
    FreeCAD.ActiveDocument.recompute()
    sketch.movePoint(3, 2, points[4], 0)
    FreeCAD.ActiveDocument.recompute()

    sketch.movePoint(4, 1, points[4], 0)
    FreeCAD.ActiveDocument.recompute()
    sketch.movePoint(4, 2, points[5], 0)
    FreeCAD.ActiveDocument.recompute()

    Rebar.OffsetStart = f_cover + diameter / 2
    Rebar.OffsetEnd = f_cover + diameter / 2
    if amount_spacing_check:
        Rebar.Amount = amount_spacing_value
        FreeCAD.ActiveDocument.recompute()
        Rebar.AmountCheck = True
    else:
        size = (
            ArchCommands.projectToVector(
                structure.Shape.copy(), face.normalAt(0, 0)
            )
        ).Length
        Rebar.Amount = get_rebar_amount_from_spacing(
            size, diameter, amount_spacing_value
        )
        FreeCAD.ActiveDocument.recompute()
        Rebar.AmountCheck = False
    Rebar.Diameter = diameter
    Rebar.FrontCover = f_cover
    Rebar.LeftCover = l_cover
    Rebar.RightCover = r_cover
    Rebar.BottomCover = b_cover
    Rebar.TopCover = t_cover
    Rebar.BentLength = bentLength
    Rebar.BentAngle = bentAngle
    Rebar.Rounding = rounding
    Rebar.TrueSpacing = amount_spacing_value
    Rebar.Orientation = orientation
    FreeCAD.ActiveDocument.recompute()
    return Rebar


def editDialog(vobj):
    FreeCADGui.Control.closeDialog()
    obj = _BentShapeRebarTaskPanel(vobj.Object)
    obj.form.frontCover.setText(
        FreeCAD.Units.Quantity(
            vobj.Object.FrontCover, FreeCAD.Units.Length
        ).UserString
    )
    obj.form.l_sideCover.setText(
        FreeCAD.Units.Quantity(
            vobj.Object.LeftCover, FreeCAD.Units.Length
        ).UserString
    )
    obj.form.r_sideCover.setText(
        FreeCAD.Units.Quantity(
            vobj.Object.RightCover, FreeCAD.Units.Length
        ).UserString
    )
    obj.form.bottomCover.setText(
        FreeCAD.Units.Quantity(
            vobj.Object.BottomCover, FreeCAD.Units.Length
        ).UserString
    )
    obj.form.diameter.setText(
        FreeCAD.Units.Quantity(
            vobj.Object.Diameter, FreeCAD.Units.Length
        ).UserString
    )
    obj.form.topCover.setText(
        FreeCAD.Units.Quantity(
            vobj.Object.TopCover, FreeCAD.Units.Length
        ).UserString
    )
    obj.form.bentLength.setText(
        FreeCAD.Units.Quantity(
            vobj.Object.BentLength, FreeCAD.Units.Length
        ).UserString
    )
    obj.form.bentAngle.setValue(vobj.Object.BentAngle)
    obj.form.rounding.setValue(vobj.Object.Rounding)
    obj.form.orientationValue.setCurrentIndex(
        obj.form.orientationValue.findText(str(vobj.Object.Orientation))
    )
    if vobj.Object.AmountCheck:
        obj.form.amount.setValue(vobj.Object.Amount)
    else:
        obj.form.amount_radio.setChecked(False)
        obj.form.spacing_radio.setChecked(True)
        obj.form.amount.setDisabled(True)
        obj.form.spacing.setEnabled(True)
        obj.form.spacing.setText(
            FreeCAD.Units.Quantity(
                vobj.Object.TrueSpacing, FreeCAD.Units.Length
            ).UserString
        )
    # obj.form.PickSelectedFace.setVisible(False)
    FreeCADGui.Control.showDialog(obj)


def CommandBentShapeRebar():
    selected_obj = check_selected_face()
    if selected_obj:
        FreeCADGui.Control.showDialog(_BentShapeRebarTaskPanel())
