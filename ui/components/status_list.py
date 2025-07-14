from PyQt5.QtWidgets import QVBoxLayout, QFrame, QLabel
from PyQt5.QtCore import Qt
import qtawesome as qta
from ui.style import ACCENT, STATUS_SUCCESS, STATUS_INFO, STATUS_ERROR, TEXT_MAIN, TEXT_SUB, PADDING, GAP

STATUS_DEFS = [
    {"key": "WORK", "label": "Work", "icon": qta.icon('fa5s.briefcase', color=STATUS_SUCCESS)},
    {"key": "IDLE", "label": "Idle", "icon": qta.icon('fa5s.coffee', color=STATUS_INFO)},
    {"key": "SLEEPING", "label": "Sleeping", "icon": qta.icon('fa5s.bed', color='#6366F1')},
    {"key": "WALKING", "label": "Walking", "icon": qta.icon('fa5s.walking', color=ACCENT)},
]

class StatusList(QFrame):
    def __init__(self, current_status="WORK"):
        super().__init__()
        self.current_status = current_status
        self.setStyleSheet(f"""
            QFrame {{
                background: transparent;
                border: none;
            }}
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(GAP)
        for status in STATUS_DEFS:
            row = QFrame()
            row_layout = QVBoxLayout(row)
            row_layout.setContentsMargins(PADDING, 4, PADDING, 4)
            row_layout.setSpacing(8)
            icon_label = QLabel()
            icon_label.setPixmap(status["icon"].pixmap(20, 20))
            text_label = QLabel(status["label"])
            text_label.setStyleSheet(f"font-size: 14px; font-weight: 500; color: {TEXT_MAIN}; margin-left: 8px;")
            row_layout.addWidget(icon_label)
            row_layout.addWidget(text_label)
            row.setLayout(row_layout)
            if status["key"] == self.current_status:
                row.setStyleSheet(f"background: rgba(0,212,170,0.08); border-radius: 10px;")
            else:
                row.setStyleSheet("")
            layout.addWidget(row)
        layout.addStretch()
        self.setLayout(layout)
    def set_status(self, status):
        self.current_status = status
        # TODO: update UI to reflect new status 