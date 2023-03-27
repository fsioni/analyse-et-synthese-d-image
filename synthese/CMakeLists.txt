cmake_minimum_required(VERSION 3.21)
project(synthese)

set(CMAKE_CXX_STANDARD 14)

include_directories(include)
include_directories(include/gkit)

add_executable(synthese
        projets/main.cpp
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
        src/gkit/vec.cpp include/customs/rendering/Renderer.h
        src/customs/rendering/Hit.cpp
        include/customs/rendering/Hit.h
        src/customs/rendering/Light.cpp
        include/customs/rendering/Light.h
        src/customs/rendering/Line.cpp
        include/customs/rendering/Line.h
        src/customs/rendering/Renderer.cpp
        include/customs/rendering/Renderer.h
        src/customs/scenes/Scene1.cpp
        include/customs/scenes/Scene1.h
        src/customs/Utils.cpp
        include/customs/Utils.h
        src/customs/drawables/Drawable.cpp
        include/customs/drawables/Drawable.h
        src/customs/drawables/Sphere.cpp
        include/customs/drawables/Sphere.h
        src/customs/drawables/Plan.cpp
        include/customs/drawables/Plan.h
        )

add_subdirectory(lib/Google_tests)
