from PyQt5.QtWidgets import  QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout ,QWidget, QVBoxLayout,QPushButton,QSpacerItem,QSizePolicy, QListWidget,QSlider ,QListWidgetItem,QScrollArea,QFileDialog,QStackedWidget,QToolButton,QMenu, QAction,QLineEdit,QDialog
from PyQt5.QtCore import Qt, QSize,QTimer ,QDateTime
from PyQt5.QtGui import QPixmap, QIcon,QMouseEvent
import os
from PIL import Image
from PyQt5.QtMultimedia import QMediaPlayer
from title_layout import Title_Form, Qss1
import pygame
import random
import shutil
from music_generator import generate
import ctypes
#* 设置全局变量
SetMasterVolume = ctypes.windll.winmm.waveOutSetVolume
# 获取主音量的函数，重新声明以确保参数和返回值类型正确
GetMasterVolume = ctypes.windll.winmm.waveOutGetVolume
GetMasterVolume.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_ulong)]
GetMasterVolume.restype = ctypes.c_ulong
# 音量范围是0 - 65535
VOLUME_RANGE = 65535
# 创建一个全局变量,用于存储音乐列表
current_index = 0
is_open = False
# 提取音乐文件
music_folder = "data/midi_songs"
icon_folder = "data/music_photo" 
music_files = []
icon_files = []
for root, dirs, files in os.walk(music_folder):
    for file in files:
        if file.endswith(('.mp3', '.wav', '.flac', '.mid', '.midi')):
            music_path = os.path.join(root, file)
            music_files.append(music_path)
for icons_root, icon_dirs, icons_files in os.walk(icon_folder):
    for icon in icons_files:
        if icon.endswith(('.jpg', '.png', '.jpeg')):
            icon_path = os.path.join(icons_root, icon)
            icon_files.append(icon_path)
music_names = [os.path.splitext(os.path.basename(file))[0] for file in music_files]
Match_name_dict = dict(zip([i for i in range(len(music_files))],music_names))
random.seed(66)
random_icon  = [random.choice(icon_files) for _ in range(len(music_files))]
random_icon_tuple  = list(zip([i for i in range(len(music_files))],random_icon))
Match_picture  = dict(random_icon_tuple)
Match_picture_dict_by_music_path  = dict(zip(music_files,random_icon_tuple))
#创建链接字典


