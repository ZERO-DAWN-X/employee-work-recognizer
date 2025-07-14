import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy, QGridLayout, QPushButton, QStackedWidget
)
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QImage, QPixmap, QPainter, QPainterPath
import qtawesome as qta
import cv2

# --- Color Palette ---
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

BTN_RADIUS = 8
BTN_SIZE = 32
BTN_BG_HOVER = "rgba(61, 225, 201, 0.10)"  # Accent, faded
BTN_BG_PRESSED = "rgba(61, 225, 201, 0.18)"  # Accent, more visible
BTN_FOCUS_SHADOW = "0 0 0 3px rgba(61,225,201,0.25)"

SIDEBAR_BTN_BG_ACTIVE = "rgba(61,225,201,0.12)"
SIDEBAR_BTN_BG_HOVER = "rgba(61,225,201,0.08)"

class ModernButton(QPushButton):
    def __init__(self, icon, tooltip, accent_color=None, parent=None):
        super().__init__(parent)
        self.setIcon(icon)
        self.setFixedSize(BTN_SIZE, BTN_SIZE)
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.StrongFocus)
        self._accent = accent_color or ACCENT
        self.setStyleSheet(f'''
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: {BTN_RADIUS}px;
                margin-left: 4px;
            }}
            QPushButton:hover {{
                background: {BTN_BG_HOVER};
            }}
            QPushButton:pressed {{
                background: {BTN_BG_PRESSED};
            }}
            QPushButton:focus {{
                outline: none;
            }}
        ''')
    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.update()
    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.update()

class SidebarButton(QPushButton):
    def __init__(self, icon, tooltip, index, parent=None):
        super().__init__(parent)
        self.setIcon(icon)
        self.setFixedSize(ICON_SIZE+12, ICON_SIZE+12)
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.NoFocus)
        self.index = index
        self.setCheckable(True)
        self.setStyleSheet(f'''
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: {BTN_RADIUS}px;
                margin: 0;
            }}
            QPushButton:hover {{
                background: {SIDEBAR_BTN_BG_HOVER};
            }}
            QPushButton:checked {{
                background: {SIDEBAR_BTN_BG_ACTIVE};
            }}
        ''')

