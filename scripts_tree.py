import os, math
import cairo
import tree_manipulator as tr
from my_globals import *

test_tree = os.path.join(amato_qiime_root,'firmicutes-tenericutes-only.tre')
test_tree = amato_qiime_tree
tre = tr.Radial_Phylogram(test_tree)

image_path = 'resources/temp.png'

WIDTH, HEIGHT = 800, 600
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)
ctx.set_source_rgb(1, 1, 1)
ctx.rectangle(0, 0, WIDTH, HEIGHT)
ctx.fill()

# ctx.set_line_width(.001)
ctx.set_source_rgb(0, 0, 0)
max_dims = tre.get_max_dims()
print max_dims
sc_x = float(WIDTH)/(max_dims[1]-max_dims[0])
sc_y = float(HEIGHT)/(max_dims[3]-max_dims[2])
sc = min(sc_x,sc_y)
ctx.scale(sc,sc)
ctx.translate(-max_dims[0],-max_dims[2])
# ctx.translate(-max_dims[0],-max_dims[2])

# ctx.set_line_width(float(WIDTH)/500.0)
# print ctx.device_to_user(0,0)
# print ctx.device_to_user(WIDTH,HEIGHT)
# print ctx.device_to_user( 0,HEIGHT)
# print ctx.device_to_user( WIDTH,0)
# print "\n"
a=ctx.get_matrix()
print a

ang = 0
ctx.rotate(float(ang)/180.0*math.pi)
# a.init_rotate(float(ang)/180.0*math.pi)
# ctx.set_matrix(a)

ct = 0
for i in tre.myt.postorder_edge_iter():
    if i.viewer_edge is not None:
        x0 = i.viewer_edge.head_x
        x1 = i.viewer_edge.tail_x
        ctx.move_to(*x0)
        ctx.line_to(*x1)

ctx.set_line_width(.002)
ctx.stroke()

# ctx.set_source_rgb(1,0,0)
# for i in tre.myt.preorder_node_iter():
#     if i.viewer_node is not None:
#         x = i.viewer_node.ts_x
#         ctx.new_sub_path()
#         ctx.arc(x[0],x[1],.005,0,2*math.pi)
#         ctx.fill()

    # if ct > 50:
    #     break
surface.write_to_png(image_path)