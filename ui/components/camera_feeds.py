from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QLabel
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPainterPath, QPen
import qtawesome as qta
import cv2
import numpy as np
from collections import deque
from ui.style import PADDING, GAP, ACCENT, STATUS_ERROR, STATUS_SUCCESS, STATUS_INFO, TEXT_MAIN, TEXT_SUB
from ui.components.card import CardFrame
from ui.components.status_card import StatusCard
from detection.face_detector import FaceDetector

class CameraFeeds(CardFrame):
    def __init__(self):
        super().__init__()
        self.cap = None
        self.timer = None
        self.detector = FaceDetector()
        self.status_buffer = deque(maxlen=10)
        self.current_status = None
        self.last_status = None
        self.status_changed_time = None
        self.work_time = 0
        self.idle_time = 0
        self.last_update_time = None
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        # StatusCard (modern, minimal)
        self.status_card = StatusCard()
        layout.addWidget(self.status_card, alignment=Qt.AlignHCenter)
        # Title + clock
        title_row = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.video', color=ACCENT).pixmap(20, 20))
        title = QLabel("LIVE CAMERA FEEDS")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 16px; font-weight: 600; letter-spacing: 0.5px;")
        title_row.addWidget(title_icon)
        title_row.addWidget(title)
        title_row.addStretch()
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
        self.video_container.setMinimumSize(360, 240)
        video_grid = QGridLayout(self.video_container)
        video_grid.setContentsMargins(0, 0, 0, 0)
        video_grid.setSpacing(0)
        self.video_border = QFrame()
        self.video_border.setStyleSheet(f"""
            background: transparent;
            border: 2px solid {ACCENT};
            border-radius: 16px;
        """)
        self.video_border.setMinimumSize(340, 220)
        border_layout = QVBoxLayout(self.video_border)
        border_layout.setContentsMargins(0, 0, 0, 0)
        border_layout.setSpacing(0)
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet(f"""
            background: #000;
            border-radius: 14px;
            color: {TEXT_SUB};
            font-size: 14px;
        """)
        self.video_label.setMinimumSize(336, 216)
        border_layout.addWidget(self.video_label)
        video_grid.addWidget(self.video_border, 0, 0, 2, 2, alignment=Qt.AlignCenter)
        layout.addWidget(self.video_container, stretch=1, alignment=Qt.AlignCenter)
        # Work/Idle time stats
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet(f"color: {TEXT_SUB}; font-size: 14px; font-weight: 500; margin-top: 8px;")
        self.stats_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.stats_label)
        self.setLayout(layout)
        self.start_camera()
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()
    def update_clock(self):
        self.clock_label.setText(QTime.currentTime().toString('hh:mm:ss'))
    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.video_label.setText("Camera not available")
            self.status_card.set_status('IDLE')
            return
        self.last_update_time = QTime.currentTime()
        self.status_buffer.clear()
        self.current_status = 'WORK'
        self.last_status = 'WORK'
        self.status_changed_time = QTime.currentTime()
        self.work_time = 0
        self.idle_time = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
    def update_frame(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_present, faces = self.detector.detect(frame_rgb)
                self.status_buffer.append('WORK' if face_present else 'IDLE')
                if self.status_buffer.count('WORK') >= 7:
                    smoothed_status = 'WORK'
                elif self.status_buffer.count('IDLE') >= 7:
                    smoothed_status = 'IDLE'
                else:
                    smoothed_status = self.current_status or 'IDLE'
                now = QTime.currentTime()
                if self.last_update_time:
                    elapsed = self.last_update_time.msecsTo(now) / 1000.0
                    if self.current_status == 'WORK':
                        self.work_time += elapsed
                    elif self.current_status == 'IDLE':
                        self.idle_time += elapsed
                self.last_update_time = now
                if smoothed_status != self.current_status:
                    self.current_status = smoothed_status
                    self.status_changed_time = now
                self.status_card.set_status(self.current_status)
                draw_frame = frame_rgb.copy()
                for (x, y, w, h) in faces:
                    cv2.rectangle(draw_frame, (x, y), (x + w, y + h), (0, 212, 170), 2)
                h, w, ch = draw_frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(draw_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
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
                self.stats_label.setText(f"Work: {int(self.work_time)}s   |   Idle: {int(self.idle_time)}s")
            else:
                self.video_label.setText("Stream error")
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