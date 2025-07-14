from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QLabel
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPainterPath, QPen
import qtawesome as qta
import cv2
import numpy as np
from collections import deque
from ui.style import PADDING, GAP, ACCENT, STATUS_ERROR, STATUS_SUCCESS, STATUS_INFO, TEXT_MAIN, TEXT_SUB
from ui.components.card import CardFrame
from detection.face_detector import FaceDetector
from random import randint

class CameraFeeds(CardFrame):
    def __init__(self):
        super().__init__()
        self.cap = None
        self.timer = None
        self.detector = FaceDetector()
        self.status_buffer = deque(maxlen=10)  # For smoothing
        self.current_status = None
        self.status_changed_time = None
        self.status_times = {k: 0 for k in ['WORK', 'IDLE', 'SLEEP', 'WALK']}
        self.last_update_time = None
        self.status_update_callback = None
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        # Title + clock
        title_row = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa.video', color=ACCENT).pixmap(20, 20))
        title = QLabel("LIVE CAMERA FEEDS")
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
        self.video_container.setMinimumSize(360, 240)
        video_grid = QGridLayout(self.video_container)
        video_grid.setContentsMargins(0, 0, 0, 0)
        video_grid.setSpacing(0)
        # Video border
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
        # Video label
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
        # Status badge
        self.status_badge = QLabel("● OFFLINE")
        self.status_badge.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {STATUS_ERROR}, stop:1 #DC2626);
            color: white;
            font-weight: 600;
            font-size: 12px;
            padding: 8px 16px;
            border-radius: 16px;
            margin: 16px;
        """)
        self.status_badge.setFixedHeight(32)
        self.status_badge.setAlignment(Qt.AlignCenter)
        video_grid.addWidget(self.status_badge, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)
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
    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.video_label.setText("Camera not available")
            self.status_badge.setText("● OFFLINE")
            self.status_badge.setStyleSheet(f"""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {STATUS_ERROR}, stop:1 #DC2626);
                color: white;
                font-weight: 600;
                font-size: 12px;
                padding: 8px 16px;
                border-radius: 16px;
                margin: 16px;
            """)
            return
        self.status_badge.setText("● WORK")
        self.status_badge.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {STATUS_SUCCESS}, stop:1 #059669);
            color: white;
            font-weight: 600;
            font-size: 12px;
            padding: 8px 16px;
            border-radius: 16px;
            margin: 16px;
        """)
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
                # Detection
                face_present, faces = self.detector.detect(frame_rgb)
                # Simulate SLEEP/WALK (for demo)
                sim_state = None
                if face_present:
                    # 10% chance to be SLEEP, 10% WALK, else WORK
                    r = randint(1, 100)
                    if r <= 10:
                        sim_state = 'SLEEP'
                    elif r <= 20:
                        sim_state = 'WALK'
                    else:
                        sim_state = 'WORK'
                else:
                    sim_state = 'IDLE'
                self.status_buffer.append(sim_state)
                # Smoothing
                smoothed_status = max(set(self.status_buffer), key=self.status_buffer.count)
                # Time tracking
                now = QTime.currentTime()
                if self.last_update_time:
                    elapsed = self.last_update_time.msecsTo(now) / 1000.0
                    if self.current_status:
                        self.status_times[self.current_status] += elapsed
                self.last_update_time = now
                # Only update status if changed
                if smoothed_status != self.current_status:
                    self.current_status = smoothed_status
                    self.status_changed_time = now
                # Update badge (color per status)
                badge_map = {
                    'WORK': ("● WORK", STATUS_SUCCESS, "#059669"),
                    'IDLE': ("● IDLE", STATUS_INFO, "#2563EB"),
                    'SLEEP': ("● SLEEPING", STATUS_WARNING, "#F59E0B"),
                    'WALK': ("● WALKING", ACCENT, "#00D4AA"),
                }
                text, color, grad = badge_map.get(self.current_status, ("● -", ACCENT, ACCENT))
                self.status_badge.setText(text)
                self.status_badge.setStyleSheet(f"""
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {color}, stop:1 {grad});
                    color: white;
                    font-weight: 600;
                    font-size: 12px;
                    padding: 8px 16px;
                    border-radius: 16px;
                    margin: 16px;
                """)
                # Draw face rectangles
                draw_frame = frame_rgb.copy()
                for (x, y, w, h) in faces:
                    cv2.rectangle(draw_frame, (x, y), (x + w, y + h), (0, 212, 170), 2)
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
                # Update status list on dashboard
                if self.status_update_callback:
                    self.status_update_callback(self.status_times.copy(), self.current_status)
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