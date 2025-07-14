import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2

class WebcamWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Work Time Recognizer")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background: #f7f7f7; font-family: Arial; color: #222;")

        self.layout = QVBoxLayout()
        self.header = QLabel("<h2>Employee Work Time Recognizer</h2>")
        self.header.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.header)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border-radius: 12px; background: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.07);")
        self.layout.addWidget(self.image_label, stretch=1)

        self.button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Webcam")
        self.stop_button = QPushButton("Stop Webcam")
        self.stop_button.setEnabled(False)
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.start_button.clicked.connect(self.start_webcam)
        self.stop_button.clicked.connect(self.stop_webcam)

    def start_webcam(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.header.setText("<h2 style='color:red;'>Error: Could not open webcam.</h2>")
            return
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.timer.start(30)

    def stop_webcam(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.image_label.clear()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_frame(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                self.image_label.setPixmap(pixmap.scaled(
                    self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.stop_webcam()
                self.header.setText("<h2 style='color:red;'>Error: Failed to capture frame.</h2>")

    def closeEvent(self, event):
        self.stop_webcam()
        event.accept()

def run_app():
    app = QApplication(sys.argv)
    window = WebcamWidget()
    window.show()
    sys.exit(app.exec_()) 