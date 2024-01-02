import sys, serial

from serial.tools import list_ports
from PyQt6.QtWidgets import QApplication, QMainWindow, \
    QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QPushButton, QWidget, QTableWidget, QComboBox, \
    QMessageBox, QTableWidgetItem, QAbstractItemView


class PortWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        '''ui图形界面'''
        self.setWindowTitle("串口通信")
        self.setFixedSize(300, 350)
        self.port_label = QLabel("串口:", self)
        # 检测串口
        self.combo_box = QComboBox()
        self.combo_box.setEditable(False)  # 不允许手动输入
        # 比特率选项
        self.rate_box=QComboBox()
        self.rate_box.addItems(["9600", "115200"])
        self.port_button = QPushButton("串口连接", self)
        self.port_button.clicked.connect(self.connect_port)

        hbox1 = QVBoxLayout()
        hbox1.addWidget(self.combo_box)
        hbox1.addWidget(self.rate_box)
        hbox1.addWidget(self.port_button)

        com_ports = list_ports.comports()  # 列出当前所有串口

        for com in com_ports:  # com[0]，串口号
            self.combo_box.addItem(com[0])

        self.result_label = QLabel("结果:", self)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["串口", "通信状态"])
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        vbox = QVBoxLayout()
        vbox.addWidget(self.port_label)
        vbox.addLayout(hbox1)
        vbox.addWidget(self.result_label)
        vbox.addWidget(self.tableWidget)
        central_widget = QWidget(self)
        central_widget.setLayout(vbox)

        self.setCentralWidget(central_widget)
        self.show()

    def connect_port(self):
        if self.combo_box.currentText():
            self.ser = serial.Serial(self.combo_box.currentText(), self.rate_box.currentText())
            if self.ser.is_open():
                self.add_table("串口已打开")
            else:
                self.add_table("串口未打开")

        QMessageBox.warning(self, "警告对话框", "串口链接失败", QMessageBox.StandardButton.Yes)

    def add_table(self, message):  # 在显示的表格里增加通信数据
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)
        self.tableWidget.setItem(rows, 0, QTableWidgetItem(self.combo_box.currentText()))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(message))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PortWindow()
    sys.exit(app.exec())
