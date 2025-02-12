from manim import *

class transform(Scene):
    def construct(self):
        # Grids
        grid1 = Axes(
            x_range=(-5,5,1),
            y_range=(-5,5,1),
            x_length=5,
            y_length=5
        ).to_edge(LEFT, buff=-0.5).scale(0.75)
        grid2 = Axes(
            x_range=(-5,5,1),
            y_range=(-5,5,1),
            x_length=5,
            y_length=5
        ).scale(0.75)
        grid3 = Axes(
            x_range=(-5,5,1),
            y_range=(-5,5,1),
            x_length=5,
            y_length=5
        ).to_edge(RIGHT, buff=-0.5).scale(0.75)

        # Mobjects
        v = Vector(grid2.c2p(2, 3), color=RED).move_to(grid1.c2p(0,0), aligned_edge=DL)
        vcopy = Vector(grid2.c2p(2, 3), color=RED).move_to(grid1.c2p(0,0), aligned_edge=DL)
        tran1 = Arrow(grid1.get_right(), grid2.get_left())
        Bv = Vector(grid2.c2p(3, -4), color=YELLOW)
        tran2 = Arrow(grid2.get_right(), grid3.get_left())
        ABv = Vector(grid2.c2p(-2, -3), color=GREEN).move_to(grid3.c2p(0,0), aligned_edge=UR)
        tran21 = CurvedArrow(grid1.c2p(2,-5), grid3.c2p(-2, -5))        

        # Labels
        B_def = MathTex(r"B").next_to(tran1, UP).scale(0.75)
        B_defc = MathTex(r"B").next_to(tran1, UP).scale(0.75)
        B_def2 = MathTex(r"B = \begin{bmatrix} \, \vec{b}_1 & \vec{b}_2 \, \end{bmatrix}").next_to(tran1, UP, buff=-0.15).scale(0.75)
        A_def = MathTex(r"A").next_to(tran2, UP).scale(0.75)
        v_label = MathTex(r"\vec{x}").next_to(v.get_end(), UR).scale(0.75)
        v_labelc = MathTex(r"\vec{x}").next_to(v.get_end(), UR).scale(0.75)
        v_label2 = MathTex(r"\vec{x}=\begin{bmatrix} x_1 \\ x_2 \end{bmatrix}").next_to(v.get_end(), UR, buff=-0.15).scale(0.75)
        Bv_label = MathTex(r"B\vec{x}").next_to(Bv.get_end()).scale(0.75)
        Bv_label2 = MathTex(r"x_1\vec{b}_1+x_2\vec{b}_2").next_to(Bv.get_end(), buff=-0.15).scale(0.75)
        ABv_label = MathTex(r"A(B\vec{x})").next_to(ABv.get_end(), LEFT, buff=-0.05).scale(0.75)
        tran21_label = MathTex(r"(AB)\vec{x}").to_edge(DOWN).scale(0.75)
        title = MarkupText("Matrix Multiplication").to_edge(UP).scale(0.75)
        title2 = MathTex(r"(AB)\vec{x} = A(B(\vec{x}))").to_edge(DOWN).scale(0.75)

        # VGroups
        v_grp = VGroup(v, v_label)
        Bv_grp = VGroup(Bv, Bv_label2)
        ABv_grp = VGroup(ABv, ABv_label)

        # Scenes
        self.play(Write(title))
        self.play(
            Create(grid1),
            Create(grid2),
            Create(grid3)
        )
        self.play(
            Create(v),
            Write(v_label)
        )
        self.wait()

        # Add B transformation

        self.play(
            Create(tran1),
            Write(B_def)
        )
        self.wait()

        self.play(
            ReplacementTransform(v_label, v_label2),
            ReplacementTransform(B_def, B_def2)
        )
        self.wait()

        lincomb = VGroup(v_label2, B_def2)

        self.play(
            FadeIn(v.copy(), v_labelc, B_defc),
            ReplacementTransform(v, Bv, run_time=2),
            ReplacementTransform(lincomb, Bv_label2, run_time=2),
        )
        self.wait()

        self.play(
            ReplacementTransform(Bv_label2, Bv_label)
        )
        self.wait()

        # Add A transformation

        self.play(
            Create(tran2),
            Write(A_def)
        )
        self.play(
            FadeIn(Bv_grp.copy()),
            Transform(Bv_grp, ABv_grp, run_time=2)
        )
        self.wait(2)

        self.play(
            Create(tran21),
            Write(tran21_label),
        )
        self.wait()

        self.play(
            FadeIn(vcopy),
            Transform(vcopy, ABv, run_time=4)
        )
        self.wait()

        self.play(
            ReplacementTransform(tran21_label, title2),
        )
        self.wait(2)