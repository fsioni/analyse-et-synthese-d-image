#include <gtest/gtest.h>
#include "customs/drawables/Sphere.h"
#include "customs/rendering/Line.h"
#include "gkit/color.h"

class SphereTest : public ::testing::Test {
protected:
    Sphere sphere;

    void SetUp() override {
        // Initialize any test data here
        sphere = Sphere(Point(0, 0, 0), 1, Black());
    }

    void TearDown() override {
        // Clean up any test data here
    }

};

TEST_F(SphereTest, TestSphereIntersect1) {
    // TEST :
    // caméra
    Line cam = Line(Point(0, 0, 0), Vector(0, 0, -1));

    // sphere
    int t = sphere.getNbIntersections(cam);

    ASSERT_DOUBLE_EQ(t, 1);
}

TEST_F(SphereTest, TestSphereIntersect2) {
    // TEST : en direction de la sphère
    Line cam = Line(Point(0, 0, 2), Vector(0, 0, -1));

    int t = sphere.getNbIntersections(cam);

    ASSERT_DOUBLE_EQ(t, 2);
}

TEST_F(SphereTest, TestSphereIntersect3) {
    // TEST : dans la sphère
    Line cam = Line(Point(0, 0, -2), Vector(0, 0, -1));

    int t = sphere.getNbIntersections(cam);

    ASSERT_DOUBLE_EQ(t, 0);
}