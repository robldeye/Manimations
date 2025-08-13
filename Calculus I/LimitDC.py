from manim import *

class LimitDC(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-1, 3, 1],
            y_range=[-5, 5, 1],
        ).add_coordinates()
        x_label = axes.get_x_axis_label("t").shift(DOWN)
        y_label = axes.get_y_axis_label("s").shift(LEFT)

        # Functions
        funcl = lambda x: x**2-4
        funcr = lambda x: x**2+1
        refdot = Dot() # Need for radius
        graphl = axes.plot(funcl, color=BLUE, x_range=[-1, 1])
        graphr = ParametricFunction(
            lambda x: axes.c2p(x, funcr(x)),
            t_range=[1, 3],
            dt=0.02,
            use_smoothing=True,
            color=BLUE
        )
        # axes.plot(funcr, color=BLUE, x_range=[1.08, 3], dt=0.02)

        # Dots
        refdot = Dot()
        limit_pointl = axes.c2p(1, funcl(1))
        limit_dotl = Dot(axes.c2p(1, funcl(1)), color=BLUE, stroke_width=5)

        limit_pointr = axes.c2p(1, funcr(1))
        limit_dotr = Circle(radius=refdot.radius, color=BLUE, fill_opacity=0).move_to(axes.c2p(1, funcr(1)))

        left_dot = Dot().move_to(axes.c2p(0.5, funcl(0.5)))
        right_dot = Dot().move_to(axes.c2p(1.5, funcr(1.5)))
        leftx_dot = Dot().move_to(axes.c2p(0.5,0)).set_opacity(0)
        rightx_dot = Dot().move_to(axes.c2p(1.5,0)).set_opacity(0)

        left_tracker = ValueTracker(0.5)
        right_tracker = ValueTracker(0.5)

        left_dot.add_updater(lambda d: d.move_to(axes.c2p(1 - left_tracker.get_value(), funcl(1 - left_tracker.get_value()))))
        right_dot.add_updater(lambda d: d.move_to(axes.c2p(1 + right_tracker.get_value(), funcr(1 + right_tracker.get_value()))))
        leftx_dot.add_updater(lambda d: d.move_to(axes.c2p(1 - left_tracker.get_value(), 0)))
        rightx_dot.add_updater(lambda d: d.move_to(axes.c2p(1 + right_tracker.get_value(), 0)))

        # Labels
        leftx_label = always_redraw(
            lambda: MathTex(f"x = {1-left_tracker.get_value():.2f}").next_to(leftx_dot, UP)
        )
        rightx_label = always_redraw(
            lambda: MathTex(f"x = {1+right_tracker.get_value():.2f}").next_to(rightx_dot, DOWN)
        )
        leftf_label = always_redraw(
            lambda: MathTex(f"{funcl(1-left_tracker.get_value()):.2f}", color=BLUE).next_to(left_dot, DOWN)
        )
        rightf_label = always_redraw(
            lambda: MathTex(f"{funcr(1+right_tracker.get_value()):.2f}", color=BLUE).next_to(right_dot, UP)
        )

        limitl_label = MathTex(r"\lim_{t \to 1^-} s(t) = -3").next_to(limit_pointl, RIGHT).scale(0.75)
        limitr_label = MathTex(r"\lim_{t \to 1^+} s(t) = 2").next_to(limit_pointr, RIGHT).scale(0.75)
        title = MarkupText("Sided-Limits").scale(0.8)

        # Lines
        left_line = always_redraw(
            lambda: Arrow(
            start=axes.c2p(1 - left_tracker.get_value(), 0),
            end=axes.c2p(1 - left_tracker.get_value(), funcl(1 - left_tracker.get_value()))
            )
        )

        right_line = always_redraw(
            lambda: Arrow(
            start=axes.c2p(1 + right_tracker.get_value(), 0),
            end=axes.c2p(1 + right_tracker.get_value(), funcr(1 + right_tracker.get_value())),
            max_tip_length_to_length_ratio=0.35
            )
        )

        discontline = DashedLine(axes.c2p(1,-3), axes.c2p(1,2), buff=0.1)

        self.play(Write(title), run_time=1)
        self.play(title.animate.to_edge(UP))
        func_label = MathTex(r"s(t)=\begin{cases}t^2-4 & t \leq 1\\t^2 +1 & t>1\end{cases}", color=BLUE).to_corner(DR)
        self.play(FadeIn(axes, x_label, y_label))
        self.play(FadeIn(graphl, graphr, func_label))
        self.play(FadeIn(limit_dotl, limit_dotr, leftx_dot, rightx_dot))
        self.wait()
        self.play(
            FadeIn(leftx_label, rightx_label),
            FadeIn(left_line, right_line),
            FadeIn(leftf_label, rightf_label),
            FadeIn(left_dot, right_dot)
        )
        self.wait(2)

        self.play(FocusOn(left_dot))
        self.play(
            left_tracker.animate.set_value(0),
            run_time=2
        )
        self.play(FadeOut(left_line, leftx_label))
        self.wait()

        self.play(FocusOn(right_dot))
        self.play(
            right_tracker.animate.set_value(0),
            run_time=2
        )
        self.play(FadeOut(right_line, rightx_label))
        self.wait()

        self.play(Create(discontline))
        self.wait()

        # Final
        self.play(FadeIn(limitl_label, limitr_label))
        DNE_label = MathTex(r"\lim_{t \to 1} s(t) \text{ DNE}").next_to(title, DOWN)
        self.play(Write(DNE_label), run_time=1)
        self.play(Indicate(left_dot), Indicate(right_dot))
        self.wait(3)