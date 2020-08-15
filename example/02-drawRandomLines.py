# This example is going to show you how to draw some random lines on the Canvas
from vispy import app, gloo
import numpy as np

vertex = """
attribute vec2 a_position;
void main(void)
{
    gl_Position = vec4(a_position, 0.0, 1.0);
}
"""

# Change line color here
fragment = """
void main()
{
    gl_FragColor = vec4(0.0, 1.0, 1.0, 1.0);
}
"""

class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, size=(800,400), title='Draw Random Lines', keys='interactive')

        self.program = gloo.Program(vert=vertex, frag=fragment)
        pointNum = 10
        data = np.c_[
            np.linspace(-1, 1, pointNum),
            np.random.uniform(-0.5, +0.5, pointNum)]
        print("coordinate of these random 10 vertices:")
        print(data)

        # gloo needs 32bit
        self.program['a_position'] = data.astype('float32') # a_ means that this is an attribute
        self.show()

    def on_draw(self, event):
        gloo.set_clear_color((0.0, 0.0, 0.0, 1.0))
        gloo.clear()
        self.program.draw('line_strip')
        # The draw function determine that what we are going to draw, likes line, triangle and others

c = Canvas()
app.run()