class Sidebar(QFrame):
    def __init__(self, on_nav):
        super().__init__()
        self.setFixedWidth(64)
        self.setStyleSheet(f"background: {BG_SIDEBAR}; border: none; border-radius: {CARD_RADIUS}px;")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, PADDING, 0, PADDING)
        layout.setSpacing(GAP)
        layout.setAlignment(Qt.AlignTop)
        self.buttons = []
        icons = [
            (qta.icon('fa5s.tachometer-alt', color=TEXT_MAIN), 'Dashboard'),
            (qta.icon('fa5s.users', color=TEXT_MAIN), 'Users'),
            (qta.icon('fa5s.chart-line', color=TEXT_MAIN), 'Analytics'),
            (qta.icon('fa5s.cog', color=TEXT_MAIN), 'Settings')
        ]
        for i, (icon, tooltip) in enumerate(icons):
            btn = SidebarButton(icon, tooltip, i)
            btn.clicked.connect(lambda checked, idx=i: on_nav(idx))
            layout.addWidget(btn, alignment=Qt.AlignHCenter)
            self.buttons.append(btn)
        layout.addStretch()
        self.setLayout(layout)
        self.set_active(0)
    def set_active(self, idx):
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == idx)

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
        # Window controls with modern effects
        self.min_btn = ModernButton(qta.icon('fa5s.window-minimize', color=TEXT_SUB), 'Minimize')
        self.max_btn = ModernButton(qta.icon('fa5s.square', color=TEXT_SUB), 'Maximize/Restore')
        self.close_btn = ModernButton(qta.icon('fa5s.times', color='#F55'), 'Close', accent_color='#F55')
        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(self.close_btn)
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
        self.cap = None
        self.timer = None
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        title = QLabel("LIVE CAMERA FEEDS")
        title.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        # Video feed container with grid layout for overlay
        self.video_container = QFrame()
        self.video_container.setStyleSheet(f"background: #181B20; border-radius: 18px; border: none;")
        self.video_container.setMinimumSize(340, 220)
        video_grid = QGridLayout(self.video_container)
        video_grid.setContentsMargins(0, 0, 0, 0)
        video_grid.setSpacing(0)
        # Border frame with rounded corners and accent border
        self.video_border = QFrame()
        self.video_border.setStyleSheet(f"background: transparent; border: 2px solid {ACCENT}; border-radius: 18px;")
        self.video_border.setMinimumSize(320, 200)
        border_layout = QVBoxLayout(self.video_border)
        border_layout.setContentsMargins(0, 0, 0, 0)
        border_layout.setSpacing(0)
        # Video label (no border, just rounded corners)
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet(f"background: #111; border-radius: 18px;")
        self.video_label.setMinimumSize(316, 196)
        border_layout.addWidget(self.video_label)
        video_grid.addWidget(self.video_border, 0, 0, 2, 2, alignment=Qt.AlignCenter)
        # LIVE badge (unchanged)
        self.live_badge = QLabel("LIVE")
        self.live_badge.setStyleSheet(f"background: {ACCENT}; color: #fff; font-weight: bold; font-size: 13px; padding: 4px 18px; border-radius: 14px; margin-top: 18px; margin-left: 18px;")
        self.live_badge.setFixedWidth(60)
        self.live_badge.setAlignment(Qt.AlignCenter)
        video_grid.addWidget(self.live_badge, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)
        # Add video container to main layout
        layout.addWidget(self.video_container, stretch=1, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.start_camera()
    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.video_label.setText("Error: Could not open webcam.")
            return
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
                # Rounded corners mask (match border radius)
                radius = 18
                rounded = QPixmap(pixmap.size())
                rounded.fill(Qt.transparent)
                painter = QPainter(rounded)
                painter.setRenderHint(QPainter.Antialiasing)
                path = QPainterPath()
                path.addRoundedRect(0, 0, pixmap.width(), pixmap.height(), radius, radius)
                painter.setClipPath(path)
                painter.drawPixmap(0, 0, pixmap)
                painter.end()
                self.video_label.setPixmap(rounded.scaled(
                    self.video_label.width(), self.video_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.video_label.setText("Error: Failed to capture frame.")
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

# Placeholder screens for each section
class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
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
        layout.addLayout(grid)

class UsersScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Users Management (Coming soon)")
        label.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 18px; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

class AnalyticsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Analytics (Coming soon)")
        label.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 18px; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Settings (Coming soon)")
        label.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 18px; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {BG_MAIN}; font-family: 'Segoe UI', Arial, sans-serif;")
        # Outer vertical layout: top bar, then main content
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        self.topbar = None
        # Main content area: sidebar + stacked content
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(GAP, GAP, GAP, GAP)
        main_layout.setSpacing(GAP)
        # Sidebar with navigation
        self.stacked = QStackedWidget()
        self.sidebar = Sidebar(self.on_nav)
        main_layout.addWidget(self.sidebar)
        # Add screens to stacked widget
        self.screens = [
            DashboardScreen(),
            UsersScreen(),
            AnalyticsScreen(),
            SettingsScreen()
        ]
        for screen in self.screens:
            self.stacked.addWidget(screen)
        main_layout.addWidget(self.stacked)
        # Add layouts to outer layout
        outer_layout.addSpacing(0)
        outer_layout.addLayout(main_layout)
    def on_nav(self, idx):
        self.sidebar.set_active(idx)
        self.stacked.setCurrentIndex(idx)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Work Time Recognizer")
        self.setMinimumSize(1100, 750)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.central = Dashboard()
        self.setCentralWidget(self.central)
        # Add custom top bar as true header
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