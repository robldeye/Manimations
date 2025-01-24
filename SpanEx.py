from manim import *

class SpanEx(Scene):
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
        v1 = Vector([1,-1], color=GREEN)
        v2 = Vector([-2, 0.5], color=YELLOW)
        x1 = ValueTracker(1)
        x2 = ValueTracker(1)
        x1v1 = always_redraw(
            lambda: Vector([x1.get_value(),-1*x1.get_value()], color=GREEN)
        )
        x2v2 = always_redraw(
            lambda: Vector([-2*x2.get_value(), 0.5*x2.get_value()], color=YELLOW)
        )
        xvsum = always_redraw(
            lambda: Vector([-2*x2.get_value(), 0.5*x2.get_value()], color=YELLOW).shift(Vector([x1.get_value(),-1*x1.get_value()], color=GREEN).get_end())  
        )
        span_v1 = Line(
            start=-6*v1.get_unit_vector(),
            end=6*v1.get_unit_vector(),
            color=PURPLE,
            stroke_width=2,
        )


        # Labels
        v1_label = MathTex(r"\mathbf{v}=\begin{bmatrix} 1 \\ -1 \end{bmatrix}", color=GREEN).next_to(v1.get_end(), RIGHT, buff=0.2)
        x1v1_label = always_redraw(
            lambda: MathTex(r"x_1 \mathbf{v}_2", color=GREEN).next_to(x1v1.get_end(), RIGHT, buff=0.2)
        )
        v2_label = MathTex(r"\mathbf{v}=\begin{bmatrix} -2 \\ 0.5 \end{bmatrix}", color=YELLOW).next_to(v2.get_end(), RIGHT, buff=0.2)
        x2v2_label = always_redraw(
            lambda: MathTex(r"x_2 \mathbf{v}_2", color=YELLOW).next_to(x2v2.get_end(), RIGHT, buff=0.2)
        )
        #sum_label = MathTex(r"x_1 \mathbf{v}_1 + x_2 \mathbf{v}_2")
        span_label = MathTex(r"\text{Span}(\mathbf{v}_1)", color=YELLOW).next_to(v1.get_end(), RIGHT, buff=0.2)

        # Initial Scene
        self.add(grid)
        self.wait()

        # Animations
        self.play(
            FadeIn(
                v1, 
                #v1_label, 
                v2, 
                #v2_label, 
                run_time=1
            )
        )
        self.wait(1)

        self.play(
            v2.animate.shift(v1.get_end())
        )

        #self.play(
            #FadeIn(
                #x1v1, 
                #x1v1_label, 
                #x2v2, 
                #x2v2_label
            #)
        #)
        self.play(
            FadeOut(v1, v2),
            FadeIn(x1v1, xvsum)
        )
        self.play(
            x1.animate.set_value(2), 
            x2.animate.set_value(-1),
            run_time=2,
            rate_func=smooth
        )
        self.play(
            x1.animate.set_value(1), 
            x2.animate.set_value(-3),
            run_time=2,
            rate_func=smooth
        )
        self.play(
            x1.animate.set_value(-1), 
            x2.animate.set_value(1),
            run_time=2,
            rate_func=smooth
        )
        
        #Swap v1 for Span(v1)
        #self.play(
            #FadeOut(
                #x1v1, 
                #x1v1_label
            #),
            #FadeIn(
                #v1, 
                #v1_label
            #),
            #Transform(
                #v1, 
                #span_v1
            #),
            #Transform(
                #v1_label, 
                #span_label
            #),
            #run_time=3,
        #)

        # Hold Final
        self.wait(3)