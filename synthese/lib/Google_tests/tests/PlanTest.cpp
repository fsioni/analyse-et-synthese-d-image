#include <gtest/gtest.h>
#include "customs/drawables/Plan.h"
#include "customs/rendering/Line.h"
#include "customs/Utils.h"
#include "gkit/color.h"

class PlanTest : public ::testing::Test {
protected:
    Plan plane;

    void SetUp() override {
        // Initialize any test data here
        plane = Plan(Point(0, 0, -1), Vector(0, 0, 1), Black());
    }

    void TearDown() override {
        // Clean up any test data here
    }

};

TEST_F(PlanTest, TestPlanIntersection1) {
    Line cam = Line(Point(0, 0, 0), Vector(0, 0, -1));

    // Call the intersect method and check the results
    Hit t = plane.intersect(cam);
    ASSERT_DOUBLE_EQ(t.position, 1.0); // Check the position of the intersection
}

TEST_F(PlanTest, TestPlanIntersection2) {
    Line cam = Line(Point(0, 0, 0), Vector(0, 0, 1));

    // Call the intersect method and check the results
    Hit t = plane.intersect(cam);
    ASSERT_DOUBLE_EQ(t.position, Utils::INF); // Check the position of the intersection
}
