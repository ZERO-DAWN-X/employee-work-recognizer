from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from ui.style import BTN_SIZE, BTN_RADIUS, ACCENT, BTN_BG_HOVER, BTN_BG_PRESSED

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