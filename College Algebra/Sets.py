import random
from sympy import Rational
from manim import *

class Sets(Scene):
    def construct(self):
        # Title
        title = Text("Commonly Encountered Sets", font_size=48)
        self.play(Write(title), run_time=1)
        self.play(title.animate.to_corner(UL))

        line = NumberLine(x_range=[-2, 2+1, 1], length=5, include_tip=True, include_numbers=True)
        # Creates left tips zzz
        def left_tip(nl: NumberLine, tip_length: float = 0.25, tip_width: float = 0.25) -> VGroup:
            x_min_point = nl.n2p(nl.x_range[0])
            segment_lengths = nl.length / (nl.x_range[1] - nl.x_range[0])
            tip = ArrowTriangleFilledTip(fill_color=nl.get_color(), stroke_width=0).scale(1.1)
            tip.next_to(x_min_point, LEFT, buff=0.65*segment_lengths)
            extension = Line(x_min_point, tip.get_right(), color=nl.get_color(), stroke_width=nl.stroke_width)
            group = VGroup(extension, tip)
            nl.add(group)
            return group

        # Naturals
        N_label = MathTex(r"\mathbb{N}=\{1,2,3,4,\dots\}").scale(0.8).next_to(title, 3*DOWN).align_to(title, LEFT)
        N_line = line.copy().to_edge(RIGHT).align_to(N_label, UP)
        N_line_left = left_tip(N_line)
        N_dots = VGroup(Dot(N_line.n2p(i), color=YELLOW) for i in np.arange(1, 3))

        self.play(Write(N_label), run_time=1)
        self.play(FadeIn(N_line, N_line_left))
        self.play(Indicate(N_label))
        self.play(LaggedStart(*(FadeIn(dot) for dot in N_dots), lag_ratio=0.5))

        # Wholes
        W_label = MathTex(r"\mathbb{W}=\{0,1,2,3,4,\dots\}").scale(0.8).next_to(N_label, 3*DOWN).align_to(title, LEFT)
        W_line = line.copy().to_edge(RIGHT).align_to(W_label, UP)
        W_line_left = left_tip(W_line)
        W_dots = VGroup(Dot(W_line.n2p(i), color=YELLOW) for i in np.arange(0, 3))

        self.play(Write(W_label), run_time=1)
        self.play(FadeIn(W_line, W_line_left))
        self.play(Indicate(W_label))
        self.play(LaggedStart(*(FadeIn(dot) for dot in W_dots), lag_ratio=0.5))

        # Integers
        Z_label = MathTex(r"\mathbb{Z}=\{\dots,-2,-1,0,1,2,\dots\}").scale(0.8).next_to(W_label, 3*DOWN).align_to(title, LEFT)
        Z_line = line.copy().to_edge(RIGHT).align_to(Z_label, UP)
        Z_line_left = left_tip(Z_line)
        Z_dots = VGroup(Dot(Z_line.n2p(i), color=YELLOW) for i in np.arange(-2, 3))

        self.play(Write(Z_label), run_time=1)
        self.play(FadeIn(Z_line, Z_line_left))
        self.play(Indicate(Z_label))
        self.play(LaggedStart(*(FadeIn(dot) for dot in Z_dots), lag_ratio=0.2))

        # Rationals
        Q_label = MathTex(r"\mathbb{Q} = \left\{x \, \middle| \, x = \frac{p}{q} \text{ for } p,q \in \mathbb{Z}\right\}").scale(0.8).next_to(Z_label, 3*DOWN).align_to(title, LEFT)
        Q_line = line.copy().to_edge(RIGHT)
        Q_line.move_to([Q_line.get_x(), Q_label.get_y()-0.17, 0])
        Q_line_left = left_tip(Q_line)
        def rationals(n, lbound, ubound, density):
            rat_dots = VGroup()
            while len(rat_dots) < n:
                num = random.randint(lbound*density, ubound*density+1)
                den = random.randint(1, density)
                r = Rational(num, den)
                if lbound <= r <= ubound:
                    rat_dots.add(Dot([Q_line.get_x()+float(r), Q_label.get_y(), 0], color=YELLOW).scale(0.75).set_opacity(0.5))
            return rat_dots
        Q_dots = rationals(100, -2, 2, 5)

        self.play(Write(Q_label), run_time=1)
        self.play(FadeIn(Q_line, Q_line_left))
        self.play(Indicate(Q_label))
        self.play(LaggedStart(*(FadeIn(dot) for dot in Q_dots), lag_ratio=0.1), run_time = 2)

        # Reals
        R_label = MathTex(r"\mathbb{R} = \text{ all numbers on the line}").scale(0.8).next_to(Q_label, 3*DOWN).align_to(title, LEFT)
        R_line = line.copy().to_edge(RIGHT).align_to(R_label, UP)
        R_line_left = left_tip(R_line)
        R_fill_progress = ValueTracker(0)
        R_fill = always_redraw(
            lambda: Line(start = R_line.n2p(-2.65), end = R_line.n2p(-2.5 + R_fill_progress.get_value()*5.2), color=YELLOW)
        )
        self.play(Write(R_label), run_time=1)
        self.play(FadeIn(R_line, R_line_left))
        self.play(Indicate(R_label))
        self.add(R_fill)
        self.play(R_fill_progress.animate.set_value(1))
        self.wait(2)

