#include "customs/rendering/LightPanel.h"

LightPanel::LightPanel(Panel *panel, Color color, int nbLights, float intensity) {
    this->panel = panel;
    this->intensity = intensity;

    float cellWidth = panel->width / static_cast<float>(nbLights);
    float cellHeight = panel->height / static_cast<float>(nbLights);

    // Centrer le panneau par rapport à sa position
    float panelCenterX = panel->position.x + panel->width / 2.0f;
    float panelCenterY = panel->position.y + panel->height / 2.0f;

    for (int i = 0; i < nbLights; i++) {
        for (int j = 0; j < nbLights; j++) {
            float x = panelCenterX + cellWidth * (static_cast<float>(i) - static_cast<float>(nbLights) / 2.0f + 0.5f);
            float y = panelCenterY + cellHeight * (static_cast<float>(j) - static_cast<float>(nbLights) / 2.0f + 0.5f);
            float z = panel->position.z;
            Point position = Point(x, y, z);
            Light light = Light(position, color, intensity/static_cast<float>(nbLights));
            lights.push_back(light);
        }
    }
}

