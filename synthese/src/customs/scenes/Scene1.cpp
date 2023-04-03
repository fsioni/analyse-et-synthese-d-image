#include "customs/scenes/Scene1.h"

#include "customs/rendering/Renderer.h"
#include "customs/drawables/Sphere.h"
#include "iostream"
#include "customs/drawables/Plan.h"
#include "customs/drawables/Panel.h"

void Scene1::Render() {
    Renderer renderer(512, 256, (char *) "../images/output", 2);

   //renderer.addLight(Light(Point(0, 0, 0), White(), 1));
    //renderer.addLight(Light(Point(0, 3, -2), Yellow(), 3));
    renderer.addLight(LightPanel(new Panel(Point(-2.5, 0, 0), Vector(0, 0, -1), 5, 5), White(), 10, 1));
    renderer.addDrawable(new Sphere(Point(0, 0, -3), 2, Red()));
    //renderer.addDrawable(new Panel(Point(0, 0, -3), Vector(0, 0.5, 0.5), 4, 4, Red()));
    renderer.addDrawable(new Plan(Point(0, -1, 0), Vector(0, 1, 0), Blue()));


    renderer.render();
}
