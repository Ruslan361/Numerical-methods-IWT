import numpy as np
import pandas as pd
# Класс для создания отчета
class ReportGenerator:
    def __init__(self, df, xlimits_input):
        self.df = df
        self.xlimits_input = xlimits_input

    def generate_report(self):
        report = ""
        amountOfIterations = len(self.df['x']) - 1
        report += f"Количество итераций: {amountOfIterations} \n"
        x = self.getColumnValues('x')
        l = len(x)
        difference_between_the_right_border_and_the_last_calculated_point = abs(
            x[l - 1] - self.xlimits_input.getEndX())
        report += f'разница между правой границей и последней вычисленной точки: {difference_between_the_right_border_and_the_last_calculated_point}\n'
        report += self.generate_error_report(report, x, symbol='e')
        report += self.generate_error_report(report, x, symbol='E')
        return report

    def generate_error_report(self, report, x, symbol):
        if symbol in self.df.columns:  # Проверка наличия столбца 'e'
            E = self.getColumnValues('e')
            maxError = max(E)
            max_error_index = E.index(maxError)
            report += f'Максимальное значение ОЛП {maxError} при x = {x[max_error_index]}\n'
            doubling = self.getColumnValues('c2')
            countOfDoubling = sum(doubling)
            report += f'Количество удвоений {countOfDoubling}\n'
            doubling = self.getColumnValues('c1')
            countOfDoubling = sum(doubling)
            report += f'Количество делений {countOfDoubling}\n'
            h = self.getColumnValues('h')
            maxStep = max(h)
            minStep = min(h)
            xMinStep = h.index(minStep)
            xMinStep = x[xMinStep]
            xMaxStep = h.index(maxStep)
            xMaxStep = x[xMaxStep]
            report += f'максимальный шаг {maxStep} при x={xMaxStep}\n'
            report += f'Минимальный шаг {minStep} при x={xMinStep}\n'
            u = np.array(self.getColumnValues('u'), dtype=np.float64)
            v = np.array(self.getColumnValues('v'), dtype=np.float64)
            difference = np.abs(u - v)
            maxDifference = np.max(difference)
            report += f'Максимальная разница численного и реального решения {maxDifference}'
            return report
        return ""

    def getColumnValues(self, column):
        return pd.to_numeric(self.df[column][1:], errors='coerce').dropna().tolist()