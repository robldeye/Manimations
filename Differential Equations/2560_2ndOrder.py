from manim import *
import numpy as np
from scipy.integrate import odeint
from scipy.interpolate import interp1d

class SecondOrder(Scene):
    def construct(self):
        # Grid
        grid = Axes(
            x_range=(0, 10, 1),
            y_range=(-5, 5, 1),
            x_length=8,
            y_length=8,
            tips=False,
            axis_config={"include_numbers": True}
        ).to_edge(RIGHT).scale(0.95)
        grid.get_axis_labels(x_label="t", y_label="y")
        
        # ODE stuff
        
        # constant coefficients
        a = 1 # a != 0
        b = 0
        c = 1 

        def sode(y, t):
            y, z = y
            dydt = [z, 1/a*(-b*z - c*y)] #[y', y'']
            return dydt

        t = np.linspace(0, 10, 100) #[t_min, t_max, t_step]
        y_0 = 2 #[y(0)]
        z_0 = 2 #[y'(0)]
        initcond = [y_0, z_0]
        sol = odeint(sode, initcond, t)[:,0]
        interp_sol = interp1d(t, sol, axis=0, kind='linear')

        # Scenes
        title = MathTex(r"\text{Solution to} \,\,", r"2^{\text{nd}} \,\, \text{order ODE}")
        self.play(Write(title))
        self.wait()
        self.play(
            title.animate.to_corner(UL)
        )
        self.wait()

        DE = MathTex(r"ay''+by'+cy=0").next_to(title, DOWN).align_to(title, LEFT)
        self.play(
            Indicate(title[1])
        )
        self.play(
            Transform(title[1].copy(), DE)
        )
        self.wait()

        Ex_l1 = MathTex(
            r"\text{Ex) For} \,\, y''+y=0 \\"
        ).next_to(DE, DOWN, buff=2).align_to(title, LEFT)

        Ex_l2 = MathTex(
            r"\text{with} \,\, y(0)=2, \, y'(0)=2"
        ).next_to(Ex_l1, DOWN).align_to(title, LEFT)

        Ex_l3 = MathTex(
            r"y(t) = 2\text{cos}(t) + 2\text{sin}(t)",
        ).next_to(Ex_l2, DOWN, buff=1).align_to(title, LEFT)

        self.play(
            Write(Ex_l1),
            Write(Ex_l2)
        )
        self.wait(2)
        self.play(
            Write(Ex_l3)
        )
        self.wait(2)
        
        self.play(
            FadeIn(grid)
        )
        self.play(Write(grid.get_axis_labels(x_label="t", y_label="y")))
        self.wait()

        tracker = ValueTracker(0)
        soldot = always_redraw(
            lambda: Dot(
                point = grid.c2p(tracker.get_value(), interp_sol(tracker.get_value())),
                color = YELLOW
            )
        )
        soldot.z_index=1
        dot_l = always_redraw(
            lambda: MathTex(
                r"y(t)"
            ).next_to(soldot.get_center(), DL)
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
            run_time=5,
            rate_func = linear
        )
        self.wait()
