from manim import *

class Span(Scene):
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
        x1 = ValueTracker(1)
        x1a1 = Vector([2*x1.get_value(), 2*x1.get_value()], color=GREEN)
        x1a1.add_updater(
            lambda l: l.become(Vector([2*x1.get_value(), 2*x1.get_value()], color=GREEN))
        )
        span_a1 = Line(
            start=6*a1.get_unit_vector(),
            end=-6*a1.get_unit_vector(),
            color=GREEN,
            stroke_width=4,
        )


        # Labels
        a1_label = MathTex(r"\vec{a}_1", color=GREEN).next_to(a1.get_end())
        a1_def = MathTex(r"\vec{a}_1=\begin{bmatrix} 2 \\ 2 \end{bmatrix}", color=GREEN).to_edge(UL)
        x1a1_label = always_redraw(
            lambda: MathTex(f"{x1.get_value():.2f}" r"\vec{a}_1", color=GREEN).next_to(x1a1.get_end())
        )
        x1_def = always_redraw(
            lambda: MathTex(f"x_1 = {x1.get_value():.2f}").next_to(a1_def, DOWN)
        )
        span_label = MathTex(r"\text{Span}(\{\vec{a}_1\})", color=GREEN).next_to(span_a1.get_center(), DR)
        title = MarkupText("Span").to_edge(UP)
        title2 = MathTex(r"\text{Span}(\{\vec{a}_1\})=\{x_1\vec{a}_1 \mid x_1 \in \mathbb{R}\}").to_edge(UP).scale(0.9)

        # Manimation

        self.add(grid)
        self.play(Write(title))
        self.play(Write(a1_def))
        self.play(FadeIn(a1, a1_label, run_time=1))
        self.wait()

        self.play(
            FadeOut(a1, a1_label),
            FadeIn(x1a1, x1a1_label)
        )
        self.wait(1)
        self.play(Write(x1_def))
        self.play(x1.animate.set_value(2), run_time=1, rate_func=linear)
        self.wait(1)
        self.play(x1.animate.set_value(-2), run_time=4, rate_func=linear)
        self.wait(1)
        self.play(
            FadeOut(x1a1, x1a1_label),
            FadeIn(span_a1, span_label)
        )
        self.wait(2)
        self.play(Transform(title, title2))
        self.wait(2)
