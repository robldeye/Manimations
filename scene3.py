from manim import *

class LimitApproachScene(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-1, 3, 0.5],
            y_range=[-5, 5, 1],
            axis_config={"include_tip": True}
        ).add_coordinates()

        # Define the function
        func = lambda x: x**2 - 4
        graph = axes.plot(func, color=BLUE, x_range=[-1, 3])

        # Add labels for axes
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("f(x)")

        # Highlight the point of interest
        limit_point = axes.input_to_graph_point(1, graph)
        limit_dot = Dot(limit_point, color=YELLOW)

        # Approaching dots from both sides
        left_dot = Dot(color=RED)
        right_dot = Dot(color=RED)

        left_tracker = ValueTracker(0.5)
        right_tracker = ValueTracker(0.5)

        left_dot.add_updater(lambda d: d.move_to(axes.c2p(1 - left_tracker.get_value(), func(1 - left_tracker.get_value()))))
        right_dot.add_updater(lambda d: d.move_to(axes.c2p(1 + right_tracker.get_value(), func(1 + right_tracker.get_value()))))

        # Annotations
        left_label = MathTex("x \\to 1^-").next_to(left_dot, LEFT)
        right_label = MathTex("x \\to 1^+").next_to(right_dot, RIGHT)

        # Make labels follow the dots
        left_label.add_updater(lambda l: l.next_to(left_dot, LEFT))
        right_label.add_updater(lambda l: l.next_to(right_dot, RIGHT))



        # Add everything to the scene
        self.add(axes, graph, x_label, y_label, limit_dot)

        # Animations
        self.play(FadeIn(left_label, right_label))
        self.play(FadeIn(left_dot, right_dot))

        self.play(
            left_tracker.animate.set_value(0),
            right_tracker.animate.set_value(0),
            run_time=4
        )

        self.play(FadeOut(left_label, right_label), FadeOut(left_dot, right_dot))

        # Final emphasize the limit
        self.play(Circumscribe(limit_dot, color=YELLOW))
        self.wait()