class MusicGeneratorApp(Title_Form):
    def __init__(self):
        super().__init__()
        self.main_widget_2.setStyleSheet(Qss2)
        self.label_2.setText("无语音乐")
        self.main_layout_2 = QHBoxLayout(self.main_widget_2)
        self.main_layout_2.setSpacing(0)
        self.main_layout_2.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setMinimumSize(100, 100)  
        self.stacked_widget.setMaximumSize(100, 100)  
        self.stacked_widget.addWidget(QWidget()) 
        self.add_always_on_top_button(True)
        self.add_minimum_button(True)
        self.add_close_button(True)
    #* 设置图标
        self.set_icon("data\page_plug_in_information\outline-music-circle.png")
    #* 按钮
        button_height = 50  
        button_width = 150
        # 创建一个垂直布局容器，用于放置按钮
        button_widget = QWidget(self.main_widget_2)
        button_widget.setObjectName("button_widget")
        button_widget.setMinimumSize(QSize(50,150))
        button_widget.setMaximumSize(QSize(300,2000))
        button_layout = QVBoxLayout(button_widget)
        button_layout.setContentsMargins(10, 50, 0, 0)
        button_layout.setSpacing(60) 
        #一共有四个按钮
        self.file_input_button = QPushButton("输入文件🔜", self)  
        self.file_input_button.setObjectName("输入文件")
        self.file_input_button.setFixedSize(button_width,button_height)  
        self.file_input_button.clicked.connect(self.open_file_input_window)
        button_layout.addWidget(self.file_input_button)

        self.generate_button = QPushButton("生成音乐🤖", self)
        self.generate_button.setObjectName("生成音乐")
        self.generate_button.setFixedSize(button_width, button_height)  
        self.generate_button.clicked.connect(self.open_music_generator_window)
        button_layout.addWidget(self.generate_button)
    

        self.change_bg_button = QPushButton("更改背景🐊", self)
        self.change_bg_button.setObjectName("更改背景")
        self.change_bg_button.setFixedSize(button_width, button_height) 
        self.change_bg_button.clicked.connect(self.open_background_selection_window)
        button_layout.addWidget(self.change_bg_button)
        
        self.show_music = QPushButton("音乐展示😽",self)
        self.show_music.setObjectName("音乐展示")
        self.show_music.setFixedSize(button_width,button_height)
        self.show_music.clicked.connect(self.show_music_in_window)
        button_layout.addWidget(self.show_music)
        self.main_layout_2.addWidget(button_widget) 
        #调整按键位置
        button_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.spacer_widget = QWidget(self.main_widget_2)
        self.spacer_widget.setObjectName("spacer_widget")
        self.spacer_widget.setMinimumSize(QSize(700, 100))
        self.spacer_widget.setMaximumSize(QSize(700, 100))
        self.space_layout = QVBoxLayout(self.spacer_widget)
        self.main_layout_2.addWidget(self.spacer_widget)
        # 设置右边区域
        self.right_widget = QWidget()
        self.right_widget.setObjectName('right_widget')
        self.right_widget.setMinimumSize(QSize(200,850))
        self.right_widget.setMaximumSize(QSize(1000,850))
        self.right_layout = QHBoxLayout(self.right_widget)
        self.time_label = QLabel(self)
        self.time_label.setWordWrap(True)
        self.time_label.setObjectName('time_label') 
        self.time_label.setMaximumSize(QSize(200,100))
        self.time_label.setMinimumSize(QSize(200,100))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.right_layout.addWidget(self.time_label)
        self.right_layout.setContentsMargins(0,0,0,750)
        self.main_layout_2.addWidget(self.right_widget)
       
    
#! 设置第三个区域
        # 下半部分的布局
        lower_widget = QWidget()
        lower_widget.setObjectName('lower_widget')
        lower_widget.setBaseSize(1200,100)
        lower_layout = QHBoxLayout(lower_widget)
        #播放音乐按钮
        self.play_button = QPushButton()
        self.play_button.setMinimumSize(QSize(40, 40))
        self.play_button.setIcon(QIcon(Match_picture[current_index]))
        self.play_button.clicked.connect(self.open_Music_player)
        # 插件区域左边的Label
        self.lower_left_label = QLabel()
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum) 
        self.love_button = self.create_button(r"data\page_plug_in_information\1_music89.png", "喜欢")
        self.prev_button = self.create_button(r"data\page_plug_in_information\1_music83.png", "上一首")
        self.play_pause_button  = self.create_button(r"data\page_plug_in_information\1_music81.png", "播放/暂停")
        self.next_button = self.create_button(r"data\page_plug_in_information\1_music82.png", "下一首")
        self.play_mode_button = self.music_mode(r'data\page_plug_in_information\1_music80.png')
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  # 添加占位符
        self.volume_slider = self.create_button("data\page_plug_in_information\声音_实体.png", "音量")
        self.list_button = self.create_button("data\page_plug_in_information\music-list.png", "列表")
        self.love_button.clicked.connect(MusicHelper.add_to_playlist)
        self.prev_button.clicked.connect(MusicHelper.play_previous)
        self.prev_button.clicked.connect(self.change_icon_and_text)
        self.play_pause_button.clicked.connect(self.open_and_close)
        self.play_pause_button.clicked.connect(self.change_icon_and_text)
        self.next_button.clicked.connect(MusicHelper.play_next)
        self.next_button.clicked.connect(self.change_icon_and_text)
        self.volume_slider.clicked.connect(self.show_volume_popup)
        lower_layout.addWidget(self.play_button)
        lower_layout.addWidget(self.lower_left_label)
        lower_layout.addItem(spacerItem)
        lower_layout.addWidget(self.love_button)
        lower_layout.addWidget(self.prev_button)
        lower_layout.addWidget(self.play_pause_button)
        lower_layout.addWidget(self.next_button)
        lower_layout.addWidget(self.play_mode_button)
        lower_layout.addItem(spacerItem)
        lower_layout.addWidget(self.volume_slider)
        lower_layout.addWidget(self.list_button)
        lower_layout.setStretch(0, 1)
        lower_layout.setStretch(1, 1)
        lower_layout.setStretch(2, 5)
        lower_layout.setStretch(3, 1)
        lower_layout.setStretch(4, 1)
        lower_layout.setStretch(5, 1)
        lower_layout.setStretch(6, 1)
        lower_layout.setStretch(7, 1)
        lower_layout.setStretch(8, 7)
        lower_layout.setStretch(9, 1)
        lower_layout.setStretch(10, 1)
         # 将下半部分布局添加到主布局
        self.main_layout.addWidget(lower_widget)
