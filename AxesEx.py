from manim import *

class AxesEx(ThreeDScene):
    def construct(self):
        # Create the 3D axes
        axes = ThreeDAxes()
        self.add(axes)

        # Define the range and step size for grid lines
        x_range = [-5, 5, 1]
        y_range = [-5, 5, 1]
        z_range = [-5, 5, 1]

        # Create grid lines parallel to the XY plane
        xy_grid = VGroup()
        for x in range(x_range[0], x_range[1] + 1, x_range[2]):
            xy_grid.add(axes.plot_parametric_curve(
                lambda t: np.array([x, t, 0]),
                t_range=y_range[:2],
                color=BLUE,
            ).set_opacity(0.5))
        for y in range(y_range[0], y_range[1] + 1, y_range[2]):
            xy_grid.add(axes.plot_parametric_curve(
                lambda t: np.array([t, y, 0]),
                t_range=x_range[:2],
                color=BLUE,
            ).set_opacity(0.5))

        # Create grid lines parallel to the XZ plane
        xz_grid = VGroup()
        for x in range(x_range[0], x_range[1] + 1, x_range[2]):
            xz_grid.add(axes.plot_parametric_curve(
                lambda t: np.array([x, 0, t]),
                t_range=z_range[:2],
                color=GREEN,
            ).set_opacity(0.5))
        for z in range(z_range[0], z_range[1] + 1, z_range[2]):
            xz_grid.add(axes.plot_parametric_curve(
                lambda t: np.array([t, 0, z]),
                t_range=x_range[:2],
                color=GREEN,
            ).set_opacity(0.5))

        # Create grid lines parallel to the YZ plane
        yz_grid = VGroup()
        for y in range(y_range[0], y_range[1] + 1, y_range[2]):
            yz_grid.add(axes.plot_parametric_curve(
                lambda t: np.array([0, y, t]),
                t_range=z_range[:2],
                color=RED,
            ).set_opacity(0.5))
        for z in range(z_range[0], z_range[1] + 1, z_range[2]):
            yz_grid.add(axes.plot_parametric_curve(
                lambda t: np.array([0, t, z]),
                t_range=y_range[:2],
                color=RED,
            ).set_opacity(0.5))

        # Combine all grid lines into one VGroup
        grid_lines = VGroup(xy_grid, xz_grid, yz_grid)

        # Add the grids to the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        self.add(grid_lines)
        self.wait(1)

        # Transformation
        transformation_matrix = [[1, -1, 2],
                                 [-1, 1, -2],
                                 [0.5, -0.5, 1]]
        self.play(grid_lines.animate.apply_matrix(transformation_matrix), run_time=3)

        # Pause
        self.wait(3)
