from manim import *

class SetOps(Scene):
    def construct(self):
        ellipse1 = Ellipse(
            width=4.0, height=5.0, fill_opacity=0.5, color=BLUE, stroke_width=10
        ).move_to(LEFT)
        ellipse2 = ellipse1.copy().set_color(color=RED).move_to(RIGHT)
        ellipse_group = Group(ellipse1, ellipse2).to_edge(LEFT)
        ellipse1_label = MathTex(r"A", color=BLUE).next_to(ellipse1, UP)
        ellipse2_label = MathTex(r"B", color=RED).next_to(ellipse2, UP)
        set_ops_text = MarkupText("<u>Set Operations</u>")
        self.play(Write(set_ops_text), run_time=1)
        self.play(set_ops_text.animate.to_corner(UL))
        self.play(FadeIn(ellipse_group, ellipse1_label, ellipse2_label))
        self.wait()

        # Intersection
        intersection_text = MathTex(r"\text{Intersection: }", r"A \cap B").to_corner(UR)
        intersection_text[1].set_color(GREEN)
        i = Intersection(ellipse1, ellipse2, color=GREEN, fill_opacity=0.5)
        self.play(Write(intersection_text))
        self.play(Indicate(i))
        self.play(i.animate.scale(0.3).next_to(intersection_text, DOWN))
        self.wait()

        # Union
        union_text = MathTex(r"\text{Union: }", r"A \cup B").next_to(i, DOWN)
        union_text[1].set_color(ORANGE)
        u = Union(ellipse1, ellipse2, color=ORANGE, fill_opacity=0.5)
        self.play(Write(union_text))
        self.play(Indicate(u))
        self.play(u.animate.scale(0.3).next_to(union_text, DOWN))
        self.wait()

        # Exclusion
        difference_text = MathTex(r"\text{Difference: }", r"A - B").next_to(u, DOWN)
        difference_text[1].set_color(YELLOW)
        d = Difference(ellipse1, ellipse2, color=YELLOW, fill_opacity=0.5)
        self.play(Write(difference_text))
        self.play(Indicate(d))
        self.play(d.animate.scale(0.3).next_to(difference_text, DOWN))
        self.wait(2)

        
        