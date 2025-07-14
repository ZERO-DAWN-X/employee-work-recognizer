from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
import qtawesome as qta
from ui.style import ACCENT, STATUS_SUCCESS, STATUS_INFO, STATUS_WARNING, STATUS_ERROR, TEXT_MAIN, TEXT_SUB

STATUS_CONFIG = {
    'WORK':    {'icon': qta.icon('fa5s.laptop', color=STATUS_SUCCESS), 'color': STATUS_SUCCESS, 'label': 'Work'},
    'IDLE':    {'icon': qta.icon('fa5s.coffee', color=STATUS_INFO),    'color': STATUS_INFO,    'label': 'Idle'},
    'SLEEP':   {'icon': qta.icon('fa5s.bed', color=STATUS_WARNING),    'color': STATUS_WARNING,  'label': 'Sleeping'},
    'WALK':    {'icon': qta.icon('fa5s.walking', color=ACCENT),        'color': ACCENT,         'label': 'Walking'},
}

class ActivityStatusList(QWidget):
    def __init__(self, status_times=None, current_status='WORK', parent=None):
        super().__init__(parent)
        self.status_times = status_times or {k: 0 for k in STATUS_CONFIG}
        self.current_status = current_status
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(18)
        self.status_labels = {}
        self.build_ui()
    def build_ui(self):
        for status, cfg in STATUS_CONFIG.items():
            row = QHBoxLayout()
            # Icon
            icon_label = QLabel()
            icon_label.setPixmap(cfg['icon'].pixmap(28, 28))
            row.addWidget(icon_label)
            # Label
            text = QLabel(cfg['label'])
            text.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 16px; font-weight: 500;")
            row.addWidget(text)
            # Spacer
            row.addStretch()
            # Time
            time_label = QLabel("0s")
            time_label.setStyleSheet(f"color: {TEXT_SUB}; font-size: 14px;")
            row.addWidget(time_label)
            # Dot
            dot = QLabel()
            dot.setFixedSize(14, 14)
            dot.setStyleSheet(f"border-radius: 7px; background: {cfg['color']}; margin-left: 10px;")
            row.addWidget(dot)
            # Highlight if current
            container = QWidget()
            container.setLayout(row)
            if status == self.current_status:
                container.setStyleSheet(f"background: rgba(0,212,170,0.10); border-radius: 10px;")
            else:
                container.setStyleSheet("")
            self.layout.addWidget(container)
            self.status_labels[status] = (time_label, container)
        self.layout.addStretch()
    def update_status(self, status_times, current_status):
        self.status_times = status_times
        self.current_status = current_status
        for status, (time_label, container) in self.status_labels.items():
            t = int(status_times.get(status, 0))
            time_label.setText(f"{t//60}m {t%60}s" if t >= 60 else f"{t}s")
            if status == current_status:
                container.setStyleSheet(f"background: rgba(0,212,170,0.10); border-radius: 10px;")
            else:
                container.setStyleSheet("") 