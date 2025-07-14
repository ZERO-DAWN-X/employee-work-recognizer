import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import qtawesome as qta

# --- Color Palette (from reference image) ---
BG_MAIN = "#181B20"         # Main background
BG_SIDEBAR = "#20242A"     # Sidebar background
BG_CARD = "#23262B"        # Card background
ACCENT = "#3DE1C9"         # Accent (teal)
TEXT_MAIN = "#F5F6FA"      # Main text (almost white)
TEXT_SUB = "#A0A4AB"       # Subtle text (gray)
BAR_WORK = "#3DE1C9"       # Bar - working
BAR_IDLE = "#4A90E2"       # Bar - idle
BAR_EAT = "#F5A623"        # Bar - eating
BAR_SLEEP = "#9B59B6"      # Bar - sleeping

# --- Spacing & Sizing ---
PADDING = 24
CARD_RADIUS = 18
GAP = 24
ICON_SIZE = 28

class Sidebar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(64)
        self.setStyleSheet(f"background: {BG_SIDEBAR}; border: none; border-radius: {CARD_RADIUS}px;")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, PADDING, 0, PADDING)
        layout.setSpacing(GAP)
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
        layout.addStretch()
        self.setLayout(layout)

class TopBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(56)
        self.setStyleSheet(f"background: {BG_MAIN}; border: none;")
        layout = QHBoxLayout()
        layout.setContentsMargins(PADDING, 0, PADDING, 0)
        title = QLabel("AI-POWERED EMPLOYEE MONITORING")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 17px; font-weight: bold; letter-spacing: 1px;")
        company = QLabel("ZERO-DAWN-X")
        company.setStyleSheet(f"color: {ACCENT}; font-size: 15px; font-weight: bold;")
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(company)
        self.setLayout(layout)

class CardFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {BG_CARD}; border-radius: {CARD_RADIUS}px;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

class CameraFeeds(CardFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        title = QLabel("LIVE CAMERA FEEDS")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        empty = QLabel("No data available")
        empty.setStyleSheet(f"color: {TEXT_SUB}; font-size: 15px;")
        empty.setAlignment(Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(empty)
        layout.addStretch()
        self.setLayout(layout)

class ActivityDetection(CardFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        title = QLabel("ACTIVITY DETECTION")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        empty = QLabel("No data available")
        empty.setStyleSheet(f"color: {TEXT_SUB}; font-size: 15px;")
        empty.setAlignment(Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(empty)
        layout.addStretch()
        self.setLayout(layout)

class AnalyticsCard(CardFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        title = QLabel("REAL-TIME ANALYTICS")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        empty = QLabel("Coming soon")
        empty.setStyleSheet(f"color: {TEXT_SUB}; font-size: 15px;")
        empty.setAlignment(Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(empty)
        layout.addStretch()
        self.setLayout(layout)

class TimelineCard(CardFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        title = QLabel("TIMELINE")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        empty = QLabel("Coming soon")
        empty.setStyleSheet(f"color: {TEXT_SUB}; font-size: 15px;")
        empty.setAlignment(Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(empty)
        layout.addStretch()
        self.setLayout(layout)

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {BG_MAIN}; font-family: 'Segoe UI', Arial, sans-serif;")
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(GAP, GAP, GAP, GAP)
        main_layout.setSpacing(GAP)
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        content = QVBoxLayout()
        content.setSpacing(GAP)
        self.topbar = TopBar()
        content.addWidget(self.topbar)
        grid = QGridLayout()
        grid.setSpacing(GAP)
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
        self.setMinimumSize(1100, 750)
        self.setCentralWidget(Dashboard())
        self.setStyleSheet(f"background: {BG_MAIN};")

def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 