#include "customs/rendering/Renderer.h"
#include "gkit/image_io.h"
#include "customs/Utils.h"

Renderer::Renderer(int width, int height, const std::string &filename, int antialiasingAmount) {
    Point DEFAULT_CAMERA_POSITION = Origin();
    Vector DEFAULT_CAMERA_DIRECTION = Vector(0, 0, -1);
    this->camera = Line(DEFAULT_CAMERA_POSITION, DEFAULT_CAMERA_DIRECTION);

    this->lights = std::vector<Light>();
    this->image = Image(width * antialiasingAmount, height * antialiasingAmount);
    this->filename = filename;

    this->xMult = (float) width / (float) height;

    if (antialiasingAmount < 1)
        this->antialiasingAmount = 1;
    else if (antialiasingAmount > 16)
        this->antialiasingAmount = 16;
    else if (antialiasingAmount % 2 != 0)
        this->antialiasingAmount = antialiasingAmount + 1;
    else
        this->antialiasingAmount = antialiasingAmount;
}

Renderer::~Renderer() {
    for (auto &drawable: drawables) {
        delete drawable;
    }
}

Line Renderer::calculateRay(int px, int py) const {
    float x = (float(px) / float(image.width()) * 2 - 1) * xMult;
    float y = (float(py) / float(image.height()) * 2 - 1);
    float z = -1;
    return {camera.position, Vector(x, y, z)};
}

void Renderer::addDrawable(Drawable *drawable) {
    drawables.push_back(drawable);
}

void Renderer::render() {
    for (int i = 0; i < image.width(); i++) {
        for (int j = 0; j < image.height(); j++) {
            processPixel(i, j);
        }
    }

    std::string path = this->filename + "-before_resize.png";
    write_image(image, path.c_str());

    // execute resize_script/main.py
    std::string command = "cd ../resize_script && python3 main.py " + path + " " +
                          std::to_string(this->antialiasingAmount);
    system(command.c_str());

    std::cout << "================ RENDER ================\n\n"
              << "rendered successfuly at " << this->filename << "\n\n";
}

void Renderer::processPixel(int i, int j) {
    Line ray = calculateRay((int) i, j);

    image((int) i, j) = background;
    Point intersectionPoint;
    Hit closestHit = calculateClosestHit(ray);

    intersectionPoint = Utils::intersectPoint(ray, closestHit.position);

    Color pixelColor = calculatePixelColor(closestHit, intersectionPoint);

    image(i, j) = pixelColor;
    image(i, j).a = 1;
}

void Renderer::addLight(const Light &light) {
    lights.push_back(light);
}

Color Renderer::calculatePixelColor(const Hit &hit, Point intersectionPoint) {
    Color pixelColor = Black();
    for (auto &light: this->lights) {
        if (isInShadow(intersectionPoint, light.position, hit.normal)) {
            continue;
        }

        Vector l = Vector(intersectionPoint, light.position);
        float cos_theta = abs(dot(normalize(hit.normal), normalize(l)));
        Color lightColor = light.intensity * light.color;

        pixelColor = pixelColor + lightColor * hit.color * cos_theta / length2(l);
    }

    pixelColor.a = 1;
    return pixelColor;
}

Hit Renderer::calculateClosestHit(const Line &ray) {
    Hit closestHit(Utils::INF, Vector(0, 0, 0), Black());

    for (auto &drawable: drawables) {
        Hit hit = drawable->intersect(ray);

        if (hit.position < closestHit.position) {
            closestHit = hit;
        }
    }

    return closestHit;
}

bool Renderer::isInShadow(const Point &origin, const Point &destination, Vector normale) {
    float epsilon = 0.001;
    Vector offset = epsilon * normale;
    Point o = origin + offset;
    Vector direction = Vector(o, destination);
    Line ray(o, direction);
    float distanceToLight = length(direction);

    for (auto &object: drawables) {
        Hit hit = object->intersect(ray);
        return (hit.position > 0 && hit.position < distanceToLight);
    }

    return false;
}

// direction miroir de v (par rapport à n)
Vector Renderer::reflect(const Vector &n, const Vector &v) {
    assert (dot(n, v) < 0);
    return v - 2 * dot(n, v) * n;
}