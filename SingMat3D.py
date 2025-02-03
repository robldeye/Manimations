from manim import *

class SingMat3D(ThreeDScene):
    def construct(self):
        # Create the 3D axes
        axes = ThreeDAxes()
        self.add(axes)

        x_range = [-5, 5, 1]
        y_range = [-5, 5, 1]
        z_range = [-5, 5, 1]

        # Create grid lines parallel to the XY plane
        xy_grid = VGroup()
        for x in range(x_range[0], x_range[1] + 1, x_range[2]):
            xy_grid.add(axes.plot_parametric_curve(
                lambda t: np.array([x, t, 0]),
                t_range=y_range[:2],
                color=BLUE,
            ).set_opacity(0.5))
        for y in range(y_range[0], y_range[1] + 1, y_range[2]):
            xy_grid.add(axes.plot_parametric_curve(
                lambda t: np.array([t, y, 0]),
                t_range=x_range[:2],
                color=BLUE,
            ).set_opacity(0.5))

        # Create grid lines parallel to the XZ plane
        xz_grid = VGroup()
        for x in range(x_range[0], x_range[1] + 1, x_range[2]):
            xz_grid.add(axes.plot_parametric_curve(
                lambda t: np.array([x, 0, t]),
                t_range=z_range[:2],
                color=GREEN,
            ).set_opacity(0.5))
        for z in range(z_range[0], z_range[1] + 1, z_range[2]):
            xz_grid.add(axes.plot_parametric_curve(
                lambda t: np.array([t, 0, z]),
                t_range=x_range[:2],
                color=GREEN,
            ).set_opacity(0.5))

        # Create grid lines parallel to the YZ plane
        yz_grid = VGroup()
        for y in range(y_range[0], y_range[1] + 1, y_range[2]):
            yz_grid.add(axes.plot_parametric_curve(
                lambda t: np.array([0, y, t]),
                t_range=z_range[:2],
                color=RED,
            ).set_opacity(0.5))
        for z in range(z_range[0], z_range[1] + 1, z_range[2]):
            yz_grid.add(axes.plot_parametric_curve(
                lambda t: np.array([0, t, z]),
                t_range=y_range[:2],
                color=RED,
            ).set_opacity(0.5))

        grid_lines = VGroup(xy_grid, xz_grid, yz_grid)

        # Vectors and Matrix
        basis_vector_1 = Arrow(ORIGIN, [1, 0, 0], buff=0, color=RED)
        basis_vector_2 = Arrow(ORIGIN, [0, 1, 0], buff=0, color=GREEN)
        basis_vector_3 = Arrow(ORIGIN, [0, 0, 1], buff=0, color=BLUE)

        matrix = [[1, -1, 2],
                  [-1, 1, -2],
                  [0.5, -0.5, 1]]

        transformed_vector_1 = Arrow(ORIGIN, np.dot(matrix, [1, 0, 0]), buff=0, color=RED)
        transformed_vector_2 = Arrow(ORIGIN, np.dot(matrix, [0, 1, 0]), buff=0, color=GREEN)
        transformed_vector_3 = Arrow(ORIGIN, np.dot(matrix, [0, 0, 1]), buff=0, color=BLUE)

        # Labels
        label = MathTex(r"A = \begin{bmatrix} 1 & -1 & 2 \\ -1 & 1 & -2 \\ 0.5 & -0.5 & 1 \end{bmatrix}").to_corner(UL).scale(0.7)
        label2 = MathTex(r"A(\mathbb{R}^3) = \text{Span}\left(\begin{bmatrix} 1 \\ -1 \\ 2 \end{bmatrix}\right)").to_corner(UR).scale(0.7)
        v_1_label = MathTex(r"\mathbf{v}_1", color=RED).next_to(basis_vector_1).scale(0.7)
        v_2_label = MathTex(r"\mathbf{v}_2", color=GREEN).next_to(basis_vector_2).scale(0.7)
        v_3_label = MathTex(r"\mathbf{v}_3", color=BLUE).next_to(basis_vector_3).scale(0.7)
        Tv_1_label = MathTex(r"A\mathbf{v}_1", color=RED).next_to(transformed_vector_1).scale(0.7)
        Tv_2_label = MathTex(r"A\mathbf{v}_2", color=GREEN).next_to(transformed_vector_2).scale(0.7)
        Tv_3_label = MathTex(r"A\mathbf{v}_3", color=BLUE).next_to(transformed_vector_3).scale(0.7)

        # Mobject groups
        vector_1_group = VGroup(basis_vector_1, v_1_label)
        vector_2_group = VGroup(basis_vector_2, v_2_label)
        vector_3_group = VGroup(basis_vector_3, v_3_label)
        transformed_vector_1_group = VGroup(transformed_vector_1, Tv_1_label)
        transformed_vector_2_group = VGroup(transformed_vector_2, Tv_2_label)
        transformed_vector_3_group = VGroup(transformed_vector_3, Tv_3_label)

        # Initialize scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        self.add(grid_lines, label, vector_1_group, vector_2_group, vector_3_group)
        self.add_fixed_in_frame_mobjects(label)
        self.add_fixed_orientation_mobjects(v_1_label, v_2_label, v_3_label),
        self.add_fixed_orientation_mobjects(Tv_1_label.set_opacity(0), Tv_2_label.set_opacity(0), Tv_3_label.set_opacity(0))
        self.wait(1)

        # Transformation
        self.play(
            grid_lines.animate.apply_matrix(matrix),
            Transform(vector_1_group, transformed_vector_1_group), 
            Transform(vector_2_group, transformed_vector_2_group),
            Transform(vector_3_group, transformed_vector_3_group),
            FadeOut(v_1_label, v_2_label, v_3_label),
            FadeIn(Tv_1_label.set_opacity(1), Tv_2_label.set_opacity(1), Tv_3_label.set_opacity(1)),
            run_time=5)
        
        # Rotate scene
        #self.add_fixed_orientation_mobjects(Tv_1_label, Tv_2_label, Tv_3_label)
        self.begin_ambient_camera_rotation(25*DEGREES, about='theta')
        self.add_fixed_in_frame_mobjects(label2)
        self.wait(4)
        self.stop_ambient_camera_rotation(about='theta')
        self.wait(2)