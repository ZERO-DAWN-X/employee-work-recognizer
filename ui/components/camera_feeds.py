from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QLabel, QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPainterPath
import qtawesome as qta
import cv2
from ui.style import PADDING, GAP, ACCENT, STATUS_ERROR, STATUS_SUCCESS
from ui.components.card import CardFrame

class CameraFeeds(CardFrame):
    def __init__(self):
        super().__init__()
        self.cap = None
        self.timer = None
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        # Enhanced title with icon
        title_layout = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.video', color=ACCENT).pixmap(20, 20))
        title = QLabel("LIVE CAMERA FEEDS")
        title.setStyleSheet(f'''
            color: #FFFFFF;
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 0.5px;
        ''')
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        # Enhanced video container
        self.video_container = QFrame()
        self.video_container.setStyleSheet(f'''
            background: #0A0E12;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        ''')
        self.video_container.setMinimumSize(360, 240)
        video_grid = QGridLayout(self.video_container)
        video_grid.setContentsMargins(0, 0, 0, 0)
        video_grid.setSpacing(0)
        # Enhanced video border with gradient
        self.video_border = QFrame()
        self.video_border.setStyleSheet(f'''
            background: transparent;
            border: 2px solid {ACCENT};
            border-radius: 16px;
        ''')
        self.video_border.setMinimumSize(340, 220)
        border_layout = QVBoxLayout(self.video_border)
        border_layout.setContentsMargins(0, 0, 0, 0)
        border_layout.setSpacing(0)
        # Enhanced video label
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet(f'''
            background: #000;
            border-radius: 14px;
            color: #9CA3AF;
            font-size: 14px;
        ''')
        self.video_label.setMinimumSize(336, 216)
        border_layout.addWidget(self.video_label)
        video_grid.addWidget(self.video_border, 0, 0, 2, 2, alignment=Qt.AlignCenter)
        # Enhanced status badge with modern design
        self.status_badge = QLabel("● OFFLINE")
        self.status_badge.setStyleSheet(f'''
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {STATUS_ERROR}, stop:1 #DC2626);
            color: white;
            font-weight: 600;
            font-size: 12px;
            padding: 8px 16px;
            border-radius: 16px;
            margin: 16px;
        ''')
        self.status_badge.setFixedHeight(32)
        self.status_badge.setAlignment(Qt.AlignCenter)
        video_grid.addWidget(self.status_badge, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(self.video_container, stretch=1, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.start_camera()
    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.video_label.setText("Camera not available")
            self.status_badge.setText("● OFFLINE")
            self.status_badge.setStyleSheet(f'''
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {STATUS_ERROR}, stop:1 #DC2626);
                color: white;
                font-weight: 600;
                font-size: 12px;
                padding: 8px 16px;
                border-radius: 16px;
                margin: 16px;
            ''')
            return
        self.status_badge.setText("● LIVE")
        self.status_badge.setStyleSheet(f'''
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {STATUS_SUCCESS}, stop:1 #059669);
            color: white;
            font-weight: 600;
            font-size: 12px;
            padding: 8px 16px;
            border-radius: 16px;
            margin: 16px;
        ''')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
    def update_frame(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                # Enhanced rounded corners with better quality
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