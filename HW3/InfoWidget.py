from PySide6 import QtWidgets
from threads import SystemInfo

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initThread()
        self.initUi()
        self.initSignals()

    def initUi(self) -> None:
        self.labelspinBox = QtWidgets.QLabel("Время задержки")
        self.spinBox = QtWidgets.QSpinBox()
        self.spinBox.setValue(2)
        self.spinBox.setMinimum(2)

        self.labelCPU = QtWidgets.QLabel("CPU")
        self.plainTextEditCPU = QtWidgets.QPlainTextEdit()
        self.plainTextEditCPU.setMaximumHeight(30)
        self.plainTextEditCPU.setReadOnly(True)

        self.labelRAM = QtWidgets.QLabel("RAM")
        self.plainTextEditRAM = QtWidgets.QPlainTextEdit()
        self.plainTextEditRAM.setMaximumHeight(30)
        self.plainTextEditRAM.setReadOnly(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.spinBox)
        layout.addWidget(self.labelCPU)
        layout.addWidget(self.plainTextEditCPU)
        layout.addWidget(self.labelRAM)
        layout.addWidget(self.plainTextEditRAM)

        self.setLayout(layout)

    def initSignals (self):
        self.spinBox.valueChanged.connect(self.ImmediateUpdate)
        self.system_info.systemInfoReceived.connect(self.InsertInfo)

    def InsertInfo(self, InfoReceived):
        self.plainTextEditCPU.setPlainText(str(InfoReceived[0]))
        self.plainTextEditRAM.setPlainText(str(InfoReceived[1]))

    def ImmediateUpdate(self):
        self.system_info.delay = self.spinBox.value()

    def initThread(self):
        self.system_info = SystemInfo()
        self.system_info.start()

    def closeEvent (self, event):
        self.system_info.terminate()

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()