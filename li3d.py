from manim import *

class li3d(ThreeDScene):
    def construct(self):
        # Grid
        grid = ThreeDAxes(
            x_range=(-5,5,1),
            y_range=(-5,5,1),
            z_range=(-5,5,1),
        )
        grid.get_axis_labels(x_label="x_1", y_label="x_2", z_label="x_3")
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        # Mobjects
        a1 = Vector(grid.c2p(2, 2, 0), color=GREEN)
        a2 = Vector(grid.c2p(1, 0, -1), color=YELLOW)
        a3 = Vector(grid.c2p(1, 1, 1), color=BLUE)
        x1 = ValueTracker(1)
        x1a3 = always_redraw(
            lambda: Vector(grid.c2p(x1.get_value(), x1.get_value(), x1.get_value()), color=BLUE)
        )

        spana1a2 = Polygon(
            grid.c2p(6,4,-2), grid.c2p(2, 4, 2), grid.c2p(-6, -4, 2), grid.c2p(-2, -4, -2),
            color=ORANGE, 
            fill_color=ORANGE,
            fill_opacity=0.25,
            stroke_width=0
        )

        spanall = Cube(
            side_length=10,
            fill_color=ORANGE,
            fill_opacity=0.35
        ).shift(grid.c2p(0, 0, 0))

        # Labels
        a1_def = MathTex(r"\vec{a}_1=\begin{bmatrix} 2 \\ 2 \\ 0 \end{bmatrix}").to_edge(UL).scale(0.5)
        a2_def = MathTex(r"\vec{a}_2=\begin{bmatrix} 1 \\ 0 \\ -1 \end{bmatrix}").next_to(a1_def, RIGHT).scale(0.5)
        a3_def = MathTex(r"\vec{a}_3=\begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}").next_to(a2_def, RIGHT).scale(0.5)
        a1_label = MathTex(r"\vec{a}_1").next_to(a1.get_center(), UL).rotate(PI/2,axis=RIGHT)
        a2_label = MathTex(r"\vec{a}_2").next_to(a2.get_center(), DL).rotate(PI/2,axis=RIGHT)
        a3_label = MathTex(r"\vec{a}_3").next_to(a3.get_center(), DL).rotate(PI/2,axis=RIGHT)
        x1a3_label = always_redraw(
            lambda: MathTex(f"{x1.get_value():.2f}" r"\vec{a}_3").next_to(x1a3.get_center(), UL).rotate(PI/2,axis=RIGHT)
        )
        span_def = MathTex(r"\text{Span}(\{\vec{a}_1, \vec{a}_2}\})", color=ORANGE).to_edge(DL).scale(0.75)
        title = MathTex(r"\text{Span}(\{\vec{a}_1, \vec{a}_2, \vec{a}_3\}) = \mathbb{R}^3").to_edge(UR).scale(0.75)
        title2 = MathTex(r"\text{Sliding along} \, x_1 \vec{a}_3 \, \text{...}").to_edge(UR).scale(0.75)

        # VGroups

        # Animation Start
        self.add(grid)
        self.wait()

        self.add_fixed_in_frame_mobjects(a1_def, a2_def, a3_def)
        self.play(FadeIn(a1, a2, a1_label, a2_label))
        self.wait()

        self.play(
            FadeIn(spana1a2),
            FadeOut(a1, a2, a1_label, a2_label)
        )
        self.add_fixed_in_frame_mobjects(span_def)
        self.wait()
  
        self.play(
            FadeIn(a3, a3_label)   
        )
        self.wait()

        # spana1a2 moves along x1a3
        self.play(
            FadeOut(a3, a3_label),
            FadeIn(x1a3, x1a3_label),
        )  
        self.wait()

        self.play(spana1a2.animate.move_to(x1a3.get_end()))
        self.move_camera(phi=85 * DEGREES, theta=-45 * DEGREES)

        self.begin_ambient_camera_rotation(34*DEGREES, about='theta')

        self.add_fixed_in_frame_mobjects(title2)
        spana1a2.add_updater(
            lambda s: s.move_to(x1a3.get_end())
        )
        self.play(
            x1.animate.set_value(3),
            run_time=2,
            rate_func=linear
        )
        self.play(
            x1.animate.set_value(-3),
            run_time=6, 
            rate_func=linear
        )
        self.wait(2)

        self.play(
            FadeOut(spana1a2, x1a3, x1a3_label),
            #FadeIn(spanall),
        )
        self.stop_ambient_camera_rotation(about='theta')
        self.remove(span_def, title2)
        self.add_fixed_in_frame_mobjects(title)
        self.wait(3)