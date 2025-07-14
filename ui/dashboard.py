from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from ui.style import BG_MAIN, GAP
from ui.components.camera_feeds import CameraFeeds
from ui.components.activity_status_list import ActivityStatusList

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f'''
            QWidget {{
                background: {BG_MAIN};
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }}
        ''')
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(GAP, GAP, GAP, GAP)
        main_layout.setSpacing(GAP)
        # Left: CameraFeeds
        self.cameras = CameraFeeds()
        main_layout.addWidget(self.cameras, stretch=2)
        # Right: ActivityStatusList
        self.status_list = ActivityStatusList()
        main_layout.addWidget(self.status_list, stretch=1)
        # Connect CameraFeeds to update status list
        self.cameras.status_update_callback = self.update_status_list
    def update_status_list(self, status_times, current_status):
        self.status_list.update_status(status_times, current_status)