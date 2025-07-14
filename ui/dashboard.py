from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
from ui.style import BG_MAIN, GAP
from ui.components.sidebar import Sidebar
from ui.components.screens import DashboardScreen, UsersScreen, AnalyticsScreen, SettingsScreen

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