from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class QDoubleButton(QPushButton):
    shortPressed = pyqtSignal()
    longPressed = pyqtSignal()
    
    def __init__(self, parent):
        super().__init__(parent)
        self._pressedTime = 0
        self._longPressTime = 0.5
        self.pressed.connect(self.handlePressed)
        self.released.connect(self.handleReleased)
        self.labelLayout = QVBoxLayout()
        self.labels = (QLabel(self), QLabel(self))
        self.labels[0].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.labels[1].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        MainWidget.mainSC.redrawStyleSignal.connect(lambda: self.labels[0].setStyleSheet(STYLE.get("BTN_LABEL_MAIN")))
        MainWidget.mainSC.redrawStyleSignal.connect(lambda: self.labels[1].setStyleSheet(STYLE.get("BTN_LABEL_SECONDARY")))
        self.labelLayout.addStretch()
        self.labelLayout.addWidget(self.labels[0])
        self.labelLayout.addWidget(self.labels[1])
        self.labelLayout.addStretch()
        self.setLayout(self.labelLayout)
        self.highlight(0)
    
    def highlight(self, index):
        self.labels[index].setStyleSheet(STYLE.get("BTN_LABEL_MAIN"))
        self.labels[1 - index].setStyleSheet(STYLE.get("BTN_LABEL_SECONDARY"))
        self.labels[0].adjustSize()
        self.labels[1].adjustSize()
    
    def setText(self, index, text):
        self.labels[index].setText(text)
        self.labels[index].adjustSize()
    
    def text(self, index):
        return self.labels[index].text()
    
    def setLongPressTime(self, lptime):
        self._longPressTime = lptime
    
    def longPressTime(self):
        return self._longPressTime
    
    def handlePressed(self):
        self._pressedTime = time.time()
        QTimer.singleShot(int(self._longPressTime * 1000), lambda: self.highlight(1) if self.isDown() else None)
    
    def handleReleased(self):
        self.highlight(0)
        dt = time.time() - self._pressedTime
        if dt >= self._longPressTime and self.hasLongAction():
            self.longPressed.emit()
        else:
            self.shortPressed.emit()
    
    def hasLongAction(self):
        return self.receivers(self.longPressed) > 0


class QHoldableButton(QPushButton):
    held = pyqtSignal()
    
    def __init__(self, parent):
        super().__init__(parent)
        self._longPressTime = 0.5
        self._timerInterval = 0.1
        self.pressed.connect(self.handlePressed)
        self.labelLayout = QVBoxLayout()
        self.timerSingle = QTimer(self)
        self.timerSingle.setInterval(int(self._longPressTime * 1000))
        self.timerSingle.setSingleShot(True)
        self.timerSingle.timeout.connect(self.startLoopTimer)
        self.timerLoop = QTimer(self)
        self.timerLoop.setSingleShot(False)
        self.timerLoop.setInterval(int(self._timerInterval * 1000))
        self.timerLoop.timeout.connect(self.timerTick)
    
    def setLongPressTime(self, lptime):
        self._longPressTime = lptime
        self.timerSingle.setInterval(int(self._longPressTime * 1000))
    
    def longPressTime(self):
        return self._longPressTime
    
    def setTimerInterval(self, tinterval):
        self._timerInterval = tinterval
        self.timerLoop.setInterval(int(self._timerInterval * 1000))
    
    def timerInterval(self):
        return self._timerInterval
    
    def handlePressed(self):
        self.timerSingle.start()
    
    def handleReleased(self):
        self.timerSingle.stop()
        self.timerLoop.stop()
    
    def startLoopTimer(self):
        if not self.isDown():
            return
        self.timerLoop.start()
    
    def timerTick(self):
        if not self.isDown():
            self.timerSingle.stop()
            self.timerLoop.stop()
            return
        self.held.emit()    