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
            [0.3, 0.1],
            [0.2, 0.4],
            ])
        A_label = MathTex(
            rf"A = \begin{{bmatrix}} {f"{A[0,0]}"} & {f"{A[0,1]}"} \\ {f"{A[1,0]}"} & {f"{A[1,1]}"} \end{{bmatrix}}"
            ).to_corner(UL)
        
        def model(v, t):
            return np.dot(A, v)
        model_label = MathTex(
            r"\frac{d\vec{x}}{dt} = A\vec{x}"
            ).next_to(A_label, DOWN).align_to(A_label, LEFT)

        v1_0 = np.array([0.25, 0.25])
        v1_0_label = MathTex(
            rf"\vec{{x}}(0) = \begin{{bmatrix}} {f"{v1_0[0]}"} \\ {f"{v1_0[1]}"} \end{{bmatrix}}"
            ).next_to(model_label, DOWN).align_to(model_label, LEFT)
        
        v1_0_dir = A @ v1_0
        dir1 = MathTex(
            r"\frac{d\vec{x}}{dt} \mid_{t = 0}",
            r"=",
            rf"\begin{{bmatrix}} {f"{v1_0_dir[0]:.2f}"} \\ {f"{v1_0_dir[1]:.2f}"} \end{{bmatrix}}"
        ).next_to(v1_0_label, DOWN).align_to(v1_0_label, LEFT)


        t = np.linspace(0, 10, 1000)
        solution1 = odeint(model, v1_0, t)
        interp_sol1 = interp1d(t, solution1, axis=0, kind='linear')

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

        labels = [A_label, model_label, v1_0_label, dir1]
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
        soldot1 = always_redraw(
            lambda: Dot(
                point = grid.c2p(*interp_sol1(tracker.get_value())),
                color = YELLOW
            )
        )
        soldot1.z_index=1
        dot_label = always_redraw(
            lambda: MathTex(
                r"\vec{x}"
            ).next_to(soldot1.get_center(), UP)
        )

        path1 = TracedPath(soldot1.get_center, stroke_color=GREEN)

        initial_objects = [soldot1, dot_label, path1]
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
