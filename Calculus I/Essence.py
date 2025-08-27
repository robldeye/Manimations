from manim import *

class Essence(Scene):
    def construct(self):
        title= MarkupText("Differentiation and Integration")
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))

        axes = Axes(
            x_range=[-2*np.pi, 2*np.pi, 1],
            y_range=[-4, 4, 1],
            x_length=2*np.pi,
            y_length=4,
            axis_config={"include_numbers": False, "tip_length": 0.25},
        ).scale(0.9).next_to(title, DOWN).to_edge(LEFT)

        axes2 = axes.copy().next_to(title, DOWN).to_edge(RIGHT)
        axes3 = axes.copy().next_to(axes, DOWN)
        axes4 = axes.copy().next_to(axes2, DOWN)

        # Define f, derivative, and integral
        def f(t):
            return np.sin(t)
        def f_prime(t):
            return np.cos(t)
        def F(t):
            return 1-np.cos(t) #using a = x_range[0]

        # Plot graphs
        graph = axes.plot(f, x_range=[-2*np.pi, 2*np.pi], color=BLUE, stroke_width=4)
        graph2 = axes2.plot(f, x_range=[-2*np.pi, 2*np.pi], color=BLUE, stroke_width=4)
        graph3 = axes3.plot(f_prime, x_range=[-2*np.pi, 2*np.pi], color=RED, stroke_width=4)
        graph4 = axes4.plot(F, x_range=[-2*np.pi, 2*np.pi], color=GREEN, stroke_width=4)


        # Value trackers
        x_value = ValueTracker(-2*np.pi)

        # Dynamic mobjects
        dot = always_redraw(
            lambda: Dot(color=YELLOW).move_to(
                axes.c2p(x_value.get_value(), f(x_value.get_value()))
            )
        )

        dot2 = always_redraw(
            lambda: Dot(color=YELLOW).move_to(
                axes2.c2p(x_value.get_value(), f(x_value.get_value()))
            )
        )

        tangent_line = always_redraw(
            lambda: axes.get_secant_slope_group(
                graph=graph,
                x=x_value.get_value(),
                dx=0.001,
                secant_line_color=RED,
                secant_line_length=2,
            )
        )

        integral_area = always_redraw(
            lambda: axes2.get_area(
                graph2,
                x_range=[-2*np.pi, x_value.get_value()],
                color=GREEN,
                opacity=0.75
            )
        )

        slope_val = always_redraw(
            lambda: MathTex(
                r"\text{Slope }", rf"= {f_prime(x_value.get_value()):.2f}"
            ).set_color_by_tex(r"\text{Slope }", RED).scale(0.8).next_to(axes, DOWN).to_edge(LEFT)
        )
        slope_dot = always_redraw(
            lambda: Dot(
                axes3.c2p(x_value.get_value(), f_prime(x_value.get_value())),
                color=RED
            )
        )
        integral_val = always_redraw(
            lambda: MathTex(
                r"\text{Area }", rf"= {F(x_value.get_value()):.2f}"
            ).set_color_by_tex(r"\text{Area }", GREEN).scale(0.8).next_to(axes2, DOWN).to_edge(RIGHT)
        )
        integral_dot = always_redraw(
            lambda: Dot(
                axes4.c2p(x_value.get_value(), F(x_value.get_value())),
                color=GREEN
            )
        )

        self.play(
            FadeIn(axes), 
            Create(graph)
            )
        self.wait()
        self.play(
            FadeIn(axes2), 
            Create(graph2)
            )
        self.wait()

        self.play(
            FadeIn(tangent_line),
            FadeIn(integral_area)
            )
        self.wait()

        self.play(
            Write(slope_val),
            Write(integral_val)
        )
        self.wait()

        self.play(x_value.animate.set_value(2*np.pi), run_time=8, rate_func=linear)
        self.wait(1)
        self.play(x_value.animate.set_value(-2*np.pi), run_time=1, rate_func=smooth)

        self.play(
            FadeIn(axes3),
            FadeIn(axes4)
        )
        self.play(
            Create(graph3),
            Create(graph4),
            FadeIn(slope_dot),
            FadeIn(integral_dot)
        )

        self.play(x_value.animate.set_value(2*np.pi), run_time=8, rate_func=linear)

        title2 = MathTex(r"f'(x)", r"\quad \quad \quad \text{ and } \quad \quad \quad", r"\int_a^x f(t)dt").to_edge(UP)
        title2[0].set_color(RED)
        title2[2].set_color(GREEN)
        self.play(Transform(title, title2))
        self.wait(3)