# 设置主页面的布局
        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 20)
        self.main_layout.setStretch(2, 1) 
#! 音量控制
    def show_volume_popup(self):
        self.volume_popup = VolumePopup(self)
        self.volume_popup.show()
#!更新时间
    def update_time(self):
        current_time = QDateTime.currentDateTime().toString('hh:mm:ss')
        self.time_label.setText(current_time)

#! 按键控制
    def open_and_close(self):
        global is_open
        if is_open:
            self.play_pause_button.setIcon(QIcon(r"data\page_plug_in_information\1_music81.png"))
            pygame.mixer.init()
            pygame.mixer.music.stop()
        else:
            self.play_pause_button.setIcon(QIcon(r"data\page_plug_in_information\播放音乐未点击.png"))
            MusicHelper.play_music()
        is_open = not is_open
    def change_icon_and_text(self):
        self.play_button.setIcon(QIcon(Match_picture[current_index]))
        self.play_button.setIconSize(QSize(self.play_button.size()))
        self.lower_left_label.setText(Match_name_dict[current_index])
#! 创建按钮
    def create_button(self, icon_path, tool_tip,parent =None):
            button = QPushButton(parent)
            button.setToolTip(tool_tip)
            button.setMinimumSize(QSize(40, 40))
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(button.size()))  
            return button
#!打开二级界面-更改页面背景
    def open_background_selection_window(self):
        self.bg_selection_window = BackgroundSelectionWindow()
        self.bg_selection_window.show()
#!打开二级界面-输入文件
    def open_file_input_window(self):
        self.file_input_window = FileInputWindow()
        self.file_input_window.show()
#!设置背景图片
    def set_background(self, image_path):
        try:
            pixmap = Image.open(image_path)
            window_width = self.main_widget_2.width()
            window_height = self.main_widget_2.height()
            scaled_image = pixmap.resize((window_width, window_height), Image.Resampling.LANCZOS)
            temp_image_path = "temp_background.png"
            scaled_image.save(temp_image_path, format='PNG' if image_path.lower().endswith('.png') else 'JPEG')
            style_sheet = f"QWidget[objectName='main_widget_2']{{background-image: url({temp_image_path}); background-repeat: no-repeat; background-position: center; }}"
            self.setStyleSheet(style_sheet)
            self.update()
            os.remove(temp_image_path)
        except Exception as e:
            print(f"设置背景图片失败: {str(e)}")
#! 回到原始界面
    def back_to_main_window(self):
        self.main_widget_2.setStyleSheet(Qss1)
#! 打开生成音乐页面
    def show_music_in_window(self):
        self.music = MusicShow()
        self.music.show()
#! 打开生成音乐的二级界面
    def open_music_generator_window(self):
        self.music_generator_window = MusicGeneratorWindow()
        self.music_generator_window.show()
#! 设置图标
    def set_icon(self, icon_path):
        self.label_picture_path = icon_path
        self._label_picture = QPixmap(self.label_picture_path)
        self.label_1.setPixmap(self._label_picture)
        self.label_1.setScaledContents(True)
