from manim import *

class LinearTransformationSceneExample(Scene):
    def construct(self):
        # Define the transformation matrix
        matrix = [[1, 1], [-1, 2]]

        # Create a grid to represent R^2
        grid = NumberPlane(background_line_style={"stroke_color": BLUE, "stroke_opacity": 0.5})

        # Label the transformation
        label = MathTex(r"A = \begin{bmatrix} 1 & 1 \\ -1 & 2 \end{bmatrix}").to_corner(UL)

        # Create the initial square
        square = Square(color=YELLOW, fill_opacity=0.5).scale(2).move_to(ORIGIN)

        # Add the grid, label, and square
        self.add(grid, label, square)

        # Apply the linear transformation
        self.play(ApplyMatrix(matrix, square))

        # Pause briefly to let the viewer see the result
        self.wait(2)
