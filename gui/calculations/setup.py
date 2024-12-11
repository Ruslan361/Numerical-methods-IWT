from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy
import sys

# Флаги компиляции (лучше вынести в отдельный файл, например, setup_build.py)
extra_compile_args = ['-std=c++11'] if not sys.platform.startswith('win') else ['/std:c++11']
extra_link_args = []

extensions = [
    Extension(
        name="calculation",
        version="0.1.0",
        sources=["calculation.pyx", "calculation_lib.cpp"],
        language="c++",
        include_dirs=[numpy.get_include(), "."],  # "." для локальных include файлов.
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    )
]

setup(
    name="calculation",
    version="0.1.0",
    #py_modules=["calculation"],
    ext_modules=cythonize(extensions, language_level=3),  # language_level соответствует версии Python
    zip_safe=False,
)