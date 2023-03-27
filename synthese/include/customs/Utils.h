#include "../gkit/vec.h"
#include "rendering/Line.h"

#include "limits"

#ifndef GKIT3_UTILS_H
#define GKIT3_UTILS_H


class Utils {
public:
    constexpr static float INF = std::numeric_limits<float>::infinity();

    static Point intersectPoint(Line &line, float t);
};


#endif //GKIT3_UTILS_H
