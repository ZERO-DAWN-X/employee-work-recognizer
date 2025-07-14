from PyQt5.QtWidgets import QFrame, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import qtawesome as qta
from ui.style import PADDING, CARD_RADIUS, SIDEBAR_BTN_BG_ACTIVE, SIDEBAR_BTN_BG_HOVER, ACCENT, TEXT_MAIN

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
                border-radius: 12px;
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
                background: #1A1F26;
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
        # Use fa5s prefix and FontAwesome 5 solid icon names
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