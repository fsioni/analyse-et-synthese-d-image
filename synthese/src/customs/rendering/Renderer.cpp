#include "customs/rendering/Renderer.h"
#include "gkit/image_io.h"
#include "customs/Utils.h"
#include <thread>

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

// Divise l'image en parties égales pour le traitement parallèle
std::vector<std::pair<int, int>> divideImage(int width, int numParts) {
    std::vector<std::pair<int, int>> parts(numParts);
    int partSize = width / numParts;
    int remainder = width % numParts;
    int start = 0;
    for (int i = 0; i < numParts; i++) {
        int end = start + partSize;
        if (i < remainder) end++;
        parts[i] = {start, end};
        start = end;
    }
    return parts;
}

// Fonction pour traiter une partie de l'image
void processPart(Renderer* renderer, int start, int end) {
    for (int i = start; i < end; i++) {
        for (int j = 0; j < renderer->image.height(); j++) {
            renderer->processPixel(i, j);
        }
    }
}

// Parallélise le rendu de l'image
void Renderer::parallelRender() {
    // Nombre de threads à utiliser
    int numThreads = (int) std::thread::hardware_concurrency();

    // Diviser l'image en parties égales
    auto parts = divideImage(image.width(), numThreads);

    // Vecteur pour stocker les threads
    std::vector<std::thread> threads(numThreads);

    // Lancer les threads pour traiter chaque partie de l'image
    for (int i = 0; i < numThreads; i++) {
        auto [start, end] = parts[i];
        threads[i] = std::thread(processPart, this, start, end);
    }

    // Attendre la fin de tous les threads
    for (auto& thread : threads) {
        thread.join();
    }
}

// Redimensionne l'image avec un script Python
void Renderer::resizeImage() const {
    std::string path = this->filename + "-before_resize.png";
    write_image(image, path.c_str());

    // execute resize_script/main.py
    std::string command = "cd ../resize_script && python3 main.py " + path + " " +
                          std::to_string(this->antialiasingAmount);
    system(command.c_str());
}

// Fonction principale de rendu de l'image
void Renderer::render() {
    std::cout << "Rendering the image...\n";
    parallelRender();
    resizeImage();
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

void Renderer::addLight(const LightPanel &lightPanel) {
    for (auto &light: lightPanel.lights) {
        addLight(light);
    }
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
