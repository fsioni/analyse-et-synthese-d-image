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

    ~Panel();

    Hit intersect(Line line);

    Vector intersectNormal(Line line) const;
};


#endif //SYNTHESE_PANEL_H
