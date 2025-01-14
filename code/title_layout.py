from PyQt5.QtWidgets import QApplication ,QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout ,QWidget, QVBoxLayout,QPushButton,QSpacerItem,QSizePolicy,QColorDialog, QListWidget, QListWidgetItem,QDesktopWidget
from PyQt5.QtCore import Qt,QRect,QSize
from PyQt5.QtGui import  QCursor,QIcon,QFont, QFontDatabase
import os
from PIL import Image
import sys


class Title_Form(QWidget):
    def __init__(self,parent=None):
       #!  初始化界面
        super().__init__(parent)
#! 设置字体
        font_path = "font\逐浪酷潮端黑体.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 12)
        QApplication.setFont(font)
        #*虽然是隐藏了,但是后面打包app的时候需要
        self.setWindowIcon( QIcon("code\icon.png"))
        # 隐藏默认标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)
         # 设置背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
#!重新创建主页面
        self.main_widget = QWidget(self)
        self.main_widget.setObjectName('main_widget')
        self.main_widget.setStyleSheet(Qss1)
        self.main_widget.resize(1200,800)
        #设置主插件的布局管理器
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
   #* 自定义标题栏       
        # 将主小插件设置为中心小部件显示
        self.title_widget = QWidget(self.main_widget)
        self.title_widget.setBaseSize(1200,40)
        self.title_widget.setMinimumSize(QSize(700,40))
        self.title_widget.setMaximumSize(QSize(41241,50))
        self.title_widget.setObjectName('title_widget')
        self.title_layout = QHBoxLayout(self.title_widget)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setSpacing(0)
        #*设置占位符
        spacerItem = QSpacerItem(10, 50, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.title_layout.addItem(spacerItem)       
    #*创建图标
        self.label_1 = QLabel( self.title_widget)
        self.label_1.setObjectName('label_1')
        sizePolicy = QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_1.sizePolicy().hasHeightForWidth())
        self.label_1.setSizePolicy(sizePolicy)
        self.label_1.setMaximumSize(QSize(40, 40))
        self.title_layout.addWidget(self.label_1)
        #*添加占位符
        spacerItem1 = QSpacerItem(10, 20,QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.title_layout.addItem(spacerItem1)
    #*设置标题
        self.label_2 = QLabel(self.title_widget)
        self.label_2.setObjectName('label_2')
        sizePolicy = QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.title_layout.addWidget(self.label_2)
        #*添加占位符
        spacerItem2 =  QSpacerItem(800,50,QSizePolicy.Maximum,QSizePolicy.Minimum)
        self.title_layout.addItem(spacerItem2)
    #*添加始终置顶按钮
        title_button_size = 30
        self.always_on_top = False 
        self.always_on_top_button = QPushButton("📌", self.title_widget)
        self.always_on_top_button.setObjectName('always_on_top_button')
        sizePolicy = QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.always_on_top_button.sizePolicy().hasHeightForWidth())
        self.always_on_top_button.setMinimumSize(QSize(title_button_size, title_button_size))
        self.always_on_top_button.setMaximumSize(QSize(title_button_size, title_button_size))
        self.always_on_top_button.setSizePolicy(sizePolicy)
        self.always_on_top_button.clicked.connect(self.toggle_always_on_top)
        #*添加占位
        self.spacerItem3 = QSpacerItem(10,50,QSizePolicy.Fixed,QSizePolicy.Fixed)
    #*添加最小化按钮
        self.minimize_button = QPushButton("-", self.title_widget)
        self.minimize_button.setObjectName('minimize_button')
        sizePolicy = QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.always_on_top_button.sizePolicy().hasHeightForWidth())
        self.minimize_button.setMinimumSize(QSize(title_button_size, title_button_size))
        self.minimize_button.setMaximumSize(QSize(title_button_size, title_button_size))
        self.minimize_button.setSizePolicy(sizePolicy)
        self.minimize_button.clicked.connect(self.showMinimized)
        #*添加占位符号
        self.spacerItem4 = QSpacerItem(10,50,QSizePolicy.Fixed,QSizePolicy.Fixed)
    #*添加关闭按钮
        self.close_button = QPushButton("x", self)
        self.close_button.setObjectName('close_button')
        sizePolicy = QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.always_on_top_button.sizePolicy().hasHeightForWidth())
        self.close_button.setMinimumSize(QSize(title_button_size, title_button_size))
        self.close_button.setMaximumSize(QSize(title_button_size, title_button_size))
        self.close_button.clicked.connect(self.close)

        # 将自定义标题栏添加到主布局
        self.main_layout.addWidget(self.title_widget)
        self.main_layout.setAlignment(self.title_widget, Qt.AlignTop)

