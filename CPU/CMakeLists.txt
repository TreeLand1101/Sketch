cmake_minimum_required(VERSION 3.14)
project(CPU)

set(CMAKE_CXX_STANDARD 14)


include_directories(.)
include_directories(Common)
include_directories(Struct)
include_directories(Src)

add_executable(CPU main.cpp)