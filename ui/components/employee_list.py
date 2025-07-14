from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QFrame, QHBoxLayout, QSizePolicy, QScrollArea
from PyQt5.QtCore import Qt
from ui.style import STATUS_SUCCESS, STATUS_INFO, STATUS_ERROR, STATUS_WARNING, TEXT_MAIN, TEXT_SUB

# Demo employee data
EMPLOYEES = [
    {"name": "Alice Smith", "id": 1},
    {"name": "Bob Johnson", "id": 2},
    {"name": "Charlie Lee", "id": 3},
]

STATUS_COLORS = {
    "WORKING": STATUS_SUCCESS,
    "IDLE": STATUS_INFO,
    "SLEEPING": STATUS_ERROR,
    "WALKING": STATUS_WARNING,
}

class EmployeeStatusItem(QFrame):
    def __init__(self, employee):
        super().__init__()
        self.employee = employee
        self.status = "IDLE"
        self.expanded = False
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        # Header row
        header = QHBoxLayout()
        self.name_label = QLabel(self.employee["name"])
        self.name_label.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 15px; font-weight: 600;")
        header.addWidget(self.name_label)
        header.addStretch()
        self.status_badge = QLabel(self.status)
        self.status_badge.setStyleSheet(self._status_style(self.status))
        header.addWidget(self.status_badge)
        self.expand_btn = QPushButton("Details ▼")
        self.expand_btn.setCheckable(True)
        self.expand_btn.setStyleSheet(f"color: #00D4AA; background: transparent; border: none; font-weight: 600;")
        self.expand_btn.clicked.connect(self.toggle_expand)
        header.addWidget(self.expand_btn)
        layout.addLayout(header)
        # Details
        self.details_frame = QFrame()
        self.details_frame.setVisible(False)
        details_layout = QVBoxLayout(self.details_frame)
        details_layout.setContentsMargins(0, 0, 0, 0)
        details_layout.setSpacing(4)
        self.stats_label = QLabel("No analytics yet.")
        self.stats_label.setStyleSheet(f"color: {TEXT_SUB}; font-size: 13px;")
        details_layout.addWidget(self.stats_label)
        layout.addWidget(self.details_frame)
        self.setLayout(layout)
        self.setFrameShape(QFrame.StyledPanel)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def _status_style(self, status):
        color = STATUS_COLORS.get(status, STATUS_INFO)
        return f"background: {color}; color: white; font-weight: 600; padding: 2px 12px; border-radius: 10px;"

    def set_status(self, status):
        self.status = status
        self.status_badge.setText(status)
        self.status_badge.setStyleSheet(self._status_style(status))

    def toggle_expand(self):
        self.expanded = not self.expanded
        self.details_frame.setVisible(self.expanded)
        self.expand_btn.setText("Details ▲" if self.expanded else "Details ▼")

class EmployeeList(QWidget):
    def __init__(self, employees=EMPLOYEES):
        super().__init__()
        self.employees = employees
        self.items = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        vbox = QVBoxLayout(content)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(12)
        for emp in employees:
            item = EmployeeStatusItem(emp)
            vbox.addWidget(item)
            self.items.append(item)
        vbox.addStretch()
        content.setLayout(vbox)
        scroll.setWidget(content)
        layout.addWidget(scroll)
        self.setLayout(layout)

    def update_statuses(self, detected_faces):
        # Map detected faces to employees by order (left-to-right)
        for i, item in enumerate(self.items):
            if i < len(detected_faces):
                item.set_status("WORKING")
            else:
                item.set_status("IDLE") 