
#include "color.h"
#include "vec.h"
#include "customs/drawables/Box.h"
#include "customs/Utils.h"


Box::Box(Point position, float width, float height, float depth, Color color) {
    this->position = position;
    this->width = width;
    this->height = height;
    this->depth = depth;
    this->color = color;
    initPanels();
}

void Box::initPanels() {
    // front
    panels[0] = Panel(position - Vector(0, 0, depth/2), Vector(0, 0, 1), width, height, color);
    // back
    panels[1] = Panel(position + Vector(0, 0, depth/2), Vector(0, 0, -1), width, height, color);
    // left
    panels[2] = Panel(position - Vector(width/2, 0, 0), Vector(-1, 0, 0), depth, height, color);
    // right
    panels[3] = Panel(position + Vector(width/2, 0, 0), Vector(1, 0, 0), depth, height, color);
    // top
    panels[4] = Panel(position + Vector(0, height/2, 0), Vector(0, 1, 0), width, depth, color);
    // bottom
    panels[5] = Panel(position - Vector(0, height/2, 0), Vector(0, -1, 0), width, depth, color);
}

Hit Box::intersect(Line line) {
    Hit hit = Hit(Utils::INF);
    for (auto & panel : panels) {
        Hit panelHit = panel.intersect(line);
        if (panelHit && panelHit.position < hit.position) {
            hit = panelHit;
        }
    }
    return hit;
}

Vector Box::intersectNormal(Line line) const {
    // calculate the normal of the closest panel
    float min = Utils::INF;
    Vector normal;
    for (Panel panel : panels) {
        Hit panelHit = panel.intersect(line);
        if (panelHit && panelHit.position < min) {
            min = panelHit.position;
            normal = panelHit.normal;
        }
    }

    return normal;
}

