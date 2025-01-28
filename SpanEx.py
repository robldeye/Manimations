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
        vsum = Vector([-1, -0.5], color=PURPLE)
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
        v1_def = MathTex(r"\mathbf{v}_1=\begin{bmatrix} 1 \\ -1 \end{bmatrix}", color=GREEN).to_edge(UL)
        v1_label = always_redraw(
            lambda: MathTex(r"\mathbf{v}_1", color=GREEN).next_to(v1.get_center(), RIGHT)
        )
        vsum_label = MathTex(r"\mathbf{v}_1 + \mathbf{v}_2", color=PURPLE).next_to(vsum.get_center(), UL)
        x1v1_label = always_redraw(
            lambda: MathTex(r"x_1 \mathbf{v}_1", color=GREEN).next_to(x1v1.get_center(), RIGHT)
        )
        v2_def = MathTex(r"\mathbf{v}_2=\begin{bmatrix} -2 \\ 0.5 \end{bmatrix}", color=YELLOW).next_to(v1_def, DOWN)
        v2_label = always_redraw(
            lambda: MathTex(r"\mathbf{v}_2", color=YELLOW).next_to(v2.get_center(), DOWN)
        )
        xvsum_label = always_redraw(
            lambda: MathTex(r"x_2 \mathbf{v}_2", color=YELLOW).next_to(xvsum.get_center(), DOWN)
        )
        #sum_label = MathTex(r"x_1 \mathbf{v}_1 + x_2 \mathbf{v}_2")
        span_label = MathTex(r"\text{Span}(\mathbf{v}_1)", color=YELLOW).next_to(v1.get_end(), RIGHT, buff=0.2)
        title = MathTex(r"\text{Span}(\{\mathbf{v}_1, \mathbf{v}_2\})=\mathbb{R}^2", color=PURPLE).to_edge(UP)




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
        self.play(FadeIn(vsum, vsum_label))
        self.wait()

        
        # Scaling v_1 and v_2 to obtain elements of their Span
        self.play(
            FadeOut(v1, v1_label, v2, v2_label, vsum, vsum_label),
            FadeIn(x1v1, x1v1_label, xvsum, xvsum_label)
        )
        self.wait()

        # 1
        self.play(
            x1.animate.set_value(2), 
            x2.animate.set_value(-1),
            run_time=1,
            rate_func=smooth
        )
        self.add(
            Vector([x1.get_value() - 2*x2.get_value(), -1*x1.get_value() + 0.5*x2.get_value()], color=PURPLE)
        )
        self.wait(0.5)


        # 2
        self.play(
            x1.animate.set_value(1), 
            x2.animate.set_value(-3),
            run_time=1,
            rate_func=smooth
        )
        self.add(
            Vector([x1.get_value() - 2*x2.get_value(), -1*x1.get_value() + 0.5*x2.get_value()], color=PURPLE)
        )
        self.wait(0.5)


        # 3
        self.play(
            x1.animate.set_value(-1), 
            x2.animate.set_value(1),
            run_time=1,
            rate_func=smooth
        )
        self.add(
            Vector([x1.get_value() - 2*x2.get_value(), -1*x1.get_value() + 0.5*x2.get_value()], color=PURPLE)
        )
        self.wait(0.5)


        # 4
        self.play(
            x1.animate.set_value(1), 
            x2.animate.set_value(1.5),
            run_time=1,
            rate_func=smooth
        )
        self.add(
            Vector([x1.get_value() - 2*x2.get_value(), -1*x1.get_value() + 0.5*x2.get_value()], color=PURPLE)
        )
        self.wait(0.5)


        # 5
        self.play(
            x1.animate.set_value(2), 
            x2.animate.set_value(2),
            run_time=1,
            rate_func=smooth
        )
        self.add(
            Vector([x1.get_value() - 2*x2.get_value(), -1*x1.get_value() + 0.5*x2.get_value()], color=PURPLE)
        )
        self.wait(0.5)


        # 6
        self.play(
            x1.animate.set_value(0.5), 
            x2.animate.set_value(1),
            run_time=1,
            rate_func=smooth
        )
        self.add(
            Vector([x1.get_value() - 2*x2.get_value(), -1*x1.get_value() + 0.5*x2.get_value()], color=PURPLE)
        )
        self.wait(0.5)


        # 7
        self.play(
            x1.animate.set_value(1.5), 
            x2.animate.set_value(1),
            run_time=1,
            rate_func=smooth
        )
        self.add(
            Vector([x1.get_value() - 2*x2.get_value(), -1*x1.get_value() + 0.5*x2.get_value()], color=PURPLE)
        )
        self.wait(0.5)


        self.play(
            FadeOut(x1v1, x1v1_label, xvsum, xvsum_label)
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
        self.play(Write(title))
        self.wait(3)