#!  音乐模式
    def music_mode(self,picture_path):
        button1 = QToolButton(self)
        button1.setMinimumSize(QSize(40, 40))
        button1.setIcon(QIcon(picture_path))
        button1.setIconSize(QSize(button1.size()))
        button1.setPopupMode(QToolButton.InstantPopup)  # 设置弹出模式为即时弹出
        # 创建QMenu并添加三个QAction
        menu = QMenu(button1)
        action1 = QAction("选项1", self)
        action2 = QAction("选项2", self)
        action3 = QAction("选项3", self)
        menu.addAction(action1)
        menu.addAction(action2)
        menu.addAction(action3)
        # 设置QToolButton的菜单
        button1.setMenu(menu)
        return button1
    def open_Music_player(self):
        self.music_player = Music_player(self)
        self.music_player.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  
        self.music_player.show()
        self.music_player.parent_widget = self  

#* 二级界面用来更改背景图片
class BackgroundSelectionWindow(Title_Form):
    def __init__(self):
        super().__init__()
        self.main_widget.resize(1000, 700)
        self.add_always_on_top_button(False)
        self.add_minimum_button(False)
        self.add_close_button(True)
        self.main_layout_2 = QVBoxLayout(self.main_widget_2)
        self.main_layout_2.setSpacing(0)
        self.main_layout_2.setContentsMargins(0, 0, 200, 0)
        self.list_widget = QListWidget()
        self.load_background_images()
        self.list_widget.itemClicked.connect(self.change_background)
        self.main_layout_2.addWidget(self.list_widget)
        # 添加还原按钮
        self.reset_button = QPushButton("还原原始背景", self)
        self.reset_button.setObjectName("reset_button")
        self.reset_button.setFixedSize(200, 50)
        self.reset_button.setContentsMargins(500,10,10,300)
        self.reset_button.clicked.connect(self.reset_background)
        self.main_layout_2.addWidget(self.reset_button)
    def load_background_images(self):
        background_folder = "data\Background_photo"
        if not os.path.exists(background_folder):
            os.makedirs(background_folder)
        for filename in os.listdir(background_folder):
            if filename.endswith((".png", ".jpg", ".jpeg", ".bmp",".webp")):
                item = QListWidgetItem(filename)
                item.setSizeHint(QSize(200, 100))
                item.setData(Qt.UserRole, os.path.join(background_folder, filename))
                self.list_widget.addItem(item)
                # 设置图标
                icon = QIcon(item.data(Qt.UserRole))
                item.setIcon(icon)
    def change_background(self, item):
        image_path = item.data(Qt.UserRole)
        # 通过全局变量更新主窗口背景
        global main_widget
        main_window.set_background(image_path)
    def reset_background(self):
        main_window.back_to_main_window()
#*二级界面用于传入文件
class FileInputWindow(Title_Form):
    def __init__(self):
        super().__init__()  
        self.main_widget.resize(700, 500)  
        self.main_layout_2 = QVBoxLayout(self.main_widget_2)
        self.main_layout_2.setSpacing(0)
        self.main_layout_2.setContentsMargins(0, 0, 500, 0)
        label = QLabel("请点击按钮选择文件")
        label.setAlignment(Qt.AlignCenter)
        label2 = QLabel('输入的文件类型为mid,会这是png等图片类型的文件')
        label2.setStyleSheet('{font-size:5px,color:black}')
        label2.setAlignment(Qt.AlignCenter)
        self.main_layout_2.addWidget(label)
        self.main_layout_2.addWidget(label2)
        button = QPushButton("选择文件")
        button_layout = QHBoxLayout()
        button.setMaximumWidth(200)
        button_layout.addWidget(button)
        button.clicked.connect(self.open_file_dialog)
        self.main_layout_2.addLayout(button_layout)
    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*);;Python Files (*.py)", options=options)
        if file_path:
            self.label.setText(f"已加载文件: {file_path}")
            # 在这里可以添加后续处理逻辑

