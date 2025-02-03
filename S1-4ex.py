from manim import *

class sl3d(ThreeDScene):
    def construct(self):
        # Grid
        grid = ThreeDAxes(
            x_range=(-5,5,1),
            y_range=(-5,5,1),
            z_range=(-5,5,1),
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

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
            u_range=[-8, 8], 
            v_range=[-8, 8],
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
        span_label = always_redraw(
            lambda: MathTex(r"\text{Span}(\vec{a}_2)", color=YELLOW).next_to(x1a1.get_end(), UR).rotate(PI/2,axis=RIGHT)
        )
        title = MathTex(r"\text{Span}(\{\vec{a}_1, \vec{a}_2\}) = \left\{\vec{b} \in \mathbb{R}^3 \mid b_1 - \frac{1}{2}b_2 + b_3 = 0 \right\}").to_edge(DOWN)

        # VGroups

        a2_grp = VGroup(a2, a2_label)
        linegroup = VGroup(x1a1, x1a1_label, span_a2, span_label)

        # Animation Start
        self.add(grid)
        self.wait()

        self.add_fixed_in_frame_mobjects(a1_def, a2_def)
        self.play(FadeIn(a1, a2))
        self.play(
            Write(a1_label),
            Write(a2_label)
        )
        self.wait()

        self.play(
            a2_grp.animate.shift(a1.get_end()),
            a2_label.animate.shift(a1.get_end(), UP)
        )
        self.wait()

        # Sweeping Line      
        self.play(
            FadeOut(a1, a1_label, a2_grp),
            FadeIn(x1a1, span_a2)    
        )
        self.play(Write(x1a1_label),
                  Write(span_label)
        )        
        self.wait(2)

        self.play(x1.animate.set_value(3), run_time=2, rate_func=linear)
        self.wait()

        self.play(
            x1.animate.set_value(-3),
            FadeIn(sweep),
            run_time=6, 
            rate_func=linear
        )
        self.wait()

        self.play(FadeOut(linegroup))
        self.add_fixed_in_frame_mobjects(title)
        self.wait(3)