from abc import ABC, abstractmethod
# from calculation import rk_4, rk4_adaptive
import calculation as calc
import pandas as pd
class Calculator(ABC):
    @abstractmethod
    def calculate(self, *args, **kwargs):
        pass

class RK4Calculator(Calculator):
    def __init__(self):
        pass

    def calculate(self, x0, u_x0, h0, x_end, amount_of_steps, L, R, E0, omega):
        try:
            result = calc.rk_4(x0, u_x0, h0, x_end, amount_of_steps, L, R, E0, omega)
            #print()
            #print(result)
            #print()
            return pd.DataFrame(result)
            # Конвертируем результат в DataFrame
            #self.parent.df = pd.DataFrame(result)
        except Exception as e:
            raise Exception(f"Ошибка во время вычислений RK4: {e}")
        
class RK4AdaptiveCalculator(Calculator):
    def __init__(self):
        pass

    def calculate(self, x0, u_x0, h0, x_end, local_error, epsilon_border, amount_of_steps, L, R, E0, omega):
        # try:
            result = calc.rk4_adaptive( x0, u_x0, h0, x_end, local_error, epsilon_border, amount_of_steps, L, R, E0, omega)
            #print()
            #print(result)
            #print()
            # return pd.DataFrame(result, columns=['x', 'v', 'v2i', 'v-v2i', 'e', 'h', 'c1', 'c2', 'u', '|ui-vi|'])
            return pd.DataFrame(result)
            #x;v;v2i;v-v2i;E;h;c1;c2;u;|ui-vi|
            # Конвертируем результат в DataFrame
            # self.parent.df = pd.DataFrame(result)
        # except Exception as e:
        #     raise Exception(f"Ошибка во время вычислений RK4 Adaptive: {e}")
        