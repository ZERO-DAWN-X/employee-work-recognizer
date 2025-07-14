from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt5.QtCore import Qt
import qtawesome as qta
from ui.style import PADDING, GAP, ACCENT, TEXT_MAIN, TEXT_SUB
from ui.components.card import CardFrame

class TimelineCard(CardFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        # Enhanced title with icon
        title_layout = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.clock', color=ACCENT).pixmap(20, 20))
        title = QLabel("ACTIVITY TIMELINE")
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
        # Enhanced timeline placeholder
        timeline_container = QFrame()
        timeline_container.setStyleSheet(f'''
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
        ''')
        timeline_layout = QVBoxLayout(timeline_container)
        timeline_layout.setSpacing(12)
        timeline_icon = QLabel("TIME")
        timeline_icon.setStyleSheet(f"font-size: 24px; color: {ACCENT}; font-weight: bold;")
        timeline_icon.setAlignment(Qt.AlignCenter)
        timeline_text = QLabel("Timeline View")
        timeline_text.setStyleSheet(f'''
            color: {TEXT_MAIN};
            font-size: 16px;
            font-weight: 600;
        ''')
        timeline_text.setAlignment(Qt.AlignCenter)
        timeline_subtext = QLabel("Track activities over time")
        timeline_subtext.setStyleSheet(f'''
            color: {TEXT_SUB};
            font-size: 14px;
        ''')
        timeline_subtext.setAlignment(Qt.AlignCenter)
        timeline_layout.addStretch()
        timeline_layout.addWidget(timeline_icon)
        timeline_layout.addWidget(timeline_text)
        timeline_layout.addWidget(timeline_subtext)
        timeline_layout.addStretch()
        layout.addWidget(timeline_container)
        self.setLayout(layout) 