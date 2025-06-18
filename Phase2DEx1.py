from manim import *
import numpy as np
from scipy.integrate import odeint
from scipy.interpolate import interp1d

class phase2d(Scene):
    def construct(self):
        # Grid
        locations = []
        lbound = -4
        ubound = 4
        grid = Axes(
            x_range=(lbound, ubound, 1),
            y_range=(lbound, ubound, 1),
            x_length=9,
            y_length=9,
            tips=True,
            axis_config={"include_numbers": False}
        ).to_edge(RIGHT).scale(0.95)
        grid.get_axis_labels(x_label="x_1", y_label="x_2")

        for x in np.arange(lbound, ubound+1):
            for y in np.arange(lbound, ubound+1):
                locations.append([x, y])

        A = np.array([
            [-0.1, -0.5],
            [0.5, -0.1],
            ])
        A_l = MathTex(
            rf"A = \begin{{bmatrix}} {f"{A[0,0]}"} & {f"{A[0,1]}"} \\ {f"{A[1,0]}"} & {f"{A[1,1]}"} \end{{bmatrix}}"
            ).to_corner(UL)
        
        def model(v, t):
            return np.dot(A, v)
        model_l = MathTex(
            r"\frac{d\vec{x}}{dt} = A\vec{x}"
            ).next_to(A_l, DOWN).align_to(A_l, LEFT)

        v0 = np.array([2, 2])
        v0_l = MathTex(
            rf"\vec{{x}}(0) = \begin{{bmatrix}} {f"{v0[0]}"} \\ {f"{v0[1]}"} \end{{bmatrix}}"
            ).next_to(model_l, DOWN).align_to(model_l, LEFT)

        t = np.linspace(0, 100, 1000)
        solution = odeint(model, v0, t)
        interp_sol = interp1d(t, solution, axis=0, kind='linear')

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

        scale = 0.5
        arrows = VGroup(
            Arrow(
                start = grid.c2p(*(np.array(loc)) - scale * unit(dir(*loc))),
                end = grid.c2p(*(np.array(loc) + scale * unit(dir(*loc)))),
            )
            for loc in locations
        )

        self.play(
            FadeIn(grid)
        )
        self.play(Write(grid.get_axis_labels(x_label="x_1", y_label="x_2")))
        self.wait()

        labels = [A_l, model_l, v0_l]
        self.play(
            LaggedStart(*(Write(label) for label in labels), lag_ratio=0.5)
        )
        self.wait()

        
        self.play(
            AnimationGroup(
                (
                    GrowFromCenter(arrow.set_opacity(0.75))
                    for arrow in arrows
                ),
                lag_ratio=0.001,
            )
        )
        self.wait()

        tracker = ValueTracker(0)
        soldot = always_redraw(
            lambda: Dot(
                point = grid.c2p(*interp_sol(tracker.get_value())),
                color = YELLOW
            )
        )
        soldot.z_index=1
        dot_l = always_redraw(
            lambda: MathTex(
                r"\vec{x}"
            ).next_to(soldot.get_center(), UP)
        )

        path = TracedPath(soldot.get_center, stroke_color=GREEN)

        initial_objects = [soldot, dot_l, path]
        self.play(
            LaggedStart(*(Create(obj) for obj in initial_objects), lag_ratio=0.5)
            )
        self.wait()

        tracker.set_value(0.0001)
        self.play(
            tracker.animate.set_value(t[-1]),
            run_time=10,
            rate_func = linear
        )
        self.wait()
