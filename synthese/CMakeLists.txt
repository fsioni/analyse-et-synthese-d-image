cmake_minimum_required(VERSION 3.21)
project(synthese)

set(CMAKE_CXX_STANDARD 14)

include_directories(include)
include_directories(include/gkit)

add_executable(synthese
        include/gkit/color.h
        include/gkit/files.h
        include/gkit/image.h
        include/gkit/image_io.h
        include/gkit/mat.h
        include/gkit/materials.h
        include/gkit/mesh_io.h
        include/gkit/stb_image.h
        include/gkit/stb_image_write.h
        include/gkit/vec.h
        projets/main.cpp
        src/gkit/color.cpp
        src/gkit/files.cpp
        src/gkit/image_io.cpp
        src/gkit/mat.cpp
        src/gkit/mesh_io.cpp
        src/gkit/vec.cpp)
