from manim import *

class Determinant(Scene):
    def construct(self):
        # Grids

        grid = NumberPlane(
            x_range=(-1, 5, 1),
            y_range=(-1, 5, 1),
            background_line_style={"stroke_color": BLUE, "stroke_opacity": 0.5}
        ).to_edge(RIGHT)

        # Mobjects
        A1 = [[3, 0], [0, 2]]

        v1 = Vector([1, 0]).shift(grid.c2p(0,0))
        A1v1 = Vector([3, 0]).shift(grid.c2p(0,0))
        v2 = Vector([0, 1]).shift(grid.c2p(0,0))
        A1v2 = Vector([0, 2]).shift(grid.c2p(0,0))

        region = Polygon(
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=0.25,
            stroke_width=1
        ).shift(grid.c2p(0,0))

        t = ValueTracker(0)

        region.add_updater(
            lambda r: r.become(
                Polygon(
                    [0, 0, 0], [1+2*t.get_value(), 0, 0], [1+2*t.get_value(), 1+t.get_value(), 0], [0, 1+t.get_value(), 0],
                    color=GREEN, 
                    fill_color=GREEN,
                    fill_opacity=0.25,
                    stroke_width=1
                ).shift(grid.c2p(0,0))
            )
        )
        def r1area(x):
            return (1+x)*(1+2*x)
            

        # Labels
        basis_label = MathTex(r"\vec{v}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \, \vec{v}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}").to_corner(UL).scale(0.65)
        A1_label = MathTex(r"A = \begin{bmatrix} 3 & 0 \\ 0 & 2 \end{bmatrix}").next_to(basis_label, DOWN)
        region_label = always_redraw(
            lambda: MathTex(r"\text{Area} = ", f"{r1area(t.get_value()):.2f}").next_to(A1_label, DOWN)
        )
        region_label[0].add_updater(
            lambda l: l.become(region_label[0].set_color(GREEN))
        )
        v1_label = MathTex(r"\vec{v}_1").next_to(v1, DR).scale(0.75)
        v2_label = MathTex(r"\vec{v}_2").next_to(v2, UL).scale(0.75)
        A1v1_label = MathTex(r"3\vec{v}_1").next_to(A1v1, DR).scale(0.75)
        A1v2_label = MathTex(r"2\vec{v}_2").next_to(A1v2, UL).scale(0.75)


        # VGroups
        v1_group = VGroup(v1, v1_label)
        v2_group = VGroup(v2, v2_label)
        A1v1_group = VGroup(A1v1, A1v1_label)
        A1v2_group = VGroup(A1v2, A1v2_label)

        # Scenes
        self.add(grid, basis_label)
        self.wait()

        self.play(
            Write(A1_label), 
            FadeIn(v1, v2),
            Write(v1_label),
            Write(v2_label)
        )
        self.wait()

        self.play(
            FadeIn(region, run_time=2)
        )
        self.wait()
        self.play(
            Write(region_label)
        )

        # Apply Transformation
        self.play(
            ApplyMatrix(A1, region),
            Transform(v1_group, A1v1_group),
            Transform(v2_group, A1v2_group),
            t.animate.set_value(1),
            run_time=3)

        self.wait(3)
