from manim import *

class tran2(Scene):
    def construct(self):
        # Grids
        grid = NumberPlane(
            background_line_style={"stroke_color": BLUE, "stroke_opacity": 0.5}
        )
        grid2 = NumberPlane(
            background_line_style={"stroke_color": BLUE, "stroke_opacity": 0.25}
        )

        # Mobjects
        matrix = [[1, 1, 0], [-1, 2, 0], [0, 0, 0]]
        t = ValueTracker(0)
        basis_vector_1 = Arrow(ORIGIN, [1, 0, 0], buff=0, color=RED)
        basis_vector_2 = Arrow(ORIGIN, [0, 1, 0], buff=0, color=GREEN)
        transformed_vector_1 = Arrow(ORIGIN, np.dot(matrix, [1, 0, 0]), buff=0, color=RED)
        transformed_vector_2 = Arrow(ORIGIN, np.dot(matrix, [0, 1, 0]), buff=0, color=GREEN)

        # Labels
        label = MathTex(r"A = \begin{bmatrix} 1 & 1 \\ -1 & 2 \end{bmatrix}").to_corner(UL).scale(0.75)
        v_1_label = MathTex(r"\begin{bmatrix} 1 \\ 0 \end{bmatrix}").next_to(basis_vector_1, DR)
        v_2_label = MathTex(r"\begin{bmatrix} 0 \\ 1 \end{bmatrix}").next_to(basis_vector_2, UL)
        Tv_1_label = MathTex(r"A\begin{bmatrix} 1 \\ 0 \end{bmatrix}").next_to(transformed_vector_1, DOWN)
        Tv_1_label2 = MathTex(r"= \begin{bmatrix} 1 \\ -1 \end{bmatrix}").next_to(Tv_1_label, RIGHT)
        Tv_2_label = MathTex(r"A\begin{bmatrix} 0 \\ 1 \end{bmatrix}").next_to(transformed_vector_2, RIGHT)
        Tv_2_label2 = MathTex(r"= \begin{bmatrix} 1 \\ 2 \end{bmatrix}").next_to(Tv_2_label, RIGHT)
        title = MarkupText("Matrices as Transformations").to_edge(UP).scale(0.65)
        tran = MathTex(r"A", r":", r"\mathbb{R}^2",  r"\rightarrow", r"\mathbb{R}^2").to_edge(DL, buff=1.5)
        trandom = MathTex(r"\vec{x}").next_to(tran[2], DOWN)
        tranarrow = MathTex(r"\mapsto").next_to(tran[3], DOWN)
        tranimg = MathTex(r"A\vec{x}").next_to(tran[4], DOWN)

        # VGroups
        vector_1_group = VGroup(basis_vector_1, v_1_label)
        vector_2_group = VGroup(basis_vector_2, v_2_label)
        transformed_vector_1_group = VGroup(transformed_vector_1, Tv_1_label)
        transformed_vector_2_group = VGroup(transformed_vector_2, Tv_2_label)

        # Scene start
        self.play(
            Write(title),
            FadeIn(grid)
        )
        self.wait()
        self.play(
            Write(label), 
            Create(basis_vector_1),
            Create(basis_vector_2),
            Write(v_1_label),
            Write(v_2_label)
        )
        self.wait(2)
        self.play(
            Write(tran),
        )
        self.wait()
        self.play(
            Write(trandom),
            Write(tranarrow),
            Write(tranimg)
        )
        self.wait()

        # Apply transformation
        self.play(
            ApplyMatrix(matrix, grid), 
            Transform(vector_1_group, transformed_vector_1_group), 
            Transform(vector_2_group, transformed_vector_2_group),
            run_time=5)
        
        self.play(
            FadeOut(grid),
            FadeIn(grid2),
        )
        self.wait()
        self.play(FadeIn(Tv_1_label2, Tv_2_label2))
        self.wait(3)
