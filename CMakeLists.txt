cmake_minimum_required(VERSION 3.27.2-msvc1)

project(ADA CXX)

add_executable(${PROJECT_NAME} src/cpp/main.cpp)

add_subdirectory(src/cpp/corpus)
add_subdirectory(src/cpp/models)
add_subdirectory(src/cpp/tokenizers)
add_subdirectory(src/cpp/util)

target_link_libraries(${PROJECT_NAME} corpus
                                      models
                                      tokenizers
                                      util)