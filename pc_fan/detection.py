import sys
import time

from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import pyqtSignal


class detection_widget(QWidget):
    detection_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        self.resize(200, 250)
        hbox = QHBoxLayout()
        # 创建垂直布局
        self.vbox = QVBoxLayout()
        # 创建第一个带标签的文本框（组地址）
        hbox1 = QHBoxLayout()
        self.label1 = QLabel('组地址:', self)
        self.textbox1 = QLineEdit(self)
        self.textbox1.setValidator(QIntValidator())  # 限制只能输入数字
        hbox1.addWidget(self.label1)
        hbox1.addWidget(self.textbox1)

        # 创建第二个带标签的文本框（机地址）
        hbox2 = QHBoxLayout()
        self.label2 = QLabel('机地址:', self)
        self.textbox2 = QLineEdit(self)
        self.textbox2.setValidator(QIntValidator())  # 限制只能输入数字
        hbox2.addWidget(self.label2)
        hbox2.addWidget(self.textbox2)

        # 将带标签的文本框布局添加到垂直布局中
        self.vbox.addLayout(hbox1)
        self.vbox.addLayout(hbox2)

        # 创建按钮1并添加到垂直布局中
        self.button1 = QPushButton('Generate Fans', self)
        self.button1.clicked.connect(self.generate_buttons)  # 连接按钮点击事件
        self.vbox.addWidget(self.button1)

        # 创建按钮2并添加到垂直布局中
        self.button2 = QPushButton('Detection Fans', self)
        self.button2.clicked.connect(self.enable_buttons)  # 连接按钮点击事件
        self.vbox.addWidget(self.button2)

        self.text = QTextEdit()
        self.text.setFixedWidth(200)
        hbox.addLayout(self.vbox)
        hbox.addWidget(self.text)

        # 设置窗口的主布局
        self.setLayout(hbox)

        # 设置窗口标题
        self.setWindowTitle('PyQt6 Dynamic Buttons')

        # 存储所有按钮的字典
        self.buttons_dict = {}
        self.grid_layout = None

    def generate_buttons(self):

        if self.grid_layout is not None:
            self.clear_layout(self.grid_layout)
        # 读取文本框中的数字

        group_number = self.textbox1.text()
        machine_number = self.textbox2.text()

        # 创建表格布局
        self.grid_layout = QGridLayout()
        # 根据输入的数字生成按钮
        try:
            group_count = int(group_number) % 256
            machine_count = int(machine_number) % 32
            for i in range(group_count):
                for j in range(machine_count):
                    button_text = f"{i + 1}_{j + 1}"
                    button = QPushButton(button_text, self)
                    button.setFixedSize(40, 30)
                    button.setObjectName(f"{i + 1}_{j + 1}")  # 设置按钮的objectName
                    button.setEnabled(False)  # 初始时按钮不可用
                    button.clicked.connect(self.button_clicked)
                    self.buttons_dict[button.objectName()] = button  # 将按钮添加到字典中
                    self.grid_layout.addWidget(button, i, j)
        except ValueError:
            # 如果输入不是数字，不做任何事情
            pass

        self.vbox.addLayout(self.grid_layout)


    def button_clicked(self):
        button_name = self.sender().objectName()
        m,g=button_name.split("_")
        data=(m,g)
        self.detection_signal.emit(data)

    def enable_buttons(self):

        a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        # 遍历列表并启用对应的按钮
        for i, row in enumerate(a):
            for j, val in enumerate(row):
                # 构造按钮的名称
                button_name = f"{i + 1}_{val}"
                # 找到对应的按钮并设置为可用
                if button_name in self.buttons_dict:
                    self.buttons_dict[button_name].setEnabled(True)
                    self.text.append(f"正在探测{button_name}")

    def clear_layout(self, layout):
        # 删除布局中的所有小部件
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = detection_widget()
    window.show()

    sys.exit(app.exec())
