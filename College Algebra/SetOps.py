from manim import *

class SetOps(Scene):
    def construct(self):
        ellipse1 = Ellipse(
            width=4.0, height=5.0, fill_opacity=0.5, color=BLUE, stroke_width=10
        ).move_to(LEFT)
        ellipse2 = ellipse1.copy().set_color(color=RED).move_to(RIGHT)
        set_ops_text = MarkupText("<u>Set Operation</u>").next_to(ellipse1, UP * 3)
        ellipse_group = Group(set_ops_text, ellipse1, ellipse2).move_to(LEFT * 3)
        self.play(FadeIn(ellipse_group))
        self.wait()

        # Intersection
        intersection_text = Text("Intersection", font_size=23).to_corner(UR)
        i = Intersection(ellipse1, ellipse2, color=GREEN, fill_opacity=0.5)
        self.play(Write(intersection_text))
        self.play(Indicate(i))
        self.play(i.animate.scale(0.3).next_to(intersection_text, DOWN))
        self.wait()

        # Union
        union_text = Text("Union", font_size=23).next_to(i, DOWN)
        u = Union(ellipse1, ellipse2, color=ORANGE, fill_opacity=0.5)
        self.play(Write(union_text))
        self.play(Indicate(u))
        self.play(u.animate.scale(0.3).next_to(union_text, DOWN))
        self.wait()

        # Exclusion
        exclusion_text = Text("Exclusion", font_size=23).next_to(u, DOWN)
        e = Exclusion(ellipse1, ellipse2, color=YELLOW, fill_opacity=0.5)
        self.play(Write(exclusion_text))
        self.play(Indicate(e))
        self.play(e.animate.scale(0.3).next_to(exclusion_text, DOWN))
        self.wait()
        
        