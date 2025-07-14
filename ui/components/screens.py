from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from ui.style import GAP, ACCENT, TEXT_MAIN, TEXT_SUB
from ui.components.camera_feeds import CameraFeeds
from ui.components.activity import ActivityDetection
from ui.components.analytics import AnalyticsCard
from ui.components.timeline import TimelineCard

class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        grid = QGridLayout()
        grid.setSpacing(GAP)
        # Set column stretch: camera feed (cols 0-1) gets 3, right-side (col 2) gets 1
        grid.setColumnStretch(0, 3)
        grid.setColumnStretch(1, 3)
        grid.setColumnStretch(2, 1)
        self.cameras = CameraFeeds()
        self.cameras.setMinimumWidth(600)  # Make camera card more prominent
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