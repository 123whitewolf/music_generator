

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form:QtWidgets.QWidget):
        # 主布局的名称
        Form.setObjectName("Form")
        # 设置主布局大小
        Form.resize(648, 432)
        # 给主布局上添加布局管理器-layout(竖直管理器,会将主布局上的小插件竖直排布)
        self.vLayout = QtWidgets.QVBoxLayout(Form) 
        # 设置主布局上的 边框分布
        self.vLayout.setContentsMargins(0, 0, 0, 0)
        # 设置主布局上的小插件之间的距离-(全局变量,将会是所有小插件的间距都是0)
        self.vLayout.setSpacing(0)
        # 给主布局布局管理器命名
        self.vLayout.setObjectName("vLayout")
#! 设置标题栏
        self.widget = QtWidgets.QWidget(Form)
        # 设置小插件大小,分别为最大宽度和最大高度
        self.widget.setMaximumSize(QtCore.QSize(16777215, 35))
        # 给小插件命名
        self.widget.setObjectName("widget")
        # 在这个小插件上面买添加水平布局管理器,这个可以说就是在准备标题了
        self.hLayout = QtWidgets.QHBoxLayout(self.widget)
        # 设置小插件在布局中距离布局四个边缘为距离
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.setSpacing(0)
        self.hLayout.setObjectName("hLayout")
#!添加占位符(在按钮之间添加一个宽为5,高为20的占位符,相当于文本输入中的空格,这个可以根据插件填入布局的顺序进行插入,可以自定义插件之间的距离.)
        spacerItem = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.hLayout.addItem(spacerItem)
#! 创建一个图标
        self.label = QtWidgets.QLabel(self.widget)
        
        # 固定小部件的大小
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # 添加水平拉伸因子,当布局中有多远的空白空间的时候就可以添加拉伸因子是的添加拉伸因子部分的插件进行拉伸
        sizePolicy.setHorizontalStretch(20)
        # 同理添加竖直拉伸因子
        sizePolicy.setVerticalStretch(20)
        # 小插件的高度,height是根据其宽度,width进行计算的,高度用过其宽度进行调整.has
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        # 设置刚才设置的大小关系
        self.label.setSizePolicy(sizePolicy)
        # 设置最大尺寸
        self.label.setMaximumSize(QtCore.QSize(20, 20))
        self.label.setObjectName("label")
        self.hLayout.addWidget(self.label)

#! 添加添加占位符
        spacerItem1 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.hLayout.addItem(spacerItem1)
#! 创建标题
        self.label_2 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())

        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.hLayout.addWidget(self.label_2)
#!添加占位符号
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hLayout.addItem(spacerItem2)
#!设置按钮
        self.pushButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton.setMaximumSize(QtCore.QSize(20, 20))
        self.pushButton.setObjectName("pushButton")
        self.hLayout.addWidget(self.pushButton)
#! 设置占位符号
        spacerItem3 = QtWidgets.QSpacerItem(8, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.hLayout.addItem(spacerItem3)
#! 添加按钮2
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMaximumSize(QtCore.QSize(20, 20))
        self.pushButton_2.setObjectName("pushButton_2")
        self.hLayout.addWidget(self.pushButton_2)
#! 添加占位符号
        spacerItem4 = QtWidgets.QSpacerItem(8, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.hLayout.addItem(spacerItem4)
#! 设置按钮3
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setMaximumSize(QtCore.QSize(20, 20))
        self.pushButton_3.setObjectName("pushButton_3")
        self.hLayout.addWidget(self.pushButton_3)
#! 设置占位符
        spacerItem5 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.hLayout.addItem(spacerItem5)
#! 将标题栏添加到主页面
        self.vLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(Form)
        self.widget_2.setObjectName("widget_2")
        self.vLayout.addWidget(self.widget_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "图标"))
        self.label_2.setText(_translate("Form", "TextLabel"))
        self.pushButton.setToolTip(_translate("Form", "<html><head/><body><p>最小化</p></body></html>"))
        self.pushButton.setText(_translate("Form", "-"))
        self.pushButton_2.setToolTip(_translate("Form", "<html><head/><body><p>最大化</p></body></html>"))
        self.pushButton_2.setText(_translate("Form", "O"))
        self.pushButton_3.setToolTip(_translate("Form", "<html><head/><body><p>关闭</p></body></html>"))
        self.pushButton_3.setText(_translate("Form", "X"))
