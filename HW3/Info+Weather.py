from PySide6 import QtWidgets
from threads import SystemInfo, WeatherHandler

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initThread()
        self.initUi()
        self.initSignals()

    def initSignals (self):
        self.spinBox.valueChanged.connect(self.ImmediateUpdate)
        self.system_info.systemInfoReceived.connect(self.InsertInfo)
        self.pushButton.clicked.connect(self.findWeather)
        self.weatherThread.weatherInfoReceived.connect(self.insertWeather)

    def InsertInfo(self, InfoReceived):
        self.plainTextEditCPU.setPlainText(str(InfoReceived[0]))
        self.plainTextEditRAM.setPlainText(str(InfoReceived[1]))

    def ImmediateUpdate(self):
        self.system_info.delay = self.spinBox.value()

    def initThread(self):
        self.system_info = SystemInfo()
        self.system_info.start()
        self.weatherThread = WeatherHandler()

    def closeEvent (self, event):
        self.system_info.terminate()

    def findWeather(self, status):

        if status:
            latitude = int(self.latitude.text())
            longitude = int(self.longitude.text())
            delay = int(self.spinBox.text())
            self.weatherThread.setCoordinates(latitude, longitude)
            self.weatherThread.setDelay(delay)
            self.weatherThread.start()
            self.spinBox.setEnabled(False)
            self.longitude.setEnabled(False)
            self.latitude.setEnabled(False)
            self.pushButton.setText("Остановить получение данных")
        else:
            self.finishWeatherThread()

    def finishWeatherThread(self):
        self.weatherThread.stop()

        self.pushButton.setText("Узнать погоду")
        self.pushButton.setEnabled(True)
        self.spinBox.setEnabled(True)
        self.longitude.setEnabled(True)
        self.latitude.setEnabled(True)

    def insertWeather(self, data):
        self.plainTextWeather.setPlainText(str(data))

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

        self.longitude = QtWidgets.QSpinBox()
        self.longitude.setMinimum(-180)
        self.longitude.setMaximum(180)

        self.latitude = QtWidgets.QSpinBox()
        self.latitude.setMinimum(-90)
        self.latitude.setMaximum(90)

        self.plainTextWeather = QtWidgets.QPlainTextEdit()
        self.plainTextWeather.setPlaceholderText("Тут будет выведена погода")
        self.pushButton = QtWidgets.QPushButton("Узнать погоду")
        self.pushButton.setCheckable(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.spinBox)
        layout.addWidget(QtWidgets.QLabel("Долгота"))
        layout.addWidget(self.longitude)
        layout.addWidget(QtWidgets.QLabel("Широта"))
        layout.addWidget(self.latitude)
        layout.addWidget(self.plainTextWeather)
        layout.addWidget(self.pushButton)
        layout.addWidget(self.labelCPU)
        layout.addWidget(self.plainTextEditCPU)
        layout.addWidget(self.labelRAM)
        layout.addWidget(self.plainTextEditRAM)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()