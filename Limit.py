from manim import *

class Limit(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-1, 3, 0.5],
            y_range=[-5, 5, 1],
            axis_config={"include_tip": False},
        ).add_coordinates()

        # Define the function
        func = lambda x: x**2 - 4
        graph = axes.plot(func, color=BLUE, x_range=[-1, 3])

        # Add labels for axes
        x_label = axes.get_x_axis_label("t")
        y_label = axes.get_y_axis_label("y")

        # Highlight the point of interest
        limit_point = axes.input_to_graph_point(1, graph)
        limit_dot = Dot(limit_point, color=YELLOW)

        # Approaching dots from both sides
        left_dot = Dot(color=RED)
        right_dot = Dot(color=GREEN)

        left_tracker = ValueTracker(0.5)
        right_tracker = ValueTracker(0.5)

        left_dot.add_updater(lambda d: d.move_to(axes.c2p(1 - left_tracker.get_value(), func(1 - left_tracker.get_value()))))
        right_dot.add_updater(lambda d: d.move_to(axes.c2p(1 + right_tracker.get_value(), func(1 + right_tracker.get_value()))))

        # Annotations
        left_label = MathTex("t \\to 1^-")
        right_label = MathTex("t \\to 1^+")
        limit_def = MathTex("\lim_{t\\to1}f(t)=f(1)=-3").next_to(limit_point, DR, buff=0.5)
        func_label = MathTex("f(t)=t^2-4").move_to(axes.c2p(2,4))
        func_label.set_color(BLUE)

        left_label.add_updater(lambda l: l.next_to(axes.c2p(1 - left_tracker.get_value(), 3), DOWN))
        right_label.add_updater(lambda l: l.next_to(axes.c2p(1 + right_tracker.get_value(), 2), DOWN))

        # Dotted lines between dots and function outputs
        left_line = always_redraw(lambda: DashedLine(
            start=axes.c2p(1 - left_tracker.get_value(), 0),
            end=axes.c2p(1 - left_tracker.get_value(), func(1 - left_tracker.get_value())),
            color=RED
        ))

        right_line = always_redraw(lambda: DashedLine(
            start=axes.c2p(1 + right_tracker.get_value(), 0),
            end=axes.c2p(1 + right_tracker.get_value(), func(1 + right_tracker.get_value())),
            color=GREEN
        ))

        # Add everything to the scene
        self.add(axes, graph, x_label, y_label, func_label, limit_dot, left_line, right_line)

        # Animations
        self.play(FadeIn(left_line, right_line))
        self.play(FadeIn(left_label, right_label))
        self.play(FadeIn(left_dot, right_dot))

        self.play(
            left_tracker.animate.set_value(0),
            right_tracker.animate.set_value(0),
            run_time=4
        )

        self.play(FadeOut(left_label, right_label), FadeOut(left_dot, right_dot), FadeOut(left_line, right_line))

        # Final emphasize the limit
        self.play(Circumscribe(limit_dot, color=YELLOW))
        self.play(FadeIn(limit_def))
        self.wait()