#include <fstream>
#include <cmath>
#include <filesystem>
#include <string>
#include <limits>
#include <filesystem>
#include <queue>
#include <vector>
#include <iostream>
//#include "calculation_lib.h"

#include <cfloat> // Для DBL_MAX

#define SEPARATE ";"
// #ifdef _WIN32
// #include <Windows.h>
// #else
// #include <unistd.h>
// #include <dlfcn.h>
// //#include <limits.h> // Для PATH_MAX (Linux/macOS)
// #endif

// #ifdef _WIN64  // Проверка на 64-битную версию Windows
// #define  __declspec(dllexport)
// #elif defined(_WIN32)  // Проверка на 32-битную версию Windows
// #define  __declspec(dllexport)
// #else
// #define  __attribute__((visibility("default")))
// #endif


// Константы, используемые в программе
// X0 - начальное значение x
// Y0 - начальное значение y
// H0 - начальный шаг
// XMAX - конечное значение x
// EPS - точность вычислений
// EPS_OUT - точность выхода
// NMAX - максимальное число шагов

const double X0 = 0.0;
const double Y0 = 1.0;
const double H0 = 0.1;
const double XMAX = 10.6657953;
const double EPS = 1e-6;
const double EPS_OUT = 1e-6;
const int NMAX = 1000;

struct Data {
    double x;
    double v;
    double v2i;
    double v_minus_v2i;
    double e;
    double h;
    int c1;
    int c2;
    double u;
    double abs_ui_minus_vi;
};

// // Получаем абсолютный путь к DLL/so/dylib, в которой находится эта функция
//  std::filesystem::path getThisLibraryPath() {
// #ifdef _WIN32
//     HMODULE hModule;
//     BOOL success = GetModuleHandleExA(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
//         GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
//         (LPCSTR)&getThisLibraryPath,
//         &hModule);
//     if (success) {
//         char buffer[MAX_PATH];
//         GetModuleFileNameA(hModule, buffer, MAX_PATH);
//         return std::filesystem::path(buffer);
//     }
// #else
//     Dl_info info;
//     if (dladdr((void*)&getThisLibraryPath, &info) != 0) {
//         return std::filesystem::path(info.dli_fname);
//     }
// #endif
//     return ""; // Возвращаем пустой путь в случае ошибки
// }



// // Формируем абсолютный путь к output
//  std::string getOutputPath() {
//     std::filesystem::path executablePath = getThisLibraryPath();
//     std::filesystem::path outputPath = executablePath.parent_path() / ".." / ".." / "output" / "output_test.csv";
//     //return outputPath.string();
//     return "output_test.csv";
// }

//#define OUT_PATH getOutputPath().c_str()

// Правая часть дифференциального уравнения dy/dx = f(x, y)
// Args:
//     x - значение независимой переменной (double)
//     y - значение зависимой переменной (double)
// Returns:
//     Значение функции f(x, y) (double)

    double rhs(double x, double I, double L, double R, double E0, double omega) {
        return (E0 * sin(omega * x) - R * I) / L;
    }


// Аналитическое решение u(x, C) = C * exp(x)
// Args:
//     x - значение независимой переменной (double)
//     C - константа интегрирования (double)
// Returns:
//     Значение аналитического решения u(x, C) (double)

    double calculateRealSolution(double x, double L, double R, double E0, double omega, double I0, double x0)
    {
        // Коэффициенты для решения
        double A = E0 * R / (R * R + L * L * omega * omega);
        double B = -E0 * L * omega / (R * R + L * L * omega * omega);
        double C = I0 + E0 * L * omega / (R * R + L * L * omega * omega);

        // Вычисление значения тока
        double exponentialPart = C * std::exp(-R * (x - x0) / L);
        double sinusoidalPart = A * std::sin(omega * x);
        double cosinusoidalPart = B * std::cos(omega * x);

        // Итоговое значение
        return exponentialPart + sinusoidalPart + cosinusoidalPart;
    }
    // double calculateRealSolution(double x, double L, double R, double E0, double omega, double I0, double x0) {
    //     double numerator = R * exp(R * x0 / L) * I0 - sin(omega*x);
    //     double denominator = R * exp(R * x / L);
    //     double term1 = numerator / denominator;

    //     double term2 = E0 * sin(x * omega) / R;


    //     return  term1 + term2; 
    // }


// шаг Метод Рунге-Кутта четвертого порядка
// Args:
//     x - значение независимой переменной (double)
//     y - значение зависимой переменной (double)
//     h - размер шага (double)
// Returns:
//     Значение y на следующем шаге (double)

