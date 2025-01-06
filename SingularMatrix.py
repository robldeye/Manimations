from manim import *

class SingularMatrix(Scene):
    def construct(self):
        # Define the transformation matrix
        matrix = [[1, -1, 0], [-1, 1, 0], [0, 0, 0]]

        # Create the number plane (grid)
        grid = NumberPlane(
            x_axis_config={"color": YELLOW},
            y_axis_config={"color": YELLOW},
            background_line_style={"stroke_color": YELLOW, "stroke_opacity": 0.5}
        )

        # Create the background plane (grid2)
        grid2 = NumberPlane(
            background_line_style={"stroke_opacity": 0.25}
        )

        # Create the initial basis vectors
        basis_vector_1 = Arrow(ORIGIN, [1, 0, 0], buff=0, color=RED)
        basis_vector_2 = Arrow(ORIGIN, [0, 1, 0], buff=0, color=GREEN)

        # Apply the transformation to the basis vectors
        transformed_vector_1 = Arrow(ORIGIN, np.dot(matrix, [1, 0, 0]), buff=0, color=RED)
        transformed_vector_2 = Arrow(ORIGIN, np.dot(matrix, [0, 1, 0]), buff=0, color=GREEN)

        # Label the transformation matrix
        label = MathTex(r"A = \begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix}").to_corner(UL)
        v_1_label = MathTex(r"\begin{bmatrix} 1 \\ 0 \end{bmatrix}").next_to(basis_vector_1, DR)
        v_2_label = MathTex(r"\begin{bmatrix} 0 \\ 1 \end{bmatrix}").next_to(basis_vector_2, UL)
        Tv_1_label = MathTex(r"A\begin{bmatrix} 1 \\ 0 \end{bmatrix}").next_to(transformed_vector_1, DOWN)
        Tv_2_label = MathTex(r"A\begin{bmatrix} 0 \\ 1 \end{bmatrix}").next_to(transformed_vector_2, UP)

        # Group each vector with its label
        vector_1_group = VGroup(basis_vector_1, v_1_label)
        vector_2_group = VGroup(basis_vector_2, v_2_label)
        transformed_vector_1_group = VGroup(transformed_vector_1, Tv_1_label)
        transformed_vector_2_group = VGroup(transformed_vector_2, Tv_2_label)

        # Add the grid, label, and basis vectors to the scene
        self.add(grid, label, basis_vector_1, basis_vector_2, v_1_label, v_2_label)

        # Apply the linear transformation to the grid
        self.play(
                ApplyMatrix(matrix, grid),
                Transform(vector_1_group, transformed_vector_1_group), 
                Transform(vector_2_group, transformed_vector_2_group),
                run_time=3
        )
        
        self.play(FadeIn(grid2, run_time=1))  

        # Hold the final scene
        self.wait(3)