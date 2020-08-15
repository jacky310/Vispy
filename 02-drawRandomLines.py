# This example is going to show you how to change the background color on the Canvas
from vispy import app, gloo
import numpy as np

vertex = """
attribute vec2 line_position;
void main(void)
{
    gl_Position = vec4(line_position, 0.0, 1.0);
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
        app.Canvas.__init__(self, size=(512,512), title='Draw Random Line', keys='interactive')

        self.program = gloo.Program(vert=vertex, frag=fragment)
        pointNum = 10
        data = np.c_[
            np.linspace(-1, 1, pointNum),
            np.random.uniform(-0.5, +0.5, pointNum)]
        print("coordinate of these random 10 vertices:")
        print(data)

        # gloo needs 32bit
        self.program['line_position'] = data.astype('float32')
        self.show()

    def on_draw(self, event):
        gloo.set_clear_color((0.0, 0.0, 0.0, 1.0))
        gloo.clear()
        self.program.draw('line_strip')

c = Canvas()
app.run()