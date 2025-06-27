from manim import *
import numpy as np
from scipy.integrate import odeint
from scipy.interpolate import interp1d

class phase_spiral_pos(Scene):
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

        titlep1  = MathTex(r"\text{System with}").to_corner(UL)
        titlep2 = MathTex(r"\text{complex eigenvalues}").next_to(titlep1, DOWN).align_to(titlep1, LEFT)
        
        A = np.array([
            [0.1, -0.5],
            [0.5, 0.1],
            ])
        A_label = MathTex(
            rf"A = \begin{{bmatrix}} {f"{A[0,0]}"} & {f"{A[0,1]}"} \\ {f"{A[1,0]}"} & {f"{A[1,1]}"} \end{{bmatrix}}"
            ).to_corner(UL).shift(1.5*DOWN) # relative anchoring is sloppy since I added title later sorry <3
        
        def model(v, t):
            return np.dot(A, v)
        model_label = MathTex(
            r"\frac{d\vec{x}}{dt} = A\vec{x}"
            ).next_to(A_label, DOWN).align_to(A_label, LEFT)

        v1_0 = np.array([1, 1])
        v1_0_label = MathTex(
            rf"\vec{{x}}(0) = \begin{{bmatrix}} {f"{v1_0[0]}"} \\ {f"{v1_0[1]}"} \end{{bmatrix}}"
            ).next_to(model_label, DOWN).align_to(model_label, LEFT)

        t = np.linspace(0, 15, 1000) # smoothness of curve later on tied to framerate, not step size
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

        # start scene
        self.play(
            Write(titlep1),
            Write(titlep2),
            FadeIn(grid)
        )
        self.play(Write(grid.get_axis_labels(x_label="x_1", y_label="x_2")))
        self.wait()

        # add system
        labels = [A_label, model_label, v1_0_label]
        self.play(
            LaggedStart(*(Write(label) for label in labels), lag_ratio=0.5)
        )
        self.wait()

        tracker = ValueTracker(0)
        soldot1 = always_redraw(
            lambda: Dot(
                point = grid.c2p(*interp_sol1(tracker.get_value())),
                color = YELLOW
            )
        )
        soldot1.z_index=1 # to place dot above (in front of) trailing path

        dot1_label1 = MathTex(
                r"\vec{x}(0)"
            ).next_to(soldot1.get_center(), UP)
        
        dot1_label2 = always_redraw(
            lambda: MathTex(
                r"\vec{x}(t)"
                # rf"\vec{{x}}({f"{tracker.get_value():.1f}"})" # to show time values instead
            ).next_to(soldot1.get_center(), UP)
        )

        path1 = TracedPath(soldot1.get_center, stroke_color=GREEN)

        initial_objects = [soldot1, dot1_label1, path1]
        self.play(
            LaggedStart(*(Create(obj) for obj in initial_objects), lag_ratio=0.8)
            )
        self.wait()
        
        # add all arrows
        self.play(
            AnimationGroup(
                (
                    GrowFromCenter(arrow.set_opacity(0.75))
                    for arrow in arrows
                ),
                lag_ratio=0.001,
            )
        )
        self.wait(2)

        self.play(
            ReplacementTransform(dot1_label1, dot1_label2),
        )

        # animate x(t)
        tracker.set_value(0.0001) # to prevent value=0 weirdness
        self.play(
            tracker.animate.set_value(t[-1]),
            run_time=8,
            rate_func = linear
        )
        self.wait()
