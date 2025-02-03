from manim import *

class sl3d(ThreeDScene):
    def construct(self):
        # Grid
        grid = ThreeDAxes(
            x_range=(-5,5,1),
            y_range=(-5,5,1),
            z_range=(-5,5,1),
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Mobjects
        a1 = Vector([2, 2, 1], color=GREEN)
        a2 = Vector([2, -1, 0], color=YELLOW)
        asum = Vector([4, 1, 1], color=PURPLE)
        x1 = ValueTracker(1)
        x2 = ValueTracker(1)
        x1a1 = always_redraw(
            lambda: Vector([2*x1.get_value(),2*x1.get_value(), 1*x1.get_value()], color=GREEN)
        )
        x2a2 = always_redraw(
            lambda: Vector([2*x2.get_value(), -1*x2.get_value(), 0], color=YELLOW)
        )
        xasum = always_redraw(
            lambda: Vector([4*x2.get_value(), 1*x2.get_value(), 0], color=YELLOW).shift(Vector([2*x1.get_value(), 2*x1.get_value(), 1*x2.get_value()], color=GREEN).get_end())  
        )
        span_a2 = Line(
            start=-10*a2.get_unit_vector(),
            end=10*a2.get_unit_vector(),
            color=YELLOW,
            stroke_width=4,
        )
        span_a2.add_updater(
            lambda l: l.move_to(x1a1.get_end())
        )

        sweep = Surface(
            lambda u, v: np.array([
                u,
                v,
                1/6*u+1/3*v
            ]),
            u_range=[-8, 8], 
            v_range=[-8, 8],
            checkerboard_colors=[RED_D, RED_E], resolution=(15, 32)
        )

        # Labels
        a1_def = MathTex(r"\vec{a}_1=\begin{bmatrix} 2 \\ 2 \\ 1 \end{bmatrix}", color=GREEN).to_edge(UL)
        a1_label = always_redraw(
            lambda: MathTex(r"\vec{a}_1", color=GREEN).next_to(a1.get_center(), UL).rotate(PI/2,axis=RIGHT)
        )
        vsum_label = MathTex(r"\vec{a}_1 + \vec{a}_2", color=PURPLE).next_to(asum.get_center(), UL)
        x1a1_label = always_redraw(
            lambda: MathTex(f"{x1.get_value():.2f}" r"\vec{a}_1", color=GREEN).next_to(x1a1.get_center(), UL).rotate(PI/2,axis=RIGHT)
        )
        a2_def = MathTex(r"\vec{a}_2=\begin{bmatrix} 2 \\ -1 \\ 0 \end{bmatrix}", color=YELLOW).next_to(a1_def, DOWN)
        a2_label = MathTex(r"\vec{a}_2", color=YELLOW).next_to(a2.get_center(), DOWN).rotate(PI/2,axis=RIGHT)
        xasum_label = always_redraw(
            lambda: MathTex(f"{x2.get_value():.2f}" r"\vec{a}_2", color=YELLOW).next_to(xasum.get_center(), DOWN).rotate(PI/2,axis=RIGHT)
        )
        x2a2_label = always_redraw(
            lambda: MathTex(f"{x2.get_value():.2f}" r"\vec{a}_2", color=YELLOW).next_to(x2a2.get_center(), DOWN).rotate(PI/2,axis=RIGHT)
        )
        #sum_label = MathTex(r"x_1 \vec{a}_1 + x_2 \vec{a}_2")
        span_label = always_redraw(
            lambda: MathTex(r"\text{Span}(\vec{a}_2)", color=YELLOW).next_to(x1a1.get_end(), UR).rotate(PI/2,axis=RIGHT)
        )
        title = MathTex(r"\text{Span}(\{\vec{a}_1, \vec{a}_2\})= \, \text{a plane}").to_edge(UP).scale(1.25)

        # VGroups

        a2_grp = VGroup(a2, a2_label)
        linegroup = VGroup(x1a1, x1a1_label, span_a2, span_label)
        #fillgroup = VGroup()
        #fillgroup.add(*[span_a2 for x1 in range(-3,3)])

        # Get to position
        self.add(grid)
        self.wait()

        self.add_fixed_in_frame_mobjects(a1_def, a2_def)
        self.play(FadeIn(a1, a2))
        self.play(
            Write(a1_label),
            Write(a2_label)
        )
        self.wait()

        self.play(
            a2_grp.animate.shift(a1.get_end()),
            a2_label.animate.shift(a1.get_end(), UP)
        )
        self.wait()

        # Sweeping Line      
        self.play(
            FadeOut(a1, a1_label, a2_grp),
            FadeIn(x1a1, span_a2)    
        )
        self.play(Write(x1a1_label),
                  Write(span_label)
        )        
        self.wait(2)

        self.play(x1.animate.set_value(3), run_time=2, rate_func=linear)
        self.wait()

        self.play(x1.animate.set_value(-3), run_time=6, rate_func=linear)
        self.wait()
        self.play(FadeOut(linegroup))
        #self.add(fillgroup)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Create(sweep))
        self.wait(3)