#include "../../gkit/vec.h"
#include "../rendering/Line.h"
#include "Drawable.h"

#ifndef GKIT3_PLAN_H
#define GKIT3_PLAN_H

class Plan : public Drawable {
public:
    Point point;
    Vector normal;
    Color color;

    Plan();

    Plan(Point point, Vector normal, Color color = Black());

    ~Plan() override;

    Hit intersect(Line line) override;

    Vector intersectNormal(Line line) const override;
};


#endif //GKIT3_PLAN_H