#* 二级界面音乐展示
class MusicShow(Title_Form):
    def __init__(self):
        self.num = 1
        super().__init__()
        self.main_widget.resize(700, 500)
        self.init_ui()
    def init_ui(self):
        self.main_layout_2 = QVBoxLayout(self.main_widget_2)
        self.main_layout_2.setSpacing(0)
        self.main_layout_2.setContentsMargins(0, 0, 0, 0)
        self.scroll_area = QScrollArea()
        self.scroll_area.setFixedSize(700, 500)
        self.scroll_area.setStyleSheet("background-color:#000000;")
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(0)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.load_music()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout_2.addWidget(self.scroll_area)
    def load_music(self):
        for music_path in music_files:
            def create_open_and_close(music_path):
                def open_and_close():
                    global is_open
                    if is_open:
                        pygame.mixer.init()
                        pygame.mixer.music.stop()
                    else:
                        n_current_index = Match_picture_dict_by_music_path[music_path][0]
                        n_music_path = music_files[n_current_index]
                        pygame.mixer.init()
                        pygame.mixer.music.load(n_music_path)
                        pygame.mixer.music.play()
                    is_open = not is_open   
                return open_and_close
            open_and_close = create_open_and_close(music_path) 
            file_name = os.path.basename(music_path)
            #1
            widget = QWidget(self)
            widget_layout = QHBoxLayout(widget)
            widget_layout.setContentsMargins(10, 10, 10, 10)
            widget_layout.setSpacing(0)
            num_label = QLabel(f'{self.num}')
            #2
            widget_layout.addWidget(num_label, 0, Qt.AlignLeft)
            temp_label = QLabel()
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(temp_label.sizePolicy().hasHeightForWidth())
            temp_label.setSizePolicy(sizePolicy)
            temp_label.setFixedSize(70, 70)
            # 利用全局字典实现图片的匹配
            icon_path = Match_picture_dict_by_music_path[music_path][1]
            label_picture = QPixmap(icon_path)
            temp_label.setPixmap(label_picture)
            temp_label.setScaledContents(True)
            #3
            widget_layout.addWidget(temp_label, 0, Qt.AlignLeft)
            name_label = QLabel(file_name)
            name_label.setMaximumWidth(100)
            name_label.setMinimumWidth(70)
            name_label.setStyleSheet('color:rgb(255, 255, 255);font-size:9px')
            widget_layout.addWidget(name_label, 0, Qt.AlignLeft)
            #4
            spacerItem = QSpacerItem(500, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)
            widget_layout.addItem(spacerItem)
            #5
            button = QPushButton()
            button.setStyleSheet('''

            QPushButton{
                background-color: transparent;
                border: none;
            }
            QPushButton:hover{
                background-color:rgb(171, 26, 26);
            }
            ''')
            button.setMinimumSize(QSize(40, 40))
            button.setMaximumSize(QSize(40, 40))
            button.setIcon(QIcon(r'data\page_plug_in_information\1_music81.png'))
            button.setIconSize(QSize(button.size()))
            button.clicked.connect(open_and_close)
            widget_layout.addWidget(button)
            widget_layout.addStretch(1)
            widget_layout.addStretch(1)
            widget_layout.addStretch(1)
            widget_layout.addStretch(20)
            widget_layout.addStretch(1)
            self.scroll_layout.addWidget(widget)
            self.num += 1
        if not music_files:
            no_music_label = QLabel("没有找到音乐文件")
            self.scroll_layout.addWidget(no_music_label)
       
    

