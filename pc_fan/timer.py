import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout
from PyQt6.QtCore import QTimer

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 存储所有按钮的字典
        self.buttons_dict = {}
        # 存储将要使能的按钮名称的队列
        self.buttons_to_enable = []
        # 创建定时器
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # 设置定时器间隔为1000毫秒（1秒）
        self.timer.timeout.connect(self.enable_next_button)  # 连接超时信号

        # 创建按钮网格布局
        self.grid_layout = QGridLayout(self)
        self.setLayout(self.grid_layout)
        self.create_buttons_grid()

    def create_buttons_grid(self):
        # 假设 a 是一个已经定义的二维列表
        a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        for i, row in enumerate(a):
            for j, val in enumerate(row):
                button_name = f"button_{i + 1}_{val}"
                button = QPushButton(button_name, self)
                button.setEnabled(False)  # 初始时按钮不可用
                self.buttons_dict[button_name] = button
                self.buttons_to_enable.append(button_name)  # 将按钮名称添加到队列
                self.grid_layout.addWidget(button, i, j)

        # 启动定时器
        self.timer.start()

    def enable_next_button(self):
        if self.buttons_to_enable:
            # 从队列中取出下一个按钮名称
            button_name = self.buttons_to_enable.pop(0)
            # 找到对应的按钮并使能
            if button_name in self.buttons_dict:
                self.buttons_dict[button_name].setEnabled(True)
        else:
            # 如果没有更多的按钮要使能，停止定时器
            self.timer.stop()

app = QApplication(sys.argv)
widget = MyWidget()
widget.show()
sys.exit(app.exec())
