from manim import *

class Determinant(Scene):
    def construct(self):
        # Grids

        grid = NumberPlane(
            x_range=(-20, 20, 1),
            y_range=(-20, 20, 1),
            background_line_style={"stroke_color": BLUE, "stroke_opacity": 0.5}
        )

        grid2 = NumberPlane(
            x_range=(-20, 20, 1),
            y_range=(-20, 20, 1),
            background_line_style={"stroke_color": BLUE, "stroke_opacity": 0.5}
        )

        # Mobjects
        matrix = [[1, 1], [0, 1]]

        basis_vector_1 = Vector([1, 0])
        basis_vector_2 = Vector([0, 1])

        transformed_vector_1 = Vector(np.dot(matrix, [1, 0]))
        transformed_vector_2 = Vector(np.dot(matrix, [0, 1]))

        region = Polygon(
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=0.25,
            stroke_width=1
        )

        t = ValueTracker(0)

        region.add_updater(
            lambda r: r.become(
                Polygon(
                    [0, 0, 0], [1, 0, 0], [1+t.get_value(), 1, 0], [t.get_value(), 1, 0],
                    color=GREEN, 
                    fill_color=GREEN,
                    fill_opacity=0.25,
                    stroke_width=1
                )
            )
        )

        # Labels
        A_label = MathTex(r"A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}").to_corner(UL)
        region_label = MathTex(r"\text{Area} = ", r"1").next_to(A_label, DOWN)
        dynreg_label = MathTex(r"\text{Area} = ", r"???").next_to(A_label, DOWN)
        v_1_label = MathTex(r"\begin{bmatrix} 1 \\ 0 \end{bmatrix}").next_to(basis_vector_1, DR).scale(0.75)
        v_2_label = MathTex(r"\begin{bmatrix} 0 \\ 1 \end{bmatrix}").next_to(basis_vector_2, UL).scale(0.75)
        Tv_1_label = MathTex(r"A\begin{bmatrix} 1 \\ 0 \end{bmatrix}").next_to(transformed_vector_1, DOWN).scale(0.75)
        Tv_2_label = MathTex(r"A\begin{bmatrix} 0 \\ 1 \end{bmatrix}").next_to(transformed_vector_2, LEFT, buff=-0.15).scale(0.75)

        # VGroups
        vector_1_group = VGroup(basis_vector_1, v_1_label)
        vector_2_group = VGroup(basis_vector_2, v_2_label)
        transformed_vector_1_group = VGroup(transformed_vector_1, Tv_1_label)
        transformed_vector_2_group = VGroup(transformed_vector_2, Tv_2_label)

        # Scenes
        self.add(grid)
        self.wait()

        self.play(
            Write(A_label), 
            FadeIn(basis_vector_1, basis_vector_2),
            Write(v_1_label),
            Write(v_2_label)
        )
        self.wait()

        self.play(
            FadeIn(region)
        )
        self.wait()
        self.play(
            Write(region_label)
        )

        # Apply Transformation
        self.play(
            ApplyMatrix(matrix, grid), 
            ApplyMatrix(matrix, region),
            Transform(vector_1_group, transformed_vector_1_group), 
            Transform(vector_2_group, transformed_vector_2_group),
            t.animate.set_value(1),
            Transform(region_label[1], dynreg_label[1].next_to(region_label[0], RIGHT)),
            run_time=3)
        
        self.play(FadeOut(grid), run_time=1)
        self.play(FadeIn(grid2), run_time=1)

        self.wait(3)
