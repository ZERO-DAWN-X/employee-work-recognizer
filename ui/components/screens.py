from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from ui.style import GAP, ACCENT, TEXT_MAIN, TEXT_SUB
from ui.components.employee_card import EmployeeCard
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
        # Left: Employee cards (vertical)
        self.employee_cards = []
        employees = [
            {"name": "Alice Smith", "status": "WORK"},
            {"name": "Bob Lee", "status": "IDLE"},
        ]
        left_col = QVBoxLayout()
        left_col.setSpacing(GAP)
        for emp in employees:
            card = EmployeeCard(employee_name=emp["name"], current_status=emp["status"])
            self.employee_cards.append(card)
            left_col.addWidget(card)
        left_col.addStretch()
        grid.addLayout(left_col, 0, 0, 2, 1)
        # Right: Activity, Analytics
        self.activity = ActivityDetection()
        grid.addWidget(self.activity, 0, 1, 1, 1)
        self.analytics = AnalyticsCard()
        grid.addWidget(self.analytics, 1, 1, 1, 1)
        # Bottom: Timeline
        self.timeline = TimelineCard()
        grid.addWidget(self.timeline, 2, 0, 1, 2)
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