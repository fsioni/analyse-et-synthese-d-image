#ifndef SYNTHESE_BOX_H
#define SYNTHESE_BOX_H

#include "Drawable.h"
#include "Panel.h"

class Box : public Drawable {
public:
    Point position;
    float width;
    float height;
    float depth;
    Color color;

    Box(Point position, float width, float height, float depth, Color color = Black());

    Hit intersect(Line line) override;

    Vector intersectNormal(Line line) const override;

private:
    Panel panels[6];
    void initPanels();
};

#endif //SYNTHESE_BOX_H