class Music_player(Title_Form):
    def __init__(self,parent= None):
        super().__init__(parent)
        # 上半部分布局
        self.main_layout_2= QHBoxLayout(self.main_widget_2)
        self.main_layout_2.setContentsMargins(0, 0, 0, 0)
        self.main_layout_2.setSpacing(0)
        # 上半部分左边的Label
        self.left_label = QLabel()
        self.left_label.setObjectName("left_label")
        self.left_label.setFixedSize(400, 400)
        pixmap = QPixmap(Match_picture[current_index])
        self.left_label.setPixmap(pixmap)
        self.main_layout_2.addWidget(self.left_label, alignment=Qt.AlignCenter)
        # 上半部分右边的两个Label
        right_layout = QVBoxLayout()
        song_label = QLabel("Pale Blue")
        lyric_label = QLabel("词: 米津玄师\n曲: 米津玄师\n我一直一直一直")
        right_layout.addWidget(song_label)
        right_layout.addWidget(lyric_label)
        self.main_layout_2.addLayout(right_layout)
        self.main_layout_2.setStretch(0,7)
        self.main_layout_2.setStretch(1,3)
         # 下半部分的布局
        lower_widget = QWidget()
        lower_widget.setBaseSize(1200,100)
        lower_layout = QHBoxLayout(lower_widget)
        #播放音乐按钮
        self.play_button = self.create_button(Match_picture[current_index], "播放")
        # 插件区域左边的Label
        self.lower_left_label = QLabel("Pale Blue")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum) 
        self.love_button = self.create_button(r"data\page_plug_in_information\1_music89.png", "喜欢")
        self.prev_button = self.create_button(r"data\page_plug_in_information\1_music83.png", "上一首")
        self.play_pause_button  = self.create_button(r"data\page_plug_in_information\1_music81.png", "播放/暂停")
        self.next_button = self.create_button(r"data\page_plug_in_information\1_music82.png", "下一首")
        self.play_mode_button = self.music_mode(r'data\page_plug_in_information\1_music80.png')
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum) 
        self.volume_slider = self.create_button("data\page_plug_in_information\声音_实体.png", "音量")
        self.list_button = self.create_button("data\page_plug_in_information\music-list.png", "列表")
        self.love_button.clicked.connect(MusicHelper.add_to_playlist)
        self.prev_button.clicked.connect(MusicHelper.play_previous)
        self.prev_button.clicked.connect(self.change_icon_and_text)
        self.play_pause_button.clicked.connect(self.open_and_close)
        self.play_pause_button.clicked.connect(self.change_icon_and_text)
        self.next_button.clicked.connect(MusicHelper.play_next)
        self.next_button.clicked.connect(self.change_icon_and_text)
        self.volume_slider.clicked.connect(self.show_volume_popup)
        lower_layout.addWidget(self.play_button)
        lower_layout.addWidget(self.lower_left_label)
        lower_layout.addItem(spacerItem)
        lower_layout.addWidget(self.love_button)
        lower_layout.addWidget(self.prev_button)
        lower_layout.addWidget(self.play_pause_button)
        lower_layout.addWidget(self.next_button)
        lower_layout.addWidget(self.play_mode_button)
        lower_layout.addItem(spacerItem)
        lower_layout.addWidget(self.volume_slider)
        lower_layout.addWidget(self.list_button)
        lower_layout.setStretch(0, 1)
        lower_layout.setStretch(1, 1)
        lower_layout.setStretch(2, 5)
        lower_layout.setStretch(3, 1)
        lower_layout.setStretch(4, 1)
        lower_layout.setStretch(5, 1)
        lower_layout.setStretch(6, 1)
        lower_layout.setStretch(7, 1)
        lower_layout.setStretch(8, 7)
        lower_layout.setStretch(9, 1)
        lower_layout.setStretch(10, 1)
         # 将下半部分布局添加到主布局
        self.main_layout.addWidget(lower_widget)
        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 20)
        self.main_layout.setStretch(2, 1)
    def show_volume_popup(self):
        self.volume_popup = VolumePopup(self)
        self.volume_popup.show()
    def open_and_close(self):
            global is_open
            if is_open:
                self.play_pause_button.setIcon(QIcon(r"data\page_plug_in_information\1_music81.png"))
                pygame.mixer.init()
                pygame.mixer.music.stop()
            else:
                self.play_pause_button.setIcon(QIcon(r"data\page_plug_in_information\播放音乐未点击.png"))
                MusicHelper.play_music()
            is_open = not is_open 
    def change_icon_and_text(self):
        self.play_button.setIcon(QIcon(Match_picture[current_index]))
        self.play_button.setIconSize(QSize(self.play_button.size()))
        self.lower_left_label.setText(Match_name_dict[current_index])
        pixmap = QPixmap(Match_picture[current_index])
        self.left_label.setPixmap(pixmap)
