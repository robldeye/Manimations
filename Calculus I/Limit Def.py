from manim import *
import numpy as np
from sympy import symbols, Eq, solve, sqrt, lambdify, latex, nsimplify

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
        x, y = symbols('x y') #for sympy operations
        f_expr = x**2
        f_num = lambdify(x, f_expr, 'numpy')
        inv_funcs = solve(Eq(y, f_expr), x)  # [-sqrt(y), sqrt(y)]
        g_y = inv_funcs[1] # Grabs sqrt(y)

        f_label = MathTex(r"f(x) = x^2", color=BLUE).to_corner(UR)

        curve = axes.plot(lambda x: f_num(x), x_range=[0, 2], color=BLUE)
        epsilon = ValueTracker(0.5*(L))

        # Function to build dynamic area region since get_area only works for integration wrt x
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

        epsilon_label = MathTex(rf"\epsilon = {epsilon.get_value():.2f}").to_edge(LEFT).align_to(title, LEFT)
        epsilon_label.add_updater(lambda l: l.become(MathTex(rf"\epsilon = {epsilon.get_value():.2f}").to_edge(LEFT).align_to(title, LEFT)))
        epsilon_u = always_redraw(lambda: MathTex(rf"L + \epsilon").next_to(axes.c2p(0, L+epsilon.get_value()), LEFT))
        epsilon_d = always_redraw(lambda: MathTex(rf"L - \epsilon").next_to(axes.c2p(0, L-epsilon.get_value()), LEFT))
        L_label = MathTex(rf"L").next_to(axes.c2p(0, L), LEFT)

        x_poly = always_redraw(
            lambda: axes.get_area(
                curve,
                x_range=[float(sqrt(L-epsilon.get_value())), float(sqrt(L+epsilon.get_value()))],
                color=GREEN
            )
        )

        delta_label = MathTex(rf"\delta = {float(sqrt(epsilon.get_value())):.2f}").next_to(epsilon_label, DOWN).align_to(title, LEFT)
        delta_label.add_updater(lambda l: l.become(MathTex(rf"\delta = {float(sqrt(epsilon.get_value())):.2f}").next_to(epsilon_label, DOWN).align_to(title, LEFT)))
        delta_r = always_redraw(lambda: MathTex(rf"a + \delta").next_to(axes.c2p(float(sqrt(L+epsilon.get_value())), 0), 2*DOWN))
        delta_l = always_redraw(lambda: MathTex(rf"a - \delta").next_to(axes.c2p(float(sqrt(L-epsilon.get_value())), 0), 2*DOWN))
        a_label = MathTex(rf"a").next_to(axes.c2p(a, 0), DOWN)

        offset = 0.75 # defined so that |f(x)-L| = offset*\epsilon
        f_dot = Dot(axes.c2p(a+offset*epsilon.get_value(), f_num(a+offset*epsilon.get_value())))
        f_dot.add_updater(lambda d: d.become(Dot(axes.c2p(a+offset*epsilon.get_value(), f_num(a+offset*epsilon.get_value())))))
        f_line = DashedLine(f_dot.get_center(), axes.c2p(a+offset*epsilon.get_value()))
        f_line.add_updater()

        self.play(Write(title), run_time=1)
        self.play(title.animate.to_corner(UL))
        self.wait()

        self.play(FadeIn(axes, labels))
        self.wait()

        self.play(Create(curve))
        self.play(FadeIn(f_label))
        self.wait()

        limitdef_1 = MathTex(r"\text{Q) How do we formalize } f(x) \to L \text{ as } x \to a\text{ ?}").scale(0.6).next_to(title, DOWN).align_to(title, LEFT)

        limitdef_2a = MathTex(r"\text{A) Whenever } |f(x) - L| \text{ becomes small,}").scale(0.6).next_to(limitdef_1, 2*DOWN).align_to(title, LEFT)
        limitdef_2b = MathTex(r"\quad \text{We need } |x - a| \text{ to also become small.}").scale(0.6).next_to(limitdef_2a, DOWN).align_to(title, LEFT)

        limitdef_3a = MathTex(r"\text{A) For any } \epsilon \text{ so that } |f(x) - L| < \epsilon,").scale(0.6).next_to(limitdef_1, 2*DOWN).align_to(title, LEFT)
        limitdef_3b = MathTex(r"\quad \text{There is a } \delta \text{ so that } |x - a | < \delta.").scale(0.6).next_to(limitdef_3a, DOWN).align_to(title, LEFT)

        self.play(Write(limitdef_1), run_time=3)
        self.wait(2)

        self.play(FadeIn(y_poly))
        self.play(Write(limitdef_2a), run_time = 2)
        self.play(FadeIn(L_label))
        self.wait(1)
        self.play(epsilon.animate.set_value(0.1), run_time=2)
        self.wait(0.5)
        self.play(epsilon.animate.set_value(1), run_time=0.25)
        self.wait()

        self.play(FadeIn(x_poly))
        self.play(Write(limitdef_2b), run_time = 2)
        self.play(FadeIn(a_label))
        self.wait(1)
        self.play(epsilon.animate.set_value(0.1), run_time=2)
        self.wait(0.5)
        self.play(epsilon.animate.set_value(1), run_time=0.25)
        self.wait()

        self.play(Indicate(limitdef_2a))
        self.play(Transform(limitdef_2a, limitdef_3a))
        self.play(Indicate(limitdef_2b))
        self.play(Transform(limitdef_2b, limitdef_3b))
        self.wait(2)

        self.play(Write(epsilon_label), Write(epsilon_u), Write(epsilon_d))        
        self.play(Write(delta_label), Write(delta_r), Write(delta_l))
        self.wait(1)

        self.play(epsilon.animate.set_value(0.1), run_time=2)
        self.wait(0.5)
        self.play(epsilon.animate.set_value(1), run_time=0.25)
        

        self.wait(3)

