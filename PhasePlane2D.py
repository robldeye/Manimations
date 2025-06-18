from manim import *
import numpy as np
from scipy.integrate import odeint

class phase2d(Scene):
    def construct(self):
        # Grid
        locations = []
        lbound = -4
        ubound = 4
        grid = Axes(
            x_range=(lbound, ubound, 1),
            y_range=(lbound, ubound, 1)
        )
        grid.get_axis_labels(x_label="x_1", y_label="x_2")

        for x in np.arange(lbound, ubound+1):
            for y in np.arange(lbound, ubound+1):
                locations.append([x, y])

        A = np.array([
            [-0.2, -0.9],
            [0.1, -0.2],
            ])
        
        def model(v, t):
            dvdt = np.dot(A, v)
            return dvdt

        v0 = np.array([2, 2])
        t = np.linspace(0, 100, 1000)
        solution = odeint(model, v0, t)

        def dir(x, y):
            return np.dot(A, np.array([x, y]))
        
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

        scale = 0.35
        arrows = VGroup(
            Arrow(
                start = grid.c2p(*(np.array(loc)) - scale * unit(dir(*loc))),
                end = grid.c2p(*(np.array(loc) + scale * unit(dir(*loc)))),
            )
            for loc in locations
        )

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

        self.add(soldot, path)
        self.play(
            tracker.animate.set_value(len(solution) - 1),
            run_time=5, 
            rate_func = linear
        )
        self.wait()
