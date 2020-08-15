# This example is going to show you how to draw some random lines on the Canvas
from vispy import app, gloo, io
import numpy as np
from vispy.geometry import MeshData
from vispy.util.transforms import translate, perspective, rotate

vertex = """
uniform mat4   u_model;         // Model matrix
uniform mat4   u_view;          // View matrix
uniform mat4   u_projection;    // Projection matrix

uniform vec4   u_color;
attribute vec3 a_position;
attribute vec4 a_color;
varying vec4 v_color;
void main(void)
{
    gl_Position = u_projection * u_view * u_model * vec4(a_position * 0.7, 1.0);
    v_color = a_color * u_color;
}
"""

# Change line color here
fragment = """
varying vec4 v_color;
void main()
{
    gl_FragColor = v_color;
}
"""

class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, size=(512,512), title='Monkey', keys='interactive')
        verts, faces, normals, texcoords = io.read_mesh("./monkey.obj")
        obj = MeshData(verts, faces)

        self.program = gloo.Program(vert=vertex, frag=fragment)

        V = verts.astype('float32')

        F = obj.get_faces().astype('uint32')

        E = obj.get_edges().astype('uint32')

        C = np.array([(1, 1, 1, 1)])
        for i in range(len(V)-1):
            if i % 2 != 0 :
                C = np.append(C, [(1, 1, 1, 1)], axis=0)
            else:
                C = np.append(C, [(0, 0, 0, 1)], axis=0)

        self.program['a_position'] = V
        self.program['a_color'] = C.astype('float32')
        self.F = gloo.IndexBuffer(F)
        self.E = gloo.IndexBuffer(E)

        gloo.set_viewport(0, 0, *self.physical_size)
        gloo.set_polygon_offset(1.0, 1.0)

        # intialize transformation matrix
        view = np.eye(4, dtype=np.float32)
        model = np.eye(4, dtype=np.float32)
        projection = np.eye(4, dtype=np.float32)

        # set view
        view = translate((0, 0, -5))
        self.program['u_model'] = model
        self.program['u_view'] = view
        self.program['u_projection'] = projection

        # bind a timer
        self.timer = app.Timer('auto', self.on_timer)
        self.theta = 0.0
        self.phi = 0.0
        self.timer.start()

        # show the canvas
        self.show()

    def on_resize(self, event):
        """ canvas resize callback """
        ratio = event.physical_size[0] / float(event.physical_size[1])
        self.program['u_projection'] = perspective(45.0, ratio, 2.0, 10.0)
        gloo.set_viewport(0, 0, *event.physical_size)

    def on_draw(self, event):
        """ canvas update callback """
        gloo.set_clear_color((0.0, 0.0, 0.0, 1.0))
        gloo.clear()
        # Filled cube
        gloo.set_state(blend=True, depth_test=True,
                       polygon_offset_fill=True)
        self.program['u_color'] = [1.0, 1.0, 1.0, 0.8]
        self.program.draw('triangles', self.F)

        # draw outline
        gloo.set_state(blend=True, depth_test=True,
                       polygon_offset_fill=True)
        self.program['u_color'] = [1.0, 1.0, 1.0, 1.0]
        self.program.draw('lines', self.E)
        # The draw function determine that what we are going to draw, likes line, triangle and others

    def on_timer(self, event):
        """ canvas time-out callback """
        self.theta += .5
        self.phi += .2
        # note the convention is, theta is applied first and then phi
        # see vispy.utils.transforms,
        # python is row-major and opengl is column major,
        # so the rotate function transposes the output.
        model = np.dot(rotate(self.theta, (0, 1, 0)),
                       rotate(self.phi, (0, 0, 1)))
        self.program['u_model'] = model
        self.update()

c = Canvas()
app.run()