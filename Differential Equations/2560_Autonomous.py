from manim import *
import numpy as np
from sympy import Matrix, Rational, latex
from scipy.integrate import odeint
from scipy.interpolate import interp1d
import math

class autonomous(Scene):
    def construct(self):
        # Grid
        locations = []
        grid_scale = 0.95
        y_radius = 4
        t_radius = y_radius
        grid = Axes(
            x_range=(0, t_radius, 1),
            y_range=(-y_radius, y_radius, 1),
            x_length=9,
            y_length=9,
            tips=True,
            axis_config={"include_numbers": False}
        ).to_edge(RIGHT).scale(grid_scale)
        grid.get_axis_labels(x_label="t", y_label="y")

        step = 0.5 #granularity of direction field
        for x in np.arange(0, 2*y_radius + step, step):
            for y in np.arange(-y_radius, y_radius + step, step):
                locations.append([x, y])

        titlep1 = MathTex(r"\text{Solutions to Autonomous}").scale(0.85).to_corner(UL)
        titlep2 = MathTex(r"\text{Differential Equation}").scale(0.85).next_to(titlep1, DOWN).align_to(titlep1, LEFT)
        titlep3 = MathTex(r"\text{Equilibrium Solutions \& Stability}").scale(0.75).to_corner(UL)

        # define ODE
        np.random.seed(42)
        # num_zeroes = 3
        # zeroes = np.random.uniform(-y_radius, y_radius, num_zeroes)
        zeroes = [-2, 0, 3] # please select integers to make constant solution finding below work
        rate = Rational(1, 50)
        def model(y, t):
            return float(rate)*math.prod((y - zero) for zero in zeroes)

        model_label = VGroup()
        model_label_strings = []
        model_label_p1 = MathTex(
            rf"\frac{{dy}}{{dt}} = {latex(rate)}"
        ).scale(0.75).next_to(titlep2, DOWN).align_to(titlep2, LEFT)
        model_label.add(model_label_p1)
        for zero in zeroes:
            # wrap negative values in parentheses
            if float(zero) < 0:
                string = rf"(y-({zero}))"
            else:
                string = rf"(y-{zero})"
            model_label_strings.append(string)
        model_label_expression = "".join(model_label_strings)
        model_label_p2 = MathTex(
            model_label_expression
        ).scale(0.75).next_to(model_label_p1, RIGHT)
        model_label.add(model_label_p2)

        # solving ODE for multiple solution paths
        tracker = ValueTracker(0)
        num_solutions = 8
        initial_values = np.random.uniform(-y_radius, y_radius, num_solutions)
        t = np.linspace(0, t_radius + 1, 1000) # smoothness of curve later on tied to framerate in manim.cfg, not step size

        def make_solution_dot(interpolated_solution, solution_color):
            return always_redraw(
                lambda: Dot(
                    point=grid.c2p(tracker.get_value(), *interpolated_solution(tracker.get_value())),
                    color=solution_color
                )
            )
        def make_solution_label(solution_dot, solution_color, index):
            return always_redraw(
                lambda: MathTex(
                    rf"y_{{{index+1}}}(t)",
                    color=solution_color
                ).next_to(solution_dot, UP)
            )
        colors = color_gradient([RED, BLUE], num_solutions)

        interpolated_solutions = []
        solution_dots = VGroup()
        solution_labels = VGroup()
        solution_paths = VGroup()

        for i, vec in enumerate(initial_values):
            solution_color = colors[i]
            solution = odeint(model, vec, t)
            interpolated_solution = interp1d(t, solution, axis=0, kind='linear')
            interpolated_solutions.append(interpolated_solution)

            solution_dot = make_solution_dot(interpolated_solution, solution_color)
            solution_dot.z_index=1 # to place dot above (in front of) trailing path
            solution_dots.add(solution_dot)

            solution_label = make_solution_label(solution_dot, solution_color, i)
            solution_label.z_index=1
            solution_labels.add(solution_label)

            solution_path = TracedPath(solution_dot.get_center, stroke_color=solution_color)
            solution_paths.add(solution_path)

        # some functions for making direction field arrows
        def model_field(x, y): #duplicate because argument ordering sucks apparently
            return float(rate)*math.prod((y - zero) for zero in zeroes)
        
        def dir(t, y):
            return np.array([1, model_field(t, y)])
        
        def unit(v):
            if np.linalg.norm(v) != 0:
                return v/np.linalg.norm(v)
            else:
                return v
            
        def potency(v):
            if np.linalg.norm(v) != 0:
                return np.linalg.norm(dir(*v))/np.linalg.norm(v)
            else:
                return v

        # vector_field = ArrowVectorField(
        #     lambda p: unit(dir(*p[:2])), #slice just (x, y) from (x, y, 0).
        #     x_range = [0, t_radius, step],
        #     y_range = [-y_radius, y_radius, step],
        #     vector_config={"stroke_width": 2, "max_tip_length_to_length_ratio": 0.3}
        # ).scale(grid_scale).move_to(grid)

        scale = 0.4*step
        arrows = VGroup(
            Arrow(
                start = grid.c2p(*(np.array(loc)) - scale * unit(dir(*loc))),
                end = grid.c2p(*(np.array(loc) + scale * unit(dir(*loc)))),
            )
            for loc in locations
        )

        constant_solutions = []
        for y in np.arange(-y_radius, y_radius+step):
            if model(y, 0) == 0:
                constant_solutions.append(y)

        constant_solution_lines = VGroup()
        constant_solution_labels = VGroup()
        for y in constant_solutions:
            line = Line(
                start = grid.c2p(0, y),
                end = grid.c2p(t_radius+1, y),
                color = PURPLE,
                stroke_width=5
            )
            constant_solution_lines.add(line)
            label = MathTex(
                rf"y = {y}",
                color = PURPLE
            ).scale(0.75).next_to(grid.c2p(0, y), LEFT, buff=0.75)
            constant_solution_labels.add(label)

        stable_labels = VGroup()
        unstable_labels = VGroup()
        semistable_labels = VGroup()
        eps = 0.01
        # constant solutions and stability type labels headache
        for i, (y, label) in enumerate(zip(constant_solutions, constant_solution_labels)):
            if i == 0:
                if model(y+eps, 0) < 0 and model(y-eps, 0) > 0:
                    stable_label = MathTex(
                        rf"\lim_{{t \rightarrow \infty}}y(t) = {y} \,\, \text{{if}} \,\, y(0) \in (-\infty, {float(constant_solutions[i+1]):.0f})"
                    ).scale(0.75).next_to(label, DOWN).align_to(label, RIGHT)
                    type_label = MathTex(
                        r"\text{Stable}",
                        color=GREEN
                    ).scale(0.75).next_to(label, LEFT)
                    stable_labels.add(stable_label)
                    stable_labels.add(type_label)
                elif model(y+eps, 0) < 0 and model(y-eps, 0) < 0:
                    semistable_label = MathTex(
                        rf"\lim_{{t \rightarrow \infty}}y(t) = {y} \,\, \text{{if}} \,\, y(0) \in (-\infty, {float(constant_solutions[i+1]):.0f})"
                    ).scale(0.75).next_to(label, DOWN).align_to(label, RIGHT)
                    type_label = MathTex(
                        r"\text{Semistable}",
                        color=YELLOW
                    ).scale(0.75).next_to(label, LEFT)
                    semistable_labels.add(semistable_label)
                    semistable_labels.add(type_label)
                elif model(y+eps, 0) > 0 and model(y-eps, 0) > 0:
                    semistable_label = MathTex(
                        rf"\lim_{{t \rightarrow \infty}}y(t) = {y} \,\, \text{{if}} \,\, y(0) = {y}"
                    ).scale(0.75).next_to(label, DOWN).align_to(label, RIGHT)
                    type_label = MathTex(
                        r"\text{Semistable}",
                        color=YELLOW
                    ).scale(0.75).next_to(label, LEFT)
                    semistable_labels.add(semistable_label)
                    semistable_labels.add(type_label)
                elif model(y+eps, 0) > 0 and model(y-eps, 0) < 0:
                    unstable_label = MathTex(
                        rf"\lim_{{t \rightarrow \infty}}y(t) = {y} \,\, \text{{if}} \,\, y(0) = {y}"
                    ).scale(0.75).next_to(label, DOWN).align_to(label, RIGHT)
                    type_label = MathTex(
                        r"\text{Unstable}",
                        color=RED
                    ).scale(0.75).next_to(label, LEFT)
                    unstable_labels.add(unstable_label)
                    unstable_labels.add(type_label)
            elif 0 < i < len(constant_solutions) - 1:
                if model(y+eps, 0) < 0 and model(y-eps, 0) > 0:
                    stable_label = MathTex(
                        rf"\lim_{{t \rightarrow \infty}}y(t) = {y} \,\, \text{{if}} \,\, y(0) \in ({float(constant_solutions[i-1]):.0f}, {float(constant_solutions[i+1]):.0f})"
                    ).scale(0.75).next_to(label, DOWN).align_to(label, RIGHT)
                    type_label = MathTex(
                        r"\text{Stable}",
                        color=GREEN
                    ).scale(0.75).next_to(label, LEFT)
                    stable_labels.add(stable_label)
                    stable_labels.add(type_label)
                elif model(y+eps, 0) < 0 and model(y-eps, 0) < 0:
                    semistable_label = MathTex(
                        rf"\lim_{{t \rightarrow \infty}}y(t) = {y} \,\, \text{{if}} \,\, y(0) \in [{y}, {float(constant_solutions[i+1]):.0f})"
                    ).scale(0.75).next_to(label, DOWN).align_to(label, RIGHT)
                    type_label = MathTex(
                        r"\text{Semistable}",
                        color=YELLOW
                    ).scale(0.75).next_to(label, LEFT)
                    semistable_labels.add(semistable_label)
                    semistable_labels.add(type_label)
                elif model(y+eps, 0) > 0 and model(y-eps, 0) > 0:
                    semistable_label = MathTex(
                        rf"\lim_{{t \rightarrow \infty}}y(t) = {y} \,\, \text{{if}} \,\, y(0) \in ({float(constant_solutions[i-1]):.0f}, {y}]"
                    ).scale(0.75).next_to(label, DOWN).align_to(label, RIGHT)
                    type_label = MathTex(
                        r"\text{Semistable}",
                        color=YELLOW
                    ).scale(0.75).next_to(label, LEFT)
                    semistable_labels.add(semistable_label)
                    semistable_labels.add(type_label)
                elif model(y+eps, 0) > 0 and model(y-eps, 0) < 0:
                    unstable_label = MathTex(
                        rf"\lim_{{t \rightarrow \infty}}y(t) = {y} \,\, \text{{if}} \,\, y(0) = {y}"
                    ).scale(0.75).next_to(label, DOWN).align_to(label, RIGHT)
                    type_label = MathTex(
                        r"\text{Unstable}",
                        color=RED
                    ).scale(0.75).next_to(label, LEFT)
                    unstable_labels.add(unstable_label)
                    unstable_labels.add(type_label)
            else:
                if model(y+eps, 0) < 0 and model(y-eps, 0) > 0:
                    stable_label = MathTex(
                        rf"\lim_{{t \rightarrow \infty}}y(t) = {y} \,\, \text{{if}} \,\, y(0) \in ({float(constant_solutions[i-1]):.0f}, \infty)"
                    ).scale(0.75).next_to(label, DOWN).align_to(label, RIGHT)
                    type_label = MathTex(
                        r"\text{Stable}",
                        color=GREEN
                    ).scale(0.75).next_to(label, LEFT)
                    stable_labels.add(stable_label)
                    stable_labels.add(type_label)
                elif model(y+eps, 0) < 0 and model(y-eps, 0) < 0:
                    semistable_label = MathTex(
                        rf"\lim_{{t \rightarrow \infty}}y(t) = {y} \,\, \text{{if}} \,\, y(0) \in [{y}, \infty)"
                    ).scale(0.75).next_to(label, DOWN).align_to(label, RIGHT)
                    type_label = MathTex(
                        r"\text{Semistable}",
                        color=YELLOW
                    ).scale(0.75).next_to(label, LEFT)
                    semistable_labels.add(semistable_label)
                    semistable_labels.add(type_label)
                elif model(y+eps, 0) > 0 and model(y-eps, 0) > 0:
                    semistable_label = MathTex(
                        rf"\lim_{{t \rightarrow \infty}}y(t) = {y} \,\, \text{{if}} \,\, y(0) \in ({float(constant_solutions[i-1]):.0f}, {y}]"
                    ).scale(0.75).next_to(label, DOWN).align_to(label, RIGHT)
                    type_label = MathTex(
                        r"\text{Semistable}",
                        color=YELLOW
                    ).scale(0.75).next_to(label, LEFT)
                    semistable_labels.add(semistable_label)
                    semistable_labels.add(type_label)
                elif model(y+eps, 0) > 0 and model(y-eps, 0) < 0:
                    unstable_label = MathTex(
                        rf"\lim_{{t \rightarrow \infty}}y(t) = {y} \,\, \text{{if}} \,\, y(0) = {y}"
                    ).scale(0.75).next_to(label, DOWN).align_to(label, RIGHT)
                    type_label = MathTex(
                        r"\text{Unstable}",
                        color=RED
                    ).scale(0.75).next_to(label, LEFT)
                    unstable_labels.add(unstable_label)
                    unstable_labels.add(type_label)
        limit_labels = VGroup()
        limit_labels.add(*stable_labels)
        limit_labels.add(*semistable_labels)
        limit_labels.add(*unstable_labels)

        # start scene
        self.play(
            Write(titlep1),
            Write(titlep2),
            FadeIn(grid)
        )
        self.play(Write(grid.get_axis_labels(x_label="t", y_label="y")))
        self.wait()

        # add system
        labels = VGroup(model_label)
        self.play(
            LaggedStart(*(Write(label) for label in labels), lag_ratio=0.5)
        )
        self.wait()
        
        # add all arrows
        self.play(
            AnimationGroup(
                (
                    GrowFromCenter(arrow.set_opacity(0.75))
                    for arrow in arrows
                ),
                lag_ratio=0.001,
            )
        )
        # self.play(
        #     FadeIn(vector_field)
        # )
        self.wait(2)

        # reset tracker to show multiple possible solutions
        tracker.set_value(0.0001)
        for dot, path, label in zip(solution_dots, solution_paths, solution_labels):
            self.play(
                LaggedStart(
                    Create(dot),
                    Create(path),
                    Write(label),
                    lag_ratio=0.35
                ),
                run_time=0.5
            )

        self.play(
            tracker.animate.set_value(t[-1]),
            run_time=5,
            rate_func = linear
        )

        # New titles
        self.play(
            FadeOut(*solution_labels)
        )
        self.play(
            model_label.animate.to_corner(DL),
            FadeOut(titlep1, titlep2),
        )
        self.play(
            Write(titlep3)
        )
        self.wait()

        # animate equilibrium solution data
        for line, label in zip(constant_solution_lines, constant_solution_labels):
            self.play(
                Create(line),
                Write(label)
            )
        self.wait(1)
        for label in limit_labels:
            self.play(
                LaggedStart(
                    Write(label),
                    lag_ratio=0.5
                )
            )
        self.wait(5)
