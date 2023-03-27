#include "customs/scenes/Scene1.h"

#include "customs/rendering/Renderer.h"
#include "customs/drawables/Sphere.h"
#include "iostream"
#include "customs/drawables/Plan.h"

void Scene1::Render() {
    Renderer renderer(512, 256, (char *) "../images/output", 2);

   renderer.addLight(Light(Point(0, 0, 0), White(), 1));
   renderer.addLight(Light(Point(0, 3, -2), Yellow(), 3));
    renderer.addDrawable(new Sphere(Point(0, 0, -3), 2, White()));
    renderer.addDrawable(new Plan(Point(0, -1, 0), Vector(0, 1, 0), White()));

    renderer.render();
}
