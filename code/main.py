from UI_interface import MusicGeneratorApp
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
main_window = MusicGeneratorApp()
main_window.show()
# QTimer.singleShot(20000, app.quit) # 设置定时器，5秒后退出应用
sys.exit(app.exec_())