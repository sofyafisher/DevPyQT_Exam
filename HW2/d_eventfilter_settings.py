from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QShortcut, QKeySequence

from d_eventfilter_settings_design import Ui_Form

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initSignals()
        QShortcut(QKeySequence(QtCore.Qt.Key.Key_Plus), self, activated = self.Plus)
        QShortcut(QKeySequence(QtCore.Qt.Key.Key_Minus), self, activated = self.Minus)

    def Plus(self):
        self.ui.dial.setValue(self.ui.dial.value() + 1)

    def Minus(self):
        self.ui.dial.setValue(self.ui.dial.value() - 1)

    def initSignals(self):
        self.ui.dial.valueChanged.connect(self.QLCDNumber_Change)
        self.ui.horizontalSlider.valueChanged.connect(self.sliderMove)
        self.ui.comboBox.currentTextChanged.connect(self.onComboBoxChange)

    def QLCDNumber_Change(self):
        self.ui.lcdNumber.display(self.ui.dial.value())
        self.ui.horizontalSlider.setValue(self.ui.dial.value())

    def sliderMove(self):
        self.ui.lcdNumber.display(self.ui.horizontalSlider.value())
        self.ui.dial.setValue(self.ui.horizontalSlider.value())

    def onComboBoxChange(self):
        if self.ui.comboBox.currentText() == 'oct':
            self.ui.lcdNumber.setOctMode()
        elif self.ui.comboBox.currentText() == 'bin':
            self.ui.lcdNumber.setBinMode()
        elif self.ui.comboBox.currentText() == 'hex':
            self.ui.lcdNumber.setHexMode()
        elif self.ui.comboBox.currentText() == 'dec':
            self.ui.lcdNumber.setHexMode()

    def closeEvent (self, event):
        QtCore.QSettings("d_eventfilter_settings").setValue("value", self.ui.horizontalSlider.value())
        QtCore.QSettings("d_eventfilter_settings").setValue("comboBoxMode", self.ui.comboBox.currentText())

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
