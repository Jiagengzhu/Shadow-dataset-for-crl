import bpy
import bpy_extras
import math
import mathutils
from itertools import product

def print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")

# point class with x, y as point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
 
def Left_index(points):
    minn = 0
    for i in range(1,len(points)):
        if points[i].x < points[minn].x:
            minn = i
        elif points[i].x == points[minn].x:
            if points[i].y > points[minn].y:
                minn = i
    return minn
 
def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - \
          (q.x - p.x) * (r.y - q.y)
 
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2
 
def convexHull(points, n, result):
     
    # There must be at least 3 points
    if n < 3:
        return
 
    # Find the leftmost point
    l = Left_index(points)
 
    hull = []
    p = l
    q = 0
    while(True):
         
        # Add current point to result
        hull.append(p)
 
        q = (p + 1) % n
 
        for i in range(n):
             
            # If i is more counterclockwise
            # than current q, then update q
            if(orientation(points[p],
                           points[i], points[q]) == 2):
                q = i
 
        p = q
 
        # While we don't come to first point
        if(p == l):
            break
 
    # Print Result
    for each in hull:
        #print("(" + str(points[each].x) + ", " + str(points[each].y) + ")")
        result.append(points[each])

# Shoelace formula to calculate the area of a polygon
# the points must be sorted anticlockwise (or clockwise)
def polygon_area(vertices):
    psum = 0
    nsum = 0

    for i in range(len(vertices)):
        sindex = (i + 1) % len(vertices)
        prod = vertices[i].x * vertices[sindex].y
        psum += prod

    for i in range(len(vertices)):
        sindex = (i + 1) % len(vertices)
        prod = vertices[sindex].x * vertices[i].y
        nsum += prod

    return abs(1/2*(psum - nsum))

def CreateCube(s):
    bpy.ops.mesh.primitive_cube_add(scale=(s, s, s))
    cube = bpy.context.object
    cube.name = 'target'
    cube.location = [0, 0, cube.dimensions.z/2]

def CreateSphere(s):
    bpy.ops.mesh.primitive_uv_sphere_add(scale=(s, s, s))
    sphere = bpy.context.object
    sphere.name = 'target'
    bpy.ops.object.shade_smooth()
    sphere.location = [0, 0, sphere.dimensions.z/2]

def CreateCylinder(s):
    bpy.ops.mesh.primitive_cylinder_add(scale=(s, s, s))
    cylinder = bpy.context.object
    cylinder.name = 'target'
    bpy.ops.object.modifier_add(type='EDGE_SPLIT')
    bpy.ops.object.modifier_add(type='SUBSURF')
    cylinder.modifiers['Subdivision'].levels = 3
    cylinder.location = [0, 0, cylinder.dimensions.z/2]

def CreateTetrahedron(s):
    bpy.ops.mesh.primitive_cone_add(vertices=3, depth=1.414213, scale=(2*s, 2*s, 2*s))
    tetra = bpy.context.object
    tetra.name = 'target'
    tetra.location = [0, 0, tetra.dimensions.z/2]

def CreateOctahedron(s):
    bpy.ops.mesh.primitive_cube_add(scale=(1.5*s, 1.5*s, 1.5*s))
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.bevel(offset=1.5*s)
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.mode_set(mode='OBJECT')
    octa = bpy.context.object
    octa.name = 'target'
    octa.location = [0, 0, octa.dimensions.z/2]

def CreateDodecahedron(s):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, scale=(2*s, 2*s, 2*s))
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.bevel(offset=0.6*s)
    bpy.ops.mesh.remove_doubles(threshold=0.001)
    bpy.ops.object.mode_set(mode='OBJECT')
    dodeca = bpy.context.object
    dodeca.name = 'target'
    dodeca.location = [0, 0, dodeca.dimensions.z/2]

def CreateIcosahedron(s):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, scale=(1.5*s, 1.5*s, 1.5*s))
    icosa = bpy.context.object
    icosa.name = 'target'
    icosa.location = [0, 0, icosa.dimensions.z/2]

