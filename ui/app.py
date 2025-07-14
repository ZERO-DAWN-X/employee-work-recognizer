import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
import cv2

# --- Color Palette ---
DARK_BG = "#181C20"
SIDEBAR_BG = "#20242A"
CARD_BG = "#23272E"
ACCENT = "#3DE1C9"
TEXT_MAIN = "#F5F6FA"
TEXT_SUB = "#A0A4AB"
BAR_WORK = "#3DE1C9"
BAR_IDLE = "#4A90E2"
BAR_EAT = "#F5A623"
BAR_SLEEP = "#9B59B6"

class Sidebar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(60)
        self.setStyleSheet(f"background: {SIDEBAR_BG}; border: none;")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        # Placeholder icons (use QLabel for now)
        for icon in ["🏠", "👤", "📊", "⚙️"]:
            lbl = QLabel(icon)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f"color: {ACCENT}; font-size: 22px;")
            layout.addWidget(lbl)
        layout.addStretch()
        self.setLayout(layout)

class TopBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(48)
        self.setStyleSheet(f"background: {DARK_BG}; border: none;")
        layout = QHBoxLayout()
        title = QLabel("AI-POWERED EMPLOYEE MONITORING")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 16px; font-weight: bold;")
        company = QLabel("ZERO-DAWN-X")
        company.setStyleSheet(f"color: {ACCENT}; font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(company)
        self.setLayout(layout)

class CameraFeeds(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {CARD_BG}; border-radius: 12px;")
        layout = QHBoxLayout()
        # Placeholder camera feeds
        for label, activity in [("/public/Office Monitoring.png", "WORKING"), ("/public/Office Surveillance-1.png", "IDLE")]:
            vbox = QVBoxLayout()
            img = QLabel()
            pix = QPixmap(label)
            img.setPixmap(pix.scaled(180, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            img.setAlignment(Qt.AlignCenter)
            vbox.addWidget(img)
            act = QLabel(activity)
            act.setStyleSheet(f"color: {ACCENT}; font-size: 13px; font-weight: bold;")
            act.setAlignment(Qt.AlignCenter)
            vbox.addWidget(act)
            layout.addLayout(vbox)
        self.setLayout(layout)

class ActivityDetection(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {CARD_BG}; border-radius: 12px;")
        layout = QVBoxLayout()
        title = QLabel("ACTIVITY DETECTION")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 13px; font-weight: bold;")
        layout.addWidget(title)
        # Activity bars
        for label, percent, color in [
            ("WORKING", 58, BAR_WORK),
            ("IDLE", 20, BAR_IDLE),
            ("EATING", 15, BAR_EAT),
            ("SLEEPING", 7, BAR_SLEEP)
        ]:
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet(f"color: {TEXT_SUB}; font-size: 12px;")
            bar = QFrame()
            bar.setFixedHeight(8)
            bar.setFixedWidth(percent * 2)
            bar.setStyleSheet(f"background: {color}; border-radius: 4px;")
            pct = QLabel(f"{percent}%")
            pct.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 12px;")
            row.addWidget(lbl, 2)
            row.addWidget(bar, 5)
            row.addWidget(pct, 1)
            layout.addLayout(row)
        self.setLayout(layout)

class AnalyticsCard(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {CARD_BG}; border-radius: 12px;")
        layout = QVBoxLayout()
        title = QLabel("REAL-TIME ANALYTICS")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 13px; font-weight: bold;")
        layout.addWidget(title)
        # Placeholder stats
        stats = QHBoxLayout()
        for label, value in [("ACTIVE", "59%"), ("IDLE", "12%"), ("AVERAGE ACTIVITY", "4h 52m")]:
            vbox = QVBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet(f"color: {TEXT_SUB}; font-size: 11px;")
            val = QLabel(value)
            val.setStyleSheet(f"color: {ACCENT}; font-size: 18px; font-weight: bold;")
            vbox.addWidget(lbl)
            vbox.addWidget(val)
            stats.addLayout(vbox)
        layout.addLayout(stats)
        # Placeholder for graph
        graph = QLabel()
        graph.setFixedHeight(40)
        graph.setStyleSheet(f"background: #222; border-radius: 8px;")
        layout.addWidget(graph)
        self.setLayout(layout)

class TimelineCard(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {CARD_BG}; border-radius: 12px;")
        layout = QVBoxLayout()
        title = QLabel("TIMELINE")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 13px; font-weight: bold;")
        layout.addWidget(title)
        # Placeholder for timeline bar
        timeline = QLabel()
        timeline.setFixedHeight(24)
        timeline.setStyleSheet(f"background: #222; border-radius: 8px;")
        layout.addWidget(timeline)
        # Placeholder for active users graph
        users = QLabel()
        users.setFixedHeight(32)
        users.setStyleSheet(f"background: #222; border-radius: 8px;")
        layout.addWidget(users)
        self.setLayout(layout)

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {DARK_BG};")
        main_layout = QHBoxLayout(self)
        # Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        # Main content
        content = QVBoxLayout()
        self.topbar = TopBar()
        content.addWidget(self.topbar)
        # Dashboard grid
        grid = QGridLayout()
        grid.setSpacing(16)
        # Live camera feeds
        self.cameras = CameraFeeds()
        grid.addWidget(self.cameras, 0, 0, 2, 2)
        # Activity detection
        self.activity = ActivityDetection()
        grid.addWidget(self.activity, 0, 2, 1, 1)
        # Analytics
        self.analytics = AnalyticsCard()
        grid.addWidget(self.analytics, 1, 2, 1, 1)
        # Timeline
        self.timeline = TimelineCard()
        grid.addWidget(self.timeline, 2, 0, 1, 3)
        content.addLayout(grid)
        main_layout.addLayout(content)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Work Time Recognizer")
        self.setMinimumSize(1000, 700)
        self.setCentralWidget(Dashboard())
        self.setStyleSheet(f"background: {DARK_BG};")

def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 