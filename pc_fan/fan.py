from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from main import analyze_ports


class fan_widget(QWidget):
    # 设置消息信号
    data_changed_signal = pyqtSignal(object)

    # mess_signal=pyqtSignal(object)
    def __init__(self):
        super().__init__()

        # 设置组地址和基地址
        self.setWindowTitle("fan")
        self.g_address_input = QLineEdit(self)
        self.g_address_label = QLabel("组地址：")
        self.g_address_input.setFixedWidth(100)
        reg = QRegularExpression("^(?:\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$")  # 正则表达式范围 0~31
        validator = QRegularExpressionValidator()  # 创建validator
        validator.setRegularExpression(reg)  # 设置validator范围
        self.g_address_input.setValidator(validator)  # 对应的QLineEdit激活validator

        self.m_address_input = QLineEdit(self)
        self.m_address_label = QLabel("机地址：")
        self.m_address_input.setFixedWidth(100)
        reg1 = QRegularExpression("^(?:[0-9]|[1-2][0-9]|3[0-1])$")
        validator1 = QRegularExpressionValidator()
        validator1.setRegularExpression(reg1)
        self.m_address_input.setValidator(validator1)

        self.g_address_input.textChanged.connect(self.check_inputs)
        self.m_address_input.textChanged.connect(self.check_inputs)

        hbox2 = QHBoxLayout()
        hbox21 = QVBoxLayout()
        hbox22 = QVBoxLayout()
        hbox23 = QVBoxLayout()

        hbox21.addWidget(self.g_address_label)
        hbox21.addWidget(self.g_address_input)
        hbox22.addWidget(self.m_address_label)
        hbox22.addWidget(self.m_address_input)

        # 命令选择
        self.mapping = {
            "设置组地址": 10,
            "设置机地址": 20,
            "设置转数因子": 30,
            "查询故障状态": 40,
            "查询组地址": 50,
            "查询机地址": 60,
            "查询最高转速": 70,
            "设置风机转速": 80,
            "查询风机转速": 90,
            "重置风机": 100
        }
        self.order_label = QLabel("命令:", self)
        self.order_input = QComboBox(self)
        self.order_input.setFixedWidth(150)
        self.order_input.setEditable(False)
        for order in self.mapping.keys():
            self.order_input.addItem(order)

        hbox23.addWidget(self.order_label)
        hbox23.addWidget(self.order_input)

        hbox2.addLayout(hbox21)
        hbox2.addLayout(hbox22)
        hbox2.addLayout(hbox23)

        fan_box = QHBoxLayout()
        fan_speed_label = QLabel("风机转速:", self)
        self.fan_speed_input = QLineEdit(self)
        self.fan_speed_input.setFixedWidth(100)
        max_speed_label = QLabel("最高转速:", self)
        self.max_speed_input = QLineEdit(self)
        self.max_speed_input.setFixedWidth(100)
        # 故障状态
        fault_state = QLabel("故障状态:", self)
        self.fault_state_input = QLineEdit(self)
        self.fault_state_input.setFixedWidth(100)
        fan_box.addWidget(fan_speed_label)
        fan_box.addWidget(self.fan_speed_input)
        fan_box.addWidget(max_speed_label)
        fan_box.addWidget(self.max_speed_input)
        fan_box.addWidget(fault_state)
        fan_box.addWidget(self.fault_state_input)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        self.search_button = QPushButton("通信", self)
        # self.search_button.setFixedSize(100, 30)
        hbox3.addWidget(self.search_button)
        hbox3.addStretch(1)
        self.search_button.setEnabled(False)
        self.search_button.clicked.connect(self.send_message)

        # 结果显示
        self.result_label = QLabel("结果:", self)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["命令", "组地址", "机地址", "状态"])
        self.tableWidget.setGeometry(10, 10, 200, 200)
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox2)
        vbox.addLayout(fan_box)
        vbox.addLayout(hbox3)
        vbox.addWidget(self.result_label)
        vbox.addWidget(self.tableWidget)
        self.setLayout(vbox)

    def check_inputs(self):  # 检测两个文本框是否有内容

        text1 = self.g_address_input.text()
        text2 = self.m_address_input.text()

        if text1 and text2:
            self.search_button.setEnabled(True)
        else:
            self.search_button.setEnabled(False)

    def send_message(self):  # 根据命令发送信息

        selected_option = self.order_input.currentText()
        selected_value = int(self.mapping.get(selected_option))

        if selected_value == 10:  # 设置组地址
            message = self.message(0x55, 0xc0)
        elif selected_value == 20:  # 设置机地址
            message = self.message(0x55, 0xc0)
        elif selected_value == 30:  # 设置转数因子
            message = self.message(0x55, 0xc0)
        elif selected_value == 40:  # 查询故障状态
            message = self.message(0x35, 0x00)
        elif selected_value == 50:  # 查询组地址
            message = self.message(0x35, 0xe0)
        elif selected_value == 60:  # 查询机地址
            message = self.message(0x35, 0xe0)
        elif selected_value == 70:  # 查询最高转速
            message = self.message(0x35, 0xe0)
        elif selected_value == 80:  # 设置风机转速
            message = self.message(0x35, 0x40)
        elif selected_value == 90:  # 查询风机转速
            message = self.message(0x15, 0x20)
        elif selected_value == 100:  # 重置风机
            message = self.message(0x15, 0x20)

        self.add_table(message)

    def add_table(self, message):  # 在显示的表格里增加通信数据
        rows = self.tableWidget.rowCount()
        option = self.order_input.currentText()
        message = str(bin(message))
        self.tableWidget.insertRow(rows)
        self.tableWidget.setItem(rows, 0, QTableWidgetItem(option))
        self.tableWidget.setItem(rows, 2, QTableWidgetItem(self.m_address_input.text()))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(self.g_address_input.text()))
        self.tableWidget.setItem(rows, 3, QTableWidgetItem(message))
        data = (self.m_address_input.text(), self.g_address_input.text(), option)
        self.data_changed_signal.emit(data)
    # 报文的发送处理函数

    def message(self, head, order):
        numbers = [head]
        b = order + int(self.m_address_input.text())
        numbers.append(b)
        numbers.append(int(self.g_address_input.text()))
        # 具体命令
        numbers.append(0x00)
        numbers.append(29)
        c = 0xff
        for a in numbers:
            c ^= a
        numbers.append(c)
        message_re = " ".join([format(i, '02X') for i in numbers])
        analyze_ports(message_re)

        # self.mess_signal.emit(numbers)

        return numbers[-1]


if __name__ == "__main__":
    app = QApplication([])
    window = fan_widget()
    window.show()
    app.exec()
