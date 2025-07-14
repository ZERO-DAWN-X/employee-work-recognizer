import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy, QGridLayout, QPushButton, QStackedWidget, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QImage, QPixmap, QPainter, QPainterPath, QLinearGradient
import qtawesome as qta
import cv2

# --- Enhanced Color Palette ---
BG_MAIN = "#0F1419"         # Darker main background for depth
BG_SIDEBAR = "#1A1F26"      # Enhanced sidebar with subtle gradient feel
BG_CARD = "#1E2329"         # Card background with better contrast
BG_CARD_HOVER = "#242A32"   # Card hover state
ACCENT = "#00D4AA"          # Modern teal accent
ACCENT_HOVER = "#00E6BB"    # Brighter accent for hover
ACCENT_DARK = "#00B899"     # Darker accent for pressed states
TEXT_MAIN = "#FFFFFF"       # Pure white for better readability
TEXT_SUB = "#9CA3AF"        # Modern gray for subtle text
TEXT_ACCENT = "#00D4AA"     # Accent color for highlights

# Status colors
STATUS_SUCCESS = "#10B981"  # Green
STATUS_WARNING = "#F59E0B"  # Amber
STATUS_ERROR = "#EF4444"    # Red
STATUS_INFO = "#3B82F6"     # Blue

# --- Enhanced Spacing & Sizing ---
PADDING = 28
CARD_RADIUS = 20
GAP = 28
ICON_SIZE = 24
TOPBAR_HEIGHT = 56

BTN_RADIUS = 12
BTN_SIZE = 40
BTN_BG_HOVER = "rgba(0, 212, 170, 0.08)"
BTN_BG_PRESSED = "rgba(0, 212, 170, 0.16)"

SIDEBAR_BTN_BG_ACTIVE = "rgba(0, 212, 170, 0.15)"
SIDEBAR_BTN_BG_HOVER = "rgba(0, 212, 170, 0.08)"

class ModernButton(QPushButton):
    def __init__(self, icon, tooltip, accent_color=None, parent=None):
        super().__init__(parent)
        self.setIcon(icon)
        self.setFixedSize(BTN_SIZE, BTN_SIZE)
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.StrongFocus)
        self._accent = accent_color or ACCENT
        
        # Add subtle shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet(f'''
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: {BTN_RADIUS}px;
                margin: 2px;
            }}
            QPushButton:hover {{
                background: {BTN_BG_HOVER};
                border: 1px solid rgba(0, 212, 170, 0.2);
            }}
            QPushButton:pressed {{
                background: {BTN_BG_PRESSED};
                border: 1px solid rgba(0, 212, 170, 0.3);
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
        self.setFixedSize(48, 48)
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.NoFocus)
        self.index = index
        self.setCheckable(True)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(6)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 1)
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet(f'''
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: {BTN_RADIUS}px;
                margin: 4px;
            }}
            QPushButton:hover {{
                background: {SIDEBAR_BTN_BG_HOVER};
            }}
            QPushButton:checked {{
                background: {SIDEBAR_BTN_BG_ACTIVE};
                border: 1px solid rgba(0, 212, 170, 0.3);
            }}
        ''')

class Sidebar(QFrame):
    def __init__(self, on_nav):
        super().__init__()
        self.setFixedWidth(80)
        
        # Add shadow effect to sidebar
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(2, 0)
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet(f'''
            QFrame {{
                background: {BG_SIDEBAR};
                border: none;
                border-radius: {CARD_RADIUS}px;
                border-right: 1px solid rgba(255, 255, 255, 0.05);
            }}
        ''')
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, PADDING, 0, PADDING)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignTop)
        
        # Logo/Brand area
        brand_label = QLabel("ZDX")
        brand_label.setStyleSheet(f'''
            color: {ACCENT};
            font-size: 18px;
            font-weight: bold;
            padding: 12px;
            margin-bottom: 20px;
        ''')
        brand_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(brand_label)
        
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
        
        # Add gradient background and shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet(f'''
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {BG_MAIN}, stop:1 #0A0E12);
                border: none;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }}
        ''')
        
        layout = QHBoxLayout()
        layout.setContentsMargins(PADDING, 0, PADDING, 0)
        layout.setSpacing(0)
        
        # Title with enhanced styling
        self.title = QLabel("AI-POWERED EMPLOYEE MONITORING")
        self.title.setStyleSheet(f'''
            color: {TEXT_MAIN};
            font-size: 18px;
            font-weight: 600;
            letter-spacing: 0.5px;
        ''')
        
        # Company name with accent styling
        self.company = QLabel("ZERO-DAWN-X")
        self.company.setStyleSheet(f'''
            color: {ACCENT};
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 1px;
        ''')
        
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.company)
        
        # Enhanced window controls
        self.min_btn = ModernButton(qta.icon('fa5s.window-minimize', color=TEXT_SUB), 'Minimize')
        self.max_btn = ModernButton(qta.icon('fa5s.square', color=TEXT_SUB), 'Maximize/Restore')
        self.close_btn = ModernButton(qta.icon('fa5s.times', color=STATUS_ERROR), 'Close', accent_color=STATUS_ERROR)
        
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
        
        # Add shadow effect to cards
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet(f'''
            QFrame {{
                background: {BG_CARD};
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: {CARD_RADIUS}px;
            }}
            QFrame:hover {{
                background: {BG_CARD_HOVER};
                border: 1px solid rgba(0, 212, 170, 0.1);
            }}
        ''')
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
        
        # Enhanced title with icon
        title_layout = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.video', color=ACCENT).pixmap(20, 20))
        title = QLabel("LIVE CAMERA FEEDS")
        title.setStyleSheet(f'''
            color: {TEXT_MAIN};
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
            color: {TEXT_SUB};
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

