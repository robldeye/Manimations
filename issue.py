from manim import *

class span3d(ThreeDScene):
    def construct(self):
        # Grid
        grid = ThreeDAxes(
            x_range=(-5,5,1),
            y_range=(-5,5,1),
            z_range=(-5,5,1),
        )

        # Mobjects
        a1 = Vector([1, -4, -3], color=GREEN)
        a2 = Vector([3, 2, -2], color=YELLOW)
        x1 = ValueTracker(1)
        x1a1 = always_redraw(
            lambda: Vector([1*x1.get_value(), -4*x1.get_value(), -3*x1.get_value()], color=GREEN)
        )
        span_a2 = Line(
            start=-10*a2.get_unit_vector(),
            end=10*a2.get_unit_vector(),
            color=YELLOW,
            stroke_width=4,
        )
        span_a2.add_updater(
            lambda l: l.move_to(x1a1.get_end())
        )

        sweep = Surface(
            lambda u, v: np.array([
                u,
                v,
                -u + 1/2*v
            ]),
            u_range=[-2, 2], 
            v_range=[-2, 2],
            checkerboard_colors=[RED_D, RED_E], resolution=(15, 32)
        ).set_opacity(0.5)

        # VGroups

        a2_grp = VGroup(a2)
        linegroup = VGroup(x1a1, span_a2)

        # Animation Start
        self.set_camera_orientation(phi=75 * DEGREES, theta=-10 * DEGREES)
        self.add(grid)
        self.wait()

        self.play(FadeIn(a1, a2))
        self.wait()

        self.play(a2_grp.animate.shift(a1.get_end()),)
        self.wait()

        # Sweeping Line      
        self.play(
            FadeOut(a1, a2_grp),
            FadeIn(x1a1, span_a2)    
        )
        self.wait()

        self.play(
            x1.animate.set_value(-2),
            FadeIn(sweep),
            run_time=6, 
            rate_func=linear
        )
        self.wait()

        self.play(FadeOut(linegroup))
        self.wait(3)