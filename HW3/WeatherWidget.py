from PySide6 import QtWidgets
from threads import WeatherHandler

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initThread()
        self.initUi()
        self.initSignals()

    def initSignals(self):
        self.pushButton.clicked.connect(self.findWeather)
        self.weatherThread.weatherInfoReceived.connect(self.insertWeather)

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

    def initThread(self):
        self.weatherThread = WeatherHandler()

    def initUi(self) -> None:

        self.spinBox = QtWidgets.QSpinBox()
        self.spinBox.setValue(2)
        self.spinBox.setMinimum(2)

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

        self.setLayout(layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()