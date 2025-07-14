from PyQt5.QtWidgets import QFrame, QSizePolicy, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from ui.style import BG_CARD, BG_CARD_HOVER, CARD_RADIUS

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
