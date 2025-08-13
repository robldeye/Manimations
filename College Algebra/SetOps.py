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
        union_text = MathTex(r"\text{Union: }", r"A \cup B").next_to(i, 2*DOWN)
        union_text[1].set_color(ORANGE)
        u = Union(ellipse1, ellipse2, color=ORANGE, fill_opacity=0.5)
        self.play(Write(union_text))
        self.play(Indicate(u))
        self.play(u.animate.scale(0.3).next_to(union_text, DOWN))
        self.wait()

        # Difference
        difference_text = MathTex(r"\text{Difference: }", r"A - B").next_to(u, 2*DOWN)
        difference_text[1].set_color(YELLOW)
        d = Difference(ellipse1, ellipse2, color=YELLOW, fill_opacity=0.5)
        self.play(Write(difference_text))
        self.play(Indicate(d))
        self.play(d.animate.scale(0.3).next_to(difference_text, DOWN))
        self.wait(3)

        # Clear screen
        self.play(FadeOut(ellipse_group, ellipse1_label, ellipse2_label, intersection_text, i, union_text, u, difference_text, d))
        
        # Subsets and Complements
        universal = Rectangle(color=GREY, height=6, width=8, fill_opacity=0.25).to_edge(LEFT)
        B2 = Ellipse(width=3, height=4, fill_opacity=0.5, color=RED, stroke_width=10).next_to(universal.get_left())
        B2_label = MathTex(r"B").next_to(B2.get_corner(UR), UR)
        A2 = Ellipse(width=2, height=2, fill_opacity=0.5, color=BLUE, stroke_width=10).next_to(B2.get_left())
        A2.set_z_index(1)
        A2_label = MathTex(r"A").move_to(A2.get_center())
        universal_label = MathTex(r"U").next_to(universal.get_corner(DL), UR)
        self.play(FadeIn(universal, universal_label))
        self.play(FadeIn(B2, B2_label, A2, A2_label))
        self.wait()

        # Subsets
        subset_text1 = MathTex(r"A", r"\subset", r"B", r",").to_corner(UR, buff=1)
        subset_text1[0].set_color(BLUE)
        subset_text1[2].set_color(RED)
        self.play(Write(subset_text1), run_time=1)
        subset = A2.copy()
        self.play(Indicate(subset))
        self.wait(0.5)
        self.play(Indicate(B2))
        self.wait(0.5)
        self.play(subset.animate.become((Difference(A2, B2, color=YELLOW, fill_opacity=0.5))).scale(0.3).next_to(subset_text1, DOWN))
        subset_text2 = MathTex(r"\underline{\text{...since } A-B=\varnothing.}").next_to(subset, DOWN).align_to(subset_text1, RIGHT)
        self.play(Write(subset_text2), run_time=1)
        self.wait(2)

        not_subset_text = MathTex(r"B", r"\not \subset", r"A").next_to(subset_text2, 3*DOWN).align_to(subset_text1, RIGHT)
        not_subset_text[0]
        not_subset_text[2]
        self.play(Write(not_subset_text), run_time=1)
        not_subset = B2.copy()
        self.play(Wiggle(not_subset))
        self.play(not_subset.animate.become((Difference(B2, A2, color=YELLOW, fill_opacity=0.5))).scale(0.3).next_to(not_subset_text, DOWN))
        not_subset_text2 = MathTex(r"\underline{\text{...since } B-A \neq \varnothing.}").next_to(not_subset, DOWN).align_to(subset_text1, RIGHT)
        self.play(Write(not_subset_text2), run_time=1)
        self.wait(2)

        complement_text = MathTex(r"\text{Complement: }", r"B'").next_to(not_subset_text2, 3*DOWN).align_to(subset_text1, RIGHT)
        complement_text[1].set_color(GRAY)
        self.play(Write(complement_text), run_time=1)
        complement = Difference(universal, B2, color=GRAY, fill_opacity=0.5)
        self.play(Indicate(complement))
        self.wait(0.5)
        self.play(complement.animate.scale(0.2).next_to(complement_text, DOWN).align_to(subset_text1, RIGHT))
        self.wait()
        

        self.wait(2)
        
        