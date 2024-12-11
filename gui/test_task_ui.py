from custom_loyauts import LatexRendererLayout, GraphLayout, IntNumberInput, NumericalIntegrationParametersInput, ScalarStartConditions, XlimitsInput
from PySide6.QtWidgets import QPushButton, QCheckBox, QHBoxLayout
from custom_loyauts import FloatNumberInput
from PySide6.QtWidgets import QGridLayout
# Класс для создания UI элементов
class TestTaskUI:
    def __init__(self, main_layout):
        self.main_layout = main_layout
        self.initial_conditions = None
        self.xlimits_input = None
        self.numerical_integration_parameters_input = None
        self.show_numeric_solve_checkbox = None
        self.show_real_solve_checkbox = None
        self.amount_of_steps_input = None
        self.graph_layout = None

    def setup_ui(self):
        #self._add_task_description()
        self._add_initial_conditions()
        self._add_parameters()
        self._add_xlimits_input()
        self._add_numerical_integration_parameters_input()
        self._add_calculate_button()
        self._add_checkboxes()
        self._add_amount_of_steps_input()
        self._add_graph_layout()
        self._add_buttons()


    def _add_parameters(self):
        self.additition_parameters = QGridLayout()

        self.L_input = FloatNumberInput("L")
        self.additition_parameters.addLayout(self.L_input, 0, 0)

        self.R_input = FloatNumberInput("R")
        self.additition_parameters.addLayout(self.R_input, 0, 1)

        self.E0_input = FloatNumberInput("E0")
        self.additition_parameters.addLayout(self.E0_input, 1, 0)

        self.omega_input = FloatNumberInput("omega")
        self.additition_parameters.addLayout(self.omega_input, 1, 1)

        self.main_layout.addLayout(self.additition_parameters)

    def _add_task_description(self):
        test_task_layout = LatexRendererLayout()
        tex_task1 = "$\\frac{du}{dx} = -\\frac{7}{2}u$"
        test_task_layout.render(tex_task1)
        self.main_layout.addLayout(test_task_layout, 1)

    def _add_initial_conditions(self):
        self.initial_conditions = ScalarStartConditions()
        self.main_layout.addLayout(self.initial_conditions)

    def _add_xlimits_input(self):
        self.xlimits_input = XlimitsInput()
        self.main_layout.addLayout(self.xlimits_input)

    def _add_numerical_integration_parameters_input(self):
        self.numerical_integration_parameters_input = NumericalIntegrationParametersInput()
        self.main_layout.addLayout(self.numerical_integration_parameters_input)

    def _add_calculate_button(self):
        calculate_button = QPushButton()
        calculate_button.setText("Начать вычисления")
        self.main_layout.addWidget(calculate_button)
        calculate_button.clicked.connect(self.parent().calculateClick)  # Вызов метода calculateClick родительского класса

    def _add_checkboxes(self):
        self.show_numeric_solve_checkbox = QCheckBox("Показать численное решение")
        self.show_real_solve_checkbox = QCheckBox("Показать аналитическое решение")
        self.show_numeric_solve_checkbox.checkStateChanged.connect(self.parent().refreshPlot)
        self.show_real_solve_checkbox.checkStateChanged.connect(self.parent().refreshPlot)
        self.main_layout.addWidget(self.show_numeric_solve_checkbox)
        self.main_layout.addWidget(self.show_real_solve_checkbox)

    def _add_amount_of_steps_input(self):
        self.amount_of_steps_input = IntNumberInput("Количество шагов")
        self.main_layout.addLayout(self.amount_of_steps_input)

    def _add_graph_layout(self):
        self.graph_layout = GraphLayout()
        self.main_layout.addLayout(self.graph_layout, 3)

    def _add_buttons(self):
        self.about_layout = QHBoxLayout()
        reference_button = QPushButton()
        reference_button.setText("Справка")
        reference_button.clicked.connect(self.parent().referenceButtonClick)  # Вызов метода referenceButtonClick родительского класса
        self.about_layout.addWidget(reference_button)
        show_table_button = QPushButton()
        show_table_button.setText("Вывести таблицу")
        show_table_button.clicked.connect(self.parent().ShowTableButtonClick)  # Вызов метода ShowTableButtonClick родительского класса
        self.about_layout.addWidget(show_table_button)

        save_settings_button = QPushButton()
        save_settings_button.setText("Сохранить настройки")
        save_settings_button.clicked.connect(self.parent().saveSettings)  # Вызов метода saveSettings родительского класса
        self.about_layout.addWidget(save_settings_button)
        load_settings_button = QPushButton()
        load_settings_button.setText("Загрузить настройки")
        load_settings_button.clicked.connect(self.parent().loadSettings)  # Вызов метода loadSettings родительского класса
        self.about_layout.addWidget(load_settings_button)

        self.main_layout.addLayout(self.about_layout)

    def parent(self):
        return self.main_layout.parent()
