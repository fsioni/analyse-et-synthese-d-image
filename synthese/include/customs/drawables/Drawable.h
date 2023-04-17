#include "../../gkit/color.h"
#include "../rendering/Line.h"
#include "../rendering/Hit.h"

#ifndef GKIT3_DRAWABLE_H
#define GKIT3_DRAWABLE_H

class Drawable {
public:
    Color color;

    virtual ~Drawable() = default;

    virtual Hit intersect(Line line) = 0;

    virtual Vector intersectNormal(Line line) const = 0;
};


#endif //GKIT3_DRAWABLE_H
