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

__title__ = "RebarCommands"
__author__ = "Amritpal Singh"
__url__ = "https://www.freecadweb.org"

from PySide.QtCore import QT_TRANSLATE_NOOP
import FreeCADGui
import os


class StraightRebarTool:
    def GetResources(self):
        return {
            "Pixmap": os.path.split(os.path.abspath(__file__))[0]
            + "/icons/dropdown_list/StraightRebar.svg",
            "MenuText": QT_TRANSLATE_NOOP(
                "Arch_Rebar_Straight", "Straight Rebar"
            ),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Rebar_Straight",
                "Creates a Striaght bar reinforcement from the selected face of"
                " the Structural element.",
            ),
        }

    def IsActive(self):
        return True if FreeCADGui.activeDocument() else False

    def Activated(self):
        import StraightRebar

        # Call to CommandStraightRebar() function
        StraightRebar.CommandStraightRebar()


class UShapeRebarTool:
    def GetResources(self):
        return {
            "Pixmap": os.path.split(os.path.abspath(__file__))[0]
            + "/icons/dropdown_list/UShapeRebar.svg",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Rebar_UShape", "U-Shape Rebar"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Rebar_UShape",
                "Creates a U-Shape bar reinforcement from the selected face of "
                "the Structural element.",
            ),
        }

    def IsActive(self):
        return True if FreeCADGui.activeDocument() else False

    def Activated(self):
        import UShapeRebar

        # Call to CommandUShaepRebar() function
        UShapeRebar.CommandUShapeRebar()


class LShapeRebarTool:
    def GetResources(self):
        return {
            "Pixmap": os.path.split(os.path.abspath(__file__))[0]
            + "/icons/dropdown_list/LShapeRebar.svg",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Rebar_LShape", "L-Shape Rebar"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Rebar_LShape",
                "Creates a L-Shape bar reinforcement from the selected face of "
                "the Structural element.",
            ),
        }

    def IsActive(self):
        return True if FreeCADGui.activeDocument() else False

    def Activated(self):
        import LShapeRebar

        # Call to CommandUShaepRebar() function
        LShapeRebar.CommandLShapeRebar()


class StirrupTool:
    def GetResources(self):
        return {
            "Pixmap": os.path.split(os.path.abspath(__file__))[0]
            + "/icons/dropdown_list/StirrupRebar.svg",
            "MenuText": QT_TRANSLATE_NOOP("Arch_Rebar_Stirrup", "Stirrup"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Rebar_Stirrup",
                "Creates a Stirrup bar reinforcement from the selected face of "
                "the Structural element.",
            ),
        }

    def IsActive(self):
        return True if FreeCADGui.activeDocument() else False

    def Activated(self):
        import Stirrup

        # Call to CommandStirrup() function
        Stirrup.CommandStirrup()


class BentShapeRebarTool:
    def GetResources(self):
        return {
            "Pixmap": os.path.split(os.path.abspath(__file__))[0]
            + "/icons/dropdown_list/BentShapeRebar.svg",
            "MenuText": QT_TRANSLATE_NOOP(
                "Arch_Rebar_BentShape", "Bent-Shape Rebar"
            ),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Rebar_BentShape",
                "Creates a BentShape bar reinforcement from the selected face "
                "of the Structural element.",
            ),
        }

    def IsActive(self):
        return True if FreeCADGui.activeDocument() else False

    def Activated(self):
        import BentShapeRebar

        # Call to CommandBentShaepRebar() function
        BentShapeRebar.CommandBentShapeRebar()


class HelicalRebarTool:
    def GetResources(self):
        return {
            "Pixmap": os.path.split(os.path.abspath(__file__))[0]
            + "/icons/dropdown_list/HelixShapeRebar.svg",
            "MenuText": QT_TRANSLATE_NOOP(
                "Arch_Rebar_Helical", "Helical Rebar"
            ),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Rebar_Helical",
                "Creates a Helical bar reinforcement from the selected face of "
                "the Structural element.",
            ),
        }

    def IsActive(self):
        return True if FreeCADGui.activeDocument() else False

    def Activated(self):
        import HelicalRebar

        # Call to CommandHelicalRebar() function
        HelicalRebar.CommandHelicalRebar()


class ColumnReinforcementTool:
    def GetResources(self):
        return {
            "Pixmap": os.path.split(os.path.abspath(__file__))[0]
            + "/icons/dropdown_list/Column.svg",
            "MenuText": QT_TRANSLATE_NOOP(
                "Arch_Column_Reinforcement", "Column Reinforcement"
            ),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Column_Reinforcement",
                "Creates a Column Reinforcement from the selected face of the "
                "Structural element.",
            ),
        }

    def IsActive(self):
        return True if FreeCADGui.activeDocument() else False

    def Activated(self):
        from ColumnReinforcement import MainColumnReinforcement

        # Call to CommandColumnReinforcement() function
        MainColumnReinforcement.CommandColumnReinforcement()