double RK_4_Step(const double &x, const double &y,const double &h, double L, double R, double E0, double omega)
{
    double k1 = h * rhs(x, y, L, R, E0, omega);
    double k2 = h * rhs(x + h / 2., y + k1 / 2., L, R, E0, omega);
    double k3 = h * rhs(x + h / 2., y + k2 / 2., L, R, E0, omega);
    double k4 = h * rhs(x + h, y + k3, L, R, E0, omega);

    double y_next = y + (k1 + 2. * k2 + 2. * k3 + k4) / 6.;

    if (std::isinf(y_next) || std::isnan(y_next) || std::fabs(y_next) > DBL_MAX) { 
        throw std::overflow_error("Value is NaN. | Value is infinite. | Value exceeds the maximum representable double.");
    }

    return y_next;
}
template <typename T>
std::vector<T> convertQueueToVector(std::queue<T>& dataQueue) {
    std::vector<T> dataVector;
    while (!dataQueue.empty()) {
        dataVector.push_back(dataQueue.front());
        dataQueue.pop();
    }
    return dataVector;
}

// Метод Рунге-Кутта 4-го порядка без контроля локальной погрешности
// Args:
//     x0 - начальное значение x (double)
//     y0 - начальное значение y (double)
//     h - размер шага (double)
//     xmax - конечное значение x (double)
//     Nmax - максимальное число шагов (int)
// Returns:
//     0 - если вычисления прошли успешно.
struct DataRK4 {
    double x;
    double v;
    double abs_ui_minus_vi;
    double u;
};
std::vector<DataRK4> RK_4(double x0, double y0, double h, double xmax, int Nmax, double L, double R, double E0, double omega)
{
    int step = 0;
    double x = x0;
    double y = y0;
    std::queue<DataRK4> dataQueue; // Добавить очередь DataRK4
    std::ofstream output("output_test.csv");
    double realSolution = calculateRealSolution(x, L, R, E0, omega, y0, x0);
    dataQueue.push({x, y, std::fabs(realSolution - y), realSolution});
    output << "x;v;u;|ui-vi|" << std::endl;     // Заголовок CSV с разделителем ;
    while (x+h <= xmax && step < Nmax) {
        y = RK_4_Step(x, y, h, L, R, E0, omega);
        x = x + h;
        realSolution = calculateRealSolution(x, L, R, E0, omega, y0, x0);
        output << x << SEPARATE << y << SEPARATE << realSolution << SEPARATE << std::fabs(realSolution - y) << std::endl;
        dataQueue.push({x, y, std::fabs(realSolution - y), realSolution});
        ++step;
        
    }

    return convertQueueToVector<DataRK4>(dataQueue);
}

// Метод Рунге-Кутта 4-го порядка с контролем локальной погрешности
// Args:
//     x0 - начальное значение x (double)
//     y0 - начальное значение y (double)
//     h0 - начальный размер шага (double)
//     xmax - конечное значение x (double)
//     eps - параметр контроля локальной погрешности (double)
//     eps_out -  эпсилон граничное (double)
//     Nmax - максимальное число шагов (int)
// Returns:
//     0 - если вычисления прошли успешно




// Функция для добавления данных в очередь
void addData(std::queue<Data>& q, double x, double y, double y2, double error, int p, double h, int c1, int c2, double y0, double L, double R, double E0, double omega, double x0) {
    Data data;
    data.x = x;
    data.v = y;
    data.v2i = y2;
    data.v_minus_v2i = y - y2;
    data.e = error * pow(2, p);
    data.h = h;
    data.c1 = c1;
    data.c2 = c2;
    data.u = calculateRealSolution(x, L, R, E0, omega, y0, x0);
    data.abs_ui_minus_vi = std::fabs(calculateRealSolution(x, L, R, E0, omega, y0, x0) - y);
    q.push(data);
}

