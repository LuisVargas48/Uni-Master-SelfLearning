cmake_minimum_required(VERSION 3.21)
project(Autom)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(Autom
        automata.cpp
        automata.h
        main.cpp)
