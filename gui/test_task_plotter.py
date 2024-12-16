# Класс для отображения графика
class TestTaskPlotter:
    def __init__(self, graph_layout, show_numeric_solve_checkbox, show_real_solve_checkbox):
        self.graph_layout = graph_layout
        self.show_numeric_solve_checkbox = show_numeric_solve_checkbox
        self.show_real_solve_checkbox = show_real_solve_checkbox

    def plot(self, x, v, u):
        self.graph_layout.clear()

        if self.show_numeric_solve_checkbox.isChecked():
            self.graph_layout.plot(x, v, '--', label="Численное решение")

        if self.show_real_solve_checkbox.isChecked():
            #print(f"x {x} \ny {u}")
            self.graph_layout.plot(x, u, label="Аналитическое решение")

        # Заголовок выводится только один раз при инициализации
        if self.graph_layout.canvas.ax.get_title() == '':
            self.graph_layout.set_title("График зависимости силы тока от времени")

        self.graph_layout.set_xlabel("x")
        self.graph_layout.set_ylabel("V(x)")
        if (self.show_real_solve_checkbox.isChecked() or self.show_numeric_solve_checkbox.isChecked()):
            self.graph_layout.legend()
        self.graph_layout.draw()