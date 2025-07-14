from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel
from PyQt5.QtCore import Qt, QTimer
from ui.style import GAP, ACCENT, TEXT_MAIN, TEXT_SUB
from ui.components.camera_feeds import CameraFeeds
from ui.components.activity import ActivityDetection
from ui.components.analytics import AnalyticsCard
from ui.components.timeline import TimelineCard
from ui.components.employee_list import EmployeeList

class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(GAP, GAP, GAP, GAP)
        main_layout.setSpacing(GAP)
        # Left: Camera feed
        self.camera_feeds = CameraFeeds()
        main_layout.addWidget(self.camera_feeds, stretch=2)
        # Right: Employee status panel
        right_panel = QVBoxLayout()
        right_panel.setSpacing(GAP)
        self.employee_list = EmployeeList()
        right_panel.addWidget(self.employee_list)
        right_panel.addStretch()
        main_layout.addLayout(right_panel, stretch=1)
        # Timer to update employee statuses from camera
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_employee_statuses)
        self.status_timer.start(500)

    def update_employee_statuses(self):
        faces = self.camera_feeds.get_latest_faces()
        self.employee_list.update_statuses(faces)

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