from manim import *

class SpanEx(Scene):
    def construct(self):
        # Grid
        grid = NumberPlane(
            x_range=(-10,10,1),
            y_range=(-5,5,1),
            background_line_style={"stroke_color": BLUE, "stroke_width": 2, "stroke_opacity": 0.8},
            faded_line_style={"stroke_color": BLUE, "stroke_width": 1, "stroke_opacity": 0.5},
            faded_line_ratio=2,
        )

        # Mobjects
        a1 = Vector([2,2], color=GREEN)
        a2 = Vector([2, -1], color=YELLOW)
        asum = Vector([4, 1], color=ORANGE)
        x1 = ValueTracker(1)
        x2 = ValueTracker(1)
        x1a1 = always_redraw(
            lambda: Vector([2*x1.get_value(),2*x1.get_value()], color=GREEN)
        )
        x2a2 = always_redraw(
            lambda: Vector([2*x2.get_value(), -1*x2.get_value()], color=YELLOW).shift(x1a1.get_end())
        )
        xasum = always_redraw(
            lambda: Vector([2*x1.get_value() + 2*x2.get_value(), 2*x1.get_value() -1*x2.get_value()], color=ORANGE)  
        )

        # Labels
        a1_def = MathTex(r"\vec{a}_1=\begin{bmatrix} 2 \\ 2 \end{bmatrix}", color=GREEN).to_edge(UL)
        a1_label = MathTex(r"\vec{a}_1", color=GREEN).next_to(a1.get_center(), UL)
        a2_def = MathTex(r"\vec{a}_2=\begin{bmatrix} 2 \\ -1 \end{bmatrix}", color=YELLOW).next_to(a1_def, DOWN)
        a2_label = MathTex(r"\vec{a}_2", color=YELLOW).next_to(a2.get_center(), DOWN)
        asum_label = MathTex(r"\vec{a}_1 + \vec{a}_2", color=ORANGE).next_to(asum.get_end(), RIGHT)
        x1a1_label = always_redraw(
            lambda: MathTex(f"{x1.get_value():.2f}" r"\vec{a}_1", color=GREEN).next_to(x1a1.get_center(), UL)
        )
        x2a2_label = always_redraw(
            lambda: MathTex(f"{x2.get_value():.2f}" r"\vec{a}_2", color=YELLOW).next_to(x2a2.get_center(), DOWN)
        )
        title = MathTex(r"\text{Some vectors in} \, \text{Span}(\{\vec{a}_1, \vec{a}_2\})").to_edge(UP).scale(1.25)




        # Vector Addition
        self.add(grid)
        self.wait()
        self.play(Write(a1_def))
        self.play(Write(a2_def))
        self.play(FadeIn(a1, a2, a1_label, a2_label, run_time=1))
        self.wait()
        self.play(
            a2.animate.shift(a1.get_end()),
            a2_label.animate.shift(a1.get_end(), UP)
        )
        self.wait()
        self.play(FadeIn(asum, asum_label))
        self.wait()

        
        # Scaling v_1 and v_2 to obtain elements of their Span
        self.play(
            FadeOut(a1, a1_label, a2, a2_label, asum),
            FadeIn(x1a1, x1a1_label, x2a2, x2a2_label)
        )
        self.wait()
        self.play(Write(title))

        # 1
        self.play(
            x1.animate.set_value(1), 
            x2.animate.set_value(-1),
            run_time=1,
            rate_func=smooth
        )
        self.add(
            Vector([2* x1.get_value() + 2*x2.get_value(), 2*x1.get_value() + -1*x2.get_value()], color=ORANGE)
        )
        self.wait()

        # 2
        self.play(
            x1.animate.set_value(-1), 
            x2.animate.set_value(1),
            run_time=1,
            rate_func=smooth
        )
        self.add(
            xasum.copy()
        )
        self.wait()


        self.play(
            FadeOut(x1a1, x1a1_label, xasum)
        )
        self.wait(3)