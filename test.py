from manim import *

class CameraTest(ThreeDScene):
    def construct(self):
        # Get the camera's value trackers
        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()

        # Add some 3D axes to visualize the scene
        axes = ThreeDAxes()
        self.add(axes)
        self.wait(1)

        # Animate the camera’s angles and position independently
        self.play(phi.animate.set_value(50 * DEGREES), run_time=2)
        self.play(theta.animate.set_value(50 * DEGREES), run_time=2)
        self.play(gamma.animate.set_value(1), run_time=2)
        self.play(distance_to_origin.animate.set_value(2), run_time=2)
        self.play(focal_distance.animate.set_value(25), run_time=2)
        self.wait(1)

