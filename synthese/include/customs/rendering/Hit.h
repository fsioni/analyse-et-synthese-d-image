#include "../../gkit/vec.h"
#include "../../gkit/color.h"

#ifndef GKIT3_HIT_H
#define GKIT3_HIT_H


class Hit {
public:
    float position; //position sur le rayon ou inf
    Vector normal;
    Color color;

    Hit(float position, Vector normal = Vector(0,0,0), Color color = Blue()) : position(position),
                                                      normal(normal), color(color) {}

    explicit operator bool() const;
};


#endif //GKIT3_HIT_H
