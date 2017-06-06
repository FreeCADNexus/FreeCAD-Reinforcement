from PySide import QtCore, QtGui
import Arch

class _StraightRebarTaskPanel:
    def __init__(self):
        self.form = FreeCADGui.PySideUic.loadUi("<path_of_StraightRebar.ui_file>")
        self.form.amount_radio.clicked.connect(self.amount_radio_clicked)
        self.form.spacing_radio.clicked.connect(self.spacing_radio_clicked)
        QtCore.QObject.connect(self.form.submit, QtCore.SIGNAL("clicked()"), self.accept)

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Close)

    def accept(self):
        try:
            f_cover = self.form.frontCover.text()
            f_cover = FreeCAD.Units.Quantity(f_cover).Value
            b_cover = self.form.bottomCover.text()
            b_cover = FreeCAD.Units.Quantity(b_cover).Value
            s_cover = self.form.sideCover.text()
            s_cover = FreeCAD.Units.Quantity(s_cover).Value
            diameter = self.form.diameter.value()
            amount_check = self.form.amount_radio.isChecked()
            spacing_check = self.form.spacing_radio.isChecked()
            if amount_check == True:
                amount = self.form.amount.value()
                makeStraightRebar(f_cover, b_cover, s_cover, diameter, True, amount)
            elif spacing_check == True:
                spacing = self.form.spacing.text()
                spacing = FreeCAD.Units.Quantity(spacing).Value
                makeStraightRebar(f_cover, b_cover, s_cover, diameter, False, spacing)
            FreeCAD.Console.PrintMessage("Done!\n")
            self.form.hide()
        except Exception as e: FreeCAD.Console.PrintMessage(str(e)+"\n")

    def amount_radio_clicked(self):
        self.form.spacing.setEnabled(False)
        self.form.amount.setEnabled(True)

    def spacing_radio_clicked(self):
        self.form.amount.setEnabled(False)
        self.form.spacing.setEnabled(True)


def makeStraightRebar(f_cover, b_cover, s_cover, diameter, amount_spacing_check, amount_spacing_value):
    """makeStraightRebar(f_cover, b_cover, s_cover, diameter, amount_spacing_check, amount_spacing_value):
    Adds the straight reinforcement bar to the selected structural object"""
    try:
        selected_obj = FreeCADGui.Selection.getSelectionEx()[0]
        selected_face = selected_obj.SubObjects[0]
        normal = selected_face.normalAt(0,0)
        normal = selected_face.Placement.Rotation.inverted().multVec(normal)
        center_of_mass = selected_face.CenterOfMass
        # Set length and width of user selected face of structural element
        flag = True
        for i in range(len(normal)):
            if round(normal[i]) == 0:
                if flag and i == 0:
                    x = center_of_mass[i]
                    length = selected_obj.Object.Length.Value
                    flag = False
                elif flag and i == 1:
                    x = center_of_mass[i]
                    length = selected_obj.Object.Width.Value
                    flag = False
                if i == 1:
                    y = center_of_mass[i]
                    width = selected_obj.Object.Width.Value
                elif i == 2:
                    y = center_of_mass[i]
                    width = selected_obj.Object.Height.Value
        sketch = FreeCAD.activeDocument().addObject('Sketcher::SketchObject','Sketch')
        sketch.MapMode = "FlatFace"
        # Calculate the start and end points for staight line (x1, y2) and (x2, y2)
        x1 = x - length/2 + s_cover
        y1 = y - width/2 + b_cover
        x2 = x - length/2 + length - s_cover
        y2 = y - width/2 + b_cover
        sketch.Support = [(selected_obj.Object, selected_obj.SubElementNames[0])]
        sketch.addGeometry(Part.LineSegment(App.Vector(x1, y1, 0), App.Vector(x2, y2, 0)), False)
        if amount_spacing_check == True:
            structure = Arch.makeRebar(selected_obj.Object, sketch, diameter, amount_spacing_value, f_cover)
        else:
            structure = Arch.makeRebar(selected_obj.Object, sketch, diameter, int((width-diameter)/amount_spacing_value), f_cover)
        FreeCAD.ActiveDocument.recompute()
    except Exception as e: FreeCAD.Console.PrintMessage(str(e)+"\n")

if FreeCAD.GuiUp:
    FreeCADGui.Control.showDialog(_StraightRebarTaskPanel())
