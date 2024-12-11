<!-- \documentclass{article}
\usepackage{amsmath, amssymb}
\usepackage[utf8]{inputenc}

\begin{document} -->

## Решение линейного неоднородного дифференциального уравнения

Задано дифференциальное уравнение:
$L \frac{dI}{dx} + R I = E_0 \sin(\omega x), \quad I(0) = I_0.$

Перепишем в стандартной форме:

$\frac{dI}{dx} + \frac{R}{L} I = \frac{E_0}{L} \sin(\omega x).$


Это линейное дифференциальное уравнение первого порядка, решение которого состоит из суммы общего решения однородного уравнения и частного решения неоднородного уравнения:
$I(x) = I_{\text{одн}}(x) + I_{\text{неодн}}(x).$

### Общее решение однородного уравнения

Рассмотрим однородное уравнение:
$\frac{dI}{dx} + \frac{R}{L} I = 0.$

Разделим переменные:
$\frac{dI}{I} = -\frac{R}{L} dx.$

Интегрируем обе части:
$\ln|I| = -\frac{R}{L}x + C_1, \quad C_1 \text{ — константа интегрирования.}$

Возьмем экспоненту от обеих частей:
$I_{\text{одн}}(x) = C e^{-\frac{R}{L}x},$
где $C = e^{C_1}$ — произвольная константа.
#### Замечание от автора
С Может быть как положительным так и отрицательным, раскрываем $|I|$. Мнимая замена.
### Частное решение неоднородного уравнения

Для уравнения
$\frac{dI}{dx} + \frac{R}{L} I = \frac{E_0}{L} \sin(\omega x),$
предположим частное решение в виде:
$I_{\text{неодн}}(x) = A \sin(\omega x) + B \cos(\omega x),$
где $A$ и $B$ — неизвестные коэффициенты.

Подставим $I_{\text{неодн}}(x)$ в уравнение.

1. Производная $I_{\text{неодн}}(x)$:
$\frac{dI_{\text{неодн}}}{dx} = A \omega \cos(\omega x) - B \omega \sin(\omega x).$

2. Подставляем $I_{\text{неодн}}(x)$ и его производную:
$L \left(A \omega \cos(\omega x) - B \omega \sin(\omega x)\right) + R \left(A \sin(\omega x) + B \cos(\omega x)\right) = E_0 \sin(\omega x).$

3. Раскрываем скобки:
$(L A \omega + R B) \cos(\omega x) + (R A - L B \omega) \sin(\omega x) = E_0 \sin(\omega x).$

4. Сравниваем коэффициенты при $\cos(\omega x)$ и $\sin(\omega x)$:
$L A \omega + R B = 0, \quad R A - L B \omega = E_0.$

Решим систему уравнений:
- Из первого уравнения выразим $B$:
$B = -\frac{L \omega}{R} A.$

- Подставим $B$ во второе уравнение:
$R A - L \omega \left(-\frac{L \omega}{R} A\right) = E_0.$

Преобразуем:
$R A + \frac{L^2 \omega^2}{R} A = E_0.$

Приведем к общему знаменателю:
$A \left(R + \frac{L^2 \omega^2}{R}\right) = E_0.$

Выразим $A$:
$A = \frac{E_0}{R + \frac{L^2 \omega^2}{R}} = \frac{E_0 R}{R^2 + L^2 \omega^2}.$

Найдем $B$:
$B = -\frac{L \omega}{R} A = -\frac{L \omega}{R} \cdot \frac{E_0 R}{R^2 + L^2 \omega^2}.$

Упростим:
$B = -\frac{E_0 L \omega}{R^2 + L^2 \omega^2}.$

Частное решение:
$I_{\text{неодн}}(x) = \frac{E_0 R}{R^2 + L^2 \omega^2} \sin(\omega x) - \frac{E_0 L \omega}{R^2 + L^2 \omega^2} \cos(\omega x).$

### Общее решение

Общее решение:
$I(x) = I_{\text{одн}}(x) + I_{\text{неодн}}(x).$

Подставляем найденные выражения:
$I(x) = C e^{-\frac{R}{L}x} + \frac{E_0 R}{R^2 + L^2 \omega^2} \sin(\omega x) - \frac{E_0 L \omega}{R^2 + L^2 \omega^2} \cos(\omega x).$

### Нахождение константы $C$

Используем начальное условие $I(0) = I_0$:
$I(0) = C e^0 + \frac{E_0 R}{R^2 + L^2 \omega^2} \sin(0) - \frac{E_0 L \omega}{R^2 + L^2 \omega^2} \cos(0).$

$I_0 = C - \frac{E_0 L \omega}{R^2 + L^2 \omega^2}.$

Выразим $C$:
$C = I_0 + \frac{E_0 L \omega}{R^2 + L^2 \omega^2}.$

### Итоговое решение

$I(x) = \left(I_0 + \frac{E_0 L \omega}{R^2 + L^2 \omega^2}\right) e^{-\frac{R}{L}x} + \frac{E_0 R}{R^2 + L^2 \omega^2} \sin(\omega x) - \frac{E_0 L \omega}{R^2 + L^2 \omega^2} \cos(\omega x).$

#### Примечание от автора
Я пробежался по решению, вроде всё нормально. Если сойдётся решение численно и теоретически, то вообще будет замечательно. К сожалению сходится только при x0 = 0.

Math GPT $I(x) = \left( I_0 + \frac{E_0 L \omega}{R^2 + L^2 \omega^2} \right) e^{-\frac{R}{L} x} + \frac{E_0 R}{R^2 + L^2 \omega^2} \sin(\omega x) - \frac{E_0 L \omega}{R^2 + L^2 \omega^2} \cos(\omega x)$.

Для сборки calculation требуется 
pip install setuptools>=61 wheel Cython numpy

cd /path/to/calculation
python -m build
pip install dist/calculation-0.1.2-...-.whl