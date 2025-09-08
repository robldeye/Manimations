from manim import *
import numpy as np
from sympy import symbols, lambdify, latex, sqrt, Piecewise, Interval, Rational

class IVT(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=7, 
            y_length=7,
            axis_config={"include_tip": True}
        ).to_corner(UR)
        labels = axes.get_axis_labels("x", "y")

        title = MathTex(r"\underline{\text{Intermediate Value Theorem}}")

        x = symbols('x') # for sympy operations
        f_expr = 4/x
        f_num = lambdify(x, f_expr, 'numpy')
        curve = axes.plot(lambda x: f_num(x), x_range=[1, 4], color=BLUE)

        tracker = ValueTracker(1)

        y_dot = Dot(axes.c2p(tracker.get_value(), f_num(tracker.get_value())), color=PURPLE)
        y_dot.add_updater(lambda d: d.become(Dot(axes.c2p(tracker.get_value(), f_num(tracker.get_value())), color=PURPLE)))
        y_line = DashedLine(axes.c2p(0, f_num(tracker.get_value())), y_dot.get_center(), color=PURPLE)
        y_line.add_updater(lambda l: l.become(DashedLine(axes.c2p(0, f_num(tracker.get_value())), y_dot.get_center(), color=PURPLE)))
        y_label1 = MathTex(rf"n = ")
        y_label2 = DecimalNumber(f_num(tracker.get_value())).next_to(y_label1, RIGHT)
        y_labelg = VGroup(y_label1, y_label2).arrange(RIGHT)
        y_labelg.add_updater(
            lambda g: g.become(
                VGroup(
                    MathTex(rf"n = "),
                    DecimalNumber(f_num(tracker.get_value()))
                ).arrange(RIGHT).next_to(axes.c2p(0, f_num(tracker.get_value())), LEFT)
            )
        )

        # Scene 1 Begins

        self.play(Write(title), run_time=1)
        self.play(title.animate.to_corner(UL))
        self.wait(0.5)

        self.play(FadeIn(axes, labels))
        self.wait(0.5)

        self.play(Create(curve), run_time=2)

        f_label = MathTex(rf"\text{{Ex) }}f(x) = {latex(f_expr)} \text{{ on }} [1, 4]", color=BLUE).next_to(title, DOWN).align_to(title, LEFT)
        
        self.play(FadeIn(f_label))
        self.wait(0.5)

        IVT1 = MathTex(r"\text{Since } f \text{ is continuous},").next_to(f_label, 1.5*DOWN).align_to(title, LEFT)
        IVT2 = MathTex(r"\text{any } n \in [f(1), f(4)] \text{ has}").next_to(IVT1, 1.5*DOWN).align_to(title, LEFT)
        IVT3 = MathTex(r"\text{a } c \in [1, 4] \text{ with } f(c)=n").next_to(IVT2, 1.5*DOWN).align_to(title, LEFT)

        self.play(Write(IVT1), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(y_labelg, y_line, y_dot))
        self.wait(0.5)

        self.play(Write(IVT2), run_time=1)
        self.wait(0.5)
        self.play(
            AnimationGroup(
                *(Indicate(m) for m in [IVT2, y_labelg])
            )
        )
        self.wait(0.5)

        self.play(tracker.animate.set_value(4), run_time=2)
        tracker.set_value(4)
        c_dot = Dot(axes.c2p(tracker.get_value(), 0), color=GREEN)
        c_dot.add_updater(lambda d: d.become(Dot(axes.c2p(tracker.get_value(), 0), color=GREEN)))
        c_line = DashedLine(y_dot.get_center(), c_dot.get_center(), color=GREEN)
        c_line.add_updater(lambda l: l.become(DashedLine(y_dot.get_center(), c_dot.get_center(), color=GREEN)))
        c_label1 = MathTex(rf"c = ")
        c_label2 = DecimalNumber(tracker.get_value())
        c_labelg = VGroup(c_label1, c_label2).arrange(RIGHT)
        c_labelg.add_updater(
            lambda g: g.become(
                VGroup(
                    MathTex(rf"c = "),
                    DecimalNumber(tracker.get_value())
                ).arrange(RIGHT).next_to(axes.c2p(tracker.get_value(), 0), DOWN)
            )
        )
        self.wait(0.5)

        self.play(FadeIn(c_labelg, c_line, c_dot))
        self.wait(0.5)

        self.play(Write(IVT3), run_time=1)
        self.wait(0.5)
        self.play(
            AnimationGroup(
                *(Indicate(m) for m in [IVT3, c_labelg])
            )
        )
        self.wait(0.5)

        self.play(tracker.animate.set_value(1.5), run_time=2)
        self.wait(0.5)
        self.play(tracker.animate.set_value(2.5), run_time=2)
        self.wait(0.5)
        self.play(tracker.animate.set_value(2), run_time=2)
        self.wait(0.5)    

        #Scene 1 Ends
        self.wait(2)

        # Next scene
        self.clear()
        self.add(title, axes, labels)

        interval1 = Interval(1, 3) # [1, 3]
        f2_expr1 = 4/x
        interval2 = Interval(3, 4, left_open=True) #(3, 4]
        f2_expr2 = Rational(0.5)*(x-3)**2
        f2_expr = Piecewise(
            (f2_expr1, interval1.contains(x)), # Second condition needs to be a boolean
            (f2_expr2, interval2.contains(x))
        )
        f2_num = lambdify(x, f2_expr, 'numpy')
        curve2a = axes.plot(lambda x: f2_num(x), x_range=[1, 3], color=BLUE)
        curve2b = axes.plot(lambda x: f2_num(x), x_range=[3+1e-9, 4], color=BLUE)
        curve2 = VGroup(curve2a, curve2b)

        tracker.set_value(1)

        bad_line = DashedLine(axes.c2p(0, 1), axes.c2p(5, 1), color=RED)
        bad_line_label = MathTex(rf"y = 1", color=RED).next_to(axes.c2p(0, 1), LEFT)
        y2_dot = Dot(axes.c2p(tracker.get_value(), f2_num(tracker.get_value())), color=PURPLE)
        y2_dot.add_updater(lambda d: d.become(Dot(axes.c2p(tracker.get_value(), f2_num(tracker.get_value())), color=PURPLE)))
        y2_line = DashedLine(axes.c2p(0, f2_num(tracker.get_value())), y2_dot.get_center(), color=PURPLE)
        y2_line.add_updater(lambda l: l.become(DashedLine(axes.c2p(0, f2_num(tracker.get_value())), y2_dot.get_center(), color=PURPLE)))
        y2_label1 = MathTex(rf"n = ")
        y2_label2 = DecimalNumber(f2_num(tracker.get_value())).next_to(y2_label1, RIGHT)
        y2_labelg = VGroup(y2_label1, y2_label2).arrange(RIGHT)
        y2_labelg.add_updater(
            lambda g: g.become(
                VGroup(
                    MathTex(rf"n = "),
                    DecimalNumber(f2_num(tracker.get_value()))
                ).arrange(RIGHT).next_to(axes.c2p(0, f2_num(tracker.get_value())), LEFT)
            )
        )

        self.play(Create(curve2), run_time=2)

        f2_label = MathTex(\
            r"""
            g(x) = \begin{cases}
                \quad \frac{4}{x} &\text{ for } 1 \leq x \leq 3 \\
                \frac{(x-3)^2}{2} &\text{ for } 3 < x \leq 4
            \end{cases}""", color=BLUE).next_to(title, DOWN).align_to(title, LEFT)
        
        self.play(FadeIn(f2_label))
        self.wait(0.5)

        IVT4 = MathTex(r"\text{Since } g \text{ is }", r"\text{not}", r"\text{ continuous},").next_to(f2_label, 1.5*DOWN).align_to(title, LEFT)
        IVT4[1].set_color(RED)
        IVT5 = MathTex(r"\text{for } 1 \in [f(1), f(4)],").next_to(IVT4, 1.5*DOWN).align_to(title, LEFT)
        IVT6 = MathTex(r"\text{there's no } c \in [1, 4] \text{ with } f(c)=1").next_to(IVT5, 1.5*DOWN).align_to(title, LEFT)

        self.play(Write(IVT4), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(y2_labelg, y2_line, y2_dot))
        self.wait(0.5)

        self.play(Write(IVT5), run_time=1)
        self.wait(0.5)
        self.play(
            AnimationGroup(
                *(Indicate(m) for m in [IVT5, y2_labelg])
            )
        )
        self.wait(0.5)

        self.play(Create(bad_line), Write(bad_line_label))
        self.wait(0.5)

        self.play(tracker.animate.set_value(3), run_time=2)
        tracker.set_value(3+1e-9)
        self.play(tracker.animate.set_value(4), run_time=1)

        self.play(Write(IVT6), run_time=1)
        self.wait(0.5)
        self.play(Indicate(IVT6))

        self.play(tracker.animate.set_value(3+1e-9), run_time=1)
        tracker.set_value(3)
        self.play(tracker.animate.set_value(4/3), run_time=1)

        self.wait(3)

