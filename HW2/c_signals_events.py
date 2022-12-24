from PySide6 import QtWidgets, QtGui, QtCore
from c_signals_events_design import Ui_Form

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initSignals()

    def initSignals(self):
        self.ui.pushButtonLT.clicked.connect(lambda: self.move(0, 0))
        self.ui.pushButtonRT.clicked.connect(self.moveRT)
        self.ui.pushButtonLB.clicked.connect(self.moveLB)
        self.ui.pushButtonRB.clicked.connect(self.moveRB)
        self.ui.pushButtonCenter.clicked.connect(self.moveCenter)
        self.ui.pushButtonMoveCoords.clicked.connect(self.MoveCoord)
        self.ui.pushButtonGetData.clicked.connect(self.GetData)


    def moveRT(self):
        current_screen = QtWidgets.QApplication.screenAt(self.pos())
        screen_width = current_screen.size().width()
        pos = screen_width - self.width()
        self.move(pos, 0)

    def moveLB(self):
        current_screen = QtWidgets.QApplication.screenAt(self.pos())
        screen_height = current_screen.size().height()
        pos = screen_height - self.height()
        self.move(0, pos)

    def moveRB(self):
        current_screen = QtWidgets.QApplication.screenAt(self.pos())
        screen_height = current_screen.size().height()
        screen_width = current_screen.size().width()
        posw = screen_width - self.width()
        posh = screen_height - self.height()
        self.move(posw, posh)

    def moveCenter(self):
        current_screen = QtWidgets.QApplication.screenAt(self.pos())
        screen_height = current_screen.size().height()
        screen_width = current_screen.size().width()
        posw = screen_width - self.width()
        posh = screen_height - self.height()
        self.move(posw // 2, posh // 2)

    def MoveCoord(self):
        x = int(self.ui.spinBoxX.text())
        y = int(self.ui.spinBoxY.text())
        self.move(x, y)

    def event(self, change):

        if change.type() == QtCore.QEvent.Type.Resize:
            print(f"{QtCore.QDateTime.currentDateTime()} изменен размер окна: {change.size().width()} на {change.size().height()}")

        if change.type() == QtCore.QEvent.Type.Move:
            print(f"{QtCore.QDateTime.currentDateTime()} окно перемещено:\n"
            f"старая позиция: {change.oldPos()}, новая позиция: {change.pos()}")

        return super(Window, self).event(change)

    def GetData(self):
        self.ui.plainTextEdit.setPlainText(
            f"Кол-во экранов: {len(QtGui.QGuiApplication.screens())}\n"
            f"Текущее основное окно: { QtGui.QGuiApplication.applicationDisplayName()}\n"
            f"Окно на экране {self.screen().name()}\n"
            f"Размеры окна: {self.width()} на {self.height()}\n"
            f"Минимальные размеры окна: {self.minimumWidth()} на {self.minimumHeight()}\n"
            f"Текущее положение окна: {self.geometry().getCoords()}\n"
            f"Координаты центра: {self.geometry().center().toTuple()}\n"
            f"Состояние окна: {QtGui.QGuiApplication.applicationState().name}")


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()