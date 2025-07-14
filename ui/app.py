import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import qtawesome as qta

DARK_BG = "#181C20"
SIDEBAR_BG = "#20242A"
CARD_BG = "#23272E"
ACCENT = "#3DE1C9"
TEXT_MAIN = "#F5F6FA"
TEXT_SUB = "#A0A4AB"
SHADOW = "0px 4px 24px rgba(0,0,0,0.18)"
BAR_WORK = "#3DE1C9"
BAR_IDLE = "#4A90E2"
BAR_EAT = "#F5A623"
BAR_SLEEP = "#9B59B6"
ICON_SIZE = 28

class Sidebar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(60)
        self.setStyleSheet(f"background: {SIDEBAR_BG}; border: none; border-radius: 16px; box-shadow: {SHADOW};")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        icons = [
            qta.icon('fa5s.tachometer-alt', color=TEXT_MAIN),  # Dashboard
            qta.icon('fa5s.users', color=TEXT_MAIN),           # Users
            qta.icon('fa5s.chart-line', color=TEXT_MAIN),      # Analytics
            qta.icon('fa5s.cog', color=TEXT_MAIN)              # Settings
        ]
        for icon in icons:
            icon_label = QLabel()
            icon_label.setPixmap(icon.pixmap(ICON_SIZE, ICON_SIZE))
            icon_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(icon_label, alignment=Qt.AlignHCenter)
            layout.addSpacing(8)
        layout.addStretch()
        self.setLayout(layout)

class TopBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(48)
        self.setStyleSheet(f"background: {DARK_BG}; border: none;")
        layout = QHBoxLayout()
        title = QLabel("AI-POWERED EMPLOYEE MONITORING")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 16px; font-weight: bold; letter-spacing: 1px;")
        company = QLabel("ZERO-DAWN-X")
        company.setStyleSheet(f"color: {ACCENT}; font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(company)
        self.setLayout(layout)

class CardFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {CARD_BG}; border-radius: 16px; box-shadow: {SHADOW};")

class CameraFeeds(CardFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("LIVE CAMERA FEEDS")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 13px; font-weight: bold;")
        layout.addWidget(title)
        empty = QLabel("No data available")
        empty.setStyleSheet(f"color: {TEXT_SUB}; font-size: 14px;")
        empty.setAlignment(Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(empty)
        layout.addStretch()
        self.setLayout(layout)

class ActivityDetection(CardFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("ACTIVITY DETECTION")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 13px; font-weight: bold;")
        layout.addWidget(title)
        empty = QLabel("No data available")
        empty.setStyleSheet(f"color: {TEXT_SUB}; font-size: 14px;")
        empty.setAlignment(Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(empty)
        layout.addStretch()
        self.setLayout(layout)

class AnalyticsCard(CardFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("REAL-TIME ANALYTICS")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 13px; font-weight: bold;")
        layout.addWidget(title)
        empty = QLabel("Coming soon")
        empty.setStyleSheet(f"color: {TEXT_SUB}; font-size: 14px;")
        empty.setAlignment(Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(empty)
        layout.addStretch()
        self.setLayout(layout)

class TimelineCard(CardFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("TIMELINE")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 13px; font-weight: bold;")
        layout.addWidget(title)
        empty = QLabel("Coming soon")
        empty.setStyleSheet(f"color: {TEXT_SUB}; font-size: 14px;")
        empty.setAlignment(Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(empty)
        layout.addStretch()
        self.setLayout(layout)

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {DARK_BG}; font-family: 'Segoe UI', Arial, sans-serif;")
        main_layout = QHBoxLayout(self)
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        content = QVBoxLayout()
        self.topbar = TopBar()
        content.addWidget(self.topbar)
        grid = QGridLayout()
        grid.setSpacing(20)
        self.cameras = CameraFeeds()
        grid.addWidget(self.cameras, 0, 0, 2, 2)
        self.activity = ActivityDetection()
        grid.addWidget(self.activity, 0, 2, 1, 1)
        self.analytics = AnalyticsCard()
        grid.addWidget(self.analytics, 1, 2, 1, 1)
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