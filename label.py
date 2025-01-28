from manim import *

class label(Scene):
    def construct(self):
        # Create a vector
        vector = Arrow(start=ORIGIN, end=3*RIGHT + 2*UP, color=BLUE, buff=0)
        
        # Add the vector to the scene
        self.play(Create(vector))
        
        # Create the label
        label = MathTex("v", color=RED)
        
        # Position the label near the middle of the vector
        label.add_updater(lambda m: m.move_to(vector.get_center() + 0.3*UP))
        
        # Add the label to the scene
        self.add(label)
        
        # Optional animation to show vector movement
        self.play(vector.animate.shift(LEFT * 2 + DOWN))
        
        # Remove the updater to freeze the label
        label.clear_updaters()
        
        # End the scene
        self.wait()
