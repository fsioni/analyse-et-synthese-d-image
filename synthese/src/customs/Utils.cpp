#include "customs/Utils.h"

Point Utils::intersectPoint(Line &line, float t) {
    float x = line.position.x + line.direction.x * t;
    float y = line.position.y + line.direction.y * t;
    float z = line.position.z + line.direction.z * t;
    return Point(x, y, z);
}