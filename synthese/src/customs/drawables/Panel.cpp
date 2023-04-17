#include "customs/drawables/Panel.h"
#include "customs/Utils.h"

Panel::Panel() {
    this->position = Point(0, 0, 0);
    this->normal = Vector(0, 0, 0);
    this->width = 0;
    this->height = 0;
    this->color = Color(0, 0, 0);
}

Panel::Panel(Point position, Vector normal, float width, float height, Color color) {
    this->position = position;
    this->normal = normal;
    this->width = width;
    this->height = height;
    this->color = color;
}

Panel::~Panel() = default;

Hit Panel::intersect(Line line) {
    float t = dot(this->normal, Vector(line.position, this->position)) / dot(this->normal, line.direction);

    if (t < 0) return {Utils::INF};

    Point p = line.position + t * line.direction;

    float halfWidth = this->width / 2.0f;
    float halfHeight = this->height / 2.0f;

    if (p.x > this->position.x - halfWidth && p.x < this->position.x + halfWidth &&
        p.y > this->position.y - halfHeight && p.y < this->position.y + halfHeight) {
        return {t, this->normal, this->color};
    }

    return {Utils::INF};
}

Vector Panel::intersectNormal(Line line) const {
    return this->normal;
}
