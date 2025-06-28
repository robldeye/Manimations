from manim import *
import numpy as np
from sympy import Matrix, Rational, latex
from scipy.integrate import odeint
from scipy.interpolate import interp1d

class phase_source(Scene):
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
        titlep2 = MathTex(r"\text{and distinct eigenvalues}").next_to(titlep1, DOWN).align_to(titlep1, LEFT)
        
        A = np.array([
            [0.3, 0.1],
            [0.2, 0.4]
            ])
        A_mat = Matrix([
            [Rational(3, 10), Rational(1, 10)],
            [Rational(1, 5), Rational(2, 5)]
        ])
        eigenvalues = []
        eigenvectors = []
        for value, mult, vector in A_mat.eigenvects():
            eigenvectors.extend(vector)
            eigenvalues.append(value)

        Eigenspaces = VGroup()
        for vector in eigenvectors:
            scale_factor = np.max(np.abs(vector))
            vector_maxscaled = vector / scale_factor # make largest entry 1
            vector_line = DashedLine(
                start = grid.c2p(*(-(bound+0.5)*vector_maxscaled)),
                end = grid.c2p(*((bound+0.5)*vector_maxscaled)),
                color = ORANGE,
            ).set_opacity(0.5)
            Eigenspaces.add(vector_line)

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

        solution_label1 = MathTex(
            r"\vec{x}(t)", 
            r"=",
        )
        solution_label1[0].set_color(YELLOW)

        minEvecs = []
        for vector in eigenvectors:
            minEvec = vector / vector[np.argmin(np.abs(vector))] # make smallest entry 1
            minEvecs.append(minEvec) #append since minEvec is a SymPy column vector
        Evec_mat = Matrix.hstack(*minEvecs)
        sol_coeffs = Evec_mat.inv() @ v1_0

        solution_label2_strings = []
        for value, minEvec, coeff in zip(eigenvalues, minEvecs, sol_coeffs):
            string = rf"{latex(coeff)} \begin{{bmatrix}} {minEvec[0]:.0f} \\ {minEvec[1]:.0f} \end{{bmatrix}} e^{{{float(value):.1f}t}}"
            solution_label2_strings.append(string)
        solution_label2_expression = " + ".join(solution_label2_strings)
        solution_label2 = MathTex(
            solution_label2_expression
        ).next_to(solution_label1, RIGHT)
        solution_label = VGroup(solution_label1, solution_label2)

        Eigenspaces_label = MathTex(
            r"\text{Nul}(A-\lambda_i I)",
            color=ORANGE
        ).to_corner(DL)

        t = np.linspace(0, 3, 1000) # smoothness of curve later on tied to framerate in manim.cfg, not step size
        solution1 = odeint(model, v1_0, t)
        interp_sol1 = interp1d(t, solution1, axis=0, kind='linear')

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
        labels = [A_label, model_label, v1_0_label]
        self.play(
            LaggedStart(*(Write(label) for label in labels), lag_ratio=0.5)
        )
        self.wait()

        tracker = ValueTracker(0)
        soldot1 = always_redraw(
            lambda: Dot(
                point = grid.c2p(*interp_sol1(tracker.get_value())),
                color = YELLOW
            )
        )
        soldot1.z_index=1 # to place dot above (in front of) trailing path

        dot1_label1 = MathTex(
                r"\vec{x}(0)",
                color=YELLOW
            ).next_to(soldot1.get_center(), UP)
        
        dot1_label2 = always_redraw(
            lambda: MathTex(
                r"\vec{x}(t)",
                # rf"\vec{{x}}({f"{tracker.get_value():.1f}"})", # to show time values instead
                color=YELLOW
            ).next_to(soldot1.get_center(), UP)
        )

        path1 = TracedPath(soldot1.get_center, stroke_color=GREEN)

        initial_objects = [soldot1, dot1_label1, path1]
        self.play(
            LaggedStart(*(Create(obj) for obj in initial_objects), lag_ratio=0.8)
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

        self.play(
            ReplacementTransform(dot1_label1, dot1_label2),
        )

        self.play(
            Write(solution_label.scale(0.8).next_to(v1_0_label, DOWN).align_to(v1_0_label, LEFT))
            )
        self.wait()


        # animate x(t)
        self.add(soldot1.copy().set_opacity(0.5)) #add copy of v1_0
        tracker.set_value(0.0001) # to prevent value=0 weirdness
        self.play(
            tracker.animate.set_value(t[-1]),
            run_time=5,
            rate_func = linear
        )
        self.wait()

        self.play(
            Write(Eigenspaces_label),
            FadeIn(Eigenspaces)
        )
        self.wait(3)