class BeamReinforcementTool:
    def GetResources(self):
        return {
            "Pixmap": os.path.split(os.path.abspath(__file__))[0]
            + "/icons/dropdown_list/Beam.svg",
            "MenuText": QT_TRANSLATE_NOOP(
                "Arch_Beam_Reinforcement", "Beam Reinforcement"
            ),
            "ToolTip": QT_TRANSLATE_NOOP(
                "Arch_Beam_Reinforcement",
                "Creates a Beam Reinforcement from the selected face of the "
                "Structural element.",
            ),
        }

    def IsActive(self):
        return True if FreeCADGui.activeDocument() else False

    def Activated(self):
        from BeamReinforcement import MainBeamReinforcement

        # Call to CommandBeamReinforcement() function
        MainBeamReinforcement.CommandBeamReinforcement()


class BillOfMaterialTool:
    def GetResources(self):
        return {
            "Pixmap": os.path.split(os.path.abspath(__file__))[0]
            + "/icons/dropdown_list/BOM.svg",
            "MenuText": QT_TRANSLATE_NOOP(
                "RebarAddon", "Rebar Bill Of Material"
            ),
            "ToolTip": QT_TRANSLATE_NOOP(
                "RebarAddon", "Generate Rebars Bill Of Material",
            ),
        }

    def IsActive(self):
        return True if FreeCADGui.activeDocument() else False

    def Activated(self):
        from BillOfMaterial import MainBillOfMaterial

        # Call to CommandBillOfMaterial() function
        MainBillOfMaterial.CommandBillOfMaterial()


class RebarShapeCutListTool:
    @staticmethod
    def GetResources():
        return {
            "Pixmap": os.path.split(os.path.abspath(__file__))[0]
            + "/icons/dropdown_list/RebarShapeCutList.svg",
            "MenuText": QT_TRANSLATE_NOOP("RebarAddon", "Rebar Shape Cut List"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "RebarAddon", "Generate Rebar Shape Cut List",
            ),
        }

    @staticmethod
    def IsActive():
        return True if FreeCADGui.activeDocument() else False

    @staticmethod
    def Activated():
        from RebarShapeCutList import MainRebarShapeCutList

        # Call to CommandRebarShapeCutList() function
        MainRebarShapeCutList.CommandRebarShapeCutList()


class BarBendingScheduleTool:
    @staticmethod
    def GetResources():
        return {
            "Pixmap": os.path.split(os.path.abspath(__file__))[0]
            + "/icons/dropdown_list/BarBendingSchedule.svg",
            "MenuText": QT_TRANSLATE_NOOP("RebarAddon", "Bar Bending Schedule"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "RebarAddon", "Generate Bar Bending Schedule",
            ),
        }

    @staticmethod
    def IsActive():
        return True if FreeCADGui.activeDocument() else False

    @staticmethod
    def Activated():
        from BarBendingSchedule import MainBarBendingSchedule

        # Call to CommandBarBendingSchedule() function
        MainBarBendingSchedule.CommandBarBendingSchedule()


def updateLocale():
    FreeCADGui.addLanguagePath(
        os.path.join(os.path.dirname(__file__), "translations")
    )
    FreeCADGui.updateLocale()


FreeCADGui.addCommand("Arch_Rebar_Straight", StraightRebarTool())
FreeCADGui.addCommand("Arch_Rebar_UShape", UShapeRebarTool())
FreeCADGui.addCommand("Arch_Rebar_LShape", LShapeRebarTool())
FreeCADGui.addCommand("Arch_Rebar_Stirrup", StirrupTool())
FreeCADGui.addCommand("Arch_Rebar_BentShape", BentShapeRebarTool())
FreeCADGui.addCommand("Arch_Rebar_Helical", HelicalRebarTool())
FreeCADGui.addCommand("Arch_Column_Reinforcement", ColumnReinforcementTool())
FreeCADGui.addCommand("Arch_Beam_Reinforcement", BeamReinforcementTool())
FreeCADGui.addCommand("Arch_Rebar_BOM", BillOfMaterialTool())
FreeCADGui.addCommand("Arch_Rebar_Shape_Cut_List", RebarShapeCutListTool())
FreeCADGui.addCommand(
    "Arch_Rebar_Bar_Bending_Schedule", BarBendingScheduleTool()
)


# List of all rebar commands
RebarCommands = [
    "Arch_Rebar_Straight",
    "Arch_Rebar_UShape",
    "Arch_Rebar_LShape",
    "Arch_Rebar_Stirrup",
    "Arch_Rebar_BentShape",
    "Arch_Rebar_Helical",
    "Arch_Column_Reinforcement",
    "Arch_Beam_Reinforcement",
    "Arch_Rebar_BOM",
    "Arch_Rebar_Shape_Cut_List",
    "Arch_Rebar_Bar_Bending_Schedule",
]
