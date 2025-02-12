from manim import *

class ld3d(ThreeDScene):
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
        a1 = Vector(grid.c2p(2, 2, 0))
        a2 = Vector(grid.c2p(1, 0, -1))
        a3 = Vector(grid.c2p(1, 2, 1))
        x1 = ValueTracker(1)
        x1a3 = always_redraw(
            lambda: Vector(grid.c2p(x1.get_value(), 2*x1.get_value(), x1.get_value()))
        )

        spana1a2 = Polygon(
            grid.c2p(12,8,-4), grid.c2p(4, 8, 4), grid.c2p(-12, -8, 4), grid.c2p(-4, -8, -4),
            color=ORANGE, 
            fill_color=ORANGE,
            fill_opacity=0.25,
            stroke_width=1
        )

        x1a3_dot = Dot3D(color=ORANGE).move_to(spana1a2.get_center())
        x1a3_dot.add_updater(
            lambda d: d.move_to(spana1a2.get_center())
        )

        spanall = Cube(
            side_length=10,
            fill_color=ORANGE,
            fill_opacity=0.35
        ).shift(grid.c2p(0, 0, 0))

        # Labels
        a1_def = MathTex(r"\vec{a}_1=\begin{bmatrix} 2 \\ 2 \\ 0 \end{bmatrix}").to_edge(UL).scale(0.65)
        a2_def = MathTex(r"\vec{a}_2=\begin{bmatrix} 1 \\ 0 \\ -1 \end{bmatrix}").next_to(a1_def, RIGHT).scale(0.65)
        a3_def = MathTex(r"\vec{a}_3=\begin{bmatrix} 1 \\ 2 \\ 1 \end{bmatrix}").next_to(a2_def, RIGHT).scale(0.65)
        a1_label = MathTex(r"\vec{a}_1").next_to(a1.get_center(), UL).rotate(PI/2,axis=RIGHT)
        a2_label = MathTex(r"\vec{a}_2").next_to(a2.get_center(), DL).rotate(PI/2,axis=RIGHT)
        a3_label = MathTex(r"\vec{a}_3").next_to(a3.get_center(), DL).rotate(PI/2,axis=RIGHT)
        x1_label = always_redraw(
            lambda: MathTex(r"x_1 = " f"{x1.get_value():.2f}").next_to(a1_def, DOWN).scale(0.75)
        )
        x1a3_label = always_redraw(
            lambda: MathTex(r"x_1\vec{a}_3").next_to(x1a3.get_center(), UL).rotate(PI/2,axis=RIGHT)
        )
        #deprel_def = MathTex(r"\vec{a}_1 - \vec{a}_2 - \vec{a}_3 = \vec{0}").next_to(x1_label, 1.1*RIGHT).scale(0.65)
        span_def = MathTex(r"\text{Span}(\{\vec{a}_1, \vec{a}_2}\})", color=ORANGE).to_edge(DL).scale(0.75)
        title = MathTex(r"\text{Span}(\{\vec{a}_1, \vec{a}_2, \vec{a}_3\}) = \, \text{a plane in} \, \mathbb{R}^3").to_edge(UR).scale(0.75)
        title2 = MathTex(r"\text{Sliding along} \, x_1 \vec{a}_3 \, \text{...}").to_edge(UR).scale(0.75)

        # VGroups

        # Animation Start
        self.add(grid)
        self.wait()

        self.add_fixed_in_frame_mobjects(a1_def, a2_def, a3_def)
        self.play(FadeIn(a1, a2, a1_label, a2_label))
        self.wait()
        self.move_camera(phi=85 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(75*DEGREES, about='theta')

        self.play(
            FadeIn(spana1a2),
            FadeOut(a1, a2, a1_label, a2_label),
            run_time=4
        )
        self.add_fixed_in_frame_mobjects(span_def)
        self.wait()
        self.stop_ambient_camera_rotation(about='theta')
  
        self.play(
            FadeIn(a3, a3_label)   
        )
        self.wait()

        # spana1a2 moves along x1a3
        self.play(
            FadeOut(a3, a3_label),
            FadeIn(x1a3, x1a3_dot, x1a3_label),
        )
        self.add_fixed_in_frame_mobjects(x1_label)
        self.wait()

        self.play(spana1a2.animate.move_to(x1a3.get_end()))

        self.begin_ambient_camera_rotation(30*DEGREES, about='theta')

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
            x1.animate.set_value(1.75),
            run_time=1, 
            rate_func=linear
        )

        self.stop_ambient_camera_rotation(about='theta')

        self.play(
            x1.animate.set_value(-3),
            run_time=4, 
            rate_func=linear
        )

        self.begin_ambient_camera_rotation(45*DEGREES, about='theta')

        self.play(
            x1.animate.set_value(1),
            run_time=4, 
            rate_func=linear
        )
        self.wait()

        self.play(
            FadeOut(spana1a2, x1a3, x1a3_dot, x1a3_label, x1_label),
            #FadeIn(spanall),
        )
        self.stop_ambient_camera_rotation(about='theta')
        self.remove(span_def, title2)
        self.add_fixed_in_frame_mobjects(title)
        self.wait(3)