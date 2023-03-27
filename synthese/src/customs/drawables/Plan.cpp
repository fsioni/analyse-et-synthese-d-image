#include "customs/drawables/Plan.h"
#include "customs/Utils.h"

Plan::Plan() {
    this->point = Point(0, 0, 0);
    this->normal = Vector(0, 0, 0);
    this->color = Color(0, 0, 0);
}

Plan::Plan(Point point, Vector normal, Color color) {
    this->point = point;
    this->normal = normal;
    this->color = color;
}

Plan::~Plan() = default;

Hit Plan::intersect(Line line) {
    float t = dot(this->normal, Vector(line.position, this->point)) / dot(this->normal, line.direction);
    //Point p = line.position + t * line.direction; // point d'intersection

    if (t > 0)
        return {t, this->normal, this->color};
    else
        return {Utils::INF, this->normal, this->color};
}

Vector Plan::intersectNormal(Line line) const {
    return this->normal;
}
