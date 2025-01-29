from manim import *

class SpanLine(Scene):
    def construct(self):
        # Create the number plane (grid)
        grid = NumberPlane(
            x_range=(-10,10,1),
            y_range=(-5,5,1),
            background_line_style={"stroke_color": BLUE, "stroke_width": 2, "stroke_opacity": 0.8},
            faded_line_style={"stroke_color": BLUE, "stroke_width": 1, "stroke_opacity": 0.5},
            faded_line_ratio=2,
        )

        # Mobjects
        v1 = Vector([2,2], color=GREEN)
        v2 = Vector([2, -1], color=YELLOW)
        vsum = Vector([4, 1], color=PURPLE)
        x1 = ValueTracker(1)
        x2 = ValueTracker(1)
        x1v1 = always_redraw(
            lambda: Vector([2*x1.get_value(),2*x1.get_value()], color=GREEN)
        )
        x2v2 = always_redraw(
            lambda: Vector([2*x2.get_value(), -1*x2.get_value()], color=YELLOW)
        )
        xvsum = always_redraw(
            lambda: Vector([4*x2.get_value(), 1*x2.get_value()], color=YELLOW).shift(Vector([x1.get_value(),-1*x1.get_value()], color=GREEN).get_end())  
        )
        span_v2 = Line(
            start=-10*v2.get_unit_vector(),
            end=10*v2.get_unit_vector(),
            color=YELLOW,
            stroke_width=4,
        )
        span_v2.add_updater(
            lambda l: l.move_to(x1v1.get_end())
        )

        # Labels
        v1_def = MathTex(r"\mathbf{v}_1=\begin{bmatrix} 2 \\ 2 \end{bmatrix}", color=GREEN).to_edge(UL)
        v1_label = always_redraw(
            lambda: MathTex(r"\mathbf{v}_1", color=GREEN).next_to(v1.get_center(), RIGHT)
        )
        vsum_label = MathTex(r"\mathbf{v}_1 + \mathbf{v}_2", color=PURPLE).next_to(vsum.get_center(), UL)
        x1v1_label = always_redraw(
            lambda: MathTex(f"{x1.get_value():.2f}" r"\mathbf{v}_1", color=GREEN).next_to(x1v1.get_center(), RIGHT)
        )
        v2_def = MathTex(r"\mathbf{v}_2=\begin{bmatrix} 2 \\ -1 \end{bmatrix}", color=YELLOW).next_to(v1_def, DOWN)
        v2_label = always_redraw(
            lambda: MathTex(r"\mathbf{v}_2", color=YELLOW).next_to(v2.get_center(), DOWN)
        )
        xvsum_label = always_redraw(
            lambda: MathTex(f"{x2.get_value():.2f}" r"\mathbf{v}_2", color=YELLOW).next_to(xvsum.get_center(), DOWN)
        )
        x2v2_label = always_redraw(
            lambda: MathTex(f"{x2.get_value():.2f}" r"\mathbf{v}_2", color=YELLOW).next_to(x2v2.get_center(), DOWN)
        )
        #sum_label = MathTex(r"x_1 \mathbf{v}_1 + x_2 \mathbf{v}_2")
        span_label = always_redraw(
            lambda: MathTex(r"\text{Span}(\mathbf{v}_2)", color=YELLOW).next_to(span_v2.get_center())
        )
        title = MathTex(r"\text{Span}(\{\mathbf{v}_1, \mathbf{v}_2\})=\mathbb{R}^2").to_edge(UP).scale(1.25)




        # Vector Addition
        self.add(grid)
        self.wait()
        self.play(Write(v1_def))
        self.play(Write(v2_def))
        self.play(FadeIn(v1, v2, v1_label, v2_label, run_time=1))
        self.wait()

        v2group = VGroup(v2, v2_label)

        self.play(
            v2group.animate.shift(v1.get_end()),
        )
        self.wait()

        self.play(FadeOut(v1, v1_label, v1_def, v2_def, v2group, run_time=1))

        x1.set_value(-2)
        self.play(FadeIn(x1v1, x1v1_label))
        linegroup = VGroup(x1v1, span_v2, span_label)
       
        self.play(FadeIn(linegroup))
        self.play(x1.animate.set_value(2), run_time=4, rate_func=linear)
        self.wait()
        self.play(Write(title))
        self.wait(3)