from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt5.QtCore import Qt
import qtawesome as qta
from ui.style import PADDING, GAP, ACCENT, TEXT_MAIN, TEXT_SUB
from ui.components.card import CardFrame

class ActivityDetection(CardFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        # Enhanced title with icon
        title_layout = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.brain', color=ACCENT).pixmap(20, 20))
        title = QLabel("ACTIVITY DETECTION")
        title.setStyleSheet(f'''
            color: {TEXT_MAIN};
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 0.5px;
        ''')
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        # Enhanced empty state
        empty_container = QFrame()
        empty_container.setStyleSheet(f'''
            background: rgba(255, 255, 255, 0.02);
            border: 2px dashed rgba(156, 163, 175, 0.3);
            border-radius: 16px;
        ''')
        empty_layout = QVBoxLayout(empty_container)
        empty_layout.setSpacing(16)
        empty_icon = QLabel("AI")
        empty_icon.setStyleSheet(f"font-size: 32px; color: {ACCENT}; font-weight: bold;")
        empty_icon.setAlignment(Qt.AlignCenter)
        empty_text = QLabel("AI Detection Ready")
        empty_text.setStyleSheet(f'''
            color: {TEXT_SUB};
            font-size: 16px;
            font-weight: 500;
        ''')
        empty_text.setAlignment(Qt.AlignCenter)
        empty_subtext = QLabel("Waiting for camera input...")
        empty_subtext.setStyleSheet(f'''
            color: {TEXT_SUB};
            font-size: 14px;
            opacity: 0.7;
        ''')
        empty_subtext.setAlignment(Qt.AlignCenter)
        empty_layout.addStretch()
        empty_layout.addWidget(empty_icon)
        empty_layout.addWidget(empty_text)
        empty_layout.addWidget(empty_subtext)
        empty_layout.addStretch()
        layout.addWidget(empty_container)
        self.setLayout(layout) 