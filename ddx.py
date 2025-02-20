from manim import *

class ddx(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()

        axes = NumberPlane(
            background_line_style={"stroke_color": BLUE, "stroke_opacity": 0.25},
        )

        # Mobjects
        def f(t):
            return 1/3 * (t-1)**3 - 1/2 * (t-1) + 1
        def fprime(t):
            return (t-1)**2 - 1/2

        fgraph = axes.plot(f, color=BLUE, x_range=[-5, 5], stroke_width=4)
        
        x_value = ValueTracker(-2)
        dx_value = ValueTracker(0)

        # Dynamic mobjects
        dot = always_redraw(
            lambda: Dot(color=YELLOW).move_to(
                axes.c2p(x_value.get_value(), f(x_value.get_value()))
            )
        )

        a_label_coord = Dot().move_to(axes.c2p(0,0)).set_opacity(0)

        # Labels
        #FTC_text = MarkupText("Fundamental Theorem of Calculus part II").to_edge(UP)
        title = MathTex(r"\text{The Derivative of} \, s \, \text{at} \, a").to_edge(UL).scale(0.75)
        slope_def = MathTex(r"\text{Slope}", r"= \frac{s(b) - s(a)}{b-a}").next_to(title, DOWN).scale(0.75)
        deriv_def = MathTex(r"s'(a) = \lim_{b \to a} \frac{s(b) - s(a)}{b-a}").next_to(title, 1.3*DOWN).scale(0.75).shift(0.25*RIGHT)
        slope_def[0].set_color(RED)
        start_label = MathTex(r"a").next_to(axes.c2p(1, 0), 1.2*DOWN)
        fstart_label = MathTex(r"s(a)").next_to(axes.c2p(0, f(1)), LEFT)
        end_label = MathTex(r"b").next_to(axes.c2p(3, 0), DOWN)
        fend_label = MathTex(r"s(b)").next_to(axes.c2p(0, f(3)), LEFT)
        graph_label = MathTex(r"s(t)", color=BLUE).next_to(axes.c2p(4, 3))
        lim_label = MathTex(r"\text{Slide} \, b \to a").next_to(axes.c2p(3,2), DR).scale(0.75)

        # Dashed Lines
        start_line = DashedLine(
            start = start_label, end = axes.c2p(1,1), color=WHITE, stroke_width=2, buff=0.1
        )
        fstart_line = DashedLine(
            start = fstart_label.get_right(), end = axes.c2p(1,1), color=WHITE, stroke_width=2, buff=0.1
        )

        # Scene

        self.play(
            Write(title),
            Create(axes), 
            Create(fgraph),
            Write(graph_label),
        )
        self.play(
            FadeIn(a_label_coord),
            FadeIn(dot),
        )
        self.wait()

        self.play(
            x_value.animate.set_value(1), 
            run_time=1, 
            rate_func=smooth
        )
        self.wait()

        self.play(
            Write(start_label),
            Write(fstart_label),
            Write(start_line),
            Write(fstart_line)
        )
        self.wait()

        scale_factor = 30

        secant_line = axes.get_secant_slope_group(
                graph=fgraph,
                x=1,
                dx=2,
                dx_line_color=WHITE,
                dy_line_color=WHITE,
                dx_label="b-a",
                dy_label="s(b) - s(a)",
                secant_line_color=RED,
                secant_line_length=30,
        )

        moving_secant = always_redraw(
            lambda: Line(
                start=axes.c2p(x_value.get_value(), f(x_value.get_value())) - 
                (axes.c2p(x_value.get_value() + dx_value.get_value(), f(x_value.get_value() + dx_value.get_value())) - 
                axes.c2p(x_value.get_value(), f(x_value.get_value()))) / np.linalg.norm(
                axes.c2p(x_value.get_value() + dx_value.get_value(), f(x_value.get_value() + dx_value.get_value())) - 
                axes.c2p(x_value.get_value(), f(x_value.get_value()))
                ) * (scale_factor - 1) / 2,
    
                end=axes.c2p(x_value.get_value() + dx_value.get_value(), f(x_value.get_value() + dx_value.get_value())) + 
                (axes.c2p(x_value.get_value() + dx_value.get_value(), f(x_value.get_value() + dx_value.get_value())) - 
                axes.c2p(x_value.get_value(), f(x_value.get_value()))) / np.linalg.norm(
                axes.c2p(x_value.get_value() + dx_value.get_value(), f(x_value.get_value() + dx_value.get_value())) - 
                axes.c2p(x_value.get_value(), f(x_value.get_value()))
                ) * (scale_factor - 1) / 2,
    
                color=RED
            )
        )

        dot2 = always_redraw(
            lambda: Dot(color=YELLOW).move_to(
                axes.c2p(x_value.get_value() + dx_value.get_value(), f(x_value.get_value() + dx_value.get_value()))
            )
        )

        self.add(dot2)
        self.play(
            dx_value.animate.set_value(2),
            run_time=2,
            rate_func=smooth
        )
        self.wait()

        end_line = DashedLine(
                start = end_label.get_center()+0.2*UP, end = axes.c2p(1+dx_value.get_value(), f(1+dx_value.get_value())), color=WHITE, stroke_width=2, buff=0.1
        )
        fend_line = DashedLine(
                start = fend_label.get_right()+0.1*RIGHT, end = axes.c2p(1+dx_value.get_value(), f(1+dx_value.get_value())), color=WHITE, stroke_width=2, buff=0.1
        )

        self.play(
            Write(end_label),
            Write(end_line),
            Write(fend_label),
            Write(fend_line)
        )
        self.wait(1)

        self.play(
            self.camera.frame.animate.scale(0.65).move_to(dot.get_center()+RIGHT),
        )

        # Introduce Secant Lines

        self.play(
            FadeIn(secant_line),
            FadeOut(start_line, fstart_line, end_line, fend_line)
        )
        self.wait()
        self.play(
            FadeOut(start_label, fstart_label, end_label, fend_label)
        )
        self.wait()

        self.play(
            Write(slope_def)
        )
        self.wait()

        self.play(
            FadeOut(secant_line),
            FadeIn(moving_secant)
        )
        self.wait()

        self.play(
            FadeIn(lim_label)
        )
        
        fend_line.add_updater(
            lambda l: l.become(
                
            )
        )

        self.play(
            dx_value.animate.set_value(0.001),
            run_time=6,
            rate_func=smooth
        )
        self.play(
            FadeOut(lim_label)
        )

        self.play(
            self.camera.frame.animate.scale(1/0.65).move_to(axes.get_center()),
        )
        self.play(
            ReplacementTransform(slope_def, deriv_def)
        )

        self.wait(4)