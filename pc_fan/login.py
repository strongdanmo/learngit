import sys

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from reportlab.lib.pagesizes import letter,A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import PageBreak

from fan import fan_widget
from port import PortWindow
from detection import detection_widget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        '''ui图形界面'''
        self.setWindowTitle("串口通信")
        self.setWindowIcon(QIcon("images\\TEBA.ico"))
        self.resize(500, 300)
        # 一级菜单
        self.main_menu = self.menuBar()  # 获取主窗口菜单
        self.file_menu = self.main_menu.addMenu("FILE")  # 主窗口菜单添加文件菜单
        self.edit_menu = self.main_menu.addMenu("EDIT")
        self.tool_menu = self.main_menu.addMenu("TOOL")
        self.settings_menu = self.main_menu.addMenu("SETTINGS")
        self.help_menu = self.main_menu.addMenu("HELP")

        new_action = QAction("新建", self)
        open_action = QAction(QIcon("images\\cpu_page.png"), "探测", self)
        port_open_action = QAction(QIcon("images\\lightning.png"), "port", self)
        port_open_action.triggered.connect(self.open_port)
        tool_bar_file = self.addToolBar("FILE")  # 主窗口添加文件工具栏

        tool_bar_file.addAction(new_action)
        tool_bar_file.addAction(open_action)
        tool_bar_file.addAction(port_open_action)

        # # ============== 状态栏 ===============
        # self.status_bar = QStatusBar()  # 状态栏实例
        # self.setStatusBar(self.status_bar)  # 主窗口添加状态栏

        # 创建一个QTreeWidget对象
        self.tree = QTreeWidget()
        self.tree.setFixedWidth(150)
        self.tree.setHeaderLabel("fans")
        # 设置QTreeWidget的上下文菜单策略为自定义,双击编辑按钮重命名
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.itemDoubleClicked.connect(self.edit_item)
        # 将QTreeWidget的customContextMenuRequested信号连接到self.open_menu槽函数
        # self.tree.customContextMenuRequested.connect(self.open_menu)

        self.stacked_widget = QStackedWidget()

        layout = QHBoxLayout()
        layout.addWidget(self.tree)
        layout.addWidget(self.stacked_widget)

        # 创建一个QWidget对象作为容器
        container = QWidget()
        container.setLayout(layout)

        # 将容器设置为主窗口的中央部件
        self.setCentralWidget(container)
        # 初始化树窗口
        self.init_ui()

    def init_ui(self):
        # 添加一些初始项
        root_item = QTreeWidgetItem(self.tree, ["fans detection"])
        history_item = QTreeWidgetItem(self.tree, ["history"])
        self.create_detection_page(root_item)
        self.create_history_page(history_item)
        # 当选择树项时，切换到对应的页面
        self.tree.itemSelectionChanged.connect(self.change_page)

    def create_history_page(self, item):
        # 创建历史界面
        history_page = QWidget()
        history_layout = QVBoxLayout()
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["time", "组地址", "机地址", "事件"])
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        pdfButton = QPushButton("Generate_PDF")
        history_layout.addWidget(self.tableWidget)
        history_layout.addWidget(pdfButton)
        history_page.setLayout(history_layout)

        # 将历史界面添加到堆叠窗口
        self.stacked_widget.addWidget(history_page)
        # 将历史项与对应的界面关联
        item_index = self.stacked_widget.count() - 1
        item.setData(0, Qt.ItemDataRole.UserRole, item_index)

    def create_detection_page(self, item):
        detection = detection_widget()
        detection.detection_signal.connect(self.add_fan_page)
        self.stacked_widget.addWidget(detection)
        # 将历史项与对应的界面关联
        item_index = self.stacked_widget.count() - 1
        item.setData(0, Qt.ItemDataRole.UserRole, item_index)

    # 通过信号在history的表格里增加通信数据
    def add_history(self, data):
        for i in range(20):
            m, g, s = data
            rows = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rows)
            current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(current_time))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(m))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(g))
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(s))

    def add_fan_page(self, data):
        m,g=data
        new_fan_item = QTreeWidgetItem(self.tree, [f"组{m}_机{g}"])
        self.add_page(new_fan_item, f"{g}", f"{m}")

    # def open_menu(self, position):
    #     selected_item = self.tree.currentItem()
    #     if selected_item and selected_item.data(0, Qt.ItemDataRole.UserRole) == 0:
    #         menu = QMenu()
    #         add_action = menu.addAction('Add fan')
    #         # add_action2 = menu.addAction('Add Root')
    #         action = menu.exec(self.tree.viewport().mapToGlobal(position))
    #         if action == add_action:
    #             selected_item = self.tree.currentItem()
    #             if not selected_item.parent():
    #                 child_count = selected_item.childCount()
    #                 new_child_item = QTreeWidgetItem(selected_item, [f'Child fan {child_count + 1}'])
    #                 new_child_item.setFlags(new_child_item.flags() | Qt.ItemFlag.ItemIsEditable)  # 重命名可编辑
    #                 self.add_page(new_child_item, f'{child_count + 1}', f'{child_count + 1}')
    #         # if action == add_action2:
            #     root_count = self.tree.topLevelItemCount()
            #     new_root_item = QTreeWidgetItem(self.tree, [f'Root Item {root_count + 1}'])
    def open_port(self):
        self.port_window = PortWindow()

    def edit_item(self, item, column):
        # 启动编辑
        self.tree.editItem(item, column)

    def add_page(self, item, text1, text2):
        a = QWidget()
        page = fan_widget()
        layout = QVBoxLayout()
        page.m_address_input.setText(text1)
        page.g_address_input.setText(text2)
        layout.addWidget(page)
        a.setLayout(layout)
        page.data_changed_signal.connect(self.add_history)
        self.stacked_widget.addWidget(a)
        # 将新页面与树项关联
        item.setData(0, Qt.ItemDataRole.UserRole, self.stacked_widget.count() - 1)

    # 变化视图
    def change_page(self):
        selected_items = self.tree.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            page_index = selected_item.data(0, Qt.ItemDataRole.UserRole)
            if page_index is not None:
                self.stacked_widget.setCurrentIndex(page_index)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("登录窗口")
        self.setWindowIcon(QIcon("images\TEBA.ico"))
        self.resize(300, 200)
        self.setFixedSize(self.width(), self.height())

        self.username_label = QLabel("用户名：", self)
        self.username_label.move(50, 50)
        self.username_lineedit = QLineEdit(self)
        self.username_lineedit.move(100, 50)

        self.password_label = QLabel("密码：", self)
        self.password_label.move(50, 100)
        self.password_lineedit = QLineEdit(self)
        self.password_lineedit.move(100, 100)

        self.login_button = QPushButton("登录", self)
        self.login_button.move(150, 150)

        self.login_button.clicked.connect(self.login)

    def login(self):
        username = self.username_lineedit.text()
        password = self.password_lineedit.text()

        if username == "" and password == "":
            self.hide()
            self.main_window = MainWindow()
            self.main_window.show()
        else:
            QMessageBox.warning(self, "错误", "用户名或密码错误")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec())
