from manim import *
import numpy as np
from scipy.integrate import odeint
from scipy.interpolate import interp1d

class SpringMassSystem(Scene):
    def construct(self):
        # Grid
        grid_scale = 0.85
        grid = Axes(
            x_range=[0, 10, 1],
            y_range=[-5, 5, 1],
            x_length=8,
            y_length=8,
            tips=False,
            x_axis_config={"include_numbers": True}
        ).to_edge(RIGHT).scale(grid_scale)
        grid.get_axis_labels(x_label="t", y_label="y")

        # to flip the y-axis cosmetically since down is the positive direction
        for y in range(-5, 6):
            label = MathTex(str(-y)).scale(grid_scale)
            label.next_to(grid.c2p(0,y), LEFT, buff=0.2)
            grid.add(label)
        
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
        tracker = ValueTracker(0)

        y_0 = 2 #[y(0)]
        z_0 = 2 #[y'(0)]
        initcond = [y_0, z_0]
        sol = odeint(sode, initcond, t)[:,0]
        interp_sol = interp1d(t, sol, axis=0, kind='linear')
        

        # Spring and Mass
        spring_x = -1.5
        def get_spring():
            t = tracker.get_value()
            top = grid.c2p(spring_x, 5)
            bottom = grid.c2p(spring_x, interp_sol(t))

            def spring_curve(u):
                point = interpolate(top, bottom, u)
                direction = bottom - top
                ortho = np.array([-direction[1], direction[0], 0])
                ortho = normalize(ortho)
                freq = 10
                amp = 0.2
                wiggle = amp * np.sin(2 * PI * freq * u) * ortho
                return point + wiggle

            return ParametricFunction(
                spring_curve,
                t_range=[0, 1],
                color=BLUE,
                stroke_width=4
            )

        spring = always_redraw(get_spring)
        square = Square(side_length=0.3, color=YELLOW, fill_opacity=0.75)
        square.add_updater(lambda m: m.move_to(grid.c2p(spring_x, interp_sol(tracker.get_value()))))

        # Scenes
        title = MathTex(r"\text{Solution to} \,\,", r"2^{\text{nd}} \,\, \text{order ODE}:")
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
            ReplacementTransform(title[1].copy(), DE)
        )
        self.wait()

        Ex_l1 = MathTex(
            r"y''+y=0"
        ).next_to(title, DOWN).align_to(title, LEFT)
        Ex_l2 = MathTex(
            rf"y(0)={f"{-y_0}"}, \, y'(0)={f"{-z_0}"}"
        ).next_to(Ex_l1, DOWN).align_to(title, LEFT)
        Exp1 = VGroup(Ex_l1, Ex_l2)

        Ex_l3 = MathTex(
            r"y(t) = 2\text{cos}(t) + 2\text{sin}(t)",
        ).next_to(Ex_l2, DOWN, buff=3).align_to(title, LEFT)

        self.play(
            Transform(DE, Exp1),
        )
        self.wait(1)

        self.play(
            Write(Ex_l3)
        )
        self.wait(2)
        
        self.play(
            FadeIn(grid)
        )
        self.play(Write(grid.get_axis_labels(x_label="t", y_label="y")))

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
            ).next_to(soldot.get_center(), UR)
        )

        path = TracedPath(soldot.get_center, stroke_color=GREEN)

        initial_objects = [soldot, dot_l, path, spring, square]
        self.play(
            LaggedStart(*(Create(obj) for obj in initial_objects), lag_ratio=0.5)
            )
        self.wait(2)

        tracker.set_value(0.0001)
        self.play(
            tracker.animate.set_value(t[-1]),
            run_time=5,
            rate_func = linear
        )
        self.wait(3)
