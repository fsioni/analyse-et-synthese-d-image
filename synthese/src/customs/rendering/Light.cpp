#include "customs/rendering/Light.h"

Light::Light(Point position, Color color, float intensity) {
    this->position = position;
    this->color = color;
    this->intensity = intensity;
}

Light::~Light() = default;