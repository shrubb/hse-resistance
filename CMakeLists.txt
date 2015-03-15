cmake_minimum_required(VERSION 3.0)
set(CMAKE_VERBOSE_MAKEFILE on)

find_package(PythonLibs 3.4.0 REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})
python_add_module(resistancecalc resistancecalc.cpp)
target_link_libraries(resistancecalc ${PYTHON_LIBRARIES})