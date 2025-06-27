from manim import *
import random

class proj(ThreeDScene):
    def construct(self):
        # Create the 3D axes
        axes = ThreeDAxes()
        self.add(axes)

        vector_pairs = []

        for i in range(5):
            x = random.randint(-3,3)
            y = random.randint(-3,3)
            F_i = Vector(axes.c2p(x, y, 0), color=GREEN)
            S_i = Vector(axes.c2p(2-x, 1-y, 2), color=BLUE).shift(axes.c2p(x, y, 0))
            vector_pairs.append((F_i, S_i))

        # Mobjects
        y = Vector(axes.c2p(2, 1, 2))
        y_proj = Vector(axes.c2p(2, 1, 0), color=YELLOW)
        z = Vector(axes.c2p(0, 0, 2), color=BLUE)
        u = Vector(axes.c2p(2/np.sqrt(5), 1/np.sqrt(5), 0), color=RED).set_opacity(0)

        plane = Polygon(
            axes.c2p(10, 0, 0), axes.c2p(0, 10, 0), axes.c2p(-10, 0, 0), axes.c2p(0, -10, 0),
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=0.25,
            stroke_width=1
        )
        line = DashedLine(
            start = axes.c2p(-4, -2, 0),
            end = axes.c2p(4, 2, 0),
            color=RED,
            fill_opacity=0.25,
            stroke_width=2
        ).set_opacity(0)

        # Labels
        title = MathTex(r"\textbf{Orthogonal Projection}").to_edge(UR).scale(0.7)
        q1 = MathTex(r"\textbf{Q: What's the most efficient way} \\ \textbf{to reach} \,\, \mathbf{\vec{y}} \,\, \textbf{from the xy-plane?}").to_edge(LEFT+UP, buff=0).scale(0.65)
        a1 = MathTex(
            r"\textbf{A:} \,\,", 
            r"\textbf{Minimize} \,\,", 
            r"\textbf{the distance} \\",
            r"\textbf{between} \,\, \mathbf{\vec{y}} \,\, \textbf{and the} \,\,",
            r"\textbf{plane}").to_edge(LEFT+UP, buff=0).scale(0.65)
        a1[1].set_color(BLUE)
        a1[4].set_color(GREEN)
        a2 = MathTex(
            r"\textbf{A: Obtain a vector}", 
            r"\,\, \mathbf{\vec{z}} \\", 
            r"\textbf{orthogonal to} \,\,", 
            r"\mathbf{\hat{y}} \\",
            r"\textbf{where} \,\,",
            r"\mathbf{\hat{y}} \,\,",
            r"\textbf{lies on} \,\,",
            r"\mathbf{L} = \textbf{span}(\mathbf{\vec{u}})"
            ).to_edge(LEFT+UP, buff=0).scale(0.65)
        a2[1].set_color(BLUE)
        a2[3].set_color(YELLOW)
        a2[5].set_color(YELLOW)
        a2[7].set_color(RED)       
        y_def = MathTex(r"\vec{y} = \begin{bmatrix} 2 \\ 1 \\ 2 \end{bmatrix}").to_edge(LEFT).scale(0.7)
        y_label = MathTex(r"\mathbf{\vec{y}}").next_to(y.get_end(), UL, buff=0.25).scale(0.7)

        # Initialize scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(
            axes,
            #plane
        )
        self.add_fixed_in_frame_mobjects(title)
        self.wait()

        self.play(
            Create(y),
        )
        self.add_fixed_in_frame_mobjects(
            #y_def, 
            y_label
        )
        self.wait()

        self.play(
            FadeIn(plane)
        )
        self.wait()

        self.add_fixed_in_frame_mobjects(q1)
        self.wait(2)        

        for (F_i, S_i) in vector_pairs:
            self.play(
                FadeIn(F_i), 
                FadeIn(S_i),
                run_time=1
            )
            self.play(
                FadeOut(F_i),
                S_i.animate.shift(-F_i.get_end()),
                run_time=1
            )
        self.wait()

        q1.set_opacity(0)
        self.add_fixed_in_frame_mobjects(a1)
        self.wait(2)

        s_vectors = [s for _, s in vector_pairs]
        self.play(
            FadeOut(*s_vectors),
        )
        self.wait()

        self.play(
            ReplacementTransform(y.copy(), y_proj),
        )
        self.wait()

        self.play(
            FadeIn(z.shift(y_proj.get_end()))
        )
        self.wait()

        a1.set_opacity(0)
        z_label = MathTex(r"\mathbf{\vec{z}}", color=BLUE).next_to(z.get_end(), DR, buff=0.5).scale(0.7)
        y_proj_label = MathTex(r"\mathbf{\hat{y}}", color=YELLOW).next_to(y_proj.get_end(), 5*DOWN).scale(0.7)
        self.add_fixed_in_frame_mobjects(a2, z_label, y_proj_label)
        self.wait(3)

        u_label = MathTex(r"\mathbf{\vec{u}}", color=RED).next_to(y_proj.get_center(), 3*DOWN+LEFT).scale(0.7)
        self.play(
            FadeOut(plane),
            u.animate.set_opacity(1),
            line.animate.set_opacity(1),
        )
        self.add_fixed_in_frame_mobjects(u_label)
        self.wait(3)

        a2.set_opacity(0)
        line.set_opacity(0)
        v_group = VGroup(y, y_proj, z, u)
        label_group = VGroup(y_label, y_proj_label, z_label, u_label)
        label_group.set_opacity(0)
        self.play(
            axes.animate.shift(2*DL),
            v_group.animate.shift(2*DL),
            run_time=1
        )
        self.wait()

        # Derivation MathTex
        eq1 = MathTex(
            r"\textbf{We have} \,\,", 
            r"\mathbf{\vec{y}} = ", 
            r"\textbf{proj}_{\mathbf{L}}\mathbf{\vec{y}}", 
            r"+", 
            r"\mathbf{\vec{z}}"
            ).scale(0.7)
        eq1[2].set_color(YELLOW)
        eq1[4].set_color(BLUE)
        eq1.next_to(title, DOWN, buff=0.3)

        eq2 = MathTex(
            r"\textbf{Also} \,\,", 
            r"\textbf{proj}_{\mathbf{L}}\mathbf{\vec{y}}",
            r"=",
            r"\mathbf{\alpha}",
            r"\mathbf{\vec{u}}",
            r"\,\, \textbf{and} \,\,",
            r"\mathbf{\vec{z}}",
            r"\perp",
            r"\mathbf{\vec{u}}",
            ).scale(0.7)
        eq2[1].set_color(YELLOW)
        eq2[3].set_color(YELLOW)
        eq2[4].set_color(RED)
        eq2[6].set_color(BLUE)
        eq2[8].set_color(RED)
        eq2.next_to(eq1, DOWN, buff=0.3)

        eq3 = MathTex(
            r"\textbf{Then} \,\,",
            r"(",
            r"\mathbf{\vec{y}}",
            r"-",
            r"\mathbf{\alpha}",
            r"\mathbf{\vec{u}}",
            r")",
            r"\cdot",
            r"\mathbf{\vec{u}}",
            r"= 0"
            ).scale(0.7)
        eq3[4].set_color(YELLOW)
        eq3[5].set_color(RED)
        eq3[8].set_color(RED)
        eq3.next_to(eq2, DOWN, buff=0.3)

        eq4 = MathTex(
            r"\textbf{And so} \,\,",
            r"\mathbf{\vec{y}}",
            r"\cdot",
            r"\mathbf{\vec{u}}",
            r"-",
            r"\mathbf{\alpha}",
            r"\mathbf{\vec{u}}",
            r"\cdot",
            r"\mathbf{\vec{u}}",
            r"= 0"
            ).scale(0.7)
        eq4[3].set_color(RED)
        eq4[5].set_color(YELLOW)
        eq4[6].set_color(RED)
        eq4[8].set_color(RED)
        eq4.next_to(eq3, DOWN, buff=0.3)

        eq5 = MathTex(
            r"\textbf{Or} \,\,",
            r"\mathbf{\alpha}",
            r"\mathbf{\vec{u}}",
            r"\cdot",
            r"\mathbf{\vec{u}}",
            r"=",
            r"\mathbf{\vec{y}}",
            r"\cdot",
            r"\mathbf{\vec{u}}"
            ).scale(0.7)
        eq5[1].set_color(YELLOW)
        eq5[2].set_color(RED)
        eq5[4].set_color(RED)
        eq5[8].set_color(RED)
        eq5.next_to(eq4, DOWN, buff=0.3)

        eq6 = MathTex(
            r"\textbf{Which implies} \,\,",
            r"\mathbf{\alpha}",
            r"=",
            r"\frac{\mathbf{\vec{y}} \cdot \mathbf{\vec{u}}}{\mathbf{\vec{u}} \cdot \mathbf{\vec{u}}}",
            ).scale(0.7)
        eq6[1].set_color(YELLOW)
        eq6.next_to(eq5, DOWN, buff=0.3)

        eq7 = MathTex(
            r"\textbf{And so} \,\,",
            r"\textbf{proj}_{\mathbf{L}}\mathbf{\vec{y}}",
            r" = \frac{\mathbf{\vec{y}} \cdot \mathbf{\vec{u}}}{\mathbf{\vec{u}} \cdot \mathbf{\vec{u}}}",
            r"\mathbf{\vec{u}}"
            ).scale(0.7)
        eq7[1].set_color(YELLOW)
        eq7.next_to(eq6, DOWN, buff=0.3)

        equations = [eq1, eq2, eq3, eq4, eq5, eq6, eq7]
        for eq in equations:
            self.add_fixed_in_frame_mobjects(eq)
            self.play(FadeIn(eq), run_time=4)
        self.wait(3)