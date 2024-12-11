#ifndef CALCULATION_LIB_H
#define CALCULATION_LIB_H

#include <vector>
#include <queue>
#include <cmath>
#include <fstream>

// Your existing C++ code declarations...

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

std::vector<Data> RK_4_adaptive(double x0, double y0, double h0, double xmax, double eps, double eps_out, int Nmax, double L, double R, double E0, double omega);

struct DataRK4 {
    double x;
    double v;
    double abs_ui_minus_vi;
    double u;
};

std::vector<DataRK4> RK_4(double x0, double y0, double h, double xmax, int Nmax, double L, double R, double E0, double omega);

#endif // CALCULATION_LIB_H