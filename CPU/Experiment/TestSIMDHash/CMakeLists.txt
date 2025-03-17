cmake_minimum_required(VERSION 3.14)
project(TestSIMDHash)

set(CMAKE_CXX_STANDARD 17)

add_compile_options(-O1 -mavx2 -mfma -mbmi2 -march=native)

include_directories(../../Common)

add_executable(TestSIMDHash TestSIMDHash.cpp)