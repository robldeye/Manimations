from manim import *

class Coordinates(Scene):
    def construct(self):

        grid = NumberPlane(
            background_line_style={"stroke_color": YELLOW, "stroke_opacity": 0.5}
        )
        grid2 = NumberPlane(
            background_line_style={"stroke_color": GREEN, "stroke_opacity": 0.25}
        )

        # Mobjects
        matrix = [[1, 1, 0], [-1, 2, 0], [0, 0, 0]]
        basis_vector_1 = Vector([1, 0, 0], color=GREEN)
        basis_vector_2 = Vector([0, 1, 0], color=GREEN)
        bvec = Vector([5, 1, 0], color=GREEN)
        transformed_vector_1 = Vector(np.dot(matrix, [1, 0, 0]), color=YELLOW)
        transformed_vector_2 = Vector(np.dot(matrix, [0, 1, 0]), color=YELLOW)

        # Labels
        title = MarkupText("Coordinates relative to a basis").to_edge(UP).scale(0.75)
        label = MathTex(r"A = \begin{bmatrix} 1 & 1 \\ -1 & 2 \end{bmatrix}").to_corner(UL).scale(0.75)
        basis1_def = MathTex("\\beta_{std}", " = \\left\\{ \\begin{bmatrix} 1 \\\ 0 \\end{bmatrix}, \\begin{bmatrix} 0 \\\ 1 \\end{bmatrix} \\right\\}").next_to(label, DOWN, buff=-0.05).scale(0.75)
        basis1_def[0].set_color(GREEN)
        basis2_def = MathTex("\\beta", " = \\left\\{ \\begin{bmatrix} 1 \\\ -1 \\end{bmatrix}, \\begin{bmatrix} 1 \\\ 2 \\end{bmatrix} \\right\\}").next_to(basis1_def, DOWN, buff=-0.05).scale(0.75)
        basis2_def[0].set_color(YELLOW)
        v_1_label = MathTex(r"\begin{bmatrix} 1 \\ 0 \end{bmatrix}").next_to(basis_vector_1.get_end(), DR)
        v_2_label = MathTex(r"\begin{bmatrix} 0 \\ 1 \end{bmatrix}").next_to(basis_vector_2.get_end(), UL)
        b_def1 = MathTex(r"[\vec{b}]_{std}", r" = \begin{bmatrix} 5 \\ 1 \end{bmatrix}").next_to(basis2_def, DOWN).scale(0.75)
        b_def1[0].set_color(GREEN)
        b_def2 = MathTex(r"[\vec{b}]_{\beta}", r" = \begin{bmatrix} 3 \\ 2 \end{bmatrix}").next_to(b_def1, RIGHT).scale(0.75)
        b_def2[0].set_color(YELLOW)
        b_label1 = MathTex(r"5\vec{v}_1+\vec{v}_2").next_to(bvec.get_end(), DOWN, buff=0.5)
        b_label2 = MathTex(r"3\vec{a}_1+2\vec{a}_2").next_to(bvec.get_end(), DOWN, buff=0.5)
        Tv_1_label = MathTex(r"\vec{a}_1").next_to(transformed_vector_1.get_end(), DOWN)
        Tv_2_label = MathTex(r"\vec{a}_2").next_to(transformed_vector_2.get_end(), UL)

        # Vgroups
        vector_1_group = VGroup(basis_vector_1, v_1_label)
        vector_2_group = VGroup(basis_vector_2, v_2_label)
        transformed_vector_1_group = VGroup(transformed_vector_1, Tv_1_label)
        transformed_vector_2_group = VGroup(transformed_vector_2, Tv_2_label)

        # Scene start
        self.play(
            Write(title),
            FadeIn(grid, label)
        )
        self.wait()
        self.play(
            FadeIn(basis1_def, vector_1_group, vector_2_group)
        )
        self.wait(2)
        self.play(
            FadeIn(bvec, b_label1, b_def1)
        )
        self.wait()


        # Apply A
        self.play(
            ApplyMatrix(matrix, grid), 
            Transform(vector_1_group, transformed_vector_1_group), 
            Transform(vector_2_group, transformed_vector_2_group),
            FadeIn(basis2_def),
            bvec.animate.set_color(YELLOW),
            run_time=3
        )
        self.wait()
        self.play(
            FadeIn(b_def2),
            Transform(b_label1, b_label2)
        )
        self.wait()
        
        #self.play(FadeOut(grid), run_time=1)
        self.play(FadeIn(grid2))
        self.wait(2)
        self.play(FadeOut(grid2))

        # Hold the final scene
        self.wait(3)
