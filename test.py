from manim import *
import numpy as np
from scipy.integrate import solve_ivp

class SpringODEScene(Scene):
    def construct(self):
        # Placeholder constants for ODE: a*y'' + b*y' + c*y = 0
        a = 1
        b = 0.5
        c = 2
        y0 = 2       # Initial position
        y_prime0 = 0  # Initial velocity

        # Time range for animation
        t_max = 10
        fps = 30
        times = np.linspace(0, t_max, int(t_max * fps))

        # Solve the ODE numerically using scipy
        def ode_system(t, y):  # y = [position, velocity]
            return [y[1], (-b * y[1] - c * y[0]) / a]

        sol = solve_ivp(ode_system, [0, t_max], [y0, y_prime0], t_eval=times)
        y_values = sol.y[0]  # position values over time

        # ValueTracker for time progression
        time_tracker = ValueTracker(0)

        # Spring base point (fixed)
        spring_top = UP * 2

        # Function to get current spring length from ODE solution
        def get_current_y():
            t = time_tracker.get_value()
            index = min(int(t * fps), len(y_values) - 1)
            return y_values[index]

        # Redraw spring based on current y-position
        def get_spring():
            length = get_current_y()
            coils = 8
            amplitude = 0.2
            return ParametricFunction(
                lambda t: spring_top + DOWN * length * t + 
                          RIGHT * amplitude * np.sin(coils * 2 * PI * t),
                t_range = [0, 1],
                color = BLUE,
                stroke_width = 4
            )

        spring = always_redraw(get_spring)

        # Create square and update its position
        square = Square(side_length=0.4, color=YELLOW, fill_opacity=1)
        square.add_updater(lambda m: m.move_to(spring_top + DOWN * get_current_y()))

        # Add to scene
        self.add(spring, square)

        # Animate time progression
        self.play(
            time_tracker.animate.set_value(t_max),
            run_time=10,
            rate_func=linear
        )

        self.wait()
