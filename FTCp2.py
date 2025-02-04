from manim import *

class FTCp2(Scene):
    def construct(self):
        # Set up the axes
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_numbers": True},
        ).to_edge(LEFT).scale(0.8)

        axes2 = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_numbers": True},
        ).to_edge(RIGHT).scale(0.8)

        # Define functions
        def f(t):
            return -0.5 * (t-2) ** 2 + 2
        def F(t):
            return -(1/6) * t ** 3 + t ** 2

        # Plot graphs
        graph = axes.plot(f, x_range=[0, 5], color=BLUE, stroke_width=4)
        graph2 = axes2.plot(F, x_range=[0, 5], color=GREEN, stroke_width=4)

        # Value trackers
        x_value = ValueTracker(0)

        # Dynamic mobjects
        dot = always_redraw(
            lambda: Dot(color=YELLOW).move_to(
                axes.c2p(x_value.get_value(), f(x_value.get_value()))
            )
        )

        dot2 = always_redraw(
            lambda: Dot(color=YELLOW).move_to(
                axes2.c2p(x_value.get_value(), F(x_value.get_value()))
            )
        )

        tangent_line = always_redraw(
            lambda: axes2.get_secant_slope_group(
                graph=graph2,
                x=x_value.get_value(),
                dx=0.001,
                secant_line_color=RED,
                secant_line_length=3,
            )
        )

        integral_area = always_redraw(
            lambda: axes.get_area(graph, x_range=[0, x_value.get_value()], color=GREEN, opacity=0.5)
        )


        # Label anchors
        a_label_coord = Dot().move_to(axes.c2p(0,0)).set_opacity(0)

        int_label_coord = always_redraw(
            lambda: Dot(color=YELLOW).move_to(
                axes.c2p(0.5 * x_value.get_value() + 0.25, 0.5)
            ).set_opacity(0)
        )

        # Labels
        #FTC_text = MarkupText("Fundamental Theorem of Calculus part II").to_edge(UP)
        derivative_text = MathTex(r"\frac{d}{dx} \int_0^x f(t)dt = f(x)").to_edge(UP).shift(LEFT)
        f_label = always_redraw(
            lambda: MathTex(f"(x, {f(x_value.get_value()):.2f})", color=BLUE).next_to(dot, UR, buff=-0.1).scale(0.8)
        )
        slope_label = always_redraw(
            lambda: MathTex(r"\text{Slope} =" f"{f(x_value.get_value()):.2f}", color=BLUE).next_to(dot2, UL, buff=-0.15).scale(0.8)
        )
        graph_label = MathTex(r"f(t)", color=BLUE).next_to(axes, DOWN)
        graph2_label = MathTex(r"F(x) = \int_0^x f(t) \, dt", color=GREEN).next_to(axes2, DOWN, buff=-0.1)

        # Add elements to the scene
        #self.play(Write(integral_text))
        self.play(Create(axes), Create(graph), FadeIn(graph_label))
        self.play(Create(axes2), Create(graph2), FadeIn(graph2_label))
        self.play(FadeIn(integral_area, int_label_coord, a_label_coord))
        self.wait(1)

        # Show dx rectangle and moving tangent
        self.play(FadeIn(dot), FadeIn(f_label))
        self.play(Create(tangent_line), FadeIn(dot2), FadeIn(slope_label))
        self.wait(1)

        # Animate the increase of x_value
        self.play(x_value.animate.set_value(4), run_time=8, rate_func=smooth)
        self.wait(1)

        # Show derivative result
        self.play(Write(derivative_text))
        self.wait(2)
