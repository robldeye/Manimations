from manim import *
import numpy as np
from sympy import symbols, Eq, solve, sqrt, lambdify, latex, nsimplify

class IVT(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 6, 1],
            x_length=5, 
            y_length=7,
            axis_config={"include_tip": True}
        ).to_corner(UR)
        labels = axes.get_axis_labels("x", "y")

        title = MathTex(r"\text{Intermediate Value Theorem}")

        x = symbols('x') #for sympy operations
        f_expr = x**3-4*x**2+2*x+5
        f_num = lambdify(x, f_expr, 'numpy')

        curve = axes.plot(lambda x: f_num(x), x_range=[-0.5, 3], color=BLUE)
        tracker = ValueTracker(0)

        y_dot = Dot(axes.c2p(tracker.get_value(), f_num(tracker.get_value())), color=PURPLE)
        y_dot.add_updater(lambda d: d.become(Dot(axes.c2p(tracker.get_value(), f_num(tracker.get_value())), color=PURPLE)))
        y_line = DashedLine(axes.c2p(0, f_num(tracker.get_value())), y_dot.get_center(), color=PURPLE)
        y_line.add_updater(lambda l: l.become(DashedLine(axes.c2p(0, f_num(tracker.get_value())), y_dot.get_center(), color=PURPLE)))
        y_label = always_redraw(
            lambda: MathTex(rf"n = {f_num(tracker.get_value()):.2f}").next_to(axes.c2p(0, f_num(tracker.get_value())), LEFT)
        )

        self.play(Write(title), run_time=1)
        self.play(title.animate.to_corner(UL))
        self.wait()

        f_label = MathTex(rf"f(x) = {latex(f_expr)}", color=BLUE).next_to(title, DOWN).align_to(title, LEFT)

        self.play(FadeIn(axes, labels))
        self.wait()

        self.play(Create(curve), run_time=2)
        self.play(FadeIn(f_label))
        self.wait()
        self.play(FadeIn(y_label, y_line, y_dot))

        self.play(tracker.animate.set_value(3), run_time=3)
        self.wait()

        IVT1 = MathTex(r"\text{Since } f \text{ is continuous},").next_to(f_label, DOWN).align_to(title, LEFT)
        IVT2 = MathTex(r"\text{any } n \in [f(0), f(3)] \text{ has}").next_to(IVT1, DOWN).align_to(title, LEFT)
        IVT3 = MathTex(r"\text{a } c \in [0, 3] \text{ with } f(c)=n").next_to(IVT2, DOWN).align_to(title, LEFT)

        c_dot = Dot(axes.c2p(tracker.get_value(), 0), color=GREEN)
        c_dot.add_updater(lambda d: d.become(Dot(axes.c2p(tracker.get_value(), 0), color=GREEN)))
        c_line = DashedLine(y_dot.get_center(), c_dot.get_center(), color=GREEN)
        c_line.add_updater(lambda l: l.become(DashedLine(y_dot.get_center(), c_dot.get_center(), color=GREEN)))
        
        c_label = always_redraw(
            lambda: MathTex(rf"c = {tracker.get_value():.2f}").next_to(axes.c2p(tracker.get_value(), 0), DOWN)
        )

        self.play(FadeIn(c_label, c_line, c_dot))
        self.wait()

        self.play(
            AnimationGroup(*(Write(l) for l in [IVT1, IVT2, IVT3]), lag_ratio=0.5)
        )

        self.play(tracker.animate.set_value(2), run_time=2)
        self.wait(0.5)
        self.play(tracker.animate.set_value(0.5), run_time=2)
        self.wait(0.5)
        self.play(tracker.animate.set_value(2.5), run_time=2)
        self.wait(0.5)
        self.play(tracker.animate.set_value(1.5), run_time=2)
        self.wait(0.5)      

        self.wait(3)

