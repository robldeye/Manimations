from manim import *

class Eigenspace(ThreeDScene):
    def construct(self):
        # Create the 3D axes
        axes = ThreeDAxes()
        self.add(axes)

        # Vectors and Matrix
        v_1 = Arrow3D(ORIGIN, axes.c2p(1/2, 1, 0))
        Av_1 = Arrow3D(ORIGIN, axes.c2p(1, 2, 0))
        v_2 = Arrow3D(ORIGIN, axes.c2p(-3, 0, 1))
        Av_2 = Arrow3D(ORIGIN, axes.c2p(-6, 0, 2))
        v_bad = Arrow3D(ORIGIN, axes.c2p(1, 1, 1))
        Av_bad = Arrow3D(ORIGIN, axes.c2p(2, -1/4, 5))

        matrix = [[4, -1, 6],
                  [2, 1, 6],
                  [2, -1, 8]]

        null = Polygon(
            axes.c2p(-5/2, 1, 1), 
            axes.c2p(7/2, 1, -1), 
            axes.c2p(5/2, -1, -1), 
            axes.c2p(-7/2, -1, 1),
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=0.5,
            stroke_width=1
        )
        L1 = Line(axes.c2p(-5/2, 1, 1), axes.c2p(7/2, 1, -1), color=GREEN)
        L2 = Line(axes.c2p(7/2, 1, -1), axes.c2p(5/2, -1, -1), color=GREEN)
        L3 = Line(axes.c2p(5/2, -1, -1), axes.c2p(-7/2, -1, 1), color=GREEN)
        L4 = Line(axes.c2p(-7/2, -1, 1), axes.c2p(-5/2, 1, 1), color=GREEN)

        # Labels
        label = MathTex(r"A = \begin{bmatrix} 4 & -1 & 6 \\ 2 & -1 & 6 \\ 2 & -1 & 8 \end{bmatrix}").to_corner(UL).scale(0.7)
        Elabel = MathTex(r"\text{Nul}(A-2I)", color=GREEN).next_to(label, DOWN).scale(0.7)
        v_1_label = MathTex(r"\mathbf{v}_1", color=RED).next_to(v_1).scale(0.7)
        v_2_label = MathTex(r"\mathbf{v}_2", color=GREEN).next_to(v_2).scale(0.7)
        

        # Mobject groups
        v_1_group = VGroup(v_1, v_1_label)
        Av_1_group = VGroup(Av_1, v_1_label.move_to(Av_1.get_end()))
        v_2_group = VGroup(v_2, v_2_label)
        Av_2_group  = VGroup(Av_2, v_2_label)

        volume_group = VGroup(
            null,
            L1,
            L2,
            L3, 
            L4
        )

        # Initialize scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=25 * DEGREES)
        self.add_fixed_in_frame_mobjects(label)
        self.wait()

        self.add(v_1_group, v_2_group)
        self.add_fixed_orientation_mobjects(v_1_label, v_2_label),
        self.wait()

        self.begin_ambient_camera_rotation(25*DEGREES, about='theta')

        self.play(
            volume_group.animate.apply_matrix(matrix), 
            Transform(v_1_group, Av_1_group),
            Transform(v_2_group, Av_2_group),
            Transform(v_bad, Av_bad),
            FadeOut(v_1_label, v_2_label),
            run_time=8,
            rate_func=smooth
        )
        self.add_fixed_in_frame_mobjects(Elabel)
        
        self.wait(4)
        self.stop_ambient_camera_rotation(about='theta')
        self.wait(2)