std::vector<Data> RK_4_adaptive(double x0, double y0, double h0, double xmax, double eps, double eps_out, int Nmax, double L, double R, double E0, double omega)
{
    double x = x0;
    double y = y0;
    double h = h0;
    double y1;
    double y2;
    int c1 = 0;
    int c2 = 0;
    int step = 0;
    double error = 0.;
    int p = 4;

    std::queue<Data> dataQueue; // Добавить очередь Data

    std::ofstream output("output_test.csv");
 
    output << "x;v;v2i;v-v2i;E;h;c1;c2;u;|ui-vi|" << std::endl;
    // double startRealSolution = calculateRealSolution(x, L, R, E0, omega, y0, x0);
    // dataQueue.push({x, y, std::fabs(startRealSolution - y), startRealSolution});

    while (x + h <= xmax && std::abs(x - xmax) > eps_out && step < Nmax) {

        // Делаем шаг методом Рунге-Кутта с h и два шага с h/2
        y1 = RK_4_Step(x, y, h, L, R, E0, omega);
        y2 = RK_4_Step(x, y, h / 2, L, R, E0, omega);
        y2 = RK_4_Step(x + h / 2, y2, h / 2, L, R, E0, omega);

        // Вычисляем оценку локальной погрешности
        error = (std::abs(y1 - y2)) / (pow(2, p) - 1);     //2^p-1 - знаменатель в формуле вычисления О.Л.П

        // Проверяем, соответствует ли оценка погрешности заданной точности
        if (error > eps) {
            h=h/2;
            ++step;
            c1++;
        }
        else if( error < eps / pow(2, p + 1) ) {  //2^(p+1)
            y = y1;
            x += h;  //Увеличиваем шаг перед выводом, т.к. метод Р.К. считает значение в следующей точке
            c2++;

            //2^p
            output << x << SEPARATE << y << SEPARATE << y2 << SEPARATE << y-y2 << SEPARATE << error * pow(2, p) << SEPARATE << h << SEPARATE << c1 << SEPARATE << c2 << SEPARATE << calculateRealSolution(x, L, R, E0, omega, y0, x0) << SEPARATE << std::fabs(calculateRealSolution(x, L, R, E0, omega, y0, x0) - y) << std::endl;
            
            // Добавить данные в очередь
            addData(dataQueue, x, y, y2, error, p, h, c1, c2, y0, L, R, E0, omega, x0);

            h *= 2;
            ++step;
  
        }
        else {
            y = y1;
            x += h;  //Увеличиваем шаг перед выводом, т.к. метод Р.К. считает значение в следующей точке
            //2^p
            double realSolution = calculateRealSolution(x, L, R, E0, omega, y0, x0);
            output << x << SEPARATE << y << SEPARATE << y2 << SEPARATE << y-y2 << SEPARATE << error * pow(2, p) << SEPARATE << h << SEPARATE << c1 << SEPARATE << c2 << SEPARATE << realSolution << SEPARATE << std::fabs(realSolution - y) << std::endl;
            
            // Добавить данные в очередь
            addData(dataQueue, x, y, y2, error, p, h, c1, c2, y0, L, R, E0, omega, x0);

            ++step;
        }
    }

    if (x + h > xmax)
    {
        h = xmax - x;
        //++c1;
        // Делаем шаг методом Рунге-Кутта с h и два шага с h/2
        y1 = RK_4_Step(x, y, h, L, R, E0, omega);
        y2 = RK_4_Step(x, y, h / 2, L, R, E0, omega);
        y2 = RK_4_Step(x + h / 2, y2, h / 2, L, R, E0, omega);
        double realSolution = calculateRealSolution(x, L, R, E0, omega, y0, x0);
        output << x+h << SEPARATE << y1 << SEPARATE << y2 << SEPARATE << y1-y2 << SEPARATE << error * pow(2, p) << SEPARATE << h << SEPARATE << c1 << SEPARATE << c2 << SEPARATE << realSolution << SEPARATE << std::fabs(realSolution - y) << std::endl;
        // Добавить данные в очередь
        addData(dataQueue, x+h, y, y2, error, p, h, c1, c2, y0, L, R, E0, omega, x0);
    }


    output.close();

    return convertQueueToVector<Data>(dataQueue);
}





int main()
{
    setlocale(LC_ALL, "Russian");

    RK_4_adaptive(1, Y0, H0, XMAX, EPS, EPS_OUT, NMAX, 1, 1, 1, 1);
    // std::vector<Data> results = RK_4_adaptive(X0, Y0, H0, XMAX, EPS, EPS_OUT, NMAX, 1, 1, 1, 0);

    // for (const auto& result : results) {
    //     std::cout << "x: " << result.x << ", v: " << result.v << ", v2i: " << result.v2i 
    //               << ", v-v2i: " << result.v_minus_v2i << ", E: " << result.E 
    //               << ", h: " << result.h << ", c1: " << result.c1 << ", c2: " << result.c2 
    //               << ", u: " << result.u << ", |ui-vi|: " << result.abs_ui_minus_vi << std::endl;
    // }

    //RK_4(X0, Y0, H0, XMAX, NMAX, 1, 1, 1, 0);

    return 0;
}