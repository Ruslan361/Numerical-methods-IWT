from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QCheckBox, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QFileDialog
import numpy as np
import sys
from report_generator import ReportGenerator
from PySide6.QtWidgets import QFileDialog
from test_task_ui import TestTaskUI
from test_task_plotter import TestTaskPlotter
from test_task_settings_manager import TestTaskSettingsManager
import os
import pandas as pd
from custom_loyauts import LatexRendererLayout, GraphLayout, IntNumberInput, NumericalIntegrationParametersInput, ScalarStartConditions, XlimitsInput, NewWindow, ErrorDialog
from calculator import RK4Calculator, RK4AdaptiveCalculator


class TabTestTask(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.settings_file = "test_task"  # Базовое имя файла без расширения
        self.df = None  # Переменная для хранения DataFrame
        self.to_be_control_local_error = False

        # Инициализируем калькуляторы с ссылкой на родителя
        self.rk4_calculator = RK4Calculator()
        self.rk4_adaptive_calculator = RK4AdaptiveCalculator()

        self.ui = TestTaskUI(self.main_layout)
        self.ui.setup_ui()
        self.plotter = TestTaskPlotter(self.ui.graph_layout, self.ui.show_numeric_solve_checkbox, self.ui.show_real_solve_checkbox)
        self.settings_manager = TestTaskSettingsManager(self.settings_file, {
            "initialConditions": self.ui.initial_conditions,
            "xlimitsInput": self.ui.xlimits_input,
            "numericalIntegrationParametersInput": self.ui.numerical_integration_parameters_input,
            "showNumericSolveCheckBox": self.ui.show_numeric_solve_checkbox,
            "showRealSolveCheckBox": self.ui.show_real_solve_checkbox,
            "amountOfStepsInput": self.ui.amount_of_steps_input,
            "omega_input": self.ui.omega_input,
            "R_input": self.ui.R_input,
            "L_input": self.ui.L_input,
            "E0_input": self.ui.E0_input,
            "parent": self
        })
        # self.loadSettings()  # Загрузка настроек после создания UI

    def calculateClick(self):
        # ... (код для получения параметров из UI)
        if self._validate_input():
            self._perform_calculation()
            #self.tryLoadResult(self.to_be_control_local_error)
            self.refreshPlot()

    def _validate_input(self):
        # ... (код для валидации входных данных)
        try:
            x_end = self.ui.xlimits_input.getEndX()
            x0 = self.ui.initial_conditions.getX0()
            amount_of_steps = self.ui.amount_of_steps_input.getIntNumber()
            h0 = self.ui.numerical_integration_parameters_input.getStartStep()
            local_error = self.ui.numerical_integration_parameters_input.getEpsilonLocalError()
        except ValueError as e:
            self.show_error(f"Ошибка: {e}")
            return False
        if x_end <= x0:
            self.show_error("Ошибка: Конечное значение X должно быть больше начального.")
            return False

        if amount_of_steps <= 0:
            self.show_error("Ошибка: Количество шагов должно быть положительным числом.")
            return False

        if h0 <= 0:
            self.show_error("Ошибка: Начальный шаг должен быть положительным числом.")
            return False

        if local_error <= 0:
            self.show_error("Ошибка: Допустимая локальная погрешность должна быть положительным числом.")
            return False

        return True  # Возвращаем True, если все данные валидны

    def _perform_calculation(self):
        try:
            # ... (код для выполнения вычислений)
            x_end = self.ui.xlimits_input.getEndX()
            x0 = self.ui.initial_conditions.getX0()
            u_x0 = self.ui.initial_conditions.getUX0()
            epsilon_border = self.ui.xlimits_input.getEndEpsilon()
            amountOfSteps = self.ui.amount_of_steps_input.getIntNumber()
            h0 = self.ui.numerical_integration_parameters_input.getStartStep()
            local_error = self.ui.numerical_integration_parameters_input.getEpsilonLocalError()
            self.to_be_control_local_error = self.ui.numerical_integration_parameters_input.isControlLocalError()
            L = self.ui.L_input.getFloatNumber()
            R = self.ui.R_input.getFloatNumber()
            E0 = self.ui.E0_input.getFloatNumber()
            omega = self.ui.omega_input.getFloatNumber()
            print(f"{self.to_be_control_local_error}")
            if self.to_be_control_local_error:
                self.df = self.rk4_adaptive_calculator.calculate(x0, u_x0, h0, x_end, local_error, epsilon_border, amountOfSteps, L, R, E0, omega)
            else:
                self.df = self.rk4_calculator.calculate(x0, u_x0, h0, x_end, amountOfSteps, L, R, E0, omega)
        except Exception as e:
            self.show_error(f"Ошибка во время вычислений: {e}")

    def refreshPlot(self):
        if self.df is not None:
            self.plotter.plot(self.getColumnValues(self.df, 'x'), self.getColumnValues(self.df, 'v'), self.getColumnValues(self.df, 'u'))

    # def closeEvent(self, event):
    #     self.saveSettings()
    #     event.accept()

    def ShowTableButtonClick(self):
        if self.df is None:
            self.show_error("Ошибка: Сначала необходимо выполнить вычисления.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Таблица результатов")
        layout = QVBoxLayout(dialog)
        table = QTableWidget()
        layout.addWidget(table)

        if self.ui.numerical_integration_parameters_input.isControlLocalError():
            self.columns = ['x', 'v', 'v2i', 'v-v2i', 'e', 'h', 'c1', 'c2', 'u', '|ui-vi|']
        else:
            self.columns = ['x', 'v', 'u', '|ui-vi|']

        table.setColumnCount(len(self.columns))
        table.setRowCount(len(self.df))
        table.setHorizontalHeaderLabels(self.columns)
        self.data = self.df.values.tolist()[1:]
        for row, data_row in enumerate(self.data):
            for col, value in enumerate(data_row):
                if col < len(self.columns):  # Проверка на выход за пределы списка columns
                    item = QTableWidgetItem(str(value))
                    table.setItem(row, col, item)

        dialog.exec()

    def referenceButtonClick(self):
        if self.df is None:
            self.show_error("Ошибка: Сначала необходимо выполнить вычисления.")
            return

        try:
            report_generator = ReportGenerator(self.df, self.ui.xlimits_input)
            report = report_generator.generate_report()

            window = NewWindow('Справка', report)
            window.show()
            window.exec()
        except Exception as e:
            self.show_error(f"Ошибка во время анализа: {e}")

    def tryLoadResult(self, to_be_control_local_error):
        try:
            current_file_path = os.path.abspath(__file__)
            current_dir = os.path.dirname(current_file_path)
            current_dir = os.path.join(current_dir, "..") 
            current_dir = os.path.join(current_dir, "output")
            file_path = os.path.join(current_dir, "output_test.csv")
            if self.to_be_control_local_error:
                self.df = pd.read_csv(file_path, delimiter=";", header=None,
                                 names=['x', 'v', 'v2i', 'v-v2i', 'e', 'h', 'c1', 'c2', 'u', '|ui-vi|'])
            else:
                self.df = pd.read_csv(file_path, delimiter=";", header=None, names=['x', 'v', 'u'])
        except Exception as e:
            self.show_error(f"Ошибка во время загрузки: {e}")

    def getColumnValues(self, df, column):
        return pd.to_numeric(df[column][1:], errors='coerce').dropna().tolist()

    def saveSettings(self):
        if self.df is not None:
            filename, _ = QFileDialog.getSaveFileName(None, "Сохранить настройки", self.settings_file, "JSON files (*.json)")
            if filename:
                self.settings_manager.save_settings(self.df, filename[:-5])  # Сохранение DataFrame и настроек

    def loadSettings(self):
        self.settings_manager.load_settings()
        self.to_be_control_local_error = self.ui.numerical_integration_parameters_input.isControlLocalError()

    def load_dataframe(self, csv_filename, control_local_error):
        """Загружает DataFrame из CSV файла в зависимости от control_local_error."""
        current_file_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file_path)
        current_dir = os.path.join(current_dir, "..") 
        current_dir = os.path.join(current_dir, "output")
        file_path = os.path.join(current_dir, csv_filename)
        try:
            if control_local_error:
                self.df = pd.read_csv(file_path, delimiter=";", header=None, low_memory=False,
                                       names=['x', 'v', 'v2i', 'v-v2i', 'e', 'h', 'c1', 'c2', 'u', '|ui-vi|'])
            else:
                self.df = pd.read_csv(file_path, delimiter=";", low_memory=False, header=None, names=['x', 'v', 'u'])
        except Exception as e:
            self.show_error(f"Ошибка при загрузке DataFrame: {e}")

    def show_error(self, message):
        """Отображает сообщение об ошибке."""
        print(message, file=sys.stderr)
        ErrorDialog(message).exec()
        # Заменяем калькуляторы на использование модуля 'calculation'

