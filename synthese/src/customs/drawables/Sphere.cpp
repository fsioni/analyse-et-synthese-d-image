#include "customs/drawables/Sphere.h"
#include "customs/Utils.h"

#include <cmath>
#include <iostream>

Sphere::Sphere() {
    position = Point(0, 0, 0);
    radius = 1;
    color = Color(0, 0, 0);
}

Sphere::Sphere(Point position, float radius, Color color) {
    this->position = position;
    this->radius = radius;
    this->color = color;
}

Sphere::~Sphere() = default;

Hit Sphere::intersect(const Line &cam, float &t1, float &t2) const {
    float a = dot(cam.direction, cam.direction);
    float b = 2 * dot(cam.direction, Vector(this->position, cam.position));
    float k = dot(Vector(this->position, cam.position), Vector(this->position, cam.position)) -
              this->radius * this->radius;
    float det = b * b - 4 * a * k;

    if (det < 0) {
        return {Utils::INF, this->intersectNormal(cam), this->color};
    } else {
        t1 = (-b - sqrt(det)) / (2 * a);
        t2 = (-b + sqrt(det)) / (2 * a);

        if (t1 > 0 && t2 > 0) { // si les deux solutions sont positives
            return {std::min(t1, t2), this->intersectNormal(cam), this->color};
        } else if (t1 > 0) { // si on est dans la sphere
            return {t1, this->intersectNormal(cam), this->color};
        } else if (t2 > 0) { // si on est dans la sphere{
            return {t2, this->intersectNormal(cam), this->color};
        }

        return {Utils::INF, this->intersectNormal(cam), this->color};
    }
}

Hit Sphere::intersect(Line cam) {
    float t1 = 0, t2 = 0;
    return this->intersect(cam, t1, t2);
}

int Sphere::getNbIntersections(const Line &cam) {
    float t1 = 0, t2 = 0;
    this->intersect(cam, t1, t2);

    if (t1 > 0 && t2 > 0)
        return 2;
    else if (t1 > 0 || t2 > 0)
        return 1;
    else
        return 0;
}

Vector Sphere::intersectNormal(Line line) const {
    return Vector(this->position, line.position);
}