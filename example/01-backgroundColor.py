# This example is going to show you how to change the background color on the Canvas
from vispy import app, gloo

class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, size=(512,512), title='Background Color', keys='interactive')
        self.show()

    def on_draw(self, event):
        gloo.set_clear_color((0, 1.0, 1.0, 1.0)) # for changing the background color
        gloo.clear()

c = Canvas()
app.run()