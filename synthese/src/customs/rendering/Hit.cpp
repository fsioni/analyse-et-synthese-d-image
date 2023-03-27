#include "customs/rendering/Hit.h"

#include "customs/Utils.h"

Hit::operator bool() const {
    return (this->position > 0 && this->position < Utils::INF);
}
