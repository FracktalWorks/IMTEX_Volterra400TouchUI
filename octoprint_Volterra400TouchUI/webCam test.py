import sys
import cv2
import time
from PyQt4 import QtGui, QtCore, uic


import sys

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class videoThread(QtCore.QThread):
    # Requires IP address of streaming server
    def __init__(self,address):
        super(videoThread,self).__init__()
        self.ip = address

    def run(self):
        # Create a capture object using the IP address specified at init.
        cap = cv2.VideoCapture("http://"+ str(self.ip) +
            "/webcam/?action=stream?dummy=param.mjpg")
        while cap.isOpened():
            ret, frame = cap.read()
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(frame)
            image = QtGui.QImage(frame.tostring(), w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
            self.emit(QtCore.SIGNAL('newImage(QImage)'), image)
            print "emmited"

            #
            # pixmap = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
            # # pix = QtGui.QPixmap.fromImage(pixmap)
            # self.emit(QtCore.SIGNAL('newImage(QImage)'), pixmap)


class MyWindow(QtGui.QMainWindow):

    def __init__(self,template):
        super(MyWindow,self).__init__()
        uic.loadUi(template,self)
        self.video = videoThread("192.168.2.152")
        self.video.start()
        self.connect(self.video,QtCore.SIGNAL('newImage(QImage)'),self.setFrame)
        self.statusBar().hide()

    def setFrame(self,frame):
        #pixmap = QtGui.QPixmap.fromImage(frame)
        self.label.setPixmap(frame)

if __name__ == '__main__':
        app = QtGui.QApplication(sys.argv)
        window = MyWindow('template.ui')
        #window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        window.show()
sys.exit(app.exec_())