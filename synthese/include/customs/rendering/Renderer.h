#include "../drawables/Drawable.h"
#include "Line.h"
#include "../../gkit/image.h"
#include "Light.h"

#ifndef GKIT3_RENDERER_H
#define GKIT3_RENDERER_H


class Renderer {
public:
    std::vector<Drawable *> drawables;
    Line camera;
    std::vector<Light> lights;

    Image image;
    std::string filename;

    float xMult;

    int antialiasingAmount;

    Renderer(int width, int height, const std::string &filename, int antialiasingAmount = 1);

    ~Renderer();

    void addDrawable(Drawable *drawable);

    void addLight(const Light &light);

    void render();

private:
    const float INF = std::numeric_limits<float>::infinity();
    Color background = Black();

    Line calculateRay(int i, int j) const;

    Color calculatePixelColor(const Hit &hit, Point intersectionPoint);

    Hit calculateClosestHit(const Line &ray);

    void processPixel(int i, int j);

    bool isInShadow(const Point &origin, const Point &destination, Vector normal);

    static Vector reflect(const Vector &n, const Vector &v);
};


#endif //GKIT3_RENDERER_H