#!设置设置第二个区域
        self.main_widget_2 = QWidget(self.main_widget)
        self.main_widget_2.setObjectName('main_widget_2')
        self.main_widget_2.setMinimumSize(QSize(1200,450))
        self.main_layout.addWidget(self.main_widget_2)


#! 增加页面功能,改变页面大小
        # 记录拖动状态
        self.dragging = False
        self.drag_position = None
        self.resizing = False
        self.resize_start_position = None
        self.resize_direction = None  
        # 设置鼠标事件
        self.title_widget.mouseMoveEvent = self.mouseMoveEvent
        self.title_widget.mousePressEvent = self.mousePressEvent
        self.title_widget.mouseReleaseEvent = self.mouseReleaseEvent     
   

#!设置鼠标
        self.title_widget.mouseMoveEvent = self.mouseMoveEvent
        self.title_widget.mousePressEvent = self.mousePressEvent
        self.title_widget.mouseReleaseEvent = self.mouseReleaseEvent

#!记录拖动状态                                                                       
        self.dragging = False
        self.drag_position = None
#? 鼠标事件
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_position)
        else:
            self.update_cursor(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(QCursor(Qt.ArrowCursor))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def update_cursor(self, pos):
        self.setCursor(QCursor(Qt.ArrowCursor))

#! 始终置顶
    def toggle_always_on_top(self):
        if self.always_on_top:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.always_on_top_button.setText("📌")  # 恢复原始图标
        else:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.always_on_top_button.setText("📍")  # 设置竖直向下的图钉图标
        self.always_on_top = not self.always_on_top
        self.show()
    def add_always_on_top_button(self,always_on_top_button):
        if always_on_top_button:
            self.title_layout.addWidget(self.always_on_top_button)
            self.title_layout.addItem(self.spacerItem3)
        else :
            spaceItem = QSpacerItem(30, 30, QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.title_layout.addItem(spaceItem)
            self.title_layout.addItem(self.spacerItem3)
    def add_minimum_button(self,minimum_button):
        if minimum_button:
            self.title_layout.addWidget(self.minimize_button)
            self.title_layout.addItem(self.spacerItem4)
        else :
            spaceItem = QSpacerItem(30, 30, QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.title_layout.addItem(spaceItem)
            self.title_layout.addItem(self.spacerItem4)
    def add_close_button(self,close_button):
        if close_button:
            self.title_layout.addWidget(self.close_button)
        else :
            spaceItem = QSpacerItem(30, 30, QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.title_layout.addItem(spaceItem)


Qss1 = """
    QPushButton[objectName = 'music_button']{
                 border-radius: 0;
                 background-color: rgb(39, 55, 66); 
            }
    QPushButton[objectName = 'music_button']:hover{
                background-color: rgb(74, 79, 74);
            }
             QWidget[objectName = 'button_widget']{
        background-color: rgb(1, 48, 58);
     }
            QWidget[objectName ='main_widget']{
             background-color: #ee897f;
             border-radius: 15px;
            }
            QWidget[objectName ='title_widget']{
             border-top-left-radius: 15px;
    border-top-right-radius:15px;
    background-color: #3c8ac4;
    color:rgb(255, 255, 255);
            }
            QWidget[objectName = 'main_widget_2']{
             background-color: #4ab3df;
    color:rgb(255, 255, 255);
            }
             QWidget[objectName = 'lower_widget']{
              background-color:#345ea7;
               color:rgb(215, 208, 208);
               border-radius: 10px;
             }
        
            QLabel {
                font-size: 24px;
                color: #FCE5BA;
            }
            QPushButton[objectName ='always_on_top_button']{
            background-color: rgb(121, 126, 126);
            border-radius: 15px;
            color: white;}
            QPushButton[objectName ='always_on_top_button']:hover{
             background-color: red;
            }
            QPushButton[objectName ='minimize_button']{
               background-color: rgb(177, 59, 59);
            border-radius: 15px;
        color: white;
            }
            QPushButton[objectName ='minimize_button']:hover{background-color: red;
            }
             QPushButton[objectName ='maximize_button']{background-color: rgb(52, 192, 49);
            border-radius: 15px;
        color: white;
             }
            QPushButton[objectName ='maximize_button']:hover{ background-color: red;
            }
            QPushButton[objectName ='close_button']{
            background-color: rgb(39, 212, 212);
            border-radius:15px;
        color: white;
            }
            QPushButton[objectName ='close_button']:hover{
             background-color: red;
            }
           
            * {
                font-size: 14px;
            }
           
"""