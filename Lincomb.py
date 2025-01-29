from manim import *

class Lincomb(Scene):
    def construct(self):
        # Create the number plane (grid)
        grid = NumberPlane(
            x_range=(-10,10,1),
            y_range=(-5,5,1),
            background_line_style={"stroke_color": BLUE, "stroke_width": 2, "stroke_opacity": 0.8},
            faded_line_style={"stroke_color": BLUE, "stroke_width": 1, "stroke_opacity": 0.5},
            faded_line_ratio=2,
        )

        # Mobjects
        a1 = Vector([2, 2], color=GREEN)
        a2 = Vector([2, -1], color=YELLOW)
        asum = Vector([4, 1], color=ORANGE)
        a1copy = Vector([2, 2], color=GREEN)
        a2copy = Vector([2, -1], color=YELLOW)

        # Labels
        a1_def = MathTex(r"\vec{a}_1=\begin{bmatrix} 2 \\ 2 \end{bmatrix}", color=GREEN).to_edge(UL)
        a1_label = MathTex(r"\vec{a}_1", color=GREEN).next_to(a1.get_center(), UL)
        a2_def = MathTex(r"\vec{a}_2=\begin{bmatrix} 2 \\ -1 \end{bmatrix}", color=YELLOW).next_to(a1_def, DOWN)
        a2_label = MathTex(r"\vec{a}_2", color=YELLOW).next_to(a2.get_center(), DOWN)
        a1copy_label = MathTex(r"\vec{a}_1", color=GREEN).next_to(a1copy.get_center(), UL)
        a2copy_label = MathTex(r"\vec{a}_2", color=YELLOW).next_to(a2copy.get_center(), DOWN)
        asum_def = MathTex(r"\vec{a}_1+\vec{a}_2=\begin{bmatrix} 4 \\ 1 \end{bmatrix}", color=ORANGE).to_edge(UR)
        asum_label = MathTex(r"\vec{a}_1 + \vec{a}_2", color=ORANGE).next_to(asum.get_end(), RIGHT)
        title = MarkupText("Vector Addition").to_edge(UP)
        title2 = MathTex(r"\vec{a}_1+\vec{a}_2 = \vec{a}_2+\vec{a}_1").to_edge(DOWN)

        # VGroups
        a1_grp = VGroup(a1, a1_label)
        a2_grp = VGroup(a2, a2_label)
        a1copy_grp = VGroup(a1copy, a1copy_label)
        a2copy_grp = VGroup(a2copy, a2copy_label)


        # Vector Addition
        self.add(grid)
        self.wait()
        self.play(Write(title))
        self.play(Write(a1_def))
        self.play(Write(a2_def))
        self.play(FadeIn(a1_grp, a2_grp, a1copy_grp, a2copy_grp, run_time=1))
        self.wait()

        self.play(
            a2copy_grp.animate.shift(a1.get_end()),
            a2copy_label.animate.shift(a1.get_end(), UP)
        )
        self.wait(2)
        self.play(
            a1copy_grp.animate.shift(a2.get_end()),
            a1copy_label.animate.shift(a2.get_end(), DR)
        )
        self.wait(2)
        self.play(FadeIn(asum, asum_label))
        self.wait(1)
        self.play(Write(asum_def))
        self.wait(1)
        self.play(Write(title2))
        self.wait(3)