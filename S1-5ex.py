from manim import *

class null(ThreeDScene):
    def construct(self):
        # Create the 3D axes
        axes = ThreeDAxes()
        self.add(axes)

        x_range = [-5, 5, 1]
        y_range = [-5, 5, 1]
        z_range = [-5, 5, 1]

        # Mobjects
        basis_vector_1 = Arrow(ORIGIN, [1, 0, 0], buff=0)
        basis_vector_2 = Arrow(ORIGIN, [0, 1, 0], buff=0)
        basis_vector_3 = Arrow(ORIGIN, [0, 0, 1], buff=0)

        matrix = [
            [3, -4, 5],
            [1, -1, 1],
            [0, -1, 2]
        ]

        cube = Cube(side_length=5, fill_opacity=0.25, color=BLUE)
        surf = Surface(
            lambda u, v: np.array([
                3*u-4*v,
                1*u-1*v,
                -1*v
            ]),
            u_range=[-8, 8], 
            v_range=[-8, 8],
            color=BLUE,
            fill_opacity=0.25, 
            resolution=(15, 32)
        )
        null = Line(axes.c2p(-5, -10, -5), axes.c2p(5, 10, 5), color=YELLOW)
        zero = Dot(color=YELLOW).move_to(axes.c2p(0,0,0))

        # Labels
        null_def = MathTex(r"\text{Span}\left(\left\{\begin{bmatrix} 1 \\ 2 \\ 1 \end{bmatrix}\right\}\right)", color=YELLOW).to_corner(DL)
        label = MathTex(r"A = \begin{bmatrix} 3 & -4 & 5 \\ 1 & -1 & 1 \\ 0 & -1 & 2 \end{bmatrix}", color=BLUE).to_corner(UL).scale(0.7)
        label2 = MathTex(r"A\text{Span}\left(\left\{\begin{bmatrix} 1 \\ 2 \\ 1 \end{bmatrix}\right\}\right) = \vec{0}").to_corner(UR).scale(0.7)

        # Mobject groups
        vector_grp = VGroup(cube, basis_vector_1, basis_vector_2, basis_vector_3)

        # Initialize scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        self.add(vector_grp, label, null)
        self.add_fixed_in_frame_mobjects(label, null_def)
        self.wait(1)

        # Transformatio
        self.play(
            vector_grp.animate.apply_matrix(matrix),
            Transform(null, zero),
            run_time=5)
        
        # Rotate scene
        self.begin_ambient_camera_rotation(25*DEGREES, about='theta')
        self.add_fixed_in_frame_mobjects(label2)
        self.wait(10)
        self.stop_ambient_camera_rotation(about='theta')
        self.wait(2)