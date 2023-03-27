#include "../rendering/Line.h"
#include "../../gkit/vec.h"
#include "../../gkit/color.h"
#include "Drawable.h"

#ifndef GKIT3_SPHERE_H
#define GKIT3_SPHERE_H


class Sphere : public Drawable {
public:
    Point position;
    float radius;
    Color color;

    Sphere();

    Sphere(Point position, float radius, Color color = Black());

    ~Sphere() override;

    Hit intersect(Line cam) override;

    int getNbIntersections(const Line &cam);

    Vector intersectNormal(Line line) const override;

private:
    Hit intersect(const Line &cam, float &t1, float &t2) const;
};


#endif //GKIT3_SPHERE_H
