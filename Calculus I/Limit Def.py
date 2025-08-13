from manim import *
import numpy as np
from sympy import symbols, Eq, solve, sqrt

class LimitDef(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            x_length=8, 
            y_length=8,
            axis_config={"include_tip": True}
        ).to_edge(RIGHT)
        labels = axes.get_axis_labels("x", "y")

        y_min = 1
        y_max = 3
        x, y = symbols('x y') #for sympy operations
        f_expr = x**2
        inv_funcs = solve(Eq(y, f_expr), x)  # [-sqrt(y), sqrt(y)]
        g_y = inv_funcs[1] # Grabs sqrt(y)

        curve = axes.plot(lambda x: x**2, x_range=[0, float(sqrt(y_max))], color=YELLOW)
        epsilon = ValueTracker(0.5*(y_max-y_min))

        # Function to build dynamic area region since get_area only works for integration wrt x
        def y_polygon(eps: float) -> VMobject:
            y_vals = np.linspace((y_max-y_min)-eps, (y_max-y_min)+eps, 300)
            curve_pts = [axes.c2p(float(g_y.subs(y, yv)), yv) for yv in y_vals]
            y_axis_pts = [axes.c2p(0.0, yv) for yv in y_vals]
            poly = Polygon(
                *y_axis_pts, *reversed(curve_pts),
                color=BLUE, fill_opacity=0.55, stroke_width=0
            )
            return poly
        area_poly = always_redraw(lambda: y_polygon(epsilon.get_value()))

        title = MathTex(r"\text{The Definition of } \displaystyle \limits\lim_{x \to a} f(x)")

        self.play(Create(axes), Write(labels))
        self.play(Create(curve))
        self.play(FadeIn(area_poly))
        self.wait(1)

        self.play(epsilon.animate.set_value(0.1), run_time=2)
        self.wait(0.5)
        self.play(epsilon.animate.set_value(1), run_time=2)
        self.wait(2)

