import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from ui.main_window import MainWindow

def run_app():
    app = QApplication(sys.argv)
    # Set application style
    app.setStyle('Fusion')
    # Enhanced font
    font = QFont("Segoe UI", 9)
    font.setHintingPreference(QFont.PreferFullHinting)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()