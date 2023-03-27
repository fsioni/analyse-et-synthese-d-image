#include "../../gkit/vec.h"

#ifndef GKIT3_CAMERA_H
#define GKIT3_CAMERA_H

class Line {
public:
    Point position;
    Vector direction;

    Line();

    Line(Point _pos, Vector _dir);

    ~Line();
};


#endif //GKIT3_CAMERA_H
