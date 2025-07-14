import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy, QGridLayout, QPushButton
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QIcon
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
TOPBAR_HEIGHT = 48

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

class CustomTopBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(TOPBAR_HEIGHT)
        self.setStyleSheet(f"background: {BG_MAIN}; border: none;")
        layout = QHBoxLayout()
        layout.setContentsMargins(PADDING, 0, PADDING, 0)
        layout.setSpacing(0)
        self.title = QLabel("AI-POWERED EMPLOYEE MONITORING")
        self.title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 17px; font-weight: bold; letter-spacing: 1px;")
        self.company = QLabel("ZERO-DAWN-X")
        self.company.setStyleSheet(f"color: {ACCENT}; font-size: 15px; font-weight: bold;")
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.company)
        # Window controls
        self.min_btn = QPushButton()
        self.max_btn = QPushButton()
        self.close_btn = QPushButton()
        for btn, icon, tooltip in [
            (self.min_btn, qta.icon('fa5s.window-minimize', color=TEXT_SUB), 'Minimize'),
            (self.max_btn, qta.icon('fa5s.square', color=TEXT_SUB), 'Maximize/Restore'),
            (self.close_btn, qta.icon('fa5s.times', color='#F55'), 'Close')
        ]:
            btn.setIcon(icon)
            btn.setFixedSize(32, 32)
            btn.setStyleSheet(f"background: transparent; border: none; margin-left: 4px;")
            btn.setToolTip(tooltip)
            layout.addWidget(btn)
        self.setLayout(layout)
        # Connect signals
        self.min_btn.clicked.connect(self._minimize)
        self.max_btn.clicked.connect(self._maximize_restore)
        self.close_btn.clicked.connect(self._close)
        self._parent = parent
        self._drag_pos = None
    def _minimize(self):
        if self._parent:
            self._parent.showMinimized()
    def _maximize_restore(self):
        if self._parent:
            if self._parent.isMaximized():
                self._parent.showNormal()
            else:
                self._parent.showMaximized()
    def _close(self):
        if self._parent:
            self._parent.close()
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self._parent.frameGeometry().topLeft()
            event.accept()
    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.LeftButton:
            self._parent.move(event.globalPos() - self._drag_pos)
            event.accept()
    def mouseReleaseEvent(self, event):
        self._drag_pos = None

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
        self.topbar = None  # Will be set by MainWindow
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
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.central = Dashboard()
        self.setCentralWidget(self.central)
        # Add custom top bar
        self.topbar = CustomTopBar(self)
        self.central.topbar = self.topbar
        layout = self.central.layout() or self.central.children()[0]
        layout.insertWidget(0, self.topbar)
        self.setStyleSheet(f"background: {BG_MAIN};")

def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 