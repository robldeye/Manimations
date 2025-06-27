from manim import *

class SpanLine(Scene):
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
        asum = Vector([4, 1], color=PURPLE)
        x1 = ValueTracker(1)
        x2 = ValueTracker(1)
        x1a1 = always_redraw(
            lambda: Vector([2*x1.get_value(),2*x1.get_value()], color=GREEN)
        )
        x2a2 = always_redraw(
            lambda: Vector([2*x2.get_value(), -1*x2.get_value()], color=YELLOW)
        )
        xasum = always_redraw(
            lambda: Vector([4*x2.get_value(), 1*x2.get_value()], color=YELLOW).shift(Vector([2*x1.get_value(), 2*x1.get_value()], color=GREEN).get_end())  
        )
        span_a2 = Line(
            start=-10*a2.get_unit_vector(),
            end=10*a2.get_unit_vector(),
            color=YELLOW,
            stroke_width=4,
        )
        span_a2.add_updater(
            lambda l: l.move_to(x1a1.get_end())
        )

        # Labels
        a1_def = MathTex(r"\vec{a}_1=\begin{bmatrix} 2 \\ 2 \end{bmatrix}", color=GREEN).to_edge(UL)
        a1_label = always_redraw(
            lambda: MathTex(r"\vec{a}_1", color=GREEN).next_to(a1.get_center(), UL)
        )
        vsum_label = MathTex(r"\vec{a}_1 + \vec{a}_2", color=PURPLE).next_to(asum.get_center(), UL)
        x1a1_label = always_redraw(
            lambda: MathTex(f"{x1.get_value():.2f}" r"\vec{a}_1", color=GREEN).next_to(x1a1.get_center(), UL)
        )
        a2_def = MathTex(r"\vec{a}_2=\begin{bmatrix} 2 \\ -1 \end{bmatrix}", color=YELLOW).next_to(a1_def, DOWN)
        a2_label = MathTex(r"\vec{a}_2", color=YELLOW).next_to(a2.get_center(), DOWN)
        xasum_label = always_redraw(
            lambda: MathTex(f"{x2.get_value():.2f}" r"\vec{a}_2", color=YELLOW).next_to(xasum.get_center(), DOWN)
        )
        x2a2_label = always_redraw(
            lambda: MathTex(f"{x2.get_value():.2f}" r"\vec{a}_2", color=YELLOW).next_to(x2a2.get_center(), DOWN)
        )
        #sum_label = MathTex(r"x_1 \vec{a}_1 + x_2 \vec{a}_2")
        span_label = always_redraw(
            lambda: MathTex(r"\text{Span}(\vec{a}_2)", color=YELLOW).next_to(x1a1.get_end(), UR)
        )
        title = MathTex(r"\text{Span}(\{\vec{a}_1, \vec{a}_2\})=\mathbb{R}^2").to_edge(UP).scale(1.25)

        # VGroups

        a2_grp = VGroup(a2, a2_label)
        linegroup = VGroup(x1a1, x1a1_label, span_a2, span_label)
        fillgroup = VGroup()
        fillgroup.add(*[span_a2 for x1 in range(-3,3)])

        # Get to position
        self.add(grid)
        self.wait()
        self.play(Write(a1_def))
        self.play(Write(a2_def))
        self.play(FadeIn(a1, a2, a1_label, a2_label, run_time=1))
        self.wait()
        self.play(
            a2_grp.animate.shift(a1.get_end()),
            a2_label.animate.shift(a1.get_end(), UP)
        )
        self.wait()

        # Sweeping Line      
        self.play(
            FadeOut(a1, a1_label, a2_grp),
            FadeIn(linegroup)
        )
        self.wait(2)
        self.play(x1.animate.set_value(3), run_time=2, rate_func=linear)
        self.wait(1)
        self.play(x1.animate.set_value(-3), run_time=6, rate_func=linear)
        self.play(FadeOut(linegroup))
        self.add(fillgroup)
        self.play(Write(title))
        self.wait(3)