from manim import *
import numpy as np
from scipy.integrate import odeint

class phase3d(ThreeDScene):
    def construct(self):
        # Grid
        locations = []
        lbound = -4
        ubound = 4
        grid = ThreeDAxes(
            x_range=(lbound, ubound, 1),
            y_range=(lbound, ubound, 1),
            z_range=(lbound, ubound, 1)
        )
        grid.get_axis_labels(x_label="x_1", y_label="x_2", z_label="x_3")

        for x in np.arange(lbound, ubound+1):
            for y in np.arange(lbound, ubound+1):
                for z in np.arange(lbound, ubound+1):
                    locations.append([x, y, z])

        A = np.array([
            [-0.2, -0.9, 0],
            [0.1, -0.2, -0.9],
            [0, -0.1, -0.2]
            ])
        
        def model(v, t):
            dvdt = np.dot(A, v)
            return dvdt

        v0 = np.array([2, 2, 2])
        t = np.linspace(0, 10, 100)
        solution = odeint(model, v0, t)

        def dir(x, y, z):
            return np.dot(A, np.array([x, y, z]))
        
        def unit(v):
            if np.linalg.norm(v) != 0:
                return v/np.linalg.norm(v)
            else:
                return v
            
        def potency(v):
            if np.linalg.norm(v) != 0:
                return np.linalg.norm(dir(*v))/np.linalg.norm(v)
            else:
                return v

        # dots = VGroup(
        #     Dot(
        #         point = grid.c2p(*np.array(loc))
        #     )
        #     for loc in locations
        # )

        scale = 0.35
        arrows = VGroup(
            Arrow(
                start = grid.c2p(*(np.array(loc)) - scale * unit(dir(*loc))),
                end = grid.c2p(*(np.array(loc) + scale * unit(dir(*loc)))),
            )
            for loc in locations
        )

        # arrows = VGroup(
        #     Arrow(
        #         start = grid.c2p(*(np.array(loc) - scale * unit(dir(*loc)))),
        #         end = grid.c2p(*(np.array(loc) + scale * unit(dir(*loc)))),
        #         buff = 0
        #     )
        #     for loc in locations
        # )

        self.set_camera_orientation(phi = 60 * DEGREES, theta = -45 * DEGREES)
        self.add(grid)

        self.play(
            AnimationGroup(
                (
                    GrowFromCenter(arrow.set_opacity(0.5))
                    for arrow in arrows
                ),
                lag_ratio=0.0005,
            )
        )
        self.wait()

        tracker = ValueTracker(0)
        soldot = always_redraw(
            lambda: Dot3D(
                point = grid.c2p(*solution[int(tracker.get_value())]),
                color = YELLOW
            )
        )
        path = TracedPath(soldot.get_center, stroke_color=GREEN)

        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()
        # self.play(phi.animate.set_value(50 * DEGREES), run_time=2)
        # self.play(theta.animate.set_value(50 * DEGREES), run_time=2)
        # self.play(gamma.animate.set_value(1), run_time=2)
        # self.play(distance_to_origin.animate.set_value(2), run_time=2)
        # self.play(focal_distance.animate.set_value(25), run_time=2)
        # self.wait(1)

        self.add(soldot, path)
        self.play(
            tracker.animate.set_value(len(solution) - 1),
            phi.animate.set_value(15 * DEGREES),
            theta.animate.set_value(45 * DEGREES),
            run_time=5, 
            rate_func = linear
        )

        # self.move_camera(phi = 15 * DEGREES, theta = -45 * DEGREES, run_time=3)
        # self.wait()
        # self.move_camera(phi = 75 * DEGREES, theta = 0 * DEGREES, run_time=2)
        self.wait()