def Generate(dataset):
    light = bpy.context.scene.objects["Light"]
    light.data.energy = 3000
    for data in dataset:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['target'].select_set(True)
        bpy.ops.object.delete()
        type = ''
        if(data[0] == 1):
            CreateCube(data[2])
            type = 'Cube'
        elif(data[0] == 2):
            CreateSphere(data[2])
            type = 'Sphere'
        elif(data[0] == 3):
            CreateCylinder(data[2])
            type = 'Cylinder'
        elif(data[0] == 4):
            CreateTetrahedron(data[2])
            type = 'Tetrahedron'
        elif(data[0] == 5):
            CreateOctahedron(data[2])
            type = 'Ocrahedron'
        elif(data[0] == 6):
            CreateDodecahedron(data[2])
            type = 'Dodecahedron'
        elif(data[0] == 7):
            CreateIcosahedron(data[2])
            type = 'Icosahedron'
        target = bpy.data.objects['target']
        target.data.materials.append(bpy.data.materials['Target_Material']);
        bpy.data.materials['Target_Material'].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = data[1][1]
        bpy.data.materials['Light_Material'].node_tree.nodes['Emission'].inputs['Color'].default_value = data[3][1]
        light.data.color.r = data[3][1][0]
        light.data.color.g = data[3][1][1]
        light.data.color.b = data[3][1][2]
        step = 1 #step<=8
        for k in range(int(8/step + 1)):
            light.location = [-4+k*step, -4+k*step, 8]
            brightest_point_global = [-4+k*step, -4+k*step, 0]
            brightest_point_camera = bpy_extras.object_utils.world_to_camera_view(bpy.data.scenes['Scene'], bpy.data.objects['Camera'], mathutils.Vector((brightest_point_global[0], brightest_point_global[1], 0.0)))
            points = []
            delete_points = []
            for j in range(len(target.data.vertices)):
                v_local = target.data.vertices[j].co # local vertex coordinate
                #print('local')
                print(v_local)
                v_global = target.matrix_world @ v_local # global vertex coordinates
                #print('global')
                #print(v_global)
                if(v_global.z <= 0.0001):
                    #print(v_global)
                    delete_point_camera = bpy_extras.object_utils.world_to_camera_view(bpy.data.scenes['Scene'], bpy.data.objects['Camera'], mathutils.Vector((v_global.x, v_global.y, 0.0)))
                    delete_points.append(Point(delete_point_camera.x*15, delete_point_camera.y*15))
                    #print("(" + str(v_global.x) + ", " + str(v_global.y) + ")")
                x = light.location.z * (v_global.x - light.location.x) / (light.location.z - v_global.z) + light.location.x
                y = light.location.z * (v_global.y - light.location.y) / (light.location.z - v_global.z) + light.location.y
                point_camera = bpy_extras.object_utils.world_to_camera_view(bpy.data.scenes['Scene'], bpy.data.objects['Camera'], mathutils.Vector((x, y, 0.0)))
                #print("(" + str(x) + ", " + str(y) + ")")
                points.append(Point(point_camera.x*15, point_camera.y*15))
            shadow = []
            delete = []
            convexHull(points, len(points), shadow)
            convexHull(delete_points, len(delete_points), delete)
            scene = bpy.context.scene
            scene.render.image_settings.file_format='PNG'
            scene.render.filepath='/Users/jiagengz/Documents/blender_scripts/sun-light-samples/datasets/' + type + '_' + data[1][0] + '_Size_' + str(data[2]) + '_LightPosition_' + str(k*step) + '_LightColor_' + data[3][0] + '_ShadowArea_' + str(format(polygon_area(shadow) - polygon_area(delete), '.3f')) + '_FloorColor_' + data[3][0] + '_Brightest_X_' + str(format(brightest_point_camera.x*15, '.3f')) + '_Y_' + str(format(brightest_point_camera.y*15, '.3f')) + '_RGB_ ' + str(data[3][2]) + '.png'
            bpy.ops.render.render(write_still=True)

bpy.context.scene.render.resolution_x = 256
bpy.context.scene.render.resolution_y = 256

types = [1, 2, 3, 4, 5, 6, 7]
target_colors = [('Red',(1,0,0,1)), ('Orange',(1,0.5,0,1)), ('Yellow',(1,1,0,1)), ('Green',(0,1,0,1)), ('Cyan',(0,1,1,1)), ('Blue',(0,0,1,1)), ('Purple',(0.5,0,1,1))]
scales = [0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
light_colors = [('SkyBlue',(0.5,1,1,1),(190,215,215)), ('Plum',(1,0.5,1,1),(215,190,215)), ('Khaki',(1,1,0.5,1),(215,215,190)), ('Lavender',(0.5,0.5,1,1),(190,190,215)), ('LightGreen',(0.5,1,0.5,1),(190,215,190)), ('Coral',(1,0.5,0.5,1),(215,190,190))]




types = [types[0]]
target_colors = [target_colors[0]]
scales = [scales[0]]
light_colors = [light_colors[0]]



dataset = list(product(types, target_colors, scales, light_colors))

Generate(dataset)

# Colors
# Red (1,0,0,1)
# Orange (1,0.5,0,1)
# Yellow (1,1,0,1)
# Green (0,1,0,1)
# Cyan (0,1,1,1)
# Blue (0,0,1,1)
# Purple (0.5,0,1,1)

# Light Colors
# SkyBlue (0.5,1,1,1)
# Plum (1,0.5,1,1)
# Khaki (1,1,0.5,1)
# Lavender (0.5,0.5,1,1)
# LightGreen (0.5,1,0.5,1)
# Coral (1,0.5,0.5,1)

# Brightest RGB
# SkyBlue (190,215,215)
# Plum (215,190,215)
# Khaki (215,215,190)
# Lavender (190,190,215)
# LightGreen (190,215,190)
# Coral (215,190,190)

#types = [1, 2, 3, 4, 5, 6, 7]
#target_colors = [('Red',(1,0,0,1)), ('Orange',(1,0.5,0,1)), ('Yellow',(1,1,0,1)), ('Green',(0,1,0,1)), ('Cyan',(0,1,1,1)), ('Blue',(0,0,1,1)), ('Purple',(0.5,0,1,1))]
#scales = [0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
#light_colors = [('SkyBlue',(0.5,1,1,1),(190,215,215)), ('Plum',(1,0.5,1,1),(215,190,215)), ('Khaki',(1,1,0.5,1),(215,215,190)), ('Lavender',(0.5,0.5,1,1),(190,190,215)), ('LightGreen',(0.5,1,0.5,1),(190,215,190)), ('Coral',(1,0.5,0.5,1),(215,190,190))]
