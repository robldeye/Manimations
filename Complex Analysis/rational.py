from manim import *
import numpy as np

class RationalTrace(Scene):
    def construct(self):
        # Set up axes for the complex plane
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=8,
            axis_config={"include_tip": True, "numbers_to_exclude": []},
        )
        
        # Add labels for axes
        labels = axes.get_axis_labels(x_label="R", y_label="iR")
        x_label = labels[0]
        x_label.next_to(axes.c2p(2, 0), direction=DR, buff=0.1)

        # Functions
        def z(theta):
            return np.exp(1j * theta)+np.exp(1j * theta * 2/3)
        
        def u(theta):
            return np.exp(1j * theta)
        
        def v(theta): 
            return np.exp(1j * theta * 2/3)

        # Create a ValueTracker for theta
        theta_tracker = ValueTracker(0)

        # Dots
        dot = Dot(color=YELLOW)
        dot.add_updater(
            lambda d: d.move_to(
                axes.c2p(z(theta_tracker.get_value()).real, z(theta_tracker.get_value()).imag)
            )
        )
        dotu = Dot(color=RED)
        dotu.add_updater(
            lambda d: d.move_to(
                axes.c2p(u(theta_tracker.get_value()).real, u(theta_tracker.get_value()).imag)
            )
        )

        # Traces
        trace = TracedPath(dot.get_center, stroke_color=YELLOW, stroke_width=4)
        L1 = Line(start=ORIGIN, end=dotu, color=RED)
        L1.add_updater(
            lambda l: l.become(
                Line(
                    ORIGIN,
                    axes.c2p(u(theta_tracker.get_value()).real, u(theta_tracker.get_value()).imag),
                    color=RED
                )
            )
        )
        L2 = Line(start=dotu, end=dot, color=YELLOW)
        L2.add_updater(
            lambda l: l.become(
                Line(
                    axes.c2p(u(theta_tracker.get_value()).real, u(theta_tracker.get_value()).imag),
                    axes.c2p(z(theta_tracker.get_value()).real, z(theta_tracker.get_value()).imag),
                    color=YELLOW
                )
            )
        )

        # Create a moving label for theta
        label = always_redraw(
            lambda: MathTex(rf"z({theta_tracker.get_value()*(1/np.pi):.2f}\pi)")
            .next_to(dot, UP)
        )
        title = MathTex("z(\\theta) =", "e^{i \\theta}", "+", "e^{i \\theta \\frac{2}{3}}").to_edge(UR)

        # Define the parametric curve to trace z(theta)
        parametric_curve = axes.plot_parametric_curve(
            lambda t: [z(t).real, z(t).imag],
            t_range=[0, 6*np.pi],
            color=BLUE
        )

        # Add the components to the scene
        self.play(Create(axes), Write(labels))
        self.play(Write(title))
        self.wait(1)
        self.add(dot, dotu, trace, label, L1, L2)

        # Animate the ValueTracker to move the dot along the curve
        self.play(
            theta_tracker.animate.set_value(6*np.pi),
            run_time=10,
            rate_func=smooth
        )
        #self.add(parametric_curve)

        self.wait(2)
