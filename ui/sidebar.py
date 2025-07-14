from PyQt5.QtWidgets import QFrame, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
import qtawesome as qta

# Sidebar constants (should match app.py)
ICON_SIZE = 28
PADDING = 24
GAP = 24
CARD_RADIUS = 18
TEXT_MAIN = "#F5F6FA"
BTN_RADIUS = 8
SIDEBAR_BTN_BG_ACTIVE = "rgba(61,225,201,0.12)"
SIDEBAR_BTN_BG_HOVER = "rgba(61,225,201,0.08)"

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
        self.setStyleSheet(f"background: #20242A; border: none; border-radius: {CARD_RADIUS}px;")
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