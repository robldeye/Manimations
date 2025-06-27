from manim import *
import numpy as np
from sympy import Matrix, Rational, latex
from scipy.integrate import odeint
from scipy.interpolate import interp1d

class phase_saddle(Scene):
    def construct(self):
        # Grid
        locations = []
        bound = 4
        grid = Axes(
            x_range=(-bound, bound, 1),
            y_range=(-bound, bound, 1),
            x_length=9,
            y_length=9,
            tips=True,
            axis_config={"include_numbers": False}
        ).to_edge(RIGHT).scale(0.95)
        grid.get_axis_labels(x_label="x_1", y_label="x_2")

        for x in np.arange(-bound, bound+1):
            for y in np.arange(-bound, bound+1):
                locations.append([x, y])

        titlep1  = MathTex(r"\text{System with positive}").to_corner(UL)
        titlep2 = MathTex(r"\text{and negative eigenvalues}").next_to(titlep1, DOWN).align_to(titlep1, LEFT)
        
        A = np.array([
            [0.2, 0.3],
            [0.1, -0.1]
            ])
        A_mat = Matrix([
            [Rational(2, 10), Rational(3, 10)],
            [Rational(1, 10), -Rational(1, 10)]
        ])

        A_label = MathTex(
            rf"A = \begin{{bmatrix}} {f"{A[0,0]}"} & {f"{A[0,1]}"} \\ {f"{A[1,0]}"} & {f"{A[1,1]}"} \end{{bmatrix}}"
            ).to_corner(UL).shift(1.5*DOWN) # not using relative anchoring is sloppy since I added title later -- sorry <3
        
        def model(v, t):
            return np.dot(A, v)
        model_label = MathTex(
            r"\frac{d\vec{x}}{dt} = A\vec{x}"
            ).next_to(A_label, DOWN).align_to(A_label, LEFT)
        
        v1_0 = np.array([1, 1])
        v1_0_label = MathTex(
            rf"\vec{{x}}(0) = \begin{{bmatrix}} {f"{v1_0[0]}"} \\ {f"{v1_0[1]}"} \end{{bmatrix}}"
            ).next_to(model_label, DOWN).align_to(model_label, LEFT)

        # Linear Algebra for solution and eigenspaces
        eigenvalues = []
        eigenvectors = []
        for value, mult, vector in A_mat.eigenvects():
            eigenvectors.extend(vector)
            eigenvalues.append(value)

        minEvecs = []
        for vector in eigenvectors:
            minEvec = vector / vector[np.argmin(np.abs(vector))] # make smallest entry 1
            minEvecs.append(minEvec) #append since minEvec is a SymPy column vector
        Evec_mat = Matrix.hstack(*minEvecs)
        sol_coeffs = Evec_mat.inv() @ v1_0

        # solution expression label
        # solution_label1 = MathTex(
        #     r"\vec{x}(t)", 
        #     r"=",
        # )
        # solution_label1[0].set_color(YELLOW)
        # solution_label2_strings = []
        # for value, minEvec, coeff in zip(eigenvalues, minEvecs, sol_coeffs):
        #     string = rf"{latex(coeff)} \begin{{bmatrix}} {minEvec[0]:.0f} \\ {minEvec[1]:.0f} \end{{bmatrix}} e^{{{float(value):.1f}t}}"
        #     solution_label2_strings.append(string)
        # solution_label2_expression = " + ".join(solution_label2_strings)
        # solution_label2 = MathTex(
        #     solution_label2_expression
        # ).next_to(solution_label1, RIGHT)
        # solution_label = VGroup(solution_label1, solution_label2)

        # lines showing eigenspaces
        Eigenspaces = VGroup()
        Eigenspace_colors = color_gradient([YELLOW, GREEN], 2)
        for i, vector in enumerate(eigenvectors):
            scale_factor = np.max(np.abs(vector))
            vector_maxscaled = vector / scale_factor # make largest entry 1
            vector_line = DashedLine(
                start = grid.c2p(*(-(bound+0.25)*vector_maxscaled)),
                end = grid.c2p(*((bound+0.25)*vector_maxscaled)),
                color = Eigenspace_colors[i],
            ).set_opacity(0.5)
            Eigenspaces.add(vector_line)

        # labels for eigenvalues (color matches eigenspace)
        Eigenvalues_labels = VGroup()
        for i, value in enumerate(eigenvalues):
            label = MathTex(
                rf"\lambda_{i+1} \sim {float(value):.2f}",
                color=Eigenspace_colors[i]
            ).next_to(model_label, 2.5*(i+1)*DOWN).align_to(model_label, LEFT)
            Eigenvalues_labels.add(label)

        # Eigenspaces_label = MathTex(
        #     r"\text{Nul}(A-\lambda_i I)",
        #     color=ORANGE
        # ).to_corner(DL)

        # solving ODE for multiple solution paths
        tracker = ValueTracker(0)
        np.random.seed(42)
        num_vectors_to_sample = 5
        angles = np.random.uniform(0, 2 * np.pi, num_vectors_to_sample)
        initial_vectors = np.column_stack((np.cos(angles), np.sin(angles)))
        t = np.linspace(0, 10, 1000) # smoothness of curve later on tied to framerate in manim.cfg, not step size

        def make_solution_dot(interpolated_solution, solution_color):
            return always_redraw(
                lambda: Dot(
                    point=grid.c2p(*interpolated_solution(tracker.get_value())),
                    color=solution_color
                )
            )
        def make_solution_label(solution_dot, solution_color, index):
            return always_redraw(
                lambda: MathTex(
                    rf"\vec{{x}}_{{{index+1}}}(t)",
                    color=solution_color
                ).next_to(solution_dot, UP)
            )
        colors = color_gradient([RED, BLUE], num_vectors_to_sample)

        interpolated_solution_vectors = []
        solution_dots = VGroup()
        solution_labels = VGroup()
        solution_paths = VGroup()

        for i, vec in enumerate(initial_vectors):
            solution_color = colors[i]
            solution = odeint(model, vec, t)
            interpolated_solution = interp1d(t, solution, axis=0, kind='linear')
            interpolated_solution_vectors.append(interpolated_solution)

            solution_dot = make_solution_dot(interpolated_solution, solution_color)
            solution_dot.z_index=1 # to place dot above (in front of) trailing path
            solution_dots.add(solution_dot)

            solution_label = make_solution_label(solution_dot, solution_color, i)
            solution_labels.add(solution_label)

            solution_path = TracedPath(solution_dot.get_center, stroke_color=solution_color)
            solution_paths.add(solution_path)

        # some functions for making direction field arrows
        def dir(x, y):
            return np.dot(A, np.array([x, y]))
        
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

        scale = 0.5
        arrows = VGroup(
            Arrow(
                start = grid.c2p(*(np.array(loc)) - scale * unit(dir(*loc))),
                end = grid.c2p(*(np.array(loc) + scale * unit(dir(*loc)))),
            )
            for loc in locations
        )

        # start scene
        self.play(
            Write(titlep1),
            Write(titlep2),
            FadeIn(grid)
        )
        self.play(Write(grid.get_axis_labels(x_label="x_1", y_label="x_2")))
        self.wait()

        # add system
        labels = VGroup(A_label, model_label)
        labels.add(*Eigenvalues_labels)
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
        self.wait(2)

        # reset tracker to show multiple possible solutions
        tracker.set_value(0.0001)
        for dot, path, label in zip(solution_dots, solution_paths, solution_labels):
            self.play(
                Create(dot),
                Create(path),
                Write(label)
            )
        # self.play(
        #     LaggedStart(*(FadeIn(obj) for obj in solution_dots), lag_ratio=0.8),
        #     LaggedStart(*(FadeIn(obj) for obj in solution_paths), lag_ratio=0.8),
        #     LaggedStart(*(Write(obj) for obj in solution_labels), lag_ratio=0.8)
        #     )
        # self.wait()

        self.play(
            tracker.animate.set_value(t[-1]),
            run_time=5,
            rate_func = linear
        )

        self.play(
            # Write(Eigenspaces_label),
            FadeIn(Eigenspaces)
        )
        self.wait(3)
