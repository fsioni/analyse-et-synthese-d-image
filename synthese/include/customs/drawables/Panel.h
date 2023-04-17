#ifndef SYNTHESE_PANEL_H
#define SYNTHESE_PANEL_H

// a panel is a 3D object with a position, a normal and a width and a height

#include "Drawable.h"

class Panel : public Drawable {
public:
    Point position;
    Vector normal;
    float width;
    float height;
    Color color;
    Panel();

    Panel(Point position, Vector normal, float width, float height, Color color = Black());

    ~Panel() override;

    Hit intersect(Line line) override;

    Vector intersectNormal(Line line) const override;
};


#endif //SYNTHESE_PANEL_H
