from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from ui.style import BG_MAIN
from ui.dashboard import Dashboard
from ui.components.topbar import CustomTopBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Work Time Recognizer")
        self.setMinimumSize(1200, 800)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # Set window background with subtle gradient
        self.setStyleSheet(f'''
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {BG_MAIN}, stop:1 #0A0E12);
            }}
        ''')
        self.central = Dashboard()
        self.setCentralWidget(self.central)
        # Add custom top bar as true header
        self.topbar = CustomTopBar(self)
        self.central.topbar = self.topbar
        layout = self.central.layout() or self.central.children()[0]
        layout.insertWidget(0, self.topbar) 