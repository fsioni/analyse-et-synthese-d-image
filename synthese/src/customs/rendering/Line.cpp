#include "customs/rendering/Line.h"

Line::Line() {
    this->position = Point(0, 0, 0);
    this->direction = Vector(1, 0, 0);
}

Line::Line(Point _pos, Vector _dir) {
    this->position = _pos;
    this->direction = _dir;
}

Line::~Line() = default;