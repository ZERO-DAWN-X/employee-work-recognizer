from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QLabel
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPainterPath, QColor
import qtawesome as qta
import cv2
import numpy as np
from collections import deque
from ui.style import PADDING, GAP, ACCENT, TEXT_MAIN, TEXT_SUB, STATUS_SUCCESS, STATUS_INFO, STATUS_ERROR, STATUS_WARNING
from ui.components.card import CardFrame
from detection.face_detector import FaceDetector

STATUS_COLORS = {
    "WORKING": STATUS_SUCCESS,
    "IDLE": STATUS_INFO,
    "SLEEPING": STATUS_ERROR,
    "WALKING": STATUS_WARNING,
}

class CameraFeeds(CardFrame):
    def __init__(self):
        super().__init__()
        self.cap = None
        self.timer = None
        self.detector = FaceDetector()
        self.last_faces = []
        self.face_buffer = deque(maxlen=5)  # Smoothing buffer for faces
        self.employee_statuses = None  # To be set externally
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        # Title + clock
        title_row = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.video', color=ACCENT).pixmap(20, 20))
        title = QLabel("OFFICE CAMERA FEED")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 16px; font-weight: 600; letter-spacing: 0.5px;")
        title_row.addWidget(title_icon)
        title_row.addWidget(title)
        title_row.addStretch()
        # Live clock
        self.clock_label = QLabel()
        self.clock_label.setStyleSheet(f"color: {TEXT_SUB}; font-size: 15px; font-weight: 500;")
        self.clock_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        title_row.addWidget(self.clock_label)
        layout.addLayout(title_row)
        # Video container
        self.video_container = QFrame()
        self.video_container.setStyleSheet(f"""
            background: #0A0E12;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        """)
        self.video_container.setMinimumSize(480, 320)
        video_grid = QGridLayout(self.video_container)
        video_grid.setContentsMargins(0, 0, 0, 0)
        video_grid.setSpacing(0)
        # Video label
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet(f"background: #000; border-radius: 14px; color: {TEXT_SUB}; font-size: 14px;")
        self.video_label.setMinimumSize(460, 300)
        video_grid.addWidget(self.video_label, 0, 0, alignment=Qt.AlignCenter)
        layout.addWidget(self.video_container, stretch=1, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.start_camera()
        # Start clock timer
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()

    def update_clock(self):
        self.clock_label.setText(QTime.currentTime().toString('hh:mm:ss'))

    def set_employee_statuses(self, statuses):
        self.employee_statuses = statuses

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.video_label.setText("Camera not available")
            return
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Detect all faces
                _, faces = self.detector.detect(frame_rgb)
                self.face_buffer.append(faces)
                # Smoothing: use the most common set of faces in the buffer
                faces_smoothed = self._smooth_faces()
                self.last_faces = faces_smoothed
                # Draw rectangles for each face, colored by status if available
                draw_frame = frame_rgb.copy()
                for i, (x, y, w, h) in enumerate(faces_smoothed):
                    status = None
                    color = (0, 212, 170)
                    if self.employee_statuses and i < len(self.employee_statuses):
                        status = self.employee_statuses[i]
                        color_hex = STATUS_COLORS.get(status, STATUS_INFO)
                        color = QColor(color_hex)
                        color = (color.red(), color.green(), color.blue())
                    cv2.rectangle(draw_frame, (x, y), (x + w, y + h), color, 2)
                    label = status if status else f"Person {i+1}"
                    cv2.putText(draw_frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                h, w, ch = draw_frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(draw_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                # Enhanced rounded corners
                radius = 14
                rounded = QPixmap(pixmap.size())
                rounded.fill(Qt.transparent)
                painter = QPainter(rounded)
                painter.setRenderHint(QPainter.Antialiasing, True)
                painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
                path = QPainterPath()
                path.addRoundedRect(0, 0, pixmap.width(), pixmap.height(), radius, radius)
                painter.setClipPath(path)
                painter.drawPixmap(0, 0, pixmap)
                painter.end()
                self.video_label.setPixmap(rounded.scaled(
                    self.video_label.width(), self.video_label.height(), 
                    Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.video_label.setText("Stream error")

    def _smooth_faces(self):
        # Use the most common face set in the buffer, or the last one
        if not self.face_buffer:
            return []
        # For simplicity, use the last faces (could be improved with tracking)
        return self.face_buffer[-1]

    def get_latest_faces(self):
        return self.last_faces

    def stop_camera(self):
        if self.timer:
            self.timer.stop()
            self.timer = None
        if self.cap:
            self.cap.release()
            self.cap = None
    def closeEvent(self, event):
        self.stop_camera()
        event.accept() 