from manim import *

class ddx(Scene):
    def construct(self):
        # Axes
        #axes = Axes(
            #x_range=[0, 6, 1],
            #y_range=[0, 6, 1],
            #x_length=6,
            #y_length=6,
            #axis_config={"include_numbers": True},
        #)

        axes = NumberPlane(
            background_line_style={"stroke_color": BLUE, "stroke_opacity": 0.25}
        )

        # Functions and VTs
        def f(t):
            return 1/3 * (t-1)**3 - 1/2 * (t-1) + 1
        def fprime(t):
            return (t-1)**2 - 1/2

        fgraph = axes.plot(f, color=BLUE, x_range=[-5, 5], stroke_width=4)
        
        x_value = ValueTracker(-2)
        dx_value = ValueTracker(2)

        # Dynamic mobjects
        dot = always_redraw(
            lambda: Dot(color=YELLOW).move_to(
                axes.c2p(x_value.get_value(), f(x_value.get_value()))
            )
        )

        tangent_line = Line(
            start = axes.c2p(1, f(1)), 
            end = axes.c2p(3, f(3)),
            color=RED
        )
        tangent_line.add_updater(
            lambda l: l.become(
                Line(
                    start = (axes.c2p(x_value.get_value(), f(x_value.get_value()))), 
                    end = (axes.c2p(x_value.get_value()+dx_value.get_value(), f(x_value.get_value()+dx_value.get_value()))),
                    color=RED
                )
            )
        )

        a_label_coord = Dot().move_to(axes.c2p(0,0)).set_opacity(0)

        # Labels
        #FTC_text = MarkupText("Fundamental Theorem of Calculus part II").to_edge(UP)
        title = MarkupText("The Derivative").to_edge(UP)
        f_label = MathTex(r"f(t)", color=BLUE).next_to(axes.c2p(-3, -2))
        slope_label = always_redraw(
            lambda: MathTex(r"\text{Slope} =" f"{fprime(x_value.get_value()):.2f}").next_to(dot, UL, buff=-0.15).scale(0.8)
        )
        graph_label = MathTex(r"f(t)").next_to(axes, DOWN)

        # Scene

        self.play(
            Write(title),
            Create(axes), 
            Create(fgraph),
            Write(graph_label),
            Write(f_label)
        )
        self.wait()

        self.play(
            FadeIn(a_label_coord),
            FadeIn(dot)
        )
        self.wait()

        self.play(
            x_value.animate.set_value(1), 
            run_time=4, 
            rate_func=smooth
        )
        self.wait()

        self.play(
            Create(tangent_line),
            FadeIn(slope_label)
        )

        self.wait(2)