#! 创建按钮
    def create_button(self, icon_path, tool_tip,parent =None):
            button = QPushButton(parent)
            button.setToolTip(tool_tip)
            button.setMinimumSize(QSize(40, 40))
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(button.size()))  
            return button
    def music_mode(self,picture_path):
        button1 = QToolButton(self)
        button1.setMinimumSize(QSize(40, 40))
        button1.setIcon(QIcon(picture_path))
        button1.setIconSize(QSize(button1.size()))
        button1.setPopupMode(QToolButton.InstantPopup)  # 设置弹出模式为即时弹出
        # 创建QMenu并添加三个QAction
        menu = QMenu(button1)
        action1 = QAction("选项1", self)
        action2 = QAction("选项2", self)
        action3 = QAction("选项3", self)
        menu.addAction(action1)
        menu.addAction(action2)
        menu.addAction(action3)
        # 设置QToolButton的菜单
        button1.setMenu(menu)
        # 设置QToolButton样式，使其看起来像三个横向排列的按钮
        button1.setStyleSheet("""
            QToolButton {
               background-color: rgb(34, 45, 107);
         color: rgb(255, 255, 255);
         border: 2px solid rgb(46, 48, 58);
        #  border-radius: 15px;
         font-size: 20px;
         font-weight: bold;
         padding: 10px;
            }
                             QToolButton::menu-indicator {
                image: none; /* 隐藏菜单指示器 */
            }
        
        """)
        return button1
    def mousePressEvent(self, event):
        if self.parent_widget:  
            # 手动创建新的QMouseEvent对象并复制相关属性
            new_event = QMouseEvent(event.type(), event.localPos(), event.windowPos(),
                                    event.screenPos(), event.button(), event.buttons(),
                                    event.modifiers(), event.source())
            new_event.setAccepted(False) 
            self.parent_widget.mousePressEvent(new_event) 
            if new_event.isAccepted(): 
                return
        super().mousePressEvent(event) 

    def mouseMoveEvent(self, event):
        main_page = self.parentWidget()  
        if main_page:
            new_event = QMouseEvent(event.type(), event.localPos(), event.windowPos(),
                                    event.screenPos(), event.button(), event.buttons(),
                                    event.modifiers(), event.source())
            new_event.setAccepted(False)
            main_page.mouseMoveEvent(new_event)
            if new_event.isAccepted():
                return
    def mouseReleaseEvent(self, event):
        if self.parent_widget:
            new_event = QMouseEvent(event.type(), event.localPos(), event.windowPos(),
                                    event.screenPos(), event.button(), event.buttons(),
                                    event.modifiers(), event.source())
            new_event.setAccepted(False)
            self.parent_widget.mouseReleaseEvent(new_event)
            if new_event.isAccepted():
                return
        super().mouseReleaseEvent(event)
#* 创造二级界面进行音乐生成
class MusicGeneratorWindow(Title_Form):
    def __init__(self):
        super().__init__()
        self.main_widget.resize(700,500)
        self.main_layout_2 = QVBoxLayout(self.main_widget_2)
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("请输入歌曲名称")
        self.input_box.setFixedWidth(500)
        self.input_box.setFixedHeight(100)
        self.main_layout_2.addWidget(self.input_box)
        self.label = QLabel("音乐生成器", self.main_widget_2)
        self.main_layout_2.addWidget(self.label)
        # 根据传入音乐生成相近的音乐按钮
        self.similar_music_button = QPushButton("生成音乐", self)
        self.similar_music_button.setObjectName("similar_music_button")
        self.similar_music_button.setBaseSize(500,200)
        self.similar_music_button.setMaximumSize(QSize(500,200))
        self.similar_music_button.setMinimumSize(QSize(500,200))
        self.main_layout_2.addWidget(self.similar_music_button)
        self.similar_music_button.clicked.connect(self.generate_similar_music)
    def generate_similar_music(self):
        name  = self.input_box.text()
        file_path = r'data\midi_songs\{}.mid'.format(name)
        generate(file_path)
        global music_files, Match_name_dict,Match_picture_dict_by_music_path, Match_picture
        music_files.append(file_path)
        Match_name_dict[len(music_files)] = name
        random.seed(66)
        random_icon = [random.choice(icon_files) for _ in range(len(music_files))]
        random_icon_tuple  = list(zip([i for i in range(len(music_files))],random_icon))
        Match_picture  = dict(random_icon_tuple)
        Match_picture_dict_by_music_path  = dict(zip(music_files,random_icon_tuple))
