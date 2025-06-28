from manim import *

class Intdx(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()
        # Set up the axes
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_numbers": True},
        ).to_edge(LEFT).scale(0.8)

        axes2 = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=5,
            y_length=5,
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
        x_value = ValueTracker(2)
        dx_value = ValueTracker(0)

        # Dynamic mobjects
        dx_rectangle = always_redraw(
            lambda: axes.get_riemann_rectangles(
                graph,
                x_range=[3, 3.5],
                dx=0.5-dx_value.get_value(),
                stroke_width=0,
                color=GREEN,
                show_signed_area=False,
            )
        )

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
        f_label = always_redraw(
            lambda: MathTex(f"(x, {f(x_value.get_value()):.2f})", color=BLUE).next_to(dot, UR, buff=-0.2).scale(0.8)
        )
        slope_label = always_redraw(
            lambda: MathTex(r"\text{Slope} =" f"{f(x_value.get_value()):.2f}", color=BLUE).next_to(dot2, UL, buff=-0.2).scale(0.8)
        )
        graph_label = MathTex(r"f(t)", color=BLUE).next_to(axes.c2p(1.75,-3)).scale(0.8)
        graph2_label = MathTex(r"F(x) = \int_0^x f(t) \, dt", color=GREEN).next_to(axes2.c2p(0.75,-3)).scale(0.8)
        x_label = always_redraw(
            lambda: MathTex(r"x", color=YELLOW).next_to(axes.c2p(x_value.get_value(), -1.25), buff=-0.15).scale(0.8)
        )
        x_label2 = always_redraw(
            lambda: MathTex(r"x", color=YELLOW).next_to(axes2.c2p(x_value.get_value(), -1.25), buff=-0.15).scale(0.8)
        )

        # Add elements to the scene
        #self.play(Write(integral_text))
        self.play(Create(axes), Create(graph), FadeIn(graph_label, x_label))
        self.play(Create(axes2), Create(graph2), FadeIn(graph2_label, x_label2))
        self.play(FadeIn(integral_area, int_label_coord, a_label_coord))
        self.wait(1)

        # Animated mobjects
        self.play(FadeIn(dot, f_label))
        self.play(FadeIn(dot2, slope_label))
        self.wait(1)

        # Animate the increase of x_value
        self.play(x_value.animate.set_value(3), run_time=3, rate_func=linear)
        self.wait(1)
        self.play(self.camera.frame.animate.scale(0.5).move_to(dot))
        self.play(FadeIn(dx_rectangle))
        self.play(dx_value.animate.set_value(0.49), run_time=5, rate_func=linear)
        self.wait(1)
