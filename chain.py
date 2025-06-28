from manim import *

class chain(Scene):
    def construct(self):
        # axes
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            x_length=6,
            y_length=6,
            x_axis_config={
                "numbers_to_include": np.arange(-3, 3.01, 1),
            },
            y_axis_config={
                "numbers_to_include": np.arange(-3, 3.01, 1)
            },
            tips=False, 
        )

        # functions

        def f(t):
            return np.sin(t)

        def g(t):
            return t**2
        
        # mobjects
        dot = Dot(position = )
    
        self.add(axes)

