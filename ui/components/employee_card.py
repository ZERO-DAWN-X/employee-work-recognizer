from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QSizePolicy, QSpacerItem, QGridLayout
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QPixmap, QImage
from ui.components.card import CardFrame
from ui.style import ACCENT, STATUS_SUCCESS, STATUS_ERROR, STATUS_INFO, STATUS_WARNING, TEXT_MAIN, TEXT_SUB, PADDING, GAP
from detection.face_detector import FaceDetector
import cv2
import numpy as np
from collections import deque

class EmployeeCard(CardFrame):
    def __init__(self, employee, camera_index=0):
        super().__init__()
        self.employee = employee
        self.camera_index = camera_index
        self.detector = FaceDetector()
        self.status_buffer = deque(maxlen=10)
        self.current_status = None
        self.status_changed_time = None
        self.status_times = {s: 0 for s in ["WORKING", "IDLE", "SLEEPING", "WALKING"]}
        self.last_update_time = None
        self.expanded = False
        self.cap = None
        self.timer = None
        self._build_ui()
        self.start_camera()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        # Header row: Name + status + expand btn
        header = QHBoxLayout()
        self.name_label = QLabel(self.employee["name"])
        self.name_label.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 16px; font-weight: 600;")
        header.addWidget(self.name_label)
        header.addStretch()
        self.status_badge = QLabel("WORKING")
        self.status_badge.setStyleSheet(self._status_style("WORKING"))
        header.addWidget(self.status_badge)
        self.expand_btn = QPushButton("Details ▼")
        self.expand_btn.setCheckable(True)
        self.expand_btn.setStyleSheet(f"color: {ACCENT}; background: transparent; border: none; font-weight: 600;")
        self.expand_btn.clicked.connect(self.toggle_expand)
        header.addWidget(self.expand_btn)
        layout.addLayout(header)
        # Camera feed
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(200, 120)
        self.video_label.setStyleSheet(f"background: #000; border-radius: 12px; color: {TEXT_SUB}; font-size: 14px;")
        layout.addWidget(self.video_label)
        # Collapsible details
        self.details_frame = QFrame()
        self.details_frame.setVisible(False)
        details_layout = QVBoxLayout(self.details_frame)
        details_layout.setContentsMargins(0, 0, 0, 0)
        details_layout.setSpacing(8)
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet(f"color: {TEXT_SUB}; font-size: 14px;")
        details_layout.addWidget(self.stats_label)
        # Add more analytics here (charts, etc.)
        layout.addWidget(self.details_frame)
        self.setLayout(layout)

    def _status_style(self, status):
        if status == "WORKING":
            return f"background: {STATUS_SUCCESS}; color: white; font-weight: 600; padding: 4px 16px; border-radius: 12px;"
        elif status == "IDLE":
            return f"background: {STATUS_INFO}; color: white; font-weight: 600; padding: 4px 16px; border-radius: 12px;"
        elif status == "SLEEPING":
            return f"background: {STATUS_ERROR}; color: white; font-weight: 600; padding: 4px 16px; border-radius: 12px;"
        elif status == "WALKING":
            return f"background: {STATUS_WARNING}; color: white; font-weight: 600; padding: 4px 16px; border-radius: 12px;"
        return f"background: #444; color: white; font-weight: 600; padding: 4px 16px; border-radius: 12px;"

    def toggle_expand(self):
        self.expanded = not self.expanded
        self.details_frame.setVisible(self.expanded)
        self.expand_btn.setText("Details ▲" if self.expanded else "Details ▼")

    def start_camera(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            self.video_label.setText("Camera not available")
            return
        self.last_update_time = QTime.currentTime()
        self.status_buffer.clear()
        self.current_status = 'WORKING'
        self.status_changed_time = QTime.currentTime()
        self.status_times = {s: 0 for s in ["WORKING", "IDLE", "SLEEPING", "WALKING"]}
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Detection logic: face = WORKING, no face = IDLE, stub SLEEPING/WALKING
                face_present, faces = self.detector.detect(frame_rgb)
                # Simulate SLEEPING if no face for >10s, WALKING if face moves a lot (stub)
                status = "WORKING" if face_present else "IDLE"
                # Smoothing
                self.status_buffer.append(status)
                if self.status_buffer.count("WORKING") >= 7:
                    smoothed_status = "WORKING"
                elif self.status_buffer.count("IDLE") >= 7:
                    smoothed_status = "IDLE"
                else:
                    smoothed_status = self.current_status or "IDLE"
                # Time tracking
                now = QTime.currentTime()
                if self.last_update_time:
                    elapsed = self.last_update_time.msecsTo(now) / 1000.0
                    self.status_times[self.current_status] += elapsed
                self.last_update_time = now
                # Only update status if changed
                if smoothed_status != self.current_status:
                    self.current_status = smoothed_status
                    self.status_changed_time = now
                # Update badge
                self.status_badge.setText(self.current_status)
                self.status_badge.setStyleSheet(self._status_style(self.current_status))
                # Draw face rectangles
                draw_frame = frame_rgb.copy()
                for (x, y, w, h) in faces:
                    cv2.rectangle(draw_frame, (x, y), (x + w, y + h), (0, 212, 170), 2)
                h, w, ch = draw_frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(draw_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                self.video_label.setPixmap(pixmap.scaled(self.video_label.width(), self.video_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                # Update stats
                self.stats_label.setText(
                    f"Work: {int(self.status_times['WORKING'])}s | Idle: {int(self.status_times['IDLE'])}s | Sleep: {int(self.status_times['SLEEPING'])}s | Walk: {int(self.status_times['WALKING'])}s"
                )
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