from manim import *
import numpy as np
from sympy import symbols, Eq, solve, sqrt, lambdify, Interval, Rational, Piecewise

class LimitDef(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            x_length=6, 
            y_length=6,
            axis_config={"include_tip": True}
        ).to_corner(UR)
        labels = axes.get_axis_labels("x", "y")

        title = MathTex(r"\text{The Definition of } \lim_{x \to a} f(x) = L")

        y_min = 1
        y_max = 3
        L = y_max-y_min
        a = float(sqrt(L))
        x, y = symbols('x y') # for sympy operations
        f_expr = x**2
        f_num = lambdify(x, f_expr, 'numpy')
        inv_funcs = solve(Eq(y, f_expr), x)  # [-sqrt(y), sqrt(y)]
        g_y = inv_funcs[1] # Grabs sqrt(y)

        f_label = MathTex(r"f(x) = x^2", color=BLUE).to_corner(UR)

        curve = axes.plot(lambda x: f_num(x), x_range=[0, 2], color=BLUE)
        epsilon = ValueTracker(0.5*(L))
        epsilon_target = ValueTracker((3/8)*(L))
        delta = ValueTracker(g_y.subs(y, epsilon.get_value()))
        # tracker = ValueTracker(float(sqrt(2.5)))

        # Function to build dynamic area region since get_area only works for integration w.r.t. x
        def y_polygon(eps: float) -> VMobject:
            y_vals = np.linspace(L-eps, L+eps, 300)
            curve_pts = [axes.c2p(float(g_y.subs(y, yv)), yv) for yv in y_vals]
            y_axis_pts = [axes.c2p(0.0, yv) for yv in y_vals]
            poly = Polygon(
                *y_axis_pts, *reversed(curve_pts),
                color=YELLOW, fill_opacity=0.55, stroke_width=0
            )
            return poly
        y_poly = always_redraw(lambda: y_polygon(epsilon.get_value()))

        epsilon_label = MathTex(rf"\epsilon = {epsilon_target.get_value():.2f}").to_edge(LEFT).align_to(title, LEFT)
        epsilon_label.add_updater(lambda l: l.become(MathTex(rf"\epsilon = {epsilon_target.get_value():.2f}").to_edge(LEFT).align_to(title, LEFT)))
        epsilon_u = always_redraw(lambda: MathTex(rf"L + \epsilon").next_to(axes.c2p(0, L+epsilon_target.get_value()), LEFT))
        epsilon_u_line = DashedLine(axes.c2p(0, L+epsilon_target.get_value()), axes.c2p(axes.x_range[1], L+epsilon_target.get_value()))
        epsilon_u_line.add_updater(lambda l: l.become(DashedLine(axes.c2p(0, L+epsilon_target.get_value()), axes.c2p(axes.x_range[1], L+epsilon_target.get_value()))))
        epsilon_d = always_redraw(lambda: MathTex(rf"L - \epsilon").next_to(axes.c2p(0, L-epsilon_target.get_value()), LEFT))
        epsilon_d_line = DashedLine(axes.c2p(0, L-epsilon_target.get_value()), axes.c2p(axes.x_range[1], L-epsilon_target.get_value()))
        epsilon_d_line.add_updater(lambda l: l.become(DashedLine(axes.c2p(0, L-epsilon_target.get_value()), axes.c2p(axes.x_range[1], L-epsilon_target.get_value()))))
        L_label = MathTex(rf"L").next_to(axes.c2p(0, L), LEFT)
        L_line = DashedLine(axes.c2p(0, L), axes.c2p(axes.x_range[1], L), color=YELLOW)

        x_poly = always_redraw(
            lambda: axes.get_area(
                curve,
                x_range=[float(sqrt(L-delta.get_value())), float(sqrt(L+delta.get_value()))],
                color=GREEN
            )
        )

        delta_label = MathTex(rf"\delta = {float(sqrt(delta.get_value())):.2f}").next_to(epsilon_label, DOWN).align_to(title, LEFT)
        delta_label.add_updater(lambda l: l.become(MathTex(rf"\delta = {float(sqrt(delta.get_value())):.2f}").next_to(epsilon_label, DOWN).align_to(title, LEFT)))
        delta_r = always_redraw(lambda: MathTex(rf"a + \delta").next_to(axes.c2p(float(sqrt(L+delta.get_value())), 0), 3*DOWN))
        delta_l = always_redraw(lambda: MathTex(rf"a - \delta").next_to(axes.c2p(float(sqrt(L-delta.get_value())), 0), 2*DOWN))
        a_label = MathTex(rf"a").next_to(axes.c2p(a, 0), DOWN)

        # x_dot = Dot(axes.c2p(tracker.get_value(), 0), color=GREEN)
        # x_dot.add_updater(lambda d: d.become(Dot(axes.c2p(tracker.get_value(), 0), color=GREEN)))
        # f_dot = Dot(axes.c2p(tracker.get_value(), f_num(tracker.get_value())), color=PURPLE)
        # f_dot.add_updater(lambda d: d.become(Dot(axes.c2p(tracker.get_value(), f_num(tracker.get_value())), color=PURPLE)))
        # x_line = DashedLine(x_dot.get_center(), f_dot.get_center(), color=GREEN)
        # x_line.add_updater(lambda d: d.become(DashedLine(x_dot.get_center(), f_dot.get_center(), color=GREEN)))
        # f_line = DashedLine(f_dot.get_center(), axes.c2p(0, f_num(tracker.get_value())), color=PURPLE)
        # f_line.add_updater(lambda l: l.become(DashedLine(f_dot.get_center(), axes.c2p(0, f_num(tracker.get_value())), color=PURPLE)))
        # f_data = VGroup(x_dot, f_dot, x_line, f_line)

        self.play(Write(title), run_time=1)
        self.play(title.animate.to_corner(UL))
        self.wait()

        self.play(FadeIn(axes, labels))
        self.wait()

        self.play(Create(curve))
        self.play(FadeIn(f_label))
        self.wait()

        # self.play(FadeIn(f_data))

        limitdef_1 = MathTex(r"\text{Q) How do we formalize }", r"f(x) \to L", r"\text{ as }",  r"x \to a", r"\text{ ?}").scale(0.6).next_to(title, DOWN).align_to(title, LEFT)

        limitdef_2a = MathTex(r"\text{A) As the distance } 0 < |x - a| \text{ becomes small,}").scale(0.6).next_to(limitdef_1, 2*DOWN).align_to(title, LEFT)
        limitdef_2b = MathTex(r"\text{the distance } |f(x) - L| \text{ should also get small.}").scale(0.6).next_to(limitdef_2a, DOWN).align_to(title, LEFT)
        limitdef_2g = VGroup(limitdef_2a, limitdef_2b)

        limitdef_2a_int = MathTex(r"\text{A) As the distance }", r"0 < |x - a| < \delta", r",").scale(0.6).next_to(limitdef_1, 2*DOWN).align_to(title, LEFT)
        limitdef_2b_int = MathTex(r"\text{we have the distance }", r"|f(x) - L| < \epsilon").scale(0.6).next_to(limitdef_2a, DOWN).align_to(title, LEFT)
        limitdef_2g_int = VGroup(limitdef_2a_int, limitdef_2b_int)

        limitdef_3a = MathTex(r"\text{A) For any }",  r"\epsilon > 0", r"\text{ we can find a }", r"\delta > 0}").scale(0.6).next_to(limitdef_1, 2*DOWN).align_to(title, LEFT)
        limitdef_3b = MathTex(r"\quad \text{so that whenever }", r"0 < |x - a| < \delta", r",").scale(0.6).next_to(limitdef_3a, DOWN).align_to(title, LEFT)
        limitdef_3b[1].set_color(GREEN)
        limitdef_3c = MathTex(r"\quad \text{we have }", r"|f(x) - L| < \epsilon", r".").scale(0.6).next_to(limitdef_3b, DOWN).align_to(title, LEFT)
        limitdef_3c[1].set_color(YELLOW)
        limitdef_3g = VGroup(limitdef_3a, limitdef_3b, limitdef_3c)

        good_limit = MathTex(r"\lim_{x \to a} f(x) = L").next_to(delta_label, 2*DOWN).align_to(title, LEFT)

        self.play(Write(limitdef_1), run_time=2)
        self.wait(2)

        self.play(FadeIn(x_poly))
        self.wait(0.5)
        self.play(Indicate(limitdef_1[3]))
        self.wait(0.5)
        self.play(Write(limitdef_2a), run_time = 2)
        self.wait(1)
        self.play(FadeIn(a_label))
        self.wait(0.5)
        self.play(delta.animate.set_value(0.25), run_time=2)
        self.wait(0.5)

        self.play(FadeIn(y_poly))
        self.wait(0.5)
        self.play(Indicate(limitdef_1[1]))
        self.wait(0.5)
        self.play(Write(limitdef_2b), run_time = 2)
        self.wait(1)
        self.play(FadeIn(L_label, L_line))
        self.wait(0.5)
        self.play(epsilon.animate.set_value(0.25), run_time=2)
        self.wait(0.5)

        self.play(
            delta.animate.set_value(1),
            epsilon.animate.set_value(1)
        )
        self.wait(0.5)

        self.play(Indicate(limitdef_2g))
        self.wait(0.5)
        self.play(
            AnimationGroup(
                ReplacementTransform(limitdef_2g[0], limitdef_2g_int[0]),
                ReplacementTransform(limitdef_2g[1], limitdef_2g_int[1]),
                lag_ratio=1
            )
        )
        self.wait(4)

        self.play(Write(epsilon_label), Write(epsilon_u), Write(epsilon_d), Create(epsilon_u_line), Create(epsilon_d_line))
        self.play(
            AnimationGroup(
                *(Indicate(m) for m in [limitdef_2b_int[1], epsilon_u, epsilon_d])
            )
        )
        self.wait(0.5)      
        self.play(Write(delta_label), Write(delta_r), Write(delta_l))
        self.play(
            AnimationGroup(
                *(Indicate(m) for m in [limitdef_2a_int[1], delta_l, delta_r])
            )
        )
        self.wait(0.5)

        for i in [1/2, 3/8, 1/4]:
            self.play(epsilon_target.animate.set_value(i), run_time=2)
            self.wait(0.5)
            self.play(
                AnimationGroup(
                    *(t.animate.set_value(i) for t in [delta, epsilon]),
                    lag_ratio=0.75,
                    run_time=1
                )
            )
        self.wait()

        self.play(ReplacementTransform(limitdef_2g_int, limitdef_3g))
        self.wait(6)

        for i in [1/5, 1/10, 1/100]:
            self.play(epsilon_target.animate.set_value(i), run_time=2)
            self.wait(0.5)
            self.play(
                AnimationGroup(
                    *(t.animate.set_value(i) for t in [delta, epsilon]),
                    lag_ratio=0.75,
                    run_time=1
                )
            )
        self.wait()

        self.play(FadeOut(epsilon_u, epsilon_d, delta_l, delta_r))
        self.wait(0.5)

        self.play(Write(good_limit))
        self.wait(3)
        
        # New Scene
        self.clear()

        title2 = MathTex(r"\underline{\text{Limit Failure}}")
        self.play(Write(title2))
        self.wait(0.5)
        self.play(title2.animate.to_corner(UL))
        self.wait(0.5)

        self.play(FadeIn(axes, labels))

        interval1 = Interval(1, 2) # [1, 2]
        f2_expr1 = 1 + 2/x
        interval2 = Interval(2, 4, left_open=True) #(2, 4]
        f2_expr2 = 1 - Rational(0.5)*(x-2)**2
        f2_expr = Piecewise(
            (f2_expr1, interval1.contains(x)), # Second condition needs to be a boolean
            (f2_expr2, interval2.contains(x))
        )
        f2_num = lambdify(x, f2_expr, 'numpy')
        curve2a = axes.plot(lambda x: f2_num(x), x_range=[1, 2], color=BLUE)
        curve2b = axes.plot(lambda x: f2_num(x), x_range=[2+1e-9, 4], color=BLUE)
        curve2 = VGroup(curve2a, curve2b)

        f2_label = MathTex(\
            r"""
            g(x) = \begin{cases}
                \quad 1+ \frac{2}{x} &\text{ for } 1 \leq x \leq 2 \\
                1 + \frac{(x-2)^2}{2} &\text{ for } 2 < x \leq 4
            \end{cases}""", color=BLUE).scale(0.75).next_to(title2, DOWN).align_to(title2, LEFT)
        
        bad_L = 1.5
        bad_epsilon_target = ValueTracker(0.4)
        bad_x = ValueTracker(4)
        
        self.play(Create(curve2))
        self.wait(0.5)
        self.play(Write(f2_label))
        self.wait(0.5)

        bad_L_label = MathTex(rf"L = 1.5", color=RED).next_to(axes.c2p(0, 1.5), LEFT)
        bad_L_line = DashedLine(axes.c2p(0, 1.5), axes.c2p(4, 1.5), color=RED)

        bad_epsilon_label = MathTex(rf"\epsilon = {bad_epsilon_target.get_value():.2f}").to_edge(LEFT).align_to(title2, LEFT)
        bad_epsilon_label.add_updater(lambda l: l.become(MathTex(rf"\epsilon = {bad_epsilon_target.get_value():.2f}").to_edge(LEFT).align_to(title2, LEFT)))
        bad_epsilon_u_line = DashedLine(axes.c2p(0, bad_L+bad_epsilon_target.get_value()), axes.c2p(axes.x_range[1], bad_L+bad_epsilon_target.get_value()))
        bad_epsilon_u_line.add_updater(lambda l: l.become(DashedLine(axes.c2p(0, bad_L+bad_epsilon_target.get_value()), axes.c2p(axes.x_range[1], bad_L+bad_epsilon_target.get_value()))))
        bad_epsilon_d_line = DashedLine(axes.c2p(0, bad_L-bad_epsilon_target.get_value()), axes.c2p(axes.x_range[1], bad_L-bad_epsilon_target.get_value()))
        bad_epsilon_d_line.add_updater(lambda l: l.become(DashedLine(axes.c2p(0, bad_L-bad_epsilon_target.get_value()), axes.c2p(axes.x_range[1], bad_L-bad_epsilon_target.get_value()))))


        x2_dot = Dot(axes.c2p(bad_x.get_value(), 0), color=GREEN)
        x2_dot.add_updater(lambda d: d.become(Dot(axes.c2p(bad_x.get_value(), 0), color=GREEN)))
        y2_dot = Dot(axes.c2p(bad_x.get_value(), f2_num(bad_x.get_value())), color=PURPLE)
        y2_dot.add_updater(lambda d: d.become(Dot(axes.c2p(bad_x.get_value(), f2_num(bad_x.get_value())), color=PURPLE)))
        y2_line = DashedLine(axes.c2p(0, f2_num(bad_x.get_value())), y2_dot.get_center(), color=PURPLE)
        y2_line.add_updater(lambda l: l.become(DashedLine(axes.c2p(0, f2_num(bad_x.get_value())), y2_dot.get_center(), color=PURPLE)))

        self.play(
            Create(bad_L_line),
            Write(bad_L_label),
            Write(bad_epsilon_label)
        )
        self.wait(0.5)

        self.play(FadeIn(bad_epsilon_u_line, bad_epsilon_d_line))
        self.wait(0.5)
        self.play(bad_epsilon_target.animate.set_value(0.25), run_time=2)

        bad_delta_label1 = MathTex(r"\text{For } \epsilon = 0.25, \text{ there is no}").next_to(bad_epsilon_label, 2*DOWN).align_to(title2, LEFT)
        bad_delta_label2 = MathTex(r"\delta > 0 \text{ so that } 0 < |x - 2| < \delta").next_to(bad_delta_label1, DOWN).align_to(title2, LEFT)
        bad_delta_label3 = MathTex(r"\text{will force } |g(x) - 1.5| < 0.25").next_to(bad_delta_label2, DOWN).align_to(title2, LEFT)
        bad_delta_labelg = VGroup(bad_delta_label1, bad_delta_label2, bad_delta_label3)
        bad_delta_labelf = MathTex(r"\lim_{x \to 2} g(x) \neq 1.5").next_to(bad_epsilon_label, 2*DOWN).align_to(title2, LEFT)

        self.play(
            AnimationGroup(
                *(Write(l) for l in bad_delta_labelg),
                lag_ratio=1
            )
        )
        self.wait(0.5)
        self.play(FadeIn(x2_dot, y2_dot, y2_line))
        self.wait(0.5)
        self.play(bad_x.animate.set_value(2+1e-9), run_time=2)
        bad_x.set_value(2)
        self.play(bad_x.animate.set_value(1), run_time=1)
        self.wait(0.5)
        self.play(bad_x.animate.set_value(2), run_time=1)
        bad_x.set_value(2+1e-9)
        self.play(bad_x.animate.set_value(4), run_time=2)
        self.play(FadeOut(x2_dot, y2_dot, y2_line))
        self.play(ReplacementTransform(bad_delta_labelg, bad_delta_labelf))
        self.wait(3)

