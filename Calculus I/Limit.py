from manim import *

class Limit(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-1, 3, 1],
            y_range=[-5, 5, 1],
        ).add_coordinates()
        x_label = axes.get_x_axis_label("t").shift(DOWN)
        y_label = axes.get_y_axis_label("s").shift(LEFT)

        # Functions
        func = lambda x: x**2 - 4
        graph = axes.plot(func, color=BLUE, x_range=[-1, 3])

        # Dots
        limit_point = axes.input_to_graph_point(1, graph)
        limit_dot = Dot(axes.input_to_graph_point(1, graph))

        left_dot = Dot().move_to(axes.c2p(0.5, func(0.5)))
        right_dot = Dot().move_to(axes.c2p(1.5, func(1.5)))
        leftx_dot = Dot().move_to(axes.c2p(0.5,0)).set_opacity(0)
        rightx_dot = Dot().move_to(axes.c2p(1.5,0)).set_opacity(0)

        left_tracker = ValueTracker(0.5)
        right_tracker = ValueTracker(0.5)

        left_dot.add_updater(lambda d: d.move_to(axes.c2p(1 - left_tracker.get_value(), func(1 - left_tracker.get_value()))))
        right_dot.add_updater(lambda d: d.move_to(axes.c2p(1 + right_tracker.get_value(), func(1 + right_tracker.get_value()))))
        leftx_dot.add_updater(lambda d: d.move_to(axes.c2p(1 - left_tracker.get_value(), 0)))
        rightx_dot.add_updater(lambda d: d.move_to(axes.c2p(1 + right_tracker.get_value(), 0)))

        # Labels
        leftx_label = always_redraw(
            lambda: MathTex(f"t={1-left_tracker.get_value():.2f}").next_to(leftx_dot, UP)
        )
        rightx_label = always_redraw(
            lambda: MathTex(f"t={1+right_tracker.get_value():.2f}").next_to(rightx_dot, UP)
        )
        leftf_label = always_redraw(
            lambda: MathTex(f"{func(1-left_tracker.get_value()):.2f}", color=BLUE).next_to(left_dot, DOWN)
        )
        rightf_label = always_redraw(
            lambda: MathTex(f"{func(1+right_tracker.get_value()):.2f}", color=BLUE).next_to(right_dot, DOWN)
        )

        func_label = MathTex(r"s(t)=t^2-4", color=BLUE).to_edge(UL)
        title = MarkupText("A typical Limit example").scale(0.8)
        limit_def = MathTex(r"\lim_{t \to 1} s(t) = -3").next_to(title, DOWN)

        # Lines
        left_line = always_redraw(
            lambda: Arrow(
            start=axes.c2p(1 - left_tracker.get_value(), 0),
            end=axes.c2p(1 - left_tracker.get_value(), func(1 - left_tracker.get_value()))
            )
        )

        right_line = always_redraw(
            lambda: Arrow(
            start=axes.c2p(1 + right_tracker.get_value(), 0),
            end=axes.c2p(1 + right_tracker.get_value(), func(1 + right_tracker.get_value())),
            max_tip_length_to_length_ratio=0.35
            )
        )

        neg3dash = DashedLine(
            start = axes.c2p(0, -3),
            end = axes.c2p(1, -3)
        )

        self.play(Write(title), run_time=1)
        self.play(title.animate.to_edge(UP))
        self.play(FadeIn(axes, x_label, y_label))
        self.play(FadeIn(graph, func_label))
        self.play(FadeIn(limit_dot, leftx_dot, rightx_dot))
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
        self.play(FadeOut(leftx_label, left_line))
        self.wait()

        self.play(FocusOn(right_dot))
        self.play(
            right_tracker.animate.set_value(0),
            run_time=2
        )
        self.play(FadeOut(rightx_label, right_line))
        self.wait()

        self.play(
            FadeOut(leftf_label, rightf_label), 
            FadeOut(left_dot, right_dot)
        )
        self.wait()

        # Final
        self.play(
            Circumscribe(limit_dot, color=YELLOW),
            Write(neg3dash)
        )
        self.play(Write(limit_def), run_time=1)
        self.play(Indicate(limit_dot))
        self.wait(3)