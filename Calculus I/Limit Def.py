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
        x, y = symbols('x y') #for sympy operations
        f_expr = x**2
        f_num = lambdify(x, f_expr, 'numpy')
        inv_funcs = solve(Eq(y, f_expr), x)  # [-sqrt(y), sqrt(y)]
        g_y = inv_funcs[1] # Grabs sqrt(y)

        curve = axes.plot(lambda x: f_num(x), x_range=[0, float(sqrt(y_max))], color=YELLOW)
        epsilon = ValueTracker(0.5*(L))

        # Function to build dynamic area region since get_area only works for integration wrt x
        def y_polygon(eps: float) -> VMobject:
            y_vals = np.linspace(L-eps, L+eps, 300)
            curve_pts = [axes.c2p(float(g_y.subs(y, yv)), yv) for yv in y_vals]
            y_axis_pts = [axes.c2p(0.0, yv) for yv in y_vals]
            poly = Polygon(
                *y_axis_pts, *reversed(curve_pts),
                color=BLUE, fill_opacity=0.55, stroke_width=0
            )
            return poly
        y_poly = always_redraw(lambda: y_polygon(epsilon.get_value()))
        epsilon_label = always_redraw(lambda: MathTex(rf"\epsilon = {epsilon.get_value():.2f}").to_edge(LEFT).align_to(title, LEFT))
        epsilon_u = always_redraw(lambda: MathTex(rf"{L} + \epsilon").next_to(axes.c2p(0, L+epsilon.get_value()), LEFT))
        epsilon_d = always_redraw(lambda: MathTex(rf"{L} - \epsilon").next_to(axes.c2p(0, L-epsilon.get_value()), LEFT))

        x_poly = always_redraw(
            lambda: axes.get_area(
                curve,
                x_range=[float(sqrt(L-epsilon.get_value())), float(sqrt(L+epsilon.get_value()))],
                color=GREEN
            )
        )

        delta_label = always_redraw(lambda: MathTex(rf"\delta = {float(sqrt(epsilon.get_value())):.2f}").next_to(epsilon_label, DOWN).align_to(title, LEFT))
        delta_r = always_redraw(lambda: MathTex(rf"{latex(nsimplify(L))} + \delta").next_to(axes.c2p(float(sqrt(L+epsilon.get_value())), 0), DOWN))
        delta_l = always_redraw(lambda: MathTex(rf"{latex(nsimplify(L))} - \delta").next_to(axes.c2p(float(sqrt(L-epsilon.get_value())), 0), DOWN, buff=1))

        self.play(Write(title), run_time=1)
        self.play(title.animate.to_corner(UL))
        self.wait()

        self.play(Create(axes), Write(labels))
        self.wait()

        self.play(Create(curve))
        self.wait()

        limitdef_1 = MathTex(r"\text{Q) How do we formalize } f(x) \to L \text{ as } x \to a\text{ ?}").scale(0.6).next_to(title, DOWN).align_to(title, LEFT)
        limitdef_2 = MathTex(r"\text{We need two things}:").scale(0.6).next_to(limitdef_1, DOWN).align_to(title, LEFT)
        limitdef_3 = MathTex(r"1) \text{Whenever the distance } |f(x) - L| \text{ decreases...}").scale(0.6).next_to(limitdef_2, DOWN).align_to(title, LEFT)
        limitdef_4 = MathTex(r"2) \text{We want to be sure the distance} |x - a| \text{ also decreases.}").scale(0.6).next_to(limitdef_3, DOWN).align_to(title, LEFT)

        self.play(Write(limitdef_1), run_time=1)
        self.wait(2)
        self.play(Write(limitdef_2), run_time=1)

        self.play(FadeIn(y_poly))
        self.play(Write(epsilon_label), Write(epsilon_u), Write(epsilon_d), run_time=1)
        self.play(Write(limitdef_3), run_time=1)
        self.wait()

        self.play(epsilon.animate.set_value(0.1), run_time=2)
        self.wait()
        self.play(epsilon.animate.set_value(1), run_time=2)
        self.wait()

        # insert limit def text at this stage
        
        self.play(Write(limitdef_4), run_time=1)
        self.wait()
        self.play(FadeIn(x_poly))
        self.play(Write(delta_label), Write(delta_r), Write(delta_l), run_time=1)
        self.wait()

        self.play(epsilon.animate.set_value(0.1), run_time=2)
        self.wait()
        self.play(epsilon.animate.set_value(1), run_time=2)
        self.wait()

