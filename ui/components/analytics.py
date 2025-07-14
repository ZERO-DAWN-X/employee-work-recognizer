from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt5.QtCore import Qt
import qtawesome as qta
from ui.style import PADDING, GAP, ACCENT, TEXT_MAIN, TEXT_SUB
from ui.components.card import CardFrame

class AnalyticsCard(CardFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(GAP)
        # Enhanced title with icon
        title_layout = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.chart-bar', color=ACCENT).pixmap(20, 20))
        title = QLabel("REAL-TIME ANALYTICS")
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
        # Enhanced coming soon state
        coming_soon_container = QFrame()
        coming_soon_container.setStyleSheet(f'''
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(0, 212, 170, 0.05), stop:1 rgba(59, 130, 246, 0.05));
            border: 1px solid rgba(0, 212, 170, 0.2);
            border-radius: 16px;
        ''')
        coming_layout = QVBoxLayout(coming_soon_container)
        coming_layout.setSpacing(12)
        chart_icon = QLabel("CHART")
        chart_icon.setStyleSheet(f"font-size: 24px; color: {ACCENT}; font-weight: bold;")
        chart_icon.setAlignment(Qt.AlignCenter)
        coming_text = QLabel("Advanced Analytics")
        coming_text.setStyleSheet(f'''
            color: {TEXT_MAIN};
            font-size: 16px;
            font-weight: 600;
        ''')
        coming_text.setAlignment(Qt.AlignCenter)
        coming_subtext = QLabel("Real-time insights coming soon")
        coming_subtext.setStyleSheet(f'''
            color: {TEXT_SUB};
            font-size: 14px;
        ''')
        coming_subtext.setAlignment(Qt.AlignCenter)
        coming_layout.addStretch()
        coming_layout.addWidget(chart_icon)
        coming_layout.addWidget(coming_text)
        coming_layout.addWidget(coming_subtext)
        coming_layout.addStretch()
        layout.addWidget(coming_soon_container)
        self.setLayout(layout) 