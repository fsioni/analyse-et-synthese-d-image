#include "../../gkit/vec.h"
#include "../../gkit/color.h"

#ifndef GKIT3_LIGHT_H
#define GKIT3_LIGHT_H


class Light {
public:
    Point position;
    Color color;
    float intensity;

    Light(Point position, Color color, float intensity = 1);

    ~Light();
};


#endif //GKIT3_LIGHT_H
