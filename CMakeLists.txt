cmake_minimum_required(VERSION 3.10)
project(practice6 C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

add_executable(mypipefifo mypipefifo.c)
add_executable(mywriter   mywriter.c)
add_executable(myreader   reader.c)

add_compile_options(-Wall -Wextra)
