from test_task import TabTestTask
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QMainWindow, QTabWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
# import os
# os.environ["QT_QPA_PLATFORM"] = "xcb"  # Use "xcb" for X11
# Сделать логарифмическую шкалу галочку
# Максимальное ОЛП в точке какой?


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Алпутов Иван ПМоп3")

        # Создание основного виджета QTabWidget
        self.tab_widget = QTabWidget()

        # Создание вкладок
        self.create_tabs()

        # Устанавливаем QTabWidget как центральный виджет
        self.setCentralWidget(self.tab_widget)

    def create_tabs(self):
        # Вкладка 1
        tab1 = TabTestTask()

        # Вкладка 2
        # tab2 = TabMainTask1()

        # tab3 = TabMainTask2()
        #layout2 = QVBoxLayout()
        #layout2.addWidget(QLabel("Содержимое второй вкладки"))
        #tab2.setLayout(layout2)

        # Добавляем вкладки в QTabWidget
        self.tab_widget.addTab(tab1, "Тестовая задача")
        # self.tab_widget.addTab(tab2, "Основная задача 1")
        # self.tab_widget.addTab(tab3, "Основная задача 2")

        # Можно добавить иконки к вкладкам, если нужно:
        # self.tab_widget.setTabIcon(0, QIcon('icon1.png'))

        # Можно изменять расп   оложение вкладок
        # self.tab_widget.setTabPosition(QTabWidget.West)
        pass


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.setMinimumSize(400, 600)
    window.show()

    app.exec()