class ActivityDetection(CardFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        
        # Enhanced title with icon
        title_layout = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.brain', color=ACCENT).pixmap(20, 20))
        title = QLabel("ACTIVITY DETECTION")
        title.setStyleSheet(f'''
            color: {TEXT_MAIN};
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 0.5px;
        ''')
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # Enhanced empty state
        empty_container = QFrame()
        empty_container.setStyleSheet(f'''
            background: rgba(255, 255, 255, 0.02);
            border: 2px dashed rgba(156, 163, 175, 0.3);
            border-radius: 16px;
        ''')
        empty_layout = QVBoxLayout(empty_container)
        empty_layout.setSpacing(16)
        
        empty_icon = QLabel("AI")
        empty_icon.setStyleSheet(f"font-size: 32px; color: {ACCENT}; font-weight: bold;")
        empty_icon.setAlignment(Qt.AlignCenter)
        
        empty_text = QLabel("AI Detection Ready")
        empty_text.setStyleSheet(f'''
            color: {TEXT_SUB};
            font-size: 16px;
            font-weight: 500;
        ''')
        empty_text.setAlignment(Qt.AlignCenter)
        
        empty_subtext = QLabel("Waiting for camera input...")
        empty_subtext.setStyleSheet(f'''
            color: {TEXT_SUB};
            font-size: 14px;
            opacity: 0.7;
        ''')
        empty_subtext.setAlignment(Qt.AlignCenter)
        
        empty_layout.addStretch()
        empty_layout.addWidget(empty_icon)
        empty_layout.addWidget(empty_text)
        empty_layout.addWidget(empty_subtext)
        empty_layout.addStretch()
        
        layout.addWidget(empty_container)
        self.setLayout(layout)

class AnalyticsCard(CardFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        
        # Enhanced title with icon
        title_layout = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.chart-bar', color=ACCENT).pixmap(20, 20))
        title = QLabel("REAL-TIME ANALYTICS")
        title.setStyleSheet(f'''
            color: {TEXT_MAIN};
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 0.5px;
        ''')
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # Enhanced coming soon state
        coming_soon_container = QFrame()
        coming_soon_container.setStyleSheet(f'''
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(0, 212, 170, 0.05), stop:1 rgba(59, 130, 246, 0.05));
            border: 1px solid rgba(0, 212, 170, 0.2);
            border-radius: 16px;
        ''')
        coming_layout = QVBoxLayout(coming_soon_container)
        coming_layout.setSpacing(12)
        
        chart_icon = QLabel("CHART")
        chart_icon.setStyleSheet(f"font-size: 24px; color: {ACCENT}; font-weight: bold;")
        chart_icon.setAlignment(Qt.AlignCenter)
        
        coming_text = QLabel("Advanced Analytics")
        coming_text.setStyleSheet(f'''
            color: {TEXT_MAIN};
            font-size: 16px;
            font-weight: 600;
        ''')
        coming_text.setAlignment(Qt.AlignCenter)
        
        coming_subtext = QLabel("Real-time insights coming soon")
        coming_subtext.setStyleSheet(f'''
            color: {TEXT_SUB};
            font-size: 14px;
        ''')
        coming_subtext.setAlignment(Qt.AlignCenter)
        
        coming_layout.addStretch()
        coming_layout.addWidget(chart_icon)
        coming_layout.addWidget(coming_text)
        coming_layout.addWidget(coming_subtext)
        coming_layout.addStretch()
        
        layout.addWidget(coming_soon_container)
        self.setLayout(layout)

class TimelineCard(CardFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        
        # Enhanced title with icon
        title_layout = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.clock', color=ACCENT).pixmap(20, 20))
        title = QLabel("ACTIVITY TIMELINE")
        title.setStyleSheet(f'''
            color: {TEXT_MAIN};
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 0.5px;
        ''')
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # Enhanced timeline placeholder
        timeline_container = QFrame()
        timeline_container.setStyleSheet(f'''
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
        ''')
        timeline_layout = QVBoxLayout(timeline_container)
        timeline_layout.setSpacing(12)
        
        timeline_icon = QLabel("TIME")
        timeline_icon.setStyleSheet(f"font-size: 24px; color: {ACCENT}; font-weight: bold;")
        timeline_icon.setAlignment(Qt.AlignCenter)
        
        timeline_text = QLabel("Timeline View")
        timeline_text.setStyleSheet(f'''
            color: {TEXT_MAIN};
            font-size: 16px;
            font-weight: 600;
        ''')
        timeline_text.setAlignment(Qt.AlignCenter)
        
        timeline_subtext = QLabel("Track activities over time")
        timeline_subtext.setStyleSheet(f'''
            color: {TEXT_SUB};
            font-size: 14px;
        ''')
        timeline_subtext.setAlignment(Qt.AlignCenter)
        
        timeline_layout.addStretch()
        timeline_layout.addWidget(timeline_icon)
        timeline_layout.addWidget(timeline_text)
        timeline_layout.addWidget(timeline_subtext)
        timeline_layout.addStretch()
        
        layout.addWidget(timeline_container)
        self.setLayout(layout)

# Enhanced placeholder screens for each section
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
        layout.setAlignment(Qt.AlignCenter)
        
        icon = QLabel("USERS")
        icon.setStyleSheet(f"font-size: 48px; color: {ACCENT}; font-weight: bold;")
        icon.setAlignment(Qt.AlignCenter)
        
        label = QLabel("Users Management")
        label.setStyleSheet(f'''
            color: {TEXT_MAIN};
            font-size: 24px;
            font-weight: 600;
            margin: 16px 0;
        ''')
        label.setAlignment(Qt.AlignCenter)
        
        sublabel = QLabel("Employee management features coming soon")
        sublabel.setStyleSheet(f'''
            color: {TEXT_SUB};
            font-size: 16px;
        ''')
        sublabel.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(icon)
        layout.addWidget(label)
        layout.addWidget(sublabel)

class AnalyticsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        icon = QLabel("ANALYTICS")
        icon.setStyleSheet(f"font-size: 48px; color: {ACCENT}; font-weight: bold;")
        icon.setAlignment(Qt.AlignCenter)
        
        label = QLabel("Advanced Analytics")
        label.setStyleSheet(f'''
            color: {TEXT_MAIN};
            font-size: 24px;
            font-weight: 600;
            margin: 16px 0;
        ''')
        label.setAlignment(Qt.AlignCenter)
        
        sublabel = QLabel("Detailed productivity insights coming soon")
        sublabel.setStyleSheet(f'''
            color: {TEXT_SUB};
            font-size: 16px;
        ''')
        sublabel.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(icon)
        layout.addWidget(label)
        layout.addWidget(sublabel)

class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        icon = QLabel("SETTINGS")
        icon.setStyleSheet(f"font-size: 48px; color: {ACCENT}; font-weight: bold;")
        icon.setAlignment(Qt.AlignCenter)
        
        label = QLabel("System Settings")
        label.setStyleSheet(f'''
            color: {TEXT_MAIN};
            font-size: 24px;
            font-weight: 600;
            margin: 16px 0;
        ''')
        label.setAlignment(Qt.AlignCenter)
        
        sublabel = QLabel("Configuration options coming soon")
        sublabel.setStyleSheet(f'''
            color: {TEXT_SUB};
            font-size: 16px;
        ''')
        sublabel.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(icon)
        layout.addWidget(label)
        layout.addWidget(sublabel)

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f'''
            QWidget {{
                background: {BG_MAIN};
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }}
        ''')
        
        # Outer vertical layout: top bar, then main content
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        
        self.topbar = None
        
        # Main content area: sidebar + stacked content
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(GAP, GAP, GAP, GAP)
        main_layout.setSpacing(GAP)
        
        # Enhanced sidebar with navigation
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
        self.setMinimumSize(1200, 800)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Set window background with subtle gradient
        self.setStyleSheet(f'''
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {BG_MAIN}, stop:1 #0A0E12);
            }}
        ''')
        
        self.central = Dashboard()
        self.setCentralWidget(self.central)
        
        # Add custom top bar as true header
        self.topbar = CustomTopBar(self)
        self.central.topbar = self.topbar
        
        layout = self.central.layout() or self.central.children()[0]
        layout.insertWidget(0, self.topbar)

def run_app():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Enhanced font
    font = QFont("Segoe UI", 9)
    font.setHintingPreference(QFont.PreferFullHinting)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())