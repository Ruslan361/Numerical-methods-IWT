import json
import os
import sys
import pandas as pd
import numpy as np
from PySide6.QtWidgets import QFileDialog
from custom_loyauts import ErrorDialog
# Класс для управления настройками
class TestTaskSettingsManager:
    def __init__(self, settings_file, ui_elements):
        self.settings_file = settings_file
        self.ui_elements = ui_elements

    def save_settings(self, df, filename):
        # Сохранение DataFrame в CSV файл
        csv_filename = filename + ".csv"
        df.to_csv(csv_filename, sep=";", index=False, header=False)

        # Сохранение настроек в JSON файл
        settings = {
            "initialConditions": {
                "X0": self.ui_elements["initialConditions"].X0Input.floatNumberLineEdit.text(),
                "UX0": self.ui_elements["initialConditions"].UX0Input.floatNumberLineEdit.text()
            },
            "xlimits": {
                "endX": self.ui_elements["xlimitsInput"].endXInput.floatNumberLineEdit.text(),
                "epsilonBorder": self.ui_elements["xlimitsInput"].epsilonBorderInput.floatNumberLineEdit.text()
            },
            "numericalIntegrationParameters": {
                "h0": self.ui_elements["numericalIntegrationParametersInput"].h0Input.floatNumberLineEdit.text(),
                "controlLocalError": self.ui_elements["numericalIntegrationParametersInput"].controlLocalErrorCheckBox.isChecked(),
                "epsilon": self.ui_elements["numericalIntegrationParametersInput"].epsilonInput.floatNumberLineEdit.text(),
                "to_be_control_local_error": self.ui_elements["numericalIntegrationParametersInput"].isControlLocalError()
            },
            "showNumericSolve": self.ui_elements["showNumericSolveCheckBox"].isChecked(),
            "showRealSolve": self.ui_elements["showRealSolveCheckBox"].isChecked(),
            "amountOfSteps": self.ui_elements["amountOfStepsInput"].intNumberLineEdit.text(),
            "csv_filename": os.path.relpath(csv_filename, os.path.dirname(filename)),  # Относительный путь
            "task_number": 0
        }

        json_filename = filename + ".json"
        try:
            with open(json_filename, "w") as f:
                json.dump(settings, f, indent=4)
            print(f"Настройки сохранены в файлы {json_filename} и {csv_filename}")
        except Exception as e:
            print(f"Ошибка при сохранении настроек: {e}", file=sys.stderr)
            ErrorDialog(f"Ошибка при сохранении настроек: {e}").exec()

    def load_settings(self):
        filename, _ = QFileDialog.getOpenFileName(
            None, "Загрузить настройки", "", "JSON files (*.json)"
        )
        if filename:
            try:
                with open(filename, "r") as f:
                    settings = json.load(f)

                if "task_number" not in settings or settings["task_number"] != 0:
                    print("Ошибка: Загруженный файл настроек не соответствует тестовой задаче.")
                    ErrorDialog("Ошибка: Загруженный файл настроек не соответствует тестовой задаче.").exec()
                    return

                self.ui_elements["initialConditions"].X0Input.floatNumberLineEdit.setText(settings["initialConditions"]["X0"])
                self.ui_elements["initialConditions"].UX0Input.floatNumberLineEdit.setText(settings["initialConditions"]["UX0"])
                self.ui_elements["xlimitsInput"].endXInput.floatNumberLineEdit.setText(settings["xlimits"]["endX"])
                self.ui_elements["xlimitsInput"].epsilonBorderInput.floatNumberLineEdit.setText(settings["xlimits"]["epsilonBorder"])
                self.ui_elements["numericalIntegrationParametersInput"].h0Input.floatNumberLineEdit.setText(settings["numericalIntegrationParameters"]["h0"])
                self.ui_elements["numericalIntegrationParametersInput"].controlLocalErrorCheckBox.setChecked(settings["numericalIntegrationParameters"]["controlLocalError"])
                self.ui_elements["numericalIntegrationParametersInput"].epsilonInput.floatNumberLineEdit.setText(settings["numericalIntegrationParameters"]["epsilon"])
                self.ui_elements["showNumericSolveCheckBox"].setChecked(settings["showNumericSolve"])
                self.ui_elements["showRealSolveCheckBox"].setChecked(settings["showRealSolve"])
                self.ui_elements["amountOfStepsInput"].intNumberLineEdit.setText(settings["amountOfSteps"])
                self.ui_elements["numericalIntegrationParametersInput"].setChecked(settings["numericalIntegrationParameters"]["to_be_control_local_error"])

                csv_filename = os.path.join(os.path.dirname(filename), settings["csv_filename"])
                self.ui_elements["parent"].load_dataframe(csv_filename, self.ui_elements["numericalIntegrationParametersInput"].isControlLocalError())
                self.ui_elements["parent"].refreshPlot()  # Обновление графика после загрузки

                print(f"Настройки загружены из файла {filename}")
            except Exception as e:
                print(f"Ошибка при загрузке настроек: {e}", file=sys.stderr)
                ErrorDialog(f"Ошибка при загрузке настроек: {e}").exec()