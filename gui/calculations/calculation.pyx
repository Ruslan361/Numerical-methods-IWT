from libcpp.vector cimport vector
from calculation_lib cimport Data, DataRK4, RK_4_adaptive, RK_4

def rk4_adaptive(
    double x0, double y0, double h0, double xmax,
    double eps, double eps_out, int Nmax,
    double L, double R, double E0, double omega
):
    cdef vector[Data] result = RK_4_adaptive(
        x0, y0, h0, xmax, eps, eps_out, Nmax,
        L, R, E0, omega
    )
    return {
        'x': [data.x for data in result],
        'v': [data.v for data in result],
        'v2i': [data.v2i for data in result],
        'v_minus_v2i': [data.v_minus_v2i for data in result],
        'e': [data.e for data in result],
        'h': [data.h for data in result],
        'c1': [data.c1 for data in result],
        'c2': [data.c2 for data in result],
        'u': [data.u for data in result],
        'abs_ui_minus_vi': [data.abs_ui_minus_vi for data in result]
    }

def rk_4(
    double x0, double y0, double h, double xmax, 
    int Nmax, double L, double R, double E0, double omega
):
    cdef vector[DataRK4] result = RK_4(
        x0, y0, h, xmax, Nmax, L, R, E0, omega
    )
    return {
        'x': [data.x for data in result],
        'v': [data.v for data in result],
        'u': [data.u for data in result],
        'abs_ui_minus_vi': [data.abs_ui_minus_vi for data in result]
    }