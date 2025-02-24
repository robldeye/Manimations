from manim import *

class nullspace2(ThreeDScene):
    def construct(self):
        # Create the 3D axes
        axes = ThreeDAxes()
        self.add(axes)

        # Vectors and Matrix
        v_1 = Arrow(ORIGIN, [1, 0, 0], buff=0, color=RED)
        v_2 = Arrow(ORIGIN, [0, 1, 0], buff=0, color=GREEN)
        v_3 = Arrow(ORIGIN, [0, 0, 1], buff=0, color=BLUE)
        n = Vector(axes.c2p(0, 1, 0), color=GREEN)

        matrix = [[1, -1, 2],
                  [-1, 1, -2],
                  [0.5, -0.5, 1]]

        Av_1 = Arrow(ORIGIN, np.dot(matrix, [1, 0, 0]), buff=0, color=RED)
        Av_2 = Arrow(ORIGIN, np.dot(matrix, [0, 1, 0]), buff=0, color=GREEN)
        Av_3 = Arrow(ORIGIN, np.dot(matrix, [0, 0, 1]), buff=0, color=BLUE)

        cube = Cube(side_length=10, fill_opacity=0.25, fill_color=BLUE)
        line1 = Line(axes.c2p(0, -10, 0), axes.c2p(0, 10, 0), color=GREEN, stroke_width=4)
        line2 = Line(axes.c2p(-10, 0, 0), axes.c2p(10, 0, 0), color=RED, stroke_width=4)
        line3 = Line(axes.c2p(0, 0, -10), axes.c2p(0, 0, 10), color=BLUE, stroke_width=4)

        null = Polygon(
            axes.c2p(10, 10, 0), axes.c2p(-20, 0, 10), axes.c2p(-10, -10, 0), axes.c2p(20, 0, -10),
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=0.25,
            stroke_width=1
        )

        # Labels
        label = MathTex(r"A = \begin{bmatrix} 1 & -1 & 2 \\ -1 & 1 & -2 \\ 0.5 & -0.5 & 1 \end{bmatrix}").to_corner(UL).scale(0.7)
        label2 = MathTex(r"\text{Col}(A)", r" = \text{Span}\left(\begin{bmatrix} 1 \\ -1 \\ 0.5 \end{bmatrix}\right)").to_corner(UR).scale(0.7)
        label2[0].set_color(BLUE)
        label3 = MathTex(r"\text{Nul}(A)", r" = \text{Span}\left(\begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix}, \begin{bmatrix} -2 \\ 0 \\ 1 \end{bmatrix}\right)").to_corner(DR).scale(0.7)
        label3[0].set_color(GREEN)
        v_1_label = MathTex(r"\mathbf{v}_1", color=RED).next_to(v_1).scale(0.7)
        v_2_label = MathTex(r"\mathbf{v}_2", color=GREEN).next_to(v_2).scale(0.7)
        v_3_label = MathTex(r"\mathbf{v}_3", color=BLUE).next_to(v_3).scale(0.7)
        Av_1_label = MathTex(r"A\mathbf{v}_1", color=RED).next_to(Av_1).scale(0.7)
        Av_2_label = MathTex(r"A\mathbf{v}_2", color=GREEN).next_to(Av_2).scale(0.7)
        Av_3_label = MathTex(r"A\mathbf{v}_3", color=BLUE).next_to(Av_3).scale(0.7)

        # Mobject groups
        v_1_group = VGroup(v_1, v_1_label)
        v_2_group = VGroup(v_2, v_2_label)
        v_3_group = VGroup(v_3, v_3_label)
        Av_1_group = VGroup(Av_1, Av_1_label)
        Av_2_group = VGroup(Av_2, Av_2_label)
        Av_3_group = VGroup(Av_3, Av_3_label)
        volume_group = VGroup(null, line1, line2, line3)

        # Initialize scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        self.add_fixed_in_frame_mobjects(label)
        self.wait()

        self.add(v_1_group, v_2_group, v_3_group)
        self.add_fixed_orientation_mobjects(v_1_label, v_2_label, v_3_label),
        self.add_fixed_orientation_mobjects(Av_1_label.set_opacity(0), Av_2_label.set_opacity(0), Av_3_label.set_opacity(0))
        self.wait()

        self.begin_ambient_camera_rotation(25*DEGREES, about='theta')

        self.play(
            volume_group.animate.apply_matrix(matrix),
            Transform(v_1_group, Av_1_group), 
            Transform(v_2_group, Av_2_group),
            Transform(v_3_group, Av_3_group),
            FadeOut(v_1_label, v_2_label, v_3_label),
            FadeIn(Av_1_label.set_opacity(1), Av_2_label.set_opacity(1), Av_3_label.set_opacity(1)),
            run_time=8,
            rate_func=smooth
        )
        self.wait()
        self.add_fixed_in_frame_mobjects(label2, label3)
        
        self.wait(4)
        self.stop_ambient_camera_rotation(about='theta')
        self.wait(2)