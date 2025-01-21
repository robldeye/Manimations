from manim import *

class SpanEx(Scene):
    def construct(self):
        # Create the number plane (grid)
        grid = NumberPlane(
            x_range=(-10,10,1),
            y_range=(-5,5,1),
            background_line_style={"stroke_color": BLUE, "stroke_width": 2, "stroke_opacity": 0.8},
            faded_line_style={"stroke_color": BLUE, "stroke_width": 1, "stroke_opacity": 0.5},
            faded_line_ratio=2,
        )

        # Create Mobjects
        v1 = np.array([1,-1,0])
        c1 = ValueTracker(-4)
        c1v1 = lambda: np.array([c1.get_value(), -1*c1.get_value(), 0])
        v1_arrow=Arrow(
            start=ORIGIN,
            end=v1,
            buff=0,
            color=RED,
            stroke_width=4,
        )
        c1v1_arrow=always_redraw(
                lambda: Arrow(
                start=ORIGIN,
                end=c1v1(),
                buff=0,
                color=YELLOW,
                stroke_width=3,
            )
        )
        span_v1 = Line(
            start=-4*v1,
            end=4*v1,
            color=YELLOW,
            stroke_width=2,
        )


        # Label the transformation matrix
        v1_label = MathTex(r"\mathbf{v}_1=\begin{bmatrix} 1 \\ -1 \end{bmatrix}", color=RED).next_to(v1_arrow)
        c1v1_label = always_redraw(
            lambda: MathTex(r"c_1 \mathbf{v}", color=YELLOW).next_to(c1v1_arrow)
        )
        #c1_label = always_redraw(
            #lambda: MathTex(f"c_1 = {c1.get_value():.2f}", color=YELLOW).next_to(grid.c2p(2,2))
        #)
        span_label = MathTex(r"\text{Span}(\mathbf{v}_1)", color=YELLOW).next_to(v1_arrow)

        # Add the grid, label, and basis vectors to the scene
        self.add(grid, v1_arrow, v1_label,)

        # Animate
        self.play(FadeIn(grid, v1_arrow, v1_label, run_time=1))
        self.wait(1)
        self.play(
            Create(c1v1_arrow),
            FadeIn(c1v1_label), #c1_label),
        )
        self.play(c1.animate.set_value(10), run_time=8, rate_func=linear)
        self.play(
            FadeOut(c1v1_arrow, c1v1_label), #c1_label),
            FadeIn(v1_arrow, v1_label),
            Transform(v1_arrow, span_v1),
            Transform(v1_label, span_label),
            run_time=2,
        )

        # Hold the final scene
        self.wait(3)