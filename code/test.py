import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSlider, QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class VolumePopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    def initUI(self):
        # 创建布局
        layout = QVBoxLayout()
        # 创建音量滑块
        self.volume_slider = QSlider()
        self.volume_slider.setOrientation(Qt.Vertical)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)  # 默认音量为50
        self.volume_slider.valueChanged.connect(self.update_volume_label)

        # 创建音量标签
        self.volume_label = QLabel("音量: 50")

        # 将控件添加到布局中
        layout.addWidget(self.volume_label)
        layout.addWidget(self.volume_slider)

        # 设置窗口布局
        self.setLayout(layout)

        # 设置窗口标题和大小
        self.setWindowTitle('音量控制')
        self.setGeometry(300, 300, 100, 200)

    def update_volume_label(self, value):
        self.volume_label.setText(f"音量: {value}")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建布局
        layout = QVBoxLayout()

        # 创建音量按钮
        self.volume_button = QPushButton("音量")
        self.volume_button.clicked.connect(self.show_volume_popup)

        # 将控件添加到布局中
        layout.addWidget(self.volume_button)

        # 设置窗口布局
        self.setLayout(layout)

        # 设置窗口标题和大小
        self.setWindowTitle('主窗口')
        self.setGeometry(300, 300, 300, 200)

    def show_volume_popup(self):
        self.volume_popup = VolumePopup(self)
        self.volume_popup.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
