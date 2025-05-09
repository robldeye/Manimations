from manim import *

class sl3d(ThreeDScene):
    def construct(self):
        # Grid
        grid = ThreeDAxes(
            x_range=(-10,10,1),
            y_range=(-10,10,1),
            z_range=(-10,10,1),
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Mobjects
        a1 = Vector(grid.c2p(2, 2, 1), color=GREEN)
        a2 = Vector(grid.c2p(2, -1, 0), color=YELLOW)
        x1 = ValueTracker(1)
        x1a1 = always_redraw(
            lambda: Vector(grid.c2p(2*x1.get_value(), 2*x1.get_value(), 1*x1.get_value()), color=GREEN)
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
            lambda u, v: grid.c2p(u, v, 1/6*u + 1/3*v),
            u_range=[-10, 10], 
            v_range=[-10, 10],
            checkerboard_colors=[RED_D, RED_E], resolution=(15, 32)
        ).set_opacity(0.5)

        # Labels
        a1_def = MathTex(r"\vec{a}_1=\begin{bmatrix} 1 \\ -4 \\ -3 \end{bmatrix}", color=GREEN).to_edge(UL)
        a1_label = always_redraw(
            lambda: MathTex(r"\vec{a}_1", color=GREEN).next_to(a1.get_center(), UL).rotate(PI/2,axis=RIGHT)
        )
        x1a1_label = always_redraw(
            lambda: MathTex(f"{x1.get_value():.2f}" r"\vec{a}_1", color=GREEN).next_to(x1a1.get_center(), UL).rotate(PI/2,axis=RIGHT)
        )
        a2_def = MathTex(r"\vec{a}_2=\begin{bmatrix} 3 \\ 2 \\ -2 \end{bmatrix}", color=YELLOW).next_to(a1_def, DOWN)
        a2_label = MathTex(r"\vec{a}_2", color=YELLOW).next_to(a2.get_center(), DOWN).rotate(PI/2,axis=RIGHT)
        span_def = MathTex(r"\text{Span}(\{\vec{a}_2})=\{c\vec{a}_2 \mid c \in \mathbb{R}\}", color=YELLOW).next_to(a1_def, DOWN).scale(0.75)
        span_label = always_redraw(
            lambda: MathTex(r"\text{Span}(\vec{a}_2)", color=YELLOW).next_to(x1a1.get_end(), UR).rotate(PI/2,axis=RIGHT)
        )
        title = MathTex(r"\text{Span}(\{\vec{a}_1, \vec{a}_2\}) = \,", r"\text{a plane}").to_edge(DOWN)
        title[1].set_color(RED)

        # VGroups

        a2_grp = VGroup(a2, a2_label)
        linegroup = VGroup(x1a1, x1a1_label, span_a2, span_label)

        # Animation Start
        self.add(grid)
        self.wait()

        self.add_fixed_in_frame_mobjects(a1_def, a2_def)
        self.play(FadeIn(a1, a2, a1_label, a2_label))
        self.wait()

        self.play(
            a2_grp.animate.shift(a1.get_end()),
            a2_label.animate.shift(a1.get_end(), UP)
        )
        self.wait()

        # Sweeping Line      
        self.play(
            FadeOut(a1, a1_label, a2_grp, a1_def, a2_def),
            FadeIn(x1a1, span_a2)    
        )
        self.play(
            Write(x1a1_label),
            Write(span_label),
        )    
        self.wait(2)

        self.begin_ambient_camera_rotation(25*DEGREES, about='theta')

        self.play(
            x1.animate.set_value(2),
            run_time=2,
            rate_func=linear
        )
        self.play(
            x1.animate.set_value(-2),
            FadeIn(sweep),
            run_time=6, 
            rate_func=linear
        )
        self.play(
            x1.animate.set_value(1),
            run_time=4
        )
        self.wait(2)
        self.play(FadeOut(linegroup))
        self.stop_ambient_camera_rotation(about='theta')
        self.add_fixed_in_frame_mobjects(title)
        self.wait(3)