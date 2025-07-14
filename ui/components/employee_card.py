from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QFrame, QPushButton
from PyQt5.QtCore import Qt
from ui.components.card import CardFrame
from ui.components.status_list import StatusList
from ui.style import PADDING, GAP, TEXT_MAIN, TEXT_SUB

class EmployeeCard(CardFrame):
    def __init__(self, employee_name="Employee 1", current_status="WORK"):
        super().__init__()
        self.expanded = False
        self.employee_name = employee_name
        self.current_status = current_status
        self.setStyleSheet("border-radius: 18px; margin-bottom: 12px;")
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        main_layout.setSpacing(GAP)
        # Left: Camera + Info
        left_col = QVBoxLayout()
        left_col.setSpacing(6)
        # Camera placeholder
        self.camera_label = QLabel("[Camera Feed]")
        self.camera_label.setFixedSize(120, 80)
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("background: #181C22; border-radius: 12px; color: #444; font-size: 13px;")
        left_col.addWidget(self.camera_label)
        # Name + status
        name_label = QLabel(self.employee_name)
        name_label.setStyleSheet(f"color: {TEXT_MAIN}; font-size: 15px; font-weight: 600;")
        left_col.addWidget(name_label)
        status_label = QLabel(f"Status: {self.current_status}")
        status_label.setStyleSheet(f"color: {TEXT_SUB}; font-size: 13px;")
        left_col.addWidget(status_label)
        # Expand button
        self.expand_btn = QPushButton("Show Details")
        self.expand_btn.setCheckable(True)
        self.expand_btn.setStyleSheet("font-size: 12px; padding: 4px 10px; border-radius: 8px; background: #23272F; color: #7DD3FC;")
        self.expand_btn.clicked.connect(self.toggle_expand)
        left_col.addWidget(self.expand_btn)
        left_col.addStretch()
        main_layout.addLayout(left_col, 2)
        # Right: Status list
        self.status_list = StatusList(current_status=self.current_status)
        main_layout.addWidget(self.status_list, 1)
        # Details (hidden by default)
        self.details_frame = QFrame()
        self.details_frame.setStyleSheet("background: #101318; border-radius: 12px; margin-top: 8px;")
        details_layout = QVBoxLayout(self.details_frame)
        details_layout.setContentsMargins(12, 8, 12, 8)
        details_label = QLabel("Workday breakdown (9:00 - 17:00):\n[Status timeline here]")
        details_label.setStyleSheet(f"color: {TEXT_SUB}; font-size: 13px;")
        details_layout.addWidget(details_label)
        self.details_frame.setVisible(False)
        # Main vertical layout
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        vbox.addLayout(main_layout)
        vbox.addWidget(self.details_frame)
        self.setLayout(vbox)
    def toggle_expand(self):
        self.expanded = not self.expanded
        self.details_frame.setVisible(self.expanded)
        self.expand_btn.setText("Hide Details" if self.expanded else "Show Details") 