from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPainter, QPixmap
import qtawesome as qta
from ui.style import STATUS_SUCCESS, STATUS_INFO, STATUS_WARNING, ACCENT, TEXT_MAIN, TEXT_SUB

STATUS_KEYS = ['WORK', 'IDLE', 'SLEEPING', 'WALKING']

class StatusCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('StatusCard')
        self.setStyleSheet(f'''
            QFrame#StatusCard {{
                background: #181B20;
                border-radius: 18px;
                border: 1.5px solid rgba(255,255,255,0.06);
                padding: 18px 0 12px 0;
                min-width: 180px;
                max-width: 220px;
            }}
        ''')
        self.status = 'IDLE'
        # Build status map with icons after QApplication is running
        self.STATUS_MAP = {
            'WORK':    {'color': STATUS_SUCCESS, 'icon': qta.icon('fa5s.user', color=STATUS_SUCCESS), 'label': 'WORK'},
            'IDLE':    {'color': STATUS_INFO,    'icon': qta.icon('fa5s.coffee', color=STATUS_INFO), 'label': 'IDLE'},
            'SLEEPING':{'color': STATUS_WARNING, 'icon': qta.icon('fa5s.bed', color=STATUS_WARNING), 'label': 'SLEEPING'},
            'WALKING': {'color': ACCENT,         'icon': qta.icon('fa5s.walking', color=ACCENT), 'label': 'WALKING'},
        }
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        # Animated indicator
        self.indicator = QLabel()
        self.indicator.setFixedSize(18, 18)
        layout.addWidget(self.indicator, alignment=Qt.AlignHCenter)
        # Large icon + label
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(44, 44)
        self.icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon_label)
        self.text_label = QLabel()
        self.text_label.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 18px; font-weight: 600;")
        self.text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.text_label)
        # Sub-label
        self.sub_label = QLabel("Current Activity")
        self.sub_label.setStyleSheet(f"color: {TEXT_SUB}; font-size: 13px; font-weight: 500;")
        self.sub_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sub_label)
        # Legend
        legend = QHBoxLayout()
        legend.setSpacing(10)
        self.legend_labels = {}
        for key in STATUS_KEYS:
            info = self.STATUS_MAP[key]
            lbl = QLabel()
            lbl.setFixedSize(22, 22)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setPixmap(info['icon'].pixmap(20, 20))
            self.legend_labels[key] = lbl
            legend.addWidget(lbl)
        layout.addLayout(legend)
        self.set_status('IDLE')
        # Animation
        self._pulse = 0
        self._pulse_dir = 1
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(40)
    def set_status(self, status):
        if status not in self.STATUS_MAP:
            status = 'IDLE'
        self.status = status
        info = self.STATUS_MAP[status]
        self.icon_label.setPixmap(info['icon'].pixmap(44, 44))
        self.text_label.setText(info['label'])
        # Highlight legend
        for key, lbl in self.legend_labels.items():
            if key == status:
                lbl.setStyleSheet(f"border-bottom: 2px solid {self.STATUS_MAP[key]['color']}; background: rgba(0,0,0,0.12);")
            else:
                lbl.setStyleSheet(f"opacity: 0.5;")
        self.update_indicator()
    def _animate(self):
        self._pulse += self._pulse_dir * 0.12
        if self._pulse > 1:
            self._pulse = 1
            self._pulse_dir = -1
        elif self._pulse < 0.2:
            self._pulse = 0.2
            self._pulse_dir = 1
        self.update_indicator()
    def update_indicator(self):
        color = QColor(self.STATUS_MAP[self.status]['color'])
        pix = QPixmap(18, 18)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.Antialiasing)
        alpha = int(180 + 60 * self._pulse)
        color.setAlpha(alpha)
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(1, 1, 16, 16)
        painter.end()
        self.indicator.setPixmap(pix) 