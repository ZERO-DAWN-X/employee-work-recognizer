from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from ui.style import PADDING, TOPBAR_HEIGHT, ACCENT, TEXT_MAIN, TEXT_SUB, STATUS_ERROR
from ui.components.modern_button import ModernButton
import qtawesome as qta

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
                    stop:0 #0F1419, stop:1 #0A0E12);
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