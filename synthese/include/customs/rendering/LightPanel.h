#ifndef SYNTHESE_LIGHTPANEL_H
#define SYNTHESE_LIGHTPANEL_H


#include <vector>
#include "customs/drawables/Panel.h"
#include "Light.h"

class LightPanel {
public:
    Panel *panel;
    std::vector<Light> lights;
    float intensity;

    LightPanel(Panel *panel, Color color, int nbLights, float intensity = 1);
};


#endif //SYNTHESE_LIGHTPANEL_H