#! 创建音量键小型界面// 这里的界面不是很好,下来有时间记得改
#????????????
#????????????
class VolumePopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        current_volume = self.get_current_volume()
        if current_volume is not None:
            self.volume_slider.setValue(int(current_volume / (VOLUME_RANGE / 100)))

    def initUI(self):
        layout = QVBoxLayout()
        self.volume_slider = QSlider()
        self.volume_slider.setOrientation(Qt.Vertical)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50) 
        self.volume_slider.valueChanged.connect(self.update_volume)
        self.volume_label = QLabel("音量: 50")
        layout.addWidget(self.volume_label)
        layout.addWidget(self.volume_slider)
        self.setLayout(layout)
        self.setWindowTitle('音量控制')
        self.setGeometry(300, 300, 100, 200)
    def update_volume(self, value):
        """
        根据滑块的值更新系统音量和音量标签显示
        """
        # 根据滑块值计算对应的音量范围值（0 - 65535）
        volume_value = int((value / 100) * VOLUME_RANGE)
        # 设置左右声道音量（在Windows下左右声道一起设置）
        left_right_volume = volume_value | (volume_value << 16)
        # 调用Windows API设置音量，添加错误处理
        result = SetMasterVolume(0, left_right_volume)
        if result == 0:
            self.volume_label.setText(f"音量: {value}")
        else:
            print(f"设置音量失败，错误码: {result}")

    def get_current_volume(self):
        """
        获取当前系统音量，添加更完善的错误处理
        """
        try:
            device_id = ctypes.c_uint(0)
            volume_ptr = ctypes.c_ulong()
            result = GetMasterVolume(device_id, volume_ptr)
            if result == 0:
                return volume_ptr.value
            else:
                print(f"获取音量失败，错误码: {result}")
                return None
        except Exception as e:
            print(f"获取音量出现异常: {str(e)}")
            return None

#! 辅助音乐播放栏
class MusicHelper:
    player = QMediaPlayer()  
    music_folder=r'data\midi_songs'
    love_folder = r'data\music'
    music_files = [f for f in os.listdir(music_folder) if f.endswith(('.mp3', '.midi', '.mid'))]
    @staticmethod
    def play_music():
        pygame.mixer.init()
        global current_index  
        if not MusicHelper.music_files:
            print("没有找到音乐文件")
            return
        if current_index >= len(MusicHelper.music_files):
            current_index = 0  # 如果超出范围，重置为第一首
        music_path = os.path.join(MusicHelper.music_folder, MusicHelper.music_files[current_index])
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()      
    @staticmethod
    def play_previous():
        global current_index ,is_open
        if current_index > 0:
            current_index -= 1
        MusicHelper.play_music()
        is_open   = True
    @staticmethod
    def play_next():
        global current_index ,is_open
        current_index += 1
        MusicHelper.play_music()
        is_open   = True
    @staticmethod
    def add_to_playlist():
        if not os.path.exists(MusicHelper.love_folder):
            os.makedirs(MusicHelper.love_folder)
        current_music = os.path.join(MusicHelper.music_folder, MusicHelper.music_files[current_index])    
        destination = os.path.join(MusicHelper.love_folder, MusicHelper.music_files[current_index])
        if not os.path.exists(destination):
            try:
                shutil.copy2(current_music, destination)
                print(f"已将 {MusicHelper.music_files[current_index]} 添加到播放列表")
            except Exception as e:
                print(f"添加到播放列表失败: {e}")
        else:
            print(f"{MusicHelper.music_files[current_index]} 已在播放列表中")


Qss2 = '''

 
     QPushButton{
         background-color: rgb(82, 86, 108);
         color: rgb(255, 255, 255);
         border: 2px solid rgb(46, 48, 58);
        #  border-radius: 15px;
         font-size: 20px;
         font-weight: bold;
         padding: 10px;
     }
   
 QLabel[objectName = 'time_label']{
            font-size: 35px;
            border: 1px solid black;
            border-radius: 5px;
            padding: 5px;
            background-color: #f0f0f0;
            color: #333;
     }

    

'''


    
   