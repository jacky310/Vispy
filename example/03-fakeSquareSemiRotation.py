# This example is going to show you how to make a square and create a timer for scaling it
from vispy import gloo, app
import numpy as np

vertex = """
uniform float scale;
attribute float a_x_position;
attribute float a_y_position;
attribute vec4 color;
varying vec4 v_color;
void main(void)
{
    gl_Position = vec4(a_x_position * scale, a_y_position, 0.0, 1.0);
    v_color = color;
}
"""

fragment = """
varying vec4 v_color;
void main()
{
    gl_FragColor = v_color;
}
"""

class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, size=(512,512), title='Fake Square Semi-Rotation', keys='interactive')

        # program with 4 vertices
        self.program = gloo.Program(vert=vertex, frag=fragment, count=4)

        self.program['a_x_position'] = [-1, -1, 1, 1]
        self.program['a_y_position'] = [-1, 1, -1, 1]
        self.program['color'] = [(1, 1, 1, 1), # for (-1, -1)
                                 (0, 1, 1, 1), # for (-1, 1)
                                 (1, 1, 0, 1), # for (1, -1)
                                 (0, 0, 0, 1)] # for (1, 1)
        self.program['scale'] = 0.0
        # bind a timer
        self.timer = app.Timer('auto', self.on_timer)
        self.clock = 0.0
        self.timer.start()

        self.show()

    def on_draw(self, event):
        gloo.set_clear_color((0.0, 0.0, 0.0, 1.0)) # for changing the background color
        gloo.clear()
        self.program.draw('triangle_strip') # draw triangle

    def on_timer(self, event):
        """ canvas time-out callback """
        self.clock += 0.01 * np.pi
        self.program['scale'] = 0.2 + 0.5 * np.cos(self.clock)
        self.update()

c = Canvas()
app.run()
